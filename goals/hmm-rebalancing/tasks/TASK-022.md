---
id: TASK-022
title: Audit the cost units and the delta=0 contribution
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-5. TASK-018 ran the cost module on the real panel and got a headline of 4,193.69 bps per year (about $8.4T on $20T). The paper reports 8 bps ($16B). Issue [#30](https://github.com/jesusvillota/replicate/issues/30) shows two problems: the unit arithmetic disagrees with the paper's worked example, and the delta=0 threshold dominates the average. The cost number cannot be read as an economic estimate until both are explained.

## Scope

Change only `src/rebal/exhibits/costs.py`, `tests/test_costs.py` and `docs/methods/costs.md`. Keep the column layout of `output/tables/costs.csv` and `figure_D5` unchanged; TASK-023 adds the canonical comparison exports afterwards.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**1. Units.** Today `annual_cost(-0.39, 0.01, 12)` returns 468 bps. The paper's worked example (§2.1.1, PDF p.21; paper-notes §3.8) says about 5 bps for the same inputs. Read the paper's text and footnotes, find the unit reading under which the example gives about 5 bps, and show it as a test. Then check the same reading against the other paper numbers: Threshold 6–27 bps over delta 0–2.5% (mean 15; 11 with a 1% trade), the Calendar trader at T−4 (about 9 bps), and the random-date mean (0.6 bps). Fix `annual_cost` and every path that feeds it (trade size, trades per year, decimal versus percent). If the paper's own arithmetic is inconsistent, say so and pick the reading that matches most of its numbers.

**2. The delta=0 case.** On the real panel the delta=0 impact is −8.37734 and its fixed-1%-trade cost is 211,108.96 bps. The daily-reset series `thr_000` is nearly a scaled copy of the current return (`max |thr_000 − 0.24·ret| = 0.0019`), and `ret` is also a regressor. The design is full rank (6,317 × 7, rank 7), so it is badly conditioned, not singular. Check the sensitivity of the delta=0 slope, and decide how delta=0 enters the average. If the choice moves the headline cost by more than 2× and the paper does not settle it, raise a `Goal-Decision` instead of picking silently.

**3. Document.** Update `docs/methods/costs.md` with the unit convention, the delta=0 treatment and the reason for each. Say which paper numbers the corrected code reproduces and which it does not.

Out of scope: `rebal.compare`, other exhibits, new data.

## Acceptance

- `uv run pytest -q tests/test_costs.py` passes. It includes a test that the paper's worked example gives about 5 bps, and a test that guards the delta=0 treatment.
- `uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5` writes both exhibits to `output/demo/`.
- The outcome gives the real-panel smoke result: the headline in bps and in $, and the Threshold range, each next to the paper (8 bps, $16B, 6–27 bps). It states whether the corrected code now agrees in size, and if not, why.

## Verify

```sh
uv run pytest -q tests/test_costs.py
uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5
ls output/demo/costs* output/demo/figure_D5*
```
