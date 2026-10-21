# TASK-013 outcome

## Acceptance

- [x] `uv run pytest tests/test_signals.py` passes. The post-rebase full run collected this file and passed all 38 signal tests; all 58 repository tests passed in 9.78s. The exact Verify command, `uv run pytest -q tests/test_signals.py`, then printed **38 passed in 5.95s** and exited 0.
- [x] `uv run python3 -m rebal.signals --demo` exits 0. It wrote **7304 rows and 63 columns**, printed **eight PASS self-checks**, and printed nonzero trade counts and annual rates for **all 41 δ values**, 0.000 through 0.040. Key rates: δ=0 gives 252.000; δ=0.011 gives 14.663; δ=0.025 gives 3.416 trades per 252 days.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only table_C1 table_C2 figure_C1` exits 0. It wrote `output/demo/table_C1.csv`, `table_C2.csv`, `figure_C1.pdf`, the figure's plotted `figure_C1.csv`, and JSON lineage. The following `ls output/demo/` listed every required exhibit. The PDF was rendered with macOS `sips` and visually checked: both panels, dates and percentage labels are readable, without clipping.
- [x] Output columns match `docs/contracts/signals.md`. `test_exact_contract_columns_and_dtypes` parses the contract table and compares the **complete ordered column list and all 63 dtypes**. It passed in both test runs above. The CLI integration test also compares the saved Parquet frame against the in-memory build.

The exact task Verify block exited **0** at implementation revision `8c589060ed896adf987064d624b3645399a83007`:

```sh
uv run pytest -q tests/test_signals.py
uv run python3 -m rebal.signals --demo
uv run python3 -m rebal.exhibits --all --demo --only table_C1 table_C2 figure_C1 && ls output/demo/
```

Output excerpts (start and final tail):

```text
......................................                                   [100%]
38 passed in 5.95s
Wrote 7304 rows, 63 columns: /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-013/output/demo/signals_clean.parquet
PASS: delta=0 daily drift
PASS: delta=1 buy-and-hold
PASS: Calendar month-end trades
PASS: 0.24 approximation
PASS: literal Threshold previous-weight reset
PASS: literal Calendar next-close reset
PASS: controlled trade counts decrease
PASS: momentum bounds
delta  rebalances  per_year (252 trading days; clean)
...
0.037     49  1.691
0.038     42  1.449
0.039     40  1.380
0.040     44  1.518
1 exhibit modules
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
13/output/demo/table_C1.csv
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
13/output/demo/table_C2.csv
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
13/output/demo/figure_C1.csv
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
13/output/demo/figure_C1.pdf
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
13/output/demo/signals_descriptive.json
figure_C1.csv
figure_C1.pdf
signals_clean.json
signals_clean.parquet
signals_descriptive.json
signals_literal.json
signals_literal.parquet
table_C1.csv
table_C2.csv
```

Additional local checks:

- `uv run pytest`: **58 passed in 9.78s** after a clean rebase onto `origin/main`.
- `uv run --with ruff ruff check` on all four changed Python files: **All checks passed!**
- `uv run --with ruff ruff format --check` on those files: **4 files already formatted**.
- Both new module `--help` commands exited 0.
- `uv run python3 -m rebal.signals --demo --timing literal --momentum all15` exited 0 with eight PASS self-checks. Its reported counts use literal timing.
- `git check-ignore` confirmed demo Parquet and PDF outputs remain ignored.

## Summary

Implemented Threshold, Calendar and selected-date portfolio simulations, including the Appendix B delayed reset option. Added the full signal frame: all threshold paths, aggregate and target variants, momentum families, trading-calendar buckets, short/long reversal and the separate S&P end-of-month control. Inputs are validated; warm-up rows remain with missing history values.

Added automatically discovered Table C.1, Table C.2 and Figure C.1. Demo exhibits use actual simulations on synthetic panel returns. The existing planted-effect fixtures and loaders retain their contract. Descriptive tests independently check moments, planted positive/negative correlations and a near-zero noise correlation. A scaffold smoke test now expects the newly added exhibit module.

`docs/methods/signals.md` records timing, momentum weighting, zero signs, all first-valid dates, fourth-Friday and holiday handling, annualization, sample selection and all 41 demo trade counts alongside the paper's three benchmarks. Both processing and exhibits write lineage metadata. Demo builds write only to ignored `output/demo/`, protecting any real processed signals.

Clarifications: monotonic trade counts are tested on a controlled constant-return synthetic path. They are not a property of arbitrary paths because reset dates differ. For example, the unmodified demo has 228 trades at 1.5% and 232 at 1.6%. No counts were smoothed. The daily end-of-month reversal accumulates only known returns after the fourth-Friday anchor, reaching the specified full return at month-end; it never fills earlier dates with future month-end returns. Both choices are documented, with no unresolved material decision.

Verified implementation revision: `8c589060ed896adf987064d624b3645399a83007`. This outcome is a documentation-only follow-up commit. The branch was rebased onto `origin/main` without conflicts. PR: https://github.com/jesusvillota/replicate/pull/14 into `main`, with `Goal-Task: hmm-rebalancing/TASK-013` and label `goal:hmm-rebalancing`.

No real panel was required or checked. No market data was fetched and no cluster job ran. TASK-018 owns real-data replication. No follow-up outside the existing task plan is proposed. GitHub Actions were not read or used.
