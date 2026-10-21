# Source card: ara

Status: available

## Source and URL or WRDS table

Da, Hua, Hung and Peng (2025), “Market Returns and a Tale of Two Types of
Attention,” Management Science 71(12), 10505–10537.
https://doi.org/10.1287/mnsc.2023.01294 .

Public author source: https://sites.google.com/site/linpengbaruch/data .
Its “Aggregate Retail/Institutional Attention data” link points to:
https://www.dropbox.com/scl/fo/xpi0irqtlnxq6rbre06k5/AH-eVcrOnGbSKMSBdSG0nEA?rlkey=y61un7nk0j45bny0z0yb8b4np&raw=1 .
Tim Hung's https://sites.google.com/view/timcchung links this coauthor data page.

Access: `uv run python3 -m rebal.fetch.ara` downloads the published folder ZIP.

## Downloaded (date)

2026-10-21.

## License class

Licensed or terms-restricted: public author download with a citation request,
but no broad redistribution grant. Store unchanged `ara.raw.zip` and tidy
`ara.csv` under `licensed_dir("ara")`, default
`~/data/replicate/licensed/ara/`, outside git.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `ara` | Market-cap weighted abnormal Google Search Volume Index | Same |

The authors define abnormal search volume relative to its trailing 180 trading-day
median, using previous-month market-cap weights. Preserve the published numeric
scale; any downstream scaling belongs to TASK-012.

## Transforms

Read `ARA.csv` inside the ZIP; parse `date` as `%d%b%Y` into ISO dates.
Keep the ZIP intact, including `Readme.pdf`. No scaling, interpolation or filling.

## Coverage

`ara.raw.zip` (ARA.csv) and `ara.csv`: 3,903 rows each, 2004-07-01 through
2019-12-31. Trading-day observations; no missing values among supplied rows.

## Known problems

The README calls the CSV tab-delimited; the published file uses commas.
History ends in 2019 and cannot supply later observations.
Dropbox returns an HTML viewer to the default Safari user agent with `dl=1`.
The fetcher uses `raw=1`, which returns the published ZIP with the same headers.

The publisher's live supplement returns HTTP 403. Its archived page at
https://web.archive.org/web/20250531025932id_/https://pubsonline.informs.org/doi/suppl/10.1287/mnsc.2023.01294
links a separate agreement form at
https://services.informs.org/dataset/download.php?doi=mnsc.2023.01294 .
That form restricts use to replication of the attention paper. No agreement was
submitted; this fetcher uses the public coauthor link instead.

## Paper datasets served (D-numbers)

D15. See `docs/contracts/daily_panel.md` for the downstream panel contract.
