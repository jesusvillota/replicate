---
id: TASK-028
title: 'Figure 5: trading-correlation code on demo data'
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-6. Figure 5 correlates the rebalancing signals with the trading of different investor groups (paper-notes §3.7 and §4): CFTC hedgers and speculators, CFTC LTPos asset managers and leveraged funds, and ICI mutual-fund flows. The ANcerno panel is not available. This task builds the code on demo data; TASK-030 runs it on real data.

## Scope

Module: `src/rebal/exhibits/trading_corr.py` (exhibit `figure_5`). Test: `tests/test_trading_corr.py`. Methods doc: `docs/methods/trading_corr.md`.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**Inputs.** `data/public/cftc/` (legacy COT `cot_legacy.csv`, TFF `tff.csv`, `ltpos.csv`; TASK-007) and the ICI weekly flows (`$REPLICATE_DATA_DIR/licensed/ici/ici_weekly_flows.csv`; TASK-008). Read the source cards `docs/data/cards/cftc.md` and `ici.md` first. The signals come from `rebal.io.load_signals`.

**Settle §5.11 and §5.12 in the methods doc.**
1. CFTC: legacy or TFF (the paper's August 2006 start matches TFF; default is the legacy report for hedgers and speculators, the TFF report for asset managers and leveraged funds, so decide and say why); the S&P contract (E-mini or the large contract); whether Q is the S&P change minus the 10-year change; Q as in Kang, Rouwenhorst and Tang (2020): the net position change between t+1 and t scaled by open interest.
2. Alignment of Tuesday positions to daily signals: the lag, and the weekly aggregation of the signals (default: the signal on the Tuesday report date, lagged as the paper says).
3. LTPos: the file holds weekly mean *daily* directional changes, not weekly position differences. Do not treat it as a weekly difference. State the aggregation.
4. ICI: equity flows minus bond flows. The data come in 39 disjoint blocks. Correlate within blocks and pool; never bridge a gap. Report N per block.
5. ANcerno: not available. Do not produce a column for it; say so in the methods doc.

**Output.** A bar or dot plot of the correlations. Write `output/figures/figure_5.csv` in the comparison key layout `exhibit,column,term,stat,value` using the keys of `docs/results/targets.csv`: `column` in `cftc_hedgers`, `cftc_speculators`, `ltpos_asset_managers`, `ltpos_leveraged_funds`, `ici`; `term` in `threshold`, `calendar`; `stat` = `value`. Add the number of observations as `stat` = `nobs`.

**Tests.** A planted correlation between a synthetic weekly series and the lagged signal is recovered; the lag direction is right (the signal at t does not correlate with the position at t−1); the ICI blocks are not bridged.

Out of scope: the real run; ANcerno; the 3:30 PM check.

## Acceptance

- `uv run pytest -q tests/test_trading_corr.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only figure_5` writes `output/demo/figure_5.pdf` and `output/demo/figure_5.csv` with five `column` values and no ANcerno row.
- `docs/methods/trading_corr.md` records every choice above.
- The outcome gives the real-data smoke correlations next to the paper (hedgers −0.10 / −0.13, speculators +0.11 / +0.17, asset managers −0.08 / −0.12, leveraged funds +0.18 / +0.13, ICI −0.17 / −0.19).

## Verify

```sh
uv run pytest -q tests/test_trading_corr.py
uv run python3 -m rebal.exhibits --all --demo --only figure_5
ls output/demo/figure_5*
```
