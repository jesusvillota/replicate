---
id: TASK-013
title: 'Signal engine: Threshold, Calendar, momentum and calendar dummies'
milestone: M-2
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-3. This task implements the paper's two rebalancing signals and their companions, per `docs/contracts/signals.md`. See paper-notes §3.2, §3.4 and §3.6. Every regression, cost and strategy result is built on them.

## Scope

No cluster jobs in this task. Build and test on the demo fixtures from `rebal.demo` and `rebal.io` (`demo=True`). The real panel may not exist yet; TASK-018 runs the real data. Follow `docs/contracts/` exactly. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below. Where the choice is cheap, also expose it as a CLI flag.

**1. `src/rebal/signals.py`.**

**Simulation.** These are the contract functions:
- `simulate_threshold(r_eq, r_bd, delta, target=0.60, timing="clean")`
- `simulate_calendar(r_eq, r_bd, target=0.60, timing="clean")`
- `simulate_dates(r_eq, r_bd, dates, target=0.60)`

Each returns `w_pre` (the drifted weight before any trade), `w_post` and `trade` (w_post − w_pre). Use the drift formula in paper-notes §3.2. The two timings:
- `timing="clean"`: s_t = drift(w_post_{t−1}, R_t) − target. Rebalance at the close of t when |s_t| ≥ δ (Threshold), or when t is the last trading day of the month (Calendar). The signal at t is s_t.
- `timing="literal"`: follow App. B exactly as written, including its one-day delay (paper-notes §5.1).

**`build(r_eq, r_bd, target=0.60, timing="clean", deltas=0.000..0.040 step 0.001)`** returns every column in the signals contract:
- `ret`;
- `thr_000`…`thr_040`, and `threshold` (the mean over δ = 0–2.5%);
- `calendar`;
- `week1`…`week4` and `days_to_month_end`, from the input's own trading-day index;
- the momentum family, per paper-notes §3.4: the sign of the cumulative k-day `ret`. A sign of 0 counts as 0. `momentum` = (mom_medium + mom_slow) / 2. A flag `--momentum all15` averages all 15 signs instead.
- `rev_st`: the cumulative `ret` over t−4..t.
- `rev_lt`: the cumulative `ret` over t−1259..t−252.
- `eom_rev`: the S&P return from the close of the month's 4th Friday to the month-end close (paper-notes §3.6). Pass the S&P series as an argument; the CLI uses `r_sp500tr`.
- the target variants `threshold_t86`/`calendar_t86`, `_t50` and `_t70`: the same construction with targets 0.86, 0.50 and 0.70.

**CLI.**
- `uv run python3 -m rebal.signals --build [--timing clean|literal]` reads `rebal.io.load_panel()` (with `r_eq = r_es`, `r_bd = r_ty`) and writes `processed_dir()/signals_<timing>.parquet`.
- `--demo` runs the same build on the demo panel and then runs the self-checks below.

**2. Exhibits: `src/rebal/exhibits/signals_descriptive.py`.**
- `table_C1`: mean, SD, AR(1), skewness and excess kurtosis of Threshold and Calendar. Annualize as the paper does: try it and document it (paper-notes §5.8).
- `table_C2`: the correlations of Threshold, Calendar, Momentum, VIX, MOVE, EPU, ADS and Sentiment.
- `figure_C1`: the time series of both signals.

**3. Methods doc.** `docs/methods/signals.md` covers:
- the timing;
- the momentum definition;
- the week1–week3 definitions;
- the burn-in, i.e. the first valid date of each column;
- on demo data: rebalances per year for each δ, next to the paper's numbers (δ = 0 → 252; δ = 1.1% → about 12; δ = 2.5% → about 4).

**4. Tests.** `tests/test_signals.py`, on synthetic returns:
- **δ = 0:** the portfolio trades on every day, and `thr_000` equals the one-day drift deviation.
- **δ = 1.0:** the portfolio never trades, and the signal equals the buy-and-hold drift.
- **Calendar:** it trades exactly once per month, on the last trading day.
- **The 0.24 rule:** with daily returns scaled to 1/10 of normal size, `calendar` ≈ 0.24 × the cumulative `ret` since the last rebalance, within 5%.
- **Trade counts:** they do not increase as δ grows.
- **Bounds:** momentum stays within [−1, 1].
- **Timing:** the `literal` and `clean` timings differ only as §5.1 describes.

Out of scope: regressions (TASK-014).

## Acceptance

- `uv run pytest tests/test_signals.py` passes.
- `uv run python3 -m rebal.signals --demo` prints the self-check results and the per-δ rebalance counts, and exits 0.
- `uv run python3 -m rebal.exhibits --all --demo --only table_C1 table_C2 figure_C1` writes these three exhibits to `output/demo/`.
- The output columns match `docs/contracts/signals.md`. A check in the test compares the column lists.

## Verify

```sh
uv run pytest -q tests/test_signals.py
uv run python3 -m rebal.signals --demo
uv run python3 -m rebal.exhibits --all --demo --only table_C1 table_C2 figure_C1 && ls output/demo/
```
