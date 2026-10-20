---
id: TASK-017
title: Front-running strategy
milestone: M-2
state: approved
depends_on: [TASK-014]
delivery: pr
---

## Why

Serves SC-5. Section 4 of the paper shows that a strategy which trades ahead of the rebalancers earns about 10% per year, with a Sharpe ratio (SR) of 1.11. This task covers Table 6 (panels A–C) and Figure 6. See paper-notes §3.9 and §4.

## Scope

No cluster jobs in this task. Build and test on the demo fixtures from `rebal.demo` and `rebal.io` (`demo=True`). The real panel may not exist yet; TASK-018 runs the real data. Follow `docs/contracts/` exactly. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below. Where the choice is cheap, also expose it as a CLI flag.

The methods doc for this task is `docs/methods/strategy.md`.

Use `rebal.regress.ols` from TASK-014 for the factor regressions.

**Module.** `src/rebal/exhibits/strategy.py`. It reads the signals frame (`calendar`, `threshold`, `week4`, `days_to_month_end`) and the panel.

**1. Weight.** w_t = the mean of two pieces:
- The Threshold piece: −threshold_t / 1.5%.
- The Calendar piece:
  - sign(−calendar_t) on week4 days;
  - sign(calendar at the first week4 day of the previous month) on the first trading day of the new month. This is our default reading of Cal_{−4} (§5.10); a flag selects the alternative reading;
  - 0 otherwise.

The strategy return is R_{t+1} = (r_es_{t+1} − r_ty_{t+1}) × w_t.

**2. Outputs.**
- **`table_6a`:** the annualized mean, volatility, SR and skewness of the strategy, `r_es` and `r_ty`.
- **`table_6b`:** alphas from four factor models, with HC standard errors; the alpha is annualized as ×252, in %. The models:
  - CAPM: `mkt_rf`;
  - Carhart 4-factor (C4): `mkt_rf`, `smb`, `hml`, `mom`;
  - Fama–French 5-factor (FF5);
  - Hou–Xue–Zhang (HXZ): `q_mkt`, `q_me`, `q_ia`, `q_roe`.
- **`table_6c`:** the mean strategy return in high and low regimes. Split at the full-sample median of `ivol`, `liquidity`, `vix`, `move` and `epu`, each measured at t.
- **`figure_6`:** the cumulative log gains of the strategy, rescaled to the volatility of `r_es`, against `r_es` and `r_ty`.
- **Extra rows in `table_6a`:**
  - SR net of costs. Find the cost per unit of turnover in Harvey et al. (2018), "The impact of volatility targeting"; if the reference is unavailable, use 1 bp per unit traded on each leg. State the assumption.
  - SR excluding September 2008 – March 2009 and March 2020.
  - The annualized volatility of each piece of the weight. The paper says both are 11.6%.

**Tests.** `tests/test_strategy.py`:
- On the demo fixture with planted negative betas, the SR is positive.
- On the zero-effect fixture, the SR is near 0 (|SR| < 0.3).
- The weight is 0 outside week4 and the first day of the month when the threshold is 0.
- The factor-regression alpha matches a hand OLS.

Out of scope: running on real data (TASK-018).

## Acceptance

- `uv run pytest tests/test_strategy.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only table_6a table_6b table_6c figure_6` writes all four exhibits to `output/demo/`.

## Verify

```sh
uv run pytest -q tests/test_strategy.py
uv run python3 -m rebal.exhibits --all --demo --only table_6a table_6b table_6c figure_6
ls output/demo/table_6* output/demo/figure_6*
```
