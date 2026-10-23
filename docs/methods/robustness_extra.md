# Extra robustness tables

Inputs and outputs follow the [panel contract](../contracts/daily_panel.md),
[signal contract](../contracts/signals.md), and
[exhibit contract](../contracts/exhibits.md). The paper specifications are in
[paper-notes §§3.6, 4 and 5](../../goals/hmm-rebalancing/paper-notes.md).
The local paper text was checked at pages 64, 69 and 75.

## Shared regression rules

The default sample is 1997-09-10 through 2023-03-17, inclusive.
Regressors at t predict the return at the next panel trading day, t+1.
Alignment, lagging and the trailing control use the full panel calendar.
Sample selection and missing-value removal happen afterward.
Both predictor and response dates must be inside the sample.
Each column uses its own complete observations. No returns are filled.
Every regression includes an intercept and uses HC1 standard errors by default.
`--se hc0` and `--se hac --hac-lags N` expose covariance alternatives.
The output records actual response dates, N and the covariance method.
`robustness_extra.metadata.json` also records these values for each column.

## D.4: index returns

The dependent variable is `r_sp500tr - r_agg`. The panel's `r_agg` is VBMFX
throughout the study. This module makes no AGG splice.

The default reading rebuilds Threshold, Calendar and Momentum from this index
pair with `rebal.signals.build`. It supplies `r_sp500tr` to that API as well.
The paper says signals are constructed as in Section 1.2, but does not clearly
name the return pair for this table. Rebuilding makes the instrument change
apply to both portfolio drift and the dependent variable.
`--d4-signals futures` retains the core futures signals and Momentum instead.
Both readings use the index spread for the response and the Ret control.
`--timing clean` is the default; `--timing literal` exposes the existing timing variant.
Leading and trailing missing index returns restrict the simulation span.
An internal gap causes a clear error. The module neither fills returns nor
joins observations across a missing day to simulate portfolio drift.

Column 1 uses Threshold, Calendar, week4, Calendar × week4, Momentum and Ret.
Only column 1 is exported. It includes the `threshold` and `calendar:week4` terms.

## D.9: control units and unavailable FEARS

Each column adds exactly one control to Table 1 column 1:

| Column | Control | Scaling |
| --- | --- | --- |
| 1 | `ra_bex` | Published risk-aversion level; multiplier 1 |
| 2 | `unc_bex` | Published uncertainty level; multiplier 1 |
| 4 | `ara` | Published retail-attention level; multiplier 1 |

There is no division by 100, logarithm, centering or standardization.
The paper does not state the BEX or ARA scaling (§5.7).
Keeping source units gives each coefficient a direct meaning: return per unit
of the published control. A constant rescaling would leave the signal
coefficients unchanged. VIX, MOVE, EPU, ADS and Sentiment are absent here.
ARA is limited to predictor dates 2004-07-01 through 2019-12-31, as in the paper.
This removes forward-filled observations beyond the published endpoint.
BEX uses its available complete observations within the requested study window.
The real smoke run gives N = 6,317 for each BEX column and N = 3,843 for ARA.
The BEX response dates run from 1997-09-11 through 2023-03-17.
ARA response dates run from 2004-07-02 through 2020-01-02. Its last predictor
is 2019-12-31, so its next-trading-day response falls in 2020.
The outcome and metadata sidecar record these samples as well.

Column 3 (FEARS) is skipped. The authors' private full-sample FEARS data are
unavailable. The public 2004–2011 subset is out of scope.
No column 3 rows are written. The metadata contains a `skipped` note with this reason.

## D.14: international returns and the extra lag

The dependent variable is `r_acwxus - rf_3m`.
The panel uses exact MSCI ACWI ex USA net total return in USD.
The MSCI level history starts on 2000-12-29. Its first panel return is
2001-01-02 because a return needs two levels. Earlier returns remain missing.
The module also masks all outcome dates before 2000-12-29.

For response date t+1, Threshold and Calendar are taken from t−1.
This is one extra trading-day lag beyond the usual t predictors.
`--d14-lag 0` exposes the unlagged timing check.
Momentum and week4 remain at t. The interaction is `calendar[t-1] * week4[t]`:
the portfolio signal is lagged, while the known month-end calendar refers to t.
The paper says to lag the rebalancing signals; it does not explicitly address
the interaction's dummy. This convention preserves the current prediction-date bucket.

The control replaces Ret with the compounded 2-day trailing S&P 500 total return:
`(1 + r_sp500tr[t]) * (1 + r_sp500tr[t-1]) - 1`.
It stays in decimal return units. There is no international-return lag control.
Column 1 uses the same other terms as D.4 and exports `threshold` and `calendar:week4`.
The real N is smaller than the paper's 6,097 because MSCI starts later and the
panel retains only dates with both core return proxies. Missing optional inputs
can remove more observations. The smoke run gives N = 5,503, with response dates
2001-01-02 through 2023-03-17. There are 5,504 panel dates from 2000-12-29
through the endpoint; only the first lacks an international return.

## Demo and commands

Demo mode loads `rebal.io` fixtures and constructs each table's actual design.
It then plants next-day Threshold and Calendar-interaction effects of −0.4 and −0.3,
with small independent noise. D.14 retains its missing pre-MSCI history.
Only synthetic responses are replaced; real mode always uses observed panel returns.
Tests also inject independent responses, compare the rebuilt D.4 design with
NumPy least squares, and distinguish D.14's extra lag using independent daily signals.

1. `uv run python3 -m rebal.exhibits --all --demo --only table_D4 table_D9 table_D14`
2. `uv run python3 -m rebal.exhibits.robustness_extra --demo --d4-signals futures --d14-lag 0`
3. `uv run python3 -m rebal.exhibits.robustness_extra --end latest`
4. `uv run pytest -q tests/test_robustness_extra.py`

Demo outputs stay in ignored `output/demo/`. Real runs write under `output/tables/`.
TASK-026 removes real smoke outputs after checking them; TASK-030 owns the final real run.
