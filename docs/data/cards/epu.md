# Source card: epu

Status: available

## Source and URL or WRDS table

Baker, Bloom and Davis; US daily news-based Economic Policy Uncertainty index.

https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv

Access: public HTTPS download via `uv run python3 -m rebal.fetch.epu`.

## Downloaded (date)

2026-10-21.

## License class

Public, redistributable under the publisher's Creative Commons Attribution 4.0 notice. Store under `data/public/epu/`.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `epu` (`daily_policy_index`) | Index points | Index points |

## Transforms

Combine `year`, `month`, `day` into ISO `date`; rename `daily_policy_index` to `epu`. No scaling, interpolation or filling.

## Coverage

`All_Daily_Policy_Data.raw.csv` and `epu.csv`: 15,268 rows each, 1985-01-01 through 2026-10-20. Daily calendar dates; no gaps or missing values.

## Known problems

Recent observations can be revised. This is the US daily news index, not a monthly EPU series. Raw CSV bytes are unchanged.

## Paper datasets served (D-numbers)

D10. See `docs/contracts/daily_panel.md` for the downstream panel contract.
