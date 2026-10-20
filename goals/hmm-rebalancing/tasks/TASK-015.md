---
id: TASK-015
title: Calibration and horizon figures
milestone: M-2
state: approved
depends_on: [TASK-014]
delivery: pr
---

## Why

Serves SC-3. This task builds the figures that calibrate the signals and trace their effect over time:
- Figure 2, Figure D.1 and Figure D.3: the per-δ t-statistics;
- Figure 3 and Figure D.2: the month-end windows;
- Figure 4 and Figure D.4: the horizon profiles.

See paper-notes §3.3, §3.5 and §4.

## Scope

No cluster jobs in this task. Build and test on the demo fixtures from `rebal.demo` and `rebal.io` (`demo=True`). The real panel may not exist yet; TASK-018 runs the real data. Follow `docs/contracts/` exactly. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below. Where the choice is cheap, also expose it as a CLI flag.

The methods doc for this task is `docs/methods/horizons.md`.

Use `rebal.regress.ols` and `rebal.regress.predictive` from TASK-014. Do not reimplement them.

**1. Calibration figures: `src/rebal/exhibits/calibration_figures.py`.**
- **`figure_2` (HC) and `figure_D1` (HAC):**
  - Eq. (1) for each δ = 0.0…4.0%, using `thr_*`.
  - Plot the t-statistic of γ1 against δ, with a dashed line at −2.58.
  - Also show the t-statistic of the aggregate `threshold`.
- **`figure_D3`:** the same regression on two subsets: days with |thr_δ| ≥ δ, and days with |thr_δ| < δ.
- **`figure_3` (HC) and `figure_D2` (HAC):**
  - Eq. (3) for N = 1…10, where Dummy^N = 1 when `days_to_month_end` ≤ N.
  - Plot the t-statistic of β2.

**2. Horizon figures: `src/rebal/exhibits/horizon_figures.py`.**
- **`figure_4`:**
  - Eq. (5). The dependent variable is the cumulative log `ret` over t+1..t+i, for i = 1…15.
  - The regressors are Threshold, Calendar, week4, Cal × week4, Momentum and Ret_t.
  - Use Hodrick (1992) 1B standard errors, as in Ang and Bekaert (2007), with 95% bands.
  - Implement Hodrick 1B in `src/rebal/regress_hodrick.py` and describe the formula in the methods doc.
- **`figure_D4`:** the single-day return n days ahead, for n = 1…15, with the eq. (4) regressors and HC bands.

**3. Tests.** `tests/test_horizons.py`:
- **Size test:**
  - Run 200 Monte Carlo draws of i.i.d. returns with a persistent AR(1) regressor (ρ = 0.9) and no true effect.
  - Use horizon h = 5.
  - The Hodrick 1B test rejects at the 5% level in 2%–10% of draws.
  - Report the rejection rate of the naive overlapping OLS test too; it should be higher.
- **Planted effect:** with the demo planted effect, `figure_2`'s data has t < −3 at δ = 0.
- **Plotted data:** each figure's CSV holds the plotted values.

Out of scope: running on real data (TASK-018).

## Acceptance

- `uv run pytest tests/test_horizons.py` passes, and the outcome quotes the Hodrick rejection rate.
- `uv run python3 -m rebal.exhibits --all --demo --only figure_2 figure_3 figure_4 figure_D1 figure_D2 figure_D3 figure_D4` writes 7 PDFs and 7 CSVs to `output/demo/`.

## Verify

```sh
uv run pytest -q tests/test_horizons.py
uv run python3 -m rebal.exhibits --all --demo --only figure_2 figure_3 figure_4 figure_D1 figure_D2 figure_D3 figure_D4
ls output/demo/figure_*
```
