# TASK-014 outcome

## Acceptance

- [x] `uv run pytest tests/test_regress.py` passes. The exact Verify command,
  `uv run pytest -q tests/test_regress.py`, printed **15 passed in 4.13s**.
  Tests recover the planted and zero effects, match HC0/HC1/HAC against
  independent statsmodels fits, check date alignment and subsets, and verify
  the D8 coefficient identity to 1e-10 with missing signals and controls.
- [x] The exact requested `rebal.exhibits --all --demo --only ...` command
  exited 0. `ls output/demo/*.csv | wc -l` printed **15**. A separate read
  of every written file confirmed **15/15** have the exact ordered columns
  from `docs/contracts/exhibits.md`, with no missing output values.
- [x] Demo Table 1 column (1) reports Threshold **-0.357940** and
  Calendar × week4 **-0.278742**. Their distances from -0.4 and -0.3 are
  0.042060 and 0.021258, both below 0.05. The zero-effect base regression
  reports Threshold **0.0431099** and Calendar × week4 **0.0221196**;
  both absolute values are below 0.05.

The complete task Verify block exited **0** on implementation revision
`aa1ad8095a0d5bedd981016ee580e2c6a46e59cf`, after a conflict-free rebase onto
`origin/main`. Commands:

```sh
uv run pytest -q tests/test_regress.py
uv run python3 -m rebal.exhibits --all --demo --only table_1 table_2a table_2b table_3 table_D1 table_D2 table_D3 table_D5 table_D6 table_D7 table_D8 table_D10 table_D11 table_D12 table_D13
ls output/demo/*.csv | wc -l
uv run python3 -c "import pandas as pd; d=pd.read_csv('output/demo/table_1.csv'); print(d[(d.column==1)][['term','coef','se','t']])"
```

Verification output, with the long absolute artifact paths omitted:

```text
...............                                                          [100%]
15 passed in 4.13s
1 exhibit modules
[15 table CSVs, magnitudes/magnitudes.csv, predictive_tables.metadata.json]
      15
             term      coef        se          t
0           const  0.000112  0.000111   1.006415
1       threshold -0.357940  0.020303 -17.630023
2        calendar -0.012174  0.010887  -1.118277
3           week4 -0.000024  0.000239  -0.100846
4  calendar:week4 -0.278742  0.023175 -12.027602
5        momentum  0.000595  0.000337   1.768308
6             ret -0.004170  0.012128  -0.343830
```

Additional local checks after the rebase:

- `uv run pytest -q`: **35 passed in 6.76s**.
- Ruff check over both new modules, demo and affected tests: **All checks passed!**
- Ruff format check: **5 files already formatted**.
- `uv run python3 -m rebal.exhibits.predictive_tables --help`: exits 0.
- `uv run python3 -m rebal.exhibits.predictive_tables --demo --se hc0 --end latest --hac-lags 3`:
  exits 0. The subsequent exact Verify command restores default HC1 outputs.
- Magnitudes CSV: **74 rows**, including Calendar and Calendar × week4
  separately, using each regression's estimation sample.

## Summary

Added `rebal.regress` with named OLS results, tidy contract output, HC0/HC1
and Newey–West covariance, and next-trading-day alignment before filtering.
Added all 15 predictive-regression tables with the paper's column layouts,
including D1's coefficient-sum inference, D8's runtime coefficient identity
check, separate asset legs, alternative targets and threshold grids.

The module writes one-SD economic effects and a JSON metadata sidecar.
`docs/methods/regressions.md` records sample timing, covariance, units,
complete-case rules and the choices needed for paper ambiguities. Table D13
uses panels A/B for ES/TY, with five columns each. No real data or cluster
jobs were needed or run; this task verifies software on the agreed demo inputs.

Two small fixture/integration changes support this task. Demo residual SD
is 0.008 instead of 0.01: the old noise produced Threshold -0.347216 in the
required full predictive design, outside the 0.05 tolerance. Planted effects,
seed, regressors and dates are unchanged. The scaffold runner smoke test now
accepts discovered exhibit modules instead of assuming there are none.

Output-layout clarification: demo magnitudes are under
`output/demo/magnitudes/magnitudes.csv`. This preserves the required count of
15 top-level CSVs while keeping all demo output under `output/demo/`.
Real magnitudes retain the specified `output/tables/magnitudes.csv` path.
Demo artifacts remain git-ignored. No task specifications, other outcomes,
decisions or goal configuration were changed.

Verified implementation: `aa1ad8095a0d5bedd981016ee580e2c6a46e59cf`.
This outcome is a documentation-only follow-up commit in the same PR.
PR: https://github.com/jesusvillota/replicate/pull/13, targeting `main`.
Proposed follow-ups: only the existing TASK-018 real-data run. Real-data
coverage and upstream signal construction are outside this task's checks.
