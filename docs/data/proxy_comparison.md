# ES and TY proxy comparison

Stored source data; no new downloads. Study: 1997-09-10–2023-03-17.

## Inputs and methods

French daily RF / 100 (published percent/day → decimal/day).

Cash proxies subtract RF. Futures returns are already excess returns and do not subtract RF.
All sources are aligned to the French equity-session calendar before returns are computed.
Missing prices/yields are never filled. A missing quote also makes the next holding return missing.
The DTB3 fallback uses SPY sessions. No upstream file is changed.

T1 uses a 10-year zero; T3 uses a **6.5-year maturity** zero as an approximate TY duration match.
This is a fixed duration assumption, not a measured cheapest-to-deliver bond history.
Zero holding return is exp(n*y_previous − (n−delta)*y_today(n−delta))−1, delta=calendar days/365.25.
Continuous yields are divided by 100. T1 interpolates SVENY09/10; T3 interpolates SVENY06/07.
T2 fixes yesterday's SVENPY10 coupon, pays semiannually, and prices that same bond on both fitted GSW curves.
It uses the Svensson parameters for every cashflow, including sub-year maturities, and dirty prices for accrual.

## Roll repair and benchmark

Calendar flags span third Friday minus eight calendar days through the following Monday in each quarterly expiry month.
Residual jumps outside that window also flag days: abs(ES−E2)>0.02 or abs(ZN−T3)>0.01.
E3 replaces flagged returns with E2; T6 uses T3. Missing reference days cannot be benchmark days.
Repaired returns in the study sample: **ES 715 days; TY 717 days**.
Returns excluded because a repair reference is missing: ES 0 days; TY 70 days. These are not counted as repairs.
These conservative flags are heuristic, not verified roll dates. Large close-time errors can also be flagged.
The benchmark uses unrepaired Yahoo close-to-close ES=F / ZN=F returns on unflagged days only, from 2000-09 through 2023-03-17.
An ES−TY pair requires both benchmark legs. Repaired observations never enter benchmark metrics.
E3 and T6 therefore have mechanical identity metrics on their own benchmark; they are not independent validation.
No benchmark exists for 1997–2000. No result establishes accuracy against Bloomberg.

## Metric definitions

Corr is contemporaneous Pearson correlation. Beta is Cov(proxy, benchmark)/Var(benchmark), with an intercept.
TE is sample SD(proxy−benchmark)×sqrt(252), shown in percent/year. Mean is proxy−benchmark in basis points/day.
Lead is Corr(proxy_t, benchmark_t+1); lag is Corr(proxy_t, benchmark_t−1). Shifts use the full session grid before filtering.
MTD corr compares 0.24×within-month cumulative simple returns on each row's identical common clean days.
This is an incomplete-month Calendar stand-in: omitted roll/missing sessions contribute to neither sum.
It is not the full paper signal, and changing a row's overlap changes this diagnostic.
Coverage start is the first usable return, before restricting the benchmark period; N counts paired clean days.
The requested end is 2023-03-17; actual overlap endpoints below reflect the excluded roll window.

## Available candidates

- **E1**: CRSP SPY total return − RF.
- **E2**: Yahoo ^SP500TR return − RF.
- **E3**: Yahoo ES=F, repaired.
- **T1**: GSW 10-year zero − RF.
- **T2**: GSW 10-year par bond − RF.
- **T3**: GSW 6.5-year zero − RF.
- **T5**: CRSP IEF total return − RF.
- **T6**: Yahoo ZN=F, repaired.

| Candidate | Coverage start | N | Overlap start | Overlap end | Corr | Beta | TE %/year | Mean bp/day | Lead | Lag | MTD corr |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| E1 | 1993-02-01 | 4940 | 2000-09-19 | 2023-03-08 | 0.9928 | 0.9882 | 2.2947 | 0.1630 | -0.0580 | -0.0585 | 0.9989 |
| E2 | 1988-01-05 | 4940 | 2000-09-19 | 2023-03-08 | 0.9849 | 0.9833 | 3.3291 | 0.2925 | -0.0656 | -0.0624 | 0.9983 |
| E3 | 2000-09-19 | 4940 | 2000-09-19 | 2023-03-08 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0594 | -0.0594 | 1.0000 |
| T1 | 1971-08-17 | 4839 | 2000-09-22 | 2023-03-08 | 0.9413 | 1.4759 | 4.1663 | 0.9569 | -0.0075 | 0.0121 | 0.9596 |
| T2 | 1971-08-17 | 4839 | 2000-09-22 | 2023-03-08 | 0.9438 | 1.2547 | 2.9725 | 0.5767 | -0.0067 | 0.0106 | 0.9634 |
| T3 | 1961-06-15 | 4839 | 2000-09-22 | 2023-03-08 | 0.9617 | 0.9819 | 1.6425 | 0.4320 | -0.0012 | 0.0137 | 0.9839 |
| T5 | 2002-07-29 | 4442 | 2002-07-29 | 2023-03-08 | 0.9327 | 1.0678 | 2.4197 | 0.3452 | 0.0167 | -0.0229 | 0.9736 |
| T6 | 2000-09-22 | 4839 | 2000-09-22 | 2023-03-08 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0060 | -0.0060 | 1.0000 |

## All available ES−TY pairs

| Candidate | Coverage start | N | Overlap start | Overlap end | Corr | Beta | TE %/year | Mean bp/day | Lead | Lag | MTD corr |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| E1/T1 | 1993-02-01 | 4839 | 2000-09-22 | 2023-03-08 | 0.9824 | 1.0768 | 4.7398 | -0.7827 | -0.0542 | -0.0551 | 0.9858 |
| E1/T2 | 1993-02-01 | 4839 | 2000-09-22 | 2023-03-08 | 0.9874 | 1.0441 | 3.7424 | -0.4025 | -0.0558 | -0.0565 | 0.9921 |
| E1/T3 | 1993-02-01 | 4839 | 2000-09-22 | 2023-03-08 | 0.9917 | 0.9972 | 2.8069 | -0.2578 | -0.0564 | -0.0573 | 0.9978 |
| E1/T5 | 2002-07-29 | 4442 | 2002-07-29 | 2023-03-08 | 0.9888 | 1.0184 | 3.2961 | -0.1664 | -0.0703 | -0.0764 | 0.9963 |
| E1/T6 | 2000-09-22 | 4839 | 2000-09-22 | 2023-03-08 | 0.9943 | 0.9907 | 2.3067 | 0.1742 | -0.0557 | -0.0570 | 0.9991 |
| E2/T1 | 1988-01-05 | 4839 | 2000-09-22 | 2023-03-08 | 0.9757 | 1.0756 | 5.4798 | -0.6812 | -0.0578 | -0.0590 | 0.9845 |
| E2/T2 | 1988-01-05 | 4839 | 2000-09-22 | 2023-03-08 | 0.9810 | 1.0429 | 4.5655 | -0.3011 | -0.0596 | -0.0605 | 0.9912 |
| E2/T3 | 1988-01-05 | 4839 | 2000-09-22 | 2023-03-08 | 0.9852 | 0.9960 | 3.7605 | -0.1563 | -0.0603 | -0.0616 | 0.9974 |
| E2/T5 | 2002-07-29 | 4442 | 2002-07-29 | 2023-03-08 | 0.9844 | 1.0221 | 3.9300 | -0.0558 | -0.0723 | -0.0862 | 0.9961 |
| E2/T6 | 2000-09-22 | 4839 | 2000-09-22 | 2023-03-08 | 0.9882 | 0.9895 | 3.3245 | 0.2757 | -0.0597 | -0.0614 | 0.9985 |
| E3/T1 | 2000-09-19 | 4839 | 2000-09-22 | 2023-03-08 | 0.9877 | 1.0861 | 4.1663 | -0.9569 | -0.0553 | -0.0549 | 0.9869 |
| E3/T2 | 2000-09-19 | 4839 | 2000-09-22 | 2023-03-08 | 0.9929 | 1.0534 | 2.9725 | -0.5767 | -0.0569 | -0.0563 | 0.9933 |
| E3/T3 | 2000-09-19 | 4839 | 2000-09-22 | 2023-03-08 | 0.9972 | 1.0065 | 1.6425 | -0.4320 | -0.0575 | -0.0571 | 0.9988 |
| E3/T5 | 2002-07-29 | 4442 | 2002-07-29 | 2023-03-08 | 0.9944 | 1.0301 | 2.4197 | -0.3452 | -0.0702 | -0.0790 | 0.9973 |
| E3/T6 | 2000-09-22 | 4839 | 2000-09-22 | 2023-03-08 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0569 | -0.0569 | 1.0000 |

## Full-sample pairs on a common comparison calendar

Ranking uses the smallest TE among pairs whose legs cover both study endpoints. All rows below use identical clean days.
This controls calendar differences when choosing among the full-history cash constructions.

| Candidate | Coverage start | N | Overlap start | Overlap end | Corr | Beta | TE %/year | Mean bp/day | Lead | Lag | MTD corr |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| E1/T1 | 1993-02-01 | 4839 | 2000-09-22 | 2023-03-08 | 0.9824 | 1.0768 | 4.7398 | -0.7827 | -0.0542 | -0.0551 | 0.9858 |
| E1/T2 | 1993-02-01 | 4839 | 2000-09-22 | 2023-03-08 | 0.9874 | 1.0441 | 3.7424 | -0.4025 | -0.0558 | -0.0565 | 0.9921 |
| E1/T3 | 1993-02-01 | 4839 | 2000-09-22 | 2023-03-08 | 0.9917 | 0.9972 | 2.8069 | -0.2578 | -0.0564 | -0.0573 | 0.9978 |
| E2/T1 | 1988-01-05 | 4839 | 2000-09-22 | 2023-03-08 | 0.9757 | 1.0756 | 5.4798 | -0.6812 | -0.0578 | -0.0590 | 0.9845 |
| E2/T2 | 1988-01-05 | 4839 | 2000-09-22 | 2023-03-08 | 0.9810 | 1.0429 | 4.5655 | -0.3011 | -0.0596 | -0.0605 | 0.9912 |
| E2/T3 | 1988-01-05 | 4839 | 2000-09-22 | 2023-03-08 | 0.9852 | 0.9960 | 3.7605 | -0.1563 | -0.0603 | -0.0616 | 0.9974 |

## Unavailable candidates

- **E4**: WRDS ES futures: TASK-010 found no usable series.
- **T4**: CRSP fixed-term Treasury index: TASK-010 access probe denied (42501).
- **T7**: WRDS TY futures: TASK-010 found no usable series.

## Close times and limits

Equities close at 16:00 ET; ES at 16:15 ET; Treasury futures settle at 15:00 ET.
Yahoo daily closes need not reproduce the paper's Bloomberg settlement convention. GSW is a fitted cash Treasury curve.
Nonzero lead/lag correlations can reflect close times, stale quotes, and market dynamics; they do not identify a cause.
No future return is used to shift a candidate. Roll repair is retrospective and can bias apparent fit toward its reference.
The fixed thresholds were not optimized for correlation. Different roll windows and the 6.5-year duration merit later sensitivity checks.

## Input lineage

Generator: `rebal.proxies`; annualization=252; GSW day count=365.25; ES cutoff=0.02; TY cutoff=0.01.

- `data/public/gsw/feds200628.csv` SHA-256: `9f2a8d6ba54d13cdb9b4f19811f9c61f72c870b8fab1562d5b8bd6dd70b337b7`
- `data/public/french/F-F_Research_Data_Factors_daily.csv` SHA-256: `2f288d35b1786a429cda4f1f9c197c053441fc59ef5ace6d5b138026d27799d6`
- `licensed/crsp/etf_daily.parquet` SHA-256: `5e7db3be218b2da873f0d4879a88fb85187ac9db9c284b01208bc1faf3fc3c17`
- `licensed/yahoo/^SP500TR.csv` SHA-256: `c0eff3c0fd74efcf0ee5e31d796c232afd13c734a84a98e170610f5e141bf424`
- `licensed/yahoo/ES=F.csv` SHA-256: `2bb8ab529576bff36b96311b88f9880f4afce62293f2678ec19c9f27f2657b11`
- `licensed/yahoo/ZN=F.csv` SHA-256: `bda304c7eb7210f6943fa4b7646bbb5e28f92f71443a8eeaef7ef6fb1fe4e2f7`

## Recommendation for DEC-001

Recommend **E1/T3: CRSP SPY total return − RF / GSW 6.5-year zero − RF** for the main panel.
Both cover 1997-09-10–2023-03-17. Pair correlation with the clean Yahoo futures benchmark is **0.9917**; annualized tracking error is **2.8069%** (N=4839).
On the common comparison calendar: correlation **0.9917**, TE **2.8069%**.
This pair has the lowest common-calendar tracking error among the full-sample candidates. Coverage here means both endpoints and available intervening sessions, with missing bond holidays left explicit.
Use **E2/T2: Yahoo ^SP500TR return − RF / GSW 10-year par bond − RF** as a robustness pair with different constructions for both legs.
Its correlation is **0.9810**; annualized TE is **4.5655%**.
E3 starts after 2000-09-18; T6 starts after 2000-09-21; T5 starts in July 2002. They cover the study only partly.
For a later futures robustness splice, use E1/T3 before the first common usable E3/T6 return, then repaired E3/T6; use T3 before T5 for an IEF check.
Splice returns, not price levels, on a documented common session. Test the break and retain source flags. No splice is built here.
TASK-012 must retain missing sessions and apply the daily-panel contract. This is evidence for DEC-001, not a recorded decision.
