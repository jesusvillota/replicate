# Source card: ICI

## Source and URL or WRDS table

Investment Company Institute, Estimated Long-Term Mutual Fund Flows (D22).
Official release: https://www.ici.org/research/stats/flows
Current original workbook: https://www.ici.org/flows_data_2026.xls

Original Excel and PDF bytes come from 56 distinct Wayback captures: 47 XLS
and nine PDF files. The committed [archive manifest](../../../src/rebal/fetch/ici_archives.csv)
lists every timestamp, original URL, and CDX SHA-1 digest. It contains no flow data.
For each row, the canonical replay URL is
`https://web.archive.org/web/<snapshot>id_/<original_url>`.
External `metadata.json` records each selected source, filename, row count, and dates.

Archive discovery searched the whole ICI domain, including both host variants,
with these CDX queries (HTTP and HTTPS versions of the CDX endpoint were used):

- `https://web.archive.org/cdx/search/cdx?url=ici.org%2F%2A&output=json&filter=statuscode%3A200&filter=original%3A.%2A%5BFf%5D%5BLl%5D%5BOo%5D%5BWw%5D.%2A&collapse=urlkey`
- `https://web.archive.org/cdx/search/cdx?url=ici.org%2F%2A&output=json&filter=statuscode%3A200&filter=original%3A.%2Aflows_data_.%2A%5B.%5Dxls&collapse=digest`
- `https://web.archive.org/cdx/search/cdx?url=ici.org%2F%2A&output=json&filter=statuscode%3A200&filter=original%3A.%2Aflows_data_.%2A%5B.%5Dpdf&collapse=digest`

Also queried individual `/info/flows_data_<year>.xls` paths for 2007–2026.
The domain search found `/info/`, `/pdf/`, `/stats/mf/`, `/statements/nr/`,
`/doc-server/info%3A`, `/doc-server/pdf%3A`, `/system/files/attachments/`,
and dated `/system/files/<year-month>/` paths. Exact original paths are in the manifest.
Middle-wildcard URL queries can return empty results despite existing captures;
the whole-domain prefix queries above avoid that error.
Combined mutual-fund-plus-ETF and ETF-only tables are separate series and excluded.

## Downloaded (date)

2026-10-22. Run `uv run python3 -m rebal.fetch.ici` to download again.

## License class

Licensed or terms-restricted: ICI's redistribution terms are unclear.
Original `.xls` and `.pdf` files, `ici_weekly_flows.csv`, and `metadata.json` stay under
`licensed_dir("ici")`: by default `~/data/replicate/licensed/ici/`.
`REPLICATE_DATA_DIR` can change the external root. No ICI data enter git.

## Series, with units

| Output series | ICI series | Raw and output units |
|---|---|---|
| `total_equity` | Total equity | USD millions |
| `domestic_equity` | Total domestic equity | USD millions |
| `world_equity` | Total world equity | USD millions |
| `hybrid` | Hybrid | USD millions |
| `taxable_bond` | Total taxable bond | USD millions |
| `municipal_bond` | Municipal bond | USD millions |
| `total` | Total long-term | USD millions |

## Transforms

Read only `Estimated Weekly Net New Cash Flow`; exclude monthly actual flows.
The nine-column Excel layout uses sheet `aggregate_summary012109`. Its series
order is equity, domestic equity, foreign/world equity, hybrid, total bond,
taxable bond, municipal bond, and total. Do not map total bond to taxable bond.
The 40-column layout uses `Weekly MF Flow Estimates` and spacer columns.
Validate headers and the published millions-of-dollars units in both layouts.
Explicitly accept the original 2016 spelling `Millions, U.S. dolllars`.

The older nine-column PDFs use the same category order. Extract their original
text with `pypdf`, validate headers and units, then parse only the weekly section.
Accept two-digit years in the January 2009 release and four-digit years elsewhere.
For example, `12/23/08` stays 2008-12-23. Keep Tuesday holiday week endings.
No OCR, monthly-to-weekly conversion, interpolation, or unit scaling is used.
For duplicate dates, use the latest archived publication, then the live file.
Validate numeric values and unique dates, and use shared `download` and `summarize`.

Cache immutable snapshots outside git and check each payload against its CDX digest
before parsing. `--refresh-archives` downloads them again. Alternate replay routes
handle intermittent connection resets; the digest protects against replay redirects.
The live workbook is downloaded on every run.

## Coverage

2008-12-03–2026-10-14; weekly; 278 rows in `ici_weekly_flows.csv`.
Requested starting-history gap: 2007-01-01–2008-12-02.
The earliest recovered weekly observations are December 2008 in the archived
January 2009 PDF. Its monthly section starts in January 2007; those monthly
values cannot supply the requested weekly estimates. Whole-domain CDX searches
did not locate an earlier weekly original. No claim is made that ICI never published one.

Every recovered block and every remaining gap through the last observed week
are listed below. A block has no separation over eight days between observations;
this allows the published Tuesday/Wednesday holiday shifts. Gap bounds are calendar
dates strictly between blocks, not invented week-ending dates. Normal days between
adjacent weekly observations are not gaps. The manifest and external CSV retain all dates.

| Recovered weekly block | Rows | Missing interval immediately before it |
|---|---:|---|
| 2008-12-03–2009-03-04 | 14 | 2007-01-01–2008-12-02 |
| 2009-12-02–2010-01-20 | 8 | 2009-03-05–2009-12-01 |
| 2010-03-03–2010-03-24 | 4 | 2010-01-21–2010-03-02 |
| 2010-10-06–2010-12-15 | 11 | 2010-03-25–2010-10-05 |
| 2011-01-05–2011-02-09 | 6 | 2010-12-16–2011-01-04 |
| 2011-03-02–2011-04-20 | 8 | 2011-02-10–2011-03-01 |
| 2011-05-04–2011-06-15 | 7 | 2011-04-21–2011-05-03 |
| 2011-08-03–2011-08-24 | 4 | 2011-06-16–2011-08-02 |
| 2011-10-05–2011-12-14 | 11 | 2011-08-25–2011-10-04 |
| 2012-01-04–2012-02-08 | 6 | 2011-12-15–2012-01-03 |
| 2012-03-07–2012-04-11 | 6 | 2012-02-09–2012-03-06 |
| 2012-05-02–2012-06-20 | 8 | 2012-04-12–2012-05-01 |
| 2012-08-01–2012-09-05 | 6 | 2012-06-21–2012-07-31 |
| 2012-10-03–2012-11-07 | 6 | 2012-09-06–2012-10-02 |
| 2012-12-05–2013-01-09 | 6 | 2012-11-08–2012-12-04 |
| 2013-02-06–2013-03-20 | 7 | 2013-01-10–2013-02-05 |
| 2013-04-03–2013-05-15 | 7 | 2013-03-21–2013-04-02 |
| 2013-07-02–2013-08-28 | 9 | 2013-05-16–2013-07-01 |
| 2013-10-02–2013-11-06 | 6 | 2013-08-29–2013-10-01 |
| 2013-12-04–2013-12-31 | 5 | 2013-11-07–2013-12-03 |
| 2014-02-05–2014-04-09 | 10 | 2014-01-01–2014-02-04 |
| 2014-06-04–2014-08-20 | 12 | 2014-04-10–2014-06-03 |
| 2014-09-03–2014-10-01 | 5 | 2014-08-21–2014-09-02 |
| 2015-02-25–2015-03-25 | 5 | 2014-10-02–2015-02-24 |
| 2015-12-02–2015-12-30 | 5 | 2015-03-26–2015-12-01 |
| 2016-02-03–2016-04-06 | 10 | 2015-12-31–2016-02-02 |
| 2017-01-04–2017-01-25 | 4 | 2016-04-07–2017-01-03 |
| 2017-06-07–2017-06-28 | 4 | 2017-01-26–2017-06-06 |
| 2017-08-02–2017-09-20 | 8 | 2017-06-29–2017-08-01 |
| 2019-12-04–2019-12-31 | 5 | 2017-09-21–2019-12-03 |
| 2020-05-27–2020-06-24 | 5 | 2020-01-01–2020-05-26 |
| 2022-02-02–2022-03-23 | 8 | 2020-06-25–2022-02-01 |
| 2024-01-03–2024-02-14 | 7 | 2022-03-24–2024-01-02 |
| 2024-10-02–2024-11-20 | 8 | 2024-02-15–2024-10-01 |
| 2024-12-04–2025-01-08 | 6 | 2024-11-21–2024-12-03 |
| 2025-10-01–2025-11-12 | 7 | 2025-01-09–2025-09-30 |
| 2025-12-03–2026-02-18 | 12 | 2025-11-13–2025-12-02 |
| 2026-03-04–2026-04-01 | 5 | 2026-02-19–2026-03-03 |
| 2026-09-02–2026-10-14 | 7 | 2026-04-02–2026-09-01 |

## Known problems

Direct requests sometimes receive Akamai HTTP 403 errors; archive replay can reset
connections. If live access fails, the command reports it and ends at the final
archived observation. A missing required snapshot, digest mismatch, or changed
schema fails loudly. Current verified live coverage ends on 2026-10-14; later
weeks have not been obtained in this session.

One indexed capture cannot be recovered as indexed:
`20250926000730`, `https://www.ici.org/system/files/2025-01/flows_data_2025.xls`.
Replay redirects to `20250118182822`, and the returned digest differs from the
September CDX digest. Only the verified January capture is included. No September
coverage is inferred. Multiple archive paths serving identical bytes are deduplicated.

Coverage remains incomplete for Figure 5. Acceptance permits an explained gap.
ICI's notes describe weekly industry estimates; monthly actuals are a different series.
Published components can differ from totals through rounding. Older releases state
95% industry-asset reporting coverage; recent releases state about 98%.

## Paper datasets served (D-numbers)

D22. The equity-minus-bond measure and Figure 5 are outside this task.
