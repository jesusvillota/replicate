# TASK-017 outcome

## Acceptance

- [x] `uv run pytest tests/test_strategy.py` passes: **13 passed in 1.74s**.
  The final exact Verify invocation, `uv run pytest -q tests/test_strategy.py`,
  also passed: **13 passed in 2.21s**.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only table_6a table_6b table_6c figure_6`
  exits 0 and writes all four exhibits under `output/demo/`.
  The subsequent `ls output/demo/table_6* output/demo/figure_6*` lists
  `table_6a.csv`, `table_6b.csv`, `table_6c.csv`, `figure_6.csv`, and `figure_6.pdf`.
  The module also writes `strategy.metadata.json` there.

The complete Verify block below exited **0** on implementation revision
`cf584b4019a82fdea5ec6c83c56ae2ddd76429df`, after a conflict-free rebase onto
`origin/main`:

```sh
uv run pytest -q tests/test_strategy.py
uv run python3 -m rebal.exhibits --all --demo --only table_6a table_6b table_6c figure_6
ls output/demo/table_6* output/demo/figure_6*
```

Output starts with:

```text
13 passed in 2.21s
1 exhibit modules
```

The final eight lines, with their absolute paths preserved, are:

```text
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-017/output/demo/figure_6.csv
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-017/output/demo/figure_6.pdf
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-017/output/demo/strategy.metadata.json
output/demo/figure_6.csv
output/demo/figure_6.pdf
output/demo/table_6a.csv
output/demo/table_6b.csv
output/demo/table_6c.csv
```

Additional local evidence:

- `uv run pytest -q`: **179 passed in 30.09s**, after the rebase.
- `uv run --with ruff ruff check src/rebal/exhibits/strategy.py tests/test_strategy.py`:
  **All checks passed!** Ruff format check: **2 files already formatted**.
- `uv run python3 -m rebal.exhibits.strategy --help`: exits 0.
- `uv run python3 -m rebal.exhibits.strategy --demo --cal-reversal lag4 --end latest --se hc0 --equity-cost-bps 1 --bond-cost-bps 1`:
  exits 0. The exact Verify run restores default outputs afterward.
- All output CSV values are complete and finite. Table 6A has **7 rows**,
  Table 6B **4 rows**, Table 6C **10 rows**, and Figure 6 **6,657 rows**.
  Tables 6B and 6C have the exact ordered columns in the exhibit contract.
- Rendered Figure 6 to PNG with Poppler and visually inspected it:
  labels and legend are readable, with no clipping or overlap.
- Planted demo Sharpe ratio: **3.248504**. Zero-effect Sharpe ratio:
  **-0.254233**, satisfying `abs(SR) < 0.3` without changing shared fixtures.
- Tests independently check Calendar weight support, both reversal readings,
  no future-signal dependence, next-panel-day alignment, missing signal dates,
  factor alpha and HC0/HC1 covariance against hand matrix calculations,
  two-leg costs, crisis dates, component volatility, regime ties/missingness,
  log compounding, input validation, and output schemas.

## Summary

Added `src/rebal/exhibits/strategy.py`, discovered through the existing runner.
It builds the equal-weighted Threshold/Calendar strategy, Table 6 A–C,
Figure 6 and its plotted data, plus a JSON lineage sidecar.
Factor regressions reuse `rebal.regress.ols`. Controls at signal date `t`
define regimes, while factors at realized return date `t+1` explain returns.
The module builds weights and turnover before applying the sample limits.

`docs/methods/strategy.md` documents all paper ambiguities, units and timing.
The default first-day reversal uses the first week4 day of the previous month;
`--cal-reversal lag4` exposes the alternate reading. The paper's 11.6% component
volatilities refer here to standalone component returns before averaging.
No scaling is fitted to that empirical target.

The Harvey et al. (2018) reference was available from the author's website.
Its PDF page 5 states costs of **1 bp for equities and 0.5 bp for bonds**
per notional traded. These are the defaults, with separate CLI overrides.
The authorized fallback was not needed. Costs apply to both position
increases and decreases, with sample-start turnover based on prior history.

The demo contract plants effects in `signals.ret`, independently of panel
asset returns. Demo mode therefore copies the panel and sets
`r_es = r_ty + signals.ret` locally. This preserves the specified two-leg
formula and leaves the shared fixtures unchanged. Real mode uses panel
returns directly. Demo performance is a software check, not an empirical
replication of the paper's headline results.

Verified implementation: `cf584b4019a82fdea5ec6c83c56ae2ddd76429df`.
This outcome is a documentation-only follow-up commit in the same PR.
PR: https://github.com/jesusvillota/replicate/pull/23, targeting `main`.
Demo outputs remain git-ignored. No task specs, other task outcomes,
decisions, or goal configuration were changed. No cluster jobs or real-data
runs were needed. Follow-up: the existing TASK-018 real-data validation.
