# Pair registry

Append-only. Never edit or delete an entry; failed pairs stay.
Screen results are appended by `tools/extract_blocks.py`.

## System

- 2026-11-08: backtest baseline set at commit <hash>
  - entry_mode=cross, entry/exit/stop z = 2 / 0.5 / 4, unblock_z=0.5
  - hl_z_mult=1, hl_hold_mult=3 (time stop capped at max_hold_days=60)
  - live filters: coint_pvalue=0.1, half-life 5–60 days
  - costs: 2 bps slippage, 1% borrow, IBKR fees
- Plan: tune on T001 over 2017–2022, check winners once on 2023–2025, then freeze.
- Status: tuning, not frozen.

## Seen before this registry (never use as a holdout)

KO/PEP, XOM/CVX, V/MA, AWR/CWT, LEA/ADNT, AA/CENX, AROC/USAC, GPRE/REX, UFPI/BCC, AESI/PUMP, L/CNA, LLYVK/LYV, PSLV/SLV, PHO/FIW

## Batch T001 (tuning set, rule-based, no LLM)

- Registered: 2026-11-08
- Selection: see `batches/T001_tuning/selection.md`
- As-of date T: 2016-12-31 Formation: 2013-12-31 to 2016-12-31 Config: v1
- Purpose: tune and freeze the backtest only; not evidence about the skill
- Status: registered, not yet screened

### T001 screen (2026-11-11, tuning mode)

- config v1 | code unknown | T=2016-12-31 | formation 2013-12-31 to 2016-12-31 | seed 0
- Rule: rank by CADF p (both directions), top 30 of 657 eligible from 6171 candidates
- Passed: tuning 30/6171
- To backtest (30): paste into the QC `pairs` parameter, and set batch_id=T001, start=2017-01-01
- pairs: ADBE/CDNS,CDNS/CTXS,LLTC/MCHP,AEP/ED,CMS/ED,CMS/XEL,D/DTE,D/EIX,D/PNW,LNT/NEE,DIS/IMAX,CCI/CONE,AMTD/GS,COG/EQT,EQT/RRC,DRH/LHO,CW/LLL,CMA/IBKC,EWBC/HBAN,FITB/ZION,PVTB/SNV,PVTB/WAL,SNV/WAL,LBTYA/LBTYK,BRX/FRT,BRX/REG,BRX/SPG,FRT/REG,CP/KSU,EFX/VRSK

### T002 screen (2026-11-11, tuning mode)

- config v1 | code fbdc43d | T=2022-12-31 | formation 2019-12-31 to 2022-12-31 | seed 0
- Rule: rank by CADF p (both directions), top 30 of 874 eligible from 6696 candidates
- Passed: tuning 30/6696
- To backtest (30): paste into the QC `pairs` parameter, and set batch_id=T002, start=2023-01-01
- pairs: CRL/IDXX,ICLR/PKI,IQV/LH,LEA/MGA,AIG/BRK.A,AIG/BRK.B,BRX/KIM,AEE/OGE,DTE/PEG,ETR/OGE,FL/URBN,AGCO/CAT,IR/PH,FFIV/MDB,FUL/LIN,IP/WRK,BEN/STT,BLK/STT,BN/NTRS,CG/NTRS,CIVI/FANG,BPOP/EWBC,EWBC/FITB,EWBC/WBS,HBAN/WBS,CHH/WH,CPRI/SIG,NVR/TOL,KNX/ODFL,WCN/WM

### System update (2026-11-12)

- Trading settings frozen as code/trading_config.py "v1" at commit e7ba388: exit_z=0, everything else as baseline.
  Confirmed: a run with the frozen defaults on T001 reproduced the exit0 result (differences only in $1 rounding).
- Tuning on T001 (2017–2022, $1M): baseline +$4.7k, reentry −$9.3k, zfixed +$0.5k, cadf_off −$27.7k, exit0 +$7.0k, reentry+exit0 −$9.7k; exit0 at 2x costs +$2.2k.
- One-time check on T002 (2023–2025): −$8.0k. About zero edge on statistically selected pairs; this is the benchmark for skill batches.
- max_price=1000 added to config v1 (whole-share sizing); T001 and T002 were screened before it.
- Note: the T001 screen entry shows `code unknown` because it was extracted before the first commit; it ran on the code committed as fac6329.
- Status: frozen. Only skill versions change from here.

## Batch T002 (check set, rule-based, no LLM)

- Registered: 2026-11-11
- Selection: see `batches/T002_tuning/selection.md` (same rule as T001)
- As-of date T: 2022-12-31 Formation: 2019-12-31 to 2022-12-31 Config: v1
- Purpose: one-time out-of-sample check of the frozen trading settings (2023–2025); not evidence about the skill
- Status: screened and checked (see T002 screen entry and backtest_check.md)

## Batch B001

- Registered: 2026-11-12
- As-of date T: 2023-12-31
- Selector: Claude Opus 5.5, knowledge cutoff 2026-06-30
- Mode: Historical-contaminated
- Formation window: 2020-12-31 to 2023-12-31
- Trading window: 2024-01-01 to 2025-12-31
- Trials in this batch: 12 Cumulative trials on this trading window: 12 (assumes no prior batches on this window; correct if not)
- Frozen thresholds: EG both directions, max p < 0.0042 (Bonferroni, N=12); half-life 5–60d; ≥12 zero-crossings/yr; split-half beta within ±25%, same sign; z entry 2.0 / exit 0.5 / stop 3.5; rolling z lookback 2× half-life (min 20d), t−1 data, t+1 execution
- Pairs:
  1. FBP/OFG – Puerto Rico banks, same economy and regulators
  2. AVA/NWE – small northern-tier electric+gas utilities
  3. GPI/ABG – franchised auto dealer groups of similar size
  4. ONTO/CAMT – inspection/metrology, advanced-packaging exposure
  5. GNK/SBLK – dry-bulk owners on the same charter rates
  6. GPRE/REX – ethanol producers on the same crush spread
  7. ICHR/UCTT – subsystem suppliers to Lam and Applied Materials
  8. WIRE/ATKR – wire and conduit via the same electrical distributors
  9. UFPI/BCC – wood products on the same lumber cycle
  10. L/CNA – Loews owns ~90% of CNA
  11. FMX/KOF – FEMSA owns ~47% of Coca-Cola FEMSA
  12. IEP/CVI – Icahn Enterprises owns ~2/3 of CVR Energy
- Pairs (paste): FBP/OFG,AVA/NWE,GPI/ABG,ONTO/CAMT,GNK/SBLK,GPRE/REX,ICHR/UCTT,WIRE/ATKR,UFPI/BCC,L/CNA,FMX/KOF,IEP/CVI
- Status: registered, not yet screened
- Note: Historical-contaminated (selector knowledge extends past T). Trading window overlaps the T002 check period (2023–2025); no settings were changed after that check.
- Note: GPRE/REX, UFPI/BCC and L/CNA are on the "Seen before this registry" list; they are screened and backtested with the batch but excluded when judging the skill.
- Note: the skill's screening spec and "Frozen thresholds" above are its own suggestion; this batch is screened with screen_config v1 and traded with trading_config v1.

### B001 screen (2026-11-13, batch mode)

- config v1 | code 9b69a08 (dirty) | T=2023-12-31 | formation 2020-12-30 to 2023-12-31 | seed 0
- Rule: CADF (both directions), none correction
- Passed: random 0/12 | same_industry 0/12 | skill_v1 0/12
- To backtest (0): paste into the QC `pairs` parameter, and set batch_id=B001, start=2024-01-01
- pairs: none
- pairs (random, run_tag=random): none
- pairs (same_industry, run_tag=same_industry): none
- Note: "(dirty)" = only notebook cell 1 batch settings were uncommitted at extraction.
- Eligible except CADF: skill 5/12 (3/9 unseen: FBP/OFG, AVA/NWE, WIRE/ATKR), random 1/12 (WPC/CMS), same_industry 1/12 (AER/R). No group passed; no gated backtests.
- Exploratory (decided after the screen, not part of the v1 protocol): backtest all 12 pairs per group, 2024-01-01 to 2025-12-31, run_tags skill_all / random_all / same_industry_all. Historical-contaminated; not evidence.
