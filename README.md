# LLM Pairs Trading

Tests how well an LLM skill picks tradable pairs for a spread mean-reversion strategy.
The backtest is tuned and frozen on rule-based pairs first, then skill batches are judged against baselines on the frozen system.

## Status

- Trading settings frozen as `code/trading_config.py` v1 (see the registry's System section for the commit).
- Benchmark: rule-based pairs on the frozen system earned about zero (T001 2017–2022: +$7.0k on $1M; T002 2023–2025: −$8.0k).
- Next: skill batches (B001+).

```
skills/            v1_SKILL.md, v2_SKILL.md ... (never edit an old version)
code/              main.py, pairs_core.py (QuantConnect backtest), research.ipynb (screen),
                   screen_config.py (all screen settings), trading_config.py (frozen trading settings)
tools/             extract_blocks.py (QuantConnect output -> repo files)
batches/
    T001_tuning/   rule-based tuning set (as of 2016-12-31): selection.md, screen.csv, backtest/
    T002_tuning/   rule-based check set (as of 2022-12-31): selection.md, screen.csv, backtest/
    B00X_<date>_<skill ver>/
        prompt.md      exact prompt sent to the skill
        response.md    full LLM output, pasted exactly as written
        screen.csv     skill + baseline screen results
        backtest/      backtest_<run_tag>.md, one per group backtested
pair_registry.md   append-only log of the system and every batch
```

Batch IDs: `T00X` = rule-based sets (no LLM), `B00X` = skill batches.

## Before any QuantConnect run

Commit `code/` and make sure QuantConnect's copy matches it (`main.py`, `pairs_core.py`, `screen_config.py`,
`trading_config.py`, `research.ipynb`). The extractor stamps the commit hash and flags it if QuantConnect ran
different code (`source_check: MISMATCH`).

## Extracting results

The notebook and backtests print paste-ready blocks; the extractor turns them into repo files.

- Screen: copy notebook cell 6 output, then `pbpaste | python tools/extract_blocks.py - batches/<batch>/`
- Backtest: download the log, then `python tools/extract_blocks.py "<log name>_logs.txt" batches/<batch>/backtest/`
  Delete downloaded logs after extracting, then commit.

## Phase 1 — tune the backtest on T001 (done)

1. Screened every same-industry pair in the pool as of 2016-12-31 (`MODE = "tuning"`); kept the 30 with the lowest CADF p-value.
2. Backtested 2017–2022 with one parameter changed per run (`baseline`, `reentry`, `zfixed`, `cadf_off`, `exit0`,
   `reentry_exit0`, `stress_x2`). Winner: `exit_z=0`.

## Phase 2 — check and freeze (done)

1. Screened a fresh rule-based set T002 as of 2022-12-31 and ran the winning settings once on 2023–2025 (`run_tag=check`).
2. Froze the settings as `trading_config.py` v1; confirmed the frozen defaults reproduce the exit0 run.
   After this, only skills change.

## Phase 3 — skill batches (B001+)

Run the skill in an incognito chat (no memory, no past chats) so it can't see earlier results.

1. Choose the as-of date. After the model's knowledge cutoff = clean (forward test / paper trade from there);
   before it = results now, but contaminated. Record which in the registry.
2. Copy `batches/_TEMPLATE` to `batches/B00X_<date>_<skill ver>/`.
3. Run the skill. Paste the prompt into `prompt.md` and the full reply into `response.md`.
   Append its registry block to `pair_registry.md`. **Commit.**
4. In `research.ipynb`: `MODE = "batch"`, set `BATCH_ID` and `AS_OF`, and paste the skill's `Pairs (paste):` line into
   `PAIRS_STR`. The pool and both baselines build automatically; each pair needs CADF p < 0.05 in both directions.
   Run all cells, extract into `batches/B00X_.../`. **Commit.**
5. Backtest each group's passing pairs as a separate run, same `batch_id`, `start` (printed by the screen) and `end`.
   Copy each group's line from the screen entry in `pair_registry.md`:
   - `run_tag=skill`: `pairs` = the `- pairs:` line
   - `run_tag=random`: `pairs` = the `- pairs (random, …):` line
   - `run_tag=same_industry`: `pairs` = the `- pairs (same_industry, …):` line
     Skip a group whose line says `none`. Extract each into `batches/B00X_.../backtest/`. **Commit.**
6. Compare groups on pass rate (screen) and on P&L, stop rate and win rate (backtest). The skill is judged
   relative to the baselines, never in absolute terms.

## QuantConnect parameters (main.py)

Defaults come from `trading_config.py` (trading) and `screen_config.py` (half-life range). Set only what a run needs.

| Parameter                                  | Default                | Purpose                                                 |
| ------------------------------------------ | ---------------------- | ------------------------------------------------------- |
| `pairs`                                    | none (required)        | `A/B,C/D,...`                                           |
| `batch_id`                                 | T001                   | label in the output file                                |
| `config`                                   | v1                     | screen config version                                   |
| `trading`                                  | v1                     | trading config version                                  |
| `start`, `end`                             | 2017-01-01, 2022-12-31 | `YYYY-MM-DD`; set per batch                             |
| `run_tag`                                  | baseline               | output file name `backtest_<run_tag>.md`                |
| `entry_mode`                               | cross                  | `reentry` = enter on the turn back inside entry_z       |
| `entry_z`, `exit_z`, `stop_z`              | 2, 0, 4                | z thresholds                                            |
| `hl_z_mult`                                | 1.0                    | z window = mult × half-life (20-day min)                |
| `hl_hold_mult`                             | 3.0                    | time stop = mult × half-life, capped at `max_hold_days` |
| `max_hold_days`                            | 60                     | time stop ceiling                                       |
| `coint_pvalue`                             | 0.1                    | live CADF filter                                        |
| `min_half_life`, `max_half_life`           | 5, 60                  | live half-life filter (from screen_config)              |
| `cost_mult`, `slippage_bps`, `borrow_rate` | 1, 2, 0.01             | costs; per-ticker overrides in `TICKER_COSTS`           |
| `verbose_log`                              | 0                      | 1 = readable per-pair lines (watch the 10KB log cap)    |

## Rules

- Never edit a registered batch, `prompt.md`, `response.md` or old results. Failed pairs stay.
- Screen settings live only in `code/screen_config.py`, trading settings only in `code/trading_config.py`;
  the versions used are recorded in every result.
- Don't change trading settings based on skill batch results. A new trading version means re-running every batch on it.
- Pairs under "Seen before this registry" can never count as holdout evidence.
- Once a trading window's results have been seen, it is spent for evaluating new batches.
- Free QuantConnect: no Object Store, and logs are capped at 10KB per backtest. Keep `verbose_log=0`.
