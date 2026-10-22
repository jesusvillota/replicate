# Master source map

The authors' source column quotes [paper-notes §2](../../goals/hmm-rebalancing/paper-notes.md#2-data-inventory).
TASK-012 records the fetched sources and the choices accepted in
[DEC-001](../../goals/hmm-rebalancing/decisions/DEC-001.md) and
[DEC-002](../../goals/hmm-rebalancing/decisions/DEC-002.md).
Coverage and access limits come from the linked source cards.
Panel transforms are defined in [panel methods](../methods/panel.md).

| D | Variable | Authors' source | Used in (exhibits) | Our source | Exact or proxy | Fetch task | Storage | Status | Source card |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Equity futures return R^SP | “Bloomberg generic ES1/ES2. "We construct continuous return series for the E-mini S&P 500 futures (ES) and the 10-year U.S. Treasury note futures (TY) using Bloomberg's nearby contracts … reported by Bloomberg as excess return price indices" (App. A, p.54)” | all main-sample exhibits | DEC-001 main E1: CRSP CIZ SPY distribution-inclusive `ret` minus French RF. Robustness E2: Yahoo `^SP500TR` return minus RF. [CRSP](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/); [Yahoo chart](https://query2.finance.yahoo.com/v8/finance/chart/%5ESP500TR) | proxy | TASK-006, TASK-009, TASK-011 | $REPLICATE_DATA_DIR/licensed/crsp/etf_daily.parquet; $REPLICATE_DATA_DIR/licensed/yahoo/^SP500TR.csv; data/public/french/ | available | [CRSP](cards/crsp.md), [Yahoo](cards/yahoo.md), [French](cards/french.md) |
| D2 | Bond futures return R^10Y | “Bloomberg TY1/TY2, built the same way” | as D1 | DEC-001 main T3: GSW 6.5-year zero-coupon holding return minus French RF. Robustness T2: GSW 10-year par-bond holding return minus RF. [Fed GSW curve](https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv) | proxy | TASK-003, TASK-006, TASK-009, TASK-010, TASK-011 | data/public/gsw/; data/public/french/ | available | [GSW](cards/gsw.md), [French](cards/french.md) |
| D3 | Holiday calendar | “"a holiday was identified whenever both front contracts, TY1 and ES1, were reported as N/A … we explicitly marked September 12–14, 2001, as exchange closures" (p.54)” | sample definition | Common observed days of the DEC-001 main pair, excluding 2001-09-11 through 2001-09-14; the alternative uses these same dates; derived by `rebal.panel` | proxy | TASK-012 | $REPLICATE_DATA_DIR/processed/daily_panel.parquet; $REPLICATE_DATA_DIR/processed/daily_panel_alt.parquet | available | [Calendar](cards/calendar.md) |
| D4 | S&P 500 Total Return Index | “Bloomberg (p.54)” | Tables D.4, D.11 | Yahoo `^SP500TR`, the S&P 500 Total Return Index; [daily chart](https://query2.finance.yahoo.com/v8/finance/chart/%5ESP500TR). CRSP SPY supplies an overlap check | exact | TASK-006, TASK-009 | $REPLICATE_DATA_DIR/licensed/yahoo/^SP500TR.csv | available | [Yahoo](cards/yahoo.md), [CRSP](cards/crsp.md) |
| D5 | Bloomberg U.S. Aggregate Bond TR Index | “Bloomberg (p.54)” | Table D.4 | Yahoo VBMFX distribution-adjusted daily total returns; [daily chart](https://query2.finance.yahoo.com/v8/finance/chart/VBMFX). Full-study history; no splice. WRDS 2004–2006 sample is only a check | proxy | TASK-009, TASK-010 | $REPLICATE_DATA_DIR/licensed/yahoo_bond_funds/VBMFX_daily.parquet | available | [Bond funds / WRDS](cards/wrds.md) |
| D6 | MSCI ACWI ex USA Net TR (USD) | “Bloomberg (p.54)” | Table D.14 | MSCI code `899901`, USD `NETR`, daily levels; [downloadLevelData](https://app2.msci.com/products/service/index/indexmaster/downloadLevelData). Source-day returns; no ETF splice | exact | TASK-006, TASK-009 | $REPLICATE_DATA_DIR/licensed/msci/acwi_ex_usa_net_usd.csv | partial (levels 2000-12-29–2026-10-20; no 1997–2000 history) | [MSCI](cards/msci.md) |
| D7 | U.S. 3-month T-bill | “not named” | Table D.14 | FRED `DTB3`; [CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3), archived official CSV when live endpoint is unavailable | exact | TASK-003 | data/public/fred/DTB3.csv | available | [FRED](cards/fred.md) |
| D8 | VIX | “Bloomberg "VIX Index" (CBOE), divided by 100” | Tables 1, 3, 6C, D.2–D.6, D.8, D.13, D.14 | FRED `VIXCLS` (CBOE), divided by 100; [CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS), archived official CSV when needed | exact | TASK-003 | data/public/fred/VIXCLS.csv | available | [FRED](cards/fred.md) |
| D9 | MOVE | “Bloomberg "MOVE Index" (ICE BofA), divided by 100” | as D8 | Yahoo `^MOVE`, divided by 100; [daily chart](https://query2.finance.yahoo.com/v8/finance/chart/%5EMOVE); early gap remains missing | exact | TASK-006 | $REPLICATE_DATA_DIR/licensed/yahoo/^MOVE.csv | partial (2002-11-12–2026-10-21) | [Yahoo](cards/yahoo.md) |
| D10 | EPU | “Baker, Bloom and Davis (2016) daily news-based index (p.18)” | Tables 1, 6C, others | Baker, Bloom and Davis US daily news EPU; [official CSV](https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv) | exact | TASK-004 | data/public/epu/epu.csv | available | [EPU](cards/epu.md) |
| D11 | ADS | “Aruoba, Diebold and Scotti (2009) index (Philadelphia Fed)” | Table 1, others | Philadelphia Fed ADS, latest revised vintage; [official workbook](https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/ads/ADS_Index_Most_Current_Vintage.xlsx) | exact | TASK-004 | data/public/ads/ads.csv | available | [ADS](cards/ads.md) |
| D12 | Sentiment | “Shapiro, Sudhof and Wilson (2022) daily news sentiment (SF Fed)” | Table 1, others | SF Fed Daily News Sentiment Index; [official workbook](https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx) | exact | TASK-004 | data/public/sentiment/sentiment.csv | available | [Sentiment](cards/sentiment.md) |
| D13 | ra^BEX, unc^BEX | “Bekaert, Engstrom and Xu (2022) risk aversion and uncertainty” | Table D.9 | BEX `ra` and monthly-variance `unc`, current revised daily workbook; [Nancy Xu data page](https://www.nancyxu.net/risk-aversion-index) | exact | TASK-004 | $REPLICATE_DATA_DIR/licensed/bex/bex.csv | available | [BEX](cards/bex.md) |
| D14 | FEARS | “Da, Engelberg and Gao (2015). The authors got it privately (footnote 23)” | Table D.9 | Archived public Da–Engelberg–Gao FEARS subset, `fears25`, `fears30`, `fears35`; [author CSV archive](https://web.archive.org/web/20230627055206id_/https://www3.nd.edu/~zda/fears_post_20140512.csv). Private extension unavailable; skip full-sample Table D.9 column | exact (public subset only) | TASK-004 | $REPLICATE_DATA_DIR/licensed/fears/fears.csv | partial (2004-07-01–2011-12-30; private extension unavailable) | [FEARS](cards/fears.md) |
| D15 | ARA (aggregate retail attention) | “Da, Hua, Hung and Peng (2025)” | Table D.9 | Da, Hua, Hung and Peng published `ara`; [Lin Peng coauthor data page](https://sites.google.com/site/linpengbaruch/data), public Dropbox archive | exact | TASK-004 | $REPLICATE_DATA_DIR/licensed/ara/ara.csv | partial (2004-07-01–2019-12-31) | [ARA](cards/ara.md) |
| D16 | Long-sample equity return | “"daily U.S. equity market total returns from Kenneth French's database"” | Table 4 | Kenneth French daily `(Mkt-RF + RF) / 100`; [three-factor ZIP](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip) | exact | TASK-005 | data/public/french/F-F_Research_Data_Factors_daily.csv | available | [French](cards/french.md) |
| D17 | Long-sample 10-year bond return | “"Federal Reserve Board Treasury data"; Table 4 note: Gürkaynak, Sack and Wright (2007) (GSW) yield curve” | Table 4 | [Fed GSW curve](https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv), converted to a 10-year zero-coupon holding return with `rebal.proxies` | exact source; constructed return | TASK-003 | data/public/gsw/ | partial (10-year yields observed 1971-08-16–2026-10-16; earlier file rows do not supply 10-year yields) | [GSW](cards/gsw.md) |
| D18 | Russell 1000, 2000, 1000 Value, 1000 Growth | “not named; likely Bloomberg; price or total return not stated” | Table 5 | CRSP CIZ distribution-inclusive `ret` for IWB, IWM, IWD, IWF; [WRDS CRSP](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/), extracted through tape-kit | proxy | TASK-006, TASK-009 | $REPLICATE_DATA_DIR/licensed/crsp/etf_daily.parquet | partial (IWB 2000-05-19; IWM/IWD/IWF 2000-05-26; all through 2026-07-31) | [CRSP](cards/crsp.md) |
| D19 | CFTC Commitments of Traders (COT) | “"weekly Commitment of Traders (COT) reports". Commercial = hedgers, non-commercial = speculators. Net positions and open interest” | Figure 5 | CFTC futures-only legacy COT and TFF; [official history](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm), `deacot<YYYY>.zip` and `fin_fut_txt_*.zip` | exact | TASK-007 | data/public/cftc/cot_legacy.csv; data/public/cftc/tff.csv | partial (legacy 1997-01-07–2026-10-13; TFF 2006-06-13–2026-10-13; full-size S&P stops 2021-09-14) | [CFTC](cards/cftc.md) |
| D20 | CFTC Large Trader Net Position Changes (LTPos) | “"Published by the CFTC on June 30, 2011, this one-time report covers the period from January 2009 to May 2011 and provides the daily average aggregate net position changes for large traders across 35 futures markets" (p.28)” | Figure 5 | CFTC official LTPos [CSV](https://www.cftc.gov/idc/groups/public/@marketreports/documents/file/lgtraderpos-csv.csv); signed buys minus sells, contracts per day | exact | TASK-007 | data/public/cftc/ltpos.csv | available | [CFTC](cards/cftc.md) |
| D21 | ANcerno institutional trades | “daily trade-level equity transactions, about 8% of CRSP volume (p.29)” | Figure 5 | No ANcerno table found in the live WRDS catalog; omit institutional-trade replication | none | TASK-010 | none | not available (licensed discontinued product; no WRDS catalog match) | [WRDS](cards/wrds.md) |
| D22 | ICI flows | “ICI estimated weekly long-term mutual fund flows: U.S. equity flows minus bond flows” | Figure 5 | ICI estimated weekly long-term flows, domestic equity and bond; [official release](https://www.ici.org/research/stats/flows), official XLS/PDF archives listed in `src/rebal/fetch/ici_archives.csv` | exact | TASK-008 | $REPLICATE_DATA_DIR/licensed/ici/ici_weekly_flows.csv | partial (278 weekly observations in 39 blocks, 2008-12-03–2026-10-14; missing 2007–2008 and later gaps) | [ICI](cards/ici.md) |
| D23 | Pension allocations | “Center for Retirement Research at Boston College, Public Plans Data: actual and target public equity and fixed income” | Figure 1 | CRR Public Plans Data [API](https://publicplansdata.org/api/) and [detailed investment workbook](https://publicplansdata.org/wp-content/uploads/2024/09/PensionInvestmentPerformanceDetailed.xlsx) | exact | TASK-008 | data/public/ppd/ppd_allocations.csv; data/public/ppd/ppd_coverage.csv | available | [PPD](cards/ppd.md) |
| D24 | Factor returns | “market excess return, Carhart 4 factors, Fama–French 5 factors, Hou–Xue–Zhang (HXZ) q-factors” | Table 6B | [French daily library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html): FF3, FF5, momentum, short/long reversal; [Global-q daily q5](https://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2025.csv) | exact | TASK-005 | data/public/french/; data/public/hxz/ | available | [French](cards/french.md), [HXZ](cards/hxz.md) |
| D25 | CRSP daily stock returns | “idiosyncratic volatility (ivol) = cross-sectional SD of individual stock returns” | Table 6C | Licensed CRSP CIZ daily common-stock returns, historical share codes 10/11; sample cross-sectional SD from tape-kit [WRDS CRSP](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/) | exact | TASK-009 | $REPLICATE_DATA_DIR/licensed/crsp/dispersion_daily.parquet | available | [CRSP](cards/crsp.md) |
| D26 | BofA Global Financial Stress Index (GFSI) Liquidity Risk | “vendor or ticker not named” | Table 6C | Hu–Pan–Wang `Noise_bp`; [Jun Pan official workbook](https://en.saif.sjtu.edu.cn/junpan/Noise_Measure_2025.xlsx). Chosen because it covers 1997–2023; OFR Funding is an unused fallback | proxy | TASK-003 | $REPLICATE_DATA_DIR/licensed/hpw/noise.csv | available | [HPW](cards/hpw.md), [OFR fallback](cards/ofr.md) |
| D27 | Dollar-scaling constants | “Fed Financial Accounts ($37.8T retirement assets, year-end 2022); CRS Report R47699 (allocations); Survey of Consumer Finances ("two-thirds of households"); Census (127M households, 2022); ICI ($45.8T at 2025-06-30)” | §2.1.1 cost estimate | Dated paper constants from [Fed Z1](https://www.federalreserve.gov/releases/z1/), [CRS R47699](https://crsreports.congress.gov/product/pdf/R/R47699), [SCF](https://www.federalreserve.gov/econres/scfindex.htm), [Census](https://www.census.gov/data/tables/time-series/demo/families/households.html), [ICI 2025 Q2](https://www.ici.org/statistical-report/ret_25_q2); documented in [costs](../methods/costs.md) | exact (paper constants) | TASK-016 | docs/methods/costs.md; src/rebal/exhibits/costs.py; no downloaded reports | available | [Scaling constants](cards/scaling_constants.md) |
| D28 | Surveys and qualitative evidence | “NASRA rebalancing-policy survey; pension memos (Seattle CERS, SCERS, SFERS, Montgomery County); Vanguard and NBIM notes; pension roundtable (2024-06-19)” | §1.1, §2.3 | Paper §1.1 and §2.3 qualitative source descriptions: NASRA, pension memos, Vanguard, NBIM and the 2024-06-19 roundtable; documentation only | none | TASK-001 | none (documentation only) | not available (qualitative evidence; numerical replication out of scope) | [Qualitative evidence](cards/qualitative.md) |

## Legend

- **exact**: the same series, obtained from its publisher or a public mirror.
- **proxy**: a different series used in place of the authors' series.
- **none**: no numerical replication source is used.
- **available**: the selected source covers its required use; cards record remaining gaps or revisions.
- **partial**: usable observations exist, but the row states the coverage limitation.
- **not available**: the row states why the required numerical source cannot be used.

D17 uses the authors' yield source, with our documented return construction.
D27 uses dated constants transcribed from the paper, not newly fetched report totals.
D3 is a derived calendar. It uses processed storage rather than a raw data directory.

## Storage classes

Public, redistributable files stay in `data/public/<source>/`, each below 20 MB.
The actual directory names include `sentiment`, `ppd` and `hxz`.
Licensed or terms-restricted files stay outside git in
`$REPLICATE_DATA_DIR/licensed/<source>/`. The default root is `~/data/replicate`.
This class includes HPW, FEARS, BEX and ARA because redistribution rights are unclear.
Processed panels stay in `$REPLICATE_DATA_DIR/processed/`.
A `none` entry reserves no raw data directory.

## Replication limits

- **D6:** MSCI history starts in December 2000. No earlier observations or ETF splice are invented.
- **D9:** MOVE starts in November 2002. The initial study gap stays missing.
- **D14:** the public FEARS subset ends in 2011. The authors' private extension remains unavailable;
  skip the full-sample FEARS column of Table D.9.
- **D15:** ARA is available only from July 2004 through December 2019.
- **D17:** ten-year GSW yields start in August 1971, despite the overall curve file starting in 1961.
- **D18:** the four Russell ETF proxies start in May 2000.
- **D19:** TFF starts in 2006 and the full-size S&P contract stops reporting in September 2021.
- **D21:** ANcerno is licensed and discontinued; the WRDS search found no matching table.
- **D22:** recovered ICI weekly history has a late start and gaps. Monthly flows are not substituted.
- **D23:** individual plan allocations can be missing; three geographic target variables are entirely missing.
- **D28:** surveys, memos and the pension roundtable are qualitative evidence, documented only.
- **Footnote 28:** the unreported 3:30 PM check used private asset-manager data.
- **Footnote 32:** the authors report an extension to 2025 without its data or full results.

Independent extensions or proxy checks cannot reproduce the unavailable author data.
