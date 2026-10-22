"""Offline sample identity, date matching, data validation and access classification."""

import json
from unittest.mock import Mock

import pandas as pd
import pytest
from sqlalchemy.exc import DBAPIError

from rebal.fetch import wrds_extract as wrds


@pytest.fixture
def headers():
    return pd.DataFrame(
        {
            "crsp_fundno": [1, 2],
            "nasdaq": ["VBMFX", "VBTLX"],
            "chgdt": ["2004-12-31"] * 2,
            "chgenddt": ["2006-12-31"] * 2,
            "first_offer_dt": ["1986-12-11", "2001-11-12"],
        }
    )


@pytest.fixture
def returns():
    return pd.DataFrame(
        {
            "crsp_fundno": [1, 2, 1, 2],
            "caldt": ["2004-01-02", "2004-01-02", "2005-01-03", "2005-01-03"],
            "dnav": [10.0, 10.0, 10.01, 10.01],
            "dret": [-0.01, -0.01, 0.003, 0.003],
        }
    )


def test_preserves_returns_and_flags_undated_tickers(headers, returns):
    result = wrds.parse_sample(headers, returns)
    assert result.ret.tolist() == returns.dret.tolist()
    assert result.is_sample.all()
    assert result.crsp_fundno.dtype == "int64"
    assert result.ticker.iloc[:2].isna().all()
    assert result.candidate_ticker.tolist() == ["VBMFX", "VBTLX"] * 2
    assert result.ticker_date_verified.tolist() == [False, False, True, True]


@pytest.mark.parametrize(
    "problem",
    [
        "duplicate",
        "nan",
        "infinite",
        "below_minus_one",
        "nav",
        "unknown_id",
        "bad_date",
    ],
)
def test_rejects_bad_returns(headers, returns, problem):
    if problem == "duplicate":
        returns = pd.concat([returns, returns.iloc[:1]])
    elif problem == "bad_date":
        returns.loc[0, "caldt"] = "bad"
    elif problem == "unknown_id":
        returns.loc[0, "crsp_fundno"] = 999
    elif problem == "nav":
        returns.loc[0, "dnav"] = 0
    else:
        returns.loc[0, "dret"] = {
            "nan": float("nan"),
            "infinite": float("inf"),
            "below_minus_one": -1.1,
        }[problem]
    with pytest.raises(ValueError):
        wrds.parse_sample(headers, returns)


@pytest.mark.parametrize(
    "problem", ["overlap", "ambiguous", "missing_ticker", "reversed"]
)
def test_rejects_bad_headers(headers, returns, problem):
    if problem == "overlap":
        headers = pd.concat([headers, headers.iloc[:1]])
    elif problem == "ambiguous":
        headers.loc[1, "crsp_fundno"] = 1
    elif problem == "missing_ticker":
        headers = headers.iloc[:1]
    else:
        headers.loc[0, "chgenddt"] = "2000-01-01"
    with pytest.raises(ValueError):
        wrds.parse_sample(headers, returns)


@pytest.mark.parametrize("code", ["42501", "42P01", "3F000", "08006", "57014"])
def test_only_explicit_access_errors_become_unavailable(monkeypatch, code):
    original = Exception("server error")
    original.pgcode = code
    error = DBAPIError("query", {}, original)
    monkeypatch.setattr(wrds, "query", Mock(side_effect=error))
    db = Mock()
    if code in {"42501", "42P01", "3F000"}:
        assert wrds.probe(db, "query")["sqlstate"] == code
    else:
        with pytest.raises(DBAPIError):
            wrds.probe(db, "query")
    db.connection.connection.rollback.assert_called_once()


def test_extract_writes_only_sample_and_reports_every_file(
    tmp_path, monkeypatch, capsys, headers, returns
):
    checks = {
        "treasury_returns": {"available": False},
        "treasury_ids": {"available": False},
        "futures": {"records": []},
    }
    monkeypatch.setattr(wrds, "access_checks", lambda db: checks)
    monkeypatch.setattr(
        wrds, "query", lambda db, sql: headers if sql == wrds.HEADER_SQL else returns
    )
    wrds.extract(Mock(), tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "bond_fund_daily.metadata.json",
        "bond_fund_daily.parquet",
    ]
    metadata = json.loads((tmp_path / "bond_fund_daily.metadata.json").read_text())
    assert metadata["is_sample"] is True
    assert metadata["undated_ticker_rows"] == 2
    assert (
        sum(line.startswith("OK ") for line in capsys.readouterr().out.splitlines())
        == 2
    )
    wrds.extract(Mock(), tmp_path)
    assert len(pd.read_parquet(tmp_path / "bond_fund_daily.parquet")) == 4


def test_inventory_lists_every_library_and_eight_relevance_answers(
    tmp_path, monkeypatch
):
    db = Mock()
    db.list_libraries.return_value = ["ff", "crspsamp_mf"]
    db.list_tables.side_effect = lambda library: (
        ["factors_daily"] if library == "ff" else ["daily_nav_ret"]
    )
    checks = {
        name: {
            "available": False,
            "sqlstate": "42501",
            "reason": "permission denied",
            "sql": sql,
        }
        for name, sql in wrds.PROBES.items()
    }
    for name in ["sample_header", "sample_returns", "factors"]:
        checks[name] = {
            "available": True,
            "rows": 1,
            "sql": wrds.PROBES[name],
            "records": [],
        }
    monkeypatch.setattr(wrds, "access_checks", lambda db: checks)
    path = tmp_path / "inventory.md"
    wrds.inventory(db, path)
    content = path.read_text()
    assert "| `crspsamp_mf` | 1 |" in content
    assert "| `ff` | 1 |" in content
    relevance = content.split("## Relevant to this replication")[1].split(
        "### Live access probes"
    )[0]
    assert (
        sum("**Yes**" in row or "**No**" in row for row in relevance.splitlines()) == 8
    )
    assert db.list_tables.call_count == 2
