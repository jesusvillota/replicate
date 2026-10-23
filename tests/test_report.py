"""Final-report acceptance with isolated exports and the checked-in contracts."""

import csv
import re
import shutil
import sys

import pytest

from rebal import report
from rebal.paths import REPO_ROOT


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)


@pytest.fixture
def inputs(tmp_path):
    root = tmp_path / "repo"
    for name in (
        "contracts/exhibits.md",
        "data/sources.md",
        "data/proxy_comparison.md",
    ):
        target = root / "docs" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / "docs" / name, target)
    methods = root / "docs/methods"
    methods.mkdir()
    (methods / "report.md").write_text("# Methods\n")
    (methods / "new_method.md").write_text("# Future method\n")
    write_csv(
        root / "docs/results/gap_notes.csv",
        ["exhibit", "cause", "note"],
        [
            ["table_2a", "proxy", "Recorded explanation | with a delimiter."],
        ],
    )
    targets = []
    actual = []
    for exhibit, ours, se in [
        ("table_1", -1.1, 0.2),
        ("table_2a", -2, 0.2),
        ("table_2b", 1, 0.2),
        ("table_3", -1, 1),
    ]:
        targets += [
            [exhibit, "1", "threshold", "coef", -1, 0, 1],
            [exhibit, "1", "threshold", "se", 0.2, 0, 1],
        ]
        actual.append([exhibit, "1", "threshold", ours, se])
    targets += [
        ["table_D9", "3", "threshold", "coef", -1, 0, 1],
        ["figure_5", "ancerno", "threshold", "value", -0.1, 1, 1],
        ["table_4", "1", "threshold", "coef", -1, 0, 1],
    ]
    write_csv(
        root / "docs/results/targets.csv",
        ["exhibit", "column", "term", "stat", "paper_value", "approx", "source_page"],
        targets,
    )
    write_csv(
        root / "output/demo/estimates.csv",
        ["exhibit", "column", "term", "coef", "se"],
        actual,
    )
    return root


def exhibit_table(text):
    section = text.split("## Exhibit table\n", 1)[1].split("## Gap notes\n", 1)[0]
    rows = [line.split(" | ") for line in section.splitlines() if line.startswith("| ")]
    return {row[0].removeprefix("| "): row[1] for row in rows[1:]}


def test_statuses_and_exact_contract_coverage(inputs, tmp_path):
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True)
    table = exhibit_table(text)
    assert table["table_1"] == "replicates"
    assert table["table_2a"] == "partly"  # size differs, same significant sign
    assert table["table_2b"] == "fails"  # opposite sign
    assert table["table_3"] == "partly"  # significance differs
    assert table["table_D9"] == table["figure_5"] == "not available"
    assert table["table_4"] == "not run"
    contract = report.contract_ids(REPO_ROOT / "docs/contracts/exhibits.md")
    assert list(table) == contract
    section = text.split("## Exhibit table\n")[1].split("## Gap notes\n")[0]
    for name in contract:
        assert section.count(f"| {name} |") == 1
    assert "Target keys joined: 8/11" in text
    assert "Numeric targets joined: 8/11" in text
    assert "Sign-match rate: 75.0% (3/4 eligible targets)" in text
    assert "Significance-match rate: 75.0% (3/4 eligible targets)" in text
    assert re.findall(r"^## (.+)$", text, re.MULTILINE) == [
        "Summary",
        "Exhibit table",
        "Gap notes",
        "Data and proxies",
        "Method choices",
        "Latest sample (footnote 32)",
    ]


def test_gap_causes_are_only_read_from_file(inputs, tmp_path):
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True)
    gaps = text.split("## Gap notes\n")[1].split("## Data and proxies\n")[0]
    assert "| table_2a | proxy | Recorded explanation \\| with a delimiter. |" in gaps
    assert "| table_2b |  |  |" in gaps  # failing result cannot invent a cause
    assert "| table_D9 |  |  |" in gaps  # inaccessible data cannot invent a cause


def test_source_map_and_method_links_follow_destination(inputs, tmp_path):
    destination = tmp_path / "external dir/report.md"
    text = report.generate_report(inputs, destination, demo=True)
    data = text.split("## Data and proxies\n")[1].split("## Method choices\n")[0]
    assert re.findall(r"^\| (D\d+) \|", data, re.MULTILINE) == [
        f"D{i}" for i in range(1, 29)
    ]
    assert "[Master source map](../repo/docs/data/sources.md)" in data
    assert "[Proxy comparison](../repo/docs/data/proxy_comparison.md)" in data
    assert "(../repo/docs/data/cards/crsp.md)" in data
    assert "[new_method.md](../repo/docs/methods/new_method.md)" in text
    assert "[report.md](../repo/docs/methods/report.md)" in text
    assert "https://wrds-www.wharton.upenn.edu/" in text


def test_cli_reads_demo_only_and_overwrites_only_destination(
    inputs, tmp_path, monkeypatch
):
    write_csv(
        inputs / "output/tables/real.csv",
        ["exhibit", "column", "term", "coef", "se"],
        [["table_1", "1", "threshold", 999, 0.2]],
    )
    before = {path: path.read_bytes() for path in inputs.rglob("*") if path.is_file()}
    destination = tmp_path / "external/report.md"
    monkeypatch.setattr(report, "REPO_ROOT", inputs)
    monkeypatch.setattr(sys, "argv", ["report", "--demo", "--out", str(destination)])
    report.main()
    assert exhibit_table(destination.read_text())["table_1"] == "replicates"
    assert "Synthetic fixture outputs" in destination.read_text()
    destination.write_text("replace me")
    report.main()
    assert destination.read_text().startswith("# Replication report\n")
    assert before == {
        path: path.read_bytes() for path in inputs.rglob("*") if path.is_file()
    }
    monkeypatch.setattr(sys, "argv", ["report", "--out", str(destination)])
    report.main()
    assert exhibit_table(destination.read_text())["table_1"] == "fails"
    assert "Synthetic fixture outputs" not in destination.read_text()


def test_missing_and_variant_exports_never_fail(inputs, tmp_path):
    demo = inputs / "output/demo"
    variant = demo / "robustness/other"
    variant.mkdir(parents=True)
    shutil.copyfile(demo / "estimates.csv", variant / "estimates.csv")
    (demo / "estimates.csv").unlink()
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True)
    assert exhibit_table(text)["table_1"] == "not run"
    assert "Sign-match rate: N/A (0/0 eligible targets)" in text
    text = report.generate_report(
        inputs, tmp_path / "report.md", demo=True, variant="other"
    )
    assert exhibit_table(text)["table_1"] == "replicates"
    with pytest.raises(ValueError, match="directory name"):
        report.generate_report(
            inputs, tmp_path / "report.md", demo=True, variant="../other"
        )


def test_incomplete_target_coverage_is_partial(inputs, tmp_path):
    with (inputs / "docs/results/targets.csv").open("a") as stream:
        stream.write("table_2b,1,calendar,coef,-1,0,1\n")
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True)
    assert exhibit_table(text)["table_2b"] == "partly"
    assert "no export: no selected CSV provides this target statistic" in text


def test_tolerance_overrides_and_zero_floor(inputs, tmp_path):
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True, relative=1)
    assert exhibit_table(text)["table_2a"] == "replicates"
    row = {
        "exhibit": "figure_1",
        "column": "x",
        "term": "zero",
        "stat": "value",
        "ours": 0,
        "paper_value": 0,
        "sign_match": True,
        "significance_match": None,
    }
    assert report.classify([row], 0.25, 0.0001) == "replicates"
    row.update(ours=0.0001, sign_match=False)
    assert (
        report.classify([row], 0.25, 0.0001) == "fails"
    )  # size floor does not override sign


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf")])
def test_invalid_tolerances(inputs, tmp_path, value):
    with pytest.raises(ValueError, match="finite and nonnegative"):
        report.generate_report(inputs, tmp_path / "report.md", relative=value)


@pytest.mark.parametrize("cause", ["invented", ""])
def test_invalid_gap_cause_is_rejected(inputs, tmp_path, cause):
    write_csv(
        inputs / "docs/results/gap_notes.csv",
        ["exhibit", "cause", "note"],
        [["table_1", cause, "Bad cause"]],
    )
    with pytest.raises(ValueError, match="invalid gap annotation"):
        report.generate_report(inputs, tmp_path / "report.md", demo=True)


def test_real_demo_export_integration(inputs, tmp_path, monkeypatch):
    from rebal.exhibits import signals_descriptive

    monkeypatch.setattr(
        signals_descriptive, "output_dir", lambda kind: inputs / "output/demo"
    )
    (inputs / "output/demo/estimates.csv").unlink()
    signals_descriptive.run(demo=True)
    shutil.copyfile(
        REPO_ROOT / "docs/results/targets.csv", inputs / "docs/results/targets.csv"
    )
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True)
    assert "| table_C1 |" in text
    assert "headline calendar:ar1 [value]" in text
    assert "Numeric targets joined: 14/399" in text


def test_latest_sample_missing_and_demo_isolation(inputs, tmp_path):
    destination = tmp_path / "report.md"
    missing = report.generate_report(inputs, destination, demo=True)
    assert missing.endswith("## Latest sample (footnote 32)\n\nnot run\n\n")
    fields = ["exhibit", "column", "term", "stat", "sample", "value"]
    for kind, value in (("tables", "real-only"), ("demo", "demo-only")):
        write_csv(
            inputs / "output" / kind / "robustness/latest/latest_comparison.csv",
            fields,
            [["table_1", "1", "threshold", "coef", "latest", value]],
        )
    demo = report.generate_report(inputs, destination, demo=True)
    real = report.generate_report(inputs, destination)
    assert "demo-only" in demo and "real-only" not in demo
    assert "real-only" in real and "demo-only" not in real
    assert demo.split("## Latest sample")[0] == missing.split("## Latest sample")[0]
    assert "repo/output/demo/robustness/latest/latest_comparison.csv" in demo


def test_latest_sample_real_export_integration(inputs, tmp_path, monkeypatch):
    from rebal import latest, paths

    monkeypatch.setattr(paths, "REPO_ROOT", inputs)
    latest.run(demo=True)
    text = report.generate_report(inputs, tmp_path / "report.md", demo=True)
    section = text.split("## Latest sample (footnote 32)\n", 1)[1]
    assert "| table_1 | 1 | threshold | coef | paper_end |" in section
    assert "| table_1 | 1 | calendar:week4 | coef | latest |" in section
    assert "| sample_end | paper_end | 2023-03-17 |" in section
    assert "| sample_end | latest | 2023-12-29 |" in section
