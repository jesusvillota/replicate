# ES and TY proxy comparison

TASK-011 supplies evidence for DEC-001. It does not choose the final panel.
See [the generated report](../data/proxy_comparison.md) for metrics, input hashes,
coverage limits, the proposed pair, and the robustness pair.

## Reusable returns

`rebal.proxies` exposes one pure function for each available candidate:
`es_spy`, `es_total_return`, `es_futures`, `ty_zero_10`, `ty_par_10`,
`ty_zero_65`, `ty_ief`, and `ty_futures`. Each returns a date-indexed
`pandas.Series` of decimal daily simple excess returns. Inputs must have
unique, increasing dates on the intended common trading calendar. Cash inputs
use decimal RF; GSW inputs retain the source's percent-per-year yield units.
Futures repair references must already be excess returns.

Align prices and curves before calculating returns. Do not fill missing prices
or yields. The CLI uses French equity trading dates and French daily RF / 100.
If that file is absent, it uses SPY dates and lagged FRED DTB3 discount quotes.
For that fallback, a 91-day bill has price `1 - (DTB3/100)*91/360`.
Its implied holding return accrues over actual calendar days. Only the cash-rate
quote is carried forward. Source cards describe regeneration; this CLI does
not download data or change upstream files.

## Bond construction

Each daily holding interval starts with a new bond at the target maturity.
The return prices that same bond at the end of the interval, after it ages.
It includes carry and curve changes. Subtract RF afterward.

For zero bonds, use `exp(n*y_previous - (n-delta)*y_today(n-delta)) - 1`,
with decimal continuous yields and actual calendar days / 365.25 for `delta`.
Interpolate published GSW zero yields linearly: SVENY09/10 for T1 and
SVENY06/07 for T3. Set T3 maturity to 6.5 years, as a transparent approximate
duration match. No cheapest-to-deliver bond history was available to estimate
a time-varying duration.

For T2, set the annual coupon to yesterday's SVENPY10 / 100. Keep it fixed
during the interval. Price semiannual coupons and principal with the previous
and current Svensson curves, using all six published parameters. Current
cashflows have shorter remaining maturities. Dirty prices include accrued
interest. The coupon resets after the return is measured. Missing active
parameters leave returns missing; an inactive second factor permits a missing
TAU2 only when BETA3 is zero.

## Rolls and comparison

Yahoo supplies front-month prices, without individual contract identities.
A third-Friday-only rule can miss the switch. Use a conservative window from
eight calendar days before each quarterly third Friday through the next Monday.
Also flag absolute residual jumps against E2 or T3, at fixed thresholds of
2 percentage points for ES and 1 percentage point for TY. These thresholds
screen large anomalies and were not fitted to maximize correlation. They can
also exclude close-time errors. The calendar is a heuristic for both contracts;
it does not establish the actual TY delivery or switch date.

Replace flagged ES returns with E2, and flagged TY returns with T3. Do not
create history before futures inception. Missing references remain missing.
Exclude every flagged day from the futures benchmark, including dates whose
reference is missing. Report actual replacements in the study interval.

Use sample standard deviation and 252 sessions for annualized tracking error.
For lead/lag correlations, shift the full session grid before filtering.
Compute the Calendar stand-in on identical common clean sessions for both
series. The resulting month sums omit excluded sessions, so they are a partial
month diagnostic. They cannot validate the full Calendar signal.

Compare every available ES/TY pair. Rank pairs with full study endpoint
coverage by tracking error on the same clean benchmark dates for all full-history
cash candidates. Keep intervening missing sessions explicit. Recommend the best
pair and a second full-history pair with different constructions for both legs.
Full futures self-comparisons have mechanical perfect fit on clean days; do not
use them to choose a full-history pair. No licensed WRDS futures or fixed-term
Treasury index was available in TASK-010.

Close-time differences, approximate duration, missing sessions, and roll-screen
choices remain limits. TASK-012 can integrate the chosen series after DEC-001.
A later sensitivity analysis can vary duration and roll rules. This task does
not splice returns, shift close times, or record the decision.
