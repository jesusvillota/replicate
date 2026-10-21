# Source card: OFR Financial Stress Index

## Source and URL or WRDS table

Office of Financial Research (OFR), U.S. Treasury.
Page: https://www.financialresearch.gov/financial-stress-index/
CSV: https://www.financialresearch.gov/financial-stress-index/data/fsi.csv
The page's CSV download form points to this URL.
Run `uv run python3 -m rebal.fetch.ofr`.

## Downloaded (date)

2026-10-21 (UTC), directly from OFR.

## License class

Public, redistributable federal data; credit OFR.
https://www.financialresearch.gov/legal-notices/ states: “No copyright may be
claimed for any work on this website that was created by a federal employee
in the course of his or her duties. However, credit is requested if you
reproduce or copy any such work.” Third-party copyrighted materials have
separate terms. Store the unchanged `fsi.raw.csv` and tidy `fsi.csv` in
`data/public/ofr/`.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| OFR FSI | Standardized financial stress index points | Unchanged |
| Credit, Equity valuation, Safe assets, Funding, Volatility | Contributions to the stress index, in index points | Unchanged |
| United States, Other advanced economies, Emerging markets | Regional contributions to the stress index, in index points | Unchanged |

## Transforms

Rename `Date` to `date`, parse dates, and sort ascending. Keep all category and
region columns under their published names. No scaling, interpolation or return
conversion. Reject duplicate dates, nonnumeric values, or a truncated Funding history.

## Coverage

Both files: **2000-01-03–2026-10-19**, **6,783 daily rows**.
All nine series, including **Funding**, have this observed coverage, with no
missing values in the published rows. No duplicate dates. Nonpublished days
are not inserted. Each file prints one `OK` line containing these endpoints.

## Known problems

The source says publication lags two business days. History may be revised.
Funding has no 1997–1999 history and cannot cover the full core study period.
OFR stress contributions differ from BofA GFSI Liquidity Risk. Funding is the
planned fallback liquidity proxy; TASK-012 chooses between it and HPW noise.
Do not interpret a category contribution as a separate standardized index.
Published values are rounded. Category sums can differ from the total by
up to 0.002 index points in this download; the stored-file test allows the
0.003 rounding bound for five contributions and the total.

## Paper datasets served (D-numbers)

D26 (candidate liquidity-stress proxy).
