"""Comparison checks use hand-calculated results, independent of the SQL join."""

import csv
import sys

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


def test_duplicate_outputs_rejected(targets, tmp_path):
    fields = ["exhibit", "column", "term", "coef"]
    row = ["table_1", "1", "threshold", -0.4]
    write_csv(tmp_path / "table_1.csv", fields, [row, row])
    with pytest.raises(ValueError, match="duplicate"):
        compare.compare(targets, [tmp_path])


@pytest.mark.parametrize("value", ["NaN", "inf", "-inf"])
def test_nonfinite_outputs_rejected(targets, tmp_path, value):
    write_csv(
        tmp_path / "table_1.csv",
        ["exhibit", "column", "term", "coef"],
        [["table_1", "1", "threshold", value]],
    )
    with pytest.raises(ValueError, match="non-finite"):
        compare.compare(targets, [tmp_path])
