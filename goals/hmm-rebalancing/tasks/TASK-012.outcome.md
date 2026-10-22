# TASK-012 outcome

## Acceptance

- [x] `uv run python3 -m rebal.panel --build && uv run python3 -m rebal.panel --check`
  exited **0** and ended with **`PANEL OK`**. Both stored parquets were reopened
  and validated. Each has 8,275 rows, 1993-02-01–2026-07-31, with the contract's
  35 columns and exact dtypes. Both core returns are complete.
- [x] The checker printed **1997-09-10 to 2023-03-17**, with **0.00% study NaN**,
  for `r_es`, `r_ty`, `rf`, `vix`, `epu`, `ads`, `sentiment`, `mkt_rf`, `smb`,
  `hml`, `rmw`, `cma`, `mom`, `q_mkt`, `q_me`, `q_ia`, `q_roe`, and `q_eg`.
  This holds in both panels. Example coverage lines appear below.
- [x] Both checker outputs printed **6,318 study rows**. This is **92 above**
  the paper's regression N=6,226 and **155 below** its approximate total of
  6,473 days, from paper-notes §5.3. The French study grid has 6,422 sessions.
  SPY covers every one; 52 missing GSW quote sessions remove 104 holding
  returns, including each following session. Thus `6422 - 104 = 6318`.
  The four September 2001 closures are already absent from French. No rows
  were filled or trimmed to match the paper. Earlier history supplies 1,122
  initialization rows; later signal and regression tasks select their samples.
- [x] `grep -cE '^\| D[0-9]+ ' docs/data/sources.md` printed **28**.
  `grep -cE '\| planned \|' docs/data/sources.md` printed **0**.
  A separate assertion checked all 28 rows: ten columns, accepted status syntax,
  and existing source-card links. The zero-match grep returns 1 by definition;
  the exact multi-command Verify block still exits 0 after pytest.
- [x] `uv run pytest -q tests/test_panel.py` passed: **19 passed**
  in the exact Verify run. Synthetic tests cover DTB3 percent/day-count units,
  the five-session fill limit, unfilled returns, all four September closures,
  source mapping, flat-curve bond pricing, HPW/OFR selection, contract failures,
  and reopening both outputs. The complete Verify block exited **0**.

## Summary

Implemented `rebal.panel --build` and `--check`. Main E1/T3 and robustness E2/T2
call the accepted `rebal.proxies` functions under DEC-001. Both files use the
main pair's common calendar. Only their two core return columns differ.
The builder preserves initialization history, applies the specified units and
five-equity-session control-fill cap, and never fills returns or factors.

Integrated validated public Yahoo VBMFX returns under DEC-002, without a splice.
The 2004–2006 WRDS sample does not replace longer public history. Integrated
the exact MSCI 899901 USD NETR series rather than a later-starting ETF.
Selected HPW `Noise_bp` for liquidity because it spans the study; OFR Funding
is a documented, tested fallback. The contract and methods now agree that
liquidity retains the selected source's published units: HPW `Noise_bp` in
basis points with full-study history, otherwise OFR `Funding` in index points.
The contract cites the methods and `panel.metadata.json` for the selected source.
These sources do not have identical units. Input hashes, choices and output coverage
are recorded in external `panel.metadata.json`.

Added `docs/methods/panel.md` with every transform, scale, choice and limitation.
Finalized all D1–D28 source rows with sources, URLs, actual storage, coverage,
availability and source-card links. Added cards for the derived calendar,
paper dollar constants and qualitative evidence. No raw or processed licensed
data entered git. No downloads or cluster jobs ran.

Limits: these remain futures proxies with cash-market calendars and differing
close times. MOVE has no early study history. MSCI starts in December 2000;
Russell ETFs start in May 2000. ARA ends in 2019. Published controls can carry
five sessions past their last source date, but leading gaps remain missing.
French and q5 current vintages can revise history. The contract has one SMB
column, supplied by the French three-factor file; it does not carry a separate
five-factor SMB. HPW's basis-point liquidity unit is documented explicitly.
The public FEARS subset does not supply the private extension; ANcerno and
qualitative numerical replication remain unavailable. ICI coverage gaps remain
documented. None of these optional-source gaps shortens the main study.

Verified implementation and units-documentation revision:
`fff7d21cd1c5590c83afc3f6b6691cf3e3d4672b`, after a conflict-free rebase onto
`origin/main` at `d1e20118fc7fbc3e09244ad7050081296b4d585b`.
The exact Verify block and `git diff --check origin/main...HEAD` also passed
on the final committed revision before push; the PR body records its SHA.
This resume changes only the liquidity contract row, its related methods text,
and this outcome. Code behavior and all other contract rows stay unchanged.
Branch:
`goal/hmm-rebalancing/task-012`. PR:
https://github.com/jesusvillota/replicate/pull/27, into `main`, with marker
`Goal-Task: hmm-rebalancing/TASK-012` and label `goal:hmm-rebalancing`.
Local verification determines delivery. GitHub Actions were not read or used.
No merge was performed. No task spec, other outcome, decision or goal definition
was edited. No material decision remains open.

Additional checks in this resume:
`uv run --with ruff ruff check src/rebal/panel.py tests/test_panel.py` passed;
`uv run --with ruff ruff format --check src/rebal/panel.py tests/test_panel.py`
reported both files formatted. All 19 metadata source hashes match the current
input files; metadata selects `HPW Noise_bp (basis points)`. All 28 source-map
IDs, ten-column rows, statuses and source-card links passed fresh assertions.
GitHub returned no PR review threads or comments to resolve.

Earlier implementation-session evidence, retained for context:
`rebal.panel --help` exited 0. The full local suite, `uv run pytest -q`, exited **0**:
**314 passed, 4 warnings in 192.05s**. The warnings are Python escape-sequence
warnings inside the installed WRDS dependency.
Proposed follow-ups: existing analysis tasks consume the panel and its documented
coverage. No new task or decision is required.

## Verify evidence

The exact task Verify block reran locally on 2026-10-23 and exited **0**.
It also passed on the final committed revision, as did
`git diff --check origin/main...HEAD`:

```sh
uv run python3 -m rebal.panel --build && uv run python3 -m rebal.panel --check
grep -cE '^\| D[0-9]+ ' docs/data/sources.md; grep -cE '\| planned \|' docs/data/sources.md
uv run pytest -q tests/test_panel.py
```

Selected main-panel coverage lines (the alternative reports the same study coverage):

```text
r_es: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
r_ty: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
rf: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
vix: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
epu: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
ads: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
sentiment: 1993-02-01 to 2026-07-31; NaN=0.00%; study=1997-09-10 to 2023-03-17; NaN=0.00%
q_eg: 1993-02-01 to 2025-12-31; NaN=1.75%; study=1997-09-10 to 2023-03-17; NaN=0.00%
```

Exact Verify output tail:

```text
daily_panel_alt: 1997-09-10 to 2023-03-17 rows=6318
Paper: regression N=6226 (difference +92); about 6473 total days (difference
-155)
PANEL OK
28
0
...................                                                      [100%]
19 passed
```
