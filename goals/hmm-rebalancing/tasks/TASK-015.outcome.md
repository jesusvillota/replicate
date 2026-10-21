# TASK-015 outcome

## Acceptance

- [x] `uv run pytest tests/test_horizons.py` passes: **9 passed in 6.62s**
  on macOS, Python 3.13.7. The fixed-seed, 200-draw null experiment reports
  **Hodrick 1B rejection rate: 5.0% (10/200)**, inside the required 2%–10%
  interval. Naive overlapping OLS rejects **35.5% (71/200)**, which is higher.
  Figure 2 at delta=0 reports **t=-17.262835**, below -3, with coefficient
  -0.710192 and 6,657 observations. Tests also cover a zero planted effect,
  independent covariance and return-timing oracles, conditional subsets,
  sample boundaries, confidence bands, and CSV values against plot artists.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only figure_2 figure_3 figure_4 figure_D1 figure_D2 figure_D3 figure_D4`
  exits **0** and writes **7 PDFs and 7 CSVs** to `output/demo/`. An independent
  file check confirmed all 14 requested artifacts exist and are nonempty.
  The CSV row counts are 42, 10, 30, 42, 10, 82 and 30, respectively.
  All seven PDFs were rendered with Poppler and visually inspected; labels,
  legends, reference lines and confidence bands are readable without clipping.

The complete task Verify block exited **0** on implementation revision
`b170625117631afc3e83fe7d566b442027461f25`, after a conflict-free rebase onto
`origin/main`:

```sh
uv run pytest -q tests/test_horizons.py
uv run python3 -m rebal.exhibits --all --demo --only figure_2 figure_3 figure_4 figure_D1 figure_D2 figure_D3 figure_D4
ls output/demo/figure_*
```

The test output was **9 passed in 6.23s**. The runner reported **2 exhibit
modules**. The final listing was:

```text
output/demo/figure_2.csv
output/demo/figure_2.pdf
output/demo/figure_3.csv
output/demo/figure_3.pdf
output/demo/figure_4.csv
output/demo/figure_4.pdf
output/demo/figure_C1.csv
output/demo/figure_C1.pdf
output/demo/figure_D1.csv
output/demo/figure_D1.pdf
output/demo/figure_D2.csv
output/demo/figure_D2.pdf
output/demo/figure_D3.csv
output/demo/figure_D3.pdf
output/demo/figure_D4.csv
output/demo/figure_D4.pdf
```

The extra C1 pair comes from the existing full-suite scaffold smoke test,
which invokes all discovered demo exhibit modules. The TASK-015 command
writes only its seven requested pairs and two JSON lineage files.

Additional local checks:

- `uv run pytest -q`: **107 passed in 23.92s**.
- `uv run --with ruff ruff check` on the five new Python files:
  **All checks passed!** Ruff is supplied as a temporary tool dependency;
  the project does not install it by default.
- `uvx ruff format --check` on those files: **5 files already formatted**.
- `git diff --check`: exits **0**.
- Both new module CLIs with `--help`: exit **0**.

## Summary

Added the five calibration figures in `calibration_figures.py` and two
horizon figures in `horizon_figures.py`. They reuse `rebal.regress.ols`,
`predictive` and `predictive_data`. A private shared renderer consumes the
same tables written to the CSVs. Module discovery needs no runner changes.

Added `rebal.regress_hodrick.hodrick` with the Hodrick 1B covariance. It
reverses the overlapping-horizon score into one-day null innovations times
backward regressor sums. Retained origins determine both sample edges and
missing-origin contributions. Figure 4 uses cumulative `log1p(ret)`;
Figure D4 uses individual simple returns at each future trading day.

`docs/methods/horizons.md` records the formula, units, sample timing, HC1
and HAC defaults, undefined subsets, log-return choice and CLI overrides.
Figure D3 explicitly records non-estimable subsets rather than inventing
zero estimates. The demo's empty delta=0 non-rebalancing subset is expected.
There are no material decisions or task-scope deviations. Demo outputs remain
ignored; no real-data run or cluster job was needed or performed.

Verified implementation: `b170625117631afc3e83fe7d566b442027461f25`.
This outcome is a documentation-only follow-up commit in the same PR.
PR: https://github.com/jesusvillota/replicate/pull/21, targeting `main`.
Proposed follow-up: the already planned TASK-018 real-data exhibit run.
No task specifications, other task outcomes, decisions or goal configuration
were edited.
