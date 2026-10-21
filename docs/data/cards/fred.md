# Source card: FRED rates and VIX

## Source and URL or WRDS table

Federal Reserve Bank of St. Louis, FRED. No API key is needed.
Live URL: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>`.
Run `uv run python3 -m rebal.fetch.fred`.

On this download date, FRED returned HTTP 200 with a maintenance HTML page.
The fetcher validates the CSV schema before accepting it. If the live request
fails or returns invalid data, it uses these recorded Wayback snapshots:

| Series | Exact archived download |
|---|---|
| DTB3 | https://web.archive.org/web/20260708052657id_/https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3 |
| DGS10 | https://web.archive.org/web/20261014114807id_/https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10 |
| VIXCLS | https://web.archive.org/web/20261012093245id_/https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS |

## Downloaded (date)

2026-10-21 (UTC). All three stored downloads came from Wayback.

## License class

Public, redistributable under this goal's FRED storage convention.
Files are in `data/public/fred/`. Each `<ID>.raw.csv` retains the published bytes;
each `<ID>.csv` is tidy. FRED aggregates third-party data; retain source credit.
DTB3 and DGS10 originate in the Federal Reserve Board H.15 release.
VIXCLS originates at Cboe. See https://fred.stlouisfed.org/legal/.
This card does not assert a separate Cboe redistribution grant.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| DTB3 | Percent per year, 3-month Treasury bill discount basis, not seasonally adjusted | Unchanged |
| DGS10 | Percent per year, 10-year Treasury constant maturity market yield, not seasonally adjusted | Unchanged |
| VIXCLS | VIX index points, daily close, not seasonally adjusted | Unchanged |

## Transforms

Rename `observation_date` to `date`; parse empty fields and `.` as missing values.
Sort by date. Retain missing dates and values; do not fill or interpolate.
No return conversion or unit scaling. Reject duplicate dates, invalid schemas,
and files without observed values at both study endpoints.

## Coverage

Raw and tidy files have identical coverage and row counts. Frequency is daily
on the source's weekday grid; holidays can have missing observations.

| Series | First date | Last date | Rows | Missing values |
|---|---|---|---|---|
| DTB3 | 1954-01-04 | 2026-07-06 | 18,916 | 799 |
| DGS10 | 1962-01-02 | 2026-10-09 | 16,899 | 720 |
| VIXCLS | 1990-01-02 | 2026-10-08 | 9,593 | 302 |

All three contain observations on 1997-09-10 and 2023-03-17.
Every raw and tidy file prints one `OK` line with its row count and endpoints.

## Known problems

The archive snapshots are the available vintages, not current FRED releases.
DTB3 is especially stale after 2026-07-06. The live endpoint is tried on every run;
when it recovers, the fetcher downloads its full available history instead.
An unavailable live source is reported before the archive is used. No source
values are fabricated. FRED's legacy download and API routes also returned
maintenance HTML on 2026-10-21. Downstream code must handle missing holidays.

## Paper datasets served (D-numbers)

D7 (cash rate), D8 (VIX). DGS10 is a reference yield for D2 and D17;
it is not a Treasury futures return.
