---
id: TASK-018
title: Core exhibits on the real panel and comparison with the paper
milestone: M-2
state: approved
depends_on: [TASK-012, TASK-015, TASK-016, TASK-017, TASK-020, TASK-021]
delivery: pr
kind: run
---

## Why

Serves SC-3, SC-4 and SC-5, and is the exit of M-2. This task runs the merged code on the real panel. It produces every core exhibit and writes `docs/results/core.md`, which compares each one with the paper.

## Scope

This task writes no new analysis code. It runs on the MacBook; the whole run takes minutes, so no cluster, shards or scale gate are needed.

**Steps.**

1. Check the panel: `uv run python3 -m rebal.panel --check`. It must end with `PANEL OK`; if the panel is missing, run `--build` first.
2. Build both signal frames: `uv run python3 -m rebal.signals --build --timing clean` and `--timing literal`.
3. Run `uv run python3 -m rebal.exhibits --all` with the default `clean` timing. Commit `output/tables/` and `output/figures/`.
4. Robustness runs. Write each to a separate output subfolder: `output/tables/robustness/<variant>/` (`output/figures/robustness/<variant>/` for figures).
   - `--timing literal`, for `table_1` and `figure_2` only;
   - the robustness proxy panel `daily_panel_alt.parquet` from DEC-001, for `table_1`, `table_3` and `costs` only.
5. Run `uv run python3 -m rebal.compare --out docs/results/core.md`.
6. Under the generated tables in `docs/results/core.md`, add a section "Reading the gaps":
   - which exhibits replicate in sign, size and significance;
   - which do not;
   - for each gap, the most likely cause: the proxy (cite `docs/data/proxy_comparison.md`), the timing reading, the sample N, or a method ambiguity from §5;
   - the results of the timing and proxy robustness runs.

**If a result looks like a bug in merged code**, do not fix it here. List it under "Proposed follow-ups" in the outcome, with the evidence.

Out of scope: the extension exhibits (M-3).

## Acceptance

- `uv run python3 -m rebal.exhibits --all` exits 0. `ls output/tables output/figures` shows every core exhibit listed in SC-3, plus `costs` and `table_6a`–`table_6c`.
- `docs/results/core.md` exists. Its summary gives the sign-match and significance-match rates.
- The outcome quotes, next to the paper's values:
  - Table 1 col. (1): Threshold and Cal × week4, with their t-statistics;
  - the headline cost in bps and in $;
  - the strategy SR.
- `uv run pytest` passes on the merged code.

## Verify

```sh
uv run python3 -m rebal.panel --check | tail -1
uv run python3 -m rebal.signals --build --timing clean && uv run python3 -m rebal.signals --build --timing literal
uv run python3 -m rebal.exhibits --all; echo "exit=$?"
uv run python3 -m rebal.compare --out docs/results/core.md && sed -n '1,40p' docs/results/core.md
uv run pytest -q
```
