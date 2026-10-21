# Signals contract

TASK-013 implements `rebal.signals.build(r_eq, r_bd, target=0.60, timing="clean", deltas=...)`.
Inputs are aligned daily return series with a sorted, unique, naive date index.
The output has a regular `date` column and no extra index column.
File: `$REPLICATE_DATA_DIR/processed/signals_<timing>.parquet`.
Read [paper-notes §3.2, §3.4 and §3.6](../../goals/hmm-rebalancing/paper-notes.md#3-methods) for definitions.

| Column | Dtype | Definition and units |
|---|---|---|
| date | datetime64[ns] | naive midnight date; sorted and unique |
| ret | float64 | r_eq minus r_bd; simple decimal daily return |
| thr_000 | float64 | Threshold deviation for delta = 0.0%; decimal portfolio weight |
| thr_001 | float64 | Threshold deviation for delta = 0.1%; decimal portfolio weight |
| thr_002 | float64 | Threshold deviation for delta = 0.2%; decimal portfolio weight |
| thr_003 | float64 | Threshold deviation for delta = 0.3%; decimal portfolio weight |
| thr_004 | float64 | Threshold deviation for delta = 0.4%; decimal portfolio weight |
| thr_005 | float64 | Threshold deviation for delta = 0.5%; decimal portfolio weight |
| thr_006 | float64 | Threshold deviation for delta = 0.6%; decimal portfolio weight |
| thr_007 | float64 | Threshold deviation for delta = 0.7%; decimal portfolio weight |
| thr_008 | float64 | Threshold deviation for delta = 0.8%; decimal portfolio weight |
| thr_009 | float64 | Threshold deviation for delta = 0.9%; decimal portfolio weight |
| thr_010 | float64 | Threshold deviation for delta = 1.0%; decimal portfolio weight |
| thr_011 | float64 | Threshold deviation for delta = 1.1%; decimal portfolio weight |
| thr_012 | float64 | Threshold deviation for delta = 1.2%; decimal portfolio weight |
| thr_013 | float64 | Threshold deviation for delta = 1.3%; decimal portfolio weight |
| thr_014 | float64 | Threshold deviation for delta = 1.4%; decimal portfolio weight |
| thr_015 | float64 | Threshold deviation for delta = 1.5%; decimal portfolio weight |
| thr_016 | float64 | Threshold deviation for delta = 1.6%; decimal portfolio weight |
| thr_017 | float64 | Threshold deviation for delta = 1.7%; decimal portfolio weight |
| thr_018 | float64 | Threshold deviation for delta = 1.8%; decimal portfolio weight |
| thr_019 | float64 | Threshold deviation for delta = 1.9%; decimal portfolio weight |
| thr_020 | float64 | Threshold deviation for delta = 2.0%; decimal portfolio weight |
| thr_021 | float64 | Threshold deviation for delta = 2.1%; decimal portfolio weight |
| thr_022 | float64 | Threshold deviation for delta = 2.2%; decimal portfolio weight |
| thr_023 | float64 | Threshold deviation for delta = 2.3%; decimal portfolio weight |
| thr_024 | float64 | Threshold deviation for delta = 2.4%; decimal portfolio weight |
| thr_025 | float64 | Threshold deviation for delta = 2.5%; decimal portfolio weight |
| thr_026 | float64 | Threshold deviation for delta = 2.6%; decimal portfolio weight |
| thr_027 | float64 | Threshold deviation for delta = 2.7%; decimal portfolio weight |
| thr_028 | float64 | Threshold deviation for delta = 2.8%; decimal portfolio weight |
| thr_029 | float64 | Threshold deviation for delta = 2.9%; decimal portfolio weight |
| thr_030 | float64 | Threshold deviation for delta = 3.0%; decimal portfolio weight |
| thr_031 | float64 | Threshold deviation for delta = 3.1%; decimal portfolio weight |
| thr_032 | float64 | Threshold deviation for delta = 3.2%; decimal portfolio weight |
| thr_033 | float64 | Threshold deviation for delta = 3.3%; decimal portfolio weight |
| thr_034 | float64 | Threshold deviation for delta = 3.4%; decimal portfolio weight |
| thr_035 | float64 | Threshold deviation for delta = 3.5%; decimal portfolio weight |
| thr_036 | float64 | Threshold deviation for delta = 3.6%; decimal portfolio weight |
| thr_037 | float64 | Threshold deviation for delta = 3.7%; decimal portfolio weight |
| thr_038 | float64 | Threshold deviation for delta = 3.8%; decimal portfolio weight |
| thr_039 | float64 | Threshold deviation for delta = 3.9%; decimal portfolio weight |
| thr_040 | float64 | Threshold deviation for delta = 4.0%; decimal portfolio weight |
| threshold | float64 | mean of thr_000 through thr_025; decimal portfolio weight |
| calendar | float64 | calendar deviation; decimal portfolio weight |
| week1 | int64 | 0/1 trading-day bucket |
| week2 | int64 | 0/1 trading-day bucket |
| week3 | int64 | 0/1 trading-day bucket |
| week4 | int64 | 0/1 trading-day bucket |
| days_to_month_end | int64 | inclusive trading-day count; 1 on the last trading day |
| mom_fast | float64 | mean of trailing-return signs, between -1 and 1 |
| mom_medium | float64 | mean of trailing-return signs, between -1 and 1 |
| mom_slow | float64 | mean of trailing-return signs, between -1 and 1 |
| momentum | float64 | mean of trailing-return signs, between -1 and 1 |
| rev_st | float64 | simple decimal cumulative return |
| rev_lt | float64 | simple decimal cumulative return |
| eom_rev | float64 | simple decimal cumulative return |
| threshold_t86 | float64 | threshold deviation for target 86%; decimal portfolio weight |
| calendar_t86 | float64 | calendar deviation for target 86%; decimal portfolio weight |
| threshold_t50 | float64 | threshold deviation for target 50%; decimal portfolio weight |
| calendar_t50 | float64 | calendar deviation for target 50%; decimal portfolio weight |
| threshold_t70 | float64 | threshold deviation for target 70%; decimal portfolio weight |
| calendar_t70 | float64 | calendar deviation for target 70%; decimal portfolio weight |

The threshold grid runs from 0.0% to 4.0%, in 0.1% steps.
The suffix is delta in tenths of a percent: `thr_025` means 2.5%, or 0.025.
The default `deltas` is this full grid. The aggregate uses the first 26 columns, including both endpoints.

`week4` covers the last 5 trading days of each month.
`week3` covers trading days 6–10 before month-end, counting the last day as 1.
`week2` covers days 11–15. `week1` covers the rest.
Each row belongs to exactly one week. Count on the full trading calendar before selecting a regression sample.

Fast momentum averages signs over lookbacks 1–10; medium uses 11–20.
Slow uses 21, 42, 63, 126 and 252 days. `momentum` averages medium and slow.
`rev_st` uses the last 5 days. `rev_lt` uses a 1260-day lookback, skipping the last year.
`eom_rev` uses S&P 500 returns from the fourth Friday close to the month-end close.
TASK-013 documents timing and warm-up choices. Required return history may produce NaN during warm-up;
dates, week flags and day counts must never be missing.

The signal at date t predicts `ret` at date t+1. Do not shift regressors forward.
In real data `ret = r_eq - r_bd`. Demo `ret` replaces that spread with planted next-day effects.
Demo auxiliary columns are synthetic placeholders. They do not implement portfolio simulation or momentum rules.
Demo dates at a truncated endpoint treat the final supplied date as month-end.

## Simulation API

Each function returns a DataFrame with the same date index as the inputs and exactly these columns:
`w_pre`, `w_post`, `trade`. Weights are decimal equity shares.
`trade = w_post - w_pre`: positive means an equity purchase; negative means a sale.

- `simulate_threshold(r_eq, r_bd, delta, target, timing)`
- `simulate_calendar(r_eq, r_bd, target, timing)`
- `simulate_dates(r_eq, r_bd, dates, target)`

`w_pre` is the equity weight after that day's returns and before a trade.
`w_post` is the weight after the trade. The simulation starts at the target.
`dates` selects rebalance dates from the input index.
See paper-notes §3.2 for drift and reset rules, and §3.6 for target variants.
