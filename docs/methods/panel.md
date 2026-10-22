# Daily panel construction

The output follows the [daily panel contract](../contracts/daily_panel.md).
Run `uv run python3 -m rebal.panel --build`, then
`uv run python3 -m rebal.panel --check`. No downloads or cluster jobs run.
Inputs come from the [final source map](../data/sources.md) and its source cards.

## Outputs and calendar

The builder writes `daily_panel.parquet` and `daily_panel_alt.parquet` under
`processed_dir()`, outside git. The default directory is `~/data/replicate/processed`.
`REPLICATE_DATA_DIR` overrides that external root. Each file has the contract's
35 columns, with a regular `datetime64[ns]` date column and 34 `float64` columns.
`panel.metadata.json` records input paths and SHA-256 hashes, construction choices,
build time, output names, full coverage and the study row count.

French daily dates define the equity-session grid before returns are computed.
GSW yields and S&P 500 total-return levels are aligned to that grid without filling.
This reproduces the accepted `rebal.proxies` constructions from TASK-011.
A missing GSW quote makes that session's holding return missing. It also makes
the next session's holding return missing. No return bridges that missing quote.

Retain dates with finite `r_es` and `r_ty` in the main pair. Remove
2001-09-11 through 2001-09-14 explicitly. These four dates are already absent
from the stored French grid. The filter also handles inputs that contain them.
Keep all common history, including dates before the study and after its end.
The stored main calendar runs from **1993-02-01 through 2026-07-31**, with
**8,275 rows**. Its **1,122 rows before 1997-09-10** permit downstream burn-in.
This task does not construct signals or select regression observations.

The alternative has exactly the same calendar and all the same noncore columns.
Only `r_es` and `r_ty` change. Missing alternative core returns fail validation;
they never trigger filling or a shorter main sample.

## Main and alternative returns

[DEC-001](../../goals/hmm-rebalancing/decisions/DEC-001.md) accepts these pairs.
The builder calls the existing `rebal.proxies` functions directly.

| Output | Main E1/T3 | Alternative E2/T2 |
|---|---|---|
| `r_es` | `es_spy`: CRSP SPY distribution-inclusive `ret` minus French RF | `es_total_return`: Yahoo `^SP500TR` Close percentage change minus RF |
| `r_ty` | `ty_zero_65`: GSW 6.5-year zero-coupon holding return minus RF | `ty_par_10`: GSW 10-year par-bond holding return minus RF |

All returns are simple decimal returns. An output of 0.01 means 1% for that day.
Cash returns subtract RF once. No Yahoo futures splice is used.

The zero-coupon construction holds yesterday's bond for actual elapsed days
divided by 365.25, then resets maturity. It interpolates SVENY06 and SVENY07
for the 6.5-year bond and its remaining maturity. GSW zero yields are continuous
percent per year, divided by 100 for pricing. Its total return is
`exp(6.5*y_previous - (6.5-delta)*y_remaining_today) - 1`.

The par construction fixes yesterday's SVENPY10 coupon, with semiannual payments.
It prices the same cash flows on the previous and current fitted GSW curves.
Dirty prices include accrued interest. It uses BETA0–BETA3 and TAU1/TAU2.
Intervals of six months or longer remain missing. See the
[proxy comparison](../data/proxy_comparison.md) for pricing details and limits.
These are cash proxies. Duration and close-time differences from futures remain.

## Cash, controls and units

Only controls can carry their last observation forward, for at most five
French trading sessions. Filling occurs before the main-calendar filter.
Thus removed bond sessions still count toward the five-session limit.
Leading gaps stay missing. Filling can extend the final published control
observation by five sessions; reported panel coverage includes those fills.
RF, factors, index returns and both core returns are never filled.

| Output | Input and transform | Reason or limit |
|---|---|---|
| `rf` | French three-factor daily RF / 100 | Published daily cash return; use the same RF as DEC-001 |
| `rf_3m` | `(DTB3 / 100) * calendar_days_to_next_retained_session / 360` | Requested discount-quote accrual convention; quote may carry five equity sessions; final row is NaN without a next date |
| `vix` | FRED VIXCLS / 100 | Paper's index scaling |
| `move` | Yahoo `^MOVE` Close / 100 | Same index scaling; source starts 2002-11-12, first retained observation 2002-11-13; early gap stays NaN |
| `epu` | Published US daily EPU index points | No additional scaling |
| `ads` | Published standardized ADS index | No scaling; latest revised vintage, not real-time information |
| `sentiment` | Published SF Fed unitless news score | No scaling; five-session rule handles short source gaps |
| `ra_bex` | Published BEX `ra`, defined as `2 * exp(qt)` | No additional scaling |
| `unc_bex` | Published BEX `unc`, monthly variance | Keep monthly variance; do not substitute annual volatility percent |
| `ara` | Published market-cap weighted abnormal Google search-volume index | No scaling; native coverage 2004-07-01–2019-12-31, then at most five carried sessions |
| `liquidity` | HPW `Noise_bp`, unchanged basis points | HPW covers the study; different measure from BofA GFSI Liquidity Risk |
| `ivol` | CRSP dispersion `ivol`, unchanged decimal sample SD | Stock-return dispersion, not a residual volatility estimate; see [ivol methods](ivol.md) |

HPW is selected because its observed history covers both study endpoints,
1987-01-02–2025-12-31. If the file is absent or its observed range does not
span the study, use OFR FSI `Funding`, unchanged index points. Record that choice
in metadata. OFR begins 2000-01-03, so this fallback leaves the earlier gap.
No interpolation, normalization, winsorization or artificial history is added.
The contract retains the selected source's published units: basis points for
HPW `Noise_bp`, or index points for OFR `Funding`. These units differ across
sources. `panel.metadata.json` records the selected source and its units.

## Factors

Divide every published percent return by 100. Do not fill missing factors.

| Output | Source column |
|---|---|
| `mkt_rf`, `smb`, `hml` | French three-factor `Mkt-RF`, `SMB`, `HML` |
| `rmw`, `cma` | French five-factor `RMW`, `CMA` |
| `mom` | French daily momentum `Mom` |
| `q_mkt`, `q_me`, `q_ia`, `q_roe`, `q_eg` | Global-q q5 `R_MKT`, `R_ME`, `R_IA`, `R_ROE`, `R_EG` |

The contract has one SMB column. It retains three-factor SMB for the common
Carhart inputs; it is not the five-factor file's differently constructed SMB.
The other French three-factor columns also come from that same file.
The q5 library's separate `R_F` does not replace French RF.
Fetched short/long reversal series remain available in source storage; the
contract has no columns for them. Current source vintages can revise history.

## Index returns

| Output | Construction and gaps |
|---|---|
| `r_sp500tr` | Yahoo `^SP500TR` Close percentage change on the French session grid, with `fill_method=None` |
| `r_agg` | TASK-010's validated Yahoo VBMFX `ret`, already a distribution-adjusted decimal return |
| `r_acwxus` | MSCI ACWI ex USA code 899901, USD NETR level percentage change on its native weekday grid, then align to US sessions |
| `r_r1k`, `r_r2k`, `r_r1kv`, `r_r1kg` | CRSP distribution-inclusive `ret` for IWB, IWM, IWD and IWF respectively |
| `r_mkt_french` | `(Mkt-RF + RF) / 100` from French's three-factor file |
| `r_10y_gsw` | `ty_zero_10(curve, rf) + rf`, the GSW 10-year zero total holding return |

VBMFX supplies usable returns across the entire study. It is preferred to the
2004–2006 WRDS sample and to AGG's later start under
[DEC-002](../../goals/hmm-rebalancing/decisions/DEC-002.md).
No source splice is needed. The source card validates adjusted prices against
Yahoo distribution events. These are not raw NAV changes. Expenses, benchmark
differences, rounded cash events and Yahoo's adjustment convention limit how
closely the fund matches Bloomberg U.S. Aggregate TR. VBTLX begins in 2001;
it is not needed to fill VBMFX. See the [bond-fund card](../data/cards/wrds.md).

MSCI supplies the exact requested index. Its levels start 2000-12-29 and its
first retained return is 2001-01-02. Keep the earlier study gap. No available
CRSP ex-US ETF starts earlier, and no ETF splice is used. Repeated MSCI holiday
levels stay as published. Russell ETFs begin in May 2000; their earlier gaps
also stay NaN. Source returns are not compounded across dates removed by the
main-calendar filter. They retain their published daily meaning.

## Coverage, validation and the paper's N

Both panels contain **6,318 rows for 1997-09-10–2023-03-17**, inclusive.
The French equity grid has **6,422 sessions** in that window. SPY has a return
on all those dates. The GSW 6.5-year holding return is missing on **104 sessions**.
There are **52 missing GSW quote sessions**; each also removes the following
holding return. The four September 2001 closures are already absent from French.
This explains `6422 - 104 = 6318` without filling returns.

[Paper-notes §5.3](../../goals/hmm-rebalancing/paper-notes.md#5-ambiguities-a-replicator-must-settle)
reports regression **N=6,226** and about **6,473 total days**.
Our panel count is **92 above** the regression N and **155 below** that total.
It is not a reproduction of either count. Cash and GSW publication calendars
differ from futures. The paper's roughly 250-day burn-in is a separate regression
selection issue. This panel keeps earlier observations so later tasks can build
rolling signals; it does not trim rows to force a paper match.

The checker reopens both files. It validates column order, exact dtypes, finite
observations, sorted unique midnight dates, complete core returns, excluded
September closures, complete required study controls/factors, both study
endpoints, and `r_mkt_french = mkt_rf + rf`. It also verifies that all noncore
columns match across panels. For every column, it prints observed endpoints
and NaN share for both full history and the study. It prints both study counts
and paper comparisons, then ends with `PANEL OK`. Violations exit nonzero.
