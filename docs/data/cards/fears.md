# Source card: fears

Status: available (archived public 2004–2011 subset); paper's private extension not available

## Source and URL or WRDS table

Da, Engelberg and Gao, “The Sum of All FEARS: Investor Sentiment and Asset Prices.”
Zhi Da's archived author page links the public historical CSV:
https://web.archive.org/web/20251213104436id_/https://www3.nd.edu/~zda/ .

Publisher appendix checked: https://doi.org/10.1093/rfs/hhu072 (HTTP 403).

Original URL: https://www3.nd.edu/~zda/fears_post_20140512.csv .
The live host resets the connection. Retrieved unchanged via the Wayback Machine:
https://web.archive.org/web/20230627055206id_/https://www3.nd.edu/~zda/fears_post_20140512.csv .

Access: `uv run python3 -m rebal.fetch.fears`.

## Downloaded (date)

2026-10-21; archive snapshot 2023-06-27; published file vintage 2014-05-12.

## License class

Licensed or terms-restricted: public download, no explicit redistribution grant
found. Store raw `fears_post_20140512.raw.csv` and tidy `fears.csv` under
`licensed_dir("fears")`, default `~/data/replicate/licensed/fears/`, outside git.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `fears25` | Published unitless FEARS score | Same |
| `fears30` | Published unitless FEARS score | Same |
| `fears35` | Published unitless FEARS score | Same |

## Transforms

Parse month/day/year dates into ISO `date`. Retain all three published variants
and their values. No scaling, interpolation, selection of a preferred variant,
or extension of the history.

## Coverage

Raw CSV and tidy CSV: 1,891 rows each, 2004-07-01 through 2011-12-30.
Trading-day observations; no missing values among supplied rows.

## Known problems

Footnote 23 says the rebalancing authors obtained FEARS privately. The public
file stops in 2011 and cannot reproduce their longer sample. The private
extension remains unavailable. Keep the archived public subset for inspection;
skip the paper's FEARS column of Table D.9 until the required series is obtained.
The archive preserves an old Google-search-based vintage; no current updates
or real-time availability are claimed.

## Paper datasets served (D-numbers)

D14, public subset only; full replication unavailable.
See `docs/contracts/daily_panel.md` for the downstream contract.
