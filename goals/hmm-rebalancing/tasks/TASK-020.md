---
id: TASK-020
title: Paper target numbers and comparison report generator
milestone: M-2
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-4 and SC-5. Every result must sit next to the paper's own number. This task encodes the paper's numbers once, as machine-readable targets, and builds the generator that writes the comparison report.

## Scope

No cluster jobs in this task.

**1. Targets file.** Write `docs/results/targets.csv` with the columns `exhibit, column, term, stat, paper_value, approx, source_page`, where:
- `stat` ∈ {coef, se, t, adj_r2, nobs, value};
- `approx` = 1 for a value read off a chart.

Encode every number in paper-notes §4. Check each one against the PDF tables, and fix the notes where they are wrong: report such fixes in the outcome; never edit paper-notes yourself.

**2. Comparison generator.** Write `src/rebal/compare.py`.
- Command: `uv run python3 -m rebal.compare [--demo] --out FILE`.
- It joins `docs/results/targets.csv` with the produced exhibit CSVs (`output/tables` and `output/figures`; `output/demo` with `--demo`). The join key is `exhibit, column, term`.
- It writes a Markdown report:
  - one section per exhibit, with the rows `term | paper | ours | ours/paper | sign match | significance match (|t| ≥ 1.96 in both or neither)`;
  - a summary section at the top: the number of targets matched; the sign-match rate; the significance-match rate; and the list of missing exhibits.
- An exhibit that has not been produced yet is listed as missing, not as an error.

**3. Test.** `tests/test_compare.py` uses a tiny fake exhibit CSV and a fake targets file to check the join, the sign match, the significance match and the reporting of missing exhibits.

Out of scope: running exhibits; writing commentary.

## Acceptance

- `uv run pytest tests/test_compare.py` passes.
- `wc -l docs/results/targets.csv` shows at least 150 rows.
- `uv run python3 -m rebal.compare --demo --out output/demo/compare.md` runs, and its summary lists the exhibits that are missing in demo mode.

## Verify

```sh
uv run pytest -q tests/test_compare.py
wc -l docs/results/targets.csv
uv run python3 -m rebal.compare --demo --out output/demo/compare.md && head -30 output/demo/compare.md
```
