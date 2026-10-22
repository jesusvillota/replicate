# Paper comparison

## Summary

- Targets matched: 252/399
- Sign-match rate: 97.5% (116/119 eligible targets)
- Significance-match rate: 85.9% (85/99 eligible targets)
- Missing exhibits: costs, figure_1, figure_2, figure_3, figure_4, figure_5, figure_6, figure_D1, figure_D2, figure_D3, figure_D4, figure_D5, table_4, table_5, table_6a, table_6b, table_6c, table_D14, table_D4, table_D9
- Matched exhibits: table_1, table_2a, table_2b, table_3, table_C1, table_C2, table_D1, table_D10, table_D11, table_D12, table_D3, table_D6, table_D7, table_D8
- Skipped CSVs: 17
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_2.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_3.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_4.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_6.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_C1.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_D1.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_D2.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_D3.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_D4.csv: missing columns column
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures/figure_D5.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/costs.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/table_6a.csv: missing columns column, exhibit, term
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/table_6b.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/table_6c.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/table_D13.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/table_D2.csv: no matching target keys
  - /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables/table_D5.csv: no matching target keys

Targets: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/docs/results/targets.csv`. Inputs: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/tables`, `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-018/output/figures`.

Each row compares one statistic. Approximate chart readings have a `~` prefix. Sign checks apply to coef, t and value. Significance checks apply to coef and t, using |t| ≥ 1.96 on both sides (or neither). Where t is absent, coef/se is used. N/A means missing data, an inapplicable check, or division by zero. Missing exhibits have no matched numeric targets; partial exhibits retain N/A rows.

## costs

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| calendar: annual_bps [value] | 5 | N/A | N/A | N/A | N/A |
| headline: annual_bps [value] | 8 | N/A | N/A | N/A | N/A |
| headline: annual_usd [value] | 1.6e+10 | N/A | N/A | N/A | N/A |
| household: annual_usd [value] | 200 | N/A | N/A | N/A | N/A |
| random: annual_bps [value] | 0.6 | N/A | N/A | N/A | N/A |
| threshold: annual_max_bps [value] | 27 | N/A | N/A | N/A | N/A |
| threshold: annual_mean_bps [value] | 15 | N/A | N/A | N/A | N/A |
| threshold: annual_min_bps [value] | 6 | N/A | N/A | N/A | N/A |
| threshold: annual_one_pct_trade_bps [value] | 11 | N/A | N/A | N/A | N/A |

## figure_1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| equity_share: actual_max [value] | ~0.68 | N/A | N/A | N/A | N/A |
| equity_share: actual_min [value] | ~0.63 | N/A | N/A | N/A | N/A |
| equity_share: target_typical [value] | ~0.65 | N/A | N/A | N/A | N/A |

## figure_2

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| delta_0.0_pct: threshold [t] | ~-3.8 | N/A | N/A | N/A | N/A |
| delta_1.0_pct: threshold [t] | ~-4.2 | N/A | N/A | N/A | N/A |
| delta_1.8_pct: threshold [t] | ~-4.3 | N/A | N/A | N/A | N/A |
| summary: one_pct_weakening_delta_pct [value] | ~2.7 | N/A | N/A | N/A | N/A |

## figure_3

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| days_1: calendar_interaction [t] | ~-0.85 | N/A | N/A | N/A | N/A |
| days_10: calendar_interaction [t] | ~-0.1 | N/A | N/A | N/A | N/A |
| days_2: calendar_interaction [t] | ~-1.15 | N/A | N/A | N/A | N/A |
| days_3: calendar_interaction [t] | ~-1 | N/A | N/A | N/A | N/A |
| days_4: calendar_interaction [t] | ~-3.1 | N/A | N/A | N/A | N/A |
| days_5: calendar_interaction [t] | ~-2.8 | N/A | N/A | N/A | N/A |
| days_6: calendar_interaction [t] | ~-2.4 | N/A | N/A | N/A | N/A |
| days_7: calendar_interaction [t] | ~-1.35 | N/A | N/A | N/A | N/A |
| days_8: calendar_interaction [t] | ~-1 | N/A | N/A | N/A | N/A |
| days_9: calendar_interaction [t] | ~-0.5 | N/A | N/A | N/A | N/A |

## figure_4

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| day_15: calendar:week4 [coef] | ~-0.13 | N/A | N/A | N/A | N/A |
| day_15: threshold [coef] | ~-0.12 | N/A | N/A | N/A | N/A |
| day_2: calendar:week4 [coef] | ~-0.52 | N/A | N/A | N/A | N/A |
| day_4: threshold [coef] | ~-0.95 | N/A | N/A | N/A | N/A |
| summary: calendar_week4_first_insignificant_day [value] | ~6 | N/A | N/A | N/A | N/A |
| summary: threshold_first_insignificant_day [value] | ~9 | N/A | N/A | N/A | N/A |

## figure_5

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| ancerno: calendar [value] | ~-0.1 | N/A | N/A | N/A | N/A |
| ancerno: threshold [value] | ~-0.1 | N/A | N/A | N/A | N/A |
| cftc_hedgers: calendar [value] | ~-0.13 | N/A | N/A | N/A | N/A |
| cftc_hedgers: threshold [value] | ~-0.1 | N/A | N/A | N/A | N/A |
| cftc_speculators: calendar [value] | ~0.17 | N/A | N/A | N/A | N/A |
| cftc_speculators: threshold [value] | ~0.11 | N/A | N/A | N/A | N/A |
| ici: calendar [value] | ~-0.19 | N/A | N/A | N/A | N/A |
| ici: threshold [value] | ~-0.17 | N/A | N/A | N/A | N/A |
| ltpos_asset_managers: calendar [value] | ~-0.12 | N/A | N/A | N/A | N/A |
| ltpos_asset_managers: threshold [value] | ~-0.08 | N/A | N/A | N/A | N/A |
| ltpos_leveraged_funds: calendar [value] | ~0.13 | N/A | N/A | N/A | N/A |
| ltpos_leveraged_funds: threshold [value] | ~0.18 | N/A | N/A | N/A | N/A |

## figure_6

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| sample_end: sp500 [value] | ~2.3 | N/A | N/A | N/A | N/A |
| sample_end: strategy [value] | ~6.2 | N/A | N/A | N/A | N/A |

## figure_D1

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| delta_1.8_pct: threshold [t] | ~-4.5 | N/A | N/A | N/A | N/A |

## figure_D2

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| days_4: calendar_interaction [t] | ~-3.65 | N/A | N/A | N/A | N/A |

## figure_D3

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| delta_0.0_pct: during_rebalancing [t] | ~-3.8 | N/A | N/A | N/A | N/A |
| delta_0.3_pct: outside_rebalancing [t] | ~2.5 | N/A | N/A | N/A | N/A |
| delta_1.8_pct: during_rebalancing [t] | ~-6.1 | N/A | N/A | N/A | N/A |
| delta_2.3_pct: outside_rebalancing [t] | ~-3 | N/A | N/A | N/A | N/A |

## figure_D4

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| day_1: calendar:week4 [coef] | ~-0.3 | N/A | N/A | N/A | N/A |
| day_1: threshold [coef] | ~-0.42 | N/A | N/A | N/A | N/A |
| day_2: calendar:week4 [coef] | ~-0.2 | N/A | N/A | N/A | N/A |
| day_2: threshold [coef] | ~-0.2 | N/A | N/A | N/A | N/A |

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
| 1: calendar:week4 [coef] | -0.1536 | N/A | N/A | N/A | N/A |
| 1: calendar:week4 [se] | 0.0471 | N/A | N/A | N/A | N/A |
| 1: threshold [adj_r2] | 0.0053 | N/A | N/A | N/A | N/A |
| 1: threshold [coef] | -0.1809 | N/A | N/A | N/A | N/A |
| 1: threshold [nobs] | 15291 | N/A | N/A | N/A | N/A |
| 1: threshold [se] | 0.062 | N/A | N/A | N/A | N/A |
| 2: calendar:week4 [coef] | -0.0284 | N/A | N/A | N/A | N/A |
| 2: calendar:week4 [se] | 0.0596 | N/A | N/A | N/A | N/A |
| 2: threshold [adj_r2] | 0.0204 | N/A | N/A | N/A | N/A |
| 2: threshold [coef] | -0.0157 | N/A | N/A | N/A | N/A |
| 2: threshold [nobs] | 8870 | N/A | N/A | N/A | N/A |
| 2: threshold [se] | 0.0576 | N/A | N/A | N/A | N/A |
| 3: calendar:week4 [coef] | -0.2569 | N/A | N/A | N/A | N/A |
| 3: calendar:week4 [se] | 0.067 | N/A | N/A | N/A | N/A |
| 3: threshold [adj_r2] | 0.017 | N/A | N/A | N/A | N/A |
| 3: threshold [coef] | -0.3685 | N/A | N/A | N/A | N/A |
| 3: threshold [nobs] | 6421 | N/A | N/A | N/A | N/A |
| 3: threshold [se] | 0.1103 | N/A | N/A | N/A | N/A |

## table_5

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| 1: calendar:week4 [coef] | -0.1174 | N/A | N/A | N/A | N/A |
| 1: calendar:week4 [se] | 0.0683 | N/A | N/A | N/A | N/A |
| 1: threshold [adj_r2] | 0.0094 | N/A | N/A | N/A | N/A |
| 1: threshold [coef] | -0.2054 | N/A | N/A | N/A | N/A |
| 1: threshold [nobs] | 4175 | N/A | N/A | N/A | N/A |
| 1: threshold [se] | 0.0597 | N/A | N/A | N/A | N/A |
| 2: calendar:week4 [coef] | -0.0678 | N/A | N/A | N/A | N/A |
| 2: calendar:week4 [se] | 0.0654 | N/A | N/A | N/A | N/A |
| 2: threshold [adj_r2] | 0.0023 | N/A | N/A | N/A | N/A |
| 2: threshold [coef] | -0.0339 | N/A | N/A | N/A | N/A |
| 2: threshold [nobs] | 4175 | N/A | N/A | N/A | N/A |
| 2: threshold [se] | 0.0478 | N/A | N/A | N/A | N/A |

## table_6a

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| sp500: mean_pct_pa [value] | 7.11 | N/A | N/A | N/A | N/A |
| sp500: sharpe [value] | 0.35 | N/A | N/A | N/A | N/A |
| sp500: skewness [value] | -0.08 | N/A | N/A | N/A | N/A |
| sp500: vol_pct_pa [value] | 20.05 | N/A | N/A | N/A | N/A |
| strategy: mean_pct_pa [value] | 10.2 | N/A | N/A | N/A | N/A |
| strategy: sharpe [value] | 1.11 | N/A | N/A | N/A | N/A |
| strategy: skewness [value] | 5.23 | N/A | N/A | N/A | N/A |
| strategy: vol_pct_pa [value] | 9.17 | N/A | N/A | N/A | N/A |
| ty: mean_pct_pa [value] | 2.92 | N/A | N/A | N/A | N/A |
| ty: sharpe [value] | 0.48 | N/A | N/A | N/A | N/A |
| ty: skewness [value] | 0.03 | N/A | N/A | N/A | N/A |
| ty: vol_pct_pa [value] | 6.13 | N/A | N/A | N/A | N/A |

## table_6b

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| c4: alpha_pct_pa [coef] | 9.64 | N/A | N/A | N/A | N/A |
| c4: alpha_pct_pa [se] | 1.78 | N/A | N/A | N/A | N/A |
| capm: alpha_pct_pa [coef] | 9.61 | N/A | N/A | N/A | N/A |
| capm: alpha_pct_pa [se] | 1.77 | N/A | N/A | N/A | N/A |
| ff5: alpha_pct_pa [coef] | 9.49 | N/A | N/A | N/A | N/A |
| ff5: alpha_pct_pa [se] | 1.74 | N/A | N/A | N/A | N/A |
| hxz: alpha_pct_pa [coef] | 9.43 | N/A | N/A | N/A | N/A |
| hxz: alpha_pct_pa [se] | 1.75 | N/A | N/A | N/A | N/A |

## table_6c

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| epu: high_mean_pct_pa [coef] | 15.16 | N/A | N/A | N/A | N/A |
| epu: high_mean_pct_pa [se] | 3.26 | N/A | N/A | N/A | N/A |
| epu: low_mean_pct_pa [coef] | 5.24 | N/A | N/A | N/A | N/A |
| epu: low_mean_pct_pa [se] | 1.56 | N/A | N/A | N/A | N/A |
| ivol: high_mean_pct_pa [coef] | 15.68 | N/A | N/A | N/A | N/A |
| ivol: high_mean_pct_pa [se] | 3.44 | N/A | N/A | N/A | N/A |
| ivol: low_mean_pct_pa [coef] | 5.09 | N/A | N/A | N/A | N/A |
| ivol: low_mean_pct_pa [se] | 1.28 | N/A | N/A | N/A | N/A |
| liquidity: high_mean_pct_pa [coef] | 17.96 | N/A | N/A | N/A | N/A |
| liquidity: high_mean_pct_pa [se] | 3.33 | N/A | N/A | N/A | N/A |
| liquidity: low_mean_pct_pa [coef] | 3.79 | N/A | N/A | N/A | N/A |
| liquidity: low_mean_pct_pa [se] | 1.85 | N/A | N/A | N/A | N/A |
| move: high_mean_pct_pa [coef] | 14.85 | N/A | N/A | N/A | N/A |
| move: high_mean_pct_pa [se] | 3.32 | N/A | N/A | N/A | N/A |
| move: low_mean_pct_pa [coef] | 5.55 | N/A | N/A | N/A | N/A |
| move: low_mean_pct_pa [se] | 1.43 | N/A | N/A | N/A | N/A |
| vix: high_mean_pct_pa [coef] | 16.5 | N/A | N/A | N/A | N/A |
| vix: high_mean_pct_pa [se] | 3.44 | N/A | N/A | N/A | N/A |
| vix: low_mean_pct_pa [coef] | 3.91 | N/A | N/A | N/A | N/A |
| vix: low_mean_pct_pa [se] | 1.11 | N/A | N/A | N/A | N/A |

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
| 1: calendar:week4 [coef] | -0.206 | N/A | N/A | N/A | N/A |
| 1: calendar:week4 [se] | 0.0535 | N/A | N/A | N/A | N/A |
| 1: threshold [coef] | -0.2723 | N/A | N/A | N/A | N/A |
| 1: threshold [nobs] | 6097 | N/A | N/A | N/A | N/A |
| 1: threshold [se] | 0.087 | N/A | N/A | N/A | N/A |

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
| 1: calendar:week4 [coef] | -0.3189 | N/A | N/A | N/A | N/A |
| 1: calendar:week4 [se] | 0.0866 | N/A | N/A | N/A | N/A |
| 1: threshold [coef] | -0.397 | N/A | N/A | N/A | N/A |
| 1: threshold [se] | 0.1199 | N/A | N/A | N/A | N/A |

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
| 1: threshold [coef] | -0.4493 | N/A | N/A | N/A | N/A |
| 1: threshold [nobs] | 6124 | N/A | N/A | N/A | N/A |
| 1: threshold [se] | 0.1152 | N/A | N/A | N/A | N/A |
| 3: threshold [coef] | -0.4226 | N/A | N/A | N/A | N/A |
| 3: threshold [nobs] | 3149 | N/A | N/A | N/A | N/A |
| 3: threshold [se] | 0.1719 | N/A | N/A | N/A | N/A |
| 4: threshold [coef] | -0.3731 | N/A | N/A | N/A | N/A |
| 4: threshold [nobs] | 3903 | N/A | N/A | N/A | N/A |
| 4: threshold [se] | 0.1537 | N/A | N/A | N/A | N/A |

## Reading the gaps

### Scope and headline results

The main run uses DEC-001 E1/T3 cash-market proxies and `clean` timing. The sample spans 1997-09-10 through 2023-03-17.
There are 6,318 panel rows and 6,317 baseline return pairs. The paper reports 6,226 regression observations.
Initialization uses earlier history. No return is filled, no sample is shortened, and no parameter is fitted to the paper.

The automated summary above covers 252/399 target statistics. Its sign rate is 97.5% (116/119). Its significance rate is 85.9% (85/99).
These rates apply only to joined targets. They exclude the direct comparisons below. A sign match does not imply a size match.
An automated “missing exhibit” can mean missing comparison keys. All required core artifacts exist.
Costs, Table 6 and the figures need keyed exports: [issue #29](https://github.com/jesusvillota/replicate/issues/29).

The report was regenerated with robustness folders temporarily outside its input roots. All main CSVs remained unchanged.
Otherwise recursive discovery can substitute robustness values: [issue #28](https://github.com/jesusvillota/replicate/issues/28).
The generated tables above and the rates here describe the main run only.

| Headline | Paper | Main run |
|---|---:|---:|
| Table 1 (1), Threshold: coefficient (t) | -0.4144 (-3.6098) | -0.464414 (-4.012118) |
| Table 1 (1), Cal × week4: coefficient (t) | -0.3029 (-3.7488) | -0.260256 (-3.418693) |
| Headline cost, bps/year | 8 | 4193.686081 |
| Headline cost, USD/year on $20T | 16,000,000,000 | 8,387,372,162,951 |
| Strategy Sharpe ratio, gross | 1.11 | 0.734083 |

Paper t-statistics above equal printed coefficient divided by printed standard error. Rounding limits their precision.
Both Table 1 signals replicate in sign and 5% significance. Threshold is 12.1% larger in absolute size; Calendar is 14.1% smaller.
One-standard-deviation return effects are −22.1274 and −16.7609 bps, versus −20 and −19.2 bps.
One basis point (bps) is 0.01 percentage points. Sharpe ratio means annual mean return divided by annual volatility.

### Which exhibits agree, and which differ

| Exhibits | Result and most likely source of the gap |
|---|---|
| Table 1 | Both main signals agree in sign and significance. Small control coefficients differ. Cash-market returns and control vintages are likely causes. |
| Tables 2A and 2B | All nine and six eligible signs agree. Table 2A has 9/9 significance matches; Table 2B has 2/6. Quarter-month subsets amplify proxy and sample differences. |
| Table 3 | Equity and bond Threshold slopes keep their expected signs. Bond Calendar is +0.01523 (t=1.234), versus +0.0362 (t≈2.317). The bond proxy is the main candidate. Overall significance agrees for 19/24 targets. |
| Tables C.1 and C.2; Figure C.1 | All 14 targeted signs agree. Distribution levels and correlations differ. These describe the proxy signals, rather than exact futures signals. Figure C.1 has no numeric targets. |
| Table D.1 | Targeted signs and significance agree. Contemporaneous return-driven signal variation is retained. |
| Tables D.2, D.5 and D.13 | Required CSVs exist. The target catalogue has no numeric targets for these tables. Selected signal estimates are listed below; no match rate is claimed. |
| Tables D.3, D.6 and D.7 | All eligible targeted signs and significance decisions agree. Sizes still differ with the proxy returns and signal distributions. |
| Table D.8 | All three signs agree. The small-signal effect is significant here, unlike the paper. Proxy measurement and the small/large split are likely causes. |
| Tables D.10–D.12 | Signs agree. D.11 end-of-month reversal is significant here, unlike the paper. D.12 week1 loses significance; week3 retains it. Calendar alignment, proxy returns and sample differences are plausible causes. |
| Figures 2 and D.1 | Negative Threshold prediction and stronger low-threshold evidence broadly agree. Some exact threshold readings differ. Timing and proxy construction both matter. |
| Figures 3 and D.2 | The four-day-window result fails: t≈0.002 instead of −3.1/−3.65. The strongest negative window here is five days. Cash-market close times, month-end calendars and timing are leading candidates. |
| Figures 4 and D.4 | Short-run negative prediction partly agrees. Cumulative effects first lose 5% significance at days 7/3, versus about 9/6. Calendar day2 is −0.0164 rather than about −0.20. Proxy close times and horizon/error conventions in paper-notes §5 are plausible causes. |
| Costs and Figure D.5 | Economic sizes fail badly. The worked-example unit mismatch and extreme delta=0 cost need code review. They cannot be explained as successful proxy replication. |
| Table 6 and Figure 6 | Gross Sharpe ratio is positive but falls from 1.11 to 0.7341. Factor alphas stay positive and significant. Low-regime means mostly lose significance. Proxy returns and the documented Calendar-reversal reading can contribute. |

[Proxy comparison](../data/proxy_comparison.md) reports E1/T3 correlation 0.9917 and tracking error 2.8069% per year.
E2/T2 gives 0.9810 and 4.5655%. These use 4,839 clean benchmark days, starting in 2000.
They do not validate Bloomberg equivalence or the 1997–2000 period. Equity and Treasury close times differ.

The panel has 91 more baseline regression pairs than the paper. Earlier initialization avoids imposing an extra 252-day burn-in.
The panel method records 52 missing GSW quote sessions and 104 removed holding returns. Returns remain unfilled.
Sample counts can explain some significance changes, but cannot identify their cause.

Paper-notes §5 also leaves HC/HAC error settings, control scaling, momentum and horizon conventions unclear.
The merged methods fix these choices in [signals](../methods/signals.md), [regressions](../methods/regressions.md),
[horizons](../methods/horizons.md), [costs](../methods/costs.md) and [strategy](../methods/strategy.md).
No new method was selected in this run. A controlled rerun would be needed to assign each gap to one cause.

### Timing and proxy robustness

Literal timing changes only signal construction. The alternative proxy rebuilds every signal from the full E2/T2 panel with clean timing.
Existing analysis functions produced these outputs. No analysis source file was changed.

| Variant | Threshold coefficient (t), Table 1 (1) | Cal × week4 coefficient (t) | Headline cost, bps/year |
|---|---:|---:|---:|
| main | -0.464414 (-4.012118) | -0.260256 (-3.418693) | 4193.686081 |
| literal | -0.269997 (-2.729659) | -0.260521 (-3.366775) | not requested |
| proxy_alt | -0.377347 (-3.389297) | -0.223696 (-3.126650) | 5552.083263 |

| Figure 2 threshold | Main t | Literal t |
|---|---:|---:|
| 0.0% | -3.629972 | -3.629972 |
| 1.0% | -4.222008 | -3.375253 |
| 1.8% | -3.944581 | -2.089239 |

Alternative-proxy Table 3 checks:

| Column and term | Main coefficient (t) | Alternative coefficient (t) |
|---|---:|---:|
| 1: threshold | -0.368583 (-3.455851) | -0.291017 (-2.960534) |
| 1: calendar:week4 | -0.245028 (-3.452627) | -0.212080 (-3.317561) |
| 3: threshold | 0.095832 (3.551138) | 0.086330 (2.670872) |
| 3: calendar:week4 | 0.015227 (1.234278) | 0.011616 (0.738411) |

Both robustness runs retain negative, significant headline signals. Literal timing weakens Threshold materially.
The proxy alternative does not repair the cost failure. Default clean timing and the accepted proxies remain the reported main specification.

### Direct comparisons for outputs without matching keys

These rows read the committed CSVs directly. They supplement the generated N/A rows; they do not change its match-rate denominators.
Units follow [comparison conventions](../methods/comparison.md). Approximate paper chart readings retain `~`.

#### costs — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| calendar: annual_bps [value] | 5 | 353.352 |
| threshold: annual_min_bps [value] | 6 | -1107.41 |
| threshold: annual_max_bps [value] | 27 | 48202.1 |
| threshold: annual_mean_bps [value] | 15 | 1595.41 |
| threshold: annual_one_pct_trade_bps [value] | 11 | 8034.02 |
| headline: annual_bps [value] | 8 | 4193.69 |
| headline: annual_usd [value] | 1.6e+10 | 8.38737e+12 |
| household: annual_usd [value] | 200 | 99063.5 |
| random: annual_bps [value] | 0.6 | 6.99019 |

#### table_6a — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| sp500: mean_pct_pa [value] | 7.11 | 7.61551 |
| sp500: vol_pct_pa [value] | 20.05 | 19.72 |
| sp500: sharpe [value] | 0.35 | 0.386183 |
| sp500: skewness [value] | -0.08 | -0.287646 |
| ty: mean_pct_pa [value] | 2.92 | 3.3924 |
| ty: vol_pct_pa [value] | 6.13 | 6.10075 |
| ty: sharpe [value] | 0.48 | 0.556063 |
| ty: skewness [value] | 0.03 | 0.0692597 |
| strategy: mean_pct_pa [value] | 10.2 | 6.44968 |
| strategy: vol_pct_pa [value] | 9.17 | 8.78603 |
| strategy: sharpe [value] | 1.11 | 0.734083 |
| strategy: skewness [value] | 5.23 | 3.88392 |

#### table_6b — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| capm: alpha_pct_pa [coef] | 9.61 | 5.71054 |
| capm: alpha_pct_pa [se] | 1.77 | 1.69888 |
| c4: alpha_pct_pa [coef] | 9.64 | 5.7564 |
| c4: alpha_pct_pa [se] | 1.78 | 1.69777 |
| ff5: alpha_pct_pa [coef] | 9.49 | 5.67533 |
| ff5: alpha_pct_pa [se] | 1.74 | 1.6739 |
| hxz: alpha_pct_pa [coef] | 9.43 | 5.56161 |
| hxz: alpha_pct_pa [se] | 1.75 | 1.66911 |

#### table_6c — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| ivol: high_mean_pct_pa [coef] | 15.68 | 11.3562 |
| ivol: high_mean_pct_pa [se] | 3.44 | 3.19438 |
| ivol: low_mean_pct_pa [coef] | 5.09 | 1.54468 |
| ivol: low_mean_pct_pa [se] | 1.28 | 1.45019 |
| liquidity: high_mean_pct_pa [coef] | 17.96 | 12.611 |
| liquidity: high_mean_pct_pa [se] | 3.33 | 3.11009 |
| liquidity: low_mean_pct_pa [coef] | 3.79 | 0.290288 |
| liquidity: low_mean_pct_pa [se] | 1.85 | 1.62029 |
| vix: high_mean_pct_pa [coef] | 16.5 | 13.0256 |
| vix: high_mean_pct_pa [se] | 3.44 | 3.29315 |
| vix: low_mean_pct_pa [coef] | 3.91 | -0.124205 |
| vix: low_mean_pct_pa [se] | 1.11 | 1.20438 |
| move: high_mean_pct_pa [coef] | 14.85 | 11.9026 |
| move: high_mean_pct_pa [se] | 3.32 | 3.48596 |
| move: low_mean_pct_pa [coef] | 5.55 | 0.33658 |
| move: low_mean_pct_pa [se] | 1.43 | 1.56808 |
| epu: high_mean_pct_pa [coef] | 15.16 | 11.6837 |
| epu: high_mean_pct_pa [se] | 3.26 | 3.05939 |
| epu: low_mean_pct_pa [coef] | 5.24 | 1.2173 |
| epu: low_mean_pct_pa [se] | 1.56 | 1.71599 |

#### figure_2 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| delta_0.0_pct: threshold [t] | ~-3.8 | -3.62997 |
| delta_1.0_pct: threshold [t] | ~-4.2 | -4.22201 |
| delta_1.8_pct: threshold [t] | ~-4.3 | -3.94458 |
| summary: one_pct_weakening_delta_pct [value] | ~2.7 | not reduced to one threshold |

#### figure_3 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| days_10: calendar_interaction [t] | ~-0.1 | 0.0755611 |
| days_9: calendar_interaction [t] | ~-0.5 | -0.360719 |
| days_8: calendar_interaction [t] | ~-1 | -1.19001 |
| days_7: calendar_interaction [t] | ~-1.35 | -1.90806 |
| days_6: calendar_interaction [t] | ~-2.4 | -1.98411 |
| days_5: calendar_interaction [t] | ~-2.8 | -2.45407 |
| days_4: calendar_interaction [t] | ~-3.1 | 0.00206371 |
| days_3: calendar_interaction [t] | ~-1 | 0.323106 |
| days_2: calendar_interaction [t] | ~-1.15 | 0.984378 |
| days_1: calendar_interaction [t] | ~-0.85 | 2.08786 |

#### figure_4 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| day_4: threshold [coef] | ~-0.95 | -0.987082 |
| day_15: threshold [coef] | ~-0.12 | -0.801446 |
| day_2: calendar:week4 [coef] | ~-0.52 | -0.283967 |
| day_15: calendar:week4 [coef] | ~-0.13 | 0.252764 |
| summary: threshold_first_insignificant_day [value] | ~9 | 7 |
| summary: calendar_week4_first_insignificant_day [value] | ~6 | 3 |

#### figure_6 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| sample_end: strategy [value] | ~6.2 | 3.15401 |
| sample_end: sp500 [value] | ~2.3 | 1.4201 |

#### figure_D1 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| delta_1.8_pct: threshold [t] | ~-4.5 | -3.73356 |

#### figure_D2 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| days_4: calendar_interaction [t] | ~-3.65 | 0.00249157 |

#### figure_D3 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| delta_0.0_pct: during_rebalancing [t] | ~-3.8 | -3.62997 |
| delta_1.8_pct: during_rebalancing [t] | ~-6.1 | -4.58305 |
| delta_0.3_pct: outside_rebalancing [t] | ~2.5 | 1.01573 |
| delta_2.3_pct: outside_rebalancing [t] | ~-3 | -1.92976 |

#### figure_D4 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| day_1: threshold [coef] | ~-0.42 | -0.464414 |
| day_2: threshold [coef] | ~-0.2 | -0.193701 |
| day_1: calendar:week4 [coef] | ~-0.3 | -0.260256 |
| day_2: calendar:week4 [coef] | ~-0.2 | -0.0164074 |

#### figure_D5 — direct CSV readings

| Target | Paper | Main run |
|---|---:|---:|
| random: mean_bps [value] | -0.6 | 6.99019 |
| random: ci95_low_bps [value] | ~-4.6 | -261.509 |
| random: ci95_high_bps [value] | ~3.2 | 278.053 |

Figure 2 is not monotonic. The paper’s rough 2.7% weakening point is not treated as a unique crossing here.
Figure 6 reports raw terminal cumulative log returns. The paper axis reading has an unresolved level convention; these levels are not claimed equivalent.
Figure D.5 uses positive loss in this code. The paper figure uses a signed mean of −0.6 bps; its text uses +0.6.
The schedule interval is a distribution across 10,000 schedules, not an uncertainty interval for the mean.

### Costs: failed size replication and proposed follow-up

The headline cost and dollar value above are raw software outputs. They are not validated economic loss estimates.
`annual_cost(-0.39, 0.01, 12)` returns 468 bps. The paper’s worked example states approximately 5 bps.
This exposes an unresolved factor-of-100 unit mismatch against that example.
The zero-threshold row also dominates the headline: impact −8.37734 and fixed-1%-trade cost 211,108.96 bps.
Its daily-reset signal is close to a scaled current return, which enters the same regression. The design is full rank.
This may make separate slope estimates unstable; it is not evidence of exact collinearity.
[Issue #30](https://github.com/jesusvillota/replicate/issues/30) requests a unit and identification audit.
The proxy alternative gives 5,552.08 bps, so proxy replacement does not resolve this failure.
No cost was rescaled, removed or replaced to match the paper.

Random tracking error is 37.4109 bps/year, near the paper’s approximately 35 bps.
This comparison does not validate the separate cost formula.

### Remaining core tables without numeric catalogue targets

The following are existing estimates. The catalogue supplies no paper target for these keys; comparisons remain unavailable.

| Exhibit/column | Threshold coefficient (t) | Cal × week4 coefficient (t) |
|---|---:|---:|
| table_D2/1 | -0.464414 (-3.899635) | -0.260256 (-3.179252) |
| table_D5/1 | -0.457335 (-3.411393) | -0.280223 (-3.056536) |
| table_D13/A1 | -0.368583 (-3.455851) | -0.245028 (-3.452627) |
| table_D13/B1 | 0.095832 (3.551138) | 0.015227 (1.234278) |

Table 6 net-of-trading-cost Sharpe ratio is 0.6576. Crisis-excluded Sharpe ratio is 0.5348.
These use the documented strategy execution-cost assumptions, separate from the failed rebalancing-cost calculation.
No extension exhibits were requested. Tables 4, 5, D.4, D.9, D.14 and Figures 1/5 remain outside this delivery.

### Reproducibility

Analysis revision: `07a995b2ccc54e37cbd86492cd720384f39d12dd` (merged main code).
Both robustness folders include lineage metadata. Main sidecars record module parameters, samples and output paths.
Processed panels and signal frames remain outside git under `~/data/replicate/processed/`.
The task outcome records verification, artifact counts, proposed follow-ups and the PR.
