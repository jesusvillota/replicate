---
id: TASK-030
title: 'Final run: all exhibits on the real panel and the replication report'
milestone: M-3
state: approved
depends_on: [TASK-022, TASK-023, TASK-024, TASK-025, TASK-026, TASK-027, TASK-028, TASK-029, DEC-004]
delivery: pr
kind: run
---

## Why

Serves SC-3, SC-4, SC-5 and SC-6, and is the exit of M-3. This task runs all merged code on the real panel, regenerates every exhibit, and writes the final replication report. It writes no new analysis code.

## Scope

Runs on the MacBook; the whole run takes minutes. No cluster, shards or scale gate. Read first: the outcomes of TASK-022 to TASK-029, `docs/results/core.md`, and the accepted DEC-004. If DEC-004 chose an extension, its tasks are dependencies and you run them too; otherwise skip them.

**Steps.**
1. Update the repo to the merged `main`. Check the panel: `uv run python3 -m rebal.panel --check` must end with `PANEL OK`.
2. Build both signal frames: `uv run python3 -m rebal.signals --build --timing clean` and `--timing literal`.
3. Run `uv run python3 -m rebal.exhibits --all` (default `clean` timing). Commit `output/tables/` and `output/figures/`. The inventory must include `table_4`, `table_5`, `table_D4`, `table_D9`, `table_D14`, `figure_1` and `figure_5` as well as every core exhibit.
4. Rerun the robustness variants as TASK-018 did, into `output/tables/robustness/<variant>/` and `output/figures/robustness/<variant>/`: `--timing literal` for `table_1` and `figure_2`; the alternative proxy panel `daily_panel_alt.parquet` for `table_1`, `table_3` and `costs`.
5. Run `uv run python3 -m rebal.compare --out docs/results/core.md`. It must now read the main outputs only, with no manual workaround.
6. Extend `docs/results/gap_notes.csv` with one note per M-3 exhibit and per exhibit whose result changed after TASK-022 and TASK-023. Each note names a cause from the allowed list and cites the evidence (proxy comparison, timing run, sample N, or a method choice in `docs/methods/`). Never invent a cause: if the cause is unknown, say so in the note.
7. Run `uv run python3 -m rebal.report --out docs/results/replication_report.md`. Check by hand that every exhibit row is right against the CSVs. Do not edit the generated file by hand; fix the notes file or raise the problem.

Out of scope: any new analysis code, any change to methods, any new data. If a merged module fails on the real data, do not fix it here: report it in the outcome, open an issue, and finish the rest.

## Acceptance

- `uv run python3 -m rebal.exhibits --all` exits 0. A listing shows every exhibit ID in `docs/contracts/exhibits.md` except those the methods docs mark as not available (FEARS column; ANcerno).
- `docs/results/replication_report.md` exists and has a row for every contract ID. Its summary gives the sign-match and significance-match rates.
- `uv run python3 -m rebal.compare` run without any manual change joins the costs, Table 6 and figure targets (the matched count is above the 252/399 of TASK-018).
- The outcome quotes, next to the paper's values: Table 1 column (1) Threshold and Cal × week4 (with t); Table 4 (three samples); Table 5; the headline cost in bps and in $; the strategy Sharpe ratio.
- `uv run pytest -q` passes on the merged code.

## Verify

```sh
uv run python3 -m rebal.panel --check | tail -1
uv run python3 -m rebal.signals --build --timing clean && uv run python3 -m rebal.signals --build --timing literal
uv run python3 -m rebal.exhibits --all; echo "exit=$?"
uv run python3 -m rebal.compare --out docs/results/core.md && sed -n '1,20p' docs/results/core.md
uv run python3 -m rebal.report --out docs/results/replication_report.md && sed -n '1,40p' docs/results/replication_report.md
uv run pytest -q
```
