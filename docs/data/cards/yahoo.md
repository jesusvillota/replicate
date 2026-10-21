# Source card: Yahoo Finance

## Source and URL or WRDS table

Yahoo Finance daily chart service, via `yfinance` 1.7.0:
`https://query2.finance.yahoo.com/v8/finance/chart/<ticker>`.
Human pages: `https://finance.yahoo.com/quote/<ticker>/history/`.
Run `uv run python3 -m rebal.fetch.yahoo` for full histories of all ten tickers.

## Downloaded (date)

2026-10-21. Each ticker's metadata records its UTC download time and raw SHA-256.

## License class

Licensed or terms-restricted. [Yahoo terms](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html).
Files stay in `$REPLICATE_DATA_DIR/licensed/yahoo/`, default
`~/data/replicate/licensed/yahoo/`. No downloaded data enters git.
Each ticker has `<ticker>.json` (original daily chart response bytes),
`<ticker>.csv` (tidy history), and `<ticker>.metadata.json` (lineage).

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `ES=F` E-mini S&P 500 futures | Quoted index points | Same |
| `ZN=F` 10-year T-note futures | Quoted price per 100 face value | Same |
| `^GSPC` S&P 500 price index | Index points | Same |
| `^SP500TR` S&P 500 total return index | Total return index points | Same |
| `^MOVE` ICE BofA MOVE | Published index points | Same |
| `^VIX` CBOE VIX | Published index points | Same |
| `^RUI`, `^RUT`, `^RLV`, `^RLG` Russell price indices | Index points | Same |

CSV columns are `date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`,
`Dividends`, and `Stock Splits`. Volume is the provider's count; action columns
keep the provider's units. Zero volume for an index does not measure trading.

## Transforms

`history(period="max", interval="1d", auto_adjust=False, back_adjust=False,
repair=False, rounding=False)`. Both Close and Adj Close remain separate.
Dates use each exchange's local calendar date; timezone removal does not shift dates.
The original chart JSON preserves the published values and metadata before parsing.
No currency conversion, return calculation, interpolation, filling, or roll correction.
`yfinance` defaults omit sessions with no quote; no synthetic calendar rows are added.
The fetcher rejects empty histories, duplicate/unsorted dates, missing prices,
or missing required sample boundaries. Each CSV passes `common.summarize`.

## Coverage

`^MOVE` coverage: **2002-11-12 to 2026-10-21**, 5,920 daily observations.
It **does not cover 1997-09-10**. The initial sample gap remains unfilled.

| Ticker | First date | Last date | Rows | Longest gap, calendar days |
|---|---|---|---:|---:|
| `ES=F` | 2000-09-18 | 2026-10-21 | 6,588 | 6 |
| `ZN=F` | 2000-09-21 | 2026-10-21 | 6,550 | 12 |
| `^GSPC` | 1927-12-30 | 2026-10-21 | 24,819 | 12 |
| `^SP500TR` | 1988-01-04 | 2026-10-21 | 9,774 | 7 |
| `^MOVE` | 2002-11-12 | 2026-10-21 | 5,920 | 10 |
| `^VIX` | 1990-01-02 | 2026-10-21 | 9,271 | 7 |
| `^RUI` | 1992-12-10 | 2026-10-21 | 8,523 | 7 |
| `^RUT` | 1987-09-10 | 2026-10-21 | 9,853 | 7 |
| `^RLV` | 2002-09-30 | 2026-10-21 | 6,053 | 5 |
| `^RLG` | 2026-10-21 | 2026-10-21 | 1 | Not applicable |

`^SP500TR` includes both 1997-09-10 and 2023-03-17. Both futures start before 2001.
Gaps include weekends and market closures; this table does not classify exchange holidays.
There are no duplicate dates or missing Close/Adj Close values in these files.

## Known problems

`ES=F` and `ZN=F` are front-month series **without roll adjustment**. Returns
across a roll date are wrong. Their first dates are 2000-09-18 and 2000-09-21.
They cannot cover the paper's first three years. TASK-011 handles rolls and proxy comparison.

`^RLG` currently returns only one observation, even with a full-history request.
It cannot check Russell Growth returns in the paper's sample. `^RLV` also starts late.
These are source limitations, not filled histories. TASK-009 supplies the ETF proxies.
TASK-012 must account for MOVE's missing early years when building the daily panel.
Yahoo may revise history or rate-limit requests. The fetcher retries rate and transport
failures with exponential backoff. The newest daily quote can still change intraday.
An `OK` line confirms the downloaded file's validity, not complete paper-sample coverage.

## Paper datasets served (D-numbers)

D1, D2, D4, D9, D18; `^GSPC` and `^VIX` provide comparison series.
