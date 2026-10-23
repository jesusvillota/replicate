# TASK-019 outcome

## Acceptance

- [ ] `goal check --goal hmm-rebalancing --json` reports no errors **after
  replanning**. The baseline command exited 0 and returned `issues: []` and
  `ok: true`, but no replan was applied. This is baseline evidence only.
- [ ] `goal graph --goal hmm-rebalancing` shows the new M-3 tasks, each
  depending only on merged work. The command exited 0, but M-3 still contains
  only TASK-019. No task IDs were allocated.
- [ ] The PR body lists the new task IDs and titles. No tasks were created;
  the draft PR records the blocker and the decision request instead.

## Summary

Blocked: the installed goal CLI cannot replan in the required task worktree.
The owner requires this work to stay on `goal/hmm-rebalancing/task-019` and
forbids edits to other tasks, decisions and `goal.yaml`. TASK-019 calls for
new specs through the goal-setup replanning procedure. That procedure requires
the CLI for structural changes. The CLI selects the separate main checkout
for both plan mutations and validation whenever that checkout exists.

Read TASK-019, the worker protocol, all owner rules, the goal definition,
`docs/results/core.md`, `docs/data/sources.md`, `docs/data/wrds_inventory.md`,
the TASK-012 and TASK-018 outcomes, and the relevant source cards and paper
ambiguities. A read-only research agent checked M-3 data availability.
No analysis code, data, task specs, decisions, goal definition or README changed.
No structural commands, worker dispatches, downloads or cluster jobs ran.
This PR changes only this outcome. It does not deliver the replan.

Inspected revision: `c537114c1030cc3e16a5d7f1d4ae76dcaccab44e`.
Live status reports TASK-001–018 and TASK-020–021 done, with DEC-001 and
DEC-002 accepted. TASK-019 is running. New exhibit work can therefore use
merged M-1/M-2 inputs once the planning authority issue is resolved.

### Evidence for the blocker

From this task worktree, `goal show TASK-019 --goal hmm-rebalancing --json`
returned:

```text
"path": "/Users/jesusvillotamiranda/GitHub/replicate/goals/hmm-rebalancing/tasks/TASK-019.md"
```

That path belongs to the separate main checkout. Source inspection of
`tools/goal-rust/goal-core/src/store.rs` in the config repository confirms
that `locate` selects `worktree_for(base)`. `mutation_cli.rs` uses that
workspace, and `mutate.rs:apply` commits there. `--no-sync` disables sync,
not workspace selection. Neither `goal add --help` nor `goal check` offers
a branch-local plan option. Running `goal add` would risk modifying and
committing in another checkout. It was not attempted.

Reported the CLI limitation after duplicate searches:
https://github.com/jesusvillota/config/issues/208.
No out-of-scope fix was attempted.

## Decision request

How should TASK-019 create and verify its replan while preserving branch isolation?

1. Have the interactive orchestrator perform the replan at the plan root.
   This uses the supported CLI path and permits immediate dispatch of new
   approved work. It changes where the plan is committed, so it requires
   an explicit change to this task's branch-only delivery instruction.
2. Add branch-local planning and verification support to the CLI, then resume
   TASK-019. This preserves the required PR review boundary. It needs a
   separate config change and safe ID allocation across concurrent planners.
3. Explicitly authorize hand-written new specs and an isolated validation
   checkout for this task. This avoids the current CLI routing limitation,
   but departs from the required structural workflow and needs a clear rule
   for allocating IDs and dispatching tasks before the planning PR merges.

### Recommendation

Use option 2 to preserve the owner's stated branch and PR boundary. Keep
TASK-019 blocked until branch-local CLI support exists. Do not redirect
mutations into main or bypass worker authority through environment changes.
Once resumed, clarify that new specs are permitted for this planning task.

### Prepared M-3 scope

These are proposed titles, not allocated task IDs or executable specs:

- Table 4 long-sample code on demo data. Document the yield-to-return method.
  GSW ten-year yields start 1971-08-16; name the pre-1971 source gap as a
  manual task. Do not call the available history a 1961 replication.
- Table 5 equity-segment code on demo data. Use IWB/IWM/IWD/IWF total-return
  proxies from May 2000, `rebal.signals.build`, the 90/10 size portfolio and
  a documented Value/Growth falsification portfolio under §5.14.
- Table D.4 code on demo data. Use `r_sp500tr - r_agg`; VBMFX supplies the
  accepted bond proxy without a splice.
- Table D.9 alternative-control code on demo data. Use BEX and available ARA
  overlap. Skip the unavailable private FEARS extension; label its public
  2004–2011 subset separately if used for a supplementary check.
- Table D.14 code on demo data. Use exact MSCI 899901 USD NETR from December
  2000, subtract `rf_3m`, and add the extra signal lag. Preserve the early gap.
- Figure 1 pension-allocation code on demo data. Use PPD FY2003–2022, with
  documented weighting, changing plan coverage and sparse target fields.
- Figure 5 trading-correlation code on demo data. Settle §5.11–§5.12:
  COT market/group selection, report dates, weekly aggregation and lags.
  LTPos contains weekly mean daily directional changes, not weekly position
  differences. Preserve the 39 disjoint ICI blocks. Skip ANcerno.
- Final-report code/template on fixture outputs. Cover every exhibit and link
  `docs/data/sources.md`; distinguish missing joins from failed replication.
- Separate work tasks for TASK-018 follow-ups: main-versus-robustness discovery
  (#28), export/target join keys (#29), and the cost-unit audit (#30).
- One real-data run and final report, using merged extension code. Record
  samples, proxy limits, local tests and all exhibit comparisons. Run no new
  analysis code in that task. Its prerequisite code must merge before launch.
- An owner decision for the optional latest-sample and 3:30 PM extensions.
  If selected, add a manual CEMFI-PC SpiderRock data-copy task. Do not copy
  data or start optional work before that decision.

The resumed planner must also reconcile the literal "each depending only on
merged work" acceptance with creating the final run now: it needs new work
outputs. Either defer that run's creation until those outputs merge or obtain
an explicit acceptance clarification. Do not omit required dependency edges.

## Verify evidence

The exact baseline Verify block ran locally and exited 0:

```sh
goal check --goal hmm-rebalancing --json
goal graph --goal hmm-rebalancing
```

Output tail:

```text
{
  "goal": "hmm-rebalancing",
  "issues": [],
  "ok": true
}
── M-1 · Data sourced 12/12 ✓ collapsed ──
── M-2 · Core replication on the real panel 8/8 ✓ collapsed ──
── M-3 · Extensions and final report 0/1 ──
▶  TASK-019  Plan: decompose M-3  [running]
```

`git diff --check` also exited 0. These results do not establish acceptance:
the CLI inspected the existing plan, and no new M-3 tasks exist. No application
tests were needed for this outcome-only change. GitHub Actions were not read.
Delivery uses exit (B): a committed outcome and a draft PR with `Goal-Blocked`
and `Goal-Decision` markers. No merge was performed.
