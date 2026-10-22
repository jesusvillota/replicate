# Source card: Kenneth French data library

## Source and URL or WRDS table

Kenneth R. French, Dartmouth, U.S. daily factor returns.
Library: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>.
Download base: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/>.
Append each exact archive name below to that base:

- `F-F_Research_Data_Factors_daily_CSV.zip`
- `F-F_Research_Data_5_Factors_2x3_daily_CSV.zip`
- `F-F_Momentum_Factor_daily_CSV.zip`
- `F-F_ST_Reversal_Factor_daily_CSV.zip`
- `F-F_LT_Reversal_Factor_daily_CSV.zip`

Access: `uv run python3 -m rebal.fetch.french`, using
`rebal.fetch.common.download`. No login or archive mirror was needed.

## Downloaded (date)

2026-10-21. Published archives use the August 2026 CRSP vintage.

## License class

Public, redistributable under the goal's public-data classification.
Unchanged ZIPs and tidy CSVs are committed in `data/public/french/`.
The archives retain the publisher's copyright notices. Cite Fama and French
and the French library when using these data; no software license is implied.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| Mkt-RF: market excess return | percent per day | percent per day |
| SMB: size factor | percent per day | percent per day |
| HML: value factor | percent per day | percent per day |
| RMW: profitability factor, five-factor file | percent per day | percent per day |
| CMA: investment factor, five-factor file | percent per day | percent per day |
| RF: risk-free return, three- and five-factor files | percent per day | percent per day |
| Mom: momentum factor | percent per day | percent per day |
| ST_Rev: short-term reversal factor | percent per day | percent per day |
| LT_Rev: long-term reversal factor | percent per day | percent per day |

## Transforms

Keep raw ZIP bytes exactly as published. Read only the first daily CSV block;
exclude notes, blank separators, annual/monthly tables and copyright footers.
Trim header spaces, name the first column `date`, and parse `YYYYMMDD` as
ISO `YYYY-MM-DD`. Keep the published series names and full histories.
Map the library's missing markers `-99.99` and `-999` to empty CSV values.
Do not fill gaps, interpolate, join, or convert returns to decimals.
Each tidy filename is the archive name with `_CSV.zip` replaced by `.csv`.

Validate columns, numeric values, unique dates and required sample endpoints.
`rebal.fetch.common.summarize` checks each raw daily block and each tidy CSV.
TASK-012 owns conversion and panel assembly under
[`docs/contracts/daily_panel.md`](../../contracts/daily_panel.md).
For D16, the total market return requires `Mkt-RF + RF`; this fetcher retains
both published components without constructing that return.

## Coverage

All files contain daily observations on the publisher's trading calendar.

| Tidy CSV stem | First date | Last date | Rows |
|---|---|---|---:|
| F-F_Research_Data_Factors_daily | 1926-07-01 | 2026-08-31 | 26317 |
| F-F_Research_Data_5_Factors_2x3_daily | 1963-07-01 | 2026-08-31 | 15897 |
| F-F_Momentum_Factor_daily | 1926-11-03 | 2026-08-31 | 26216 |
| F-F_ST_Reversal_Factor_daily | 1926-01-26 | 2026-08-31 | 26446 |
| F-F_LT_Reversal_Factor_daily | 1930-03-20 | 2026-08-31 | 25216 |

The three-factor file covers 1961-06-16 through 2023-03-17.
All other files cover 1997-09-10 through 2023-03-17.
Both required endpoints exist, with all series observed. Stored-file tests
found no missing factor values or duplicate dates in any file.
Nontrading dates stay absent; historical calendars can include Saturdays.

## Known problems

These are current-vintage data, not a frozen vintage from the paper.
Historical returns can change when CRSP or the library revises its data.
Three- and five-factor files use their own published factor definitions;
do not assume their overlapping factor values are identical.
The archive notes a risk-free source change in June 2024, from Ibbotson
Associates to the ICE BofA US 1-Month Treasury Bill Index.

## Paper datasets served (D-numbers)

D16 (long-sample equity return components) and D24 (Carhart, FF5 and reversal factors).
