# Paper comparison

## Summary

- Targets matched: 388/399
- Sign-match rate: 92.5% (196/212 eligible targets)
- Significance-match rate: 83.1% (123/148 eligible targets)
- Missing exhibits: figure_6, figure_D5
- Matched exhibits: costs, figure_1, figure_2, figure_3, figure_4, figure_5, figure_D1, figure_D2, figure_D3, figure_D4, table_1, table_2a, table_2b, table_3, table_4, table_5, table_6a, table_6b, table_6c, table_C1, table_C2, table_D1, table_D10, table_D11, table_D12, table_D14, table_D3, table_D4, table_D6, table_D7, table_D8, table_D9
- Skipped CSVs: 18
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_1_yearly.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_2.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_3.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_4.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_6.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_C1.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_D1.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_D2.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_D3.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_D4.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures/figure_D5.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/costs.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/table_6a.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/table_6b.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/table_6c.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/table_D13.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/table_D2.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables/table_D5.csv: no matching target keys

Targets: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/docs/results/targets.csv`. Inputs: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables`, `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures`.

Each row compares one statistic. Approximate chart readings have a `~` prefix. Sign checks apply to coef, t and value. Significance checks apply to coef and t, using |t| ≥ 1.96 on both sides (or neither). Where t is absent, coef/se is used. N/A means missing data, an inapplicable check, or division by zero. Missing exhibits have no matched numeric targets; partial exhibits retain N/A rows.

## costs

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| calendar: annual_bps [value] | 5 | 3.33281 | 0.666561 | yes | N/A |
| headline: annual_bps [value] | 8 | 1.22151 | 0.152689 | yes | N/A |
| headline: annual_usd [value] | 1.6e+10 | 2.44303e+09 | 0.152689 | yes | N/A |
| household: annual_usd [value] | 200 | 28.8547 | 0.144273 | yes | N/A |
| random: annual_bps [value] | 0.6 | N/A | N/A | N/A | N/A |
| threshold: annual_max_bps [value] | 27 | 6.56819 | 0.243266 | yes | N/A |
| threshold: annual_mean_bps [value] | 15 | -5.55416 | -0.370277 | no | N/A |
| threshold: annual_min_bps [value] | 6 | -18.5702 | -3.09504 | no | N/A |
| threshold: annual_one_pct_trade_bps [value] | 11 | -0.889777 | -0.0808888 | no | N/A |

## figure_1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| equity_share: actual_max [value] | ~0.68 | 0.619532 | 0.911076 | yes | N/A |
| equity_share: actual_min [value] | ~0.63 | 0.412023 | 0.654005 | yes | N/A |
| equity_share: target_typical [value] | ~0.65 | 0.483315 | 0.743561 | yes | N/A |

## figure_2

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| delta_0.0_pct: threshold [t] | ~-3.8 | -3.62997 | 0.955256 | yes | yes |
| delta_1.0_pct: threshold [t] | ~-4.2 | -4.22201 | 1.00524 | yes | yes |
| delta_1.8_pct: threshold [t] | ~-4.3 | -3.94458 | 0.917344 | yes | yes |
| summary: one_pct_weakening_delta_pct [value] | ~2.7 | 1.4 | 0.518519 | yes | N/A |

## figure_3

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| days_1: calendar_interaction [t] | ~-0.85 | 2.08786 | -2.4563 | no | no |
| days_10: calendar_interaction [t] | ~-0.1 | 0.0755611 | -0.755611 | no | yes |
| days_2: calendar_interaction [t] | ~-1.15 | 0.984378 | -0.855981 | no | yes |
| days_3: calendar_interaction [t] | ~-1 | 0.323106 | -0.323106 | no | yes |
| days_4: calendar_interaction [t] | ~-3.1 | 0.00206371 | -0.000665714 | no | no |
| days_5: calendar_interaction [t] | ~-2.8 | -2.45407 | 0.876454 | yes | yes |
| days_6: calendar_interaction [t] | ~-2.4 | -1.98411 | 0.826711 | yes | yes |
| days_7: calendar_interaction [t] | ~-1.35 | -1.90806 | 1.41338 | yes | yes |
| days_8: calendar_interaction [t] | ~-1 | -1.19001 | 1.19001 | yes | yes |
| days_9: calendar_interaction [t] | ~-0.5 | -0.360719 | 0.721437 | yes | yes |

## figure_4

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| day_15: calendar:week4 [coef] | ~-0.13 | 0.252764 | -1.94434 | no | N/A |
| day_15: threshold [coef] | ~-0.12 | -0.801446 | 6.67872 | yes | N/A |
| day_2: calendar:week4 [coef] | ~-0.52 | -0.283967 | 0.546091 | yes | N/A |
| day_4: threshold [coef] | ~-0.95 | -0.987082 | 1.03903 | yes | N/A |
| summary: calendar_week4_first_insignificant_day [value] | ~6 | 3 | 0.5 | yes | N/A |
| summary: threshold_first_insignificant_day [value] | ~9 | 7 | 0.777778 | yes | N/A |

## figure_5

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| ancerno: calendar [value] | ~-0.1 | N/A | N/A | N/A | N/A |
| ancerno: threshold [value] | ~-0.1 | N/A | N/A | N/A | N/A |
| cftc_hedgers: calendar [value] | ~-0.13 | -0.128595 | 0.98919 | yes | N/A |
| cftc_hedgers: threshold [value] | ~-0.1 | -0.0897218 | 0.897218 | yes | N/A |
| cftc_speculators: calendar [value] | ~0.17 | 0.153255 | 0.9015 | yes | N/A |
| cftc_speculators: threshold [value] | ~0.11 | 0.0940242 | 0.854765 | yes | N/A |
| ici: calendar [value] | ~-0.19 | -0.174532 | 0.91859 | yes | N/A |
| ici: threshold [value] | ~-0.17 | -0.0446147 | 0.262439 | yes | N/A |
| ltpos_asset_managers: calendar [value] | ~-0.12 | -0.04124 | 0.343667 | yes | N/A |
| ltpos_asset_managers: threshold [value] | ~-0.08 | -0.0218508 | 0.273135 | yes | N/A |
| ltpos_leveraged_funds: calendar [value] | ~0.13 | 0.0890576 | 0.685058 | yes | N/A |
| ltpos_leveraged_funds: threshold [value] | ~0.18 | 0.0187796 | 0.104331 | yes | N/A |

## figure_6

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| sample_end: sp500 [value] | ~2.3 | N/A | N/A | N/A | N/A |
| sample_end: strategy [value] | ~6.2 | N/A | N/A | N/A | N/A |

## figure_D1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| delta_1.8_pct: threshold [t] | ~-4.5 | -3.73356 | 0.829681 | yes | yes |

## figure_D2

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| days_4: calendar_interaction [t] | ~-3.65 | 0.00249157 | -0.000682621 | no | no |

## figure_D3

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| delta_0.0_pct: during_rebalancing [t] | ~-3.8 | -3.62997 | 0.955256 | yes | yes |
| delta_0.3_pct: outside_rebalancing [t] | ~2.5 | 1.01573 | 0.406292 | yes | no |
| delta_1.8_pct: during_rebalancing [t] | ~-6.1 | -4.58305 | 0.751319 | yes | yes |
| delta_2.3_pct: outside_rebalancing [t] | ~-3 | -1.92976 | 0.643252 | yes | no |

## figure_D4

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| day_1: calendar:week4 [coef] | ~-0.3 | -0.260256 | 0.867519 | yes | N/A |
| day_1: threshold [coef] | ~-0.42 | -0.464414 | 1.10575 | yes | N/A |
| day_2: calendar:week4 [coef] | ~-0.2 | -0.0164074 | 0.0820371 | yes | N/A |
| day_2: threshold [coef] | ~-0.2 | -0.193701 | 0.968504 | yes | N/A |

## figure_D5

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| random: ci95_high_bps [value] | ~3.2 | N/A | N/A | N/A | N/A |
| random: ci95_low_bps [value] | ~-4.6 | N/A | N/A | N/A | N/A |
| random: mean_bps [value] | -0.6 | N/A | N/A | N/A | N/A |

## table_1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar [coef] | 0.0553 | 0.0593131 | 1.07257 | yes | yes |
| 1: calendar [se] | 0.0709 | 0.0609854 | 0.86016 | N/A | N/A |
| 1: calendar:week4 [coef] | -0.3029 | -0.260256 | 0.859214 | yes | yes |
| 1: calendar:week4 [se] | 0.0808 | 0.0761273 | 0.942169 | N/A | N/A |
| 1: calendar:week4 [value] | -19.2 | -16.7609 | 0.872966 | yes | N/A |
| 1: momentum [coef] | 0.0023 | 0.00237626 | 1.03316 | yes | yes |
| 1: momentum [se] | 0.0006 | 0.000585765 | 0.976275 | N/A | N/A |
| 1: ret [coef] | -0.0203 | -0.00653488 | 0.321915 | yes | yes |
| 1: ret [se] | 0.0289 | 0.0280405 | 0.970261 | N/A | N/A |
| 1: threshold [adj_r2] | 0.0239 | 0.0201099 | 0.84142 | N/A | N/A |
| 1: threshold [coef] | -0.4144 | -0.464414 | 1.12069 | yes | yes |
| 1: threshold [nobs] | 6226 | 6317 | 1.01462 | N/A | N/A |
| 1: threshold [se] | 0.1148 | 0.115753 | 1.0083 | N/A | N/A |
| 1: threshold [value] | -20 | -22.1274 | 1.10637 | yes | N/A |
| 1: week4 [coef] | 0.0002 | 0.000654251 | 3.27125 | yes | yes |
| 1: week4 [se] | 0.0004 | 0.000436887 | 1.09222 | N/A | N/A |
| 2: calendar [coef] | 0.0689 | 0.0917961 | 1.33231 | yes | yes |
| 2: calendar [se] | 0.0686 | 0.0659197 | 0.960929 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.3036 | -0.280219 | 0.922988 | yes | yes |
| 2: calendar:week4 [se] | 0.0808 | 0.0915561 | 1.13312 | N/A | N/A |
| 2: momentum [coef] | 0.0024 | 0.0019281 | 0.803373 | yes | yes |
| 2: momentum [se] | 0.0007 | 0.000761193 | 1.08742 | N/A | N/A |
| 2: move [coef] | -0.002 | -0.0028613 | 1.43065 | yes | no |
| 2: move [se] | 0.0011 | 0.00107224 | 0.974762 | N/A | N/A |
| 2: ret [coef] | -0.0167 | -0.0253512 | 1.51804 | yes | yes |
| 2: ret [se] | 0.0289 | 0.0328591 | 1.13699 | N/A | N/A |
| 2: threshold [adj_r2] | 0.0252 | 0.0255585 | 1.01423 | N/A | N/A |
| 2: threshold [coef] | -0.4208 | -0.454239 | 1.07947 | yes | yes |
| 2: threshold [nobs] | 6226 | 5043 | 0.80999 | N/A | N/A |
| 2: threshold [se] | 0.1164 | 0.134813 | 1.15819 | N/A | N/A |
| 2: vix [coef] | 0.009 | 0.00785299 | 0.872554 | yes | yes |
| 2: vix [se] | 0.0053 | 0.00602233 | 1.13629 | N/A | N/A |
| 2: week4 [coef] | 0.0002 | 0.000909721 | 4.5486 | yes | yes |
| 2: week4 [se] | 0.0004 | 0.000494108 | 1.23527 | N/A | N/A |
| 3: ads [coef] | 0 | 3.49089e-05 | N/A | no | yes |
| 3: ads [se] | 0.0002 | 0.000206386 | 1.03193 | N/A | N/A |
| 3: calendar [coef] | 0.0572 | 0.0614874 | 1.07495 | yes | yes |
| 3: calendar [se] | 0.0696 | 0.0594965 | 0.854834 | N/A | N/A |
| 3: calendar:week4 [coef] | -0.3026 | -0.260699 | 0.861529 | yes | yes |
| 3: calendar:week4 [se] | 0.0805 | 0.0756538 | 0.939798 | N/A | N/A |
| 3: epu [coef] | 0.0005 | 5.28049e-06 | 0.010561 | yes | yes |
| 3: epu [se] | 0.0003 | 2.74594e-06 | 0.00915312 | N/A | N/A |
| 3: momentum [coef] | 0.0024 | 0.00248461 | 1.03526 | yes | yes |
| 3: momentum [se] | 0.0006 | 0.000600722 | 1.0012 | N/A | N/A |
| 3: ret [coef] | -0.0198 | -0.00639189 | 0.322823 | yes | yes |
| 3: ret [se] | 0.0281 | 0.0277158 | 0.986328 | N/A | N/A |
| 3: threshold [adj_r2] | 0.0243 | 0.0206265 | 0.848826 | N/A | N/A |
| 3: threshold [coef] | -0.4254 | -0.475037 | 1.11668 | yes | yes |
| 3: threshold [nobs] | 6226 | 6317 | 1.01462 | N/A | N/A |
| 3: threshold [se] | 0.1098 | 0.113086 | 1.02993 | N/A | N/A |
| 3: week4 [coef] | 0.0002 | 0.000647285 | 3.23643 | yes | yes |
| 3: week4 [se] | 0.0004 | 0.0004366 | 1.0915 | N/A | N/A |
| 4: calendar [coef] | 0.0542 | 0.0585601 | 1.08044 | yes | yes |
| 4: calendar [se] | 0.0713 | 0.0613237 | 0.86008 | N/A | N/A |
| 4: calendar:week4 [coef] | -0.3032 | -0.260844 | 0.860302 | yes | yes |
| 4: calendar:week4 [se] | 0.0806 | 0.0759123 | 0.941841 | N/A | N/A |
| 4: momentum [coef] | 0.0025 | 0.0025109 | 1.00436 | yes | yes |
| 4: momentum [se] | 0.0006 | 0.000604824 | 1.00804 | N/A | N/A |
| 4: ret [coef] | -0.0192 | -0.00601297 | 0.313176 | yes | yes |
| 4: ret [se] | 0.0287 | 0.0279392 | 0.97349 | N/A | N/A |
| 4: sentiment [coef] | -0.0016 | -0.00116131 | 0.725816 | yes | yes |
| 4: sentiment [se] | 0.0012 | 0.00120756 | 1.0063 | N/A | N/A |
| 4: threshold [adj_r2] | 0.0242 | 0.0201886 | 0.834241 | N/A | N/A |
| 4: threshold [coef] | -0.4254 | -0.471351 | 1.10802 | yes | yes |
| 4: threshold [nobs] | 6226 | 6317 | 1.01462 | N/A | N/A |
| 4: threshold [se] | 0.1133 | 0.114615 | 1.01161 | N/A | N/A |
| 4: week4 [coef] | 0.0002 | 0.000654947 | 3.27474 | yes | yes |
| 4: week4 [se] | 0.0004 | 0.000436749 | 1.09187 | N/A | N/A |
| 5: ads [coef] | 0.0001 | 1.07136e-05 | 0.107136 | yes | yes |
| 5: ads [se] | 0.0002 | 0.000207615 | 1.03808 | N/A | N/A |
| 5: calendar [coef] | 0.0666 | 0.092637 | 1.39095 | yes | yes |
| 5: calendar [se] | 0.0686 | 0.0666326 | 0.97132 | N/A | N/A |
| 5: calendar:week4 [coef] | -0.3033 | -0.280151 | 0.923675 | yes | yes |
| 5: calendar:week4 [se] | 0.0808 | 0.0915389 | 1.13291 | N/A | N/A |
| 5: epu [coef] | 0.0002 | 9.82324e-07 | 0.00491162 | yes | yes |
| 5: epu [se] | 0.0004 | 4.00876e-06 | 0.0100219 | N/A | N/A |
| 5: momentum [coef] | 0.0024 | 0.00190609 | 0.794204 | yes | yes |
| 5: momentum [se] | 0.0007 | 0.000761219 | 1.08746 | N/A | N/A |
| 5: move [coef] | -0.0019 | -0.00279462 | 1.47085 | yes | no |
| 5: move [se] | 0.0011 | 0.0011551 | 1.05009 | N/A | N/A |
| 5: ret [coef] | -0.0173 | -0.0256826 | 1.48455 | yes | yes |
| 5: ret [se] | 0.0286 | 0.0327021 | 1.14343 | N/A | N/A |
| 5: sentiment [coef] | -0.0003 | 0.000389999 | -1.3 | no | yes |
| 5: sentiment [se] | 0.0013 | 0.001572 | 1.20923 | N/A | N/A |
| 5: threshold [adj_r2] | 0.0248 | 0.0250033 | 1.0082 | N/A | N/A |
| 5: threshold [coef] | -0.4226 | -0.453113 | 1.0722 | yes | yes |
| 5: threshold [nobs] | 6226 | 5043 | 0.80999 | N/A | N/A |
| 5: threshold [se] | 0.1139 | 0.133549 | 1.17251 | N/A | N/A |
| 5: vix [coef] | 0.0076 | 0.00789532 | 1.03886 | yes | yes |
| 5: vix [se] | 0.0062 | 0.00854751 | 1.37863 | N/A | N/A |
| 5: week4 [coef] | 0.0002 | 0.000907458 | 4.53729 | yes | yes |
| 5: week4 [se] | 0.0004 | 0.000494053 | 1.23513 | N/A | N/A |

## table_2a

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar [coef] | -0.0778 | -0.0514901 | 0.661826 | yes | yes |
| 1: calendar [se] | 0.0582 | 0.0548035 | 0.94164 | N/A | N/A |
| 1: threshold [adj_r2] | 0.013 | 0.0117359 | 0.902759 | N/A | N/A |
| 1: threshold [coef] | -0.3281 | -0.368398 | 1.12282 | yes | yes |
| 1: threshold [nobs] | 6226 | 6317 | 1.01462 | N/A | N/A |
| 1: threshold [se] | 0.1113 | 0.11239 | 1.00979 | N/A | N/A |
| 2: calendar [coef] | 0.0553 | 0.0593131 | 1.07257 | yes | yes |
| 2: calendar [se] | 0.0709 | 0.0609854 | 0.86016 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.3029 | -0.260256 | 0.859214 | yes | yes |
| 2: calendar:week4 [se] | 0.0808 | 0.0761273 | 0.942169 | N/A | N/A |
| 2: threshold [adj_r2] | 0.0239 | 0.0201099 | 0.84142 | N/A | N/A |
| 2: threshold [coef] | -0.4144 | -0.464414 | 1.12069 | yes | yes |
| 2: threshold [nobs] | 6226 | 6317 | 1.01462 | N/A | N/A |
| 2: threshold [se] | 0.1148 | 0.115753 | 1.0083 | N/A | N/A |
| 3: calendar [coef] | 0.0735 | 0.0708831 | 0.964396 | yes | yes |
| 3: calendar [se] | 0.0749 | 0.0646402 | 0.86302 | N/A | N/A |
| 3: calendar:week4 [coef] | -0.3511 | -0.289924 | 0.825758 | yes | yes |
| 3: calendar:week4 [se] | 0.0963 | 0.0922901 | 0.95836 | N/A | N/A |
| 3: threshold [adj_r2] | 0.0244 | 0.0202242 | 0.828862 | N/A | N/A |
| 3: threshold [coef] | -0.4789 | -0.505706 | 1.05597 | yes | yes |
| 3: threshold [nobs] | 6226 | 6317 | 1.01462 | N/A | N/A |
| 3: threshold [se] | 0.1308 | 0.127935 | 0.9781 | N/A | N/A |
| 3: threshold:week4 [coef] | 0.2137 | 0.139613 | 0.653315 | yes | yes |
| 3: threshold:week4 [se] | 0.162 | 0.170783 | 1.05422 | N/A | N/A |

## table_2b

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.2509 | -0.409862 | 1.63357 | yes | no |
| 1: calendar:week4 [se] | 0.159 | 0.13501 | 0.849122 | N/A | N/A |
| 1: threshold [adj_r2] | 0.011 | 0.0311895 | 2.83541 | N/A | N/A |
| 1: threshold [coef] | -0.2723 | -0.351894 | 1.2923 | yes | yes |
| 1: threshold [nobs] | 2078 | 2087 | 1.00433 | N/A | N/A |
| 1: threshold [se] | 0.2075 | 0.203393 | 0.980206 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.3487 | -0.120561 | 0.345745 | yes | no |
| 2: calendar:week4 [se] | 0.1062 | 0.107317 | 1.01052 | N/A | N/A |
| 2: threshold [adj_r2] | 0.0234 | 0.00783728 | 0.334927 | N/A | N/A |
| 2: threshold [coef] | -0.4153 | -0.299747 | 0.721759 | yes | no |
| 2: threshold [nobs] | 2052 | 2063 | 1.00536 | N/A | N/A |
| 2: threshold [se] | 0.1666 | 0.197734 | 1.18688 | N/A | N/A |
| 3: calendar:week4 [coef] | -0.34 | -0.186251 | 0.547797 | yes | no |
| 3: calendar:week4 [se] | 0.13 | 0.123267 | 0.948211 | N/A | N/A |
| 3: threshold [adj_r2] | 0.0469 | 0.0368088 | 0.784836 | N/A | N/A |
| 3: threshold [coef] | -0.5845 | -0.714395 | 1.22223 | yes | yes |
| 3: threshold [nobs] | 2097 | 2167 | 1.03338 | N/A | N/A |
| 3: threshold [se] | 0.2083 | 0.199425 | 0.957392 | N/A | N/A |

## table_3

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar [coef] | 0.0424 | 0.0584386 | 1.37827 | yes | yes |
| 1: calendar [se] | 0.0665 | 0.0584191 | 0.878483 | N/A | N/A |
| 1: calendar:week4 [coef] | -0.2667 | -0.245028 | 0.918742 | yes | yes |
| 1: calendar:week4 [se] | 0.0758 | 0.0709687 | 0.936263 | N/A | N/A |
| 1: calendar:week4 [value] | -16.9 | -15.7803 | 0.933744 | yes | N/A |
| 1: momentum [coef] | 0.0018 | 0.00173518 | 0.96399 | yes | yes |
| 1: momentum [se] | 0.0005 | 0.000530167 | 1.06033 | N/A | N/A |
| 1: ret [coef] | -0.0223 | -0.0144981 | 0.650138 | yes | yes |
| 1: ret [se] | 0.0264 | 0.0252939 | 0.958101 | N/A | N/A |
| 1: threshold [adj_r2] | 0.0225 | 0.0207898 | 0.92399 | N/A | N/A |
| 1: threshold [coef] | -0.3302 | -0.368583 | 1.11624 | yes | yes |
| 1: threshold [nobs] | 6223 | 6317 | 1.01511 | N/A | N/A |
| 1: threshold [se] | 0.1062 | 0.106655 | 1.00428 | N/A | N/A |
| 1: threshold [value] | -15.9 | -17.5615 | 1.10449 | yes | N/A |
| 1: week4 [coef] | 0.0005 | 0.000977248 | 1.9545 | yes | no |
| 1: week4 [se] | 0.0004 | 0.000386855 | 0.967138 | N/A | N/A |
| 2: calendar [coef] | 0.0441 | 0.0907044 | 2.05679 | yes | yes |
| 2: calendar [se] | 0.0645 | 0.0636823 | 0.987322 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.2671 | -0.272857 | 1.02155 | yes | yes |
| 2: calendar:week4 [se] | 0.0762 | 0.08516 | 1.11759 | N/A | N/A |
| 2: momentum [coef] | 0.0018 | 0.00130648 | 0.725822 | yes | no |
| 2: momentum [se] | 0.0006 | 0.000693274 | 1.15546 | N/A | N/A |
| 2: ret [coef] | 0.003 | -0.0319598 | -10.6533 | no | yes |
| 2: ret [se] | 0.043 | 0.0295942 | 0.688237 | N/A | N/A |
| 2: threshold [adj_r2] | 0.0242 | 0.0273245 | 1.12911 | N/A | N/A |
| 2: threshold [coef] | -0.3261 | -0.346917 | 1.06384 | yes | yes |
| 2: threshold [nobs] | 6223 | 5043 | 0.810381 | N/A | N/A |
| 2: threshold [se] | 0.1049 | 0.123111 | 1.1736 | N/A | N/A |
| 2: week4 [coef] | 0.0005 | 0.00121732 | 2.43464 | yes | no |
| 2: week4 [se] | 0.0004 | 0.000434416 | 1.08604 | N/A | N/A |
| 3: calendar [coef] | -0.0129 | -0.000874457 | 0.0677874 | yes | yes |
| 3: calendar [se] | 0.0116 | 0.010048 | 0.866211 | N/A | N/A |
| 3: calendar:week4 [coef] | 0.0362 | 0.0152273 | 0.420644 | yes | no |
| 3: calendar:week4 [se] | 0.0128 | 0.012337 | 0.96383 | N/A | N/A |
| 3: calendar:week4 [value] | 2.3 | 0.980667 | 0.426377 | yes | N/A |
| 3: momentum [coef] | -0.0005 | -0.000641076 | 1.28215 | yes | yes |
| 3: momentum [se] | 0.0001 | 0.00013487 | 1.3487 | N/A | N/A |
| 3: ret [coef] | -0.002 | -0.00796321 | 3.9816 | yes | yes |
| 3: ret [se] | 0.0065 | 0.00630868 | 0.970566 | N/A | N/A |
| 3: threshold [adj_r2] | 0.0078 | 0.00647432 | 0.83004 | N/A | N/A |
| 3: threshold [coef] | 0.0842 | 0.0958319 | 1.13815 | yes | yes |
| 3: threshold [nobs] | 6223 | 6317 | 1.01511 | N/A | N/A |
| 3: threshold [se] | 0.0269 | 0.0269862 | 1.00321 | N/A | N/A |
| 3: threshold [value] | 4.1 | 4.566 | 1.11366 | yes | N/A |
| 3: week4 [coef] | 0.0004 | 0.000322997 | 0.807493 | yes | yes |
| 3: week4 [se] | 0.0001 | 0.000114725 | 1.14725 | N/A | N/A |
| 4: calendar [coef] | -0.0148 | -0.00193262 | 0.130583 | yes | yes |
| 4: calendar [se] | 0.0113 | 0.0115526 | 1.02235 | N/A | N/A |
| 4: calendar:week4 [coef] | 0.0372 | 0.00729388 | 0.196072 | yes | no |
| 4: calendar:week4 [se] | 0.0127 | 0.0144962 | 1.14143 | N/A | N/A |
| 4: momentum [coef] | -0.0005 | -0.00059961 | 1.19922 | yes | yes |
| 4: momentum [se] | 0.0001 | 0.000162613 | 1.62613 | N/A | N/A |
| 4: ret [coef] | -0.0027 | -0.0062772 | 2.32489 | yes | yes |
| 4: ret [se] | 0.0093 | 0.00730741 | 0.785743 | N/A | N/A |
| 4: threshold [adj_r2] | 0.0072 | 0.00735414 | 1.02141 | N/A | N/A |
| 4: threshold [coef] | 0.0841 | 0.106196 | 1.26273 | yes | yes |
| 4: threshold [nobs] | 6223 | 5043 | 0.810381 | N/A | N/A |
| 4: threshold [se] | 0.027 | 0.0319049 | 1.18166 | N/A | N/A |
| 4: week4 [coef] | 0.0004 | 0.000309863 | 0.774657 | yes | yes |
| 4: week4 [se] | 0.0001 | 0.00012791 | 1.2791 | N/A | N/A |

## table_4

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.1536 | -0.151346 | 0.985326 | yes | yes |
| 1: calendar:week4 [se] | 0.0471 | 0.0459788 | 0.976195 | N/A | N/A |
| 1: threshold [adj_r2] | 0.0053 | 0.0053391 | 1.00738 | N/A | N/A |
| 1: threshold [coef] | -0.1809 | -0.173107 | 0.956923 | yes | yes |
| 1: threshold [nobs] | 15291 | 14796 | 0.967628 | N/A | N/A |
| 1: threshold [se] | 0.062 | 0.0613394 | 0.989344 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.0284 | -0.106168 | 3.73831 | yes | yes |
| 2: calendar:week4 [se] | 0.0596 | 0.0612268 | 1.0273 | N/A | N/A |
| 2: threshold [adj_r2] | 0.0204 | 0.0265478 | 1.30136 | N/A | N/A |
| 2: threshold [coef] | -0.0157 | -0.0185372 | 1.18071 | yes | yes |
| 2: threshold [nobs] | 8870 | 8478 | 0.955806 | N/A | N/A |
| 2: threshold [se] | 0.0576 | 0.059397 | 1.0312 | N/A | N/A |
| 3: calendar:week4 [coef] | -0.2569 | -0.200243 | 0.779458 | yes | yes |
| 3: calendar:week4 [se] | 0.067 | 0.0669303 | 0.998959 | N/A | N/A |
| 3: threshold [adj_r2] | 0.017 | 0.0139001 | 0.817654 | N/A | N/A |
| 3: threshold [coef] | -0.3685 | -0.363704 | 0.986985 | yes | yes |
| 3: threshold [nobs] | 6421 | 6317 | 0.983803 | N/A | N/A |
| 3: threshold [se] | 0.1103 | 0.109614 | 0.993779 | N/A | N/A |

## table_5

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.1174 | -0.0743924 | 0.633666 | yes | yes |
| 1: calendar:week4 [se] | 0.0683 | 0.171212 | 2.50677 | N/A | N/A |
| 1: threshold [adj_r2] | 0.0094 | 0.00135596 | 0.144251 | N/A | N/A |
| 1: threshold [coef] | -0.2054 | 5.81835e-05 | -0.000283269 | no | no |
| 1: threshold [nobs] | 4175 | 4109 | 0.984192 | N/A | N/A |
| 1: threshold [se] | 0.0597 | 0.0392838 | 0.65802 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.0678 | -0.151665 | 2.23695 | yes | yes |
| 2: calendar:week4 [se] | 0.0654 | 0.176584 | 2.70006 | N/A | N/A |
| 2: threshold [adj_r2] | 0.0023 | 0.00109898 | 0.477816 | N/A | N/A |
| 2: threshold [coef] | -0.0339 | 0.0109586 | -0.323261 | no | yes |
| 2: threshold [nobs] | 4175 | 4109 | 0.984192 | N/A | N/A |
| 2: threshold [se] | 0.0478 | 0.0332114 | 0.694798 | N/A | N/A |

## table_6a

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| sp500: mean_pct_pa [value] | 7.11 | 7.61551 | 1.0711 | yes | N/A |
| sp500: sharpe [value] | 0.35 | 0.386183 | 1.10338 | yes | N/A |
| sp500: skewness [value] | -0.08 | -0.287646 | 3.59557 | yes | N/A |
| sp500: vol_pct_pa [value] | 20.05 | 19.72 | 0.983539 | yes | N/A |
| strategy: mean_pct_pa [value] | 10.2 | 6.44968 | 0.632321 | yes | N/A |
| strategy: sharpe [value] | 1.11 | 0.734083 | 0.661336 | yes | N/A |
| strategy: skewness [value] | 5.23 | 3.88392 | 0.742624 | yes | N/A |
| strategy: vol_pct_pa [value] | 9.17 | 8.78603 | 0.958127 | yes | N/A |
| ty: mean_pct_pa [value] | 2.92 | 3.3924 | 1.16178 | yes | N/A |
| ty: sharpe [value] | 0.48 | 0.556063 | 1.15847 | yes | N/A |
| ty: skewness [value] | 0.03 | 0.0692597 | 2.30866 | yes | N/A |
| ty: vol_pct_pa [value] | 6.13 | 6.10075 | 0.995228 | yes | N/A |

## table_6b

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| c4: alpha_pct_pa [coef] | 9.64 | 5.7564 | 0.597137 | yes | yes |
| c4: alpha_pct_pa [se] | 1.78 | 1.69777 | 0.953802 | N/A | N/A |
| capm: alpha_pct_pa [coef] | 9.61 | 5.71054 | 0.594229 | yes | yes |
| capm: alpha_pct_pa [se] | 1.77 | 1.69888 | 0.959819 | N/A | N/A |
| ff5: alpha_pct_pa [coef] | 9.49 | 5.67533 | 0.598033 | yes | yes |
| ff5: alpha_pct_pa [se] | 1.74 | 1.6739 | 0.962009 | N/A | N/A |
| hxz: alpha_pct_pa [coef] | 9.43 | 5.56161 | 0.589778 | yes | yes |
| hxz: alpha_pct_pa [se] | 1.75 | 1.66911 | 0.953779 | N/A | N/A |

## table_6c

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| epu: high_mean_pct_pa [coef] | 15.16 | 11.6837 | 0.770693 | yes | yes |
| epu: high_mean_pct_pa [se] | 3.26 | 3.05939 | 0.938463 | N/A | N/A |
| epu: low_mean_pct_pa [coef] | 5.24 | 1.2173 | 0.232309 | yes | no |
| epu: low_mean_pct_pa [se] | 1.56 | 1.71599 | 1.09999 | N/A | N/A |
| ivol: high_mean_pct_pa [coef] | 15.68 | 11.3562 | 0.724249 | yes | yes |
| ivol: high_mean_pct_pa [se] | 3.44 | 3.19438 | 0.9286 | N/A | N/A |
| ivol: low_mean_pct_pa [coef] | 5.09 | 1.54468 | 0.303473 | yes | no |
| ivol: low_mean_pct_pa [se] | 1.28 | 1.45019 | 1.13296 | N/A | N/A |
| liquidity: high_mean_pct_pa [coef] | 17.96 | 12.611 | 0.702172 | yes | yes |
| liquidity: high_mean_pct_pa [se] | 3.33 | 3.11009 | 0.933961 | N/A | N/A |
| liquidity: low_mean_pct_pa [coef] | 3.79 | 0.290288 | 0.0765931 | yes | no |
| liquidity: low_mean_pct_pa [se] | 1.85 | 1.62029 | 0.875831 | N/A | N/A |
| move: high_mean_pct_pa [coef] | 14.85 | 11.9026 | 0.801523 | yes | yes |
| move: high_mean_pct_pa [se] | 3.32 | 3.48596 | 1.04999 | N/A | N/A |
| move: low_mean_pct_pa [coef] | 5.55 | 0.33658 | 0.0606451 | yes | no |
| move: low_mean_pct_pa [se] | 1.43 | 1.56808 | 1.09656 | N/A | N/A |
| vix: high_mean_pct_pa [coef] | 16.5 | 13.0256 | 0.789433 | yes | yes |
| vix: high_mean_pct_pa [se] | 3.44 | 3.29315 | 0.957312 | N/A | N/A |
| vix: low_mean_pct_pa [coef] | 3.91 | -0.124205 | -0.0317659 | no | no |
| vix: low_mean_pct_pa [se] | 1.11 | 1.20438 | 1.08503 | N/A | N/A |

## table_C1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| calendar: ar1 [value] | 0.91 | 0.916567 | 1.00722 | yes | N/A |
| calendar: excess_kurtosis [value] | 6.27 | 13.9984 | 2.23259 | yes | N/A |
| calendar: mean_annualized [value] | 0.18 | 0.190591 | 1.05884 | yes | N/A |
| calendar: sd_annualized [value] | 0.16 | 0.167953 | 1.0497 | yes | N/A |
| calendar: skewness [value] | -1.43 | -2.18726 | 1.52955 | yes | N/A |
| threshold: ar1 [value] | 0.61 | 0.611547 | 1.00254 | yes | N/A |
| threshold: excess_kurtosis [value] | 2.69 | 2.7104 | 1.00758 | yes | N/A |
| threshold: mean_annualized [value] | 0.49 | 0.506814 | 1.03431 | yes | N/A |
| threshold: sd_annualized [value] | 0.08 | 0.0756384 | 0.945481 | yes | N/A |
| threshold: skewness [value] | -0.98 | -1.06002 | 1.08166 | yes | N/A |

## table_C2

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| calendar: threshold [value] | 0.605 | 0.584193 | 0.965609 | yes | N/A |
| momentum: calendar [value] | 0.676 | 0.657341 | 0.972398 | yes | N/A |
| momentum: threshold [value] | 0.676 | 0.681038 | 1.00745 | yes | N/A |
| vix: threshold [value] | -0.353 | -0.401126 | 1.13633 | yes | N/A |

## table_D1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: ret_1 [adj_r2] | 0.802 | 0.780017 | 0.972589 | N/A | N/A |
| 1: ret_1 [coef] | 0.1466 | 0.125714 | 0.857531 | yes | yes |
| 1: ret_1 [se] | 0.01 | 0.00583265 | 0.583265 | N/A | N/A |
| 2: ret_1 [adj_r2] | 0.7194 | 0.730161 | 1.01496 | N/A | N/A |

## table_D10

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: rev_st [coef] | -0.0377 | -0.0309824 | 0.821814 | yes | yes |
| 1: rev_st [nobs] | 6473 | 6317 | 0.9759 | N/A | N/A |
| 1: rev_st [se] | 0.0136 | 0.012457 | 0.915959 | N/A | N/A |
| 2: rev_st [coef] | -0.0122 | -0.0102223 | 0.837897 | yes | yes |
| 2: rev_st [se] | 0.0195 | 0.0178237 | 0.914034 | N/A | N/A |

## table_D11

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: eom_rev [coef] | -0.0159 | -0.096502 | 6.06931 | yes | no |
| 1: eom_rev [nobs] | 6173 | 6317 | 1.02333 | N/A | N/A |
| 1: eom_rev [se] | 0.0154 | 0.0402806 | 2.61563 | N/A | N/A |

## table_D12

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week1 [coef] | 0.2262 | 0.0746176 | 0.329875 | yes | no |
| 1: calendar:week1 [se] | 0.1018 | 0.113366 | 1.11361 | N/A | N/A |
| 3: calendar:week3 [coef] | 0.2579 | 0.207145 | 0.803199 | yes | yes |
| 3: calendar:week3 [se] | 0.0887 | 0.0754753 | 0.850906 | N/A | N/A |

## table_D14

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.206 | -0.15501 | 0.752476 | yes | yes |
| 1: calendar:week4 [se] | 0.0535 | 0.0541024 | 1.01126 | N/A | N/A |
| 1: threshold [coef] | -0.2723 | -0.668625 | 2.45547 | yes | yes |
| 1: threshold [nobs] | 6097 | 5503 | 0.902575 | N/A | N/A |
| 1: threshold [se] | 0.087 | 0.0817158 | 0.939262 | N/A | N/A |

## table_D3

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: mom_fast [coef] | 0.0006 | 0.000572684 | 0.954473 | yes | yes |
| 1: mom_fast [se] | 0.0005 | 0.000490384 | 0.980768 | N/A | N/A |
| 1: mom_medium [coef] | 0.0013 | 0.00131723 | 1.01325 | yes | yes |
| 1: mom_medium [se] | 0.0004 | 0.00042928 | 1.0732 | N/A | N/A |
| 1: mom_slow [coef] | 0.001 | 0.00102626 | 1.02626 | yes | yes |
| 1: mom_slow [se] | 0.0004 | 0.000399137 | 0.997843 | N/A | N/A |

## table_D4

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.3189 | -0.261891 | 0.821232 | yes | yes |
| 1: calendar:week4 [se] | 0.0866 | 0.0771764 | 0.891183 | N/A | N/A |
| 1: threshold [coef] | -0.397 | -0.449384 | 1.13195 | yes | yes |
| 1: threshold [se] | 0.1199 | 0.110055 | 0.917891 | N/A | N/A |

## table_D6

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: threshold [coef] | -0.3938 | -0.463537 | 1.17709 | yes | yes |
| 1: threshold [se] | 0.1237 | 0.124051 | 1.00284 | N/A | N/A |
| 3: threshold [coef] | -0.398 | -0.446236 | 1.1212 | yes | yes |
| 3: threshold [se] | 0.1104 | 0.111299 | 1.00815 | N/A | N/A |

## table_D7

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.6008 | -0.486946 | 0.810496 | yes | yes |
| 1: calendar:week4 [se] | 0.16 | 0.150833 | 0.942703 | N/A | N/A |
| 1: threshold [coef] | -0.8453 | -0.383527 | 0.453717 | yes | yes |
| 1: threshold [se] | 0.212 | 0.118123 | 0.557182 | N/A | N/A |
| 2: calendar:week4 [coef] | -0.2914 | -0.248343 | 0.852242 | yes | yes |
| 2: calendar:week4 [se] | 0.076 | 0.072945 | 0.959803 | N/A | N/A |
| 2: threshold [coef] | -0.4098 | -0.441857 | 1.07823 | yes | yes |
| 2: threshold [se] | 0.107 | 0.112143 | 1.04806 | N/A | N/A |
| 3: calendar:week4 [coef] | -0.346 | -0.288855 | 0.834842 | yes | yes |
| 3: calendar:week4 [se] | 0.091 | 0.087015 | 0.956209 | N/A | N/A |
| 3: threshold [coef] | -0.4822 | -0.414557 | 0.85972 | yes | yes |
| 3: threshold [se] | 0.131 | 0.116699 | 0.89083 | N/A | N/A |

## table_D8

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: threshold_large [coef] | -0.4264 | -0.470275 | 1.1029 | yes | yes |
| 1: threshold_large [se] | 0.1143 | 0.115697 | 1.01222 | N/A | N/A |
| 1: threshold_small [coef] | -0.2289 | -0.353777 | 1.54555 | yes | no |
| 1: threshold_small [se] | 0.1637 | 0.15511 | 0.947525 | N/A | N/A |
| 3: threshold_perp [coef] | -0.4144 | -0.464414 | 1.12069 | yes | yes |
| 3: threshold_perp [se] | 0.1148 | 0.115753 | 1.0083 | N/A | N/A |

## table_D9

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: threshold [coef] | -0.4493 | -0.491847 | 1.0947 | yes | yes |
| 1: threshold [nobs] | 6124 | 6317 | 1.03152 | N/A | N/A |
| 1: threshold [se] | 0.1152 | 0.115902 | 1.00609 | N/A | N/A |
| 3: threshold [coef] | -0.4226 | N/A | N/A | N/A | N/A |
| 3: threshold [nobs] | 3149 | N/A | N/A | N/A | N/A |
| 3: threshold [se] | 0.1719 | N/A | N/A | N/A | N/A |
| 4: threshold [coef] | -0.3731 | -0.385589 | 1.03347 | yes | yes |
| 4: threshold [nobs] | 3903 | 3843 | 0.984627 | N/A | N/A |
| 4: threshold [se] | 0.1537 | 0.150572 | 0.979648 | N/A | N/A |

## Export coverage

Joined exhibit keys: costs, figure_1, figure_2, figure_3, figure_4, figure_5, figure_6, figure_D1, figure_D2, figure_D3, figure_D4, figure_D5, table_1, table_2a, table_2b, table_3, table_4, table_5, table_6a, table_6b, table_6c, table_C1, table_C2, table_D1, table_D10, table_D11, table_D12, table_D14, table_D3, table_D4, table_D6, table_D7, table_D8, table_D9

Blank canonical values join keys only; they do not count as numeric matches.

## Unmatched targets

| exhibit | column | term | stat | reason |
|---|---|---|---|---|
| costs | random | annual_bps | value | paper-only data: random-date cost sign conflicts between text and Figure D.5 |
| figure_5 | ancerno | calendar | value | not available: FEARS is private; ANcerno is licensed and unavailable |
| figure_5 | ancerno | threshold | value | not available: FEARS is private; ANcerno is licensed and unavailable |
| figure_6 | sample_end | sp500 | value | paper-only data: Figure 6 axis transformation is unresolved |
| figure_6 | sample_end | strategy | value | paper-only data: Figure 6 axis transformation is unresolved |
| figure_D5 | random | ci95_high_bps | value | paper-only data: random-date cost sign conflicts between text and Figure D.5 |
| figure_D5 | random | ci95_low_bps | value | paper-only data: random-date cost sign conflicts between text and Figure D.5 |
| figure_D5 | random | mean_bps | value | paper-only data: random-date cost sign conflicts between text and Figure D.5 |
| table_D9 | 3 | threshold | coef | not available: FEARS is private; ANcerno is licensed and unavailable |
| table_D9 | 3 | threshold | nobs | not available: FEARS is private; ANcerno is licensed and unavailable |
| table_D9 | 3 | threshold | se | not available: FEARS is private; ANcerno is licensed and unavailable |
