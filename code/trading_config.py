"""Frozen trading settings for the backtest. main.py reads its defaults from here.
QC parameters still override any value for a one-off run (e.g. cost_mult=2 stress tests).
Never edit a version once a batch has been backtested with it; add a new version instead."""

TRADING = {
    "v1": dict(                    # frozen 2026-11: tuned on T001 (2017-2022), checked on T002 (2023-2025)
        beta_lookback=252,         # days used to estimate the hedge ratio
        z_lookback=60,             # fallback z window; overridden when hl_z_mult > 0
        entry_z=2.0,               # enter when |z| passes this
        exit_z=0.0,                # exit at the mean (tuning winner: exit0)
        stop_z=4.0,                # stop when z moves this far against the trade
        max_hold_days=60,          # time stop, and the ceiling on the half-life time stop
        gross_leverage=1.0,        # long + short notional, as a multiple of the pair's capital
        borrow_rate=0.01,          # annual fee on short market value (per-ticker overrides in main.py's TICKER_COSTS)
        slippage_bps=2.0,          # per-fill slippage
        entry_mode="cross",        # "cross" or "reentry" (reentry tested worse)
        unblock_z=0.5,             # after a stop, re-allow entries once |z| is within this
        hl_z_mult=1.0,             # z window = mult x half-life (20-day min)
        hl_hold_mult=3.0,          # time stop = mult x half-life at entry, capped at max_hold_days
        coint_pvalue=0.1,          # live CADF filter on the trailing beta window (turning it off lost money)
    ),
}