# TASK-031 outcome

## Summary

Implemented `rebal.latest` for the accepted latest-sample extension in DEC-004.
It imports the required predictive-table APIs and builds the paper-end and
latest samples in memory. It writes latest Tables 1 and 3, a 120-row Table 1
comparison, and metadata only under `robustness/latest/`. The report adds a
Latest sample section and says `not run` when the comparison is absent.
`docs/methods/latest_sample.md` records the choices and output schema.

Verified implementation revision: `1e4507334b2d65cbebb8173072c52f30f58298c3`.
The outcome-only commit follows this revision. The branch was rebased onto
`origin/main` without conflicts. No task specifications, decisions, contracts,
restricted modules, main outputs, or other task files were changed.
No deviations, cluster jobs, or real-data runs. TASK-032 remains responsible
for the real-data run and interpretation; no additional follow-ups are proposed.

## Acceptance

- [x] `uv run pytest -q tests/test_latest.py tests/test_report.py` passes.
  Evidence: final focused run reported `20 passed in 12.36s`.
- [x] `uv run python3 -m rebal.latest --demo` exits 0 and writes the required files.
  Evidence: the command succeeded, and `ls output/demo/robustness/latest/`
  listed `table_1.csv`, `table_3.csv`, `latest_comparison.csv`, and
  `latest.metadata.json`. The comparison has 120 rows; the paper-end outcome
  date is 2023-03-17 and the latest demo outcome date is 2023-12-29.
- [x] Tests prove that files in `output/tables/` outside `robustness/latest/`
  do not change.
  Evidence: `test_cli_protects_all_other_outputs` passes for demo/clean and
  non-demo/literal runs using synthetic inputs. It compares all protected file
  paths, contents and modification times, detects additions and deletions,
  and excludes only the selected output destination. Fixtures include main
  tables, metadata, another robustness folder, and `archive/latest/`.
  A synthetic panel ending 2026-02-13 also proves the endpoint is data-driven.
- [x] `uv run python3 -m rebal.report --demo --out /tmp/report_demo.md`
  exits 0 and includes the Latest sample part.
  Evidence: the final command succeeded; grep printed
  `189:## Latest sample (footnote 32)`. Report tests also cover missing inputs,
  demo/real isolation and the actual latest exporter.
- [x] `uv run pytest -q` passes.
  Evidence: full local run reported `393 passed, 4 warnings in 252.68s (0:04:12)`.
  The warnings come from escape sequences in the installed `wrds` package.

Additional checks: Ruff check and format check passed for all four changed
Python files; `rebal.latest --help` exited 0. `git diff --check` passed.
`git status --short output/` printed nothing. No generated outputs are committed.
The required Verify command sequence exited 0. GitHub Actions were not inspected.
