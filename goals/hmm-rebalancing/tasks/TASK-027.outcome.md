# TASK-027 outcome

## Acceptance

- [x] `uv run pytest -q tests/test_pension.py` passes.
  Evidence: 12 tests passed in this session. Tests cover hand-calculated
  asset-weighted means and ranges, independent missing-field exclusions,
  contributing counts, invalid assets, reported zeros, empty years, equal
  weights, planted and zero gaps, comparison keys, plotted values, and coverage validation.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only figure_1`
  writes `output/demo/figure_1.pdf` and `output/demo/figure_1.csv`.
  Evidence: the command and `ls output/demo/figure_1*` exited 0.
  The CSV columns are `exhibit,column,term,stat,value`. The keys are
  `figure_1,equity_share,{actual_min,actual_max,target_typical},value`.
  Demo values are 0.625, 0.675 and 0.65. The key test compares against
  `docs/results/targets.csv`. The command also writes `figure_1_yearly.csv`
  and `pension.metadata.json`. Poppler rendering and visual inspection
  confirmed readable labels, separate actual and target lines, and no clipping.
- [x] `docs/methods/pension.md` states weighting, plan counts per year,
  and missing-field rules.
  Evidence: it defines the asset-weighted ratio with separate denominators,
  the public equity fields, all 20 years of raw and contributing plan counts,
  missing-share counts, invalid-asset counts, and no-fill rules.
- [x] Real-data smoke values are recorded next to the paper values.
  Evidence: a real `run(demo=False)` read the committed PPD allocations and
  coverage and wrote all four outputs into a temporary directory. Independent
  arithmetic with Python `csv`, weighted sums, and `statistics.median`
  matched all three results to within 1e-12. The temporary files were removed.

| Comparison key | Real-data smoke | Paper, approximate | Real minus paper |
|---|---:|---:|---:|
| `actual_min` | 0.412023020200 | 0.63 | -0.217976979800 |
| `actual_max` | 0.619531886112 | 0.68 | -0.060468113888 |
| `target_typical` | 0.483314542027 | 0.65 | -0.166685457973 |

## Summary

Added `src/rebal/exhibits/pension.py`, `tests/test_pension.py` and
`docs/methods/pension.md`. The existing discovery runner finds `figure_1`
without a shared registration change. The module reads PPD allocations and
checks source coverage. DuckDB computes annual asset-weighted actual and target
means independently. The module exports comparison keys, exact annual plotted
values and counts, a PDF, and lineage metadata. The CLI exposes equal weights
and sample-year overrides for sensitivity checks.

The implementation followed three steps: define the available-case aggregation,
add deterministic pension fixtures and hand-calculation tests, then verify exports
and document the real-data smoke. No shared modules, contracts, task specifications,
other tasks, decisions or goal configuration were changed. No cluster jobs were used.

Deviation: the shared `rebal.demo` and `rebal.io` fixtures do not provide pension
allocations. The module therefore owns its synthetic plan table. Shared files
remain unchanged. The fixture has unequal assets, changing plan coverage, sparse
targets, and known annual gaps. Tests also verify a zero-gap variant.

Verified implementation revision: `893ef22b59a4b39f1591667dc9f7abc0cbcd012e`,
after rebasing this branch onto `origin/main` without conflicts.
The outcome commit adds this report only.

Validation in this session:

```sh
uv run pytest -q tests/test_pension.py
uv run python3 -m rebal.exhibits --all --demo --only figure_1
ls output/demo/figure_1*
uv run --with ruff ruff check src/rebal/exhibits/pension.py tests/test_pension.py
uv run python3 -m rebal.exhibits.pension --help
uv run pytest -q tests/test_scaffold.py::test_exhibit_discovery_and_selection
```

All passed. Ruff was run through `--with ruff` because it is not a project dependency.
The runner discovery test passed (1 test). The required Verify command block
exited 0. Its output includes:

```text
............                                                             [100%]
12 passed
1 exhibit modules
output/demo/figure_1.csv
output/demo/figure_1.pdf
output/demo/figure_1_yearly.csv
```

No real exhibit outputs were written under `output/`; the real smoke used a
temporary output directory. Demo files remain ignored. No real outputs are committed.
GitHub Actions were not read or used. Local verification determines delivery.

Proposed follow-up for TASK-030: report the substantial real-data gap and investigate
sample or source-vintage differences. The current PPD has 253 rows every year,
but only 172–228 actual contributors and 136–234 target contributors.
The fixed method required by this task was not changed to fit the paper.
This task delivers the code and records the mismatch; the final real run belongs to TASK-030.

Delivery PR: https://github.com/jesusvillota/replicate/pull/36
Base: `main`. Branch: `goal/hmm-rebalancing/task-027`.
