# Front-running strategy

This module implements Section 4, Table 6 A–C and Figure 6.
The inputs and output locations follow these contracts:
[daily panel](../contracts/daily_panel.md),
[signals](../contracts/signals.md), and
[exhibits](../contracts/exhibits.md).

## Weights and timing

The Threshold component is `-threshold_t / 0.015`.
The Calendar component is `-sign(calendar_t)` on week4 days.
On the first trading day of each new month, it is the sign of Calendar
on the first week4 day of the previous calendar month.
On all other days, the Calendar component is zero.
The strategy weight is the arithmetic mean of the two components.
We do not clip weights or fit the scaling constant to demo returns.

This resolves paper-notes §5.10 with the default required by TASK-017.
`--cal-reversal lag4` instead uses Calendar four panel trading days before
the first trading day of the month. The default is `previous-week4`.
The sign is evaluated each day in week4; we do not freeze its first value.
The first-day reversal takes precedence if a very short month overlaps week4.
An unavailable previous-month reference remains missing.

We build weights on the full panel trading calendar before sample selection.
Each signal at `t` earns `(r_es[t+1] - r_ty[t+1]) * weight[t]`.
Missing signal dates do not change which panel day is `t+1`.
Both signal and return dates must fall in the requested sample.
The default sample is 1997-09-10 through 2023-03-17; `--end latest` uses
the last panel date. Output dates describe realized returns at `t+1`.
The default demo therefore starts its return sample on 1997-09-11.
Missing or nonfinite strategy returns are excluded, without filling returns.

Factors are measured on the realized return date, `t+1`.
Regime controls are measured on the signal date, `t`.
The panel returns are already excess returns. No further cash return is deducted.

## Demo returns

`rebal.demo.make_signals` plants its negative effects in `signals.ret`.
Its independent panel spread has no planted effect, by contract.
With `demo=True`, this module copies the loaded panel and sets
`r_es = r_ty + signals.ret`, before next-day alignment.
Thus the demo still evaluates the specified two-leg return formula.
The shared fixtures and input frames remain unchanged.
Factors and controls remain synthetic fixture values; demo statistics do not
estimate the paper's empirical performance. Real mode always uses the panel
returns directly and ignores `signals.ret`.

## Performance and transaction costs

Annual mean is daily mean times 252; annual volatility is sample standard
deviation (`ddof=1`) times `sqrt(252)`. Sharpe ratio is their quotient.
Skewness uses the bias-corrected Fisher–Pearson sample estimator.
Means and volatilities in Table 6A are percentages per year.

We obtained Harvey, Hoyle, Korgaonkar, Rattray, Sargaison and Van Hemert
(2018), *The impact of volatility targeting*, Journal of Portfolio Management
45, 14–33, from the
[author's PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)
on 2026-10-22. PDF page 5 states costs as fractions of notional traded:
**1.0 bp for equities and 0.5 bp for bonds**.
Here one basis point (bp) is 0.0001 of notional.
Footnote 12 notes that these estimates describe markets after the 2008 crisis
and may not represent earlier costs. We apply the constants across the sample.
The authorized 1 bp per leg fallback was not needed.

Each leg trades `abs(weight_t - weight_{t-1})` units of notional.
Total two-leg turnover is twice this amount. Net return deducts
`abs(delta_weight) * (1.0 + 0.5) / 10000`.
`--equity-cost-bps` and `--bond-cost-bps` override these one-way costs.
Both position increases and decreases incur costs. Positions before sample
start determine the first sample trade; we do not restart the strategy there.
The full input history starts from zero. A missing prior position leaves net
return missing; it does not imply a free trade. We exclude neither commissions
nor slippage separately, and do not add futures roll costs. The cited paper
also excludes turnover from futures rolls.

The crisis-exclusion row removes realized returns in September 2008 through
March 2009 and March 2020, inclusive, without rebuilding weights or joining
disconnected days into new holding periods.

The paper describes each component as contributing 11.6% annual volatility.
We interpret this as the volatility of the standalone component's **return**:
the stock-minus-bond return times its full component weight, before averaging.
Table 6A reports both component rows without fitting their demo volatilities
to 11.6%. Weight volatility is not an asset-return volatility.

## Factor models and regimes

Table 6B calls `rebal.regress.ols`, with an intercept and these models:

| Model | Factors |
|---|---|
| CAPM | `mkt_rf` |
| C4 | `mkt_rf`, `smb`, `hml`, `mom` |
| FF5 | `mkt_rf`, `smb`, `hml`, `rmw`, `cma` |
| HXZ | `q_mkt`, `q_me`, `q_ia`, `q_roe` |

Each model uses its own complete observations. The default covariance is HC1,
a correction that permits error variance to differ across days and adjusts
for estimated parameters. `--se hc0` omits that parameter-count adjustment.
Alpha and its standard error are multiplied by `252 * 100`.
The t-statistic and p-value remain those of the daily regression.

Table 6C uses one full-sample median for each of `ivol`, `liquidity`, `vix`,
`move`, and `epu` at `t`, over the strategy's retained sample pairs.
We exclude nonfinite controls separately for each split. Values strictly above
the median are high; ties join low. The medians do not change by regime.
An intercept-only OLS gives each regime mean and its HC standard error.
Both are annualized in percent, matching Panel B's units and CSV schema.
Missing factors do not remove observations from Panels A or C.

## Figure and output columns

Figure 6 scales daily strategy returns once by
`std(r_es) / std(strategy)` on their common sample.
It then plots cumulative `log1p` returns for this scaled series and both assets.
Asset returns remain the excess returns from the panel, consistent with Table 6.
The module fails if any scaled return is at most -1, rather than clipping it.
No full-sample volatility scale enters the trading weights or Table 6.
The first plotted point includes the first day's log return, with zero
understood as initial wealth's log value before that day.

Table 6A is a descriptive table with columns `asset`, `mean_pct_pa`,
`volatility_pct_pa`, `sharpe`, `skewness`, `nobs`, `sample_start`, `sample_end`.
Its rows include gross strategy, both assets, net strategy, both standalone
components, and strategy excluding crises. Zero volatility yields undefined
Sharpe ratio and skewness. Tables 6B and 6C use the exact ordered regression
columns in the exhibit contract; terms are `alpha` and `mean`, respectively.

The plotted CSV has `date`, `strategy_log_gain`, `r_es_log_gain`, and
`r_ty_log_gain`. Log gains are dimensionless, without multiplication by 100.
The JSON sidecar records input loaders, demo substitution, parameters,
actual sample, medians, volatility scale, cost source and artifact paths.
All demo artifacts go to the ignored `output/demo/` directory.
