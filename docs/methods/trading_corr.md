# Figure 5: trading correlations

The implementation is `rebal.exhibits.trading_corr`. It follows the
[exhibit contract](../contracts/exhibits.md) and
[signal contract](../contracts/signals.md).
The source definitions are in the [CFTC card](../data/cards/cftc.md) and
[ICI card](../data/cards/ici.md). Paper-notes §3.7, §5.11 and §5.12 identify
the ambiguities below. The paper text on pages 27–30 supplies the direction
of the lag, but does not specify every weekly construction.

## CFTC report and contracts

The default is futures-only legacy COT. Hedgers are commercial traders;
speculators are noncommercial traders. Net positions equal long minus short.
Spreading positions do not enter either signed position.
The sample starts on 2006-08-01, although legacy history starts earlier.
This matches the paper's August 2006 start without changing its group definitions.
TFF history starts in June 2006; its availability alone does not establish
that the paper used its different trader classifications.

`--cftc-report tff` exposes a sensitivity proxy. It maps dealers to hedgers
and sums asset managers, leveraged funds and other reportables as speculators.
These groups are not equivalent to commercial/noncommercial traders.
The default therefore remains legacy. TFF provides the financial-group taxonomy;
the two LTPos columns use the actual LTPos file, not TFF position differences.

`--contract emini` is the default: E-mini S&P market code `13874A`, versus
10-year Treasury code `043602`. LTPos uses ES and TY, respectively.
The E-mini is the equity instrument used for the main signals and has continuing history.
`--contract large` uses full-size S&P code `138741` and LTPos SP.
The full-size contract ends in September 2021. No other contract fills its gaps.
No contracts are combined, and no dollar or notional weights are applied.

For group g and consecutive weekly report dates t and t+1, define

```text
net_g,m,t = long_g,m,t - short_g,m,t
Q_g,t+1 = (net_g,ES,t+1 - net_g,ES,t) / OI_ES,t
          - (net_g,TY,t+1 - net_g,TY,t) / OI_TY,t
```

Thus Q is equity change minus bond change. Each leg uses its own beginning
open interest, as the paper states. Its units are contracts per outstanding contract.
Nonpositive open interest yields a missing value. Q is not the difference
between two position-to-open-interest ratios. Both contracts must be observed
at both endpoints, and dates must be six to eight days apart.
Missing reports are never converted into multiweek changes.

## Weekly signal alignment

The default `--lag-weeks 1` pairs Q ending at t+1 with the signal at t.
For CFTC, t is the previous report date, normally Tuesday. This is a position-date
alignment, not an alignment to the later Friday publication date.
The default `--aggregation date` uses that date's Threshold and Calendar levels.
Calendar is used directly; it is not multiplied by a month-end indicator.
If the reference is a holiday or weekend, use the most recent signal within
four calendar days. No signal after the reference date is used.
Missing signal values are dropped separately for each correlation.

`--aggregation mean` instead uses all available trading-day signals in
`(reference - 7 calendar days, reference]`, with equal weights.
It never uses signals from the response week when the lag is one week.
`--lag-weeks 0` exposes contemporaneous alignment. Larger nonnegative lags
select earlier report weeks. Source gaps invalidate those pairs.

The default response-date end is 2023-03-17, inclusive; `--end latest`
uses all available dates. The reference must also follow the sample start.
`--timing clean` reads `signals_clean.parquet`; other timing files are selectable.
The module does not rebuild or modify signals.

## LTPos aggregation

The source has weekly means of daily directional position changes, in contracts
per day. Use `asset_managers_net_change` and `leveraged_funds_net_change` directly.
For each week, subtract TY from ES (or SP). Do not difference successive rows,
multiply by five, or treat these values as weekly position levels.
No open-interest scaling is applied: LTPos does not supply that denominator.
These are contract-count proxies, not dollar trades.

At the default lag, use the signal before `period_start`: the reference is
the preceding calendar day, whose latest trading signal is normally Friday.
This excludes every day covered by the published daily mean.
For lag k >= 1, move this reference back by another `7 * (k - 1)` days.
For lag zero, use the week-ending date. The weekly-mean option applies to
the trailing week ending at the same reference. Both markets must share a period start.

## ICI flows, blocks and pooling

Use domestic U.S. equity flows minus total bond flows:
`domestic_equity - taxable_bond - municipal_bond`, in USD millions.
The paper says U.S. equity; `total_equity` also includes world equity and is excluded.
Hybrid funds are excluded. Flows are already weekly amounts, so do not difference them.
No monthly data, interpolation, asset scaling or gap filling enters this calculation.

Identify blocks on the complete source calendar before sample selection.
A separation greater than eight days starts a new block. This preserves the
Tuesday/Wednesday holiday shifts documented by the source card.
The real source contains 39 blocks. The default paper endpoint uses 32 blocks;
later blocks remain in the metadata with zero usable observations.
At lag one, pair a flow with the previous observed endpoint inside its own block.
Drop the first flow in every block. At lag k, require k prior endpoints in that
same block and an elapsed time between `6*k` and `8*k` days.
No pair crosses a missing interval. Signal means use only the trailing
seven days ending at the selected reference, not the interval spanning a gap.

Compute Pearson correlation separately in each block for diagnostics.
For the pooled estimate, subtract each block's paired-sample mean from both
series, then pool their centered cross-products and sums of squares:

```text
r = sum_b sum_i (x_bi - mean_b(x)) * (y_bi - mean_b(y))
    / sqrt(sum_b sum_i (x_bi - mean_b(x))^2
           * sum_b sum_i (y_bi - mean_b(y))^2)
```

This removes differences in average flow and signal levels between blocks.
It weights observations through their within-block variation. It is not an
unweighted average of correlations or a correlation across block means.
Singleton paired blocks have no within-block information and are excluded from pooled N.
Constant series give an undefined correlation; the final exhibit fails clearly
if any of its ten pooled correlations is undefined.

`figure_5.metadata.json` records every source block's bounds and source count,
plus separate correlation and paired N for each signal. This includes blocks
outside the selected sample. Pairwise missing values can give different Ns.
The main CSV gives pooled N as `stat=nobs` for each investor/signal pair.

## Outputs and demo

The CSV has exactly `exhibit,column,term,stat,value`. Its five columns use the
target keys: `cftc_hedgers`, `cftc_speculators`, `ltpos_asset_managers`,
`ltpos_leveraged_funds`, and `ici`. Terms are `threshold` and `calendar`.
`stat=value` is a dimensionless correlation; `stat=nobs` is a paired count.
The PDF plots the ten correlation values with a zero line and a common [-1, 1] axis.
ANcerno is unavailable. It has no row, plotted group, or replacement estimate.

Real runs write under `output/figures/`. Demo runs write under ignored
`output/demo/`. Metadata records input paths, parameters, response bounds,
creation time, block diagnostics and output names.
Demo inputs use shared `rebal.io.load_signals(demo=True)` and local deterministic
weekly fixtures, seed 28. No shared demo or IO module is changed.
The fixtures plant negative rebalancer correlations, positive liquidity-provider
correlations, and separated ICI blocks. They are not calibrated to the paper.
Tests also plant independent weekly signals to check lag direction and zero effects.

TASK-028 runs a real-data smoke check and records its numbers in its outcome.
It commits no real output; TASK-030 owns the final run and comparison.
