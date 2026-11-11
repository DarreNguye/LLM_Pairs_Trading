from AlgorithmImports import *
"""Pure-Python core of the pairs backtester (no LEAN imports, so it can be unit-tested offline).

Per pair:  PairModel  -> signal (rolling hedge ratio, z-score, entry/exit state machine)
           PairBook   -> isolated P&L ledger built from actual fills
           PairEngine -> glue: turns bars into orders, routes fills back
Timing contract: on_bar() is called with CLOSE prices of day t; the orders it returns
must be filled no earlier than the OPEN of day t+1. Nothing here reads future data.
"""
import math
from collections import deque
from dataclasses import dataclass

import numpy as np
from statsmodels.tsa.stattools import coint


@dataclass
class Params:

    # Trading Parameters
    beta_lookback: int = 252     # days used to estimate the hedge ratio
    z_lookback: int = 60         # days used for the spread mean / std
    entry_z: float = 2.0
    exit_z: float = 0.5          # exit when the spread is back within this many sigmas of the mean
    stop_z: float = 4.0
    max_hold_days: int = 60      # trading days
    gross_leverage: float = 1.0  # long notional + short notional, as a multiple of the pair's capital
    borrow_rate: float = 0.01    # annual fee on short market value

    # Entry / Exit Logic
    entry_mode: str = "cross"    # "cross" = enter when |z| first crosses entry_z; "reentry" = wait for z to turn back inside entry_z
    unblock_z: float = 0.5       # after a stop, allow entries again once |z| is within this (separate from exit_z so exit_z = 0 still unblocks)

    # Mean-Reversion Filters (Chan ch. 2)
    coint_pvalue: float = 0.1   # CADF gate: enter only if trailing p-value is below this (1.0 = off)
    min_half_life: float = 5.0   # skip spreads that revert too fast to beat costs (days)
    max_half_life: float = 60.0  # skip spreads that revert too slowly to trade (days)
    hl_z_mult: float = 1.0       # >0: z window = this x half-life; 0 = fixed z_lookback
    hl_hold_mult: float = 3.0    # >0: time stop = this x half-life at entry; 0 = fixed max_hold_days

    def validate(self):
        '''Validation for parameters'''
        assert self.beta_lookback >= self.z_lookback >= 20, "need beta_lookback >= z_lookback >= 20"
        assert 0 <= self.exit_z < self.entry_z < self.stop_z, "need exit_z < entry_z < stop_z"
        assert self.max_hold_days >= 1 and self.gross_leverage > 0 and self.borrow_rate >= 0
        assert 0 < self.coint_pvalue <= 1, "need 0 < coint_pvalue <= 1"
        assert 0 < self.min_half_life < self.max_half_life, "need 0 < min_half_life < max_half_life"
        assert self.hl_z_mult >= 0 and self.hl_hold_mult >= 0, "half-life multipliers must be >= 0"
        assert self.entry_mode in ("cross", "reentry"), "entry_mode must be 'cross' or 'reentry'"
        assert 0 < self.unblock_z < self.entry_z, "need 0 < unblock_z < entry_z"

# Validates prices
def _ok(p):
    return p is not None and isinstance(p, (int, float)) and math.isfinite(p) and p > 0


class PairModel:
    """Spread = log(A) - beta*log(B).  direction +1 = long A / short B, -1 = the reverse."""

    def __init__(self, params: Params):
        '''Setup rolling windows for log prices'''
        self.p = params
        self.la = deque(maxlen=params.beta_lookback)
        self.lb = deque(maxlen=params.beta_lookback)
        self.direction = 0
        self.blocked = False      # set after a stop-out; cleared once the spread normalises
        self.armed = 0            # Reentry mode only; side (+1/-1) of z after it pushed past entry_z, 0 = not armed
        self.days_held = 0
        self.entry = None         # frozen (beta, mu, sigma) of the open trade
        self.z = float("nan")
        self.beta = float("nan")

        # Mean-reversion diagnostics
        self.half_life = float("nan")                  # latest half-life of the spread (days)
        self.pvalue = float("nan")                     # latest CADF p-value (only computed on entry signals)
        self.hold_limit = params.max_hold_days        # time stop for the open trade, set at entry
        self.filtered = {"half_life": 0, "cadf": 0}    # entry signals rejected by each filter (counted per day)

    @property
    def ready(self):
        '''True when enough stored data of prices'''
        return len(self.la) == self.p.beta_lookback

    def push(self, pa, pb):
        '''Add today's log prices to rolling windows'''
        self.la.append(math.log(pa))
        self.lb.append(math.log(pb))
        if self.direction != 0:
            self.days_held += 1

    def _stats(self):
        '''Regresses log(A) on log(B) and returns mean and standard deviation of spread.
        Also updates self.half_life using the full beta window'''

        # Set up 
        a, b = np.asarray(self.la), np.asarray(self.lb)
        var_b = np.var(b, ddof=1)
        if not var_b > 0:
            return None

        # Regression
        beta = float(np.cov(a, b, ddof=1)[0, 1] / var_b)
        if not math.isfinite(beta):
            return None

        # Half-life of the spread over the full beta window
        self.half_life = self._half_life(a - beta * b)

        # Pick z window: fixed, or scaled to half-life if enabled (clamped to [20, beta_lookback])
        n = self.p.z_lookback
        if self.p.hl_z_mult > 0 and math.isfinite(self.half_life):
            n = min(max(int(round(self.p.hl_z_mult * self.half_life)), 20), self.p.beta_lookback)

        # Calculate spread
        s = a[-n:] - beta * b[-n:]
        sd = float(np.std(s, ddof=1))
        if not sd > 1e-12:
            return None
        return beta, float(np.mean(s)), sd

    @staticmethod
    def _half_life(s):
        '''Regresses daily change in spread on yesterday's spread; half-life = -ln(2) / slope'''
        lag, ds = s[:-1], np.diff(s)
        var_lag = np.var(lag, ddof=1)
        if not var_lag > 0:
            return float("inf")
        lam = float(np.cov(ds, lag, ddof=1)[0, 1] / var_lag)

        # Slope must be negative (pulled back to mean); otherwise it never reverts
        return -math.log(2) / lam if lam < 0 else float("inf")

    def _passes_filters(self):
        '''Checks half-life range, then CADF p-value on the trailing beta window (no future data)'''

        # Half-life must be in a tradeable range (cheap check first)
        if not (self.p.min_half_life <= self.half_life <= self.p.max_half_life):
            self.filtered["half_life"] += 1
            return False

        # CADF (Engle-Granger): regress log(A) on log(B), then ADF on the residual
        # with cointegration critical values (stricter than plain ADF since beta is estimated)
        if self.p.coint_pvalue < 1:
            try:
                self.pvalue = float(coint(np.asarray(self.la), np.asarray(self.lb), trend="c")[1])
            except Exception:
                self.pvalue = float("nan")
            if not self.pvalue < self.p.coint_pvalue:
                self.filtered["cadf"] += 1
                return False
        return True

    def decide(self):
        """Return None, ('enter', direction) or ('exit', reason). Call after push()."""

        # If not ready
        if not self.ready:
            return None

        # Check exit conditions
        if self.direction != 0:

            # Caluate z score (frozen z score for exit)
            beta, mu, sd = self.entry
            self.z = (self.la[-1] - beta * self.lb[-1] - mu) / sd

            # Check if stop, target, or time condition triggered
            adverse = self.direction * self.z
            if adverse <= -self.p.stop_z:
                return self._exit("stop", block=True)
            if adverse >= -self.p.exit_z:
                return self._exit("target")
            if self.days_held >= self.hold_limit:
                return self._exit("time")
            return None

        # Pull mean and std of spread
        st = self._stats()
        if st is None:
            self.z = float("nan")
            return None
        beta, mu, sd = st
        self.beta = beta

        # Calculate z score (rolling z score for entry)
        self.z = (self.la[-1] - beta * self.lb[-1] - mu) / sd

        # Check if z score fell within acceptable threshold to unblock
        if self.blocked:
            self.armed = 0
            if abs(self.z) <= self.p.unblock_z:
                self.blocked = False
            return None

        # Never trade negative hedge ratio (which is long or short both)
        if beta <= 0:
            self.armed = 0
            return None

        # If z is too high, direction -1 (short A, long B)
        # If z is too low, direction +1 (long A, short B)
        if self._entry_signal():

            # Only enter if the spread is currently mean-reverting (run last since CADF is the slow step)
            if not self._passes_filters():
                return None

            self.direction = -1 if self.z > 0 else 1
            self.entry = st
            self.days_held = 0

            # Set time stop: fixed scaled to half-life and capped at the max hold days
            self.hold_limit = self.p.max_hold_days
            if self.p.hl_hold_mult > 0:  
                self.hold_limit = min(self.p.max_hold_days, max(1, int(round(self.p.hl_hold_mult * self.half_life))))
            return ("enter", self.direction)
        return None

    def _entry_signal(self):
        '''True on the bar to enter, per entry_mode. Uses only today's and earlier z (no future data)'''
        az = abs(self.z)

        # Cross mode (original rule): enter as soon as |z| is between entry_z and stop_z
        if self.p.entry_mode == "cross":
            return self.p.entry_z <= az < self.p.stop_z

        # Reentry mode: arm when |z| pushes past entry_z, enter when it turns back inside on the same side
        side = 1 if self.z > 0 else -1
        if az >= self.p.stop_z:                          # blew through the stop level: disarm, don't catch it
            self.armed = 0
            return False
        if az >= self.p.entry_z:                         # still stretched: arm and wait for the turn
            self.armed = side
            return False
        if self.armed == side and az > self.p.exit_z:    # turned back inside entry_z: enter
            self.armed = 0                               # If the filters then reject, this excursion is skipped
            return True
        self.armed = 0                                   # crossed the mean, or gapped straight to the exit band
        return False

    def _exit(self, reason, block=False):
        '''Closes out and blocks re-entry until z score falls back'''
        self.reset()
        self.blocked = block
        return ("exit", reason)

    def reset(self):
        '''Clears'''
        self.direction, self.entry, self.days_held = 0, None, 0
        self.armed = 0

    def target_shares(self, capital, pa, pb):
        """Dollar weights proportional to (1, -beta): the hedge implied by a log-price spread."""
        beta = self.entry[0]
        gross = capital * self.p.gross_leverage
        qa = int(self.direction * gross / (1 + beta) / pa)
        qb = int(-self.direction * gross * beta / (1 + beta) / pb)
        return qa, qb


class PairBook:
    """P&L ledger for one pair. equity == cumulative net P&L (starts at 0)."""

    def __init__(self, capital, borrow_rate, borrow_rate_b=None):
        self.capital = capital
        # Per-leg borrow rates (hard-to-borrow names cost more); leg B defaults to leg A's rate
        self.borrow_rate_a = borrow_rate
        self.borrow_rate_b = borrow_rate if borrow_rate_b is None else borrow_rate_b
        self.qa = self.qb = 0
        self.cash = 0.0
        self.fees = self.borrow = 0.0
        self.dates, self.equity, self.in_market = [], [], []
        self.trades, self.cur = [], None
        self._last = None   # (date, pa, pb) of the previous mark

    def open_trade(self, date, direction, beta, z):
        '''Record new trade detail'''
        self.cur = dict(entry_date=date, direction=direction, beta=beta, entry_z=z,
                        cash0=self.cash, filled=False, exit_date=None, reason=None, days=None)

    def note_exit(self, date, reason, days):
        '''Note exit date, reason for exiting, and days held for open trade'''
        if self.cur:
            self.cur.update(exit_date=date, reason=reason, days=days)
            self._maybe_close()

    def discard_trade(self):
        '''Throw away the trade record'''
        self.cur = None

    def on_fill(self, leg, qty, price, fee):
        '''Update share count, cash, and fee when order filled'''
        if leg == "a":
            self.qa += qty
        else:
            self.qb += qty
        self.cash -= qty * price + fee
        self.fees += fee
        if self.cur:
            self.cur["filled"] = True
            self._maybe_close()

    def _maybe_close(self):
        '''Finalizes a trade in the book with P&L'''
        c = self.cur
        if c and c["filled"] and c["exit_date"] is not None and self.qa == 0 and self.qb == 0:
            c["pnl"] = self.cash - c.pop("cash0")
            c.pop("filled")
            self.trades.append(c)
            self.cur = None

    def mark(self, date, pa, pb):
        '''Charge borrow costs on shorts and record equity and if a position is open'''
        if self._last is not None:   # borrow accrues on the short held since the previous mark
            d0, pa0, pb0 = self._last
            short_cost_rate = max(-self.qa, 0) * pa0 * self.borrow_rate_a + max(-self.qb, 0) * pb0 * self.borrow_rate_b
            cost = short_cost_rate * (date - d0).days / 360.0
            self.cash -= cost
            self.borrow += cost
        self._last = (date, pa, pb)
        self.dates.append(date)
        self.equity.append(self.cash + self.qa * pa + self.qb * pb)
        self.in_market.append(self.qa != 0 or self.qb != 0)


class PairEngine:
    def __init__(self, name, params: Params, capital, borrow_rates=None):
        params.validate()
        self.name, self.capital = name, capital
        self.model = PairModel(params)
        ra, rb = borrow_rates if borrow_rates else (params.borrow_rate, params.borrow_rate)   # (leg A, leg B) annual borrow
        self.book = PairBook(capital, ra, rb)
        self.pending = 0        # orders submitted and not yet finished
        self.rejected = 0
        self.skipped_bars = 0
        self.dead = False       # Set when a leg delists; the pair is closed and never re-entered

    def warm(self, pa, pb):
        '''Feeds prestart prices into the model'''
        if _ok(pa) and _ok(pb):
            self.model.push(pa, pb)

    def on_bar(self, date, pa, pb):
        """Close prices in -> list of (leg, signed_shares) to send for the next open."""
        if not (_ok(pa) and _ok(pb)):
            self.skipped_bars += 1
            return []
        self.book.mark(date, pa, pb)
        if self.dead:           # Closed for good after a delisting; keep marking, never trade
            return []
        self.model.push(pa, pb)
        if self.pending > 0:    # never stack decisions on unfilled orders
            return []
        m, b = self.model, self.book
        if m.direction != 0 and (b.qa == 0 or b.qb == 0):   # an entry leg was rejected
            days = m.days_held
            m.reset()
            if b.qa == 0 and b.qb == 0:
                b.discard_trade()
                return []
            b.note_exit(date, "broken_leg", days)
            return self._flatten()
        days = m.days_held
        act = m.decide()
        if act is None:
            return []
        if act[0] == "enter":
            qa, qb = m.target_shares(self.capital, pa, pb)
            if qa == 0 or qb == 0:
                m.reset()
                return []
            b.open_trade(date, act[1], m.entry[0], m.z)
            self.pending = 2
            return [("a", qa), ("b", qb)]
        b.note_exit(date, act[1], days)
        return self._flatten()

    def _flatten(self):
        '''Builds orders to close out positions'''
        orders = [(leg, -q) for leg, q in (("a", self.book.qa), ("b", self.book.qb)) if q != 0]
        self.pending = len(orders)
        return orders

    def on_fill(self, leg, qty, price, fee, final=True):
        '''Passes a filled order to ledger and marks order done'''
        self.book.on_fill(leg, qty, price, fee)
        if final:
            self.pending -= 1

    def on_order_dead(self):
        '''Marks a rejected or canceled order done'''
        self.pending -= 1
        self.rejected += 1

    def force_exit(self, date, reason="delisted"):
        '''Close the pair now (e.g. a leg is about to delist) and stop trading it.
        Returns flatten orders. Positions still in flight from unfilled orders are not covered.'''
        self.dead = True
        m, b = self.model, self.book
        days = m.days_held
        m.reset()
        if b.qa == 0 and b.qb == 0:
            b.discard_trade()
            return []
        b.note_exit(date, reason, days)
        return self._flatten()

    def on_external_close(self, date, leg, price):
        '''A fill we didn't send closed one leg (LEAN auto-liquidates delisted stocks).
        Books that leg flat at the fill price, then flattens the other leg.'''
        held = self.book.qa if leg == "a" else self.book.qb
        if held == 0:
            return []
        self.book.on_fill(leg, -held, price, 0.0)   # Fee unknown per pair, booked as 0
        if self.dead:                               # already exiting: our own flatten order handles the rest
            return []
        return self.force_exit(date, "delisted")


def scorecard(engine: PairEngine):
    '''Computes metrics and per-pair items'''
    b = engine.book
    eq = np.asarray(b.equity, dtype=float)
    out = dict(pair=engine.name, days=len(eq), trades=len(b.trades), rejected_orders=engine.rejected,
               skipped_bars=engine.skipped_bars, open_trade_at_end=b.cur is not None,
               delisted=engine.dead,                   # True if the pair was force-closed by a delisting
               filtered=dict(engine.model.filtered))   # entry signal-days blocked by each filter
    if len(eq) < 2:
        return out
    ret = np.diff(np.concatenate([[0.0], eq])) / b.capital   # daily return on allocated capital
    sd = ret.std(ddof=1)
    peak = np.maximum.accumulate(np.concatenate([[0.0], eq]))
    years = len(eq) / 252.0
    pnls = np.array([t["pnl"] for t in b.trades])
    wins, losses = pnls[pnls > 0], pnls[pnls <= 0]
    yearly = {}
    prev = 0.0
    for d, e in zip(b.dates, b.equity):
        yearly[d.year] = yearly.get(d.year, 0.0) + (e - prev)
        prev = e
    reasons = {}
    for t in b.trades:
        reasons[t["reason"]] = reasons.get(t["reason"], 0) + 1
    out.update(
        net_pnl=float(eq[-1]),
        total_return=float(eq[-1] / b.capital),
        annual_return=float(eq[-1] / b.capital / years),          # simple, non-compounded
        sharpe=float(ret.mean() / sd * math.sqrt(252)) if sd > 0 else 0.0,
        max_drawdown=float((peak - np.concatenate([[0.0], eq])).max() / b.capital),
        win_rate=float(len(wins) / len(pnls)) if len(pnls) else None,
        profit_factor=float(wins.sum() / -losses.sum()) if len(losses) and losses.sum() < 0 else None,
        avg_trade_pnl=float(pnls.mean()) if len(pnls) else None,
        avg_hold_days=float(np.mean([t["days"] for t in b.trades])) if b.trades else None,
        time_in_market=float(np.mean(b.in_market)),
        exit_reasons=reasons,
        fees=float(b.fees), borrow_cost=float(b.borrow),
        pnl_by_year={int(y): round(v, 2) for y, v in yearly.items()},
        positive_years=f"{sum(v > 0 for v in yearly.values())}/{len(yearly)}",
    )
    return out

def parse_pairs(text):
    '''"AWR/CWT, LEA/ADNT" -> [("AWR","CWT"), ("LEA","ADNT")]. Spaces ignored; empty -> [].
    Raises on anything malformed so a typo fails at startup, not mid-backtest.'''
    pairs = []
    for item in (text or "").replace(" ", "").split(","):
        if not item:
            continue
        legs = item.upper().split("/")
        if len(legs) != 2 or not all(legs) or legs[0] == legs[1]:
            raise ValueError(f"bad pair '{item}': use TICKER/TICKER, comma-separated")
        if tuple(legs) in pairs:
            raise ValueError(f"duplicate pair '{item}'")
        pairs.append(tuple(legs))
    return pairs


def source_fingerprint(path):
    '''Short hash of a source file, ignoring line endings and trailing whitespace.
    Must stay identical to fingerprint() in tools/extract_blocks.py.'''
    import hashlib
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return "unavailable"
    text = "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip("\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]

def repo_block(filename, text):
    '''Wraps text in BEGIN/END markers so tools/extract_blocks.py (or copy-paste) can lift it into the repo'''
    return f"===== BEGIN {filename} =====\n{text.rstrip()}\n===== END {filename} ====="


def backtest_markdown(cards, meta, params):
    '''Paste-ready backtest_<run_tag>.md: run metadata, scorecard CSV, yearly P&L CSV.
    Kept compact (~300 bytes per pair) because free-tier QuantConnect caps logs at 10KB per backtest.'''
    import json
    f = lambda v, nd: "" if v is None else (f"{v:.{nd}f}" if isinstance(v, float) else str(v))

    # Run metadata
    lines = [f"# Backtest {meta.get('batch_id')} | run {meta.get('run_tag')}",
             " | ".join(f"{k}: {v}" for k, v in meta.items()),
             f"params: {json.dumps(params, default=str, separators=(',', ':'))}",
             "", "## Scorecard", "```csv"]

    # One row per pair
    lines.append("pair,trades,total_return,annual_return,sharpe,max_dd,win_rate,profit_factor,avg_hold_days,"
                 "time_in_mkt,exit_target,exit_stop,exit_time,exit_other,fees,borrow,positive_years,"
                 "filtered_hl,filtered_cadf,rejected_orders,open_at_end,delisted")
    for c in cards:
        r = c.get("exit_reasons", {})
        other = sum(v for k, v in r.items() if k not in ("target", "stop", "time"))
        lines.append(",".join([
            c["pair"], str(c["trades"]), f(c.get("total_return"), 4), f(c.get("annual_return"), 4),
            f(c.get("sharpe"), 2), f(c.get("max_drawdown"), 4), f(c.get("win_rate"), 3), f(c.get("profit_factor"), 2),
            f(c.get("avg_hold_days"), 1), f(c.get("time_in_market"), 3),
            str(r.get("target", 0)), str(r.get("stop", 0)), str(r.get("time", 0)), str(other),
            f(c.get("fees"), 0), f(c.get("borrow_cost"), 0), str(c.get("positive_years", "")),
            str(c["filtered"].get("half_life", 0)), str(c["filtered"].get("cadf", 0)),
            str(c["rejected_orders"]), str(c["open_trade_at_end"]), str(c.get("delisted", False))]))
    lines.append("```")

    # Yearly P&L, one row per pair, one column per year (dollars)
    years = sorted({y for c in cards for y in c.get("pnl_by_year", {})})
    lines += ["", "## P&L by year ($)", "```csv", "pair," + ",".join(map(str, years))]
    for c in cards:
        py = c.get("pnl_by_year", {})
        lines.append(c["pair"] + "," + ",".join(f"{py[y]:.0f}" if y in py else "" for y in years))
    lines.append("```")
    return repo_block(f"backtest_{meta.get('run_tag', 'base')}.md", "\n".join(lines))


def format_scorecard(s):
    if "net_pnl" not in s:
        return f"{s['pair']}: not enough data ({s['days']} days)"
    f = lambda v, spec: "n/a" if v is None else format(v, spec)
    return (f"{s['pair']}: ret {s['total_return']:+.1%} ({s['annual_return']:+.1%}/yr) | Sharpe {s['sharpe']:.2f} | "
            f"maxDD {s['max_drawdown']:.1%} | trades {s['trades']} win {f(s['win_rate'], '.0%')} "
            f"PF {f(s['profit_factor'], '.2f')} hold {f(s['avg_hold_days'], '.0f')}d | exits {s['exit_reasons']} | "
            f"in-mkt {s['time_in_market']:.0%} | fees ${s['fees']:,.0f} borrow ${s['borrow_cost']:,.0f} | "
            f"+yrs {s['positive_years']} | rejected {s['rejected_orders']} | filtered {s['filtered']}"
            + (" | OPEN TRADE AT END (marked to market)" if s["open_trade_at_end"] else "")
            + (" | DELISTED (force-closed)" if s.get("delisted") else ""))