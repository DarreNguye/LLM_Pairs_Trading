# Response — B001

**Historical-contaminated.** My knowledge runs through the end of June 2026, so I've seen 2024–25. Use this batch to debug the pipeline and compare against a baseline, not as evidence that the selection works. No web search was used. Every pair is justified by structure knowable at T. I did not use post-T events I'm aware of to pick or drop any pair.

## Run header

- **Batch ID:** B001
- **As-of date T:** 2023-12-31
- **Formation window:** 2020-12-31 to 2023-12-31
- **Trading window:** 2024-01-01 to 2025-12-31
- **Universe:** US-listed stocks and ADRs only, with no ETFs or CEFs. Price must be $5–$1,000 at T, median daily dollar volume above $5M over the formation window, and listed for the whole window.
- **Selector:** Claude Opus 5.5, knowledge cutoff end of June 2026
- **Mode:** Historical-contaminated

## Candidates

Legs are listed as A / B. Trade direction comes from the spread z-score.

| #   | Legs        | Link type               | Structural rationale (knowable at T)                                                                                                        | What would break it                                                                                                       | Crowding check                                   | Flags                                 |
| --- | ----------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------- |
| 1   | FBP / OFG   | Narrow peer             | Both are Puerto Rico–centric banks of similar size. They share the island economy, regulators, and deposit and consumer/auto-loan markets.  | M&A among PR banks; a credit event in one book; mainland/USVI expansion                                                   | Not a known example; PR niche                    | none                                  |
| 2   | AVA / NWE   | Narrow peer             | Small multi-state electric and gas utilities in the Pacific NW and Northern Plains. Similar size, regulated returns and generation mix.     | Adverse rate case or wildfire liability at one leg; M&A                                                                   | Utilities often paired, this pair isn't          | none                                  |
| 3   | GPI / ABG   | Narrow peer             | Franchised dealer groups of similar size, driven by the same OEM allocation, used-car pricing and F&I margins.                              | Large acquisition (ABG's Larry H. Miller deal sits inside formation); GPI's UK segment diverging                          | Dealer pairs far less crowded than OEM pairs     | none                                  |
| 4   | ONTO / CAMT | Narrow peer             | Inspection and metrology toolmakers, both heavily exposed to advanced packaging and the same foundry/OSAT customers.                        | Share shift in packaging inspection; Israel-specific risk at CAMT (war ongoing at T); M&A                                 | Semicap pairs usually megacaps; this is niche    | factor-mismatch                       |
| 5   | GNK / SBLK  | Narrow peer             | Dry-bulk owners whose earnings follow the same Capesize/Supramax charter rates and fuel costs.                                              | SBLK's pending acquisition of Eagle Bulk (announced Dec 2023) changes fleet mix; dividend-policy divergence               | Niche                                            | none                                  |
| 6   | GPRE / REX  | Shared input            | Ethanol producers whose margins come from the same corn, ethanol and natural-gas crush spread.                                              | GPRE's mix shift to protein and corn oil; carbon-capture pipeline outcomes; REX's large cash balance dampening its moves  | Niche                                            | liquidity-borderline, factor-mismatch |
| 7   | ICHR / UCTT | Shared customer         | Gas and fluid delivery subsystem suppliers. Revenue for both is concentrated in Lam Research and Applied Materials spend.                   | Customer insourcing or share shift between them; UCTT services growth                                                     | Niche                                            | none                                  |
| 8   | WIRE / ATKR | Shared customer + input | Building wire and conduit sold through the same electrical distributors into construction. Both pass through copper, steel and PVC pricing. | M&A; conduit pricing normalizing differently from copper-linked wire                                                      | Niche                                            | none                                  |
| 9   | UFPI / BCC  | Shared input            | Wood-products makers and distributors on the same lumber/panel cycle and housing/R&R demand.                                                | BCC's mill/EWP exposure vs UFPI's packaging/industrial mix; M&A                                                           | Homebuilders are the crowded version; this isn't | none                                  |
| 10  | L / CNA     | Ownership               | Loews owns roughly 90% of CNA, its largest asset.                                                                                           | Loews buying in the CNA minority; hotels, Boardwalk or Altium diverging; Loews buybacks                                   | Holdco trades known; this one rarely cited       | borrow-risk                           |
| 11  | FMX / KOF   | Ownership               | FEMSA owns about 47% of Coca-Cola FEMSA. Both are NYSE ADRs with the same MXN and Mexican-consumer exposure.                                | FEMSA selling KOF stake; OXXO (FMX's main value driver) diverging; FEMSA Forward divestments                              | Niche                                            | borrow-risk, factor-mismatch          |
| 12  | IEP / CVI   | Ownership               | Icahn Enterprises owns about two-thirds of CVR Energy, a large share of IEP's NAV.                                                          | IEP's other holdings or hedge book; distribution cuts; Icahn margin-loan pressure (public since May 2023); CVI stake sale | Niche                                            | borrow-risk                           |

**Considered and excluded at T, for reasons knowable at T:**

- **CCL/CUK:** dual-listed twin shares, which is the crowded share-class type.
- **EGLE:** pending Star Bulk deal at T.
- **CCRN:** pending Aya deal at T.
- **SAVE:** pending JetBlue deal at T.

## Screening spec (frozen, formation window only)

- **Data:** daily log prices, split- and dividend-adjusted.
- **Cointegration:** Engle-Granger in both directions, using the larger p-value. Require p < 0.05/12 = 0.0042 (Bonferroni, N = 12). Report Benjamini-Hochberg at 5% FDR alongside, for reference only.
- **Hedge ratio:** OLS β on the full window. The β fitted on each half must have the same sign and sit within ±25% of the full-window β.
- **Half-life:** AR(1) on the spread, between 5 and 60 trading days.
- **Zero-crossings:** at least 12 per year (36 over formation).
- **Signals:** spread = log A − β·log B, with β frozen. z uses a rolling mean and standard deviation, lookback = 2× half-life (minimum 20 days), data through t−1. Entry at |z| ≥ 2.0, exit at |z| ≤ 0.5, stop at |z| ≥ 3.5.
- **Execution:** a signal on bar t executes on bar t+1.
- **Liquidity:** re-verify the $5M median dollar-volume floor; REX is the likeliest to fail.
- **Costs:** model half-spread, slippage, and borrow fees, with higher borrow for the flagged legs (CNA, KOF, IEP, CVI). Charge dividends on short legs; GNK, SBLK, IEP and CVI pay large ones.
- **Delisting:** close the pair at the last tradable price and keep it in the results.

## Registry entry

```
## Batch B001
- Registered: 2026-11-12
- As-of date T: 2023-12-31
- Selector: Claude Opus 5.5, knowledge cutoff 2026-06-30
- Mode: Historical-contaminated
- Formation window: 2020-12-31 to 2023-12-31
- Trading window: 2024-01-01 to 2025-12-31
- Trials in this batch: 12   Cumulative trials on this trading window: 12 (assumes no prior batches on this window; correct if not)
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
```

**Weakest candidates:**

- **IEP/CVI and FMX/KOF:** the parent's value depends heavily on assets other than the listed stake, and both have borrow-cost drag.
- **GPRE/REX:** GPRE was mid-transformation at T, and REX may fail the liquidity floor.
