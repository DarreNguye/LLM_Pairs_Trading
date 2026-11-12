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
