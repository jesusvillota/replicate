# Calibration and horizon figures

The inputs and outputs follow [daily_panel](../contracts/daily_panel.md),
[signals](../contracts/signals.md) and [exhibits](../contracts/exhibits.md).
Equations and exhibit definitions come from
[paper-notes §3.3, §3.5 and §4](../../goals/hmm-rebalancing/paper-notes.md).
These builders use `rebal.regress.ols`, `predictive` and `predictive_data`.
They use `rebal.io` for both demo fixtures and real input files.

The default sample is 1997-09-10 through 2023-03-17. Both the origin date
and final outcome date must be inside it. `--end latest` extends the sample.
Leads and windows are built on the complete panel trading calendar before
sample selection or subset selection. Missing days are never compressed.
Missing values inside a future window invalidate that window.

## Calibration

Figures 2 and D1 fit eq. (1) separately for each of the 41 `thr_*` signals.
Their x coordinate `delta_pct` is delta in percent portfolio weight:
`thr_010` is 1.0%, or 0.01 in the regression input. Each plot also shows
the aggregate `threshold` t-statistic as a horizontal dotted line. That
line's CSV row has `series=aggregate` and a missing `delta_pct`, because
the aggregate has no single delta. It uses the supplied contract column.

Figure D3 fits eq. (1) independently on days with `abs(thr_delta) >= delta`
and on days with `abs(thr_delta) < delta`. Equality belongs to the first
subset. Selection uses the signal date; the response stays on the next
actual trading day. At delta=0 the second subset is empty. Any subset with
fewer than three rows, or a constant signal, has `status=not_estimable`.
Its estimates and dates are missing; `nobs` reports its actual size. Such
rows create plot gaps. We do not report invented zero t-statistics.

Figures 3 and D2 fit eq. (3) for each N=1,...,10. `dummy` equals
`days_to_month_end <= N`; these counts are inclusive and already supplied
by the signal contract. The plotted coefficient is `calendar:dummy`.
Each calibration CSV includes the plotted `t`, the fitted `coef`, `se`,
`p`, `nobs`, `se_type`, actual outcome sample dates and `critical_t=-2.58`.
The reference line is the paper's single-test 1% reference; it does not
adjust for multiple testing.

## Horizon outcomes

Both figures use the six eq. (4)/(5) regressors: `threshold`, `calendar`,
`week4`, `calendar:week4`, `momentum`, and contemporaneous `ret`, plus an
intercept. There are no extra controls. Each horizon is fit on its own
complete sample. The plots show Threshold and Calendar × week4 in separate
panels. They do not combine the Calendar main effect with the interaction.

Figure 4 uses `sum(log1p(ret[t+j]), j=1,...,h)` for h=1,...,15.
We apply `log1p` to the contract's simple cross-asset `ret`, as the task
requires; we do not substitute the difference between the asset log returns.
Returns at or below -1 raise an error. Figure D4 predicts only the simple
`ret[t+h]`, with no sum and no subsampling of origins. Its future returns
do not overlap within each regression. Regressors remain at t.

`horizon_days` counts trading days. `coef`, `se`, `ci_low` and `ci_high`
measure return per decimal portfolio weight. A coefficient of -0.4 means
a one-percentage-point signal predicts a -0.004 return. Confidence bands
are `coef ± norm.ppf(0.975)*se`, recorded in each CSV and used verbatim
for plotting. PDFs use no external TeX installation.

## Hodrick (1992) 1B covariance

For each retained origin t, let x_t include the intercept and let
y_t be the h-period sum of one-day log returns. `rebal.regress.ols`
estimates the usual coefficients. Inference uses the no-predictability
null: one-day innovations are u_q = r_q - mean(r), rather than residuals
from an overlapping-horizon regression. The mean uses the unique daily
returns that contribute to retained outcomes.

Reverse the order of summation in the regression score. For each daily
outcome date q define

```text
w_q = sum of x_t over retained origins satisfying t < q <= t+h
s_q = u_q * w_q
A   = sum_t x_t x_t'
V_1B = A^(-1) [sum_q s_q s_q'] A^(-1).
```

For interior observations, w_q is the backward sum of the h regressor
vectors x_(q-1),...,x_(q-h). This is the Hodrick 1B reverse-regression
construction used for overlapping returns, as in Ang and Bekaert (2007).
The full intercept is included in the sandwich. The implied slope block
therefore accounts for regressor means. This is a null-based covariance;
the demo's nonzero effects do not make it an alternative-model estimator.

At sample edges we include only origins that actually enter OLS. This
avoids discarding usable return innovations or importing origins outside
the sample. A missing regressor removes its origin from every reverse
sum, while the calendar positions stay fixed. No Bartlett weighting,
overlapping residuals, or extra degrees-of-freedom multiplier enters 1B.
This formula assumes uncorrelated one-day null innovations and permits
conditional heteroskedasticity. It does not correct arbitrary serial
correlation in one-day returns.

## Paper ambiguities and exposed choices

The paper does not state the HC variant, HAC lag count, or exact Hodrick
implementation (paper-notes §5.6). We use HC1 by default, consistent with
TASK-014. `--se hc0` selects HC0 for Figures 2, 3, D3 and D4. Figures D1
and D2 always use Bartlett Newey–West HAC without a small-sample multiplier.
Their default lag count is `floor(4*(nobs/100)^(2/9))`, from TASK-014;
`--hac-lags N` overrides it in the calibration module. Figure 4 always
uses the 1B formula above and normal 95% bands. Signal timing is inherited
from the selected signal file; both modules expose `--timing clean|...`.
The runner uses all these defaults.

Each module writes a JSON lineage file containing inputs, run time,
parameters and output filenames. Actual estimation dates and counts are
recorded separately for every plotted fit. Demo files stay git-ignored.
`tests/test_horizons.py` checks independent coefficient/covariance oracles,
sample edges, conditional subsets, planted and zero effects, and the actual
plot artists against the written CSVs. Its size test uses 200 draws,
1,000 dates, independent Gaussian returns, an AR(1) regressor with rho=0.9,
h=5 and a fixed seed of 2026. It reports both Hodrick and naive OLS rejection
rates at the two-sided normal 5% threshold.
