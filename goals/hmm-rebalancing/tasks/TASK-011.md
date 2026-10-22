---
id: TASK-011
title: Compare candidate proxies for ES and TY futures returns
milestone: M-1
state: approved
depends_on: [TASK-003, TASK-006, TASK-009, TASK-010]
delivery: pr
kind: discovery
route: {platform: codex, model: gpt-6-astra, effort: high}
---

## Why

Serves SC-1 and SC-2, and supplies the evidence for DEC-001. The paper's main input is Bloomberg's continuous ES and TY futures excess returns (D1, D2; paper-notes §3.1). We have no Bloomberg, so this task measures how well each candidate proxy tracks real futures returns. The signals are cumulative sums of Ret = R^SP − R^TY, so small daily errors can add up.

## Scope

No cluster jobs in this task. Runs on the MacBook. It reads the outputs of TASK-003, TASK-006, TASK-009 and TASK-010; read their cards in `docs/data/cards/`.

**Code.** `src/rebal/proxies.py`. It holds one pure function per candidate. Each function returns a daily simple excess-return series, indexed by date. TASK-012 reuses these functions, so keep each one documented and tested.

**ES candidates:**
- E1: CRSP SPY `ret` minus `rf`.
- E2: Yahoo `^SP500TR` return minus `rf`.
- E3: Yahoo `ES=F` close-to-close return, with roll days repaired:
  - Detect roll days from the quarterly expiry calendar (the third Friday of March, June, September and December) and from price jumps against E2.
  - Replace the return on a roll day with E2.
  - Report the count of repaired days.
- E4: WRDS futures, if TASK-010 found them. Roll at the end of the month before expiry (paper-notes §3.1).

**TY candidates:**
- T1: the GSW 10-year zero-coupon bond return, from `SVENY10` (log price = −n·y), minus `rf`.
- T2: the GSW 10-year par-bond return, from `SVENPY10` (a coupon bond priced off the fitted curve), minus `rf`.
- T3: a GSW zero-coupon bond with maturity of about 6.5 years, matched to the duration of the TY cheapest-to-deliver bond, minus `rf`. Report the maturity you used.
- T4: the CRSP 10-year fixed-term Treasury index (WRDS), minus `rf`.
- T5: IEF total return minus `rf` (from 2002).
- T6: Yahoo `ZN=F` with roll days repaired, as for E3.
- T7: WRDS futures, if found.

For `rf`, use the French daily RF from TASK-005 if it is merged; otherwise use FRED DTB3 converted to a daily return. Futures returns are already excess returns, so E3, E4, T6 and T7 do not subtract `rf`.

**Benchmark.** Use the best futures series available: E4/T7 if they exist; otherwise E3/T6 on days that are not roll days, from 2000-09 to 2023-03-17.

**Metrics.** For each candidate, and for each pair `Ret = ES − TY`, report:
- the coverage start;
- correlation with the benchmark;
- beta on the benchmark;
- annualized tracking error;
- the mean difference;
- the lead and lag correlation (proxy at t against benchmark at t±1), which detects mismatched close times;
- the correlation of 0.24 × month-to-date cumulative Ret with the benchmark's. This is a cheap stand-in for the Calendar signal (paper-notes §3.2).

**Report.** `docs/data/proxy_comparison.md`:
- the metrics tables;
- a note on close times (equities 16:00 ET, ES 16:15, Treasury futures settlement 15:00);
- a final section, "Recommendation for DEC-001", that names one ES and one TY series for the main panel, plus one alternative pair for a robustness check. It must cover the sample from 1997-09-10. Name any candidate that covers it only partly, and how it could be spliced.

**Tests.** `tests/test_proxies.py` uses small synthetic inputs to check:
- the zero-coupon return formula, against a hand computation;
- roll-day repair, with a planted jump that is removed;
- that the excess-return subtraction is applied only to cash proxies.

Out of scope: building the panel (TASK-012), and changing data from earlier tasks.

## Acceptance

- `uv run python3 -m rebal.proxies --report docs/data/proxy_comparison.md` regenerates the report.
- The report shows a metrics table for every available candidate, and the section "Recommendation for DEC-001".
- `uv run pytest tests/test_proxies.py` passes.
- The outcome repeats the recommended ES/TY pair, with its correlation and tracking error against the benchmark.

## Verify

```sh
uv run python3 -m rebal.proxies --report docs/data/proxy_comparison.md
sed -n '/Recommendation for DEC-001/,$p' docs/data/proxy_comparison.md
uv run pytest -q tests/test_proxies.py
```
