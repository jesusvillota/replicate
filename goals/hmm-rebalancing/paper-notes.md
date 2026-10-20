# Paper notes: Harvey, Mazzoleni and Melone (2026)

"The Unintended Consequences of Rebalancing". SSRN / Dice Center WP 2025-01, version of January 14, 2026, 76 PDF pages.

- **Paper files:** the PDF is at the repo root: `Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.pdf`. OCR text is in `ocr/<tool>/`. `ocr/paperextract/` and `ocr/chandra/` read tables best.
- **Page numbers:** "p." below means the PDF page. The printed page number is the PDF page minus 2.
- **Approximate values:** a value marked "≈" was read off a chart.
- **Authority:** this file is the planner's reading of the paper. Workers cite it by section, such as "paper-notes §3.2". If the PDF and this file disagree, the PDF wins: note the difference in your outcome.

## 1. Summary

**Research question.** Does routine rebalancing of balanced equity/bond portfolios move aggregate U.S. stock and bond prices? If it does, what does it cost investors?

**Mechanism.** Many institutions hold fixed stock/bond targets, such as 60/40: pensions, target-date funds (TDFs), mutual funds and sovereign funds. When stocks beat bonds, equity becomes overweight, so these funds sell stocks and buy bonds. They trade at about the same time, either on a calendar (month-end) or when the weight leaves a tolerance band. Because the trades line up in direction and timing, they move prices.

**Signals.** The authors simulate a 60/40 portfolio of S&P 500 futures and 10-year Treasury futures, daily, 1997–2023. From it they build two signals. Each is the distance of the equity weight from its 60% target:
- **Threshold:** the portfolio rebalances when the weight leaves a band of size δ. The signal is averaged over δ from 0% to 2.5%.
- **Calendar:** the portfolio rebalances on the last business day of each month. Its predictive power sits in the last 5 trading days ("week4").

**Findings.**
- **Prediction:** both signals predict next-day returns of the S&P 500 minus the 10-year Treasury futures, with a negative sign and t ≈ 3.6–3.8.
- **Size:** a one-standard-deviation (1-SD) signal moves next-day equity returns by about −16 to −17 bps and bond returns by about +2 to +4 bps.
- **Controls:** the result survives momentum, reversal, VIX/MOVE, economic policy uncertainty (EPU), the ADS business-conditions index and sentiment.
- **Reversal:** the effect reverts within about 2 weeks.
- **Patterns:** the effect is strongest at quarter-end. It is absent before 1997. It appears for large vs small caps but not for value vs growth. It also appears in international equity.
- **Trade data:** CFTC, ANcerno and ICI data show hedgers, asset managers, pensions and mutual funds trading as rebalancers.
- **Cost:** about 8 bps per year. On about $20T of assets, this is about $16B per year, or about $200 per U.S. household.
- **Random dates:** rebalancing on random dates cuts the cost to about 0.6 bps.
- **Front-running:** a strategy that trades ahead of the rebalancers earns about 10% per year, with a Sharpe ratio (SR) of 1.11 and an alpha of about 9.5% per year (t > 4).

## 2. Data inventory

| # | Variable | Authors' source | Freq. | Sample | Notes | Used in |
|---|---|---|---|---|---|---|
| D1 | Equity futures return R^SP | Bloomberg generic ES1/ES2. "We construct continuous return series for the E-mini S&P 500 futures (ES) and the 10-year U.S. Treasury note futures (TY) using Bloomberg's nearby contracts … reported by Bloomberg as excess return price indices" (App. A, p.54) | daily close | 1997-09-10 to 2023-03-17; footnote 32 (p.38) says it was extended to 2025 | E-mini S&P 500 | all main-sample exhibits |
| D2 | Bond futures return R^10Y | Bloomberg TY1/TY2, built the same way | daily | as D1 | 10-year T-note futures | as D1 |
| D3 | Holiday calendar | "a holiday was identified whenever both front contracts, TY1 and ES1, were reported as N/A … we explicitly marked September 12–14, 2001, as exchange closures" (p.54) | daily | as D1 | — | sample definition |
| D4 | S&P 500 Total Return Index | Bloomberg (p.54) | daily | 1997–2023 | — | Tables D.4, D.11 |
| D5 | Bloomberg U.S. Aggregate Bond TR Index | Bloomberg (p.54) | daily | 1997–2023 | — | Table D.4 |
| D6 | MSCI ACWI ex USA Net TR (USD) | Bloomberg (p.54) | daily | 1997–2023, N = 6,097 | international equity | Table D.14 |
| D7 | U.S. 3-month T-bill | not named | daily | 1997–2023 | cash leg | Table D.14 |
| D8 | VIX | Bloomberg "VIX Index" (CBOE), divided by 100 | daily | 1997–2023 | — | Tables 1, 3, 6C, D.2–D.6, D.8, D.13, D.14 |
| D9 | MOVE | Bloomberg "MOVE Index" (ICE BofA), divided by 100 | daily | 1997–2023 | — | as D8 |
| D10 | EPU | Baker, Bloom and Davis (2016) daily news-based index (p.18) | daily | 1997–2023 | scaling not stated | Tables 1, 6C, others |
| D11 | ADS | Aruoba, Diebold and Scotti (2009) index (Philadelphia Fed) | daily | 1997–2023 | — | Table 1, others |
| D12 | Sentiment | Shapiro, Sudhof and Wilson (2022) daily news sentiment (SF Fed) | daily | 1997–2023 | — | Table 1, others |
| D13 | ra^BEX, unc^BEX | Bekaert, Engstrom and Xu (2022) risk aversion and uncertainty | daily | N = 6,124 | — | Table D.9 |
| D14 | FEARS | Da, Engelberg and Gao (2015). The authors got it privately (footnote 23) | daily | 2004-07-01 to 2016-12-30, N = 3,149 | private | Table D.9 |
| D15 | ARA (aggregate retail attention) | Da, Hua, Hung and Peng (2025) | daily | 2004-07-01 to 2019-12-31, N = 3,903 | — | Table D.9 |
| D16 | Long-sample equity return | "daily U.S. equity market total returns from Kenneth French's database" | daily | 1961-06-16 to 2023-03-17 | — | Table 4 |
| D17 | Long-sample 10-year bond return | "Federal Reserve Board Treasury data"; Table 4 note: Gürkaynak, Sack and Wright (2007) (GSW) yield curve | daily | 1961–2023 | method to turn yields into returns not stated | Table 4 |
| D18 | Russell 1000, 2000, 1000 Value, 1000 Growth | not named; likely Bloomberg; price or total return not stated | daily | 2006-08-17 to 2023-03-17, N = 4,175 | — | Table 5 |
| D19 | CFTC Commitments of Traders (COT) | "weekly Commitment of Traders (COT) reports". Commercial = hedgers, non-commercial = speculators. Net positions and open interest | weekly | from August 2006 | S&P 500 and 10-year T-note futures | Figure 5 |
| D20 | CFTC Large Trader Net Position Changes (LTPos) | "Published by the CFTC on June 30, 2011, this one-time report covers the period from January 2009 to May 2011 and provides the daily average aggregate net position changes for large traders across 35 futures markets" (p.28) | weekly as used | Jan 2009 to May 2011 | asset managers, leveraged funds | Figure 5 |
| D21 | ANcerno institutional trades | daily trade-level equity transactions, about 8% of CRSP volume (p.29) | daily | Jan 1999 to Sep 2011 | S&P 500 constituents; buy ratio = $buys / ($buys + $sells) | Figure 5 |
| D22 | ICI flows | ICI estimated weekly long-term mutual fund flows: U.S. equity flows minus bond flows | weekly | from Jan 2007 | — | Figure 5 |
| D23 | Pension allocations | Center for Retirement Research at Boston College, Public Plans Data: actual and target public equity and fixed income | annual | FY2003–2022 | U.S. public defined-benefit (DB) plans | Figure 1 |
| D24 | Factor returns | market excess return, Carhart 4 factors, Fama–French 5 factors, Hou–Xue–Zhang (HXZ) q-factors | daily | 1997–2023 | — | Table 6B |
| D25 | CRSP daily stock returns | idiosyncratic volatility (ivol) = cross-sectional SD of individual stock returns | daily | 1997–2023 | stock filters not stated | Table 6C |
| D26 | BofA Global Financial Stress Index (GFSI) Liquidity Risk | vendor or ticker not named | daily | 1997–2023 | — | Table 6C |
| D27 | Dollar-scaling constants | Fed Financial Accounts ($37.8T retirement assets, year-end 2022); CRS Report R47699 (allocations); Survey of Consumer Finances ("two-thirds of households"); Census (127M households, 2022); ICI ($45.8T at 2025-06-30) | point values | — | — | §2.1.1 cost estimate |
| D28 | Surveys and qualitative evidence | NASRA rebalancing-policy survey; pension memos (Seattle CERS, SCERS, SFERS, Montgomery County); Vanguard and NBIM notes; pension roundtable (2024-06-19) | — | — | not quantitative | §1.1, §2.3 |

**No intraday data.** The paper uses no intraday data. Footnote 28 mentions an unreported check with 3:30 PM prices that an asset manager supplied.

## 3. Methods

### 3.1 Futures return series (App. A)

1. Use ES1 and TY1 by default.
2. Roll to ES2 or TY2 at the end of the month before the expiry month.
3. Ret = R^SP − R^TY. Both legs are futures returns, so they are already excess returns.

### 3.2 Portfolio simulation and signals (p.12; App. B)

**Drift (no trading):** w_{t+1} = w_t(1+R^SP_{t+1}) / [w_t(1+R^SP_{t+1}) + (1−w_t)(1+R^10Y_{t+1})]. The target is 60%, and w = 60% on the first day.

**Threshold rule.** Reset to 60% if |w^T_t − 60%| ≥ δ; otherwise drift.
- **Signal:** Threshold^δ_{t+1} = w^T_{t+1}(w^T_t; R_{t+1}) − 60%, i.e. the drifted weight before any trade.
- **Rebalances per year:** δ = 0 gives 252, δ = 1.1% about 12, δ = 2.5% about 4. The median over the grid is about 16.

**Aggregate Threshold (eq. 2).** The mean of Threshold^δ over δ = 0%, 0.1%, …, 2.5% (N = 26).

**Calendar rule.** Reset w^C to 60% on the last business day of each month.
- **Signal:** Calendar_{t+1} = w^C_{t+1}(w^C_t; R_{t+1}) − 60%.

**Rule of thumb.** The deviation is about 0.24 × (R^E − R^B) since the last rebalance, because 0.6 × 0.4 = 0.24.

**week4** = 1 on the last 5 trading days of the month.

### 3.3 Calibration regressions

- **Eq. (1):** Ret_{t+1} = γ0 + γ1 Threshold^δ_t + ε, for δ = 0 to 4% in steps of 0.1%.
  - Figure 2 uses heteroskedasticity-robust (HC) t-statistics.
  - Figure D.1 uses heteroskedasticity- and autocorrelation-consistent (HAC) t-statistics.
  - Figure D.3 splits the days into |Threshold^δ_t| ≥ δ and |Threshold^δ_t| < δ.
- **Eq. (3):** Ret_{t+1} = β0 + β1 Cal_t + β2 Cal_t × Dummy^N_t + β3 Dummy^N_t + ε, for N = 1…10 days before month-end. The plot shows the t-statistic of β2: HC in Figure 3, HAC in Figure D.2.

### 3.4 Main predictive regression (eq. 4)

Ret_{t+1} = β0 + β1 Threshold_t + β2 Cal_t + β3 week4_t + β4 Cal_t × week4_t + ψ Momentum_t + ζ Ret_t + γ′X_t + ε_{t+1}

- **Estimation:** time-series OLS with White HC standard errors. There are no fixed effects and no clustering.
- **Momentum:** for each look-back k, take the sign of the cumulative S&P-minus-TY return over the last k days.
  - fast = mean over k = 1…10
  - medium = mean over k = 11…20
  - slow = mean over k ∈ {21, 42, 63, 126, 252}
  - Momentum = mean of medium and slow.
- **Controls X:** VIX/100, MOVE/100, EPU, ADS and Sentiment, in levels. Table D.5 uses changes.
- **"1 SD" magnitudes:** they imply a daily SD of about 0.48% for Threshold and about 0.634% for Cal × week4.

### 3.5 Horizon regression (eq. 5)

- **Specification:** the dependent variable is the cumulative log return Ret_{t+1:t+i}, for i = 1…15. The regressors are the signals, Momentum and Ret_t. There are no X controls.
- **Standard errors:** Hodrick (1992) reverse-regression SEs, as in Ang and Bekaert (2007), with 95% bands.
- **Figure D.4:** the single-day return n days ahead, using the eq. (4) regressors and HC bands.

### 3.6 Robustness variants

- **Other targets:** signals from 86/14, 50/50 and 70/30 portfolios (Table D.7).
- **State dependence (Table D.8):**
  - Threshold Small/Large = Threshold × 1{|Threshold| below/above its median}.
  - Threshold⊥ = residual of Threshold on Momentum. By the Frisch–Waugh–Lovell theorem, its coefficient equals the baseline Threshold coefficient exactly. Use this as a built-in check.
- **Reversal (Table D.10):** short-term = trailing 5-day S&P-minus-TY return; long-term = trailing 1260-day return, skipping the last year.
- **EoM Rev (Graziani 2024; Table D.11):** the S&P 500 return from the close on the 4th Friday of the month to the month-end close.
- **Week-of-month dummies week1–week3** (Table D.12).
- **Month of quarter (Table 2B):** separate samples for the 1st, 2nd and 3rd month of each quarter. Table 2A column (3) adds Threshold × week4.
- **Separate legs (Tables 3, D.13):** R^SP alone, or R^TY alone, as the dependent variable.
- **Long sample (Table 4):** French market return minus a GSW-based 10-year return, split at 1997-09-10.
- **Equity segments (Table 5):**
  - R1K vs R2K uses a 90/10 portfolio. Signals, momentum and Ret are built within the segment.
  - R1K Value vs Growth is a falsification test; its weights are not stated.
- **International (Table D.14):**
  - Dependent variable: MSCI ACWI ex US minus the 3-month T-bill.
  - The signals are lagged one more day (t−1).
  - The control is the 2-day trailing S&P 500 return.
- **Other δ ranges (Table D.6):** [0, 2%] and [0.1%, 2.5%].
- **Signals on trailing returns (Table D.1):** regress the signals on trailing S&P-minus-TY returns over 1, 2, 3, 4, 5, 10, 15, 21, 42, 63, 126 and 252 days, with HAC SEs. The coefficients sum to about 0.24.

### 3.7 Trading-data correlations (Figure 5)

- **CFTC:** Q follows Kang, Rouwenhorst and Tang (2020): the cross-asset net position change between t+1 and t, scaled by open interest, in week t. Compute it for hedgers and for speculators, then correlate it with the signals at t.
- **LTPos:** weekly net trading by asset managers and by leveraged funds vs lagged signals.
- **ANcerno:** aggregate buy ratio vs lagged signals.
- **ICI:** weekly equity-minus-bond flows vs lagged signals.

### 3.8 Cost of rebalancing (§2.1.1, pp.21–23)

**Formula:** Cost = price impact × average trade size × trades per year.

**Price impact.** The eq. (4) coefficient, estimated only on the days when rebalancing should happen:
- Calendar: week4 days.
- Threshold: days with |Threshold^δ| ≥ δ.
- Footnote 17 gives an alternative: the full sample with an interaction term.

**Trade size.** The average absolute distance to target on rebalancing days.

**Headline numbers.**
- Calendar: [−0.39] × 1% × 12 ≈ 5 bps.
- Threshold: 6–27 bps over δ from 0 to 2.5%, averaging 15 bps; about 11 bps with a 1% trade size.
- Headline cost: about 8 bps.
- A Calendar trader at T−4 pays about 9 bps (footnote 18).

**Random dates.** One random day per month, 10,000 simulations. Mean cost 0.6 bps, median 0.5 bps. The Figure D.5 legend says "Mean = −0.6 bps"; its 95% interval is about −4.6 to +3.2 bps. Tracking error is about 35 bps.

**Dollar cost.**
- 8 bps × "more than $20T" = $16B per year.
- $16B / (2/3 × 127M households) ≈ $189 per household, which the paper rounds to "almost $200".

**Utility (footnote 36).** U = r̄ − 0.5γσ² with γ = 3. Threshold 2.5% beats buy-and-hold by about 18 bps; monthly Calendar by about 10 bps.

### 3.9 Front-running strategy (§4)

**Return:** R^Strat_{t+1} = (R^SP_{t+1} − R^TY_{t+1}) × w_t.

**Weight:** w_t is the mean of two pieces.
- Threshold piece: −Threshold_t / 1.5%.
- Calendar piece:
  - sign(−Cal_t) in week4;
  - sign(Cal_{−4}) on the first business day of the new month;
  - 0 otherwise.

**Evaluation.**
- Panel A: annualized mean, volatility, SR, skewness.
- Panel B: alphas from CAPM, Carhart 4-factor (C4), Fama–French 5-factor (FF5) and HXZ, with HC SEs.
- Panel C: mean returns in high vs low regimes, split at the median of ivol, GFSI liquidity, VIX, MOVE and EPU.
- SR net of costs is about 1, under the assumptions of Harvey et al. (2018).
- SR without crises (Sep 2008 to Mar 2009, and Mar 2020) is 0.90.
- Figure 6: cumulative performance, scaled to the volatility of the S&P 500.

## 4. Exhibits and target numbers

The default sample is 1997-09-10 to 2023-03-17, N = 6,226 days, with HC SEs.

**Figures 1–6**

- **Figure 1:** DB pension equity share, actual ≈ 0.63–0.68 vs target ≈ 0.65, FY2003–2022.
- **Figure 2:** t-statistic by δ. About −3.8 at δ = 0 and about −4.2 near δ = 1.0; the lowest is about −4.3 near δ = 1.8. Mostly insignificant above about 2.7%.
- **Figure 3:** t-statistic of β2 for each N:

  | N | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | t | −0.1 | −0.5 | −1.0 | −1.35 | −2.4 | −2.8 | −3.1 (peak) | −1.0 | −1.15 | −0.85 |

- **Figure 4** (Hodrick SEs):
  - Threshold is lowest at day 4 (≈ −0.95), insignificant from day 9, and ≈ −0.12 at day 15.
  - Cal × week4 is lowest at day 2 (≈ −0.52), insignificant from day 6, and ≈ −0.13 at day 15.
- **Figure 5:** correlations with lagged signals (Threshold / Calendar), all approximate:
  - CFTC hedgers −0.10 / −0.13; speculators +0.11 / +0.17
  - LTPos asset managers −0.08 / −0.12; leveraged funds +0.18 / +0.13
  - ANcerno −0.10 / −0.10
  - ICI −0.17 / −0.19
- **Figure 6:** cumulative log gains: the strategy ends at ≈ 6.2 and the S&P at ≈ 2.3.

**Tables 1–6**

- **Table 1 col (1):** Threshold −0.4144 (0.1148); Calendar 0.0553 (0.0709); week4 0.0002; Cal × week4 −0.3029 (0.0808); Momentum 0.0023 (0.0006); Ret −0.0203; adj. R² 0.0239.
  - Col (5) adds all controls: Threshold −0.4226 (0.1139), Cal × week4 −0.3033 (0.0808), adj. R² 0.0248.
  - A 1-SD signal gives 20 bps (Threshold) and 19.2 bps (Calendar).
- **Table 2A:**
  - Col (1), no interaction: Threshold −0.3281, Calendar −0.0778 (insignificant), R² 0.0130.
  - Col (3): Threshold −0.4789, Cal × week4 −0.3511, Threshold × week4 +0.2137 (insignificant), R² 0.0244.
- **Table 2B**, by month of quarter (N = 2,078 / 2,052 / 2,097):
  - Threshold −0.2723 (insignificant) / −0.4153** / −0.5845***
  - Cal × week4 −0.2509 (insignificant) / −0.3487*** / −0.3400***
- **Table 3:**
  - S&P leg: Threshold −0.3302 (0.1062), Cal × week4 −0.2667 (0.0758), R² 0.0225.
  - 10-year leg: Threshold +0.0842 (0.0269), Cal × week4 +0.0362 (0.0128).
  - 1-SD effects: 15.9 / 16.9 bps for equity and 4.1 / 2.3 bps for bonds.
- **Table 4** (Threshold, Cal × week4):

  | Sample | N | Threshold | Cal × week4 |
  |---|---|---|---|
  | 1961–2023 | 15,291 | −0.1809*** | −0.1536*** |
  | 1961–1997 | 8,870 | −0.0157 (ins.) | −0.0284 (ins.) |
  | 1997–2023 | 6,421 | −0.3685*** | −0.2569*** |

- **Table 5** (N = 4,175): R1K/R2K Threshold −0.2054***, Cal × week4 −0.1174*. Value/Growth −0.0339 and −0.0678, both insignificant.
- **Table 6:**
  - Panel A, strategy: mean 10.20, vol 9.17, SR 1.11, skew 5.23. S&P: 7.11 / 20.05 / 0.35. 10-year: 2.92 / 6.13 / 0.48.
  - Panel B alphas: CAPM 9.61 (1.77), C4 9.64, FF5 9.49, HXZ 9.43.
  - Panel C mean return, high vs low regime:

    | Split variable | High | Low |
    |---|---|---|
    | ivol | 15.68 | 5.09 |
    | Liquidity | 17.96 | 3.79 |
    | VIX | 16.50 | 3.91 |
    | MOVE | 14.85 | 5.55 |
    | EPU | 15.16 | 5.24 |

**Appendix C**

- **Table C.1:**
  - Threshold: mean 0.49, SD 0.08 (annualized), AR(1) 0.61, skewness −0.98.
  - Calendar: mean 0.18, SD 0.16, AR(1) 0.91, skewness −1.43.
- **Table C.2:** corr(Threshold, Calendar) 0.605; corr(Momentum, each signal) 0.676; corr(VIX, Threshold) −0.353.

**Appendix D figures**

- **Figure D.1:** lowest t ≈ −4.5 near δ = 1.8.
- **Figure D.2:** t ≈ −3.65 at N = 4.
- **Figure D.3:** on predicted rebalancing days t ≈ −4 to −6; on other days, insignificant.
- **Figure D.4:** Threshold ≈ −0.42 at day 1 and −0.20 at day 2; Cal × week4 ≈ −0.30 and −0.20; near 0 after that.
- **Figure D.5:** random-rebalancing cost, mean −0.6 bps, 95% interval about −4.6 to +3.2.

**Appendix D tables**

- **Table D.1:** Threshold on the 1-day return 0.1466, adj. R² 0.802. Calendar adj. R² 0.719.
- **Table D.3:** fast momentum 0.0006 (insignificant), medium 0.0013***, slow 0.0010**.
- **Table D.4:** Threshold −0.3970, Cal × week4 −0.3189.
- **Table D.6:** Threshold over [0, 2%] −0.3938; over [0.1%, 2.5%] −0.3980.
- **Table D.7** (Threshold, Cal × week4):

  | Target | Threshold | Cal × week4 |
  |---|---|---|
  | 86/14 | −0.8453 | −0.6008 |
  | 50/50 | −0.4098 | −0.2914 |
  | 70/30 | −0.4822 | −0.3460 |

- **Table D.8:** Small −0.2289 (insignificant), Large −0.4264***, Threshold⊥ −0.4144.
- **Table D.9:**
  - ra^BEX column: Threshold −0.4493, N = 6,124.
  - FEARS column: Threshold −0.4226, N = 3,149.
  - ARA column: Threshold −0.3731, N = 3,903.
- **Table D.10:** short-term reversal alone −0.0377*** (N = 6,473). With the signals: −0.0122 (insignificant).
- **Table D.11:** EoM Rev −0.0159 (insignificant), N = 6,173.
- **Table D.12:** Cal × week1 +0.2262**, Cal × week3 +0.2579***.
- **Table D.14:** Threshold −0.2723***, Cal × week4 −0.2060***, N = 6,097.

**Text only**

- Costs: Calendar 5 bps; Threshold 6–27 bps (average 15; 11 with a 1% trade); headline 8 bps; $16B per year; about $200 per household; random dates 0.6 bps.

## 5. Ambiguities a replicator must settle

Record each choice you make in your task's `docs/methods/<topic>.md`.

1. **Threshold timing.** Read literally, App. B adds a one-day delay. The clean version: s_t = drift(w^post_{t−1}, R_t) − 0.6; w^post_t = 0.6 if |s_t| ≥ δ, else 0.6 + s_t. Calendar: reset at the close of the last business day.
2. **Momentum:** the mean of the two sub-averages, or of all 15 signs? How are zero returns treated?
3. **Sample size:** the regressions have N = 6,226, but about 6,473 days exist (Table D.10). This suggests a burn-in of about 250 days for the 252-day momentum.
4. **Futures returns:**
   - What exactly is Bloomberg's "excess return price index"?
   - How to treat a day when only one of the two markets is closed?
   - Simple or log returns? Eq. (5) uses log returns; elsewhere they are presumably simple.
5. **Calendar dummies:** week4 means the last 5 trading days. Weeks 1–3 are not defined.
6. **Standard errors:** the HC type, the HAC lag length and the Hodrick (1992) implementation are not given.
7. **Control scaling:** EPU, ADS, Sentiment, BEX and ARA scaling is not stated.
8. **"1 SD" magnitudes:** the implied SDs are 0.48% for Threshold and 0.634% for Cal × week4.
9. **Cost details:**
   - Which regressors enter the subsample regressions?
   - How are trade size and trades per year measured for each δ?
   - How is a random day drawn?
   - Is the random-date mean +0.6 or −0.6 bps?
10. **Strategy details:** the meaning of Cal_{−4}, how the Calendar sign spans week4, the "11.6%" volatility, and the cost assumptions of Harvey et al. (2018).
11. **CFTC:**
    - Legacy or Traders in Financial Futures (TFF) report? The August 2006 start matches TFF.
    - E-mini or the big S&P contract?
    - Is Q the S&P change minus the TY change?
    - How to align Tuesday positions with daily signals?
12. **LTPos, ANcerno, ICI:** the lags and the aggregation level.
13. **Table 4 bond returns:**
    - How are GSW yields turned into returns?
    - GSW has no 10-year yield before about August 1971.
    - Is the French total return equal to Mkt-RF + RF?
14. **Table 5:** the Russell source, price or total return, and the Value/Growth weights.
15. **Tables D.4 and D.14:** in D.4, are the signals rebuilt from the S&P TR and Agg returns? The D.14 T-bill source is not named.
16. **Stock filters and GFSI:** the stock filters behind ivol and the GFSI ticker are not given.
17. **Not replicable:** FEARS, ANcerno, the 3:30 PM check (footnote 28), the 2025 extension (footnote 32) and the pension roundtable.
