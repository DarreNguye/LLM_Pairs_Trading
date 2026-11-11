---
name: "pair-discovery"
description: "Propose non-obvious, uncrowded candidate pairs for a pairs-trading (spread mean-reversion) strategy with strict data-leakage controls. Use whenever Darren asks for new pairs, pair ideas, candidates to backtest, or whether a pair is too crowded."
---

# Pair Discovery

Propose candidate pairs for a spread mean-reversion strategy. The pairs go into Darren's QuantConnect backtester, whose job is to judge whether his selection process finds pairs that make money. That makes this skill the *selection process under test*, so two things matter more than cleverness:

1. **The pairs must not be crowded.** Textbook pairs are arbitraged by everyone; whatever edge they had is gone after costs.
2. **The selection must not leak.** If the choice of a pair was informed, even indirectly, by how that pair behaved during the period it is later tested on, the backtest measures hindsight, not skill.

Read the leakage section before proposing anything. It changes how you should think, not just what you output.

## Step 0: Fix the frame before generating ideas

Establish these first. Ask only for what is missing; otherwise state the default you used.

- **As-of date (T):** the date the selection is pretending to be made. Default: today.
- **Formation window:** data used to screen pairs statistically. Default: the 3 years ending at T.
- **Trading window:** strictly after T. Never used for any selection decision.
- **Universe and liquidity floor:** default US-listed equities and ETFs, price > $5, median daily dollar volume > $5M over the formation window, listed for the whole formation window.
- **Batch size:** default 8 to 12 candidates. Most should fail screening; that is expected.

Then state your own knowledge cutoff and classify the run:

- **Forward mode (T at or after your knowledge cutoff):** the trading window is genuinely unseen. This is the only clean evidence of returns.
- **Historical mode (T before your knowledge cutoff):** you have seen what happened next. Results are *contaminated* and are useful for debugging the pipeline and comparing against a baseline, not as proof the selection works. Say this plainly at the top of the output, every time.

## Leakage controls

There are three separate leaks. Guard against each.

### 1. Selector leakage (you)

You cannot un-know what you were trained on. You know which companies went bankrupt, got acquired, re-rated, or diverged. A pair that "feels" stable may feel that way because you know it stayed stable. Mitigations:

- **Justify every pair by a structural link that was knowable at T**, such as shared input costs, the same regulator and rate regime, a holding-company stake, the same end customer. Never justify a pair by how the prices or the spread behaved.
- **Do not recall or reason about price paths, returns, correlations, or events after T.** If you notice your reason for liking or rejecting a pair depends on something after T, drop that reasoning and flag the pair `hindsight-risk`.
- **Do not quote statistics from memory** (correlation, cointegration p-values, half-lives). You are not computing them, so any number you produce is either invented or leaked. Statistics come only from the formation-window screen.
- **Do not prune by survival.** Include candidates you suspect later broke. A list containing only pairs that survived is itself a leak.
- **Web search:** in historical mode, do not search, because results carry post-T information. In forward mode, searching for current structural facts (ownership stakes, business mix, listing status) is fine.

### 2. Screening leakage (the statistics)

- All statistical tests, hedge ratios, and thresholds are fitted on the formation window only and then frozen.
- Count the trials. If N candidates are screened, apply a multiple-testing correction (Bonferroni or Benjamini-Hochberg) rather than a raw p < 0.05. Screening 100 pairs at 5% yields about 5 false positives by chance.
- Use a point-in-time universe including delisted names. QuantConnect's equity data is survivorship-bias free; keep it that way by selecting the universe as of T, not as of today.

### 3. Iteration leakage (the loop)

The quiet one: run a batch, look at trading-window results, ask for "better" pairs, repeat. After a few rounds the selection has been fitted to the test period.

- **Pre-register every batch before any backtest runs** (see the registry format below).
- Never revise, drop, or replace a registered pair after seeing its results. Failed pairs stay in the registry.
- If asked for a new batch after results on the same trading window have been seen, say that the window is now spent for evaluation and recommend a fresh, later window.
- Do not use past batch results to steer new picks unless the new picks are tested on data later than everything already viewed.

## Finding uncrowded pairs

### What counts as crowded

Exclude a pair if any of these hold:

- It appears as an example in textbooks, tutorials, blog posts, or platform docs. **Ease-of-recall test:** if the pair comes to mind instantly as "a classic pairs trade", that is the evidence it is crowded.
- Both legs are the mega-cap leaders of the same industry.
- It is a well-known ETF pair or share-class pair.

Non-exhaustive blocklist to illustrate the type: KO/PEP, XOM/CVX, V/MA, HD/LOW, GM/F, UPS/FDX, JPM/BAC, GS/MS, WMT/TGT, GLD/GDX, GLD/SLV, SPY/IVV, QQQ/XLK, EWA/EWC, GOOG/GOOGL, BRK.A/BRK.B.

### Where to look instead

Prefer links that need some domain knowledge to spot, in names with enough liquidity to trade but little analyst and quant attention:

- **Narrow sub-industry peers in mid and small caps**, where both firms have nearly the same business mix (for example two regional operators under the same regulatory regime, two single-product processors of the same commodity).
- **Shared-input or shared-customer exposure** across different industries, where both are driven by the same cost or demand factor.
- **Supply-chain links**, where one firm's revenue is largely the other's spend.
- **Ownership links**: a holding company versus its listed stake, a parent versus a partially listed subsidiary.
- **Cross-listed or economically identical claims** with a persistent friction: ADR versus a close local-market proxy, closed-end fund versus its liquid underlying basket.
- **Niche ETF versus a peer ETF or tight basket** tracking overlapping but not identical holdings.

Balance the batch across at least three of these link types so one bad idea-family does not sink the whole batch.

### The tradeoff to keep honest

Uncrowded usually means less liquid. Every candidate must pass the liquidity floor, and the handoff must tell the backtester to model realistic spreads, slippage, and short-borrow cost. A pair that only works at zero cost is not a find.

Prefer pairs where the two legs have similar market cap, beta, and sector exposure, so the spread isolates the relationship rather than a hidden factor bet.

## Formation-window screen (spec for the backtester or research notebook)

You propose; the data disposes. Hand over this spec rather than guessing outcomes. Defaults assume daily bars and can be overridden:

- Log prices, adjusted for splits and dividends, formation window only.
- Engle-Granger cointegration tested in both directions; require significance after multiple-testing correction.
- Hedge ratio by OLS (or total least squares), then checked for stability across two halves of the formation window.
- Spread half-life (from an AR(1) fit) between 5 and 60 trading days.
- A minimum number of spread zero-crossings (default 12 per year) so the result is not driven by one episode.
- Entry, exit, and stop z-score thresholds fixed now, before the trading window is touched.

Backtester reminders to include in the handoff: rolling statistics use data through t-1 only; signals on bar t execute on bar t+1; a pair where either leg delists is closed at the last tradable price, not dropped from results.

## Output format

Use this structure.

**Run header:** as-of date, formation window, trading window, universe and liquidity floor, your knowledge cutoff, mode (Forward or Historical-contaminated), batch ID.

**Candidate table**, one row per pair:

| # | Long/short legs | Link type | Structural rationale (knowable at T) | What would break it | Crowding check | Flags |

- *What would break it* names the specific event that would end the relationship (M&A, business-mix shift, regulatory change). This is the stop-loss thesis.
- *Flags* uses: `hindsight-risk`, `liquidity-borderline`, `borrow-risk`, `factor-mismatch`, or none.

**Screening spec:** the frozen thresholds from the section above, with the number of trials N for the correction.

**Registry entry:** a block ready to append to `pair_registry.md`:

```
## Batch <ID>
- Registered: <today's date>
- As-of date T: <date>
- Selector: <model name>, knowledge cutoff <date>
- Mode: Forward | Historical-contaminated
- Formation window: <start> to <T>
- Trading window: <T+1> to <end>
- Trials in this batch: <N>   Cumulative trials on this trading window: <total>
- Frozen thresholds: <cointegration alpha after correction, half-life range, z entry/exit/stop>
- Pairs: <list with one-line rationale each>
- Pairs (paste): <every pair as A/B, comma-separated, no spaces, same order and leg order as the candidate table>
- Status: registered, not yet screened
```

End with one or two lines naming the weakest candidates and why, so expectations are set before results exist.

## What not to do

- Do not promise or estimate returns, Sharpe, or win rates for any pair.
- Do not present a historical-mode batch as evidence that the selection works.
- Do not pad the batch with crowded pairs to reach the batch size. Return fewer and say so.
- Do not quietly swap a registered pair. Register a new batch instead.