---
id: TASK-021
title: Export Tables C.1 and C.2 in the comparison key schema
milestone: M-2
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-5 (compare each result with the paper). The TASK-020 review found that `rebal.compare` skips `table_C1` and `table_C2` with "missing columns column, exhibit, term". So the 14 Table C.1/C.2 targets in `docs/results/targets.csv` can never match. TASK-018 writes no new code, so this gap must close first.

## Scope

- Change only `src/rebal/exhibits/signals_descriptive.py` (TASK-013) and its test.
- Make `table_C1.csv` and `table_C2.csv` follow the key schema in `docs/methods/comparison.md` ("Schema and units"): `exhibit,column,term` plus a `value` column (wide), or `exhibit,column,term,stat,value` (long).
- Use the exact keys and units in `docs/results/targets.csv`:
  - C.1: `column` is `threshold` or `calendar`; `term` is `mean_annualized`, `sd_annualized`, `ar1`, `skewness` or `excess_kurtosis`. Check the annualization the paper uses (PDF page 56) and state it in the module docstring.
  - C.2: `column` and `term` are the two predictors of each correlation pair, with the names the targets use (`threshold`, `calendar`, `momentum`, `vix`, ...). Emit each unordered pair at least in the orientation the targets use.
- Keep `figure_C1` unchanged.
- Out of scope: `rebal.compare`, `targets.csv`, other exhibits.

## Acceptance

- After the demo run, `rebal.compare` matches every `table_C1` and `table_C2` target. It does not list them as skipped.
- A test checks the new C.1/C.2 columns and keys.
- `uv run pytest -q` passes.

## Verify

```sh
uv run python3 -m rebal.exhibits --all --demo && uv run python3 -m rebal.compare --demo 2>&1 | grep -E 'table_C[12]'
uv run pytest -q
```
