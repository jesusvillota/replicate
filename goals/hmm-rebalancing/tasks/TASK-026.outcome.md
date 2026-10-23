# TASK-026 outcome

## Summary

Implemented `rebal.exhibits.robustness_extra` for Tables D.4, D.9 and D.14.
The shared runner discovers it without registration changes.
Only this module, its tests, this outcome and its methods document change.
No shared Python modules, contracts, task specifications or real outputs change.

D.4 rebuilds signals from the index pair by default. The CLI exposes the
futures-signal reading. D.9 uses published control levels without rescaling.
It exports columns 1, 2 and 4 and records skipped FEARS column 3 in metadata.
D.14 uses the extra signal lag and compounded two-day S&P 500 control.
The methods document explains the interaction timing and missing-history rules.

The resumed code had lost the required `date` column at the regression boundary.
The module now resets its date index before calling the shared regression API.
Independent test responses distinguish D.4 from D.9's extra-control design.

Verified implementation revision: `f4c98a86e06783574737426a1bf2810fa7177ba3`.
The outcome and measured-sample documentation follow in a documentation-only commit.
The branch was rebased onto `origin/main` without conflicts.
No material decision is missing. TASK-030 owns the final real-output run.
No additional follow-up is proposed.

Additional verification at `b7b44f7183a1e36bfd902c6a01da14b9ebc8b381`:

- `uv run pytest -q tests/test_scaffold.py tests/test_regress.py`: **35 passed**,
  including the complete demo exhibit runner.
- The exact required demo command and `ls` command pass again.
- `uvx ruff check src/rebal/exhibits/robustness_extra.py tests/test_robustness_extra.py`:
  all checks passed. Ruff was not installed in the project environment, so `uvx`
  supplied it without changing dependencies.
- `uvx ruff format --check src/rebal/exhibits/robustness_extra.py tests/test_robustness_extra.py`:
  both files already formatted.
- `git diff --check origin/main...HEAD`: passes.

## Acceptance

- [x] `uv run pytest -q tests/test_robustness_extra.py` passes.
  Session result: **10 passed** after the rebase. Tests cover planted and zero
  effects for all tables, independent D.4 least squares, D.14 lag separation,
  its two-day control, missing returns, column samples and skipped FEARS metadata.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only table_D4 table_D9 table_D14`
  succeeds and writes `output/demo/table_D4.csv`, `table_D9.csv`, `table_D14.csv`
  and `robustness_extra.metadata.json`. The required `ls` command finds all three
  CSVs. Reading `table_D9.csv` gives exactly column values **[1, 2, 4]**.
- [x] `docs/methods/robustness_extra.md` states the D.4 default and alternative
  signal readings, control scaling, D.14 extra lag and control, and skipped FEARS
  column. It also records the real sample sizes and date ranges.
- [x] The real-data smoke command
  `uv run python3 -m rebal.exhibits.robustness_extra` succeeds against the local
  processed panel. Its measured coefficients and paper references appear below.
  After inspection, `git restore output/` restored tracked outputs, and all four
  new smoke artifacts under `output/tables/` were deleted. No real output is committed.

## Real-data smoke comparison

Default choices: clean timing, HC1 standard errors, rebuilt index signals for
D.4, one extra signal lag for D.14, study endpoint 2023-03-17.
All estimates below are observed-data results, without planted responses.

| Table / column | Term | Our smoke result | Paper | Our N | Paper N |
| --- | --- | ---: | ---: | ---: | ---: |
| D.4 / 1 | Threshold | -0.449384 | -0.3970 | 6,317 | 6,226 |
| D.4 / 1 | Calendar × week4 | -0.261891 | -0.3189 | 6,317 | 6,226 |
| D.9 / 1, ra^BEX | Threshold | -0.491847 | -0.4493 | 6,317 | 6,124 |
| D.9 / 2, unc^BEX | Threshold | -0.480745 | -0.4375 | 6,317 | 6,124 |
| D.9 / 4, ARA | Threshold | -0.385589 | -0.3731 | 3,843 | 3,903 |
| D.14 / 1 | Threshold | -0.668625 | -0.2723 | 5,503 | 6,097 |
| D.14 / 1 | Calendar × week4 | -0.155010 | -0.2060 | 5,503 | 6,097 |

The smoke results do not reproduce every paper coefficient, especially D.14's
Threshold estimate. This task verifies the implementation and reports the gap;
TASK-030 owns the full comparison. Our panel uses the selected core return
proxies and VBMFX instead of the paper's Bloomberg instruments.

Actual response dates:

| Table / columns | First response | Last response | N |
| --- | --- | --- | ---: |
| D.4 / 1 | 1997-09-11 | 2023-03-17 | 6,317 |
| D.9 / 1 and 2 | 1997-09-11 | 2023-03-17 | 6,317 |
| D.9 / 4 | 2004-07-02 | 2020-01-02 | 3,843 |
| D.14 / 1 | 2001-01-02 | 2023-03-17 | 5,503 |

ARA predictor dates are limited to 2004-07-01 through 2019-12-31, as in the
paper. The final predictor's next trading day is 2020-01-02. No post-2019
forward-filled attention values enter the design. Each D.9 column uses its
own complete observations; there is no common-sample restriction.

D.14 has fewer observations than the paper because our exact MSCI history
starts with a level on 2000-12-29. Its first return is 2001-01-02. The shared
panel also retains only dates with both core return proxies. In the resulting
panel there are 5,504 dates from 2000-12-29 through 2023-03-17, with one missing
international return on the first date. The regression uses the remaining
5,503 responses. There is no fill or earlier international proxy splice.

Input SHA-256 hashes, measured in this session:

- `daily_panel.parquet`: `0aa723f34422fae7bcedb41bfaf0e7a5c3685688a1a9c7e3addec7af0463a4cd`
- `signals_clean.parquet`: `ac21349f54e9b1efcee38b25317dfcf7350f23490646b661a4e2caf52dddbed1`
