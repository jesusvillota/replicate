"""Contract and integration checks for the shared rebal scaffold."""

import importlib
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
import requests
import statsmodels.api as sm

from rebal import io, paths
from rebal.demo import make_panel, make_signals
from rebal.exhibits import __main__ as exhibits
from rebal.fetch.common import download, summarize


def contract_schema(name):
    rows = (
        (paths.REPO_ROOT / "docs" / "contracts" / f"{name}.md").read_text().splitlines()
    )
    return {
        cells[0]: cells[1]
        for row in rows
        if row.startswith("| ") and not row.startswith("| Column ")
        for cells in [[cell.strip() for cell in row.split("|")[1:-1]]]
    }


@pytest.fixture(scope="module")
def panel():
    return make_panel()


@pytest.fixture(scope="module")
def signals(panel):
    return make_signals(panel)


@pytest.mark.parametrize("contract", ["daily_panel", "signals"])
def test_exact_contract_schema(contract, panel, signals):
    frame = panel if contract == "daily_panel" else signals
    schema = contract_schema(contract)
    assert list(frame.columns) == list(schema)
    for name, dtype in schema.items():
        assert str(frame[name].dtype) == dtype
    assert frame.date.is_unique and frame.date.is_monotonic_increasing
    assert frame.date.dt.tz is None
    assert not frame.isna().any().any()


def test_panel_scales(panel):
    assert panel.r_es.std() * np.sqrt(252) == pytest.approx(0.18, abs=0.01)
    assert panel.r_ty.std() * np.sqrt(252) == pytest.approx(0.06, abs=0.005)
    assert panel.r_es.corr(panel.r_ty) == pytest.approx(-0.2, abs=0.04)
    np.testing.assert_allclose(panel.r_mkt_french, panel.mkt_rf + panel.rf)


@pytest.mark.parametrize("expected", [(-0.4, -0.3), (0.0, 0.0)])
def test_planted_next_day_ols(panel, expected):
    frame = make_signals(panel, *expected)
    # Independent OLS oracle; a wrong lag in the demo check cannot hide here.
    x = np.column_stack(
        (
            frame.threshold.to_numpy()[:-1],
            (frame.calendar * frame.week4).to_numpy()[:-1],
        )
    )
    result = sm.OLS(frame.ret.to_numpy()[1:], sm.add_constant(x)).fit()
    np.testing.assert_allclose(result.params[1:], expected, atol=0.05, rtol=0)


def test_signal_scales_and_calendar(signals):
    assert signals.threshold.std() == pytest.approx(0.0048, rel=0.1)
    assert signals.calendar.std() == pytest.approx(0.01, rel=0.1)
    assert signals.threshold.autocorr() == pytest.approx(0.61, abs=0.05)
    assert signals.calendar.autocorr() == pytest.approx(0.91, abs=0.03)
    np.testing.assert_allclose(
        signals.filter(regex=r"^thr_0(0[0-9]|1[0-9]|2[0-5])$").mean(axis=1),
        signals.threshold,
    )
    assert (signals[[f"week{i}" for i in range(1, 5)]].sum(axis=1) == 1).all()
    assert (signals.week4 == (signals.days_to_month_end <= 5)).all()
    assert (signals.week3 == signals.days_to_month_end.between(6, 10)).all()
    assert (signals.week2 == signals.days_to_month_end.between(11, 15)).all()
    assert (signals.week1 == (signals.days_to_month_end > 15)).all()
    assert signals.groupby(signals.date.dt.to_period("M")).week4.sum().eq(5).all()


def test_fixture_determinism_and_no_mutation(panel, signals):
    original = panel.copy(deep=True)
    pd.testing.assert_frame_equal(make_panel(), panel)
    pd.testing.assert_frame_equal(make_signals(panel), signals)
    pd.testing.assert_frame_equal(panel, original)
    assert not make_signals(panel, seed=1).equals(signals)


@pytest.mark.parametrize(
    "module,args,output",
    [
        ("rebal.demo", ["--check"], "PASS"),
        ("rebal.exhibits", ["--all", "--demo"], "exhibit modules"),
    ],
)
def test_cli(module, args, output):
    result = subprocess.run(
        [sys.executable, "-m", module, *args],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert output in result.stdout


def test_exhibit_discovery_and_selection(monkeypatch, capsys):
    calls = []
    modules = {}
    for name, ids in [("tables", ["table_1", "table_2a"]), ("figures", ["figure_2"])]:
        module = ModuleType(f"rebal.exhibits.{name}")
        module.EXHIBITS = ids
        module.run = lambda demo, name=name: (
            calls.append((name, demo)) or [Path(f"{name}.csv")]
        )
        modules[module.__name__] = module
    monkeypatch.setattr(
        exhibits.pkgutil,
        "iter_modules",
        lambda _: [
            SimpleNamespace(name="tables"),
            SimpleNamespace(name="_helper"),
            SimpleNamespace(name="figures"),
        ],
    )
    monkeypatch.setattr(importlib, "import_module", modules.__getitem__)
    monkeypatch.setattr(
        sys, "argv", ["exhibits", "--all", "--only", "table_1", "--demo"]
    )
    exhibits.main()
    assert calls == [("tables", True)]
    assert "1 exhibit modules" in capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", ["exhibits", "--only", "missing"])
    with pytest.raises(SystemExit, match="Unknown exhibit IDs: missing"):
        exhibits.main()


def test_paths_and_loaders(monkeypatch, tmp_path, panel, signals):
    monkeypatch.setattr(paths, "REPO_ROOT", tmp_path / "repo")
    monkeypatch.setenv("REPLICATE_DATA_DIR", str(tmp_path / "external"))
    assert paths.public_dir("fed") == tmp_path / "repo/data/public/fed"
    assert paths.licensed_dir("wrds") == tmp_path / "external/licensed/wrds"
    assert paths.processed_dir() == tmp_path / "external/processed"
    for kind in ("tables", "figures", "demo"):
        assert paths.output_dir(kind).is_dir()
    with pytest.raises(FileNotFoundError, match="rebal.panel --build"):
        io.load_panel()
    with pytest.raises(FileNotFoundError, match="rebal.signals --build"):
        io.load_signals(timing="literal")
    panel.to_parquet(paths.processed_dir() / "daily_panel.parquet", index=False)
    signals.to_parquet(paths.processed_dir() / "signals_literal.parquet", index=False)
    pd.testing.assert_frame_equal(io.load_panel(), panel)
    pd.testing.assert_frame_equal(io.load_signals(timing="literal"), signals)
    pd.testing.assert_frame_equal(io.load_panel(demo=True), panel)
    pd.testing.assert_frame_equal(io.load_signals(demo=True), signals)
    with pytest.raises(ValueError):
        paths.licensed_dir("../public")
    with pytest.raises(ValueError):
        paths.output_dir("invalid")
    with pytest.raises(ValueError):
        io.load_signals(timing="../bad")


def test_default_data_root(monkeypatch, tmp_path):
    monkeypatch.delenv("REPLICATE_DATA_DIR", raising=False)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    assert paths.licensed_dir("test").is_dir()
    assert paths.processed_dir().parent == tmp_path / "data/replicate"


@pytest.mark.parametrize("extension", ["csv", "parquet", "xlsx"])
def test_summarize_valid_file(tmp_path, capsys, extension):
    frame = pd.DataFrame({"date": ["2020-01-03", "2020-01-02"], "value": [1, 2]})
    path = tmp_path / f"source.{extension}"
    getattr(
        frame, {"csv": "to_csv", "parquet": "to_parquet", "xlsx": "to_excel"}[extension]
    )(path, index=False)
    summarize(path, "date")
    assert (
        capsys.readouterr().out
        == f"OK {path} rows=2 first=2020-01-02 last=2020-01-03\n"
    )


@pytest.mark.parametrize(
    "dates,error",
    [
        ([], "at least one row"),
        (["bad date"], "Unknown datetime"),
        (["2020-01-02", "2020-01-02"], "duplicate dates"),
        (["2020-01-02", None], "nonmissing"),
    ],
)
def test_summarize_rejects_invalid_files(tmp_path, capsys, dates, error):
    path = tmp_path / "invalid.csv"
    pd.DataFrame({"date": dates}).to_csv(path, index=False)
    with pytest.raises((ValueError, pd.errors.ParserError), match=error):
        summarize(path, "date")
    assert capsys.readouterr().out == ""


def test_download_errors_and_atomic_write(monkeypatch, tmp_path):
    dest = tmp_path / "file.csv"
    dest.write_bytes(b"original")
    response = MagicMock()
    response.__enter__.return_value = response
    response.raise_for_status.side_effect = requests.HTTPError("503")
    get = MagicMock(return_value=response)
    monkeypatch.setattr(requests, "get", get)
    monkeypatch.setattr("rebal.fetch.common.sleep", lambda _: None)
    with pytest.raises(requests.HTTPError, match="503"):
        download("https://example.invalid/data", dest, retries=2)
    assert get.call_count == 3
    assert dest.read_bytes() == b"original"
    response.raise_for_status.side_effect = None
    response.iter_content.return_value = [b"new", b" content"]
    assert download("https://example.invalid/data", dest) == dest
    assert dest.read_bytes() == b"new content"
    assert "Mozilla/" in get.call_args.kwargs["headers"]["User-Agent"]
    assert list(tmp_path.iterdir()) == [dest]
    with pytest.raises(ValueError):
        download("https://example.invalid/data", dest, retries=-1)
