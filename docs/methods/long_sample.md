# Table 4: long-sample returns and regressions

`rebal.exhibits.long_sample` owns `table_4`. It follows the
[exhibits contract](../contracts/exhibits.md) and
[signals contract](../contracts/signals.md). It does not change the main panel.

## Equity and cash

French daily `Mkt-RF` and `RF` enter in percent. The equity total return is
`r_mkt_french = (Mkt-RF + RF) / 100`. Thus, the answer to paper-notes §5.13's
French-return question is yes. This is the French broad market, rather than
the S&P 500 futures series used in the main sample.

Subtract the same French daily `RF / 100` from both asset total returns.
Build signals from this excess-return pair, as the main panel does.
The common cash leg cancels in the dependent spread:
`ret = r_es - r_ty = equity_total - bond_total`.

## Yield-to-return conversion

Reuse `rebal.proxies.ty_zero_10` and `zero_coupon_return`, as described in
[proxies.md](proxies.md). A zero-coupon bond makes one payment at maturity.
Start each holding interval with a new 10-year zero-coupon bond. Price that
same bond after it ages, then reset its maturity for the next interval.
With decimal continuous yields, the simple total return is:

```text
delta = actual calendar days between equity sessions / 365.25
return = exp(10 * y_previous(10) - (10 - delta) * y_today(10 - delta)) - 1
```

GSW `SVENY09` and `SVENY10` enter in percent per year. Interpolate the aged
bond's yield as `SVENY10 - delta * (SVENY10 - SVENY09)`, then divide by 100.
This includes carry, aging and yield changes. It is a zero-coupon holding
return, not an observed Treasury note or futures return.

## Before 1971 and the source seam

Default `--pre-1971 dgs10` uses FRED `DGS10` before 1971-08-16. Apply the
same `zero_coupon_return` function with a flat local curve. Treat `DGS10 / 100`
as a continuous zero yield for this approximation.

DGS10 is a constant-maturity par yield. A par yield is the coupon rate that
prices a coupon-paying bond at face value. A zero yield discounts one payment.
They differ because coupons occur before maturity. DGS10 also uses a different
yield convention. Treating it as a continuous zero yield is a documented proxy;
one maturity cannot identify the full discount curve. No bootstrapped curve
is available for this early sample.

Convert each source to returns separately. Do not join yield levels across
the seam: their level difference would create a false bond price change.
GSW's first 10-year quote is 1971-08-16. Its first holding return is
1971-08-17. Omit 1971-08-16 rather than price across two sources.
`--pre-1971 omit` uses GSW only and therefore starts its return history on
1971-08-17. This flag exposes the early-source choice without changing inputs.

## Dates, missing values and warm-up

Align yield quotes on French equity sessions before calculating returns.
Do not carry missing yield quotes forward. A missing quote removes its return
and the next interval's return. Retain common finite asset returns using
`rebal.panel.trading_calendar`, including its September 2001 closure rule.
Signals use this retained calendar, as in the main panel. Missing sessions
therefore affect the trading-day counts and momentum lookbacks.

The paper starts on 1961-06-16. These inputs cannot support that start.
DGS10 begins on 1962-01-02; the first usable holding return is **1962-01-03**.
Build signals on the whole available history before choosing regression dates.
Do not replace the missing early bond history with zero returns.

The 252-return momentum warm-up first completes on **1963-01-10** in the
stored real inputs. The first predicted outcome is **1963-01-11**. The real
default sample is therefore shorter than the paper's sample. Metadata records
the first return, first momentum date and actual outcome dates for each column.

## Regression and control set

Use equation (4), with the terms printed in the paper's Table 4 (PDF p.36):
an intercept, `threshold`, `calendar`, `week4`, `calendar:week4`, `momentum`
and `ret`. The controls are **momentum and the current spread return**.
Omit `vix`, `move`, `epu`, `ads` and `sentiment` from every column: these
level controls do not cover the full long sample. Do not add them only to
the late column. Table 4 itself does not tabulate these additional controls.

Default momentum averages the 11–20 day sign family and the
21/42/63/126/252 day sign family with equal family weights.
`--momentum all15` gives each of these 15 signs equal weight instead.
Use the standard 60/40 target, the full signal grid and `--timing clean`.
`--timing literal` exposes the existing delayed-reset alternative.

The shared `predictive` estimator regresses `ret[t+1]` on terms at `t`.
Use HC1 standard errors by default. `--se hc0|hc1|hac` and `--hac-lags`
expose covariance alternatives. The columns select these inclusive windows:

| Column | Window | Actual outcome start | N, stored real inputs |
|---|---|---|---|
| 1 | 1961-06-16 through 2023-03-17 | 1963-01-11 | 14,796 |
| 2 | 1961-06-16 through 1997-09-09 | 1963-01-11 | 8,478 |
| 3 | 1997-09-10 through 2023-03-17 | 1997-09-11 | 6,317 |

Both predictor and outcome must fall inside the selected window. Thus column
3's first predictor is 1997-09-10 and its first outcome is 1997-09-11.
The cross-split pair belongs only to column 1, so its N exceeds the sum of
columns 2 and 3 by one. Signals and momentum never restart at the split.
The default endpoint is 2023-03-17; `--end latest` uses all available history.
Month-end flags are built before the endpoint cut, including the partial final
month's later sessions. Actual outcome dates populate the CSV contract fields.

## Demo and lineage

The local demo uses `rebal.demo.make_panel` from 1960 onward and the real
`rebal.signals.build` engine. It replaces only the response with next-day
effects: zero before the split, Threshold −0.4 and Calendar × week4 −0.3 after
the split, plus independent noise. Tests also use zero effects throughout.
Demo weekdays are synthetic; they are not an exchange holiday calendar.

`table_4.metadata.json` records parameters, input SHA-256 hashes, actual dates,
sample counts and omitted controls. Demo files stay in `output/demo/`.
TASK-024's real run is a smoke check only. Its numbers appear in the outcome;
TASK-030 owns committed real outputs and the final comparison.
