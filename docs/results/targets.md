# Paper comparison targets

`targets.csv` records the numeric results in paper-notes section 4.
The source is the January 14, 2026 version of Harvey, Mazzoleni and Melone,
*The Unintended Consequences of Rebalancing*, stored at the repository root.
The original PDF controls where the notes and the paper differ.

## Schema and units

The CSV key is `exhibit,column,term,stat`. The comparison joins an estimate to
its target on `exhibit,column,term`, then selects the named `stat`.
Produced CSVs may be wide (`exhibit,column,term,coef,se,t,nobs,adj_r2,value`)
or long (`exhibit,column,term,stat,value`). The contract regression CSV adds
its other required fields. Join strings must match exactly, including case
and column names. There are no guessed aliases or automatic unit conversions.
For figures, use a canonical comparison CSV with these keys; an arbitrary
plotting-data layout cannot be joined without an explicit export.

`source_page` is the one-based PDF page number. Subtract two for the printed
page number. For example, Table 1 is PDF page 19, printed page 17.

`approx=1` means a chart reading. Every chart value was checked on a rendered
page. Printed table entries, text estimates and the printed Figure D.5 legend
have `approx=0`. The flag describes the source, not precision: a rounded text
estimate remains rounded even when the flag is zero. Dates, sample periods,
column numbers and axis coordinates are metadata, not separate estimates.

Regression coefficients and standard errors retain the paper's units and
rounding. Returns and portfolio weights use fractions where the table does.
The canonical signal names are `threshold`, `calendar`, `week4`,
`calendar_week4`, `momentum` and `ret`. Control names use lowercase.
Regression `coef` targets have companion `se` targets where the paper gives
standard errors. No t-statistics are invented from significance stars.
A comparison may calculate `coef / se` from the printed values. Rounding can
make this differ from the authors' unrounded t-statistic near a cutoff.

Regression columns use their printed numbers. Table 1 includes all five
columns and all displayed estimates. Table 2 is split into `table_2a` and
`table_2b`; Table 3 includes all four displayed columns. Table 4 columns
`1`, `2`, `3` mean 1961-2023, 1961-1997 and 1997-2023. Table 5 columns
`1`, `2` mean R1K/R2K and Value/Growth. Model `nobs` and `adj_r2` targets
attach to the first estimated term, usually `threshold`. Exceptions are
`ret_1d` for Table D.1, `short_term_reversal` for Table D.10 column 1,
and `eom_reversal` for Table D.11 column 1. Produced regression CSVs repeat
these model statistics on their term rows, as the exhibit contract requires.

Other keys follow these rules:

| Exhibit | `column` | `term` and units |
|---|---|---|
| `table_1`, `table_3` | `one_sd_bps` | One-standard-deviation return magnitudes in basis points; Table 3 prefixes terms with `sp500_` or `ty_`. |
| `table_6a` | `sp500`, `ty`, `strategy` | `mean_pct_pa`, `vol_pct_pa` are annual percentage points; `sharpe`, `skewness` are dimensionless. |
| `table_6b` | `capm`, `c4`, `ff5`, `hxz` | `alpha_pct_pa`, with annual percentage-point SEs. |
| `table_6c` | `ivol`, `liquidity`, `vix`, `move`, `epu` | `high_mean_pct_pa`, `low_mean_pct_pa`, with annual percentage-point SEs. |
| `table_C1` | `threshold`, `calendar` | Printed `mean_annualized`, `sd_annualized`, `ar1`, `skewness`, `excess_kurtosis`; retain source scaling. |
| `table_C2` | Matrix row name | Matrix column name; a correlation. |
| `table_D1` | `threshold`, `calendar` | `ret_1d`: coefficient on trailing one-day return. |
| `table_D7` | `86_14`, `50_50`, `70_30` | Equity/bond allocation identifies the regression. |
| `figure_1` | `equity_share` | `actual_min`, `actual_max`, `target_typical`, in fractions. |
| `figure_2`, `figure_D1`, `figure_D3` | `delta_X_pct` | Threshold in percentage points identifies a plotted t-statistic. Figure D.3 terms identify the during/outside-rebalancing series. |
| `figure_3`, `figure_D2` | `days_N` | `calendar_interaction`: t-statistic for the last-N-days interaction. |
| `figure_4`, `figure_D4` | `day_N` | `threshold` or `calendar_week4`: predictive coefficient. |
| `figure_4` | `summary` | First insignificant horizon, in trading days, based on the plotted 95% band. |
| `figure_5` | Investor group/source | `threshold` or `calendar`: correlation. |
| `figure_6` | `sample_end` | `strategy`, `sp500`: terminal readings on the axis labeled "Cumulative Gains (Log Scale)". |
| `figure_D5` | `random` | Signed `mean_bps`, `ci95_low_bps`, `ci95_high_bps`. |
| `costs` | Rebalancing rule or beneficiary | `annual*_bps` in annual basis points; `annual_usd` in dollars per year. |

`figure_2,summary,one_pct_weakening_delta_pct` preserves the notes' rough
2.7-percentage-point threshold. It refers to the chart's 1% reference line.
It does not set the comparison report's 5% significance rule (`abs(t)>=1.96`).
Figure D.3 stores representative coordinates for the notes' qualitative range.
Only visible source coordinates are recorded; unreported coordinates are not
interpolated or assigned invented values.
It does not treat that range as a constant coefficient across all thresholds.

`figure_1`, `figure_5`, `table_4` and `table_5` appear in section 4 but are absent
from the current exhibit contract's ID list. Their paper targets are retained.
The comparison should report them missing until their CSVs exist.
No task specification or exhibit contract is changed here.

## Source checks and corrections to paper-notes section 4

1. Table D.1, PDF page 62, gives Calendar adjusted R-squared as **0.7194**.
   The notes round this to 0.719. The target preserves the table's precision.
2. Table 3, PDF page 34, has **6,223** observations in each of its four columns.
   Section 4's opening default of 6,226 does not apply to this table.
3. Figure D.3, PDF page 59, does not show uniformly insignificant results
   outside predicted rebalancing days. The orange bars reach about **+2.5**
   at delta 0.3% and **-3.0** at delta 2.3%. The latter exceeds even the
   chart's 1% reference line. The notes' blanket statement is too strong.
   During-rebalancing t-statistics also weaken at large thresholds; their
   approximate minimum is **-6.1** at delta 1.8%.
4. Figure 2, PDF page 13, uses a **1%** critical reference line, about 2.58.
   The notes' "mostly insignificant above about 2.7%" refers to that line.
   Several larger-threshold bars still exceed 1.96 in absolute value.
5. Figure D.5, PDF page 61, prints **Mean = -0.6 bps** in its legend.
   The cost discussion on PDF page 22 reports a positive **0.6 bps** cost.
   Both source conventions are retained: signed chart mean in `figure_D5`,
   positive cost magnitude in `costs`. They are separate targets.
6. Figure 6, PDF page 42, labels its axis "Cumulative Gains (Log Scale)".
   The targets preserve the plotted readings, about 6.2 and 2.3. They do not
   assume a conversion to either wealth multiples or unshifted log returns.

All other section 4 numeric estimates agree with the source at their stated
precision. Full table extraction was checked against the original PDF text.
Chart readings were checked on rendered PDF pages 9, 13, 15, 24, 28, 42,
58, 59, 60 and 61. The quoted household cost remains the paper's rounded
"almost $200" estimate, not a new calculation.
