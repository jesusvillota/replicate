# TASK-019 outcome

## Acceptance

- [x] `goal check --goal hmm-rebalancing --json` reports `ok: true` and no issues after the replan.
- [x] `goal graph --goal hmm-rebalancing` shows the new M-3 tasks with explicit dependency edges.
  The work tasks depend only on merged work. TASK-030 (the final run) depends on the new work tasks.
  The owner clarified this in DEC-003.
- [x] The new task IDs and titles are listed below.

## Summary

The first worker attempt (PR #32) stopped because the `goal` CLI cannot plan inside a task worktree.
The owner accepted DEC-003 option 1: the orchestrator replans at the plan root. This outcome records that replan.
PR #32 is closed without merge; its blocked outcome is superseded by this one.

New tasks (all in M-3):

| ID | Title | Depends on |
|---|---|---|
| TASK-022 | Audit the cost units and the delta=0 contribution (issue #30) | none |
| TASK-023 | Comparison: main-run discovery and canonical exports (issues #28, #29) | TASK-022 |
| TASK-024 | Table 4: long-sample code on demo data | none |
| TASK-025 | Table 5: equity-segment code on demo data | none |
| TASK-026 | Tables D.4, D.9 and D.14: robustness code on demo data | none |
| TASK-027 | Figure 1: pension-allocation code on demo data | none |
| TASK-028 | Figure 5: trading-correlation code on demo data | none |
| TASK-029 | Final-report generator on fixture outputs | TASK-023 |
| DEC-004 | Choose the optional extensions: latest sample and 3:30 PM check | none |
| TASK-030 | Final run: all exhibits on the real panel and the replication report | TASK-024 to TASK-029, DEC-004 (TASK-022 and TASK-023 via TASK-029) |

Choices:
- Tables D.4, D.9 and D.14 share one task. They use one regression helper and are small. Issues #28 and #29 share one task because both change `rebal.compare`.
- TASK-029 builds the report generator on fixtures. TASK-030 only runs it, so the final run writes no analysis code.
- `docs/contracts/exhibits.md` now lists `table_4`, `table_5`, `figure_1` and `figure_5` (commit 4cf3e09), so parallel tasks do not edit the contract.
- Every work task may run on the real panel as a smoke check but commits no outputs. TASK-030 commits them.
- The pre-1971 10-year yield for Table 4 uses FRED `DGS10` (daily from 1962-01-02), already fetched. No manual task is needed. The sample therefore starts in 1962, not 1961-06-16; TASK-024 records this.
- The optional extensions are DEC-004. If the owner chooses the 3:30 PM check, a manual data-copy task (SpiderRock SPY 1-minute bars on the CEMFI PC) is added then.
- No outside blocker exists for the planned tasks. FEARS and ANcerno stay "not available".
- The `W104` warnings from `goal check` (redundant dependencies on TASK-022 and TASK-023) were fixed by removing those edges.

## Verify evidence

```sh
goal check --goal hmm-rebalancing --json   # ok: true, issues: []
goal graph --goal hmm-rebalancing
```
