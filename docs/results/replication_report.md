# Replication report

## Summary

Main-run output comparison with the paper.

- Target keys joined: 394/399
- Numeric targets joined: 388/399
- Sign-match rate: 92.5% (196/212 eligible targets)
- Significance-match rate: 83.1% (123/148 eligible targets)
- replicates (7): table_C2, table_D1, table_D3, table_D4, table_D6, table_D10, figure_D1
- partly (24): table_1, table_2a, table_2b, table_3, table_4, table_5, table_C1, table_D7, table_D8, table_D9, table_D11, table_D12, table_D14, figure_1, figure_2, figure_3, figure_4, figure_5, figure_D3, figure_D4, costs, table_6a, table_6b, table_6c
- fails (1): figure_D2
- not available (0): none
- not run (6): table_D2, table_D5, table_D13, figure_6, figure_C1, figure_D5

Targets: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/docs/results/targets.csv`. Inputs: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/tables`, `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/output/figures`.
Gap annotations: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-030/docs/results/gap_notes.csv`. Size tolerance: 25.0% relative, 0.0001 absolute (target units). Significance: abs(t) ≥ 1.96, from rebal.compare.

## Exhibit table

One row per contract ID, including text costs and strategy results (table_6a–table_6c). The status covers all primary targets; the headline is one named statistic. Missing values cannot establish a failed replication.

| exhibit | status | headline paper value | our value | note |
|---|---|---|---|---|
| table_1 | partly | -0.4144 | -0.464414 | 92/92 numeric targets; headline 1:threshold [coef] |
| table_2a | partly | -0.3281 | -0.368398 | 24/24 numeric targets; headline 1:threshold [coef] |
| table_2b | partly | -0.2723 | -0.351894 | 18/18 numeric targets; headline 1:threshold [coef] |
| table_3 | partly | -0.3302 | -0.368583 | 60/60 numeric targets; headline 1:threshold [coef] |
| table_4 | partly | -0.1809 | -0.173107 | 18/18 numeric targets; headline 1:threshold [coef] |
| table_5 | partly | -0.2054 | 5.81835e-05 | 12/12 numeric targets; headline 1:threshold [coef] |
| table_C1 | partly | 0.91 | 0.916567 | 10/10 numeric targets; headline calendar:ar1 [value] |
| table_C2 | replicates | 0.605 | 0.584193 | 4/4 numeric targets; headline calendar:threshold [value] |
| table_D1 | replicates | 0.1466 | 0.125714 | 4/4 numeric targets; headline 1:ret_1 [coef] |
| table_D2 | not run | N/A | N/A | 0/0 numeric targets; no numeric paper targets; status not assessed |
| table_D3 | replicates | 0.0006 | 0.000572684 | 6/6 numeric targets; headline 1:mom_fast [coef] |
| table_D4 | replicates | -0.397 | -0.449384 | 4/4 numeric targets; headline 1:threshold [coef] |
| table_D5 | not run | N/A | N/A | 0/0 numeric targets; no numeric paper targets; status not assessed |
| table_D6 | replicates | -0.3938 | -0.463537 | 4/4 numeric targets; headline 1:threshold [coef] |
| table_D7 | partly | -0.8453 | -0.383527 | 12/12 numeric targets; headline 1:threshold [coef] |
| table_D8 | partly | -0.4264 | -0.470275 | 6/6 numeric targets; headline 1:threshold_large [coef] |
| table_D9 | partly | -0.4493 | -0.491847 | 6/9 numeric targets; headline 1:threshold [coef]; not available: FEARS is private; ANcerno is licensed and unavailable |
| table_D10 | replicates | -0.0377 | -0.0309824 | 5/5 numeric targets; headline 1:rev_st [coef] |
| table_D11 | partly | -0.0159 | -0.096502 | 3/3 numeric targets; headline 1:eom_rev [coef] |
| table_D12 | partly | 0.2262 | 0.0746176 | 4/4 numeric targets; headline 1:calendar:week1 [coef] |
| table_D13 | not run | N/A | N/A | 0/0 numeric targets; no numeric paper targets; status not assessed |
| table_D14 | partly | -0.2723 | -0.668625 | 5/5 numeric targets; headline 1:threshold [coef] |
| figure_1 | partly | ~0.68 | 0.619532 | 3/3 numeric targets; headline equity_share:actual_max [value] |
| figure_2 | partly | ~-3.8 | -3.62997 | 4/4 numeric targets; headline delta_0.0_pct:threshold [t] |
| figure_3 | partly | ~-0.85 | 2.08786 | 10/10 numeric targets; headline days_1:calendar_interaction [t] |
| figure_4 | partly | ~-0.12 | -0.801446 | 6/6 numeric targets; headline day_15:threshold [coef] |
| figure_5 | partly | ~-0.1 | N/A | 10/12 numeric targets; headline ancerno:threshold [value]; not available: FEARS is private; ANcerno is licensed and unavailable |
| figure_6 | not run | ~2.3 | N/A | 0/2 numeric targets; headline sample_end:sp500 [value]; paper-only data: Figure 6 axis transformation is unresolved |
| figure_C1 | not run | N/A | N/A | 0/0 numeric targets; no numeric paper targets; status not assessed |
| figure_D1 | replicates | ~-4.5 | -3.73356 | 1/1 numeric targets; headline delta_1.8_pct:threshold [t] |
| figure_D2 | fails | ~-3.65 | 0.00249157 | 1/1 numeric targets; headline days_4:calendar_interaction [t] |
| figure_D3 | partly | ~-3.8 | -3.62997 | 4/4 numeric targets; headline delta_0.0_pct:during_rebalancing [t] |
| figure_D4 | partly | ~-0.42 | -0.464414 | 4/4 numeric targets; headline day_1:threshold [coef] |
| figure_D5 | not run | ~3.2 | N/A | 0/3 numeric targets; headline random:ci95_high_bps [value]; paper-only data: random-date cost sign conflicts between text and Figure D.5 |
| costs | partly | 8 | 1.22151 | 8/9 numeric targets; headline headline:annual_bps [value]; paper-only data: random-date cost sign conflicts between text and Figure D.5 |
| table_6a | partly | 1.11 | 0.734083 | 12/12 numeric targets; headline strategy:sharpe [value] |
| table_6b | partly | 9.64 | 5.7564 | 8/8 numeric targets; headline c4:alpha_pct_pa [coef] |
| table_6c | partly | 15.16 | 11.6837 | 20/20 numeric targets; headline epu:high_mean_pct_pa [coef] |

## Gap notes

Only checked-in annotations assign causes. Blank means no recorded cause. Notes preserve the historical core run, including its tentative explanations; they do not diagnose the current or synthetic run.

| exhibit | cause | note |
|---|---|---|
| table_1 | proxy | Historical core run: cash-market returns and control vintages are likely causes of small-control gaps. |
| table_1 | sample | Latest-sample result only: docs/results/latest_sample.md (TASK-032) extends the actual endpoint to 2026-07-31, with N=7152 versus paper-end 6317. Threshold changes -0.46441444537986687 to -0.4101349210644659; Cal x week4 changes -0.26025581705921746 to -0.2362462490035583. Both stay negative and significant but weaken, contrary to footnote 32. The cause is unknown. |
| table_2a | proxy | Historical core run: quarter-month subsets amplify proxy differences. |
| table_2a | sample | Historical core run: quarter-month subsets amplify sample differences. |
| table_2b | proxy | Historical core run: quarter-month subsets amplify proxy differences. |
| table_2b | sample | Historical core run: quarter-month subsets amplify sample differences. |
| table_3 | proxy | Historical core run: the bond proxy is the main candidate for the bond Calendar significance gap. |
| table_3 | sample | Latest-sample result only: docs/results/latest_sample.md (TASK-032) records all eight signs and 5% decisions unchanged through 2026-07-31. Coefficients move toward zero and absolute t statistics fall. Bond Calendar remains insignificant in both windows, unlike the paper. The cause of weaker results is unknown. |
| table_4 | sample | Final real run: docs/methods/long_sample.md records first outcome 1963-01-11 after the bond-history and momentum warm-up; N=14796/8478/6317 versus paper 15291/8870/6421. DGS10 before 1971 is a yield proxy. The Calendar subsample gap cause is unknown. |
| table_5 | proxy | Final real run: docs/methods/segments.md uses IWB/IWM/IWD/IWF total returns and 90/10 weights. Each pair has N=4109 versus paper 4175. The size effects do not replicate; the cause is unknown. ETF substitution and the panel calendar limit comparability. |
| table_C1 | proxy | Historical core run: distributions and correlations describe proxy signals rather than exact futures signals. |
| table_C2 | proxy | Historical core run: distributions and correlations describe proxy signals rather than exact futures signals. |
| table_D1 |  |  |
| table_D2 |  |  |
| table_D3 | proxy | Historical core run: sizes differ with proxy returns and signal distributions. |
| table_D4 | method | Final real run: docs/methods/robustness_extra.md rebuilds signals from the index pair and uses VBMFX rather than Bloomberg Aggregate returns. N=6317 versus paper 6226. These are documented differences; the coefficient-gap cause is unknown. |
| table_D5 |  |  |
| table_D6 | proxy | Historical core run: sizes differ with proxy returns and signal distributions. |
| table_D7 | proxy | Historical core run: sizes differ with proxy returns and signal distributions. |
| table_D8 | proxy | Historical core run: proxy measurement is a likely cause of the small-signal significance gap. |
| table_D8 | method | Historical core run: the small/large split is a likely cause of the significance gap. |
| table_D9 | data | Final real run: docs/methods/robustness_extra.md exports BEX columns 1/2 and ARA column 4; private FEARS column 3 is unavailable. BEX N=6317 versus paper 6124; ARA N=3843 versus 3903. Published control levels are retained. Residual gap causes are unknown. |
| table_D10 | timing | Historical core run: calendar alignment is a plausible cause of significance differences. |
| table_D10 | proxy | Historical core run: proxy returns are a plausible cause of significance differences. |
| table_D10 | sample | Historical core run: sample differences are a plausible cause of significance differences. |
| table_D11 | timing | Historical core run: calendar alignment is a plausible cause of significance differences. |
| table_D11 | proxy | Historical core run: proxy returns are a plausible cause of significance differences. |
| table_D11 | sample | Historical core run: sample differences are a plausible cause of significance differences. |
| table_D12 | timing | Historical core run: calendar alignment is a plausible cause of significance differences. |
| table_D12 | proxy | Historical core run: proxy returns are a plausible cause of significance differences. |
| table_D12 | sample | Historical core run: sample differences are a plausible cause of significance differences. |
| table_D13 |  |  |
| table_D14 | sample | Final real run: docs/methods/robustness_extra.md uses MSCI history from 2000-12-29 and N=5503 versus paper 6097. It uses one extra signal lag with the current week4 dummy and a compounded two-day stock control. These limits do not identify the large Threshold-gap cause; it is unknown. |
| figure_1 | sample | Final real run: docs/methods/pension.md uses asset-weighted allocations and changing observed contributor sets in 2003-2022. There are 253 source rows per year but 172-228 actual and 136-234 target contributors. Actual min/max and typical target differ substantially from the paper. The exact cause is unknown; coverage and source vintage are candidates, not established causes. |
| figure_2 | timing | Historical core run: timing matters for exact threshold readings. |
| figure_2 | proxy | Historical core run: proxy construction matters for exact threshold readings. |
| figure_2 | timing | Final real run: output/figures/robustness/literal/figure_2.csv reruns delayed-reset timing. docs/methods/comparison.md defines the first sampled delta below abs(t)=2.58. Timing sensitivity is observed; it does not by itself establish the cause of the paper-grid gap. |
| figure_3 | timing | Historical core run: close times, month-end calendars and timing are leading candidates for the four-day-window gap. |
| figure_3 | method | Final real run: docs/methods/comparison.md now joins computed days_N calendar_interaction t statistics through the canonical sidecar. docs/methods/horizons.md records window construction. New comparison coverage is an export change, not a changed estimate; the paper-gap cause is unknown. |
| figure_4 | proxy | Historical core run: proxy close times are a plausible cause of horizon differences. |
| figure_4 | method | Historical core run: horizon and error conventions in paper-notes section 5 are plausible causes. |
| figure_4 | method | Final real run: docs/methods/comparison.md joins exact plotted coefficients and the first sampled horizon whose 95% band contains zero. docs/methods/horizons.md records overlapping-horizon errors. Coverage changed after TASK-023; the paper-gap cause is unknown. |
| figure_5 | data | Final real run: docs/methods/trading_corr.md uses 867 COT pairs, 125 LTPos pairs and 194 ICI pairs per signal. ICI pools within recovered blocks without bridging missing intervals; ANcerno is unavailable. All ten available correlation signs agree. Source coverage and lag conventions limit magnitude comparisons; the residual-gap cause is unknown. |
| figure_6 | proxy | Historical core run: proxy returns can contribute to strategy differences. |
| figure_6 | method | Historical core run: the documented Calendar-reversal reading can contribute to strategy differences. |
| figure_6 | method | Final real run: docs/methods/comparison.md leaves both canonical terminal targets blank because the paper axis transformation is unresolved. The computed gross strategy plot remains available. No wealth/log conversion is invented. |
| figure_C1 | proxy | Historical core run: distributions and correlations describe proxy signals rather than exact futures signals. |
| figure_D1 | timing | Historical core run: timing matters for exact threshold readings. |
| figure_D1 | proxy | Historical core run: proxy construction matters for exact threshold readings. |
| figure_D1 | method | Final real run: docs/methods/comparison.md joins the delta_1.8_pct Threshold t statistic through the canonical sidecar; the figure uses HAC errors as documented in docs/methods/horizons.md. Export coverage changed after TASK-023; the remaining paper-gap cause is unknown. |
| figure_D2 | timing | Historical core run: close times, month-end calendars and timing are leading candidates for the four-day-window gap. |
| figure_D2 | method | Final real run: docs/methods/comparison.md joins the days_4 calendar_interaction t statistic from its canonical sidecar. The documented HAC window estimate is retained. Export coverage changed after TASK-023; the paper-gap cause is unknown. |
| figure_D3 | method | Final real run: docs/methods/comparison.md maps during/outside-rebalancing t statistics to explicit delta keys. Undefined subset estimates remain blank. These are new export comparisons; the paper-gap cause is unknown. |
| figure_D4 | proxy | Historical core run: proxy close times are a plausible cause of horizon differences. |
| figure_D4 | method | Historical core run: horizon and error conventions in paper-notes section 5 are plausible causes. |
| figure_D4 | method | Final real run: docs/methods/comparison.md joins exact plotted day_1/day_2 coefficients via the canonical sidecar. The estimation method in docs/methods/horizons.md is unchanged. New coverage does not identify the paper-gap cause; it is unknown. |
| figure_D5 | method | Historical core run: unit mismatch and extreme delta=0 costs required review; TASK-022 later corrected units and excluded delta=0 from summaries. |
| figure_D5 | method | Final real run: corrected cost units are documented in docs/methods/costs.md. The paper text reports +0.6 bps while its chart legend reports -0.6 bps. As docs/methods/comparison.md requires, the three canonical chart targets remain blank; raw 10000-draw results remain in figure_D5.csv. |
| costs | method | Historical core run: unit mismatch and extreme delta=0 costs required review; TASK-022 later corrected units and excluded delta=0 from summaries. |
| costs | method | Final real run: docs/methods/costs.md applies the corrected squared-trade-share formula and DEC-005 excludes delta=0 from summary means while retaining raw estimates. This directly explains the change from TASK-018 units and headline. The remaining gap from the paper is not resolved by that correction. |
| costs | proxy | Final real run: robustness/proxy_alt/costs.csv reruns the same corrected cost method on daily_panel_alt.parquet with 10000 random schedules and seed 16. The comparison measures proxy sensitivity; it does not establish why the paper headline differs. |
| table_6a | proxy | Historical core run: proxy returns can contribute to strategy differences. |
| table_6a | method | Historical core run: the documented Calendar-reversal reading can contribute to strategy differences. |
| table_6a | method | Final real run: docs/methods/comparison.md maps strategy mean/volatility/Sharpe keys without extra annualization. docs/methods/strategy.md records Calendar reversal and gross returns. New comparison coverage is an export change; the Sharpe-gap cause is unknown. |
| table_6b | proxy | Historical core run: proxy returns can contribute to strategy differences. |
| table_6b | method | Historical core run: the documented Calendar-reversal reading can contribute to strategy differences. |
| table_6b | method | Final real run: docs/methods/comparison.md maps lowercase factor-model keys and annual percentage-point alpha without rescaling. docs/methods/strategy.md records estimation. New comparison coverage is an export change; the alpha-gap cause is unknown. |
| table_6c | proxy | Historical core run: proxy returns can contribute to strategy differences. |
| table_6c | method | Historical core run: the documented Calendar-reversal reading can contribute to strategy differences. |
| table_6c | method | Final real run: docs/methods/comparison.md maps high/low control-state returns without rescaling. docs/methods/strategy.md records state splits. New comparison coverage is an export change; remaining gap causes are unknown. |

Skipped comparison inputs:

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

## Data and proxies

[Master source map](../data/sources.md) · [Proxy comparison](../data/proxy_comparison.md)

| dataset | variable | our source or proxy | class | availability | source card |
|---|---|---|---|---|---|
| D1 | Equity futures return R^SP | DEC-001 main E1: CRSP CIZ SPY distribution-inclusive `ret` minus French RF. Robustness E2: Yahoo `^SP500TR` return minus RF. [CRSP](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/); [Yahoo chart](https://query2.finance.yahoo.com/v8/finance/chart/%5ESP500TR) | proxy | available | [CRSP](../data/cards/crsp.md), [Yahoo](../data/cards/yahoo.md), [French](../data/cards/french.md) |
| D2 | Bond futures return R^10Y | DEC-001 main T3: GSW 6.5-year zero-coupon holding return minus French RF. Robustness T2: GSW 10-year par-bond holding return minus RF. [Fed GSW curve](https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv) | proxy | available | [GSW](../data/cards/gsw.md), [French](../data/cards/french.md) |
| D3 | Holiday calendar | Common observed days of the DEC-001 main pair, excluding 2001-09-11 through 2001-09-14; the alternative uses these same dates; derived by `rebal.panel` | proxy | available | [Calendar](../data/cards/calendar.md) |
| D4 | S&P 500 Total Return Index | Yahoo `^SP500TR`, the S&P 500 Total Return Index; [daily chart](https://query2.finance.yahoo.com/v8/finance/chart/%5ESP500TR). CRSP SPY supplies an overlap check | exact | available | [Yahoo](../data/cards/yahoo.md), [CRSP](../data/cards/crsp.md) |
| D5 | Bloomberg U.S. Aggregate Bond TR Index | Yahoo VBMFX distribution-adjusted daily total returns; [daily chart](https://query2.finance.yahoo.com/v8/finance/chart/VBMFX). Full-study history; no splice. WRDS 2004–2006 sample is only a check | proxy | available | [Bond funds / WRDS](../data/cards/wrds.md) |
| D6 | MSCI ACWI ex USA Net TR (USD) | MSCI code `899901`, USD `NETR`, daily levels; [downloadLevelData](https://app2.msci.com/products/service/index/indexmaster/downloadLevelData). Source-day returns; no ETF splice | exact | partial (levels 2000-12-29–2026-10-20; no 1997–2000 history) | [MSCI](../data/cards/msci.md) |
| D7 | U.S. 3-month T-bill | FRED `DTB3`; [CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3), archived official CSV when live endpoint is unavailable | exact | available | [FRED](../data/cards/fred.md) |
| D8 | VIX | FRED `VIXCLS` (CBOE), divided by 100; [CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS), archived official CSV when needed | exact | available | [FRED](../data/cards/fred.md) |
| D9 | MOVE | Yahoo `^MOVE`, divided by 100; [daily chart](https://query2.finance.yahoo.com/v8/finance/chart/%5EMOVE); early gap remains missing | exact | partial (2002-11-12–2026-10-21) | [Yahoo](../data/cards/yahoo.md) |
| D10 | EPU | Baker, Bloom and Davis US daily news EPU; [official CSV](https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv) | exact | available | [EPU](../data/cards/epu.md) |
| D11 | ADS | Philadelphia Fed ADS, latest revised vintage; [official workbook](https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/ads/ADS_Index_Most_Current_Vintage.xlsx) | exact | available | [ADS](../data/cards/ads.md) |
| D12 | Sentiment | SF Fed Daily News Sentiment Index; [official workbook](https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx) | exact | available | [Sentiment](../data/cards/sentiment.md) |
| D13 | ra^BEX, unc^BEX | BEX `ra` and monthly-variance `unc`, current revised daily workbook; [Nancy Xu data page](https://www.nancyxu.net/risk-aversion-index) | exact | available | [BEX](../data/cards/bex.md) |
| D14 | FEARS | Archived public Da–Engelberg–Gao FEARS subset, `fears25`, `fears30`, `fears35`; [author CSV archive](https://web.archive.org/web/20230627055206id_/https://www3.nd.edu/~zda/fears_post_20140512.csv). Private extension unavailable; skip full-sample Table D.9 column | exact (public subset only) | partial (2004-07-01–2011-12-30; private extension unavailable) | [FEARS](../data/cards/fears.md) |
| D15 | ARA (aggregate retail attention) | Da, Hua, Hung and Peng published `ara`; [Lin Peng coauthor data page](https://sites.google.com/site/linpengbaruch/data), public Dropbox archive | exact | partial (2004-07-01–2019-12-31) | [ARA](../data/cards/ara.md) |
| D16 | Long-sample equity return | Kenneth French daily `(Mkt-RF + RF) / 100`; [three-factor ZIP](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip) | exact | available | [French](../data/cards/french.md) |
| D17 | Long-sample 10-year bond return | [Fed GSW curve](https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv), converted to a 10-year zero-coupon holding return with `rebal.proxies` | exact source; constructed return | partial (10-year yields observed 1971-08-16–2026-10-16; earlier file rows do not supply 10-year yields) | [GSW](../data/cards/gsw.md) |
| D18 | Russell 1000, 2000, 1000 Value, 1000 Growth | CRSP CIZ distribution-inclusive `ret` for IWB, IWM, IWD, IWF; [WRDS CRSP](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/), extracted through tape-kit | proxy | partial (IWB 2000-05-19; IWM/IWD/IWF 2000-05-26; all through 2026-07-31) | [CRSP](../data/cards/crsp.md) |
| D19 | CFTC Commitments of Traders (COT) | CFTC futures-only legacy COT and TFF; [official history](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm), `deacot<YYYY>.zip` and `fin_fut_txt_*.zip` | exact | partial (legacy 1997-01-07–2026-10-13; TFF 2006-06-13–2026-10-13; full-size S&P stops 2021-09-14) | [CFTC](../data/cards/cftc.md) |
| D20 | CFTC Large Trader Net Position Changes (LTPos) | CFTC official LTPos [CSV](https://www.cftc.gov/idc/groups/public/@marketreports/documents/file/lgtraderpos-csv.csv); signed buys minus sells, contracts per day | exact | available | [CFTC](../data/cards/cftc.md) |
| D21 | ANcerno institutional trades | No ANcerno table found in the live WRDS catalog; omit institutional-trade replication | none | not available (licensed discontinued product; no WRDS catalog match) | [WRDS](../data/cards/wrds.md) |
| D22 | ICI flows | ICI estimated weekly long-term flows, domestic equity and bond; [official release](https://www.ici.org/research/stats/flows), official XLS/PDF archives listed in `src/rebal/fetch/ici_archives.csv` | exact | partial (278 weekly observations in 39 blocks, 2008-12-03–2026-10-14; missing 2007–2008 and later gaps) | [ICI](../data/cards/ici.md) |
| D23 | Pension allocations | CRR Public Plans Data [API](https://publicplansdata.org/api/) and [detailed investment workbook](https://publicplansdata.org/wp-content/uploads/2024/09/PensionInvestmentPerformanceDetailed.xlsx) | exact | available | [PPD](../data/cards/ppd.md) |
| D24 | Factor returns | [French daily library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html): FF3, FF5, momentum, short/long reversal; [Global-q daily q5](https://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2025.csv) | exact | available | [French](../data/cards/french.md), [HXZ](../data/cards/hxz.md) |
| D25 | CRSP daily stock returns | Licensed CRSP CIZ daily common-stock returns, historical share codes 10/11; sample cross-sectional SD from tape-kit [WRDS CRSP](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/) | exact | available | [CRSP](../data/cards/crsp.md) |
| D26 | BofA Global Financial Stress Index (GFSI) Liquidity Risk | Hu–Pan–Wang `Noise_bp`; [Jun Pan official workbook](https://en.saif.sjtu.edu.cn/junpan/Noise_Measure_2025.xlsx). Chosen because it covers 1997–2023; OFR Funding is an unused fallback | proxy | available | [HPW](../data/cards/hpw.md), [OFR fallback](../data/cards/ofr.md) |
| D27 | Dollar-scaling constants | Dated paper constants from [Fed Z1](https://www.federalreserve.gov/releases/z1/), [CRS R47699](https://crsreports.congress.gov/product/pdf/R/R47699), [SCF](https://www.federalreserve.gov/econres/scfindex.htm), [Census](https://www.census.gov/data/tables/time-series/demo/families/households.html), [ICI 2025 Q2](https://www.ici.org/statistical-report/ret_25_q2); documented in [costs](../methods/costs.md) | exact (paper constants) | available | [Scaling constants](../data/cards/scaling_constants.md) |
| D28 | Surveys and qualitative evidence | Paper §1.1 and §2.3 qualitative source descriptions: NASRA, pension memos, Vanguard, NBIM and the 2024-06-19 roundtable; documentation only | none | not available (qualitative evidence; numerical replication out of scope) | [Qualitative evidence](../data/cards/qualitative.md) |

## Method choices

- [comparison.md](../methods/comparison.md)
- [costs.md](../methods/costs.md)
- [horizons.md](../methods/horizons.md)
- [ivol.md](../methods/ivol.md)
- [latest_sample.md](../methods/latest_sample.md)
- [long_sample.md](../methods/long_sample.md)
- [panel.md](../methods/panel.md)
- [pension.md](../methods/pension.md)
- [proxies.md](../methods/proxies.md)
- [regressions.md](../methods/regressions.md)
- [report.md](../methods/report.md)
- [robustness_extra.md](../methods/robustness_extra.md)
- [segments.md](../methods/segments.md)
- [signals.md](../methods/signals.md)
- [strategy.md](../methods/strategy.md)
- [trading_corr.md](../methods/trading_corr.md)

## Latest sample (footnote 32)

[Latest-sample comparison](../../output/tables/robustness/latest/latest_comparison.csv). Table 1 compares paper_end with latest; sample dates are actual outcome dates.

| exhibit | column | term | stat | sample | value |
|---|---|---|---|---|---|
| table_1 | 1 | threshold | coef | paper_end | -0.46441444537986687 |
| table_1 | 1 | threshold | se | paper_end | 0.11575294423394449 |
| table_1 | 1 | threshold | t | paper_end | -4.012117777680489 |
| table_1 | 1 | threshold | nobs | paper_end | 6317 |
| table_1 | 1 | threshold | sample_start | paper_end | 1997-09-11 |
| table_1 | 1 | threshold | sample_end | paper_end | 2023-03-17 |
| table_1 | 1 | calendar:week4 | coef | paper_end | -0.26025581705921746 |
| table_1 | 1 | calendar:week4 | se | paper_end | 0.07612728958494706 |
| table_1 | 1 | calendar:week4 | t | paper_end | -3.418692803568286 |
| table_1 | 1 | calendar:week4 | nobs | paper_end | 6317 |
| table_1 | 1 | calendar:week4 | sample_start | paper_end | 1997-09-11 |
| table_1 | 1 | calendar:week4 | sample_end | paper_end | 2023-03-17 |
| table_1 | 2 | threshold | coef | paper_end | -0.45423891397538146 |
| table_1 | 2 | threshold | se | paper_end | 0.134812995516382 |
| table_1 | 2 | threshold | t | paper_end | -3.3694000510520805 |
| table_1 | 2 | threshold | nobs | paper_end | 5043 |
| table_1 | 2 | threshold | sample_start | paper_end | 2002-11-14 |
| table_1 | 2 | threshold | sample_end | paper_end | 2023-03-17 |
| table_1 | 2 | calendar:week4 | coef | paper_end | -0.2802191658157103 |
| table_1 | 2 | calendar:week4 | se | paper_end | 0.09155611489325852 |
| table_1 | 2 | calendar:week4 | t | paper_end | -3.0606275303665544 |
| table_1 | 2 | calendar:week4 | nobs | paper_end | 5043 |
| table_1 | 2 | calendar:week4 | sample_start | paper_end | 2002-11-14 |
| table_1 | 2 | calendar:week4 | sample_end | paper_end | 2023-03-17 |
| table_1 | 3 | threshold | coef | paper_end | -0.4750372989106889 |
| table_1 | 3 | threshold | se | paper_end | 0.11308634818672872 |
| table_1 | 3 | threshold | t | paper_end | -4.200659995902468 |
| table_1 | 3 | threshold | nobs | paper_end | 6317 |
| table_1 | 3 | threshold | sample_start | paper_end | 1997-09-11 |
| table_1 | 3 | threshold | sample_end | paper_end | 2023-03-17 |
| table_1 | 3 | calendar:week4 | coef | paper_end | -0.26069860784404336 |
| table_1 | 3 | calendar:week4 | se | paper_end | 0.07565377420149139 |
| table_1 | 3 | calendar:week4 | t | paper_end | -3.4459431878403777 |
| table_1 | 3 | calendar:week4 | nobs | paper_end | 6317 |
| table_1 | 3 | calendar:week4 | sample_start | paper_end | 1997-09-11 |
| table_1 | 3 | calendar:week4 | sample_end | paper_end | 2023-03-17 |
| table_1 | 4 | threshold | coef | paper_end | -0.471350996587544 |
| table_1 | 4 | threshold | se | paper_end | 0.1146154010968456 |
| table_1 | 4 | threshold | t | paper_end | -4.112457768125512 |
| table_1 | 4 | threshold | nobs | paper_end | 6317 |
| table_1 | 4 | threshold | sample_start | paper_end | 1997-09-11 |
| table_1 | 4 | threshold | sample_end | paper_end | 2023-03-17 |
| table_1 | 4 | calendar:week4 | coef | paper_end | -0.2608436502270011 |
| table_1 | 4 | calendar:week4 | se | paper_end | 0.07591234492784421 |
| table_1 | 4 | calendar:week4 | t | paper_end | -3.4361163586098784 |
| table_1 | 4 | calendar:week4 | nobs | paper_end | 6317 |
| table_1 | 4 | calendar:week4 | sample_start | paper_end | 1997-09-11 |
| table_1 | 4 | calendar:week4 | sample_end | paper_end | 2023-03-17 |
| table_1 | 5 | threshold | coef | paper_end | -0.4531130140223321 |
| table_1 | 5 | threshold | se | paper_end | 0.13354865427155208 |
| table_1 | 5 | threshold | t | paper_end | -3.392868438052484 |
| table_1 | 5 | threshold | nobs | paper_end | 5043 |
| table_1 | 5 | threshold | sample_start | paper_end | 2002-11-14 |
| table_1 | 5 | threshold | sample_end | paper_end | 2023-03-17 |
| table_1 | 5 | calendar:week4 | coef | paper_end | -0.28015076868501965 |
| table_1 | 5 | calendar:week4 | se | paper_end | 0.09153893342606692 |
| table_1 | 5 | calendar:week4 | t | paper_end | -3.060454805400245 |
| table_1 | 5 | calendar:week4 | nobs | paper_end | 5043 |
| table_1 | 5 | calendar:week4 | sample_start | paper_end | 2002-11-14 |
| table_1 | 5 | calendar:week4 | sample_end | paper_end | 2023-03-17 |
| table_1 | 1 | threshold | coef | latest | -0.4101349210644659 |
| table_1 | 1 | threshold | se | latest | 0.10936162870972839 |
| table_1 | 1 | threshold | t | latest | -3.7502634690368497 |
| table_1 | 1 | threshold | nobs | latest | 7152 |
| table_1 | 1 | threshold | sample_start | latest | 1997-09-11 |
| table_1 | 1 | threshold | sample_end | latest | 2026-07-31 |
| table_1 | 1 | calendar:week4 | coef | latest | -0.2362462490035583 |
| table_1 | 1 | calendar:week4 | se | latest | 0.07320189737061752 |
| table_1 | 1 | calendar:week4 | t | latest | -3.2273241198579243 |
| table_1 | 1 | calendar:week4 | nobs | latest | 7152 |
| table_1 | 1 | calendar:week4 | sample_start | latest | 1997-09-11 |
| table_1 | 1 | calendar:week4 | sample_end | latest | 2026-07-31 |
| table_1 | 2 | threshold | coef | latest | -0.3868993765849918 |
| table_1 | 2 | threshold | se | latest | 0.12519693844967486 |
| table_1 | 2 | threshold | t | latest | -3.090326180304424 |
| table_1 | 2 | threshold | nobs | latest | 5878 |
| table_1 | 2 | threshold | sample_start | latest | 2002-11-14 |
| table_1 | 2 | threshold | sample_end | latest | 2026-07-31 |
| table_1 | 2 | calendar:week4 | coef | latest | -0.24891959856609716 |
| table_1 | 2 | calendar:week4 | se | latest | 0.08692611066532892 |
| table_1 | 2 | calendar:week4 | t | latest | -2.863576854651343 |
| table_1 | 2 | calendar:week4 | nobs | latest | 5878 |
| table_1 | 2 | calendar:week4 | sample_start | latest | 2002-11-14 |
| table_1 | 2 | calendar:week4 | sample_end | latest | 2026-07-31 |
| table_1 | 3 | threshold | coef | latest | -0.4196023156003738 |
| table_1 | 3 | threshold | se | latest | 0.10690421616476821 |
| table_1 | 3 | threshold | t | latest | -3.925030561504268 |
| table_1 | 3 | threshold | nobs | latest | 7152 |
| table_1 | 3 | threshold | sample_start | latest | 1997-09-11 |
| table_1 | 3 | threshold | sample_end | latest | 2026-07-31 |
| table_1 | 3 | calendar:week4 | coef | latest | -0.23723586369457048 |
| table_1 | 3 | calendar:week4 | se | latest | 0.07283972908400813 |
| table_1 | 3 | calendar:week4 | t | latest | -3.25695697496293 |
| table_1 | 3 | calendar:week4 | nobs | latest | 7152 |
| table_1 | 3 | calendar:week4 | sample_start | latest | 1997-09-11 |
| table_1 | 3 | calendar:week4 | sample_end | latest | 2026-07-31 |
| table_1 | 4 | threshold | coef | latest | -0.418820934222676 |
| table_1 | 4 | threshold | se | latest | 0.10828877822258287 |
| table_1 | 4 | threshold | t | latest | -3.8676300637708536 |
| table_1 | 4 | threshold | nobs | latest | 7152 |
| table_1 | 4 | threshold | sample_start | latest | 1997-09-11 |
| table_1 | 4 | threshold | sample_end | latest | 2026-07-31 |
| table_1 | 4 | calendar:week4 | coef | latest | -0.2370157043554433 |
| table_1 | 4 | calendar:week4 | se | latest | 0.07297298952621772 |
| table_1 | 4 | calendar:week4 | t | latest | -3.2479922488345956 |
| table_1 | 4 | calendar:week4 | nobs | latest | 7152 |
| table_1 | 4 | calendar:week4 | sample_start | latest | 1997-09-11 |
| table_1 | 4 | calendar:week4 | sample_end | latest | 2026-07-31 |
| table_1 | 5 | threshold | coef | latest | -0.38682231105008325 |
| table_1 | 5 | threshold | se | latest | 0.12449901281175886 |
| table_1 | 5 | threshold | t | latest | -3.1070311508008044 |
| table_1 | 5 | threshold | nobs | latest | 5878 |
| table_1 | 5 | threshold | sample_start | latest | 2002-11-14 |
| table_1 | 5 | threshold | sample_end | latest | 2026-07-31 |
| table_1 | 5 | calendar:week4 | coef | latest | -0.24878089150164273 |
| table_1 | 5 | calendar:week4 | se | latest | 0.08690052659429458 |
| table_1 | 5 | calendar:week4 | t | latest | -2.862823750920473 |
| table_1 | 5 | calendar:week4 | nobs | latest | 5878 |
| table_1 | 5 | calendar:week4 | sample_start | latest | 2002-11-14 |
| table_1 | 5 | calendar:week4 | sample_end | latest | 2026-07-31 |

