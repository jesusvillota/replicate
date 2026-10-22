"""Comparison checks use hand-calculated results, independent of the SQL join."""

import csv
import sys
from pathlib import Path

import pytest

from rebal import compare


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(fields)
        writer.writerows(rows)
    return path


@pytest.fixture
def targets(tmp_path):
    return write_csv(
        tmp_path / "targets.csv",
        ["exhibit", "column", "term", "stat", "paper_value", "approx", "source_page"],
        [
            ["table_1", "1", "threshold", "coef", -0.4, 0, 20],
            ["table_1", "1", "threshold", "se", 0.1, 0, 20],
            ["table_1", "1", "calendar", "coef", 0.05, 0, 20],
            ["table_1", "1", "calendar", "t", 0.5, 0, 20],
            ["table_1", "2", "threshold", "coef", -0.2, 0, 20],
            ["table_1", "2", "threshold", "t", -1.96, 0, 20],
            ["table_1", "1", "zero", "coef", 0, 0, 20],
            ["table_1", "1", "unproduced", "coef", 1, 0, 20],
            ["figure_6", "strategy", "end", "value", 6.2, 1, 40],
        ],
    )


def test_join_statistics_significance_and_missing(targets, tmp_path):
    folder = tmp_path / "output"
    write_csv(
        folder / "table_1.csv",
        ["exhibit", "column", "term", "coef", "se", "t"],
        [
            ["table_1", "1", "threshold", -0.6, 0.2, ""],
            ["table_1", "1", "calendar", -0.1, 0.1, -1],
            ["table_1", "2", "threshold", -0.1, 0.1, -1],
            ["table_1", "1", "zero", 0.1, 0.1, 1],
            ["table_1", "3", "threshold", 99, 1, 99],
        ],
    )
    rows = compare.compare(targets, [folder])
    by_key = {(r["column"], r["term"], r["stat"]): r for r in rows}
    threshold = by_key["1", "threshold", "coef"]
    assert threshold["ours"] == -0.6
    assert threshold["ratio"] == pytest.approx(1.5)
    assert threshold["sign_match"] is True
    assert (
        threshold["significance_match"] is True
    )  # t derived from coef/se on both sides
    assert by_key["1", "threshold", "se"]["ours"] == 0.2
    assert by_key["1", "threshold", "se"]["sign_match"] is None
    assert by_key["1", "calendar", "coef"]["sign_match"] is False
    assert by_key["1", "calendar", "coef"]["significance_match"] is True
    assert by_key["2", "threshold", "coef"]["significance_match"] is False
    assert by_key["1", "zero", "coef"]["ratio"] is None
    assert by_key["1", "zero", "coef"]["significance_match"] is None
    assert by_key["1", "unproduced", "coef"]["ours"] is None
    report = compare.render_report(rows, targets, [folder])
    assert "Targets matched: 7/9" in report
    assert "Sign-match rate: 50.0% (3/6 eligible targets)" in report
    assert "Significance-match rate: 60.0% (3/5 eligible targets)" in report
    assert "Missing exhibits: figure_6\n" in report
    assert "| 1: threshold [coef] | -0.4 | -0.6 | 1.5 | yes | yes |" in report
    assert "| strategy: end [value] | ~6.2 | N/A |" in report


def test_long_figures_and_wide_values(targets, tmp_path):
    folder = tmp_path / "figures"
    path = folder / "figure_6.csv"
    for fields, values in [
        (["stat", "value"], ["value", 3.1]),
        (["value"], [3.1]),
    ]:
        write_csv(
            path,
            ["exhibit", "column", "term", *fields],
            [["figure_6", "strategy", "end", *values]],
        )
        rows = compare.compare(targets, [folder])
        row = next(r for r in rows if r["exhibit"] == "figure_6")
        assert row["ratio"] == 0.5
        assert row["sign_match"] is True
        assert row["significance_match"] is None


def test_empty_outputs_and_demo_isolation(targets, tmp_path, monkeypatch):
    destination = tmp_path / "docs" / "results" / "targets.csv"
    destination.parent.mkdir(parents=True)
    destination.write_bytes(targets.read_bytes())
    # Real results must not leak into demo mode.
    write_csv(
        tmp_path / "output" / "tables" / "figure_6.csv",
        ["exhibit", "column", "term", "value"],
        [["figure_6", "strategy", "end", 6.2]],
    )
    report_path = tmp_path / "output" / "demo" / "compare.md"
    monkeypatch.setattr(compare, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["compare", "--demo", "--out", str(report_path)])
    compare.main()
    report = report_path.read_text()
    assert "Targets matched: 0/9" in report
    assert "Sign-match rate: N/A (0/0 eligible targets)" in report
    assert "Missing exhibits: figure_6, table_1" in report
    monkeypatch.setattr(sys, "argv", ["compare", "--out", str(report_path)])
    compare.main()
    assert "Targets matched: 1/9" in report_path.read_text()


def test_duplicate_outputs_skipped(targets, tmp_path):
    fields = ["exhibit", "column", "term", "coef"]
    row = ["table_1", "1", "threshold", -0.4]
    write_csv(tmp_path / "table_1.csv", fields, [row, row])
    skipped = []
    rows = compare.compare(targets, [tmp_path], skipped=skipped)
    assert all(row["ours"] is None for row in rows)
    assert any("table_1.csv: duplicate" in reason for reason in skipped)


@pytest.mark.parametrize("value", ["NaN", "inf", "-inf"])
def test_nonfinite_outputs_skipped(targets, tmp_path, value):
    write_csv(
        tmp_path / "table_1.csv",
        ["exhibit", "column", "term", "coef"],
        [["table_1", "1", "threshold", value]],
    )
    skipped = []
    rows = compare.compare(targets, [tmp_path], skipped=skipped)
    assert all(row["ours"] is None for row in rows)
    assert any("table_1.csv: non-finite" in reason for reason in skipped)


@pytest.mark.parametrize(
    "fields, values, reason",
    [
        (["signal", "mean"], [["threshold", 0.49]], "missing columns"),
        (["predictor", "threshold"], [["calendar", 0.605]], "missing columns"),
        (
            ["exhibit", "column", "term", "stat"],
            [["table_1", "1", "threshold", "coef"]],
            "value column",
        ),
        (
            ["exhibit", "column", "term", "coef"],
            [["table_1", "1", "threshold", "bad"]],
            "could not convert",
        ),
        (
            ["exhibit", "column", "term", "value"],
            [["table_1", "1", "threshold"]],
            "row width",
        ),
        (
            ["exhibit", "column", "term", "value"],
            [["table_1", "1", "threshold", 1, 2]],
            "row width",
        ),
        (
            ["exhibit", "column", "term", "value"],
            [["table_1", "", "threshold", 1]],
            "nonempty",
        ),
        (
            ["exhibit", "column", "term", "stat", "value"],
            [["table_1", "1", "threshold", "bad", 1]],
            "invalid statistic",
        ),
        (
            ["exhibit", "column", "term", "date"],
            [["table_1", "1", "threshold", "2000"]],
            "no supported",
        ),
        (
            ["exhibit", "column", "term", "coef"],
            [["unknown", "1", "threshold", 1]],
            "no matching target",
        ),
    ],
)
def test_unjoinable_csv_reported_while_valid_csv_matches(
    targets, tmp_path, fields, values, reason
):
    folder = tmp_path / "output"
    write_csv(folder / "unsupported.csv", fields, values)
    write_csv(
        folder / "figure_6.csv",
        ["exhibit", "column", "term", "value"],
        [["figure_6", "strategy", "end", 3.1]],
    )
    skipped = []
    rows = compare.compare(targets, [folder], skipped=skipped)
    report = compare.render_report(rows, targets, [folder], skipped=skipped)
    assert "Targets matched: 1/9" in report
    assert "Missing exhibits: table_1\n" in report
    assert "Skipped CSVs: 1" in report
    assert "unsupported.csv" in report and reason in report


@pytest.mark.parametrize(
    "relative_path", ["magnitudes/magnitudes.csv", "magnitudes.csv"]
)
def test_signed_magnitudes_and_zero(targets, tmp_path, relative_path):
    folder = tmp_path / "output"
    write_csv(
        folder / "table_1.csv",
        ["exhibit", "column", "term", "coef"],
        [["table_1", "1", "threshold", -0.4], ["table_1", "1", "zero", 0]],
    )
    write_csv(
        folder / relative_path,
        ["exhibit", "column", "term", "coef", "magnitude_bps"],
        [["table_1", "1", "threshold", -0.4, -20]],
    )
    with targets.open("a") as stream:
        stream.write("table_1,1,threshold,value,-20,0,20\n")
    skipped = []
    rows = compare.compare(targets, [folder], skipped=skipped)
    by_key = {(r["term"], r["stat"]): r for r in rows if r["column"] == "1"}
    assert by_key["threshold", "value"]["ours"] == -20
    assert by_key["threshold", "value"]["sign_match"] is True
    assert by_key["threshold", "coef"]["ours"] == -0.4
    assert by_key["zero", "coef"]["ours"] == 0
    assert not skipped


def test_duplicate_across_files_skips_whole_later_file(targets, tmp_path):
    folder = tmp_path / "output"
    fields = ["exhibit", "column", "term", "coef"]
    write_csv(folder / "a.csv", fields, [["table_1", "1", "threshold", -0.4]])
    write_csv(
        folder / "b.csv",
        fields,
        [["table_1", "1", "threshold", 99], ["table_1", "1", "calendar", 99]],
    )
    skipped = []
    rows = compare.compare(targets, [folder], skipped=skipped)
    assert sum(row["ours"] is not None for row in rows) == 1
    assert "b.csv: duplicate key across CSV files" in skipped[0]


def test_invalid_targets_still_fail(targets, tmp_path):
    with targets.open("a") as stream:
        stream.write("table_1,1,threshold,coef,-0.4,0,20\n")
    with pytest.raises(ValueError, match="targets: duplicate"):
        compare.compare(targets, [tmp_path / "empty"])


def test_current_predictive_outputs_match_all_their_targets(tmp_path, monkeypatch):
    """Exercise the actual exporters so renamed keys cannot silently disappear."""
    from rebal.exhibits import predictive_tables, signals_descriptive

    # Build real demo exports in isolation; never depend on existing output/demo.
    monkeypatch.setattr(predictive_tables, "output_dir", lambda kind: tmp_path)
    monkeypatch.setattr(signals_descriptive, "output_dir", lambda kind: tmp_path)
    predictive_tables.run(demo=True)
    signals_descriptive.run(demo=True)
    targets = Path(__file__).resolve().parents[1] / "docs/results/targets.csv"
    skipped = []
    rows = compare.compare(targets, [tmp_path], skipped=skipped)
    produced = set(predictive_tables.EXHIBITS)
    relevant = [row for row in rows if row["exhibit"] in produced]
    assert len(relevant) == 238
    assert all(row["ours"] is not None for row in relevant)
    assert sum(row["stat"] == "value" for row in relevant) == 6
    descriptive_rows = [
        row for row in rows if row["exhibit"] in {"table_C1", "table_C2"}
    ]
    assert len(descriptive_rows) == 14
    assert all(row["ours"] is not None for row in descriptive_rows)
    assert not any(
        f"{name}.csv:" in reason
        for name in ("table_C1", "table_C2")
        for reason in skipped
    )
    for name in (
        "figure_C1",
        "table_D2",
        "table_D5",
        "table_D13",
    ):
        assert any(f"{name}.csv:" in reason for reason in skipped)
    # All six magnitude targets use emitted column keys and the signed source field.
    with (tmp_path / "magnitudes" / "magnitudes.csv").open() as stream:
        magnitudes = {
            tuple(row[key] for key in compare.KEY): float(row["magnitude_bps"])
            for row in csv.DictReader(stream)
        }
    for row in relevant:
        if row["stat"] == "value":
            assert row["ours"] == magnitudes[tuple(row[key] for key in compare.KEY)]
            assert row["source_page"] == ("20" if row["exhibit"] == "table_1" else "33")
            assert (row["paper_value"] > 0) == (row["column"] == "3")
