# LLM Pairs Trading

Tests how well an LLM skill picks tradable pairs for a spread mean-reversion strategy.

```
skills/            v1_SKILL.md, v2_SKILL.md ... (never edit an old version)
code/              main.py, pairs_core.py (QuantConnect backtest), research.ipynb (screen), screen_config.py (all screen settings)
tools/             extract_blocks.py (QuantConnect output -> repo files)
batches/
    T001_tuning/   rule-based tuning set: selection.md, screen.csv, backtest/
    B00X_<date>_<skill ver>/
        prompt.md      exact prompt sent to the skill
        response.md    full LLM output, pasted exactly as written
        screen.csv     skill + baseline screen results
        backtest/      backtest_<run_tag>.md, only for pairs that passed the screen
pair_registry.md   append-only log of the system and every batch
```

Batch IDs: `T00X` = tuning sets (no LLM), `B00X` = skill batches.

## Before any QuantConnect run

Commit `code/` and make sure QC's copy matches it. The extractor stamps the commit hash
and flags it if QC ran different code (`source_check: MISMATCH`).

## Phase 1 — tune the backtest (T001)

1. Check `batches/T001_tuning/selection.md` matches `TUNING` and `pool_top_n` in `code/screen_config.py`. **Commit.**
2. In `research.ipynb`: `MODE = "tuning"`, `BATCH_ID = "T001"`, `AS_OF = 2016-12-31`. Run all cells (it screens every
   same-industry pair in the pool and selects the 30 best by CADF p-value), then:
3. In `research.ipynb`: `MODE = "batch"`, set `BATCH_ID`, `AS_OF`, and paste the skill's `Pairs (paste):` line into
   `PAIRS_STR` (the pool and baselines build automatically; each pair needs CADF p < 0.05 in both directions). Run all cells, then:
4. Repeat step 3 changing one parameter per run, each with its own `run_tag`
   (e.g. `entry_mode=reentry`, `exit_z=0`, `hl_hold_mult=2`/`4`, `max_hold_days=90`, `coint_pvalue=0.05`, `cost_mult=2`).
   Keep a change only if it helps most pairs and has a reason. Stop after 5–8 runs.

## Phase 2 — freeze

1. Run the winning settings once on 2023–2025 (`start=2023-01-01`, `end=2025-12-31`, `run_tag=check`).
2. Put the winners in `main.py` defaults, commit, and append to the registry's System section:
   "frozen at commit <hash>". After this, only skills change.

## Phase 3 — skill batches (B001+)

Run the skill in an incognito chat (no memory, no past chats) so it can't see earlier results.

1. Copy `batches/_TEMPLATE` to `batches/B00X_<date>_<skill ver>/`.
2. Run the skill. Paste the prompt into `prompt.md` and the full reply into `response.md`.
   Append its registry block to `pair_registry.md`. **Commit.**
3. In `research.ipynb`: `MODE = "batch"`, set `BATCH_ID`, `AS_OF`, `BASELINE_POOL`, `INDUSTRY`, and paste the
   skill's `Pairs (paste):` line into `PAIRS_STR`. Run all cells, then:
   `python tools/extract_blocks.py <output.txt | -> batches/B00X_.../` **Commit.**
4. In QC parameters set `pairs`, `batch_id`, `start` (printed in step 3), `end`, `run_tag`. Backtest, then:
   `python tools/extract_blocks.py <log.txt> batches/B00X_.../backtest/` **Commit.**

## QuantConnect parameters (main.py)

| Parameter                                  | Default                | Purpose                                                 |
| ------------------------------------------ | ---------------------- | ------------------------------------------------------- |
| `pairs`                                    | none (required)        | `A/B,C/D,...`                                           |
| `batch_id`                                 | T001                   | label in the output file                                |
| `config`                                   | v1                     | screen config version                                   |
| `start`, `end`                             | 2017-01-01, 2022-12-31 | `YYYY-MM-DD` (tuning period)                            |
| `run_tag`                                  | baseline               | output file name `backtest_<run_tag>.md`                |
| `entry_mode`                               | cross                  | `reentry` = enter on the turn back inside entry_z       |
| `entry_z`, `exit_z`, `stop_z`              | 2, 0.5, 4              | z thresholds                                            |
| `hl_z_mult`                                | 1.0                    | z window = mult × half-life (20-day min)                |
| `hl_hold_mult`                             | 3.0                    | time stop = mult × half-life, capped at `max_hold_days` |
| `max_hold_days`                            | 60                     | time stop ceiling                                       |
| `coint_pvalue`                             | 0.1                    | live CADF filter                                        |
| `min_half_life`, `max_half_life`           | 5, 60                  | live half-life filter (matches screen_config)           |
| `cost_mult`, `slippage_bps`, `borrow_rate` | 1, 2, 0.01             | costs; per-ticker overrides in `TICKER_COSTS`           |
| `verbose_log`                              | 0                      | 1 = readable per-pair lines (watch the 10KB log cap)    |

## Rules

- Never edit a registered batch, `prompt.md`, `response.md` or old results. Failed pairs stay.
- Screen settings live only in `code/screen_config.py`; the version used is recorded in every registry entry.
- Pairs under "Seen before this registry" can never count as holdout evidence.
- Once a trading window's results have been seen, it is spent for evaluating new batches.
- Free QuantConnect: no Object Store, and logs are capped at 10KB per backtest. Keep `verbose_log=0`.
