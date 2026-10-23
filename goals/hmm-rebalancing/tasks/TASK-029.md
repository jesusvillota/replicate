---
id: TASK-029
title: Final-report generator on fixture outputs
milestone: M-3
state: approved
depends_on: [TASK-023]
delivery: pr
---

## Why

Serves SC-6. The goal ends with one report that covers every exhibit of the paper: whether it replicates, which proxy or ambiguity explains each gap, and a link to the data map. The report is generated from the outputs, so that TASK-030 can regenerate it from the real run without hand editing. This task builds the generator and the template on fixture outputs.

## Scope

Module: `src/rebal/report.py`, run as `uv run python3 -m rebal.report --out docs/results/replication_report.md`. Test: `tests/test_report.py`. Methods doc: `docs/methods/report.md`.

No cluster jobs. Build and test on the demo fixtures (`rebal.io` with `demo=True`, `rebal.demo`). Follow `docs/contracts/` exactly; `docs/contracts/exhibits.md` already lists the exhibit IDs. Write every choice about a paper ambiguity (paper-notes §5) in the methods doc named below, and expose the cheap ones as CLI flags.

**Shared files.** Several M-3 tasks run in parallel. Put your code in your own module and your own test file. Do not edit `rebal.demo`, `rebal.io`, `rebal.regress`, `rebal.signals`, `rebal.panel`, `rebal.compare`, `docs/data/sources.md` or the contracts. If a shared module needs a change, keep it additive and tiny, and say so in the outcome.

**Real-data smoke check (optional).** The real panel is at `~/data/replicate/processed/`. You may run your module on it to catch real-data problems. Quote the numbers in the outcome, then run `git restore output/` and delete new untracked files under `output/`. TASK-030 commits the real outputs; this task commits none.

**Content.** The report has these parts:
1. **Summary.** Match counts from `rebal.compare` (targets joined, sign rate, significance rate), and the list of exhibits by status.
2. **Exhibit table.** One row for every ID in `docs/contracts/exhibits.md` plus the text-only results (costs, strategy). Columns: exhibit, status, headline paper value, our value, and a short note. Status values: `replicates` (sign and significance agree, size within a stated tolerance), `partly` (sign agrees, size or significance differs), `fails`, `not available` (data cannot be had: FEARS, ANcerno), `not run`. Define the tolerance in the methods doc.
3. **Gap notes.** Notes are read from a small checked-in file, `docs/results/gap_notes.csv` (columns `exhibit,cause,note`), where `cause` is one of `proxy`, `timing`, `sample`, `method`, `data`. The generator never invents a cause. The initial file carries the causes already recorded in `docs/results/core.md` ("Reading the gaps"); TASK-030 extends it for the M-3 exhibits.
4. **Data and proxies.** A table of the proxy used for each dataset D1–D28, read from `docs/data/sources.md`, with a link to it and to `docs/data/proxy_comparison.md`.
5. **Method choices.** A list of links to every file in `docs/methods/`.

**Rules.** The report distinguishes a missing join from a failed replication (a target with no export is `not run` or listed with its reason, never `fails`). It runs on fixture outputs (`--demo`) so that the tests need no real data. It overwrites only its own output file. Keep it one module, standard library plus pandas.

**Tests.** On a small fixture with one matching, one partly matching, one failing and one unavailable exhibit, the statuses are right. Every contract ID appears exactly once. A missing gap note leaves the cause blank, not invented.

Out of scope: the real run and the real-data gap notes for new exhibits (TASK-030); changes to `rebal.compare` (TASK-023, merged first).

## Acceptance

- `uv run pytest -q tests/test_report.py` passes.
- `uv run python3 -m rebal.report --demo --out /tmp/replication_report_demo.md` exits 0 and the file has the five parts.
- Every ID in `docs/contracts/exhibits.md` appears in the demo report's exhibit table.

## Verify

```sh
uv run pytest -q tests/test_report.py
uv run python3 -m rebal.report --demo --out /tmp/replication_report_demo.md
grep -c '^|' /tmp/replication_report_demo.md
```
