# Source card: ICI

## Source and URL or WRDS table

Investment Company Institute, Estimated Long-Term Mutual Fund Flows (D22).
Official release: https://www.ici.org/research/stats/flows
Current original workbook: https://www.ici.org/flows_data_2026.xls

Original Excel bytes recovered from these Wayback snapshots:

- https://web.archive.org/web/20251126095130id_/https://www.ici.org/flows_data_2025.xls
- https://web.archive.org/web/20260115002828id_/https://www.ici.org/flows_data_2026.xls
- https://web.archive.org/web/20260227055331id_/https://www.ici.org/flows_data_2026.xls
- https://web.archive.org/web/20260412002219id_/https://www.ici.org/flows_data_2026.xls

## Downloaded (date)

2026-10-21. Run `uv run python3 -m rebal.fetch.ici` to download again.

## License class

Licensed or terms-restricted: ICI's redistribution terms are unclear.
Original `.xls` files, `ici_weekly_flows.csv`, and `metadata.json` stay under
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

Read only the `Estimated Weekly Net New Cash Flow` section of sheet
`Weekly MF Flow Estimates`. Exclude monthly actual flows in the same workbook.
Keep reported week-ending dates, including holiday weeks ending on Tuesdays.
Keep signed dollar flows without scaling. Do not interpolate missing weeks.
For duplicate dates, use the latest archived publication, then the live file.
For example, the February snapshot revises the January 7 equity estimate.
Validate headers, units, numeric values, and unique dates. Use the shared
`download` and `summarize` helpers. Metadata record every successful source URL.

## Coverage

2025-10-01–2026-10-14; weekly; 31 rows in `ici_weekly_flows.csv`.
Gap: requested 2007-01-01–2025-09-30 history was not recovered.
Recovered blocks: 2025-10-01–11-12, 2025-12-03–2026-02-18,
2026-03-04–04-01, and 2026-09-02–10-14.

Further missing intervals: 2025-11-13–12-02, 2026-02-19–03-03, and
2026-04-02–09-01. The source files contain only a short window of weekly estimates.
Their longer monthly sections do not supply the requested weekly history.
Wayback CDX queries for `www.ici.org/flows_data_<year>.xls`, 2007–2024,
returned no successful captures. Those queries do not prove all earlier ICI URLs
are absent. The four original snapshots above are the history recovered here.

## Known problems

Direct requests sometimes receive Akamai HTTP 403 errors. The live original
workbook succeeded in this session. When live access fails, the command reports
it and uses the four archived originals; the printed last date then ends earlier.
An unavailable archive or changed workbook schema fails loudly.
Coverage is incomplete and cannot support the full Figure 5 sample yet.
The owner explicitly permits an explained history gap in this task's acceptance.
ICI says weekly estimates cover about 98% of industry assets; monthly actuals
are a different series. Published components can differ from totals through rounding.
No third-party text conversion is used as a substitute for original Excel bytes.

## Paper datasets served (D-numbers)

D22. The equity-minus-bond measure and Figure 5 are outside this task.
