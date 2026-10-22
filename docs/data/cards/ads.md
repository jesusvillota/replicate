# Source card: ads

Status: available

## Source and URL or WRDS table

Philadelphia Fed; Aruoba–Diebold–Scotti Business Conditions Index.

https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/ads

Download: https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/ads/ADS_Index_Most_Current_Vintage.xlsx

Access: public HTTPS download via `uv run python3 -m rebal.fetch.ads`.

## Downloaded (date)

2026-10-21.

## License class

Public, redistributable Fed data. Store under `data/public/ads/`; credit the Philadelphia Fed.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `ads` (`ADS_Index`) | Standardized index, zero average business conditions | Same |

## Transforms

Parse `Date` as `%Y:%m:%d`; rename `ADS_Index` to `ads`. Keep the full published workbook, including `RECBARS` recession bars. Tidy CSV contains the ADS series only. No scaling, interpolation or filling.

## Coverage

`ADS_Index_Most_Current_Vintage.xlsx` (Sheet1) and `ads.csv`: 24,330 rows each, 1960-03-01 through 2026-10-10. Daily calendar dates; no gaps or missing values.

## Known problems

We use the latest vintage, not a real-time vintage. Historical observations incorporate later information and revisions; they are unsuitable for a claim of real-time availability.

## Paper datasets served (D-numbers)

D11. See `docs/contracts/daily_panel.md` for the downstream panel contract.
