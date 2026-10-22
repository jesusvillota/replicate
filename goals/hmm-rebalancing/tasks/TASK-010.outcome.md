# TASK-010 outcome

## Summary

Blocked: full CRSP Mutual Funds access is denied; the available VBMFX/VBTLX sample
covers only 2004-01-02 through 2006-12-29.

Live MacBook checks on 2026-10-22 UTC (2026-10-23 in Madrid) authenticated without a
prompt. They listed 229 libraries and successfully listed tables in every library.
The committed inventory records each library and eight replication relevance checks.
The source card records exact queries, permissions, sample fund IDs and coverage.

CRSP Treasuries and Mutual Funds appear through aliases, but their underlying schemas
deny row access. Treasuries are explicitly optional under the task's acceptance rule.
The mutual-fund sample identifies both requested funds, but provides only three years.
That limitation needs a scope decision before implementing the requested extraction.

No series were saved, no proxy was selected, and no cluster job ran. No task spec,
other task, decision file or goal.yaml was edited. No PR was merged.
The reusable CLI and offline tests remain unimplemented. This is blocked exit (B),
not a completed delivery. The native goal must not be marked complete.

## Acceptance

- [x] Inventory exists and lists at least one library, with yes/no answers in
  `Relevant to this replication`. Evidence: `db.list_libraries()` returned 229;
  all 229 `list_tables` calls succeeded. `docs/data/wrds_inventory.md` contains
  229 library rows and eight relevance rows.
- [ ] `--extract` prints `OK` for each written file, and Treasury coverage is
  verified or lack of subscription is documented. The Treasury alternative is
  satisfied by `docs/data/cards/wrds.md`: both Treasury queries returned
  `permission denied for schema crsp_a_treasuries`. The extractor does not yet
  exist, so this combined requirement is not satisfied. No output files were written.
- [x] `git status --porcelain` lists no data file. Only this outcome, the source
  card and the inventory belong to this change. No CSV, parquet or other series
  artifact was created in the worktree or staged.
- [ ] `uv run pytest tests/test_wrds_extract.py` passes. The local quiet invocation
  exited 4: `ERROR: file or directory not found: tests/test_wrds_extract.py`;
  `no tests ran in 0.00s`. Tests were not created because implementation stopped
  at the access/scope gate.

## Local verification

Both requested CLI invocations exited 1 with
`No module named rebal.fetch.wrds_extract`. The test invocation exited 4, as above.
The delivery Verify block does not pass. No GitHub Actions were read or used.

Live subscription evidence:

- `crsp.tfz_dly_ft` and `crsp.tfz_idx`: denied for `crsp_a_treasuries`.
- `crsp.fund_hdr`, `fund_hdr_hist`, `fund_names`, `daily_returns`, `daily_nav_ret`:
  denied for `crsp_q_mutualfunds`.
- Sample headers: VBMFX = 31239, VBTLX = 31244. Both return series have 755
  nonmissing observations, 2004-01-02 through 2006-12-29.
- Actual reads succeeded for `crsp.dsp500`, `crsp.dsi`, `ff.factors_daily`,
  `ftsesamp.ctr_monthly_us` and the Datastream sample contract tables.
- Datastream has no ES/TY/ZN contracts in the sample. OptionMetrics futures
  tables deny access to `optionm_europe`.

Base revision inspected after rebase: `f2598606294245c7428451abb0a2e4384d16a936`.
The only changes after that revision are these three documentation files.

## Decision request

Should TASK-010 require full CRSP Mutual Funds access, or proceed with the 2004–2006 sample?

1. Enable full CRSP Mutual Funds access, then resume the task. This preserves the
   intended long-sample proxy comparison. It requires an external subscription change.
2. Approve a limited sample extraction and document full-history VBMFX/VBTLX as
   unavailable. This can proceed with existing access, but cannot support the full
   1997–2023 comparison. TASK-011 must account for the short coverage and use its
   already planned alternatives where needed.

### Recommendation

Approve option 2 if full access cannot be enabled. Keep the limited sample clearly
identified and leave the final proxy choice to TASK-011/DEC-001. Do not silently
shorten the replication period or present the sample as full subscription coverage.

Proposed follow-up after the decision: implement the inventory/extraction CLI for
approved sources, add offline parsing tests, run every Verify command, and update
this outcome before marking the PR ready. No new task or decision file was created.
