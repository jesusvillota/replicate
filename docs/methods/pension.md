# Figure 1: Public pension equity allocations

Use the output schema in [the exhibits contract](../contracts/exhibits.md).
The source is [CRR Public Plans Data (PPD)](../data/cards/ppd.md), downloaded
on 2026-10-22. The default sample is fiscal years 2003–2022, inclusive.
Fiscal years are labels. They do not imply that all plans report on December 31.

## Equity definition and weighting

Public equity is `EQTotal_Actl` for actual allocations and `EQTotal_Trgt`
for targets. These are the PPD total equity fields. Private equity has
separate `PETotal_Actl` and `PETotal_Trgt` fields and is excluded.
Do not add domestic, international or global components to these totals.
The components are incomplete and could duplicate totals.
The published numbers are fractions: `0.65` means 65%. No conversion is applied.

For each year and each series, compute `sum(assets * share) / sum(assets)`
over eligible plans. Assets are `MktAssets_net`, the fiscal year-end net
market value in USD thousands. The asset unit cancels in this ratio.
These are asset-weighted means, with separate denominators for actual and target.
There are no lagged weights and no fixed or balanced plan sample.
The paper does not provide enough detail to recover its precise sample or weights.
The task requires asset weights. `--weighting equal` exposes a sensitivity check.

`actual_min` and `actual_max` are the minimum and maximum annual actual mean.
`target_typical` is the median annual target mean. For 20 years, it is
the average of the tenth and eleventh sorted values.
Each year has equal weight in this median.

## Missing-field rules

- Exclude missing actual values from the actual mean only.
- Exclude missing target values from the target mean only.
- Keep reported zero shares. Do not replace them with missing values.
- With asset weights, exclude missing, nonfinite, zero or negative assets from both means.
- With equal weights, assets are not required. Keep the asset quality count for reference.
- Never fill allocations, assets or annual means. Never carry targets between years.
- Reject duplicate plan-year keys, missing keys, noninteger keys and shares outside `[0, 1]`.
- Keep years with no eligible plans as missing means, with zero contributing counts.
  The plot shows gaps. Summary statistics omit these missing annual means.
  If an entire series is missing, its summary value is missing too.

## Counts and changing coverage

`figure_1_yearly.csv` records `fy`, `plan_count`, `actual_plan_count`,
`target_plan_count`, `actual_missing_count`, `target_missing_count`,
`invalid_assets_count`, `actual_share`, and `target_share`.
Shares are fractions. Counts are numbers of plans, not asset totals.
The missing-field counts include all rows, even rows with invalid assets.
Thus missing-field and invalid-asset counts can overlap.
The two contributing counts apply both the share and weight rules.

The loader checks row counts against `ppd_coverage.csv` before computing means.
The current source has 253 plan rows each year, including rows with missing fields.
The contributing samples change over time. Changes in the aggregate can therefore
reflect plan coverage, asset weights and allocations. They do not isolate rebalancing
by a fixed group of plans.

The real-data smoke check in TASK-027 produced these counts under asset weights:

| Fiscal year | All plans | Actual contributors | Target contributors | Missing actual | Missing target | Invalid assets |
|---|---:|---:|---:|---:|---:|---:|
| 2003 | 253 | 172 | 136 | 79 | 117 | 17 |
| 2004 | 253 | 179 | 149 | 72 | 104 | 15 |
| 2005 | 253 | 183 | 161 | 68 | 90 | 12 |
| 2006 | 253 | 191 | 166 | 62 | 87 | 8 |
| 2007 | 253 | 197 | 174 | 56 | 79 | 6 |
| 2008 | 253 | 198 | 175 | 55 | 78 | 4 |
| 2009 | 253 | 203 | 180 | 50 | 73 | 5 |
| 2010 | 253 | 201 | 187 | 52 | 66 | 5 |
| 2011 | 253 | 208 | 190 | 45 | 63 | 4 |
| 2012 | 253 | 209 | 192 | 44 | 61 | 3 |
| 2013 | 253 | 214 | 196 | 39 | 57 | 2 |
| 2014 | 253 | 211 | 213 | 42 | 40 | 2 |
| 2015 | 253 | 212 | 218 | 40 | 35 | 5 |
| 2016 | 253 | 215 | 221 | 38 | 32 | 4 |
| 2017 | 253 | 224 | 227 | 29 | 26 | 4 |
| 2018 | 253 | 226 | 231 | 27 | 22 | 4 |
| 2019 | 253 | 224 | 230 | 28 | 22 | 6 |
| 2020 | 253 | 225 | 229 | 28 | 24 | 5 |
| 2021 | 253 | 228 | 232 | 25 | 21 | 5 |
| 2022 | 253 | 228 | 234 | 25 | 19 | 5 |

## Outputs and reproduction

```sh
uv run python3 -m rebal.exhibits --all --demo --only figure_1
uv run python3 -m rebal.exhibits.pension --demo --weighting equal
uv run python3 -m rebal.exhibits.pension --demo --start 2005 --end latest
```

`--end` accepts a fiscal year, an ISO date (using its year), or `latest`.
`latest` means the latest fiscal year in the allocation source, currently 2022.
The demo fixture also ends in 2022.

Demo files go to `output/demo/`. Real files go to `output/figures/`.
`figure_1.csv` has exactly the comparison columns `exhibit,column,term,stat,value`.
Its three keys match `docs/results/targets.csv`: `figure_1,equity_share`,
terms `actual_min`, `actual_max`, `target_typical`, and stat `value`.
`figure_1_yearly.csv` contains the exact series plotted in `figure_1.pdf`.
`pension.metadata.json` records inputs, parameters, units, time and output names.
Subsequent runs overwrite these files. Separate runs are needed for sensitivity checks.

The shared `rebal.demo` and `rebal.io` fixtures contain daily returns and signals,
not pension allocations. This module uses its own deterministic, synthetic pension
fixture to keep shared files unchanged. It has unequal assets, changing coverage,
missing targets and a planted annual actual-target gap of plus or minus 0.025.
The demo is not evidence about real pension allocations.

The real smoke values are about 0.412023, 0.619532 and 0.483315.
The paper values are about 0.63, 0.68 and 0.65.
These differ substantially. No field, weight or sample was changed to fit the paper.
TASK-030 must report this gap and investigate sample or source-vintage differences.
This task commits no real exhibit outputs.
