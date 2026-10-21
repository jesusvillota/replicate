# Master source map

The authors' source column quotes [paper-notes §2](../../goals/hmm-rebalancing/paper-notes.md#2-data-inventory).
Our source follows the [Data plan](../../goals/hmm-rebalancing/README.md#data-plan-what-the-paper-needs-what-we-use).
All entries are planned. No data was downloaded in TASK-001.
After TASK-001, only TASK-012 updates this table.

| D | Variable | Authors' source | Used in (exhibits) | Our source | Exact or proxy | Fetch task | Storage | Status |
|---|---|---|---|---|---|---|---|---|
| D1 | Equity futures return R^SP | “Bloomberg generic ES1/ES2. "We construct continuous return series for the E-mini S&P 500 futures (ES) and the 10-year U.S. Treasury note futures (TY) using Bloomberg's nearby contracts … reported by Bloomberg as excess return price indices" (App. A, p.54)” | all main-sample exhibits | Chosen in DEC-001. Candidates: CRSP SPY total return minus T-bill; Yahoo `ES=F` with roll-day correction | proxy | TASK-006, TASK-009, TASK-011 | $REPLICATE_DATA_DIR/licensed/crsp/ or yahoo/ (DEC-001 pending) | planned |
| D2 | Bond futures return R^10Y | “Bloomberg TY1/TY2, built the same way” | as D1 | Chosen in DEC-001. Candidates: GSW 7- or 10-year zero/par return minus T-bill; CRSP 10-year fixed-term Treasury index (WRDS); IEF; Yahoo `ZN=F` | proxy | TASK-003, TASK-006, TASK-009, TASK-010, TASK-011 | data/public/gsw/ or $REPLICATE_DATA_DIR/licensed/wrds/, crsp/, yahoo/ (DEC-001 pending) | planned |
| D3 | Holiday calendar | “"a holiday was identified whenever both front contracts, TY1 and ES1, were reported as N/A … we explicitly marked September 12–14, 2001, as exchange closures" (p.54)” | sample definition | Trading days of the chosen proxies; 2001-09-12..14 marked closed | proxy | TASK-012 | $REPLICATE_DATA_DIR/processed/ | planned |
| D4 | S&P 500 Total Return Index | “Bloomberg (p.54)” | Tables D.4, D.11 | Yahoo `^SP500TR`; check against CRSP SPY | exact / proxy | TASK-006, TASK-009 | $REPLICATE_DATA_DIR/licensed/yahoo/ or crsp/ | planned |
| D5 | Bloomberg U.S. Aggregate Bond TR Index | “Bloomberg (p.54)” | Table D.4 | CRSP Mutual Funds VBMFX daily return (WRDS); AGG ETF from 2003 | proxy | TASK-009, TASK-010 | $REPLICATE_DATA_DIR/licensed/wrds/ or crsp/ | planned |
| D6 | MSCI ACWI ex USA Net TR (USD) | “Bloomberg (p.54)” | Table D.14 | msci.com end-of-day index download if available; else CRSP ETFs (VEU, ACWX, EFA) | exact / proxy | TASK-006, TASK-009 | $REPLICATE_DATA_DIR/licensed/msci/ or crsp/ | planned |
| D7 | U.S. 3-month T-bill | “not named” | Table D.14 | FRED `DTB3` | exact | TASK-003 | data/public/fred/ | planned |
| D8 | VIX | “Bloomberg "VIX Index" (CBOE), divided by 100” | Tables 1, 3, 6C, D.2–D.6, D.8, D.13, D.14 | FRED `VIXCLS` (CBOE) | exact | TASK-003 | data/public/fred/ | planned |
| D9 | MOVE | “Bloomberg "MOVE Index" (ICE BofA), divided by 100” | as D8 | Yahoo `^MOVE`; if the history is short, fill the gap with a documented proxy | exact / proxy | TASK-006 | $REPLICATE_DATA_DIR/licensed/yahoo/ | planned |
| D10 | EPU | “Baker, Bloom and Davis (2016) daily news-based index (p.18)” | Tables 1, 6C, others | policyuncertainty.com | exact | TASK-004 | data/public/epu/ | planned |
| D11 | ADS | “Aruoba, Diebold and Scotti (2009) index (Philadelphia Fed)” | Table 1, others | Philadelphia Fed, latest vintage | exact | TASK-004 | data/public/ads/ | planned |
| D12 | Sentiment | “Shapiro, Sudhof and Wilson (2022) daily news sentiment (SF Fed)” | Table 1, others | SF Fed | exact | TASK-004 | data/public/sf_fed/ | planned |
| D13 | ra^BEX, unc^BEX | “Bekaert, Engstrom and Xu (2022) risk aversion and uncertainty” | Table D.9 | Bekaert's public data page | exact | TASK-004 | $REPLICATE_DATA_DIR/licensed/bex/ | planned |
| D14 | FEARS | “Da, Engelberg and Gao (2015). The authors got it privately (footnote 23)” | Table D.9 | not available; Table D.9 FEARS column skipped | none | TASK-004 | none | planned |
| D15 | ARA (aggregate retail attention) | “Da, Hua, Hung and Peng (2025)” | Table D.9 | the authors' public file if one exists; else skipped | exact / none | TASK-004 | $REPLICATE_DATA_DIR/licensed/ara/ | planned |
| D16 | Long-sample equity return | “"daily U.S. equity market total returns from Kenneth French's database"” | Table 4 | Kenneth French daily data library | exact | TASK-005 | data/public/french/ | planned |
| D17 | Long-sample 10-year bond return | “"Federal Reserve Board Treasury data"; Table 4 note: Gürkaynak, Sack and Wright (2007) (GSW) yield curve” | Table 4 | Fed `feds200628.csv` (GSW), with our yield-to-return method | exact source | TASK-003 | data/public/gsw/ | planned |
| D18 | Russell 1000, 2000, 1000 Value, 1000 Growth | “not named; likely Bloomberg; price or total return not stated” | Table 5 | CRSP ETFs IWB, IWM, IWD, IWF (total return); Yahoo `^RUI` `^RUT` `^RLV` `^RLG` price indices as a check | proxy | TASK-006, TASK-009 | $REPLICATE_DATA_DIR/licensed/crsp/ or yahoo/ | planned |
| D19 | CFTC Commitments of Traders (COT) | “"weekly Commitment of Traders (COT) reports". Commercial = hedgers, non-commercial = speculators. Net positions and open interest” | Figure 5 | CFTC legacy COT and TFF history files | exact | TASK-007 | data/public/cftc/ | planned |
| D20 | CFTC Large Trader Net Position Changes (LTPos) | “"Published by the CFTC on June 30, 2011, this one-time report covers the period from January 2009 to May 2011 and provides the daily average aggregate net position changes for large traders across 35 futures markets" (p.28)” | Figure 5 | CFTC website, if still hosted | exact | TASK-007 | data/public/cftc/ | planned |
| D21 | ANcerno institutional trades | “daily trade-level equity transactions, about 8% of CRSP volume (p.29)” | Figure 5 | not available, unless TASK-010 finds it in our WRDS subscription | none | TASK-010 | none; $REPLICATE_DATA_DIR/licensed/wrds/ only if access exists | planned |
| D22 | ICI flows | “ICI estimated weekly long-term mutual fund flows: U.S. equity flows minus bond flows” | Figure 5 | ICI estimated long-term flows files | exact | TASK-008 | $REPLICATE_DATA_DIR/licensed/ici/ | planned |
| D23 | Pension allocations | “Center for Retirement Research at Boston College, Public Plans Data: actual and target public equity and fixed income” | Figure 1 | publicplansdata.org | exact | TASK-008 | data/public/crr/ | planned |
| D24 | Factor returns | “market excess return, Carhart 4 factors, Fama–French 5 factors, Hou–Xue–Zhang (HXZ) q-factors” | Table 6B | French library; global-q.org | exact | TASK-005 | data/public/french/ and data/public/global_q/ | planned |
| D25 | CRSP daily stock returns | “idiosyncratic volatility (ivol) = cross-sectional SD of individual stock returns” | Table 6C | tape-kit CRSP CIZ on the cluster | exact | TASK-009 | $REPLICATE_DATA_DIR/licensed/crsp/ | planned |
| D26 | BofA Global Financial Stress Index (GFSI) Liquidity Risk | “vendor or ticker not named” | Table 6C | OFR Financial Stress Index, liquidity category | proxy | TASK-003 | data/public/ofr/ | planned |
| D27 | Dollar-scaling constants | “Fed Financial Accounts ($37.8T retirement assets, year-end 2022); CRS Report R47699 (allocations); Survey of Consumer Finances ("two-thirds of households"); Census (127M households, 2022); ICI ($45.8T at 2025-06-30)” | §2.1.1 cost estimate | the same public reports, cited in `docs/methods/costs.md` | exact | TASK-016 | data/public/reports/ | planned |
| D28 | Surveys and qualitative evidence | “NASRA rebalancing-policy survey; pension memos (Seattle CERS, SCERS, SFERS, Montgomery County); Vanguard and NBIM notes; pension roundtable (2024-06-19)” | §1.1, §2.3 | not replicated; documentation only | none | TASK-001 | none (documentation only) | planned |

## Legend

- **exact**: the same series, obtained from its publisher or a public mirror.
- **proxy**: a different series used in place of the authors' series.
- **none**: no usable source is available or no numerical replication is planned.

Combined classes show a choice that remains open. “Exact source” for D17 describes the yields;
our yield-to-return transform still needs a documented method. DEC-001 selects D1 and D2.

## Storage classes

Public, redistributable files go to `data/public/<source>/` as CSV, each under 20 MB.
This class covers Fed, FRED, OFR, CFTC, French, EPU, ADS, SF Fed, CRR and global-q.

Licensed or terms-restricted files go to `$REPLICATE_DATA_DIR/licensed/<source>/` and never enter git.
This class covers WRDS, CRSP via tape-kit, Yahoo, MSCI, ICI, BEX and ARA.
The default root is `~/data/replicate`. Processed files go to `$REPLICATE_DATA_DIR/processed/`.
D3 is a derived calendar, so it has processed storage rather than a raw download directory.
A `none` entry reserves no data directory. Source cards record license and coverage details.

## Not replicable

- **D14:** FEARS was supplied privately to the authors. Skip that column in Table D.9.
- **D21:** ANcerno is licensed and discontinued. Skip it unless TASK-010 confirms access through WRDS.
- **D28:** surveys, memos and the pension roundtable are qualitative evidence. We document them only.
- **Footnote 28:** the unreported 3:30 PM check used private asset-manager data.
- **Footnote 32:** the authors report an extension to 2025 without its data or full results.

The M-3 planner may propose an independent extension or a 3:30 PM proxy check.
Neither would reproduce unavailable author data.
