# Source card: CFTC positioning

## Source and URL or WRDS table

Publisher: U.S. Commodity Futures Trading Commission (CFTC). Futures only.

- History index: https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
- Legacy annual ZIPs: `https://www.cftc.gov/files/dea/history/deacot<YYYY>.zip`, 1997–2026.
- TFF early history: https://www.cftc.gov/files/dea/history/fin_fut_txt_2006_2016.zip
- TFF annual ZIPs: `https://www.cftc.gov/files/dea/history/fut_fin_txt_<YYYY>.zip`, 2017–2026.
- LTPos page: https://www.cftc.gov/MarketReports/NetPositionChangesData/index.htm
- LTPos original CSV: https://www.cftc.gov/idc/groups/public/@marketreports/documents/file/lgtraderpos-csv.csv
- LTPos explanatory notes (live URL returned HTTP 403): https://www.cftc.gov/MarketReports/LgTraderExplanatory.html
- LTPos explanatory notes recovered through Wayback, HTTP 200: https://web.archive.org/web/20180413220527id_/https://www.cftc.gov/MarketReports/LgTraderExplanatory.html

The notes date the one-time LTPos release June 30, 2011. The data page and original CSV returned HTTP 200.

## Downloaded (date)

2026-10-21. `data/public/cftc/manifest.json` records each ZIP URL, byte size and SHA-256 hash, plus the LTPos URL and hash. No data came from a third-party mirror. Wayback supplied only the explanatory notes.

## License class

Public, redistributable U.S. government data. Store in `data/public/cftc/`.
The ZIPs and `lgtraderpos-csv.csv` are byte-for-byte downloads. Raw files contain all published markets; the tidy files contain only the requested markets. All files are below 20 MB.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| Legacy positions, open interest, weekly changes | Futures contracts | Unchanged |
| Legacy percentages and trader counts | Percent; traders | Unchanged |
| TFF positions, open interest, weekly changes | Futures contracts | Unchanged |
| TFF percentages and trader counts | Percent; traders | Unchanged |
| LTPos group buys and sells | Weekly mean of daily changes, contracts per day | Unchanged |
| LTPos group directional net change | Buys minus sells, contracts per day | Contracts per day |
| LTPos aggregate changes and trade volume | Weekly mean, contracts per day | Unchanged |

Legacy COT supports the paper's **commercial / non-commercial** split. TFF and LTPos support the **asset managers / leveraged funds** split. Dealer intermediaries and other reportables remain separate groups in TFF and LTPos.

Legacy and TFF retain every published column. Their first two columns are added `date` and `market_code`. Market codes are text: `043602` (10-year Treasury), `138741` (full-size S&P 500), and `13874A` (E-mini S&P 500). Names were checked against these codes in the archives.

LTPos retains Treasury contracts TU (2-year), FB (5-year), TY (10-year), US (T-bond), and equity contracts SP (S&P 500) and ES (E-mini). Fed funds and Eurodollar are excluded. Its first three columns are `date` (week ending), `market`, and `period_start`. The four groups each have `_buys`, `_sells`, and `_net_change` columns. The final columns preserve the published aggregate and trade volume.

## Transforms

Run `uv run python3 -m rebal.fetch.cftc`. `--end-year 2023` restricts the tidy history to the replication sample. The default includes the current archive year. Completed ZIPs are cached; the current-year ZIPs refresh each run. `--refresh` downloads all sources again. No cluster is used.

Legacy uses annual archives, including 1997–2016. The redundant multi-year archive `https://www.cftc.gov/files/dea/history/deacot1986_2016.zip` was tested and is available (22,917,634 bytes). It exceeds the task's per-file limit. Annual archives provide the same requested early years within that limit, without splitting or altering an original archive.

CSV ingestion preserves published text values, including leading zeros. Header whitespace is stripped to align an old trailing-space header with later archives. Original headers and values remain in the raw ZIPs. Added dates use ISO format; original date fields remain. TFF's early archive has timestamp-style dates, handled explicitly. Rows sort by date and market. Duplicate date/market keys, missing required years, unexpected schemas and incorrect code/name pairs fail validation. No date is fabricated or interpolated.

LTPos's wide, three-row header is reshaped to one row per market and week. Published buys and sells are positive magnitudes. Directional net change is `buys - sells`, computed from the published rounded figures. This is a flow, not a position level. The separate source aggregate is `(sum(buys) + sum(sells)) / 2`, subject to rounding; it must not be read as the signed directional net change. No scale conversion is applied.

## Coverage

| File | First date | Last date | Rows | Frequency |
|---|---|---|---|---|
| `cot_legacy.csv` | 1997-01-07 | 2026-10-13 | 4,316 | Weekly per market |
| `tff.csv` | 2006-06-13 | 2026-10-13 | 2,882 | Weekly per market |
| `ltpos.csv` | 2009-01-09 | 2011-05-27 | 750 | 125 weeks × six markets |

LTPos's first period starts 2009-01-05. Each market has all 125 periods. Legacy has 131 columns: 129 original plus two added columns. TFF has 89: 87 original plus two added columns. LTPos has 17.

## Known problems

- The full-size S&P contract (`138741`) stops in both history files at 2021-09-14. Legacy has 1,248 rows for it; TFF has 758. It has reporting gaps near the end of its life. No later rows are inserted.
- Legacy E-mini starts 1997-09-16. Early gaps over 14 days end at 1998-01-13 and 1998-10-06. The 10-year Treasury has continuous weekly observations. Both continuing contracts have every requested year through 2023 and onward to the current archive.
- Recent data can be revised by the CFTC. SHA-256 hashes identify this download. The current-year archive is incomplete by definition.
- LTPos is a one-time release. Its changes can include option exercises, delivery, expiry, and related position adjustments. They are not pure executed trade volume. Each weekly value is a mean of daily trader-level changes, not the change between two weekly COT observations.
- The exact column spelling differs between legacy and TFF. Use the original source headers when selecting trader fields. CSV readers must specify text dtype for codes to preserve `043602`.

## Paper datasets served (D-numbers)

D19 (legacy COT and TFF); D20 (LTPos). The data supports later Figure 5 work. No Q measure, correlation, or unit conversion is computed here.
