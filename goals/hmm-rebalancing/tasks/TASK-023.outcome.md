# TASK-023 outcome

Status: Delivered. Local acceptance and Verify checks pass.

## Summary

Default discovery now selects top-level main CSVs. It also retains the named
legacy magnitude sidecar, without recursive discovery. `--variant NAME`
selects only `robustness/NAME/` under each input folder. It never falls back
to main outputs or another variant.

Costs, Table 6A–C, calibration figures and horizon figures now write thirteen
`<id>_comparison.csv` sidecars. Existing plotted and regression CSVs remain
available. Values use their existing units, including the corrected TASK-022
cost units and the accepted DEC-005 exclusion of delta=0 from summaries.
No analysis estimates were changed.

Every missing numeric target has a reason. FEARS and ANcerno are marked
`not available`. Figure 6's axis transformation and the random-date cost sign
remain unresolved, as the task requires. Their six target keys join with
blank values. These keys count toward export coverage, never numeric matches.
Two Figure 4 summary targets are also blank: the demo confidence bands do
not cross zero on the sampled horizon grid.

Demo coverage: **386/399 numeric targets**, **84/84 core target keys**
across all thirteen requested groups. All **13** unmatched targets are listed:
six paper-ambiguity targets, five unavailable-source targets and two summaries
without a sampled crossing. The report distinguishes joined keys from values.

The methods document records exact mappings, sidecar naming, units and summary
rules. Figure 2 uses the first sampled delta below the paper's 1% reference;
`--weakening-critical-t` exposes that choice. Figure 4 uses the first horizon
whose plotted 95% band contains zero. No interpolation or invented crossing
is used.

Most new logic is in `rebal.comparison_exports`. The restricted shared
`rebal.compare` has only small additive integration changes: discovery and
coverage calls, the variant argument, and the joined-key indicator. This is
the shared-module exception required by the task's discovery scope.
Exporter metadata lists the new sidecars. Tests retain the original schema
checks and extend output lists for those files.

Verified analysis revision: `376e969bef915641594dce8ff7f9f11522cfd73b`.
Only this outcome documentation follows that revision. The branch rebased
onto `origin/main` without conflicts. No task specs, decisions, contracts,
`goal.yaml`, target values or real output files changed. No cluster or
real-data runs were needed. Demo outputs remain ignored.

Proposed follow-up: TASK-030 should preserve these explicit ambiguity and
unavailable-source reasons in the final comparison. No new task was created.

## Acceptance

- [x] `uv run pytest -q tests/test_compare.py` exited 0: **24 passed in 8.17s**.
  Includes distinct main/robustness values, API and CLI variant selection,
  no fallback, and actual canonical exports from every requested group.
  All 84 core keys join; numeric checks preserve the six explicit ambiguities.
- [x] `uv run python3 -m rebal.exhibits --all --demo` exited 0 in this session.
  Artifact inspection confirmed all **13 canonical comparison CSVs**.
  A final figure-only rerun verified the updated lineage helper. Metadata
  checks confirmed sidecar counts of 5 calibration, 2 horizon, 4 strategy
  and 2 costs. No demo outputs are committed.
- [x] `uv run python3 -m rebal.compare --demo` exited 0 and wrote
  `output/demo/compare.md`. Its `Joined exhibit keys` line contains all
  thirteen core groups. It reports **386/399 numeric matches** and explains
  every one of the **13** unmatched targets. An independent artifact check
  counted each reason row and verified all **84/84** core keys joined.

## Verify evidence

All three specified Verify commands exited 0. Output tails below use paths
relative to the repository root; terminal wrapping is removed.

```text
$ uv run pytest -q tests/test_compare.py tests/test_costs.py tests/test_strategy.py tests/test_horizons.py
...........................................................              [100%]
59 passed in 20.80s
$ uv run python3 -m rebal.exhibits --all --demo
output/demo/figure_5.csv
output/demo/figure_5.pdf
output/demo/figure_5.metadata.json
$ uv run python3 -m rebal.compare --help
  --demo             Read only output/demo CSVs.
  --variant VARIANT  Compare only robustness/NAME; default: main outputs.
  --out OUT          Markdown destination (default: output/[demo/]compare.md).
```

Additional checks: Ruff lint and format checks pass on all ten changed Python
files. `git diff --check` passes. The artifact checker confirms thirteen
sidecars, all 84 core target keys, every missing-target reason and metadata.
GitHub Actions were not inspected or used as a delivery gate.

PR: https://github.com/jesusvillota/replicate/pull/39, into `main`, with
`Goal-Task: hmm-rebalancing/TASK-023` and label `goal:hmm-rebalancing`.
The PR is not merged.
