# region imports
from AlgorithmImports import *
import json
import pairs_core
from pairs_core import Params, PairEngine, scorecard, format_scorecard, backtest_markdown, parse_pairs, source_fingerprint
import screen_config
from screen_config import CONFIGS
import trading_config
from trading_config import TRADING
from datetime import datetime
# endregion

# Run meta data is handled on QC

# Pairs to trade (default; the `pairs` parameter, e.g. "AWR/CWT,LEA/ADNT", overrides this list)
PAIRS = []

# For niche assets, per-ticker cost overrides for thin or hard-to-borrow names (fill from IBKR borrow rates / typical quoted spread).
# Anything not listed uses slippage_bps and borrow_rate below. Both are still scaled by cost_mult.
TICKER_COSTS = {
    # "AESI": dict(slippage_bps=10.0, borrow_rate=0.05),
}


class PairsBacktester(QCAlgorithm):
    """Evaluates pairs. Every pair trades its own fixed capital slice with identical rules.
    Signals use daily closes; orders are market-on-open for the next session (no lookahead)."""

    def initialize(self):

        # Quant Connect parameter helper
        gp = lambda k, d: type(d)(self.get_parameter(k, d))

        # Run meta data
        self.batch_id = gp("batch_id", "T001")          # batch folder this run belongs to (T001 = rule-based tuning set)
        self.config_ver = gp("config", "v1")            # code/screen_config.py version the pairs were screened with
        hl_min, hl_max = CONFIGS[self.config_ver]["hl_range"]
        self.trading_ver = gp("trading", "v1")          # code/trading_config.py version (frozen trading settings)
        T = TRADING[self.trading_ver]
        self.pairs = parse_pairs(gp("pairs", "")) or PAIRS   # paste the screen's "pairs:" line
        if not self.pairs:
            raise ValueError("No pairs: set the `pairs` parameter (e.g. AWR/CWT,LEA/ADNT)")

        # Backtest Parameters (defaults = tuning period 2017-2022; 2023-2025 is the results)
        self.set_start_date(datetime.strptime(gp("start", "2017-01-01"), "%Y-%m-%d"))
        self.set_end_date(datetime.strptime(gp("end", "2022-12-31"), "%Y-%m-%d"))
        self.set_cash(1_000_000)
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN)

        # cost_mult scales slippage and borrow
        self.cost_mult = gp("cost_mult", 1.0)
        self.slippage_bps = gp("slippage_bps", float(T["slippage_bps"]))

        # Meta data to tag and verbose output
        self.run_tag = gp("run_tag", "baseline")
        self.verbose_log = gp("verbose_log", 0)

        # Trading Parameters (defaults from trading_config.py; a QC parameter overrides any one of them)
        self.params = Params(
            beta_lookback=gp("beta_lookback", T["beta_lookback"]),
            z_lookback=gp("z_lookback", T["z_lookback"]),
            entry_z=gp("entry_z", T["entry_z"]),
            exit_z=gp("exit_z", T["exit_z"]),
            stop_z=gp("stop_z", T["stop_z"]),
            max_hold_days=gp("max_hold_days", T["max_hold_days"]),
            gross_leverage=gp("gross_leverage", T["gross_leverage"]),
            borrow_rate=gp("borrow_rate", T["borrow_rate"]) * self.cost_mult,

            # Logic switches
            # cross:   enter as soon as |z| passes entry_z (may enter as spread is still widening)
            # reentry: arm when |z| passes entry_z, enter once it turns back inside (enters when spread is starting to revert)
            entry_mode=gp("entry_mode", T["entry_mode"]),
            unblock_z=gp("unblock_z", T["unblock_z"]),
            hl_z_mult=gp("hl_z_mult", T["hl_z_mult"]),
            hl_hold_mult=gp("hl_hold_mult", T["hl_hold_mult"]),

            # Filters to determine if mean reversion is valid (half-life range from screen_config.py)
            coint_pvalue=gp("coint_pvalue", T["coint_pvalue"]),
            min_half_life=gp("min_half_life", float(hl_min)),
            max_half_life=gp("max_half_life", float(hl_max)))
        self.params.validate()

        # Split capital between each pair
        capital = self.portfolio.cash / len(self.pairs)

        # Sets up engine for pairs
        self.engines = []
        self._orders = {}
        self._legs = {}            # symbol -> [(engine, leg)], to route non-sent delistings and fills 
        for ta, tb in self.pairs:
            syms, borrows = [], []
            for t in (ta, tb):
                c = TICKER_COSTS.get(t, {})
                sec = self.add_equity(t, Resolution.DAILY)
                sec.set_fee_model(InteractiveBrokersFeeModel())
                sec.set_slippage_model(ConstantSlippageModel(c.get("slippage_bps", self.slippage_bps) / 1e4 * self.cost_mult))
                syms.append(sec.symbol)
                borrows.append(c["borrow_rate"] * self.cost_mult if "borrow_rate" in c else self.params.borrow_rate)
            eng = PairEngine(f"{ta}/{tb}", Params(**vars(self.params)), capital, borrow_rates=tuple(borrows))
            self._warm(eng, syms[0], syms[1])
            self.engines.append((eng, syms[0], syms[1]))
            self._legs.setdefault(syms[0], []).append((eng, "a"))
            self._legs.setdefault(syms[1], []).append((eng, "b"))

    def _warm(self, eng, a, b):
        '''Pull closes for lookback days'''
        hist = self.history([a, b], self.params.beta_lookback, Resolution.DAILY)
        if hist.empty:
            return
        closes = hist["close"].unstack(level=0).dropna()
        if a in closes.columns and b in closes.columns:
            for pa, pb in zip(closes[a].values, closes[b].values):
                eng.warm(float(pa), float(pb))

    def on_data(self, data: Slice):
        '''Gives data to engine and places orders when instructed'''

        # A leg is about to delist so close the whole pair at the next open 
        for sym in list(data.delistings.keys()):
            if data.delistings[sym].type == DelistingType.WARNING:
                for eng, _ in self._legs.get(sym, []):
                    if not eng.dead:
                        self._send(eng, *self._syms_of(eng), eng.force_exit(self.time.date(), "delisted"))

        for eng, a, b in self.engines:
            if a not in data.bars or b not in data.bars:
                continue
            pa, pb = float(data.bars[a].close), float(data.bars[b].close)
            self._send(eng, a, b, eng.on_bar(self.time.date(), pa, pb))
            if eng.book.equity:
                self.plot("Pair P&L", eng.name, eng.book.equity[-1])

    def _send(self, eng, a, b, orders):
        '''Places market-on-open orders for the next session and tracks them (moved out of on_data so delistings can reuse it)'''
        for leg, qty in orders:
            ticket = self.market_on_open_order(a if leg == "a" else b, qty, tag=eng.name)
            if ticket.status == OrderStatus.INVALID:
                eng.on_order_dead()
                self.error(f"{eng.name}: order rejected for leg {leg}")
            else:
                self._orders[ticket.order_id] = (eng, leg)

    def _syms_of(self, eng):
        '''(symbol A, symbol B) for an engine'''
        return next((a, b) for e, a, b in self.engines if e is eng)

    def on_order_event(self, e: OrderEvent):
        '''Records if trades get filled'''
        ref = self._orders.get(e.order_id)
        if ref is None:
            # A fill was not sent so close that leg in every pair holding it
            if e.status == OrderStatus.FILLED:
                for eng, leg in self._legs.get(e.symbol, []):
                    self._send(eng, *self._syms_of(eng), eng.on_external_close(self.time.date(), leg, float(e.fill_price)))
            return
        eng, leg = ref
        if e.status in (OrderStatus.PARTIALLY_FILLED, OrderStatus.FILLED):
            final = e.status == OrderStatus.FILLED
            eng.on_fill(leg, int(e.fill_quantity), float(e.fill_price), float(e.order_fee.value.amount), final)
            if final:
                del self._orders[e.order_id]
        elif e.status in (OrderStatus.CANCELED, OrderStatus.INVALID):
            eng.on_order_dead()
            del self._orders[e.order_id]
            self.error(f"{eng.name}: order {e.order_id} {e.status} for leg {leg}")

    def on_end_of_algorithm(self):
        '''Logs scorecards for each pair'''
        cards = [scorecard(eng) for eng, _, _ in self.engines]

        # Readable lines switch
        if self.verbose_log:
            self.log(f"=== PAIR SCORECARD (cost_mult={self.cost_mult}) ===")
            for c in cards:
                self.log(format_scorecard(c))
                if "pnl_by_year" in c:
                    self.log(f"   by year: {c['pnl_by_year']}")

        # Generate a paste ready file of results
        meta = dict(batch_id=self.batch_id, run_tag=self.run_tag, config=self.config_ver, trading=self.trading_ver, code="{CODE_COMMIT}",
                    src_main=source_fingerprint(globals().get("__file__", "")),
                    src_core=source_fingerprint(getattr(pairs_core, "__file__", "")),
                    src_config=source_fingerprint(getattr(screen_config, "__file__", "")),
                    src_trading=source_fingerprint(getattr(trading_config, "__file__", "")),
                    window=f"{self.start_date:%Y-%m-%d} to {self.end_date:%Y-%m-%d}",
                    pairs=",".join(f"{a}/{b}" for a, b in self.pairs),
                    cost_mult=self.cost_mult, slippage_bps=self.slippage_bps, ticker_costs=TICKER_COSTS or "none")
        block = backtest_markdown(cards, meta, vars(self.params))
        if len(block.encode()) > 9000:
            self.error(f"Repo block is {len(block.encode())} bytes; free-tier logs cap at 10KB, so it may be cut off")
        self.log(block)
        try:    # optional copy for the notebook; free-tier accounts may lack Object Store write access
            self.object_store.save(f"pairs_scorecard_x{self.cost_mult:g}.json", json.dumps(cards, default=str))
        except Exception as ex:
            self.log(f"Scorecard not saved to Object Store ({type(ex).__name__}); it is in the log above.")