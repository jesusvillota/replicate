---
id: TASK-032
title: 'Latest sample (footnote 32): real run and comparison'
milestone: M-3
state: approved
depends_on: [TASK-031]
delivery: pr
kind: run
---

## Why

Serves SC-6 and DEC-004 (accepted: latest sample only). This task runs the merged `rebal.latest` code on the real panel and reports whether the main result of footnote 32 holds to the latest date.

## Scope

Runs on the MacBook; the run takes minutes. No cluster. Write no new analysis code. Read first: `docs/methods/latest_sample.md` and the TASK-031 outcome.

**Steps.**
1. Update the repo to the merged `main`. Check the panel: `uv run python3 -m rebal.panel --check | tail -1` must print `PANEL OK`. The panel and the signal files already run to 2026-07-31; do not rebuild them.
2. Run `uv run python3 -m rebal.latest`. Commit `output/tables/robustness/latest/` (`table_1.csv`, `table_3.csv`, `latest_comparison.csv`).
3. Check that `git status --short output/tables` shows no change outside `robustness/latest/`. If a main exhibit changed, run `git restore` on it.
4. Write `docs/results/latest_sample.md`. Put the 1997-2023 and the latest values side by side: Table 1 column (1) Threshold and Cal x week4 (coefficient, t, N), and Table 3. Give the actual last sample date. State in plain words whether the sign and the 5% significance hold. Quote the paper's footnote 32 claim next to it. Do not invent a cause for any change; if the cause is unknown, say so.

Out of scope: any new analysis code; a 2025-12-31 run (dropped by the owner); the 3:30 PM check; the final report (TASK-030). If the merged module fails on the real data, do not fix it here: report it in the outcome, open an issue and stop.

## Acceptance

- `uv run python3 -m rebal.latest` exits 0.
- `output/tables/robustness/latest/latest_comparison.csv` exists and its `latest` sample ends on the last date of the panel.
- `git diff --stat main -- output/tables output/figures` lists files only under `robustness/latest/`.
- `docs/results/latest_sample.md` quotes both samples and answers: do the signs and the 5% significance hold? It quotes the exact numbers.
- `uv run pytest -q` passes.

## Verify

```sh
uv run python3 -m rebal.panel --check | tail -1
uv run python3 -m rebal.latest; echo "exit=$?"
column -s, -t output/tables/robustness/latest/latest_comparison.csv | head -30
git status --short output/
uv run pytest -q
```
