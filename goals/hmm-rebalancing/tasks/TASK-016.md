---
id: TASK-016
title: Rebalancing cost estimates
milestone: M-2
state: approved
depends_on: [TASK-013, TASK-014]
delivery: pr
---

## Why

Serves SC-5. This task estimates what current rebalancing practice costs investors (paper-notes §3.8):
- about 8 bps per year;
- about $16B per year;
- about $200 per household;
- about 0.6 bps for random-date rebalancing (Figure D.5).

## Scope

No cluster jobs in this task. Build and test on the demo fixtures from `rebal.demo` and `rebal.io` (`demo=True`). The real panel may not exist yet; TASK-018 runs the real data. Follow `docs/contracts/` exactly. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below. Where the choice is cheap, also expose it as a CLI flag.

The methods doc for this task is `docs/methods/costs.md`.

Use `rebal.signals.simulate_*` from TASK-013 and `rebal.regress` from TASK-014.

**Module.** `src/rebal/exhibits/costs.py`. It produces `costs.csv` (long format: `item, value, unit, note`) and `figure_D5`.

**1. Calendar cost.**
- **Impact:** the Calendar coefficient from eq. (4), estimated on week4 days only.
- **Trade size:** the mean |trade| on rebalancing days, from `simulate_calendar`.
- **Trades:** 12 per year.
- **Cost:** impact × size × trades, in bps per year.
- **Variants:** a trader at T−4 (footnote 18), and the samples before and after 2006 (the Pension Protection Act).

**2. Threshold cost.** For each δ from 0 to 2.5%:
- **Impact:** the coefficient on `thr_δ`, estimated on the days with |thr_δ| ≥ δ.
- **Size:** the mean |trade| on those days.
- **Trades:** rebalances per year.
- **Cost:** report the per-δ cost, the average over δ, and the version with a fixed 1% trade size.

**3. Headline cost.** The mean of the Calendar cost and the 1%-size Threshold cost.

**4. Full-sample alternative** (footnote 17): one regression with an interaction term.

**5. Random dates.**
- Run 10,000 simulations. Each picks one uniformly random trading day per month; week4 days are allowed.
- Use `simulate_dates` and the same cost formula.
- Report the mean, the median and the 95% interval.
- `figure_D5` is the histogram.
- Report the tracking error against the monthly Calendar portfolio.
- Seed the generator so the result is reproducible.
- `--n-sims` makes demo runs fast.

**6. Dollar cost.**
- Dollar cost = headline bps × assets. Use $20T as the paper does, and also the Fed Z.1 total.
- Per household = dollar cost / (2/3 × 127M).
- Cite each constant (D27) in the methods doc: the Fed Financial Accounts, CRS Report R47699, the Survey of Consumer Finances, the Census and ICI.

**7. Utility comparison** (footnote 36).
- U = mean − 0.5 · γ · var, with γ = 3.
- Compare buy-and-hold, Threshold rebalancing at δ = 2.5% and monthly Calendar rebalancing.
- Use the 60/40 portfolio return w · r_es + (1 − w) · r_ty.

The methods doc must cover every open point in paper-notes §5.9.

**Tests.** `tests/test_costs.py`:
- On a synthetic series with zero price impact, the costs are about 0.
- With a planted impact, the Calendar cost equals impact × size × 12 to rounding.
- The random-date distribution is centred on about 0 when there is no impact.

Out of scope: running on real data (TASK-018).

## Acceptance

- `uv run pytest tests/test_costs.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5` writes `output/demo/costs.csv`, and `output/demo/figure_D5.pdf` with its CSV.
- The printed `costs.csv` lists every item from paper-notes §3.8.

## Verify

```sh
uv run pytest -q tests/test_costs.py
uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5
uv run python3 -c "import pandas as pd; print(pd.read_csv('output/demo/costs.csv').to_string())"
```
