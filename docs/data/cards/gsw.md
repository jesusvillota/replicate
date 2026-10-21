# Source card: Fed GSW nominal yield curve

## Source and URL or WRDS table

Federal Reserve Board, Gürkaynak–Sack–Wright nominal Treasury yield curve.
https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv
Documentation: https://www.federalreserve.gov/data/nominal-yield-curve.htm
Run `uv run python3 -m rebal.fetch.gsw`.

## Downloaded (date)

2026-10-21 (UTC), directly from the Fed.

## License class

Public, redistributable federal research data. Credit the Federal Reserve Board
and Gürkaynak, Sack and Wright. Both files are committed in `data/public/gsw/`.
`feds200628.raw.csv` retains all published bytes, including the header notes
and forward-rate columns. `feds200628.csv` is the selected tidy data.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| SVENY01–SVENY30 | Percent per year, continuously compounded zero-coupon yields | Unchanged |
| SVENPY01–SVENPY30 | Percent per year, coupon-equivalent par yields | Unchanged |
| BETA0–BETA3 | Published curve parameters (yield level coefficients) | Unchanged |
| TAU1, TAU2 | Published curve parameters (decay time constants, years) | Unchanged |

The source marks parameter compounding as `N/A`.

## Transforms

Locate the `Date,` header after the notes. Rename `Date` to `date`, select all
60 yield columns and six parameters, and sort by date. Parse `NA` and the
parameter sentinel `-999.99` as missing values. Do not fill gaps or scale units.
If the tidy CSV would reach 20,000,000 bytes, remove only SVENPY11–SVENPY30.
That reduction was not needed: all 66 series remain.

## Coverage

Both raw and tidy files: 17,048 daily rows, 1961-06-14–2026-10-16.
The raw file is 16,661,023 bytes; the tidy file is 10,812,413 bytes.
Each is below 20 MB and prints its own `OK` coverage line.

SVENY10 and SVENPY10 have observed values from **1971-08-16–2026-10-16**.
Each has 3,285 missing rows, including the period before 1971-08-16.
Both have observed values at 1997-09-10 and 2023-03-17.
Longer maturities start later. Missing holidays and unavailable maturities remain
missing. There are no duplicate dates.

## Known problems

This is a staff research product, not an official statistical release. The Fed
can revise history and methods without notice. Ten-year yields are unavailable
before August 1971; the overall file start must not be used as their start date.
The early model has no active second decay parameter; its sentinel becomes missing.
No yield-to-return conversion is part of this task.

## Paper datasets served (D-numbers)

D2 (candidate Treasury proxy input), D17 (long-sample Treasury input).
