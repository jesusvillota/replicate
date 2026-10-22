# TASK-021 outcome

## Acceptance

- [x] After the demo run, `rebal.compare` matches every `table_C1` and `table_C2` target and skips neither CSV. The required full demo and comparison commands exited 0. `output/demo/compare.md` lists both as matched exhibits, with numeric results for all 10 C.1 and all 4 C.2 targets. Its skipped-file list includes neither table. The comparison integration test also asserts these 14 joins and the absence of both skip entries.
- [x] A test checks the new C.1/C.2 columns and keys. `test_exhibits_write_demo_outputs` asserts exact exported columns, unique and complete keys (10 C.1 statistics and 64 C.2 matrix cells), finite values, and annualized means and SDs against the plotted daily signals. Both updated tests failed before the exporter change and passed afterward (`2 passed in 5.21s`).
- [x] `uv run pytest -q` passes. The full suite completed with `200 passed in 181.33s (0:03:01)` and exit code 0.

## Summary

- Exported both descriptive tables with `exhibit,column,term,value` comparison keys. C.1 keeps observation counts and sample dates. C.2 exports the full correlation matrix, including both orientations of every pair, using the existing predictor names.
- Preserved statistical calculations and Figure C.1. Checked PDF page 56: Table C.1 states that daily means and SDs are annualized. The module docstring now states the 252-trading-day convention: decimal mean times 252 and SD times sqrt(252), without a percentage conversion.
- Added schema and numerical assertions to the existing descriptive exporter test. Updated the existing comparison integration test, which previously required C.1/C.2 to be skipped, to require all their targets to join.
- Verified implementation revision: `6ea71f20dcbd75dfb18daa18644cb0103ac87c81`, rebased onto `origin/main` without conflicts. This outcome commit only adds the acceptance record.
- Deviations: none. Verification uses synthetic demo data; matching means the target keys join, not that synthetic estimates equal the paper's estimates. No follow-ups proposed.

## Verification

The following combined command exited 0:

```sh
uv run python3 -m rebal.exhibits --all --demo && uv run python3 -m rebal.compare --demo && grep -E 'table_C[12]' output/demo/compare.md && uv run pytest -q
```

Relevant output and final tail:

```text
- Matched exhibits: table_1, table_2a, table_2b, table_3, table_C1, table_C2, table_D1, table_D10, table_D11, table_D12, table_D3, table_D6, table_D7, table_D8
## table_C1
## table_C2
..................................................                 [100%]
200 passed in 181.33s (0:03:01)
```

`uvx ruff check src/rebal/exhibits/signals_descriptive.py tests/test_signals.py tests/test_compare.py` passed. Used `uvx` because Ruff is not installed in the project's environment. `git diff --check` passed.
