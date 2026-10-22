# TASK-011 outcome

## Acceptance

1. [x] `uv run python3 -m rebal.proxies --report docs/data/proxy_comparison.md`
   regenerates the report. The exact post-rebase Verify block exited **0** and
   printed `OK docs/data/proxy_comparison.md candidates=8 pairs=15`. Regeneration
   left the committed report unchanged.
2. [x] The report has metrics for **all eight available candidates and all 15
   ES/TY pairs**, plus `## Recommendation for DEC-001`. A separate assertion on
   the real generated report checked every candidate and pair row, the heading,
   and the recommended pair's correlation and tracking error. It exited 0.
   E4, T4 and T7 are explicitly unavailable under TASK-010's inventory.
3. [x] `uv run pytest -q tests/test_proxies.py` passed: **19 passed in 0.65s**.
   The tests cover hand-computed zero and par holding returns, calendar-day
   carry, curve interpolation, planted roll jumps, inception and missing-data
   limits, cash-only RF subtraction, metric formulas, month resets, planted
   demo fit and a zero effect, report rows, French RF and FRED fallback units.
4. [x] Recommended main pair: **E1/T3 — CRSP SPY total return minus French daily
   RF / GSW 6.5-year zero-coupon bond return minus French daily RF**.
   Against the clean Yahoo futures benchmark, the pair has **correlation
   0.9917** and **annualized tracking error 2.8069%**, on **4,839 paired days**,
   2000-09-22–2023-03-08. The common-calendar ranking gives the same values.
   Separately, E1 has correlation 0.9928 and tracking error 2.2947%; T3 has
   correlation 0.9617 and tracking error 1.6425%. Both main legs cover the study
   endpoints, 1997-09-10 and 2023-03-17. Missing intervening sessions remain
   explicit. The robustness pair is **E2/T2**, with pair correlation **0.9810**
   and annualized tracking error **4.5655%**.

## Summary

Added `src/rebal/proxies.py`, `tests/test_proxies.py`, the generated comparison
report, and `docs/methods/proxies.md`. Each available candidate has a pure,
documented function for TASK-012. The CLI aligns source inputs, constructs
cash excess returns and repaired futures returns, and compares every candidate
and pair. DuckDB reads source files and aggregates metrics. NumPy prices the
GSW curve. The report includes source hashes, coverage, beta, daily mean error,
lead/lag correlations, and the month-to-date Calendar diagnostic.

Plan completed: inspect dependency outcomes and cards; implement reusable
returns and roll repair; compare candidates on clean benchmark sessions; test
synthetic pricing and diagnostics; regenerate the real report; publish this
outcome and the PR. No upstream data was changed. No cluster jobs ran.

Bond returns include calendar-day carry and remaining maturity. The par bond
holds yesterday's coupon fixed and prices its semiannual cashflows using both
GSW Svensson curves. T3 uses a fixed 6.5-year maturity as an approximate duration
match. The roll screen uses a conservative quarterly window plus fixed residual
jump cutoffs. It repaired 715 ES and 717 TY returns in the study. Another 70 TY
returns lack repair references and stay missing. Every flagged date is excluded
from the benchmark. Its actual last clean session is March 8, 2023.

Limits and deviations: WRDS supplies no usable ES/TY futures or fixed-term
Treasury index, as documented by TASK-010. Yahoo supplies the benchmark only
from September 2000. Its own candidate comparisons are mechanical identities.
The Calendar check uses identical common clean sessions within each month;
it is an incomplete-month diagnostic. Close-time differences and approximate
Treasury duration remain limits. Roll dates are heuristic, not verified
contract switches. No unavailable history was invented, and no splice was made.
These choices and the possible later splice are documented in the report.

No new decision blocks this comparison. The recommendation supplies evidence
for the existing DEC-001; no final panel choice or decision was recorded.
Proposed follow-ups stay within existing work: DEC-001 selects the pair, and
TASK-012 integrates it under the daily-panel contract. Duration and roll-rule
sensitivity remain documented checks for subsequent analysis.

Verified implementation revision: `653d1cc6aa5ed3944e59effdfa87999bfa99a0e3`, after a conflict-free rebase
onto `origin/main`. This outcome is a documentation-only follow-up. Ruff lint
and format checks passed. The demo CLI and `--help` passed. `git diff --check`
passed. The real report row assertions passed. GitHub Actions were not read
or used. No task spec, other task, decision, goal.yaml, or source map was edited.

PR: https://github.com/jesusvillota/replicate/pull/26, base `main`, branch
`goal/hmm-rebalancing/task-011`, label `goal:hmm-rebalancing`. The PR was opened
as a draft after the first implementation commit. It is marked ready after
this outcome is committed and pushed. Never merged.

## Verify

The exact Verify block below exited **0** after rebasing:

```sh
uv run python3 -m rebal.proxies --report docs/data/proxy_comparison.md
sed -n '/Recommendation for DEC-001/,$p' docs/data/proxy_comparison.md
uv run pytest -q tests/test_proxies.py
```

Captured output, including the test tail:

```text
[00:49:33] Input: stored source-card files                        proxies.py:607
           Report:                                                proxies.py:610
           /Users/jesusvillotamiranda/orca/workspaces/replicate/g
           oal-hmm-rebalancing-task-011/docs/data/proxy_compariso
           n.md
OK docs/data/proxy_comparison.md candidates=8 pairs=15
## Recommendation for DEC-001

Recommend **E1/T3: CRSP SPY total return − RF / GSW 6.5-year zero − RF** for the main panel.
Both cover 1997-09-10–2023-03-17. Pair correlation with the clean Yahoo futures benchmark is **0.9917**; annualized tracking error is **2.8069%** (N=4839).
On the common comparison calendar: correlation **0.9917**, TE **2.8069%**.
This pair has the lowest common-calendar tracking error among the full-sample candidates. Coverage here means both endpoints and available intervening sessions, with missing bond holidays left explicit.
Use **E2/T2: Yahoo ^SP500TR return − RF / GSW 10-year par bond − RF** as a robustness pair with different constructions for both legs.
Its correlation is **0.9810**; annualized TE is **4.5655%**.
E3 starts after 2000-09-18; T6 starts after 2000-09-21; T5 starts in July 2002. They cover the study only partly.
For a later futures robustness splice, use E1/T3 before the first common usable E3/T6 return, then repaired E3/T6; use T3 before T5 for an IEF check.
Splice returns, not price levels, on a documented common session. Test the break and retain source flags. No splice is built here.
TASK-012 must retain missing sessions and apply the daily-panel contract. This is evidence for DEC-001, not a recorded decision.
...................                                                      [100%]
19 passed in 0.65s
```
