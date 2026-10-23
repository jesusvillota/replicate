# Paper comparison targets

[`targets.csv`](../results/targets.csv) records the numeric results in paper-notes section 4.
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
`calendar:week4`, `momentum` and `ret`. Other interactions also use colons:
`threshold:week4`, `calendar:week1` and `calendar:week3`.
The extension terms are `mom_fast`, `mom_medium`, `mom_slow`, `rev_st`,
`eom_rev` and `threshold_perp`. Control names use lowercase.
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
`ret_1` for Table D.1, `rev_st` for Table D.10 column 1,
and `eom_rev` for Table D.11 column 1. Produced regression CSVs repeat
these model statistics on their term rows, as the exhibit contract requires.

Other keys follow these rules:

| Exhibit | `column` | `term` and units |
|---|---|---|
| `table_1`, `table_3` | `1` (spread/equity), `3` (bonds) | `threshold`, `calendar:week4` with `stat=value`: signed one-SD effects in basis points, from `magnitudes.csv`. |
| `table_6a` | `sp500`, `ty`, `strategy` | `mean_pct_pa`, `vol_pct_pa` are annual percentage points; `sharpe`, `skewness` are dimensionless. |
| `table_6b` | `capm`, `c4`, `ff5`, `hxz` | `alpha_pct_pa`, with annual percentage-point SEs. |
| `table_6c` | `ivol`, `liquidity`, `vix`, `move`, `epu` | `high_mean_pct_pa`, `low_mean_pct_pa`, with annual percentage-point SEs. |
| `table_C1` | `threshold`, `calendar` | Printed `mean_annualized`, `sd_annualized`, `ar1`, `skewness`, `excess_kurtosis`; retain source scaling. |
| `table_C2` | Matrix row name | Matrix column name; a correlation. |
| `table_D1` | `1`, `2` | Threshold and Calendar outcomes; `ret_1` is the trailing one-day return. |
| `table_D7` | `1`, `2`, `3` | Equity/bond allocations 86/14, 50/50 and 70/30, respectively. |
| `figure_1` | `equity_share` | `actual_min`, `actual_max`, `target_typical`, in fractions. |
| `figure_2`, `figure_D1`, `figure_D3` | `delta_X_pct` | Threshold in percentage points identifies a plotted t-statistic. Figure D.3 terms identify the during/outside-rebalancing series. |
| `figure_3`, `figure_D2` | `days_N` | `calendar_interaction`: t-statistic for the last-N-days interaction. |
| `figure_4`, `figure_D4` | `day_N` | `threshold` or `calendar:week4`: predictive coefficient. |
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

## Produced CSVs

Real runs read CSVs under `output/tables/` and `output/figures/`.
Demo runs read only `output/demo/`. Both modes read only top-level CSVs,
plus the named legacy `magnitudes/magnitudes.csv` file. They do not scan
subdirectories recursively. `--variant NAME` instead reads only
`robustness/NAME/` below each selected folder, with no fallback to main.
Variant magnitudes may use the same named legacy subfolder.
The default report is `output/compare.md`, or `output/demo/compare.md` with
`--demo`. `--out FILE` overrides the destination.

Regression CSVs follow the exhibit contract's full wide schema:

```text
exhibit,column,term,coef,se,t,p,nobs,adj_r2,se_type,sample_start,sample_end
```

Figure and summary exporters can use keyed long data:

```text
exhibit,column,term,stat,value
```

For example, a Figure 3 row can use
`figure_3,days_4,calendar_interaction,t,-3.1`. A scalar summary can instead
use wide data with `exhibit,column,term,value`. The comparison requires the
exact target keys and units. It does not adapt arbitrary plotting columns.

The one-SD targets use the baseline columns of Tables 1 and 3. Their keys
match the original `exhibit,column,term` fields in TASK-014's magnitude file.
Only its signed `magnitude_bps` field becomes `stat=value`; its `coef` field
is not loaded again. Demo input is `output/demo/magnitudes/magnitudes.csv`;
real input is `output/tables/magnitudes.csv`. Spread and equity effects have
negative paper values; bond effects have positive values. The paper describes
the effect of a signal decrease, so those text magnitudes reverse direction
when expressed as coefficient times a positive SD. No absolute value is taken.

Each CSV is validated before any of its rows enter the join. Unsupported
layouts, malformed rows, invalid statistics, non-finite values and duplicate
keys cause that file to be skipped. A later file with a key already loaded
is also skipped. Other files remain available. The summary lists every skipped
file with its reason, including keyed files without any target keys.
Invalid targets still fail: they are the comparison's required source.

Tables C.1 and C.2 already have keyed exports. Their fourteen targets join.
`figure_C1.csv` lacks comparison keys and is listed as skipped.
TASK-014's D2, D5 and D13 have no targets in paper-notes section 4; their
files are reported as skipped with no matching target keys. Every target
for its other twelve produced tables must join, including the magnitude rows.

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
   positive cost magnitude in `costs`. They are separate targets. The sign
   conflict remains unresolved; comparison sidecars leave all four random-cost
   values blank. No sign flip or absolute value is applied.
6. Figure 6, PDF page 42, labels its axis "Cumulative Gains (Log Scale)".
   The targets preserve the plotted readings, about 6.2 and 2.3. They do not
   assume a conversion to either wealth multiples or unshifted log returns.
7. The bond one-SD effects, **4.1 bps** and **2.3 bps**, are on PDF page
   **33**, with the equity effects. The previous citation to page 35 was wrong.

All other section 4 numeric estimates agree with the source at their stated
precision. Full table extraction was checked against the original PDF text.
Chart readings were checked on rendered PDF pages 9, 13, 15, 24, 28, 42,
58, 59, 60 and 61. The quoted household cost remains the paper's rounded
"almost $200" estimate, not a new calculation.

## Canonical sidecars (TASK-023)

Each changed exporter writes `<id>_comparison.csv` next to `<id>.csv`.
The sidecar uses `exhibit,column,term,stat,value`. Discovery reads it through
its top-level `*.csv` rule. The original plotted data and regression layouts
remain available. Sidecars use computed values, never the paper targets.

Costs map `calendar`, `threshold_min`, `threshold_max`, `threshold_average`,
`threshold_fixed_1pct_average` and `headline` to their named annual-bps keys.
`dollar_cost_paper` and `per_household_paper` supply annual dollar targets.
Values already use the corrected TASK-022 units. DEC-005 excludes delta=0
from default summaries; all raw per-delta estimates remain available.

Table 6A maps `r_es/r_ty` to `sp500/ty` and `volatility_pct_pa` to
`vol_pct_pa`. Table 6B lowercases model names and maps `alpha` to
`alpha_pct_pa`. Table 6C splits `control:H/L` into its control column and
`high_mean_pct_pa/low_mean_pct_pa`. No further annualization is applied.

Calibration figures use one-decimal delta keys (`delta_1.8_pct`), or
`days_N` window keys. Figure D3 maps the rebalancing/other series to
during/outside-rebalancing terms. Horizon figures use `day_N` and preserve
coefficients in decimal return per decimal weight.

The Figure 2 weakening summary is the first increasing sampled delta where
`abs(t) < 2.58`. This is a grid summary, not an interpolated crossing or a
claim that all later deltas remain insignificant. Use the calibration CLI's
`--weakening-critical-t` to change this reference. Its default follows the
paper's 1% line; comparison significance checks still use 1.96.
Figure 4 summaries use the first sampled horizon whose 95% confidence band
contains zero, including an endpoint. If no crossing occurs on the sampled
grid, the summary value is blank. Undefined subset estimates are also blank.

Figure 6 and Figure D5 sidecars retain target keys with blank values.
Figure 6 requires an unresolved paper axis transformation. Figure D5 and
the random-cost summary require an unresolved sign convention. Keeping their
keys supports export coverage checks without inventing numeric comparisons.
The report lists these as `paper-only data` with the specific ambiguity.
It counts numeric matches separately from joined export keys.

Every target without a numeric match has a reason: `no export`,
`paper-only data`, or `not available`. Private FEARS (Table D9 column 3)
and licensed ANcerno targets are `not available`; they are not failures.
A supplied blank value is `not available` when no finite estimate or crossing
exists. A missing selected file or statistic is `no export`.

The comparison integration lives in `rebal.comparison_exports`. The shared
`rebal.compare` module only calls discovery and coverage helpers, adds the
variant argument, and records whether each target key joined. No target
keys, paper readings, contracts or analysis specifications were changed.
