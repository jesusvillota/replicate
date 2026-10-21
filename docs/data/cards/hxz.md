# Source card: Hou–Xue–Zhang q5 factors

## Source and URL or WRDS table

Global-q, the authors' public factor library:
<https://global-q.org/factors.html>.
Newest daily q5 CSV linked when downloaded:
<https://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2025.csv>.

Access: `uv run python3 -m rebal.fetch.hxz`, using
`rebal.fetch.common.download`. The fetcher reads the official factors page
each time and chooses the daily q5 link with the largest year suffix.
It excludes monthly/weekly files, benchmark portfolios and external hosts.
`data/public/hxz/source.json` records the chosen URL, UTC download time,
raw SHA-256 checksum, row count, dates and units. No login or mirror was needed.

## Downloaded (date)

2026-10-21. The newest linked daily file ends in 2025.

## License class

Public, redistributable under the goal's public-data classification.
Store the unchanged source as `data/public/hxz/q5_factors_daily.raw.csv`
and the tidy output as `data/public/hxz/q5_factors_daily.csv`.
Credit Hou, Xue and Zhang and Global-q when using these data.
The CSV does not contain a separate software license.

## Series, with units

| Published column | Meaning | Raw units | Output units |
|---|---|---|---|
| R_F | Risk-free return | percent per day | percent per day |
| R_MKT | MKT, market excess return | percent per day | percent per day |
| R_ME | ME, size factor | percent per day | percent per day |
| R_IA | IA, investment factor | percent per day | percent per day |
| R_ROE | ROE, profitability factor | percent per day | percent per day |
| R_EG | EG, expected growth factor | percent per day | percent per day |

## Transforms

Keep the source CSV bytes unchanged. Parse `date` as ISO `YYYY-MM-DD`,
sort dates, and retain the published column names and full history.
No scaling, interpolation, joining, or factor construction occurs.
The published risk-free series is retained alongside the five factors.
Validate the exact schema, numeric values, unique dates and sample endpoints.
`rebal.fetch.common.summarize` checks both raw and tidy files.
TASK-012 owns unit conversion and mapping to the panel under
[`docs/contracts/daily_panel.md`](../../contracts/daily_panel.md).

## Coverage

Daily, 1967-01-03 through 2025-12-31, 14848 rows in each CSV.
All six series cover 1997-09-10 through 2023-03-17, with both endpoints observed.
Stored-file tests found no missing values or duplicate dates.
Nontrading dates stay absent; no artificial calendar rows are added.

## Known problems

This is the current public q5 vintage, not the paper's historical vintage.
New releases can revise returns. The fetcher follows the newest linked year,
and fails if the page no longer lists a daily q5 CSV.
The first request with default HTTP headers returned HTTP 400 during this
session. The project's downloader headers succeeded for the page and CSV.
Keep the q5 library's risk-free return separate from French RF.

## Paper datasets served (D-numbers)

D24 (HXZ q factors, with the expected growth factor also retained).
