# T002 — check set (rule-based, no LLM)

Used once to check the frozen trading settings on fresh pairs and recent data. Never used to judge the skill.

## Selection rule (same as T001; settings in code/screen_config.py)

- Pool: top 1000 (`pool_top_n`) US stocks by dollar volume with a Morningstar industry code, price > $5, daily dollar volume > $5M, as of 2022-12-31
- Candidates: every same-industry pair in the pool
- Eligible: passes every non-CADF check in config v1
- Selected: the 30 eligible pairs with the lowest CADF p-value (both directions)
- Screen: config v1, `MODE = "tuning"`, formation 2019-12-31 to 2022-12-31

## Period

- Check once: 2023-01-01 to 2025-12-31 with trading_config v1
