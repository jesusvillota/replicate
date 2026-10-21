# CRSP CIZ: ETF returns, index returns, and daily stock dispersion

Source: licensed WRDS CRSP CIZ daily stock data, supplied by tape-kit. Reference:
https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/

Extracted on 2026-10-21. Source vintage: 2026-08-18, observations through
2026-07-31. The promoted archive is `crsp-research-v1`, published 2026-09-27
from tape-kit's `annual-v2` release. This task did not download from WRDS.
The source publication metadata SHA-256 is
`c3eab8f182f4580554145d8d1cb9973285df958ec758dd04becf2622b08ab7ac`.

License class: licensed, non-redistributable. Parquets are never committed.
Cluster inputs are read-only under
`/mnt/slurm-beegfs/Users/j-vill36/tape-kit-data/crsp/`:
`data/daily/YYYY.parquet`, `data/benchmarks/YYYY.parquet`, and
`security_history/security_info.parquet`.

Cluster outputs: `/mnt/slurm-beegfs/Users/j-vill36/replicate-data/licensed/crsp/`.
MacBook outputs: `${REPLICATE_DATA_DIR:-$HOME/data/replicate}/licensed/crsp/`.
`cluster-kit sync cp` copied each final file and `extraction.json`.
The three MacBook SHA-256 values match the cluster values exactly.

## Series and units

- `etf_daily.parquet`: `date`, `ticker`, `permno`, `ret`, `retx`, `prc`, `vol`.
  Returns are decimal simple returns. `ret` includes distributions; `retx`
  excludes ordinary dividends. Prices are dollars per share. Volume is raw
  shares. Prices and volume are not split-adjusted historical levels.
- `benchmarks_daily.parquet`: `date`, `vwretd`, `vwretx`, `ewretd`, `ewretx`,
  `sprtrn`. Decimal simple returns. The first four are value/equal-weighted
  CRSP market returns with/without dividends. `sprtrn` is an S&P 500 return.
- `dispersion_daily.parquet`: `date`, `ivol`, `ivol_w`, `n_stocks`.
  Dispersion is sample SD in decimal return units. `ivol_w` winsorizes each
  daily cross-section at its 1st and 99th percentiles. It is not value weighted.

## ETF identity and observed coverage

PERMNO is CRSP's stable security identifier. Only historical FUND/ETF records
qualify. Observations join on PERMNO and inclusive descriptor dates.

| Ticker | PERMNO | Rows | First date | Last date |
| --- | --- | ---: | --- | --- |
| ACWX | 92586 | 4615 | 2008-03-28 | 2026-07-31 |
| AGG | 89848 | 5747 | 2003-09-26 | 2026-07-31 |
| EFA | 89129 | 6274 | 2001-08-17 | 2026-07-31 |
| IEF | 89469 | 6042 | 2002-07-26 | 2026-07-31 |
| IVV | 88215 | 6588 | 2000-05-19 | 2026-07-31 |
| IWB | 88221 | 6588 | 2000-05-19 | 2026-07-31 |
| IWD | 88219 | 6583 | 2000-05-26 | 2026-07-31 |
| IWF | 88220 | 6583 | 2000-05-26 | 2026-07-31 |
| IWM | 88222 | 6583 | 2000-05-26 | 2026-07-31 |
| SPY | 84398 | 8433 | 1993-01-29 | 2026-07-31 |
| TLT | 89468 | 6042 | 2002-07-26 | 2026-07-31 |
| VEU | 91886 | 4881 | 2007-03-08 | 2026-07-31 |

Dispersion: 7,267 dates, 1997-09-10 through 2026-07-31.
Daily `n_stocks`: minimum 3,562, maximum 7,465 across the full output.
Benchmarks: 16,755 dates, 1960-01-04 through 2026-07-31.

## Transforms and limitations

See [ivol.md](../../methods/ivol.md) for the exact historical CIZ share-code
10/11 filters, return duration rules, missing values, and SD definition.
No price screen is used. Missing ETF returns remain null. No second delisting
return is added. Annual parts permit restart with `--skip-existing`.

SPY previously named stocks with PERMNOs 33910 and 60716. AGG previously named
PERMNO 17232. Those records are excluded from these ETF outputs. Ambiguous ETF
identities or overlapping historical intervals fail rather than mix securities.
Coverage starts at the first CRSP observation, which need not be the fund's
legal inception date. This vintage can revise earlier observations.

These ETFs are cash-fund proxies for the paper's futures or index series.
They have different inception dates and do not supply earlier index history.
TASK-011 selects proxies; TASK-012 integrates the
[daily panel contract](../../contracts/daily_panel.md).

## Run evidence

Implementation: `99764c1`. SLURM jobs `25494` (10 seconds) and `25495`
(9 seconds) both show `COMPLETED`. Final extraction metadata names `25495`.
Both used `cpu_shared`, 4 CPUs, 16 GB, and a one-hour limit. SLURM reported
MaxRSS as 0 for batch/extern steps, so no useful peak-memory value is available.
An accidental duplicate submission overlapped the first run for four seconds;
the task outcome records this breach of the one-job budget.

## File integrity

| File | SHA-256 (cluster and MacBook) |
| --- | --- |
| `etf_daily.parquet` | `5e7db3be218b2da873f0d4879a88fb85187ac9db9c284b01208bc1faf3fc3c17` |
| `dispersion_daily.parquet` | `5283f121f81241c047fc74d8c4cfe0017ca05d46e9d4547adc598bb614432cd1` |
| `benchmarks_daily.parquet` | `b51e748ede9b8e94b72266e853bab224473c637da68b242440e6bc70acdcb481` |
