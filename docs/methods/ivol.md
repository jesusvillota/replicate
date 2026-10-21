# Daily stock return dispersion

`ivol` is the sample standard deviation (`stddev_samp`, denominator n−1) of
CRSP CIZ daily total returns. It measures differences between stock returns
on one date. It is not a firm's residual volatility. Units are decimal returns.

The sample starts on 1997-09-10, the paper's required start, and ends at the
latest source date. ETFs start at their first CRSP observation. Benchmarks
start in 1960. No stock-level CRSP calculation runs on the MacBook.

The historical daily descriptors must satisfy all these conditions:

| Field | Values | Reason |
| --- | --- | --- |
| `sharetype` | `NS` | Ordinary shares without a special designation |
| `securitytype` | `EQTY` | Equity |
| `securitysubtype` | `COM` | Common shares |
| `usincflg` | `Y` | U.S. incorporation |
| `issuertype` | `ACOR`, `CORP` | Both legacy share codes 10 and 11 |
| `primaryexch` | `N`, `A`, `Q` | NYSE, NYSE American/AMEX, Nasdaq |

This is tape-kit's documented five-field CIZ equivalent of `SHRCD IN (10,11)`,
plus the three exchanges. It excludes foreign incorporation, ADRs, REITs,
funds, and other security types. Distinct share classes remain separate
PERMNOs. There is no price, volume, size, current-active, regular-way, or
active-trading filter. This is a cross-section, not a portfolio holding rule.

Returns must be finite, at least −1, and have `dlyretdurflg` in
`D1`, `D2`, `D3`, `D4`, `DU`. These flags cover one trading period, including
weekends and holidays. Multi-period returns are excluded from daily dispersion.
Null returns are excluded; they are never replaced with zero. Valid total-loss
returns are retained. No external delisting return is added to `dlyret`.
Terminal observations with qualifying descriptors and a one-period return
remain eligible. A terminal row with missing or changed descriptors is not
assigned an earlier classification. No delisting loss is imputed.

`n_stocks` counts qualifying securities with usable returns on that date.
`ivol_w` uses the same sample. For each date, DuckDB computes the linearly
interpolated 1st and 99th percentiles (`quantile_cont`). Returns below or above
these bounds are set to the respective bound before computing sample SD.
The raw `ivol` remains unchanged. A date needs at least two usable returns.

The extractor scans one calendar year at a time. Each year has dispersion at
`parts/YYYY.parquet` and ETF observations at `parts/etf/YYYY.parquet`.
Writes are atomic. `--skip-existing` validates both parts before skipping.
A partial or invalid pair is recomputed. All selected annual parts must exist
before merge. Reuse parts only with unchanged inputs and method; rerun without
`--skip-existing` after a source or method change.

ETF resolution uses only `securitytype='FUND'`, `securitysubtype='ETF'` records
in `security_history/security_info.parquet`. Each requested ticker must resolve
to one PERMNO. Overlapping descriptor intervals fail. Daily observations join
on PERMNO and inclusive `secinfostartdt`..`secinfoenddt`, so prior stocks with
reused tickers cannot enter ETF series. Missing ETF returns remain null.
`retx` excludes ordinary dividends; prices and volume retain source units.

References read locally: tape-kit `docs/reference/crsp-daily-stock-file.md`,
`crsp-processing-policy.md`, and `crsp-extraction.md`. The daily panel contract
is [daily_panel.md](../contracts/daily_panel.md); TASK-012 owns panel integration.
