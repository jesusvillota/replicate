---
id: TASK-025
title: 'Table 5: equity-segment code on demo data'
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-6. Table 5 repeats the regression on equity segments: Russell 1000 versus Russell 2000 (a 90/10 portfolio), and Russell 1000 Value versus Growth as a falsification test (paper-notes §3.6, §4 and §5.14). This task builds the code on demo data; TASK-030 runs it on real data.

## Scope

Module: `src/rebal/exhibits/segments.py` (exhibit `table_5`). Test: `tests/test_segments.py`. Methods doc: `docs/methods/segments.md`.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**Inputs.** Panel columns `r_r1k`, `r_r2k`, `r_r1kv`, `r_r1kg` (D18). These are CRSP total returns of the ETFs IWB, IWM, IWD and IWF, starting May 2000 (D18 proxy; see `docs/data/sources.md`). Cash leg: `rf_3m`.

**Method (settle §5.14 in the methods doc).**
1. R1K versus R2K: simulate the 90/10 portfolio with `rebal.signals.build` on the segment pair (R1K as the large leg, R2K as the small leg, target 90/10 instead of 60/40). Signals, momentum and `ret` are built within the segment. The dependent variable is the next-day R1K minus R2K return.
2. Value versus Growth: the paper does not state the weights. Default: the same 90/10 construction with Value as the 90% leg, plus a flag for 50/50. Say why. The outcome is the next-day Value minus Growth return.
3. Sample: 2006-08-17 to 2023-03-17, as in the paper (N = 4,175). ETF history before that only initializes the signals. Record the real N.
4. Controls: as eq. (4), built within the segment (momentum, `ret`); controls that need other series (VIX, MOVE, and so on) as in the main Table 1 column (1). State the list.

Write `table_5.csv` in the regression layout: `column` 1 = R1K/R2K, 2 = Value/Growth; terms `threshold` and `calendar:week4`.

**Tests.** A planted Threshold effect in the segment spread is recovered; a zero effect gives about zero; the Value/Growth column on a zero-effect fixture is insignificant. Check that the segment signals are built from the segment returns and not from the futures pair.

Out of scope: the real run; the Russell price-index check (`^RUI` and the others).

## Acceptance

- `uv run pytest -q tests/test_segments.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only table_5` writes `output/demo/table_5.csv` with columns 1 and 2.
- `docs/methods/segments.md` states the weights, the sample, the controls and the reasons.
- The outcome gives the real-data smoke result (Threshold and Cal × week4 with N), next to the paper (−0.2054 / −0.1174 for R1K/R2K; −0.0339 / −0.0678 for Value/Growth).

## Verify

```sh
uv run pytest -q tests/test_segments.py
uv run python3 -m rebal.exhibits --all --demo --only table_5
head -5 output/demo/table_5.csv
```
