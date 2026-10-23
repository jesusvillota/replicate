---
id: TASK-027
title: 'Figure 1: pension-allocation code on demo data'
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-6. Figure 1 of the paper shows the equity share of U.S. public defined-benefit pension plans, actual and target, for FY2003–2022 (paper-notes §4, D23). It motivates the paper: plans rebalance toward a target. This task builds the code on demo data; TASK-030 runs it on real data.

## Scope

Module: `src/rebal/exhibits/pension.py` (exhibit `figure_1`). Test: `tests/test_pension.py`. Methods doc: `docs/methods/pension.md`.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**Inputs.** `data/public/ppd/ppd_allocations.csv` and `ppd_coverage.csv` (TASK-008; read `docs/data/cards/ppd.md` first). Fiscal years 2003–2022.

**Method.** For each fiscal year compute the plan-weighted (by assets) mean actual public-equity share and the mean target share. Document in the methods doc:
- the weighting, and the effect of the plan coverage changing over the years (report the number of plans per year);
- how plans with a missing target or a missing actual share are handled (sparse target fields; drop and count, never fill);
- the definition of public equity (which PPD fields).

**Output.** Plot actual and target share by fiscal year. Write the plotted data to `output/figures/figure_1.csv` in the comparison key layout `exhibit,column,term,stat,value` with the keys of `docs/results/targets.csv`: `column` = `equity_share`; `term` = `actual_min`, `actual_max` (the range of the yearly actual share), `target_typical` (the typical target, the median over years); `stat` = `value`. Add a second, clearly named file only if you need yearly values (`output/figures/figure_1_yearly.csv`), and document it.

**Tests.** On a synthetic plan table with known shares, the weighted mean and the range match a hand calculation; a plan with a missing target is excluded from the target mean only; the number of plans per year is reported.

Out of scope: the real run; the pension roundtable and survey material (D28).

## Acceptance

- `uv run pytest -q tests/test_pension.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only figure_1` writes `output/demo/figure_1.pdf` and `output/demo/figure_1.csv` with the comparison keys.
- `docs/methods/pension.md` states the weighting, the plan counts per year and the missing-field rules.
- The outcome gives the real-data smoke values (actual min and max, typical target) next to the paper (about 0.63, 0.68 and 0.65).

## Verify

```sh
uv run pytest -q tests/test_pension.py
uv run python3 -m rebal.exhibits --all --demo --only figure_1
ls output/demo/figure_1*
```
