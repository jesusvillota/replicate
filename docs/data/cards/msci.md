# Source card: MSCI

## Source and URL or WRDS table

MSCI public End of day index data search:
<https://app2.msci.com/products/index-data-search/>.
The former `https://app2.msci.com/products/indexes/performance/regional_chart.html`
redirects here. The `www.msci.com/end-of-day-data-search` entry returned HTTP 403.
The working Excel service is
`https://app2.msci.com/products/service/index/indexmaster/downloadLevelData`.
Run `uv run python3 -m rebal.fetch.msci`.

Parameters: `output=INDEX_LEVELS`, `currency_symbol=USD`, `index_variant=NETR`,
`data_frequency=daily`, `index_codes=899901`, `start_date=19970101`.
The default end date comes from the same service's `getLatestWorldDate` endpoint.

**Verified index code: `899901`.** The downloaded workbook identifies
`ACWI ex USA Standard (Large+Mid Cap)`, `Index Level : Net`, `Currency : USD`.
The proposed `991000` instead downloads `WORLD ex USA Standard (Large+Mid Cap)`.
The fetcher checks all three labels before writing a CSV, so this substitution fails loudly.

## Downloaded (date)

2026-10-21. Latest published world date: 2026-10-20.
Status: available, with partial sample coverage.

## License class

Licensed or terms-restricted. MSCI's workbook includes its copyright and use restrictions.
[MSCI terms](https://www.msci.com/terms-of-use). All files stay in
`$REPLICATE_DATA_DIR/licensed/msci/`, default `~/data/replicate/licensed/msci/`.
The original workbook is `acwi_ex_usa_net_usd.xls`. The tidy CSV is
`acwi_ex_usa_net_usd.csv`. Its metadata records the URL, parameters, index identity,
coverage, download time, and original workbook SHA-256. `latest_world_date.txt`
preserves the service's date response. No downloaded data enters git.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| MSCI ACWI ex USA, Net Total Return, USD (`899901`) | Published index points | Same |

## Transforms

Read the workbook's `History Index` sheet. Verify index identity, Net variant and USD.
Remove the title rows and license footer. Parse dates and numeric levels without scaling.
Write `date,acwi_ex_usa_net_usd`; preserve the original workbook unchanged.
Reject missing/nonpositive levels, duplicate/unsorted dates, and dates outside the request.
Validate the CSV with `common.summarize`. No returns, interpolation, or gap filling.

## Coverage

**2000-12-29 to 2026-10-20**, daily, **6,733 rows**. Requested from 1997-01-01.
It **does not cover 1997-09-10**; the public download supplies no earlier observations.
Longest calendar gap: 3 days. No duplicate dates or missing levels were found.

The service returns weekday levels, including some market holidays. Repeated levels
remain unchanged. The first published level is 100; this is the provider's scale.
The requested 1997-01-01 through 2000-12-28 period remains absent.

## Known problems

The public history starts after the paper's sample begins. TASK-009's CRSP ETFs
(VEU, ACWX, EFA) are proxy candidates; TASK-012 handles panel integration.
No proxy is selected or spliced in this task. Provider access and history can change.
`getLevelDataForDate` returned HTTP 404; use the working `downloadLevelData` service.
The current service is available, so an archive fallback is not needed.

## Paper datasets served (D-numbers)

D6.
