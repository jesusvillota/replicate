# Source card: Hu–Pan–Wang Treasury noise

## Source and URL or WRDS table

Jun Pan's current faculty page: https://en.saif.sjtu.edu.cn/junpan/
The page links “Download the Noise Measure (updated to end-2025)” to
https://en.saif.sjtu.edu.cn/junpan/Noise_Measure_2025.xlsx.
Hu, Pan and Wang (2013), daily Treasury noise illiquidity measure.
Run `uv run python3 -m rebal.fetch.hpw`.

## Downloaded (date)

2026-10-21 (UTC), directly from Jun Pan's faculty site.

## License class

External storage; redistribution permission is unconfirmed. Neither the faculty
page nor the workbook supplies an explicit redistribution grant. Public access
alone does not establish that grant. As the task permits, keep both files in
`licensed_dir("hpw")`, outside git. This is a conservative storage choice,
not a claim that the authors prohibit redistribution.

Default paths: `~/data/replicate/licensed/hpw/Noise_Measure_2025.xlsx` (unchanged
workbook) and `~/data/replicate/licensed/hpw/noise.csv` (tidy data).
`REPLICATE_DATA_DIR` overrides the external root. No HPW data is committed in
`data/public/`. Another machine must run the fetcher before the stored-file test.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| Noise_bp | Basis points, Treasury yield-curve noise | Basis points, unchanged |

## Transforms

Read sheet `Noise Measure`, columns A:B (`Date`, `Noise_bp`). Other cells hold
publisher notes, not series. The Excel reader decodes native Excel dates;
date parsing also accepts the sheet's text dates. Rename `Date` to `date`
and sort. No winsorization, interpolation, return conversion or unit scaling.

## Coverage

Both files: **1987-01-02–2025-12-31**, **9,751 daily rows**.
Noise_bp has no missing values in those rows. Dates are unique. Nonpublished
days are not inserted. Observations exist at both core study endpoints,
1997-09-10 and 2023-03-17. Both files print an `OK` line with their coverage.

## Known problems

The workbook warns that occasional spikes reflect data-quality problems when
the four-standard-deviation mispricing filter misses extreme observations.
It cites 2024-06-03, when noise rose to 4.31 basis points because two outlier
bonds passed the filter. Preserve these published values without adjustment.
The current linked workbook stops at end-2025 and needs a new published version
for later dates. This measure differs from BofA GFSI Liquidity Risk.
TASK-012 chooses the proxy; this task only supplies and documents its inputs.

## Paper datasets served (D-numbers)

D26 (first-choice liquidity proxy candidate).
