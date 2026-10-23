---
id: TASK-026
title: 'Tables D.4, D.9 and D.14: robustness code on demo data'
milestone: M-3
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-6. Three robustness tables of the paper's appendix need extra inputs: Table D.4 (S&P 500 total return minus the Aggregate Bond index instead of the futures pair), Table D.9 (alternative uncertainty and attention controls), and Table D.14 (international equity). See paper-notes §3.6, §4 and §5.15.

## Scope

Module: `src/rebal/exhibits/robustness_extra.py` (exhibits `table_D4`, `table_D9`, `table_D14`). Test: `tests/test_robustness_extra.py`. Methods doc: `docs/methods/robustness_extra.md`.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**Table D.4.** Dependent variable `r_sp500tr − r_agg` (panel columns, D4 and D5). Settle §5.15 in the methods doc: whether the signals are rebuilt from this pair (default: yes, with `rebal.signals.build` and its `r_sp500tr` option as needed) or kept from the futures pair; expose the other reading as a flag. `r_agg` is VBMFX over the full study, with no splice. Output `column` 1; terms `threshold` and `calendar:week4`.

**Table D.9.** The main Table 1 column (1) regression with one extra control per column. `column` 1 = `ra_bex`, 2 = `unc_bex`, 4 = `ara`. Column 3 (FEARS) is not available for the full sample (the authors' data were private). Do not write column 3, and say so in the methods doc and in a `skipped` note in the module's metadata sidecar. State the scaling you apply to each control (paper-notes §5.7) and the real N for each column.

**Table D.14.** Dependent variable `r_acwxus − rf_3m` (MSCI ACWI ex USA net total return, exact, from 2000-12-29). The signals are lagged one more day (t−1). The control is the 2-day trailing S&P 500 return. Output `column` 1; terms `threshold` and `calendar:week4`. The panel has no MSCI returns before 2000-12-29; do not fill them. Record the real N (paper: 6,097; ours will be smaller) and the cause.

**Tests.** For each table a planted effect is recovered and a zero effect gives about zero. D.14: the extra lag is applied (a signal planted at t−1 only is found with the extra lag and not without). D.9: the skipped column is absent.

Out of scope: the real run; a supplementary FEARS result from the public 2004–2011 subset.

## Acceptance

- `uv run pytest -q tests/test_robustness_extra.py` passes.
- `uv run python3 -m rebal.exhibits --all --demo --only table_D4 table_D9 table_D14` writes the three tables to `output/demo/`; `table_D9.csv` has columns 1, 2 and 4 only.
- `docs/methods/robustness_extra.md` states the D.4 signal reading, the control scaling, the D.14 lag and control, and the skipped FEARS column.
- The outcome gives the real-data smoke results next to the paper: D.4 −0.3970 / −0.3189; D.9 Threshold −0.4493 (ra^BEX) and −0.3731 (ARA); D.14 −0.2723 / −0.2060.

## Verify

```sh
uv run pytest -q tests/test_robustness_extra.py
uv run python3 -m rebal.exhibits --all --demo --only table_D4 table_D9 table_D14
ls output/demo/table_D4.csv output/demo/table_D9.csv output/demo/table_D14.csv
```
