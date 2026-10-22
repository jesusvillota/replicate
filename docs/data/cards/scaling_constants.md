# Source card: dollar-scaling constants

Status: available (dated paper constants)

## Source and storage

D27 uses constants transcribed from paper pp. 21–23 and footnotes 19 and 21.
The source references are:

- [Federal Reserve Financial Accounts](https://www.federalreserve.gov/releases/z1/):
  $37.8T retirement assets at year-end 2022.
- [CRS R47699](https://crsreports.congress.gov/product/pdf/R/R47699):
  public/private plan and IRA allocations supporting the rounded $20T base.
- [Survey of Consumer Finances](https://www.federalreserve.gov/econres/scfindex.htm):
  approximately two-thirds household participation.
- [Census household tables](https://www.census.gov/data/tables/time-series/demo/families/households.html):
  approximately 127M households in 2022.
- [ICI 2025 Q2](https://www.ici.org/statistical-report/ret_25_q2):
  $45.8T retirement assets at 2025-06-30, for the paper's growth discussion only.

No report files were downloaded. References and calculations are stored in
[cost methods](../../methods/costs.md) and `src/rebal/exhibits/costs.py`.
These public reference links do not create a raw data directory.

## Transforms and limits

Dollar loss is annual basis points divided by 10,000, times the asset base.
Household loss divides by `(2/3) * 127,000,000`. Keep the paper's rounded values.
They describe specific dates and are not current estimates. The $37.8T base
includes more assets than the rounded $20T public equity/debt estimate.
