# Rebalancing costs

This implements paper-notes §3.8 and documents the cost ambiguities in §5.9.
The delta=0 summary policy awaits the TASK-022 decision request.
Inputs and outputs follow [daily_panel](../contracts/daily_panel.md),
[signals](../contracts/signals.md), and [exhibits](../contracts/exhibits.md).
Run `uv run python3 -m rebal.exhibits.costs --demo --n-sims 100` for a quick run.
The exhibit runner uses 10,000 simulations by default, including in demo mode.

## Regression specification and sign

All estimates use `rebal.regress.predictive`, with next-day alignment before
subsetting, an intercept, HC1 errors, and the contract sample. Both predictor
and outcome must be inside the sample. `--end latest` extends its end.
Simulation starts at 60/40 at the beginning of available history. Sampling
never restarts the portfolio. The default timing is the signal engine's `clean`.

The Calendar regression on week4 uses Threshold, Calendar, Momentum and current
Ret, the baseline equation (4) terms. The week4 dummy is constant and its Calendar
interaction duplicates Calendar in this subset, so both are omitted. Each
Threshold regression replaces aggregate Threshold with `thr_delta` and retains
Calendar, week4, Calendar × week4, Momentum and Ret. Select days where
`abs(thr_delta) >= delta`, including equality and delta=0. These choices avoid
counting the same predictor twice. `--controls` adds VIX, MOVE, EPU, ADS and
Sentiment. Without it, use equation (4)'s baseline column, as in the paper's
headline regressions. Missing momentum warm-up rows drop only from regression
estimation. Trade size and frequency use all simulation sample days.

Cost in annual basis points is **−beta × size² × frequency × 10,000**.
Both the return and weight inputs use decimals, per the contracts. The slope
is decimal return per decimal weight; changing both to percentages leaves it
unchanged. First, `beta × size` predicts the cross-asset price change. Then
multiply by the portfolio share traded, also `size`. The annual calculation
uses the square of the mean absolute trade, rather than the mean squared trade,
to follow the paper's average-trade approximation.

For the paper's example, `beta = −0.39`, `size = 0.01`, and `frequency = 12`.
The predicted price change is −0.0039 (−0.39%). Trading 1% of the portfolio
loses 0.000039 of portfolio value per event. Twelve events cost **4.68 bps**.
The previous calculation reported 468 bps because it omitted the portfolio
share traded. All Calendar, Threshold, fixed-size, interaction and random-date
paths now use this same conversion. Tracking error and gross utility already
measure portfolio returns; their conversion to bps remains unchanged.

The printed expression `|−0.39| × 1% × 12 ≈ 5 bps` (paper §2.1.1,
PDF p.21) suppresses a unit or a multiplication: taken literally with the
regression slope, it gives 468 bps. Reading −0.39 as the **percentage price
change for a 1% trade** gives 4.68 bps. This also agrees with the paragraph's
two-step description: multiply the slope by trade size to obtain price impact,
then multiply that price impact by the share traded. Footnote 13 and the
Table 1 one-standard-deviation effects support the slope's decimal/decimal
units. Dividing every slope by 100 would match this one example, but would
make its assumed 1% signal size universal, even at other thresholds.
The square-size reading preserves the stated regression units and scales
impact with the actual trade. The paper does not provide enough per-delta
inputs to reconstruct its complete 6–27 bps range from text alone.
One basis point (bps) is 0.01 percentage points. A negative predictive coefficient
implies a positive loss. A positive coefficient produces a signed gain; do not
clip or take the absolute value. The text gives random-date mean +0.6 bps,
whereas Figure D.5 labels −0.6 bps. We consistently report positive losses,
without forcing a target sign. Demo values are software checks, not estimates
of the paper's market effects.

The full-sample footnote 17 alternative includes the signal, an active-day dummy,
and their interaction, plus the same remaining regressors. Impact on active days
is the **sum of the base and interaction slopes**. For Calendar the active dummy
is week4. For Threshold retain the separate Calendar × week4 term. At delta=0,
the active dummy is always one, so fit the baseline only. Report per-delta
alternative costs, averages, fixed-size average and alternative headline.

## Size, frequency and Calendar variants

Use actual trades from `simulate_calendar`, `simulate_threshold` and
`simulate_dates`. Calendar size is mean absolute nonzero month-end trade;
frequency is fixed at 12. Threshold size is mean absolute trade on the
signal's active days. Frequency is nonzero trades divided by sample trading
days / 252. Thus no annual average is distorted by incomplete calendar years.
For each of 26 deltas (0 through 2.5%, step 0.1%), report impact, size,
annual frequency, cost and cost at a fixed 1% size. In that counterfactual,
keep the slope and frequency unchanged; use 0.01 for both the signal magnitude
and the portfolio share traded. This follows the paper's scenario of trading
earlier, at about 1% deviation, rather than applying the original deviation's
price change to a smaller trade. The headline is half Calendar cost plus
half the mean fixed-size Threshold cost. `--delta-zero include|exclude` selects
the summary grid. The existing inclusion default is retained pending a decision,
not accepted as an economic estimate. Every per-delta row, including zero,
is retained under either flag. Means, the Threshold range, both headlines and
dollar amounts use the selected grid. Notes and metadata record the choice.

T is the final trading day; T−4 has `days_to_month_end == 5`. Estimate its
Calendar slope on those days and simulate its separate monthly reset schedule
for its trade size. Pre-2006 means dates before 2006-01-01; post-2006 starts
2007-01-01. Exclude the PPA transition year 2006 from both variants. Each uses
its own regression and size, while preserving the full-history weight path.
Short samples lacking either period fail clearly rather than invent estimates.

## Delta=0 identification and unresolved decision

The paper includes zero in the aggregate signal (equation 2), and describes
costs over 0–2.5%. It does not explain a special treatment of the daily-reset
slope when current return is also included. Table D.6 and footnotes 10 and 16
exclude zero from the **aggregate predictive signal** as a robustness check;
they do not prescribe its treatment in the average of individual cost estimates.
Footnote 17 changes active-day estimation, not the near-collinearity at zero.

For a daily-reset 60/40 portfolio, the exact drift is
`0.24 * ret / (1 + 0.6*r_es + 0.4*r_ty)`. Thus `thr_000` is close to
`0.24 * ret`, as footnote 13 anticipates. The real-panel design is full rank:
6,317 observations, seven columns, rank seven. Its condition number is
16,277 (110 after centering and scaling nonconstant columns). The largest
`abs(thr_000 - 0.24*ret)` is 0.0018976. The two predictors leave little
independent daily-reset variation. This is weak separation, not singularity
or a floating-point solver failure.

On the local processed panel, the daily-reset slope is −8.37734 (HC1 standard
error 7.36926). Omitting current return gives −0.38963 (SE 0.09850), but changes
the model. Splitting at 2006 gives −15.70496 before 2006 and −7.36068 after
2006 (excluding the transition year). Rounding only `thr_000` to four, five,
and six decimals gives −6.80283, −8.26869, and −8.36786. Adding macro controls
gives −7.75663, on a smaller complete-case sample of 5,043 observations.
These are diagnostics, not replacement estimates. Do not omit current return,
clip the slope, or silently substitute another estimate.

With corrected units, the zero-delta fixed-1%-trade cost is 2,111.09 bps/year.
Including it gives a 41.83650 bps headline; excluding it gives 1.22151 bps,
a **34.25×** change. The task requires a material decision above 2× when the
paper does not settle the choice. The outcome requests that decision; this PR
must remain draft until it is resolved.

## Real-panel audit against paper targets

Smoke run: local `daily_panel.parquet` and `signals_clean.parquet`, default
1997-09-10..2023-03-17 sample, no macro controls, 100 random schedules, seed 16.
The smoke run kept results in memory; no real exhibit was committed.
Positive values denote losses; negative values denote signed gains.

| Quantity | Corrected, include zero | Corrected, exclude zero | Paper |
|---|---:|---:|---:|
| Calendar | 3.33 bps | 3.33 bps | about 5 bps |
| Calendar T−4 | 9.85 bps | 9.85 bps | about 9 bps |
| Threshold range | −18.57 to 110.06 bps | −18.57 to 6.57 bps | 6–27 bps |
| Threshold mean | −1.11 bps | −5.55 bps | 15 bps |
| Fixed-1%-trade Threshold mean | 80.34 bps | −0.89 bps | 11 bps |
| Headline | 41.84 bps | 1.22 bps | 8 bps |
| Annual dollars on $20T | $83.67B | $2.44B | $16B |
| Random-date mean (100 draws) | 0.031 bps | unchanged | 0.6 bps |

The worked-example arithmetic is reproduced exactly at 4.68 bps. The real
T−4 estimate agrees roughly in size. Calendar is of the same order, but lower.
The corrected headline and Threshold distribution do **not** reproduce the
paper under either zero policy. Inclusion remains dominated by the weakly
separated daily-reset slope. Exclusion does not fix the other thresholds:
some slopes imply gains, unlike the paper's positive cost range. The local
panel uses return proxies rather than the authors' Bloomberg ES/TY series;
the resulting coefficients and simulated paths differ. Unit correction cannot
resolve those differences. The 100-draw random mean is a smoke diagnostic,
not a replication of the paper's 10,000-draw estimate. Its small value does
not establish the paper's 0.6 bps magnitude or its disputed sign.

## Random schedules and tracking error

Seed NumPy's default generator with 16 (`--seed` changes it). Draw one day
uniformly within every observed sample month, independently across months and
simulations. Include week4 and partial endpoint months. No replacement issue
arises because months have disjoint dates. Use 10,000 draws by default;
`--n-sims` changes this count. `simulate_dates` carries returns through the full
history, starting at 60/40, with no random resets before the sample begins.
The Calendar comparison retains its full-history monthly resets.

On each schedule, estimate a regression on selected dates. Its predictor is
that portfolio's pre-trade equity deviation. Control for aggregate Threshold,
Calendar, week4, Calendar × week4, Momentum and Ret (and optional macro controls).
Keeping the institutional Calendar terms controls for coincident market pressure;
the random investor's own deviation replaces none of these institutional terms.
The size is the mean absolute executed trade on selected dates, and frequency
is 12. Report the distribution mean, median and empirical 2.5/97.5 percentiles.
These percentiles describe schedules, not a confidence interval for the mean.

Tracking error is the sample standard deviation of daily random-minus-Calendar
portfolio returns, times sqrt(252), times 10,000. Report the average across draws.
The CSV for Figure D.5 contains one row per simulation: `simulation` (1-based),
`cost_bps_year`, and `tracking_error_bps_year`. The PDF histogram uses this data.

## Dollar scaling and D27 sources

Use `headline_bps / 10000 * assets`, and divide by `(2/3) * 127,000,000`
for participating-household costs. The paper's $20T base (`--assets`) is a
rounded estimate of public equity and debt. The Fed $37.8T alternative
(`--fed-assets`) uses all retirement assets and is explicitly a broader base.
These are dated constants transcribed from the paper, not newly fetched totals.
At a hypothetical headline of 8 bps, $20T gives $16B and $188.98 per participating
household. Both dollar bases and both per-household costs appear in `costs.csv`.

D27 sources (paper pp. 21–23 and footnotes 19, 21):

- [Federal Reserve Financial Accounts](https://www.federalreserve.gov/releases/z1/):
  year-end 2022 retirement assets, $37.8T, including public/private defined benefit
  and contribution plans and IRAs, excluding Social Security.
- [CRS Report R47699](https://crsreports.congress.gov/product/pdf/R/R47699):
  2023 allocation review. The paper attributes $7.2T public-plan equity/debt,
  $6.8T private DC, $2.3T private DB, and $4.8T IRAs to this review.
  Their sum is $21.1T; use the paper's rounded $20T headline base, not a revised sum.
- [Survey of Consumer Finances](https://www.federalreserve.gov/econres/scfindex.htm):
  paper's approximately two-thirds household participation in retirement assets.
- [Census household tables](https://www.census.gov/data/tables/time-series/demo/families/households.html):
  paper's approximately 127M U.S. households, 2022. Use this stated rounded number.
- [ICI, 2025 Q2 retirement report](https://www.ici.org/statistical-report/ret_25_q2):
  $45.8T as of 2025-06-30. This supports the paper's growth discussion only;
  it does not replace the year-end 2022 Fed alternative.

## Utility and demo boundaries

For buy-and-hold, Threshold delta=2.5%, and monthly Calendar, compute each
portfolio's daily simple return from **the previous close's post-trade weight**:
`w * r_es + (1-w) * r_ty`. Using today's pre-trade weight would look ahead.
The initial weight is 0.6. Buy-and-hold never resets. Utility is annualized as
`252 * (mean(return) - 0.5 * 3 * var(return, ddof=1))`, converted to bps.
Report all three levels and Threshold-minus-buy-and-hold and
Calendar-minus-buy-and-hold differences. These are gross excess-return utilities;
no execution-cost model, cash return, or separately estimated cost is subtracted.

Demo loads `rebal.io.load_panel(demo=True)` and builds actual signals with
`rebal.signals.build`, like the descriptive exhibit module. The scaffold's
planted signal placeholders do not correspond to executed Threshold trades.
Using them for conditional costs can leave high-delta regressions empty.
Tests instead plant next-day effects on actual simulated signals and use the
same estimation API. Real runs read the processed signal contract. No real panel
or cluster is required for demo checks. TASK-022 also audits the existing real
panel; TASK-030 owns committed real exhibit outputs.
