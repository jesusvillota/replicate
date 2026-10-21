# Predictive regressions

The output schema is [the exhibits contract](../contracts/exhibits.md).
Inputs follow [the panel contract](../contracts/daily_panel.md) and
[the signals contract](../contracts/signals.md). Specifications follow
[paper-notes §§3.4, 3.6, 4 and 5](../../goals/hmm-rebalancing/paper-notes.md).
The exact column layouts were checked against the local OCR paper, pages
19–20 and 58–70 (`ocr/paperextract/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md`).

## Timing, samples and units

`predictive` joins the full panel trading calendar and signal dates first.
It pairs regressors at t with the outcome at t+1. It then applies the
sample, subset and joint finite-value mask. A missing signal date does not
change the meaning of the next trading day. Signals supply `ret`, including
the planted demo return; separate leg outcomes come from the panel.
Interactions use colon names, such as `calendar:week4`.

Both predictor and outcome dates must lie within the inclusive sample,
1997-09-10 through 2023-03-17 by default. Recorded sample endpoints are the
actual dependent-variable dates, except D1, which is contemporaneous.
`--end latest` extends the endpoint. No extra fixed 252-day burn-in is
imposed: missing values from the upstream momentum history determine it.
Each specification uses its own complete observations. Table D11 also
requires `eom_rev` availability in its baseline column, matching its caption.
Subsets, including month of quarter, refer to predictor dates.

Returns and signals stay in decimal units. Controls use the contract scales:
VIX and MOVE are already divided by 100; EPU, ADS and Sentiment stay in
published units. There is no further scaling, imputation or standardization.
Table D5 differences controls over one panel trading day before sample selection.
Momentum, reversal, week flags and target signals come from the signal frame;
this task does not rebuild TASK-013's signal rules.

## Covariance choices

Every model includes an intercept. HC1 is the default White covariance,
with its n/(n-k) correction. `--se hc0` removes that correction and provides
the paper-ambiguity check. Point estimates are unchanged by covariance choice.
Tests compare HC0 and HC1 coefficients, standard errors, t ratios and p values
with independent statsmodels fits. The HC0/HC1 SE ratio is sqrt((n-k)/n).
D1 and D2 always use HAC (Newey–West). The kernel is Bartlett, without a
small-sample correction. Lags are floor(4(T/100)^(2/9)), where T is the
complete estimation-sample size. `--hac-lags N` overrides this choice.
All p values use the asymptotic normal distribution, as statsmodels does
for robust covariance with `use_t=False`. Empty, undersized or rank-deficient
designs fail instead of returning an unidentified estimate.

## Table columns

- Table 1 and D2: base; VIX/MOVE; EPU/ADS; Sentiment; all five controls.
  Base is Threshold, Calendar, week4, Calendar × week4, Momentum and lagged Ret.
- Table 2A: base without Calendar × week4; base; base plus Threshold × week4.
  Column 1 retains week4, as the paper caption specifies.
- Table 2B: base for months 1, 2 and 3 within each quarter.
- Table 3: ES base/all controls, followed by TY base/all controls.
  D13 is the full five-column control sequence for each leg. Column strings
  A1–A5 denote ES, and B1–B5 denote TY. Controls are levels, per the task.
  The paper's N differs between Table 3 and D13 (6,223 versus 6,226);
  we use the same date and missing-value rules rather than deleting rows to match N.
- D1: Threshold and Calendar, each jointly regressed on all twelve trailing
  return sums (1, 2, 3, 4, 5, 10, 15, 21, 42, 63, 126, 252 days).
  Sums include date t and use simple decimal returns. Each `coefficient_sum`
  row excludes the intercept. Its SE includes all covariance cross terms.
- D3: Table 1 with Momentum replaced by fast, medium and slow momentum,
  included together. D5 has four columns: each control block in differences,
  then all controls in differences; it omits a duplicate baseline column.
- D6: [0, 2%] without/with all controls, then [0.1%, 2.5%] without/with
  all controls. Grid endpoints are inclusive; a missing grid member makes
  that day's aggregate missing. D7 has base columns for 86/14, 50/50, 70/30.
- D8: Small/Large without/with controls, then Threshold-perpendicular
  without/with controls. The split uses the baseline complete sample's median
  absolute Threshold. Ties belong to Small. Small and Large sum to Threshold.
  Residualization fits Threshold on an intercept and Momentum separately on
  each final complete sample. Both regressions retain Momentum and all other
  baseline terms. The coefficient identity is checked with absolute tolerance
  1e-10 and zero relative tolerance; a failure raises `AssertionError`.
- D10: short reversal alone; signals and short reversal; long reversal alone;
  signals and long reversal; signals and both reversals. These columns include
  Momentum with the signals but omit lagged Ret, matching the paper.
- D11: eom_rev alone; base; base plus eom_rev; ES base plus eom_rev;
  TY base plus eom_rev. No extra controls.
- D12: Threshold, Calendar, Momentum and Ret with each week1–week3 dummy
  and its Calendar interaction separately. Columns 4–6 also include week4
  and Calendar × week4. This avoids the four-dummy intercept collinearity.

## One-SD magnitudes and output layout

For every Table 1 and Table 3 regressor, report coefficient times sample SD
with ddof=1, using that column's complete estimation sample. Include Calendar
and Calendar × week4 as distinct rows. `magnitude` uses decimal daily returns;
`magnitude_bps` multiplies it by 10,000. Signed effects are retained.
Real output is `output/tables/magnitudes.csv`.

The demo acceptance asks for exactly 15 top-level CSV files and also asks
for magnitudes under `output/demo/`. To satisfy both, the 15 table CSVs are
at that directory's top level; magnitudes are at
`output/demo/magnitudes/magnitudes.csv`. A JSON sidecar records inputs,
parameters, outcome mappings and output paths. All demo artifacts are ignored.
Each module run overwrites only its own artifacts.

The scaffold's demo used residual SD 0.01. Its full base regression within
the specified sample produced Threshold -0.347216, a finite-sample error
of 0.052784. Set the residual SD to 0.008 so the required full-design and
zero-effect recovery checks satisfy the 0.05 tolerance. Dates, regressors,
planted coefficients and seed are unchanged. Demo leg returns remain synthetic
panel draws and do not inherit the spread's planted effects. Demo results
are software checks, not evidence about market returns.

## Commands

1. `uv run python3 -m rebal.exhibits --all --demo`
2. `uv run python3 -m rebal.exhibits.predictive_tables --demo --se hc0`
3. `uv run python3 -m rebal.exhibits.predictive_tables --demo --se hac --hac-lags 10 --end latest`
4. `uv run pytest tests/test_regress.py`

The discovered runner uses module defaults. Use the module entry point for
endpoint, timing and covariance overrides.
