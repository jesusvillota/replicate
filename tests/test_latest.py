"""Latest-sample estimates and isolation of main-run outputs."""

import csv
import json
import sys

import pandas as pd
import pytest

from rebal import latest, paths
from rebal.demo import make_panel, make_signals
from rebal.exhibits.predictive_tables import BASE, CONTROL_SETS
from rebal.regress import DEFAULT_SAMPLE, TABLE_COLUMNS, predictive


@pytest.fixture(scope="module")
def demo_run(tmp_path_factory):
    root = tmp_path_factory.mktemp("latest")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(paths, "REPO_ROOT", root)
        outputs = latest.run(demo=True)
    return outputs[0].parent


def test_latest_exports_and_planted_effects(demo_run):
    panel = make_panel()
    signals = make_signals(panel)
    table = pd.read_csv(demo_run / "table_1.csv", dtype={"column": str})
    assert list(table) == TABLE_COLUMNS
    assert table.column.nunique() == 5
    assert set(table.sample_end) == {panel.date.max().date().isoformat()}
    coefs = table[table.column == "1"].set_index("term").coef
    assert coefs.threshold == pytest.approx(-0.4, abs=0.05)
    assert coefs["calendar:week4"] == pytest.approx(-0.3, abs=0.05)
    table3 = pd.read_csv(demo_run / "table_3.csv", dtype={"column": str})
    assert list(table3) == TABLE_COLUMNS
    assert table3.column.nunique() == 4
    for column, outcome in (("1", "r_es"), ("3", "r_ty")):
        expected = predictive(
            signals, panel, BASE, y=outcome, sample=(DEFAULT_SAMPLE[0], "latest")
        )
        actual = table3[table3.column == column].set_index("term")
        assert actual.loc["threshold", "coef"] == pytest.approx(expected.coef.threshold)


def test_comparison_matches_independent_regressions(demo_run):
    with (demo_run / "latest_comparison.csv").open(newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == latest.COMPARISON_COLUMNS
        rows = list(reader)
    assert len(rows) == 2 * 5 * 2 * 6
    assert len(
        {tuple(row[key] for key in latest.COMPARISON_COLUMNS[:-1]) for row in rows}
    ) == len(rows)
    panel = make_panel()
    signals = make_signals(panel)
    counts = {}
    for sample, end in (("paper_end", DEFAULT_SAMPLE[1]), ("latest", "latest")):
        for column, controls in enumerate(CONTROL_SETS, 1):
            expected = predictive(
                signals, panel, BASE + controls, sample=(DEFAULT_SAMPLE[0], end)
            )
            for row in rows:
                if row["sample"] != sample or row["column"] != str(column):
                    continue
                target = expected.tidy.set_index("term").loc[row["term"], row["stat"]]
                assert row["exhibit"] == "table_1"
                if row["stat"] in {"sample_start", "sample_end"}:
                    assert row["value"] == target
                else:
                    assert float(row["value"]) == pytest.approx(target)
            counts[sample, column] = expected.nobs
    assert counts["latest", 1] > counts["paper_end", 1]


@pytest.mark.parametrize("demo,timing", [(True, "clean"), (False, "literal")])
def test_cli_protects_all_other_outputs(tmp_path, monkeypatch, demo, timing):
    monkeypatch.setattr(paths, "REPO_ROOT", tmp_path)
    # Include main tables, metadata and nested outputs in the protected tree.
    for name in (
        "table_1.csv",
        "table_3.csv",
        "magnitudes.csv",
        "metadata.json",
        "robustness/other/table_1.csv",
        "archive/latest/table_1.csv",
    ):
        path = tmp_path / "output/tables" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"preserve {name}\n")
    demo_table = tmp_path / "output/demo/table_1.csv"
    demo_table.parent.mkdir(parents=True, exist_ok=True)
    demo_table.write_text("preserve demo main\n")
    destination = (
        tmp_path / "output" / ("demo" if demo else "tables") / "robustness/latest"
    )

    def snapshot():
        return {
            path.relative_to(tmp_path): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in (tmp_path / "output").rglob("*")
            if path.is_file() and not path.is_relative_to(destination)
        }

    before = snapshot()
    seen = []
    panel = make_panel(end="2026-02-13")
    signals = make_signals(panel, beta_threshold=0, beta_calweek4=0)
    monkeypatch.setattr(latest, "load_panel", lambda **kwargs: panel)

    def load_signals(**kwargs):
        seen.append(kwargs)
        return signals

    monkeypatch.setattr(latest, "load_signals", load_signals)
    args = ["latest", "--timing", timing] + (["--demo"] if demo else [])
    monkeypatch.setattr(sys, "argv", args)
    latest.main()
    assert seen == [{"demo": demo, "timing": timing}]
    assert snapshot() == before  # detects edits, deletions and new files anywhere else
    assert {path.name for path in destination.iterdir()} == {
        "table_1.csv",
        "table_3.csv",
        "latest_comparison.csv",
        "latest.metadata.json",
    }
    table = pd.read_csv(destination / "table_1.csv")
    assert set(table.sample_end) == {"2026-02-13"}
    assert table[table.term.isin(latest.TERMS)].coef.abs().lt(0.05).all()
    metadata = json.loads((destination / "latest.metadata.json").read_text())
    assert metadata["samples"]["latest"][1] == "2026-02-13"
    assert metadata["samples"]["paper_end"] == list(DEFAULT_SAMPLE)


def test_invalid_timing():
    with pytest.raises(ValueError, match="timing"):
        latest.run(timing="../other")
