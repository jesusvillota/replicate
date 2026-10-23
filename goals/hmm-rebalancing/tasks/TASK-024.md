---
id: TASK-024
title: 'Table 4: long-sample code on demo data'
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-6. Table 4 of the paper repeats the main regression on a long sample from 1961 and splits it at 1997-09-10 (paper-notes §3.6 and §4). It shows that the effect is absent before 1997 and strong after. This task builds the code on demo data; TASK-030 runs it on the real data.

## Scope

Module: `src/rebal/exhibits/long_sample.py` (exhibit `table_4`). Test: `tests/test_long_sample.py`. Methods doc: `docs/methods/long_sample.md`.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**Inputs.**
- Equity return: `r_mkt_french = Mkt-RF + RF` from `data/public/french/` (D16). It starts 1926, so it covers the whole table.
- 10-year return (D17): `data/public/gsw/` and `rebal.proxies`. GSW has no 10-year yield before 1971-08-16. FRED `DGS10` (`data/public/fred/DGS10.csv`, H.15 constant-maturity, from 1962-01-02) is already fetched.
- Controls in the paper's Table 4 regression are as in eq. (4); take the control set from paper-notes §4 (PDF p.36) and use only those with history for the whole sample. List the rest as omitted.

**Settle §5.13 in the methods doc.**
1. How the yield becomes a holding return. Reuse the merged method in `rebal.proxies` (see `docs/methods/proxies.md`) for the part of the sample it covers.
2. The pre-1971 10-year yield. Default: use `DGS10` before 1971-08-16 with the same conversion, and document the seam and the difference between a par yield and a zero-coupon yield. Report the first usable date honestly: the sample starts in 1962 or later, not on the paper's 1961-06-16. Expose the choice as a flag. Name the real start and N for each column in the outcome.
3. Whether the French total return equals `Mkt-RF + RF`.

**Build.** Build the signals for the long sample with `rebal.signals.build` on the long return pair (the equity-minus-bond excess pair with the same cash leg convention as the main panel). Warm up the 252-day momentum on earlier history, as the main panel does. Write `table_4.csv` in the regression layout with `column` 1 = full sample, 2 = up to 1997-09-09, 3 = from 1997-09-10, terms `threshold` and `calendar:week4` (as in `docs/results/targets.csv`).

**Tests.** The demo builds a synthetic long sample with a planted negative Threshold effect after the split date and none before. The test recovers the planted split, and finds about zero for a zero effect. The 1961 sample date logic (first usable date) has its own test.

Out of scope: the real run; changes to the main panel.

## Acceptance

- `uv run pytest -q tests/test_long_sample.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only table_4` writes `output/demo/table_4.csv` with the contract columns and the three `column` values.
- `docs/methods/long_sample.md` states the yield-to-return method, the pre-1971 choice, the real first date, and the control set.
- The outcome gives the real-data smoke result per column, next to the paper (−0.1809 / −0.0157 / −0.3685 for Threshold).

## Verify

```sh
uv run pytest -q tests/test_long_sample.py
uv run python3 -m rebal.exhibits --all --demo --only table_4
head -5 output/demo/table_4.csv
```
