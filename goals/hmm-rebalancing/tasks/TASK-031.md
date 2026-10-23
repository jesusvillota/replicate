---
id: TASK-031
title: 'Latest sample (footnote 32): code on demo data'
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-6 and DEC-004 (accepted: latest sample only). Footnote 32 (p.38) says the main regression still holds when the sample runs to 2025. This task builds the code that reruns the main regressions to the latest date and compares them with the 1997-2023 sample. TASK-032 runs it on the real panel.

## Scope

Module: `src/rebal/latest.py`, run as `uv run python3 -m rebal.latest [--demo] [--timing clean|literal]`. Test: `tests/test_latest.py`. Methods doc: `docs/methods/latest_sample.md`.

The module imports `build_tables`, `DEFAULT_SAMPLE`, `load_panel` and `load_signals` from `rebal.exhibits.predictive_tables`. It calls `build_tables(..., end="latest")` and writes `table_1.csv` and `table_3.csv` to `output/tables/robustness/latest/` (demo: `output/demo/robustness/latest/`). It must never write to `output/tables/` itself, because the main exhibits live there.

It also writes `latest_comparison.csv` in the same folder. Columns: `exhibit,column,term,stat,sample,value`, where `sample` is `paper_end` (default end 2023-03-17) or `latest`. It includes the coefficient, standard error, t-value and N for the Threshold and Cal x week4 terms of Table 1, and it records the first and last date of each sample. The `latest` end is the last date of the panel; the code reads it from the data and never hard-codes a date.

Add a part "Latest sample (footnote 32)" to `rebal.report`. It is additive and small: the part is read from `output/tables/robustness/latest/latest_comparison.csv` when the file exists, and says "not run" when it does not. Do not change any other behaviour of `rebal.report`. Write the choice in `docs/methods/latest_sample.md`.

No cluster jobs. Build and test on the demo fixtures. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts.

**Real-data smoke check (optional).** You may run the module on the real panel at `~/data/replicate/processed/`. Quote the numbers in the outcome. Then run `git restore output/` and delete new untracked files under `output/`. This task commits no outputs.

Out of scope: the real run and its write-up (TASK-032); other exhibits with `--end latest` (costs, Table 4, figures); the 3:30 PM check (rejected in DEC-004).

## Acceptance

- `uv run pytest -q tests/test_latest.py tests/test_report.py` passes.
- `uv run python3 -m rebal.latest --demo` exits 0 and writes `table_1.csv`, `table_3.csv` and `latest_comparison.csv` under `output/demo/robustness/latest/`.
- The test proves that a run does not change any file in `output/tables/` outside `robustness/latest/`.
- `uv run python3 -m rebal.report --demo --out /tmp/report_demo.md` exits 0 and the file has the "Latest sample" part.
- `uv run pytest -q` passes.

## Verify

```sh
uv run pytest -q tests/test_latest.py tests/test_report.py
uv run python3 -m rebal.latest --demo; ls output/demo/robustness/latest/
uv run python3 -m rebal.report --demo --out /tmp/report_demo.md && grep -n "Latest sample" /tmp/report_demo.md
uv run pytest -q
git status --short output/
```
