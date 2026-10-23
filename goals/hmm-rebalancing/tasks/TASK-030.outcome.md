# TASK-030 outcome

Status: Delivered. All five acceptance requirements and local Verify commands pass.

## Summary

Ran all merged analysis code on the real MacBook panel. Committed every main
exhibit, canonical comparison export, required robustness variant, and the
final generated replication report. No analysis code or method changed.
No data was fetched. No cluster job ran. TASK-032 was not rerun.

Verified analysis revision: `28daff83285f5f150a85d444c0b2e8a8cae92a58`,
`origin/main` at the initial base sync. The branch rebased without conflicts
and remains `goal/hmm-rebalancing/task-030`. Artifact/report commit: `d82650d`.
The outcome commit adds documentation only. No task specification, other task,
decision, `goal.yaml`, contract, method, source map or input data changed.

Delivery PR: https://github.com/jesusvillota/replicate/pull/44, into `main`.
Local verification determines delivery. GitHub Actions were not read or used.

## Acceptance

1. [x] `uv run python3 -m rebal.exhibits --all` exited **0**, printed
   **11 exhibit modules**, and ended with `exit=0`. An independent listing
   verified **38/38 contract IDs**: 26 table CSVs and 12 figure CSV/PDF pairs.
   This includes Tables 4, 5, D4, D9, D14 and Figures 1 and 5.
   D9 exports columns 1, 2 and 4; private FEARS column 3 is omitted.
   Figure 5 exports five available investor groups; ANcerno is omitted.
2. [x] `docs/results/replication_report.md` has all **38 contract rows**,
   once each, in contract order. Its summary gives **92.5% sign agreement
   (196/212)** and **83.1% significance agreement (123/148)**.
   The filled **Latest sample (footnote 32)** section matches all **120 rows**
   of TASK-032's saved comparison. All four latest exports are unchanged
   from the merged base. Independent CSV checks reproduced every report
   headline, coverage count and status. Added 23 cited gap annotations.
3. [x] Both `uv run python3 -m rebal.compare` and the explicit core-report
   command exited **0**, without moving inputs or changing exports manually.
   Their contents agree. They join **388/399 numeric targets**, above
   TASK-018's 252/399, and **394/399 export keys**. Costs, Tables 6A–C and
   the available figure targets now join through their canonical exports.
   Five targets require FEARS/ANcerno. Six retain documented paper ambiguities:
   two Figure 6 axis values, three Figure D5 values and one random-cost value.
   These blanks are not numeric matches. The temporary default report copy
   was removed after equality was checked; `docs/results/core.md` is retained.
4. [x] The tables below quote both Table 1 signals with t statistics;
   both signals for all three Table 4 samples and both Table 5 pairs;
   the headline cost in bps and dollars; and the gross strategy Sharpe.
   All numbers were read from the saved main CSVs and paper target CSV.
5. [x] `uv run pytest -q` exited **0** on the merged code: **393 passed,
   4 warnings in 981.31s (0:16:21)**. The warnings are invalid escape
   sequences in the installed `wrds` dependency. No test failed.

## Headline comparisons

The t statistic measures an estimate relative to its standard error.
Paper t statistics below are **calculated from printed coefficient / SE**;
they are not unrounded t statistics supplied by the authors.
Our t statistics use the saved HC1 standard errors. HC1 adjusts for unequal
return variances. N is the number of daily prediction/outcome pairs.

### Table 1, column (1)

| Column / sample | Signal | Paper coefficient (t) | Our coefficient (t) | Our N / paper N | Actual outcome dates |
|---|---|---:|---:|---:|---|
| 1, core | Threshold | -0.4144 (-3.609756) | -0.464414445 (-4.012118) | 6317 / 6226 | 1997-09-11–2023-03-17 |
| 1, core | Cal × week4 | -0.3029 (-3.748762) | -0.260255817 (-3.418693) | 6317 / 6226 | 1997-09-11–2023-03-17 |

Both main effects are negative and significant at 5%, as in the paper.
The panel uses SPY-minus-cash and a GSW 6.5-year zero-coupon return proxy,
rather than Bloomberg ES/TY futures. See `docs/data/proxy_comparison.md`.

### Table 4: three samples

| Column / sample | Signal | Paper coefficient (t) | Our coefficient (t) | Our N / paper N | Actual outcome dates |
|---|---|---:|---:|---:|---|
| 1, full | Threshold | -0.1809 (-2.917742) | -0.173107406 (-2.822127) | 14796 / 15291 | 1963-01-11–2023-03-17 |
| 1, full | Cal × week4 | -0.1536 (-3.261146) | -0.151346082 (-3.291651) | 14796 / 15291 | 1963-01-11–2023-03-17 |
| 2, early | Threshold | -0.0157 (-0.272569) | -0.018537183 (-0.312090) | 8478 / 8870 | 1963-01-11–1997-09-09 |
| 2, early | Cal × week4 | -0.0284 (-0.476510) | -0.106168001 (-1.734011) | 8478 / 8870 | 1963-01-11–1997-09-09 |
| 3, late | Threshold | -0.3685 (-3.340888) | -0.363703871 (-3.318048) | 6317 / 6421 | 1997-09-11–2023-03-17 |
| 3, late | Cal × week4 | -0.2569 (-3.834328) | -0.200242838 (-2.991813) | 6317 / 6421 | 1997-09-11–2023-03-17 |

The Threshold pattern agrees: the early effect is absent and the late effect
is stronger. Calendar differs more across subsamples. Although column 1 is
nominally 1961 onward, bond-history limits and momentum initialization move
our first outcome to 1963. `docs/methods/long_sample.md` records the early
DGS10 approximation, source seam and retained calendar. These differences
limit comparability. The remaining coefficient-gap cause is unknown.

### Table 5: equity segments

| Column / sample | Signal | Paper coefficient (t) | Our coefficient (t) | Our N / paper N | Actual outcome dates |
|---|---|---:|---:|---:|---|
| 1, R1K/R2K | Threshold | -0.2054 (-3.440536) | 0.000058183 (0.001481) | 4109 / 4175 | 2006-08-18–2023-03-17 |
| 1, R1K/R2K | Cal × week4 | -0.1174 (-1.718887) | -0.074392361 (-0.434503) | 4109 / 4175 | 2006-08-18–2023-03-17 |
| 2, Value/Growth | Threshold | -0.0339 (-0.709205) | 0.010958554 (0.329964) | 4109 / 4175 | 2006-08-18–2023-03-17 |
| 2, Value/Growth | Cal × week4 | -0.0678 (-1.036697) | -0.151664973 (-0.858883) | 4109 / 4175 | 2006-08-18–2023-03-17 |

None of our four effects is significant at 5%. The paper's size-segment
results are not reproduced. We use ETF total-return proxies and 90/10
weights. The shared calendar and inside-window pairing reduce N.
See `docs/methods/segments.md`. The exact cause of the gap is unknown.

### Costs and strategy

| Quantity | Paper | Main real run |
|---|---:|---:|
| Headline annual cost | 8 bps | 1.2215145687131197 bps |
| Annual cost on $20 trillion | $16,000,000,000 | $2,443,029,137.4262395 |
| Gross strategy Sharpe ratio | 1.11 | 0.7340831337181071 |
| Gross strategy mean return | 10.20%/year | 6.449675588374807%/year |
| Gross strategy volatility | 9.17%/year | 8.786028846225372%/year |

A basis point (bps) is 0.01 percentage point. Sharpe divides annual return
by annual volatility under the strategy's documented convention.
Sources: `output/tables/costs.csv`, `table_6a.csv` and `docs/results/targets.csv`.

TASK-022 corrected the squared-trade-share cost formula. DEC-005 excludes
delta=0 from summary means while retaining all 26 raw estimates. The main
Threshold mean is -5.554162 bps and its range is -18.570229 to 6.568186 bps,
versus the paper's 15 bps and 6–27 bps. These do not reproduce the paper's
costs. The 10,000 random monthly schedules, seed 16, give a raw mean cost
of 0.07326281236780777 bps. The canonical random-cost targets remain blank
because the paper's text and chart use conflicting signs.
No units or parameters were adjusted to match the paper.

## Robustness runs

Used the same existing APIs as TASK-018. Inline run orchestration selected
outputs without changing any shared panel, signal, code or main exhibit.
The literal run uses `signals_literal.parquet`; the alternative run builds
clean signals on the full `daily_panel_alt.parquet` history.
Run metadata records the analysis revision, input hashes, timing and selection.

| Variant / Table 1 column (1) | Threshold coefficient (t) | Cal × week4 coefficient (t) |
|---|---:|---:|
| Main | -0.464414 (-4.012118) | -0.260256 (-3.418693) |
| Literal timing | -0.269997 (-2.729659) | -0.260521 (-3.366775) |
| Alternative proxy | -0.377347 (-3.389297) | -0.223696 (-3.126650) |

Both variants retain negative signs and 5% significance. Literal Table 1
and Figure 2 are saved under `robustness/literal/`. Alternative Tables 1
and 3 and costs are saved under `robustness/proxy_alt/`. The corrected
alternative cost is **1.3562740905168837 bps**, or **$2,712,548,181.033767**
on $20 trillion. It also falls below the paper's 8 bps and $16 billion.
Both cost runs used 10,000 schedules and seed 16.

## Latest sample (footnote 32)

This paragraph uses only TASK-032's `docs/results/latest_sample.md`.
That run ends on **2026-07-31**, with **7,152** core observations, versus
6,317 at the paper endpoint. Threshold moves from -0.46441444537986687
(t=-4.012117777680489) to -0.4101349210644659 (t=-3.7502634690368497).
Cal × week4 moves from -0.26025581705921746 (t=-3.418692803568286) to
-0.2362462490035583 (t=-3.2273241198579243). Both remain negative and
significant, but weaken. This does not support footnote 32's stronger-results
claim. Table 3 retains all eight signs and 5% decisions; bond Calendar
remains insignificant. The cause of weaker estimates is unknown.
No latest-sample output was rewritten by this task.

## Report interpretation and remaining gaps

The generated report assesses seven exhibits as `replicates`, 24 as `partly`
and Figure D2 as `fails`, using the documented 25% size tolerance.
Four exhibits have no numeric paper targets: D2, D5, D13 and Figure C1.
Their `not run` status means unassessed comparison; their real outputs exist.
Figures 6 and D5 also say `not run` because their paper conventions remain
unresolved. Their plots and raw data exist. Figure 5's headline selects
unavailable ANcerno by the fixed key order; ten available correlations still
enter its row and the rates. No entire exhibit is omitted for unavailable data.

Figure 1's actual min/max/typical target are about 0.412023/0.619532/0.483315,
versus the paper's approximate 0.63/0.68/0.65. The default covers fiscal years
2003–2022. Source coverage changes by year: 172–228 actual contributors and
136–234 target contributors among 253 source rows. `docs/methods/pension.md`
records this coverage and the asset weighting. These are plausible sample or
source-vintage limits; the exact cause of the large gap remains unknown.
Figure 5's ten available signs agree, with 867 COT, 125 LTPos and 194 ICI
pairs per signal. Sparse ICI blocks and the lag/scaling methods limit comparison.
D14 uses 5,503 observations from 2001, versus the paper's 6,097.

An independent read-only audit checked all exhibit rows directly against CSVs.
It caught a Figure 1 year typo in the new gap note; the note was corrected
to 2003–2022 and the report was regenerated with its CLI.
All 13 one-page PDFs (12 main plus literal Figure 2) were rendered with
Poppler and visually inspected. Labels, axes, legends and bands are readable.
The report was never edited by hand. Generated CSV line endings and the
report generator's terminal blank line were retained.

One unrelated documentation error was reported and left outside this task:
https://github.com/jesusvillota/replicate/issues/43. The comparison methods
still describe four current contract IDs as absent. The actual contract
controls this run. No analysis failure, missing access, missing data within
the accepted scope, or new material decision blocks delivery.

## Verify evidence

The requested commands ran in order on the merged analysis code:

```sh
uv run python3 -m rebal.panel --check | tail -1
uv run python3 -m rebal.signals --build --timing clean && uv run python3 -m rebal.signals --build --timing literal
uv run python3 -m rebal.exhibits --all; echo "exit=$?"
uv run python3 -m rebal.compare --out docs/results/core.md && sed -n '1,20p' docs/results/core.md
uv run python3 -m rebal.report --out docs/results/replication_report.md && sed -n '1,40p' docs/results/replication_report.md
uv run pytest -q
```

Panel validation printed `PANEL OK`. Both signal builds wrote 8,275 rows
and 63 columns. The exhibit runner printed 11 modules and `exit=0`.
Comparison/report excerpts were printed in this session and match the
coverage and rates above. The report command ran again after the note typo
was corrected; no analysis code or output estimate changed.

The final test tail was:

```text
........................................................................ [ 73%]
........................................................................ [ 91%]
.................................                                        [100%]
=============================== warnings summary ===============================
[4 SyntaxWarning entries in installed wrds/sql.py]
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
393 passed, 4 warnings in 981.31s (0:16:21)
```

Every command in the requested Verify sequence exited 0. The no-argument
comparison additionally passed and produced the same report contents.
The report regeneration after the gap-note correction also exited 0.
`git -c core.whitespace=cr-at-eol,-blank-at-eof diff --check origin/main...HEAD`
passes, allowing the existing CSV line endings and generated final blank line.
An additional independent check matched all 12 required signal coefficient/t
comparisons in this outcome against the saved CSVs.

The PR has `Goal-Task: hmm-rebalancing/TASK-030` and label
`goal:hmm-rebalancing`. It is ready for review into `main`; never merged here.
No acceptance requirement remains open. Issue #43 is a reporting-document
follow-up only; no new task or decision was created.
