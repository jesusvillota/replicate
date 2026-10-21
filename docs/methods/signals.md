# Signal construction

This module implements [the signals contract](../contracts/signals.md).
The source is [paper-notes §3.2, §3.4, §3.6 and §5](../../goals/hmm-rebalancing/paper-notes.md).
Appendix B and Tables C.1–C.2 were also checked against the paper's OCR.

## Portfolio weights and timing

Inputs are aligned, finite simple decimal returns, with naive midnight dates.
Dates must be sorted and unique. Each asset return must exceed −1.
The simulator starts at the target immediately before the first supplied return.
It processes that return on the first row. It does not discard the row.

For previous post-trade weight `p`, the new pre-trade weight is:

```text
w_pre[t] = p * (1 + r_eq[t]) / (p * (1 + r_eq[t]) + (1-p) * (1 + r_bd[t]))
signal[t] = w_pre[t] - target
trade[t] = w_post[t] - w_pre[t]
```

With `--timing clean` (default), Threshold resets at that close when
`abs(signal[t]) >= delta`. Calendar resets at the last supplied trading close of each month.
The final supplied date counts as month-end, including a truncated final month.
`simulate_dates` resets at the close of exactly the selected input dates.
All three APIs return the input date index and `w_pre`, `w_post`, `trade`.
A positive trade buys equity. A zero-sized reset has zero `trade`.

With `--timing literal`, Appendix B's condition uses the previous date.
Threshold tests `abs(w_post[t-1] - target) >= delta`, then resets at close `t`.
Calendar resets at the next supplied trading close after month-end.
The signal still uses today's drift before today's reset. It is not a shifted clean signal.
The first previous weight is the target; there is no prior month-end flag.
For either timing, signals dated `t` predict returns dated `t+1`.

The default Threshold averages all 26 deviations from δ = 0 through 0.025 inclusive.
The file also includes the 41 individual paths through δ = 0.040.
The 0.86, 0.50 and 0.70 target variants rerun the complete recursion.
They do not rescale the 60/40 path. The absolute δ grid stays the same.
Custom API grids must retain the 26 aggregate points. They may omit diagnostics above 0.025.
The full default grid produces the exact contract columns and order.

## Momentum and reversal returns

`ret` is the daily simple spread `r_eq - r_bd`.
A cumulative k-day spread return is `product(1 + ret[t-k+1:t+1]) - 1`.
This compounds the daily spread. It does not subtract two compounded asset returns.
The sign of exactly zero is zero.

Fast momentum averages signs for k = 1–10. Medium averages k = 11–20.
Slow averages k = 21, 42, 63, 126 and 252.
The default `--momentum medium-slow` gives medium and slow equal weight.
`--momentum all15` gives each of their 15 signs equal weight.
Fast momentum never enters that aggregate. Each family requires all its lookbacks.
No partial-window averages are used.

`rev_st` compounds `ret` from t−4 through t.
`rev_lt` compounds `ret` from t−1259 through t−252, inclusive: 1008 observations.
It excludes the latest 252 observations and requires 1260 rows of history.

`eom_rev` uses the separately supplied `r_sp500tr`, never the futures return.
The fourth Friday means the fourth occurrence, even in a five-Friday month.
If Friday is closed, the last supplied trading close before it is the anchor.
The anchor day's return is excluded. The following trading day's return is included.
The daily control is zero up to the fourth-Friday close, then compounds through the current close.
At month-end it equals the stated fourth-Friday-to-month-end return.
It resets to zero in the new month. This uses only returns known at each date.
Repeating the final month's return on earlier dates would use future information.
If input begins after the anchor, that month's post-anchor values are missing.
Missing post-anchor S&P returns propagate through month-end. Missing S&P input leaves the entire column missing.
This daily interpretation resolves the paper's unspecified within-month assignment.

## Calendar buckets

Count supplied trading dates backward from each month's end, inclusive.
`days_to_month_end` equals 1 at month-end.
`week4` covers counts 1–5; `week3` covers 6–10; `week2` covers 11–15.
`week1` covers every remaining date. Each row has exactly one bucket.
The calculation uses the full input calendar, before exhibit sample selection.
It does not assume weekdays are an exchange calendar.

## Burn-in

Rows stay in the output during warm-up. Required unavailable histories are `NaN`.
Positions below are one-based, assuming complete return inputs.

| Columns | First valid row | First default demo date |
|---|---:|---|
| date, ret, thr_000…thr_040, threshold, calendar, all target variants | 1 | 1996-01-02 |
| week1…week4, days_to_month_end | 1 | 1996-01-02 |
| mom_fast | 10 | 1996-01-15 |
| mom_medium | 20 | 1996-01-29 |
| mom_slow, momentum (both modes) | 252 | 1996-12-18 |
| rev_st | 5 | 1996-01-08 |
| rev_lt | 1260 | 2000-10-30 |
| eom_rev, with S&P history before the anchor | 1 | 1996-01-02 |

The default demo covers 1996-01-02 through 2023-12-29, using weekdays.
These dates are fixture dates, not claims about exchange sessions.
Real missing asset returns are rejected. Upstream data selection owns that policy.
Descriptive exhibits first build the full history, then select 1997-09-10 through 2023-03-17.
Their standalone CLI accepts `--end latest`.

## Demo trade counts

These are actual nonzero trades from `--timing clean`, on all 7304 demo rows.
The annual rate is `count * 252 / 7304`, matching the paper's trading-year convention.
This avoids treating the demo's 260 weekdays per calendar year as 252 exchange sessions.
Counts are not calibrated to the paper.

| δ | Trades | Trades per 252 days | Paper comparison |
|---:|---:|---:|---|
| 0.0% | 7304 | 252.000 | 252 |
| 0.1% | 5463 | 188.482 | — |
| 0.2% | 3810 | 131.451 | — |
| 0.3% | 2685 | 92.637 | — |
| 0.4% | 1883 | 64.967 | — |
| 0.5% | 1422 | 49.061 | — |
| 0.6% | 1070 | 36.917 | — |
| 0.7% | 854 | 29.464 | — |
| 0.8% | 716 | 24.703 | — |
| 0.9% | 601 | 20.735 | — |
| 1.0% | 499 | 17.216 | — |
| 1.1% | 425 | 14.663 | about 12 |
| 1.2% | 370 | 12.766 | — |
| 1.3% | 330 | 11.386 | — |
| 1.4% | 263 | 9.074 | — |
| 1.5% | 228 | 7.866 | — |
| 1.6% | 232 | 8.004 | — |
| 1.7% | 190 | 6.555 | — |
| 1.8% | 167 | 5.762 | — |
| 1.9% | 170 | 5.865 | — |
| 2.0% | 142 | 4.899 | — |
| 2.1% | 120 | 4.140 | — |
| 2.2% | 119 | 4.106 | — |
| 2.3% | 114 | 3.933 | — |
| 2.4% | 107 | 3.692 | — |
| 2.5% | 99 | 3.416 | about 4 |
| 2.6% | 93 | 3.209 | — |
| 2.7% | 87 | 3.002 | — |
| 2.8% | 85 | 2.933 | — |
| 2.9% | 68 | 2.346 | — |
| 3.0% | 71 | 2.450 | — |
| 3.1% | 68 | 2.346 | — |
| 3.2% | 66 | 2.277 | — |
| 3.3% | 61 | 2.105 | — |
| 3.4% | 61 | 2.105 | — |
| 3.5% | 53 | 1.829 | — |
| 3.6% | 49 | 1.691 | — |
| 3.7% | 49 | 1.691 | — |
| 3.8% | 42 | 1.449 | — |
| 3.9% | 40 | 1.380 | — |
| 4.0% | 44 | 1.518 | — |

Strictly decreasing counts are not guaranteed for every realized return path.
A different threshold changes reset dates and thus the next starting weight.
For example, the demo has 228 trades at 1.5% and 232 at 1.6%.
The count test therefore uses constant positive equity returns and zero bond returns.
On that controlled synthetic path, counts never increase as δ grows.
The CLI reports every original demo count without smoothing or changing the simulation.

## Descriptive exhibits and units

Table C.1 multiplies the daily mean by 252 and the sample SD by √252.
It keeps decimal weight units. It uses adjacent-date Pearson correlation for AR(1),
bias-corrected skewness and bias-corrected excess kurtosis.
The reported paper SD 0.08 implies daily SD `0.08 / sqrt(252) = 0.00504`.
That is close to the 0.0048 implied elsewhere in the paper.
Thus decimals, without another factor of 100, are a plausible Table C.1 convention.
For Calendar, 0.16 implies daily SD 0.01008.
Demo results are written to `table_C1.csv`; synthetic returns need not match paper estimates.
The file records each signal's count and the actual sample dates.

Table C.2 uses one complete-case sample across Threshold, Calendar, Momentum,
VIX, MOVE, EPU, ADS and Sentiment. It writes the full symmetric correlation matrix.
Missing momentum history is excluded; missing controls are not filled.
Its JSON lineage records the complete-case count and selected date range.
Figure C.1 has two panels, with deviations plotted in percentage points.
Its companion CSV retains decimal weights and the exact plotted dates.

Demo exhibits use synthetic panel returns with the actual signal engine.
They do not use the placeholder signals from `rebal.demo.make_signals`.
That fixture and `rebal.io.load_signals(demo=True)` retain their planted-effect contract.
The engine's demo `ret` remains the actual synthetic `r_es - r_ty` spread.
Tests verify descriptive moments against independent Pandas calculations.
They also recover planted positive/negative correlations and a near-zero noise correlation.

No real panel, fetcher, cluster job or regression implementation is part of TASK-013.
