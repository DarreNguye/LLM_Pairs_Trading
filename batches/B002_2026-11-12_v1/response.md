# Response — B002

I'll load the pair-discovery skill and follow it for batch B002.

**Pair Discovery: Batch B002**

**Run header**

- As-of date T: 2026-11-12
- Formation window: 2023-11-12 to 2026-11-12
- Trading window: 2026-11-13 onward. Never used for selection.
- Universe: US-listed equities and ETFs, price > $5, median daily dollar volume > $5M over the formation window, listed for the whole window. I did not compute liquidity; the screen must enforce it.
- Selector knowledge cutoff: end of June 2026
- Mode: **Forward.** T is after my cutoff, so the trading window is unseen.
- Batch ID: B002

**Structural checks (web, structural facts only).** These checks removed four ideas before registration. They were never screened, so they are not trials.

- **RIG/VAL:** Transocean expects to close its acquisition of Valaris on or about December 1, 2026, at a fixed exchange ratio. That makes the pair a merger arb, not a mean-reversion spread.
- **MTH/TMHC:** Berkshire agreed to buy Taylor Morrison for $72.50 per share in cash, after which it will be delisted.
- **RRC/AR:** EQT will acquire Range in an all-stock deal expected to close in Q1 2027.
- **BOH/FHB:** First Hawaiian is acquiring California-based TriCo Bancshares, expected to close by end of 2026. That breaks the "same isolated island economy" thesis.

I could not find `pair_registry.md` or any record of B001 in your Drive. B002 was therefore chosen without reference to B001 or its results.

**Candidate table**

Leg order is for record-keeping only. Trade direction comes from the signal.

| #   | Legs        | Link type           | Structural rationale (knowable at T)                                     | What would break it                                                                                               | Crowding check                       | Flags                        |
| --- | ----------- | ------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------- |
| 1   | AWR / CWT   | Narrow peers        | California water utilities, same CPUC rate-case regime                   | Large M&A; wildfire/liability event at one utility                                                                | Not a textbook pair                  | none                         |
| 2   | OGS / SR    | Narrow peers        | Pure-play gas distribution utilities, rate-base driven, rate-sensitive   | Takeover of either; major state rate-case shock                                                                   | Obscure                              | none                         |
| 3   | FBP / OFG   | Narrow peers        | Puerto Rico banks: same island economy and regulators                    | PR bank consolidation; mainland expansion by one                                                                  | Obscure                              | none                         |
| 4   | GBX / TRN   | Narrow peers        | Railcar builders with leasing fleets; same build cycle and lease rates   | One exits manufacturing; M&A                                                                                      | Low                                  | none                         |
| 5   | KNX / WERN  | Narrow peers        | Truckload carriers driven by the same contract/spot rate cycle           | Mix divergence: Werner bought FirstFleet to lift dedicated revenue ~50%                                           | Low                                  | none                         |
| 6   | AGCO / CNH  | Narrow peers        | #2/#3 global ag-equipment makers; same farm-income cycle                 | Large portfolio moves (AGCO's PTx shift); M&A                                                                     | Low                                  | none                         |
| 7   | FNF / FAF   | Narrow peers        | Title-insurance duopoly; premiums track home sales and mortgage volumes  | FNF's F&G annuity stake dominating; regulatory reform of title insurance                                          | Moderate (industry leaders, mid-cap) | none                         |
| 8   | LEA / ADNT  | Shared customer     | Seating suppliers to the same auto OEMs                                  | One wins or loses a major OEM program; M&A                                                                        | Low                                  | none                         |
| 9   | ONTO / NVMI | Shared customer     | Metrology/inspection tools sold into the same fab capex budgets          | Mix shift: Onto is buying a 27% stake in Rigaku, closing H2 2026                                                  | Low                                  | none                         |
| 10  | AR / CNX    | Shared output price | Appalachian gas producers, same basis differentials                      | Takeover premium after EQT/RRC; hedge-book divergence                                                             | Low                                  | none                         |
| 11  | AMR / HCC   | Shared output price | US met-coal exporters priced off the seaborne coking-coal benchmark      | Mine disaster; HCC Blue Creek ramp changing cost mix                                                              | Low                                  | none                         |
| 12  | ALB / SQM   | Shared output price | Major lithium producers exposed to the same lithium price                | Chile policy (Codelco JV terms); country-risk shock                                                               | Moderate                             | factor-mismatch              |
| 13  | UFPI / BLDR | Shared input        | Both driven by lumber prices and housing starts                          | BLDR's acquisitive push into manufacturing; UFPI packaging mix                                                    | Low                                  | factor-mismatch              |
| 14  | PBF / DK    | Shared input/output | Independent refiners, both on crack-spread economics                     | Refinery outage; asset sales; DK logistics restructuring                                                          | Low (VLO/MPC is the crowded one)     | none                         |
| 15  | LBRT / PUMP | Shared customer     | Pressure pumpers serving the same E&P completions budgets                | Both pivoting to power at different speeds (PROPWR targets ~2.6 GW by 2031; Liberty plans ~3 GW of power by 2029) | Low                                  | none                         |
| 16  | RS / NUE    | Supply chain        | Reliance's steel input cost is Nucor's output price                      | Steel tariff regime change; RS mix shift to aerospace                                                             | Low                                  | factor-mismatch              |
| 17  | SKYW / UAL  | Supply chain        | SkyWest flies capacity-purchase contracts, largely for United            | Contract loss or renegotiation; pilot-supply shock                                                                | Obscure                              | factor-mismatch              |
| 18  | LNG / CQP   | Ownership           | Cheniere controls CQP's GP and holds roughly half its units (verify %)   | CQP buy-in or simplification; distribution policy change                                                          | Moderate                             | borrow-risk                  |
| 19  | L / CNA     | Ownership           | Loews owns ~90% of CNA; CNA is most of Loews' earnings                   | Loews buys out CNA; large non-CNA deal at Loews                                                                   | Low                                  | liquidity-borderline         |
| 20  | BN / BAM    | Ownership           | Brookfield Corp owns ~73% of BAM (verify)                                | Stake sale; further restructuring                                                                                 | Low                                  | factor-mismatch              |
| 21  | IEP / CVI   | Ownership           | IEP holds a controlling stake (~two-thirds) in CVR Energy                | CVR's $4.2B refinery deal with Trafigura equity shifts both stake and economics; IEP distribution cuts            | Low                                  | borrow-risk, factor-mismatch |
| 22  | FMX / KOF   | Ownership           | FEMSA owns ~47% of Coca-Cola FEMSA                                       | FEMSA sells down KOF; OXXO retail mix dominating FMX                                                              | Low                                  | liquidity-borderline         |
| 23  | ITUB / BBD  | ADR peers           | Brazil's large private banks: same central bank, rates and regulator     | Credit-cycle divergence (BBD turnaround); M&A                                                                     | Moderate                             | none                         |
| 24  | KB / SHG    | ADR peers           | Korean bank holding companies under the same FSC and value-up program    | Capital-return policy divergence; Korea policy shock                                                              | Low                                  | liquidity-borderline         |
| 25  | PAC / ASR   | ADR peers           | Mexican airport concessions under the same tariff and master-plan regime | Concession/tariff reform hitting one; ASR's PR/Colombia mix                                                       | Low                                  | none                         |
| 26  | PSLV / SLV  | Identical claim     | Both hold physical silver; PSLV trades at a premium or discount          | Redemption-mechanism change; trust structure change                                                               | Moderate                             | none                         |
| 27  | URA / URNM  | Niche ETFs          | Overlapping uranium/nuclear holdings, different weights                  | Index methodology change; fund closure                                                                            | Low                                  | liquidity-borderline         |
| 28  | OIH / XES   | Niche ETFs          | Oilfield services, cap-weighted vs equal-weighted                        | Holdings drift (power pivots); fund closure                                                                       | Low                                  | liquidity-borderline         |

**Screening spec (frozen)**

- **Data:** daily bars, log prices adjusted for splits and dividends, formation window only. The universe is selected as of T and includes delisted names.
- **Cointegration:** Engle-Granger in both directions. Trials N = 28 pairs × 2 directions = **56 tests**. A pair passes if its smaller p-value survives Benjamini-Hochberg at q = 0.05 across all 56 tests (for reference, the Bonferroni threshold would be 0.05/56 ≈ 0.00089).
- **Hedge ratio:** OLS on the full window. Re-estimated on each half, both betas must fall within ±20% of the full-window beta. The ratio is then frozen.
- **Half-life:** AR(1) half-life between 5 and 60 trading days.
- **Zero-crossings:** at least 12 per year (≥ 36 over the window).
- **Signals:** z-score uses a 60-day rolling mean and standard deviation through t-1. Entry at |z| ≥ 2.0, exit at |z| ≤ 0.5, stop at |z| ≥ 3.5. A signal on bar t executes on bar t+1.
- **Costs:** model realistic spreads and slippage, using at least double the base assumption for `liquidity-borderline` legs. Charge actual borrow cost, with a high default for `borrow-risk` legs.
- **Delistings:** if either leg delists, close the pair at the last tradable price. Never drop it from results.

**Registry entry**

```
## Batch B002
- Registered: 2026-11-12
- As-of date T: 2026-11-12
- Selector: Claude Opus 5.5, knowledge cutoff 2026-06-30
- Mode: Forward
- Formation window: 2023-11-12 to 2026-11-12
- Trading window: 2026-11-13 to open (fix an evaluation end date before first look)
- Trials in this batch: 56 (28 pairs x 2 EG directions)   Cumulative trials on this trading window: 56 + B001's tests if B001's trading window overlaps (B001 record not found)
- Frozen thresholds: EG both directions, BH q=0.05 over 56 tests; hedge-ratio half-stability ±20%; half-life 5–60d; ≥12 zero-crossings/yr; z entry 2.0 / exit 0.5 / stop 3.5 (60d rolling, t-1)
- Pre-registration exclusions (not screened, not trials): RIG/VAL (pending merger), MTH/TMHC (cash takeout), RRC/AR (EQT acquiring RRC), BOH/FHB (FHB–TriCo mix change)
- Pairs:
  1 AWR/CWT – California water utilities, same CPUC regime
  2 OGS/SR – pure-play gas distribution utilities
  3 FBP/OFG – Puerto Rico banks
  4 GBX/TRN – railcar builders + lessors
  5 KNX/WERN – truckload carriers
  6 AGCO/CNH – ag equipment #2/#3
  7 FNF/FAF – title-insurance duopoly
  8 LEA/ADNT – seating suppliers, same OEMs
  9 ONTO/NVMI – metrology tools, same fab customers
  10 AR/CNX – Appalachian gas producers
  11 AMR/HCC – US met-coal exporters
  12 ALB/SQM – lithium producers
  13 UFPI/BLDR – lumber/housing input
  14 PBF/DK – independent refiners
  15 LBRT/PUMP – pressure pumpers
  16 RS/NUE – steel distributor vs mill
  17 SKYW/UAL – capacity-purchase supplier vs main customer
  18 LNG/CQP – parent vs controlled MLP
  19 L/CNA – holding co vs ~90% subsidiary
  20 BN/BAM – parent vs ~73% subsidiary
  21 IEP/CVI – holding co vs controlled refiner
  22 FMX/KOF – parent vs ~47% bottler stake
  23 ITUB/BBD – Brazilian private banks (ADRs)
  24 KB/SHG – Korean bank holding cos (ADRs)
  25 PAC/ASR – Mexican airport concessions (ADRs)
  26 PSLV/SLV – physical silver claims with trust friction
  27 URA/URNM – overlapping uranium ETFs
  28 OIH/XES – oil services ETFs, cap vs equal weight
- Pairs (paste): AWR/CWT,OGS/SR,FBP/OFG,GBX/TRN,KNX/WERN,AGCO/CNH,FNF/FAF,LEA/ADNT,ONTO/NVMI,AR/CNX,AMR/HCC,ALB/SQM,UFPI/BLDR,PBF/DK,LBRT/PUMP,RS/NUE,SKYW/UAL,LNG/CQP,L/CNA,BN/BAM,IEP/CVI,FMX/KOF,ITUB/BBD,KB/SHG,PAC/ASR,PSLV/SLV,URA/URNM,OIH/XES
- Status: registered, not yet screened
```

**Caveats**

- Two kinds of facts were not verified this session. Ownership percentages come from memory (marked "verify"); confirm them from the latest filings. Pending deals were checked only for the names listed in the structural checks above. For the other names, scan for pending M&A as of T before screening, because a stock-for-stock deal can look like a perfect cointegrated pair.
- No pair was chosen or dropped because of how its prices or spread behaved, so none carries a `hindsight-risk` flag.

**Weakest candidates**

- **IEP/CVI:** CVR's new refinery deal and Trafigura equity raise change both IEP's stake and CVR's economics, and IEP is hard to borrow.
- **PSLV/SLV:** the spread is mostly trust premium/discount noise, so costs will probably swamp it.
- **LBRT/PUMP and SKYW/UAL:** both carry a business-mix or factor gap large enough that the spread may trend rather than revert.

Sources:

- [Transocean schedules shareholder vote and court hearing for Valaris acquisition (Investing.com)](https://www.investing.com/news/sec-filings/transocean-schedules-shareholder-vote-and-court-hearing-for-valaris-acquisition-93CH-4970436)
- [Berkshire Hathaway to buy Taylor Morrison (investingLive)](https://investinglive.com/stock-market-update/berkshire-hathaway-to-buy-taylor-morrison-in-85bn-all-cash-housing-deal-20260531/)
- [EQT to acquire Range Resources (Benzinga via Webull)](https://www.webull.com/news/15813962700804096)
- [First Hawaiian to acquire TriCo Bancshares (InsideArbitrage)](https://www.insidearbitrage.com/?p=173019)
- [CVR Energy to buy two Marathon refineries (Credence Research)](https://www.credenceresearch.com/news/cvr-energy-acquire-marathon-refineries-st-paul-park-mandan-4-2-billion)
- [Werner acquires FirstFleet (Pulse 2.0)](https://pulse2.com/werner-acquires-firstfleet-to-expand-dedicated-trucking-scale-and-earnings/amp/)
- [Onto Innovation acquires 27% stake in Rigaku (Pulse)](https://www.pulse.bot/ai/deals/onto-innovation-acquires-27-stake-in-japans-rigaku-for-710m-c1136193-4b3e-448b-8338-d77896b034b0/)
- [PROPWR framework agreement with Caterpillar](https://www.caterpillar.com/en/news/corporate-press-releases/h/pro-pwr-agreement.html)
- [SLB and Liberty Energy alliance (Oil & Gas 360)](https://www.oilandgas360.com/?p=1048717)
