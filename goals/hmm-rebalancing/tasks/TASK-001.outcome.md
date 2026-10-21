# TASK-001 outcome

## Acceptance

- [x] `uv sync` and `uv run pytest` succeed. The full test run collected 20 tests and printed `20 passed in 3.04s`. The exact Verify block then printed `20 passed in 2.19s`; dependency sync resolved 64 packages and audited 57 installed packages.
- [x] `uv run python3 -m rebal.demo --check` exits 0. Planted coefficients: threshold **-0.359851**, calendar × week4 **-0.301344**. Zero-effect coefficients: **0.040149**, **-0.001344**. Each differs from its target by at most 0.05. Both lines printed `PASS`.
- [x] `uv run python3 -m rebal.exhibits --all --demo` printed `0 exhibit modules`; the following shell command printed `exit=0`.
- [x] `grep -cE '^\| D[0-9]+ ' docs/data/sources.md` printed **28**.
- [x] `ls docs/contracts/` listed **daily_panel.md**, **exhibits.md**, **signals.md**.
- [x] `git check-ignore .env output/demo/x data/foo` printed all three paths. `git check-ignore data/public/x` printed nothing and exited 1, as expected for an unignored path. The fallback printed `data/public not ignored`.

The complete task Verify block exited **0**. Its output was:

```text
Resolved 64 packages in 8ms
Audited 57 packages in 2ms
....................                                                     [100%]
20 passed in 2.19s
planted: beta_threshold=-0.359851 beta_calweek4=-0.301344 expected=(-0.4, -0.3) PASS
zero: beta_threshold=0.040149 beta_calweek4=-0.001344 expected=(0.0, 0.0) PASS
0 exhibit modules
exit=0
28
daily_panel.md
exhibits.md
signals.md
.env
output/demo/x
data/foo
data/public not ignored
```

Additional local validation: `uv run --with ruff ruff check src tests` printed `All checks passed!`; `uv run --with ruff ruff format --check src tests` reported 9 files already formatted. Ruff was used as a temporary tool, without adding a project dependency.

## Summary

Added the installable `rebal` src package, required runtime dependencies, pytest and the git-pinned `cluster-kit` source in `uv.lock`. Added storage helpers, atomic downloads with retries and HTTP error propagation, file validation, real/demo loaders, and an exhibit runner that discovers modules with `pkgutil`.

Wrote all three data contracts, the 28-row planned source map, a source-card template and the repo run order. Public files can enter git; licensed and processed data use the external root. Demo outputs are ignored.

The deterministic fixtures contain all 35 panel columns and 63 signal columns. Tests compare column names, order and dtypes directly with the contracts. Independent statsmodels OLS tests verify next-day timing for the planted and zero-effect runs. Other tests cover scales, calendar flags, deterministic behavior, loaders, path creation, HTTP errors and retries, validation failures, and exhibit discovery and filtering.

Deviations: none. Demo dates are weekdays, not an exchange calendar. Auxiliary demo signals are placeholders, as documented. The fixture replaces `ret` with the planted equation without changing the input panel. No fetcher, real signal engine or regression toolkit was added. No market data was downloaded and no cluster job ran.

Verified implementation revision: `25651bb9e801040506b58bfe5d4837e9fd8a3762`, after a clean rebase onto `origin/main`. This outcome is a documentation-only follow-up commit. PR: https://github.com/jesusvillota/replicate/pull/10, into `main`, with `Goal-Task: hmm-rebalancing/TASK-001` and label `goal:hmm-rebalancing`.

Proposed follow-ups: none beyond the existing goal tasks. TASK-012 owns the real panel and future source-map updates; TASK-013 owns the real signal and simulation APIs. DEC-001 still selects the futures proxies. Live source access is outside this scaffold task and was not tested.
