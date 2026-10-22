# Daily panel contract

File: `$REPLICATE_DATA_DIR/processed/daily_panel.parquet`.
TASK-012 is the only writer. The default external root is `~/data/replicate`.
Each row is one trading day. `date` is a regular column, sorted and unique.
It has no time zone or time-of-day component. The pandas index is not part of the contract.
All returns are simple decimal daily returns: 0.01 means 1% in one day.
Core returns must exist on every retained date. Optional sources can have missing observations.

| Column | Dtype | Units | May be NaN | Dataset |
|---|---|---|---|---|
| date | datetime64[ns] | naive calendar date at midnight | no | D3 |
| r_es | float64 | simple decimal daily excess return | no | D1 |
| r_ty | float64 | simple decimal daily excess return | no | D2 |
| rf | float64 | simple decimal daily cash return | yes | D16 / D24 (French RF) |
| rf_3m | float64 | simple decimal daily cash return | yes | D7 |
| vix | float64 | index level / 100 | yes | D8 |
| move | float64 | index level / 100 | yes | D9 |
| epu | float64 | published index level | yes | D10 |
| ads | float64 | published index level | yes | D11 |
| sentiment | float64 | published index level | yes | D12 |
| ra_bex | float64 | published index level | yes | D13 |
| unc_bex | float64 | published index level | yes | D13 |
| ara | float64 | published index level | yes | D15 |
| liquidity | float64 | selected source's published units: HPW `Noise_bp` in basis points when full-study history is available; otherwise OFR `Funding` in index points; see [methods](../methods/panel.md#cash-controls-and-units) and `panel.metadata.json` for the selected source | yes | D26 |
| ivol | float64 | cross-sectional SD of simple decimal daily stock returns | yes | D25 |
| mkt_rf | float64 | simple decimal daily factor return | yes | D24 |
| smb | float64 | simple decimal daily factor return | yes | D24 |
| hml | float64 | simple decimal daily factor return | yes | D24 |
| rmw | float64 | simple decimal daily factor return | yes | D24 |
| cma | float64 | simple decimal daily factor return | yes | D24 |
| mom | float64 | simple decimal daily factor return | yes | D24 |
| q_mkt | float64 | simple decimal daily factor return | yes | D24 |
| q_me | float64 | simple decimal daily factor return | yes | D24 |
| q_ia | float64 | simple decimal daily factor return | yes | D24 |
| q_roe | float64 | simple decimal daily factor return | yes | D24 |
| q_eg | float64 | simple decimal daily factor return | yes | D24 |
| r_sp500tr | float64 | simple decimal daily total return | yes | D4 |
| r_agg | float64 | simple decimal daily total return | yes | D5 |
| r_acwxus | float64 | simple decimal daily total return | yes | D6 |
| r_r1k | float64 | simple decimal daily total return | yes | D18 |
| r_r2k | float64 | simple decimal daily total return | yes | D18 |
| r_r1kv | float64 | simple decimal daily total return | yes | D18 |
| r_r1kg | float64 | simple decimal daily total return | yes | D18 |
| r_mkt_french | float64 | simple decimal daily total return | yes | D16 |
| r_10y_gsw | float64 | simple decimal daily total return | yes | D17 |

`r_mkt_french = mkt_rf + rf`. Futures proxies in `r_es` and `r_ty` are excess of cash.
The chosen D1/D2 proxy and each source transform are documented by their later tasks.

Returns are never forward-filled. Controls may be forward-filled for at most 5 trading days.
Longer gaps remain NaN. Factors and index returns also remain NaN when missing.
The 5-day limit is a maximum, not a requirement to fill every control.

The demo uses weekdays, without an exchange holiday calendar. It supplies all columns without missing values.
It does not claim real source coverage or exchange dates.
