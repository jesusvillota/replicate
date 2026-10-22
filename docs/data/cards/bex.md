# Source card: bex

Status: available

## Source and URL or WRDS table

Bekaert, Engstrom and Xu (2021), The Time Variation in Risk Appetite and Uncertainty. Nancy Xu's official data page.

https://www.nancyxu.net/risk-aversion-index

Resolved on 2026-10-21: https://www.nancyxu.net/_files/ugd/efd0b7_0a8d3633a3ad4be7b8f536261e500250.xlsx?dn=BEX_Indices_20261005.xlsx

Access: public HTTPS download via `uv run python3 -m rebal.fetch.bex`.

## Downloaded (date)

2026-10-21.

## License class

Licensed or terms-restricted: no clear redistribution grant found. Raw `bex.raw.xlsx` and tidy `bex.csv` stay under `licensed_dir("bex")` (`$REPLICATE_DATA_DIR/licensed/bex/`, default `~/data/replicate/licensed/bex/`), outside git.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `ra` (`ra_bex_PAPER`) | Risk aversion index, 2 × exp(qt) | Same |
| `unc` (`unc_bex_PAPER`) | Monthly variance | Same |

## Transforms

Resolve the current BEX workbook link from the author's page. Read `DATA_PLOT_daily` columns A:C; parse `yyyymmdd` as `%Y%m%d`; rename B/C to `ra`/`unc`. Preserve all sheets in the raw workbook. No scaling, interpolation or filling. Do not substitute column D (`unc_bex_AnnualVolPercentage`) for monthly variance.

## Coverage

`bex.raw.xlsx` (DATA_PLOT_daily) and `bex.csv`: 10,073 rows each, 1986-05-30 through 2026-09-30. Trading-day observations; no missing values in `ra` or `unc`.

## Known problems

The workbook is updated over time; each run resolves its current link. Latest revised history, not real-time vintages. Redistribution terms are unclear, so no BEX data enter git.

## Paper datasets served (D-numbers)

D13. See `docs/contracts/daily_panel.md` for the downstream panel contract.
