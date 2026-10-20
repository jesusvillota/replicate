---
id: TASK-019
title: 'Plan: decompose M-3'
milestone: M-3
state: approved
depends_on: [TASK-018]
delivery: pr
kind: plan
---

## Why

Serves SC-6. This task plans M-3, the extension exhibits and the final report, using the evidence from M-1 and M-2.

## Scope

This is a planning task for the orchestrator. Use the `goal-setup` skill's replanning rules. Read first:
- `docs/results/core.md`;
- `docs/data/sources.md`;
- `docs/data/wrds_inventory.md`;
- the outcomes of TASK-012 and TASK-018.

Then add one task per item below. Each task needs a full spec that follows the README conventions: work tasks on demo data first, then one run task.

1. **Table 4, the long sample:** French `r_mkt_french` minus the GSW 10-year return, 1961–2023, split at 1997-09-10. Settle §5.13: the method that turns yields into returns, and the pre-1971 10-year yield.
2. **Table 5, equity segments:** R1K/R2K as a 90/10 portfolio, and R1K Value/Growth as the falsification test (§5.14). Use `rebal.signals.build` on segment returns.
3. **Table D.4:** `r_sp500tr` minus `r_agg`.
4. **Table D.9, alternative controls:** ra^BEX, unc^BEX, ARA and FEARS. Skip any that is "not available", and say so.
5. **Table D.14, international equity:** MSCI ACWI ex US minus `rf_3m`, with the signals lagged one more day.
6. **Figure 1, pension allocations:** from the PPD data (TASK-008).
7. **Figure 5, trading-data correlations:**
   - CFTC hedgers vs speculators (legacy COT), and asset managers vs leveraged funds (TFF, LTPos);
   - ICI flows;
   - ANcerno is not available unless the WRDS inventory found it.
   Settle §5.11 and §5.12.
8. **Final report:** `docs/results/replication_report.md`. It covers every exhibit: whether it replicates, and the proxy and ambiguity notes. It links to `docs/data/sources.md`.
9. **Optional; the owner chooses, through a decision node:**
   - extend the sample to the latest data;
   - the 3:30 PM check with tape-kit SpiderRock SPY 1-minute bars. These exist from 2018, on the CEMFI PC only, so this needs a `--manual` data-copy task.
   - Also add any follow-ups proposed in the TASK-018 outcome.

Name every outside blocker as a `--manual` task.

## Acceptance

- `goal check --goal hmm-rebalancing --json` reports no errors after the replanning.
- `goal graph --goal hmm-rebalancing` shows the new M-3 tasks, each depending only on merged work.
- The PR body lists the new task IDs and titles.

## Verify

```sh
goal check --goal hmm-rebalancing --json
goal graph --goal hmm-rebalancing
```
