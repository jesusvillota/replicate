---
id: TASK-023
title: 'Comparison: main-run discovery and canonical exports'
milestone: M-3
state: approved
depends_on: [TASK-022]
delivery: pr
---

## Why

Serves SC-5. TASK-018 found two defects in `rebal.compare`: issue [#28](https://github.com/jesusvillota/replicate/issues/28) (recursive discovery can pick robustness CSVs instead of the main results) and issue [#29](https://github.com/jesusvillota/replicate/issues/29) (costs, Table 6 and all quantitative core figures use layouts that do not join to `docs/results/targets.csv`). With them, the default report shows 252 of 399 targets and needs a manual workaround. The final report needs every available target to join.

## Scope

Change `src/rebal/compare.py`, the exporters `src/rebal/exhibits/{costs,strategy,calibration_figures,horizon_figures}.py`, their tests, and `docs/methods/comparison.md`. Do not change `docs/results/targets.csv` except to fix a proven key typo, and say so.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**1. Discovery (#28).** By default the real run reads only the main outputs: `output/tables/*.csv` and `output/figures/*.csv`, not the `robustness/` subfolders. Add an explicit option to compare one variant, for example `--variant literal`. Test it with distinct main and robustness values, as the issue describes.

**2. Canonical exports (#29).** For each exhibit that is skipped today (`costs`, `table_6a`, `table_6b`, `table_6c`, `figure_2`, `figure_3`, `figure_4`, `figure_6`, `figure_D1`–`figure_D5`), add a canonical comparison CSV in the key layout of `docs/methods/comparison.md`: `exhibit,column,term,stat,value`, with `column`, `term` and `stat` equal to the keys in `targets.csv`. Keep the plotted-data files, and name the new files so that `compare` finds them (document the naming rule). TASK-022 fixes the cost values and units; build on the merged `costs.py`. Do not guess Figure 6 axis transformations or the sign convention of the random-date cost (paper-notes §3.8 notes the conflict); leave those targets unmatched and list them with the reason.

**3. Report.** `compare` lists, for every target that stays unmatched, a reason: no export, paper-only data, or not available. Targets of data we cannot get (FEARS, ANcerno) are listed as `not available`, not as failures.

Out of scope: new exhibits (TASK-024 to TASK-028), cost methodology (TASK-022).

## Acceptance

- `uv run pytest -q tests/test_compare.py` passes. It includes tests for the default main-only discovery, the `--variant` option, and the join of at least one canonical export per exhibit group above.
- `uv run python3 -m rebal.exhibits --all --demo` exits 0 and the demo outputs include the canonical exports.
- On the demo outputs, `uv run python3 -m rebal.compare --demo` (or the module's documented demo option) reports every core exhibit above as joined, and lists each unmatched target with a reason.

## Verify

```sh
uv run pytest -q tests/test_compare.py tests/test_costs.py tests/test_strategy.py tests/test_horizons.py
uv run python3 -m rebal.exhibits --all --demo
uv run python3 -m rebal.compare --help
```
