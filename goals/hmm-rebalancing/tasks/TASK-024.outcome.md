# TASK-024 outcome

## Acceptance

- [x] `uv run pytest -q tests/test_long_sample.py` passes.
  Final Verify: **10 passed in 5.04s**, exit 0. Tests recover the planted
  post-split effects and zero effects. They also check the contract, dates,
  252-return warm-up, cash legs, missing quotes and the 1971 seam.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only table_4` writes
  `output/demo/table_4.csv`. Final Verify exits 0 and reports one module.
  The CSV has exactly the 12 contract columns and column values `1`, `2`, `3`.
  The CSV/metadata writer test checks these values after reading the file.
- [x] `docs/methods/long_sample.md` states the yield-to-return method,
  pre-1971 choice, real first date and control set. It documents DGS10 as
  a par-yield proxy, the GSW seam, French `Mkt-RF + RF`, common cash legs,
  the 1962-01-03 return start and the 1963-01-11 first regression outcome.
  The design uses momentum and current return, with no extra level controls.
- [x] The real-data smoke result appears below for every column, beside
  the paper's Threshold estimate, with actual dates and N.

## Real-data smoke check

Ran locally with the stored public inputs:

```sh
uv run python3 -m rebal.exhibits.long_sample
```

Exit 0. Defaults: DGS10 before 1971-08-16, GSW 10-year zero afterward,
clean signal timing, medium/slow family momentum, HC1 covariance, endpoint
2023-03-17. The module reads the full public French/GSW/FRED history directly.
The processed main panel starts too late for this table and is not used.

| Column | Actual outcome dates | N | Threshold smoke | Paper Threshold | HC1 SE | p |
|---|---|---:|---:|---:|---:|---:|
| 1, full | 1963-01-11–2023-03-17 | 14,796 | −0.173107 | −0.1809 | 0.061339 | 0.004771 |
| 2, early | 1963-01-11–1997-09-09 | 8,478 | −0.018537 | −0.0157 | 0.059397 | 0.754972 |
| 3, late | 1997-09-11–2023-03-17 | 6,317 | −0.363704 | −0.3685 | 0.109614 | 0.000906 |

| Column | Calendar × week4 smoke | Paper Calendar × week4 |
|---|---:|---:|
| 1 | −0.151346 | −0.1536 |
| 2 | −0.106168 | −0.0284 |
| 3 | −0.200243 | −0.2569 |

The Threshold estimates agree closely in size and reproduce the absent early
effect and stronger late effect. The Calendar interaction differs more in the
subsamples. This is a proxy replication, with fewer observations than the
paper's 15,291 / 8,870 / 6,421. Early yields, the warm-up and the retained
common trading calendar differ from the paper. Exact agreement is not claimed.

The real first return is 1962-01-03. Momentum first completes on 1963-01-10.
The first full/early predictor is 1963-01-10, predicting 1963-01-11.
The first late predictor is 1997-09-10, predicting 1997-09-11. Both sides of
a predictive pair must be inside the selected window. The cross-split pair
belongs only to column 1; its N therefore exceeds columns 2 plus 3 by one.

Input SHA-256 values from the smoke metadata:

- `french/F-F_Research_Data_Factors_daily.csv`:
  `2f288d35b1786a429cda4f1f9c197c053441fc59ef5ace6d5b138026d27799d6`
- `gsw/feds200628.csv`:
  `9f2a8d6ba54d13cdb9b4f19811f9c61f72c870b8fab1562d5b8bd6dd70b337b7`
- `fred/DGS10.csv`:
  `cbf5871fb1b3e12a83f6e89dd291564b9512301f0cf0fc1a0965772a8f352b3b`

Real smoke outputs are removed after inspection. This PR commits no outputs.

## Verify

The required block completed with exit 0 at code revision
`6db78ec8d9c6bd955dc04e92bf6019a70905c48f`:

```sh
uv run pytest -q tests/test_long_sample.py
uv run python3 -m rebal.exhibits --all --demo --only table_4
head -5 output/demo/table_4.csv
```

Output tail (the runner also reports both output paths):

```text
10 passed in 5.04s
1 exhibit modules
exhibit,column,term,coef,se,t,p,nobs,adj_r2,se_type,sample_start,sample_end
table_4,1,const,9.843903065147309e-06,1.0885206026543575e-05,0.9043377811263242,0.36581631898023015,16110,0.571033292731316,hc1,1961-06-19,2023-03-17
table_4,1,threshold,-0.13105230791634565,0.004218192698822215,-31.068354926729043,6.447460430594793e-212,16110,0.571033292731316,hc1,1961-06-19,2023-03-17
table_4,1,calendar,0.004512603154567401,0.0019175963286697801,2.3532602180656834,0.018609605867172613,16110,0.571033292731316,hc1,1961-06-19,2023-03-17
table_4,1,week4,4.7528211317849e-06,3.461009066074736e-05,0.13732472354298852,0.8907741289983372,16110,0.571033292731316,hc1,1961-06-19,2023-03-17
```

`uv run --with ruff ruff check src/rebal/exhibits/long_sample.py tests/test_long_sample.py`
passes. Ruff is supplied with `--with` because it is not a project dependency.

Broader integration verification also passes:

```sh
uv run pytest -q tests/test_long_sample.py tests/test_regress.py tests/test_signals.py tests/test_proxies.py tests/test_scaffold.py
```

Result: **102 passed in 180.60s**, exit 0. This includes the full demo exhibit
runner. `git diff --check` also passes.

## Summary

Added one exhibit module, one test module and one methods document. The
runner discovers the module without registry changes. Source reads reuse
`rebal.panel.read_source`; conversion, signals and regressions use the existing
shared APIs. No shared module, contract, task spec or decision changed.

The early-source approximation follows the task's default. The seam omits the
first GSW day rather than creating a cross-source price jump. The actual
regression starts in 1963 because no earlier bond returns can warm up momentum.
These method choices and alternatives are documented and exposed as flags.
No material decision or missing data blocks delivery.

Verified code revision: `6db78ec8d9c6bd955dc04e92bf6019a70905c48f`, rebased
successfully onto `origin/main`. Later commits contain documentation and this
outcome only. The real smoke ran before that rebase with identical module code.
Proposed follow-up: TASK-030 runs and commits the real outputs and comparison,
including the differing Calendar interaction. No new task is needed.
