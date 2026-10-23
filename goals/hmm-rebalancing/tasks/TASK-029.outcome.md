# TASK-029 outcome

Status: Delivered. Local acceptance and Verify checks pass.

## Summary

Added `rebal.report`, an existing-output report generator, plus its isolated
fixture tests, reporting methods and checked-in historical gap annotations.
The report has the five specified parts. Its exhibit table contains all 38
contract IDs once, including costs and Table 6 strategy results. It reads
D1–D28 from the master source map and discovers all 15 method documents.
Relative links also work when the destination is outside the repository.

The summary consumes `rebal.compare` results. It distinguishes joined export
keys from numeric matches. Missing exports, blank estimates and unresolved
paper conventions cannot establish failure. Partial FEARS/ANcerno coverage
retains its unavailable-source reasons. Gap causes come only from the checked-in
CSV; absent annotations remain blank. Historical core explanations retain their
tentative wording and do not diagnose fixture or future real-run results.

The methods document defines whole-exhibit status aggregation and a 25% relative
size tolerance with a 0.0001 absolute floor in target units. Both tolerances,
the gap-note file and robustness variant are CLI options. No new analysis
choice about paper-notes section 5 was made. The generator writes only the
requested Markdown file, with lineage inside that file. It uses standard-library
logging to respect the task's standard-library-plus-pandas scope.

Verified implementation revision: `8ce35f9a2d242ccb1b662db312b12c6874993fa7`.
Only this outcome documentation follows that revision. The branch rebased onto
the fetched `origin/main` without conflicts and remains
`goal/hmm-rebalancing/task-029`. No shared module, contract, task specification,
other task, decision, `goal.yaml` or real output was changed. No cluster job
or real-data check was needed. Generated demo artifacts remain ignored.

The full `uv run python3 -m rebal.exhibits --all --demo` exited 0. A subsequent
fixture smoke run also passed, using two random cost schedules rather than
10,000; the final report verification reads those smoke artifacts. These are
synthetic outputs, not evidence of real-data replication. Final coverage is
394/399 export keys and 386/399 numeric targets. Sign agreement is 153/210
(72.9%); significance agreement is 115/148 (77.7%).

Proposed follow-up: TASK-030 should regenerate the report from real outputs
and review/extend gap notes for M-3. No new task was created.

## Acceptance

- [x] `uv run pytest -q tests/test_report.py` exited 0: **13 passed in 3.21s**.
  Tests cover matching, partial, failing, unavailable and missing exports;
  whole-contract coverage; blank unrecorded causes; CLI demo isolation;
  destination-only writes; tolerances; variants; source/method links; and
  integration with actual `rebal.io`/`rebal.demo` descriptive exports.
- [x] `uv run python3 -m rebal.report --demo --out /tmp/replication_report_demo.md`
  exited 0. Independent artifact inspection found exactly **five parts**:
  Summary, Exhibit table, Gap notes, Data and proxies, Method choices.
- [x] Every ID in `docs/contracts/exhibits.md` appears in the demo exhibit table.
  Independent artifact inspection compared the ordered contract list with
  table rows: **38/38 IDs, each exactly once**. It also checked D1–D28 and
  links to every one of the 15 current method documents.

## Verify evidence

The exact three Verify commands ran sequentially with `set -e` and exited 0.
Their terminal tail was:

```text
$ uv run pytest -q tests/test_report.py
.............                                                            [100%]
13 passed in 3.21s
$ uv run python3 -m rebal.report --demo --out /tmp/replication_report_demo.md
Replication report: /private/tmp/replication_report_demo.md
$ grep -c '^|' /tmp/replication_report_demo.md
127
```

Independent artifact check:

```text
PASS: 38/38 contract IDs, each exactly once; 5 report parts; D1–D28; 15 method links
```

Additional verification after the base sync: `uv run pytest -q tests/test_report.py
tests/test_compare.py` exited 0: **37 passed in 9.19s**. Ruff lint and format
checks pass for both new Python files. `uv run ruff` was unavailable in the
project environment, so the same checks ran successfully through `uvx ruff`.
`git diff --check` passes. GitHub Actions were not inspected or used as a gate.

## Review correction

Review of `e00b7c8` found 44 trailing-whitespace errors in the full PR diff.
The earlier `git diff --check` checked only uncommitted changes and missed them.
Converted `docs/results/gap_notes.csv` from CRLF to LF without changing any
CSV field. The fixture CSV writer now sets `lineterminator="\n"` explicitly.

All three Verify commands and the independent five-part/38-ID artifact check
above ran again after the fix. The report reader parsed all 43 annotations;
their fields match the original file at `e00b7c8` exactly. The CSV contains no
carriage returns. `git ls-files --eol docs/results/gap_notes.csv` reports
`i/lf w/lf`. `git diff --check origin/main...HEAD` exits 0 at the verified
implementation revision. Ruff lint and format checks pass for the changed
fixture test file. The combined 37-test result above is from the original
implementation session. PR #40 has no review threads or open review comments.

PR: https://github.com/jesusvillota/replicate/pull/40, into `main`, with
`Goal-Task: hmm-rebalancing/TASK-029` and label `goal:hmm-rebalancing`.
The PR is not merged.
