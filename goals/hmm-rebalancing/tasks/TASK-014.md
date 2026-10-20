---
id: TASK-014
title: Regression toolkit and predictive-regression tables
milestone: M-2
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-3. This task implements the main predictive regression (eq. 4) and every table built from it. See paper-notes §3.4, §3.6 and §4.

## Scope

No cluster jobs in this task. Build and test on the demo fixtures from `rebal.demo` and `rebal.io` (`demo=True`). The real panel may not exist yet; TASK-018 runs the real data. Follow `docs/contracts/` exactly. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below. Where the choice is cheap, also expose it as a CLI flag.

The methods doc for this task is `docs/methods/regressions.md`.

**1. `src/rebal/regress.py`.** This is a thin wrapper on `statsmodels`.

`ols(y, X, se="hc1", hac_lags=None)` returns:
- `coef`, `se`, `t`, `p`, `nobs`, `adj_r2`;
- a tidy frame in the long format of `docs/contracts/exhibits.md`.

It supports `se` = `hc0`, `hc1` and `hac`. For `hac`, use Newey–West, with lags = floor(4(T/100)^(2/9)) unless `hac_lags` is given.

`predictive(signals, panel, terms, y="ret", lead=1, sample=("1997-09-10","2023-03-17"), subset=None)` aligns the dependent variable at t+1 with regressors at t, drops rows with missing values, and applies an optional boolean subset.

**Defaults.**
- HC1. Report HC0 in the methods doc as a check.
- The default sample runs from 1997-09-10 to 2023-03-17. `--end latest` extends it.

**2. Exhibits: `src/rebal/exhibits/predictive_tables.py`.** Each table follows paper-notes §4 and §3.6. The column order and the regressors are those of the paper.

| Exhibit | Content |
|---|---|
| `table_1` | 5 columns: base; + VIX/MOVE; + EPU/ADS; + Sentiment; all controls |
| `table_2a` | (1) no interaction; (2) = Table 1 col. 1; (3) + Threshold × week4 |
| `table_2b` | separate samples for the 1st, 2nd and 3rd month of the quarter |
| `table_3` | the S&P leg (`r_es`) and the TY leg (`r_ty`) as dependent variables, without and with controls |
| `table_D13` | the full version of `table_3` |
| `table_D1` | each signal regressed on trailing `ret` sums over 1, 2, 3, 4, 5, 10, 15, 21, 42, 63, 126 and 252 days, with HAC; also report the coefficient sum |
| `table_D2` | Table 1 with HAC |
| `table_D3` | fast, medium and slow momentum as separate regressors |
| `table_D5` | controls in first differences |
| `table_D6` | Threshold averaged over δ ∈ [0, 2%] and over [0.1%, 2.5%], built from the `thr_*` columns |
| `table_D7` | the target variants 86/14, 50/50 and 70/30 |
| `table_D8` | Threshold Small/Large, split at the median of abs(Threshold); and Threshold⊥, the residual of Threshold on Momentum |
| `table_D10` | short-term reversal alone; with the signals; long-term reversal |
| `table_D11` | `eom_rev` |
| `table_D12` | week1–week3 dummies and their interactions with Calendar |

**Runtime check in `table_D8`.** By the Frisch–Waugh–Lovell theorem, the Threshold⊥ coefficient must equal the baseline Threshold coefficient. Assert this to within 1e-10, and fail loudly if it does not hold.

Also write the "1 SD" economic magnitudes for Table 1 and Table 3 (coefficient × the SD of each regressor) to `output/tables/magnitudes.csv` (`output/demo/` in demo mode). The paper states its SD convention only implicitly (§5.8). Report both the SD of `calendar` and the SD of `calendar × week4`.

**3. Tests.** `tests/test_regress.py`:
- On the demo signals with planted β (−0.4, −0.3), `table_1` col. (1) recovers both within 0.05, and the zero-effect fixture gives |β| < 0.05.
- The HC1 standard errors match `statsmodels` directly.
- The FWL assertion holds.

Out of scope: per-δ and horizon figures (TASK-015); costs (TASK-016); the strategy (TASK-017); Tables 4, 5, D.4, D.9 and D.14 (M-3).

## Acceptance

- `uv run pytest tests/test_regress.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only table_1 table_2a table_2b table_3 table_D1 table_D2 table_D3 table_D5 table_D6 table_D7 table_D8 table_D10 table_D11 table_D12 table_D13` writes 15 CSV files to `output/demo/`. Each file has the columns from the contract.
- The demo `table_1` col. (1) shows Threshold ≈ −0.4 and Cal × week4 ≈ −0.3; the outcome quotes these numbers.

## Verify

```sh
uv run pytest -q tests/test_regress.py
uv run python3 -m rebal.exhibits --all --demo --only table_1 table_2a table_2b table_3 table_D1 table_D2 table_D3 table_D5 table_D6 table_D7 table_D8 table_D10 table_D11 table_D12 table_D13
ls output/demo/*.csv | wc -l
uv run python3 -c "import pandas as pd; d=pd.read_csv('output/demo/table_1.csv'); print(d[(d.column==1)][['term','coef','se','t']])"
```
