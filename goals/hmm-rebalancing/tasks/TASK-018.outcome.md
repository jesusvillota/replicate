# TASK-018 outcome

## Acceptance

1. [x] `uv run python3 -m rebal.exhibits --all` exited **0** (`exit=0`).
   `ls output/tables output/figures` showed every SC-3 core exhibit, `costs`,
   and `table_6a`–`table_6c`. An independent inventory assertion passed:
   **21 required table CSVs and 10 figure CSV/PDF pairs**. This includes
   Figure 6 and Figure D.5. `magnitudes.csv` is also committed.
2. [x] `docs/results/core.md` exists. Its main-run summary gives
   **97.5% sign matches (116/119)** and **85.9% significance matches (85/99)**.
   The generator joins **252/399 target statistics**. These are rates among
   eligible joined targets, not all core results. Direct comparisons cover
   costs, Table 6 and figures whose exports do not join automatically.
3. [x] The side-by-side headline values appear below and in the report's
   “Reading the gaps” section. These quote the actual main CSVs, not a
   robustness variant. Cost replication fails economically; raw outputs remain.
4. [x] Table 1 column (1), coefficient and t-statistic:

   | Term | Paper coefficient (t) | Main coefficient (t) |
   |---|---:|---:|
   | Threshold | −0.4144 (−3.6098) | −0.464414 (−4.012118) |
   | Cal × week4 | −0.3029 (−3.7488) | −0.260256 (−3.418693) |

   Paper t-statistics divide printed coefficients by printed standard errors
   (0.1148 and 0.0808). Both main effects are negative and significant at 5%.
   Main HC1 estimates use **6,317 pairs**, versus paper **6,226**.
5. [x] Headline annual cost: **4,193.686081 bps** versus paper **8 bps**;
   **$8,387,372,162,951/year** on $20T versus paper **$16,000,000,000/year**.
   These are raw outputs, not validated economic costs. The unit mismatch
   and extreme zero-threshold contribution are documented in issue #30.
6. [x] Gross strategy Sharpe ratio: **0.734083**, versus paper **1.11**.
   `output/tables/table_6a.csv` reports mean **6.449676%/year** and volatility
   **8.786029%/year**, versus paper **10.20%** and **9.17%**.
7. [x] `uv run pytest -q` passed on the merged analysis code:
   **314 passed, 4 warnings in 189.53s (0:03:09)**, exit **0**.
   Warnings come from escape sequences in the installed WRDS dependency.
   The complete exact Verify block exited **0**. `git diff --check` passed.

## Summary

Ran the merged code on the MacBook, with DEC-001 main E1/T3 proxies and clean
signal timing. Panel validation ended `PANEL OK`. Both clean and literal
signal builds wrote **8,275 rows and 63 columns**. Earlier history initializes
signals; the study has **6,318 panel rows**, 1997-09-10–2023-03-17.
No analysis code, tests, task specs, other outcomes, decisions or goal.yaml
were changed. No data was downloaded, no cluster job ran, and no licensed or
processed input entered git. This branch stays `goal/hmm-rebalancing/task-018`.

Verified analysis revision: `07a995b2ccc54e37cbd86492cd720384f39d12dd`, also
`origin/main` at final fetch. The branch rebased onto it without conflicts.
The delivery commits contain artifacts and documentation only. Main-run
sidecars record parameters and samples. Robustness run sidecars also record
panel hashes, timing, selected outputs and the same analysis revision.

Committed the requested robustness artifacts:

- `output/tables/robustness/literal/table_1.csv` and
  `output/figures/robustness/literal/figure_2.{csv,pdf}`.
- `output/tables/robustness/proxy_alt/{table_1,table_3,costs}.csv`.

Existing `predictive_tables.build_tables` and `calibration_figures.build_figures`
produced the selected robustness tables/figure. The alternative panel was loaded
from `daily_panel_alt.parquet`; `signals.build` rebuilt all clean signals over
its full history, including `r_sp500tr`. The existing `costs.run` was called
with its panel/signal loaders and output directory temporarily redirected in
that process. Defaults remained 10,000 schedules, seed 16 and HC1. No shared
panel or signal file was replaced. Only the requested outputs were retained.

Literal Table 1 gives Threshold **−0.269997 (t=−2.729659)** and Calendar
**−0.260521 (t=−3.366775)**. Alternative-proxy Table 1 gives
**−0.377347 (t=−3.389297)** and **−0.223696 (t=−3.126650)**.
Both variants retain the headline signs and 5% significance. Alternative-proxy
cost is **5,552.083 bps**, so it does not resolve the cost failure.
The report provides Figure 2 and Table 3 robustness readings beside the main run.

The report explains sign, size and significance gaps, cites
`docs/data/proxy_comparison.md`, and distinguishes proxy, timing, sample and
paper-notes §5 method limits. It includes direct readings for all targeted
available figures, cost components, dollar scaling and Table 6 A–C.
It identifies the absent catalogue targets for D.2, D.5 and D.13 and gives
selected existing estimates without claiming unsupported match rates.
All **11 PDF files** (ten main and one literal robustness) were rendered with
Poppler and visually inspected. Labels, legends and confidence bands are readable.

### Proposed follow-ups

Per task scope, the following merged-code problems were reported, not fixed:

- https://github.com/jesusvillota/replicate/issues/28 — recursive comparison
  discovery can select robustness CSVs before the main CSVs. Reproduced with
  distinct main −0.4 and robustness −0.2 values: the report selected −0.2.
- https://github.com/jesusvillota/replicate/issues/29 — existing costs, strategy
  and figure layouts/keys prevent automatic target joins. Direct report
  comparisons preserve their real values without changing analysis exports.
- https://github.com/jesusvillota/replicate/issues/30 — cost-unit audit needed.
  `annual_cost(-0.39, 0.01, 12)` gives **468 bps**, versus the paper's worked
  example of approximately **5 bps**. Zero-threshold impact is **−8.37734**;
  its fixed-1%-trade cost is **211,108.96 bps** and dominates the mean.
  Its design is full rank (6,317 × 7, rank 7); no exact-collinearity claim is
  made. The initial issue text overstated collinearity and was corrected
  after direct rank and residual checks. No replacement method is chosen here.

These findings limit empirical agreement but do not prevent the requested
run, comparisons and local verification. No access, data or new decision is
missing for this task. No material method change was made. The cost number
must not be read as successful economic replication.

## Verify evidence

The exact user/spec block ran locally and exited **0**:

```sh
uv run python3 -m rebal.panel --check | tail -1
uv run python3 -m rebal.signals --build --timing clean && uv run python3 -m rebal.signals --build --timing literal
uv run python3 -m rebal.exhibits --all; echo "exit=$?"
uv run python3 -m rebal.compare --out docs/results/core.md && sed -n '1,40p' docs/results/core.md
uv run pytest -q
```

Output included `PANEL OK`, both 8,275-row signal builds, `6 exhibit modules`
and `exit=0`. Its final tail was:

```text
.................................................................... [ 91%]
..........................                                               [100%]
=============================== warnings summary ===============================
[4 SyntaxWarning entries in installed wrds/sql.py]
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
314 passed, 4 warnings in 189.53s (0:03:09)
```

That first comparison encountered issue #28 because robustness outputs already
existed. After it, the main comparison command was repeated with both
`output/{tables,figures}/robustness` directories moved to a temporary folder
outside `output/`. A `try/finally` restored them immediately after comparison.
No main CSV changed. The corrected report printed:

```text
Comparison report: docs/results/core.md
Targets matched: 252/399
Sign-match rate: 97.5% (116/119 eligible targets)
Significance-match rate: 85.9% (85/99 eligible targets)
Skipped CSVs: 17
```

“Reading the gaps” was then appended, as required by the spec. To regenerate
that baseline summary before the discovery follow-up lands, temporarily move
both robustness directories outside the input roots, run the same comparison
command, restore both directories, and retain the hand-written section.
A direct read of `table_1.csv` independently confirmed the reported main
coefficients. Local verification determines delivery. GitHub Actions were
not read or used; no merge was performed.
