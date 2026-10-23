# Final replication report

Run `uv run python3 -m rebal.report --out docs/results/replication_report.md`.
The generator reads existing exports. It writes only its requested Markdown file.
It uses the standard library and the existing `rebal.compare` API. It does not
change estimates, export layouts, targets, source cards or shared modules.

For fixtures, first run `uv run python3 -m rebal.exhibits --all --demo`, then
`uv run python3 -m rebal.report --demo --out /tmp/replication_report_demo.md`.
Demo mode reads only `output/demo/` and labels all findings as synthetic.
It does not require a real panel. With no exports it still lists every exhibit,
with `not run` or an unavailable-source reason. It never creates fixture exports.

## Comparison and status rules

The IDs and their order come from [the contract](../contracts/exhibits.md).
There is one exhibit-table row per ID. Costs and the strategy are already
represented by `costs` and `table_6a`–`table_6c`; no duplicate aliases are added.
The report joins [paper targets](../results/targets.csv) through `rebal.compare`.
Its numeric coverage and sign/significance rates use exactly that API's rows.
Joined export keys include blank canonical values. Numeric coverage excludes them.
Rates use only eligible, nonmissing comparisons, not all paper targets.

`--size-tolerance` defaults to **0.25**, or 25% of the absolute paper value.
`--absolute-tolerance` defaults to **0.0001** in each target's original units.
A size agrees if `abs(ours - paper) <= max(absolute, relative * abs(paper))`.
The absolute floor handles zero and small rounded targets. Both options must
be finite and nonnegative. These are descriptive report thresholds, not a
statistical test or a tolerance stated by the authors. No unit conversion occurs.
Approximate chart readings keep the `~` marker and use the same tolerance.

Primary targets are `coef` and `value`, plus `t` when that term has no `coef`
target. Standard errors, sample counts and adjusted R-squared support the
comparison but do not decide size agreement. Coefficient significance must be
comparable to certify replication. Value-only summaries have no significance
requirement. Significance uses `rebal.compare`: both absolute t-statistics
are at least 1.96, or both are below it; coef/se is its fallback.

- `replicates`: all numeric targets are present; all primary signs, sizes and
  applicable significance decisions agree.
- `partly`: at least one number is present, but coverage is incomplete, signs
  are mixed, sizes differ, significance differs, or a coefficient test is missing.
- `fails`: coverage is complete and all eligible primary signs disagree.
- `not available`: all targets require inaccessible FEARS or ANcerno data.
- `not run`: no comparable numbers exist, or no numeric paper targets exist.

An exhibit with both accessible and inaccessible columns is `partly` when
accessible numbers exist. Its note retains unavailable-source reasons. It is
`not run` when accessible columns have no numbers. Missing exports, blank
values and unresolved paper conventions never establish failure. The notes
retain the comparison API's specific missing-value reasons, even where that
API calls an undefined grid estimate `not available`. Only inaccessible data
qualify for that whole-exhibit status.

The headline is selected by fixed key preferences, never by agreement: prefer
primary statistics, then Threshold/annual-bps/Sharpe terms, then
column 1/headline/strategy, then lexical comparison key order. Its column,
term and statistic appear in the note. Whole-exhibit status uses all primary
targets, so one good headline cannot certify the full exhibit.
`--variant NAME` uses the comparison API's isolated robustness directory,
without fallback. Main inputs remain the default.

## Gap causes and inherited ambiguities

[Gap notes](../results/gap_notes.csv) contain only `exhibit,cause,note`.
Allowed causes are `proxy`, `timing`, `sample`, `method`, and `data`.
Unknown IDs, invalid causes, malformed rows and blank annotations raise errors.
A missing annotation leaves the report cause blank. Several annotations per
exhibit can preserve several tentative causes. The generator does not infer
causes from failed statistics or missing exports.

The initial annotations transcribe the explanations in
[core.md, Reading the gaps](../results/core.md#reading-the-gaps).
They describe that historical run, not new diagnoses. Tentative causes retain
that wording. The historical cost-unit problem remains identified as historical;
TASK-022 corrected units and excluded delta=0 from summaries under DEC-005.
TASK-030 must review real-run notes and add M-3 causes where evidence supports them.

No new choice about paper-notes §5 is needed for this reporting layer.
Timing, momentum, samples, returns, calendar windows, standard errors, control
scales, magnitudes, costs, strategy and trading-data alignment remain the
choices in the linked analysis methods. The Figure 6 axis transformation and
random-cost sign remain unresolved; blank exports keep their explicit reasons.
The CLI changes report tolerances and input selection only.

## Data map, method links and lineage

The data table reads D1–D28 directly from [sources.md](../data/sources.md),
including each current source/proxy, classification and availability. It checks
that every dataset occurs once. It links that map and
[proxy_comparison.md](../data/proxy_comparison.md). Relative source-card links
are rebased for the report destination, including destinations outside the repo.
The method list discovers all Markdown files in `docs/methods/` on each run.
Input paths, fixture mode, selected variant, tolerances and skipped-file reasons
are recorded inside the report. No separate metadata file is written.
