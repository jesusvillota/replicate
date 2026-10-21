# Source card: CRR Public Plans Data

## Source and URL or WRDS table

Center for Retirement Research at Boston College, Public Plans Data (PPD).
Citation: Public Plans Data, 2001–2025. Center for Retirement Research at Boston
College, MissionSquare Research Institute, National Association of State
Retirement Administrators, and Government Finance Officers Association.

- Download page: https://publicplansdata.org/public-plans-database/download-full-data-set/
- Full CSV: `https://publicplansdata.org/api/`, using the site's `QVariables`
  query and complete current variable list. Exact request URL is in `metadata.json`.
- Download definition: https://publicplansdata.org/wp-content/themes/publicplans2024/js/ppd.js
- Codebook: https://publicplansdata.org/api/?q=gettemplate&template=data-codebook&format=csv&filename=ppd-codebook.csv&includeheader=1
- Detailed investment data: https://publicplansdata.org/wp-content/uploads/2024/09/PensionInvestmentPerformanceDetailed.xlsx
- Detailed codebook: https://publicplansdata.org/wp-content/uploads/2013/12/Investment-Codebook.xlsx

## Downloaded (date)

2026-10-21. Run `uv run python3 -m rebal.fetch.ppd` to download again.

## License class

Public, redistributable, with CRR attribution. Stored under `data/public/ppd/`.
Keep original full CSV, detailed workbook, both codebooks, and download definition.
Each is below 20 MB, so the full raw dataset is retained unchanged.
`ppd_allocations.csv` contains only the needed fields. `metadata.json` records URLs.

## Series, with units

Original variable names are retained in the tidy output:

| Role | Variables used | Raw and output units |
|---|---|---|
| Plan key | `ppd_id`, `PlanName` | Identifier, text |
| Fiscal year | `fy` | Year |
| Total assets | `MktAssets_net` | USD thousands, end-of-year net market assets |
| Total equity, actual and target | `EQTotal_Actl`, `EQTotal_Trgt` | Published allocation values |
| Fixed income, actual and target | `FITotal_Actl`, `FITotal_Trgt` | Published allocation values |
| Cash, actual and target | `CashTotal_Actl`, `CashTotal_Trgt` | Published allocation values |
| Domestic equity, actual | `EQDomesticMisc_Actl`, `EQDomesticLarge_Actl`, `EQDomesticMid_Actl`, `EQDomesticSmall_Actl` | Published allocation values |
| Domestic equity, target | `EQDomesticMisc_Trgt`, `EQDomesticLarge_Trgt`, `EQDomesticMid_Trgt`, `EQDomesticSmall_Trgt` | Published allocation values |
| International equity, actual | `EQIntlMisc_Actl`, `EQIntlDev_Actl`, `EQIntlEmerg_Actl`, `EQIntlPass_Actl`, `EQIntlActv_Actl` | Published allocation values |
| International equity, target | `EQIntlMisc_Trgt`, `EQIntlDev_Trgt`, `EQIntlEmerg_Trgt`, `EQIntlPass_Trgt`, `EQIntlActv_Trgt` | Published allocation values |
| Global equity, actual and target | `EQGlobal_Actl`, `EQGlobal_Trgt`, `EQGlobalGrowth_Actl`, `EQGlobalGrowth_Trgt` | Published allocation values |

The codebook labels allocations “Percentage point”. The CSV actually expresses
them as fractions: `0.25` represents a 25% allocation. Preserve these raw values;
TASK-012 owns conversions. Do not multiply allocations or assets in this fetcher.
Domestic and international component variables come from the detailed workbook.
Global equity remains separate because it can contain both domestic and foreign stocks.

## Transforms

Decode the full CSV as Windows-1252. Keep fiscal years 2003–2022.
Read the detailed workbook's plan-level rows and join on `ppd_id`, `fy`, one to one.
Keep domestic and international components as published, without adding them into
invented geographic totals. Preserve missing values and reported zeros.
Add `date=fy-12-31` as a fiscal-year label, not the plan's actual reporting date.
Sort by fiscal year and plan ID. Validate unique plan-year keys, numeric values,
and observations for all six main allocation variables in every required year.
Dates repeat across plans. The shared `summarize` helper checks unique annual
labels in `ppd_coverage.csv`; the fetcher separately checks the panel keys.

## Coverage

Fiscal years 2003–2022, all 20 years; 5,060 plan-year rows in `ppd_allocations.csv`.
`ppd_coverage.csv`: 20 rows, 2003-12-31–2022-12-31; each row counts plans.
The raw full file contains 7,578 rows; the raw detailed file contains 6,052 rows.
There are missing allocations for individual plans; no values are filled.

## Known problems

The sample is not a balanced panel: plan availability differs by year.
Detailed geography has fewer observations than the main totals. The detailed file
retains its published vintage; it is not silently replaced by a newer total-series vintage.
`EQIntlPass_Trgt`, `EQIntlActv_Trgt`, and `EQGlobalGrowth_Trgt` are entirely missing
in 2003–2022. Other geographic targets are sparse. Their blank columns are retained.
The main file no longer supplies the legacy `equities_domestic` and
`equities_international` fields; the official detailed data supply the components.
No domestic/international aggregate is inferred from total equity or global equity.
The current download includes some placeholder years outside our selected range.

## Paper datasets served (D-numbers)

D23. Figure 1 and allocation analysis are outside this task.
