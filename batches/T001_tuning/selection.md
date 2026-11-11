# T001 — tuning set (rule-based, no LLM)

Used only to tune and then freeze the backtest. Never used to judge the skill.

## Selection rule (fixed before screening; settings in code/screen_config.py)

- Pool: top 1000 (`pool_top_n`) US stocks by dollar volume with a Morningstar industry code, price > $5, daily dollar volume > $5M, as of 2016-12-31 (QuantConnect universe_history, research.ipynb cell 4)
- Candidates: every same-industry pair in the pool (`TUNING["max_candidates"] = None`)
- Eligible: passes every non-CADF check in config v1 (listed full window, liquidity, beta > 0 and stable, half-life 5–60, ≥ 12 crossings/yr)
- Selected: the 30 (`TUNING["n_select"]`) eligible pairs with the lowest CADF p-value (both directions: the larger of the two p-values)
- Screen: config v1, `MODE = "tuning"`, formation 2013-12-31 to 2016-12-31

## Periods

- Tune: 2017-01-01 to 2022-12-31 (`start`/`end` defaults in main.py)
- Check once, after tuning: 2023-01-01 to 2025-12-31
