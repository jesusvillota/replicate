"""Distribution-inclusive returns, missing data and study boundary safeguards."""

import numpy as np
import pandas as pd
import pytest

from rebal.fetch.yahoo_bond_funds import total_returns


def history():
    # A cash distribution offsets the NAV drop. Raw NAV loses 10%; total return is zero.
    return pd.DataFrame(
        {
            "date": ["1997-09-09", "1997-09-10", "2023-03-17"],
            "Close": [10.0, 9.0, 9.9],
            "Adj Close": [9.0, 9.0, 9.9],
            "Dividends": [0.0, 0.75, 0.0],
            "Capital Gains": [0.0, 0.25, 0.0],
            "Stock Splits": [0.0, 0.0, 0.0],
        }
    )


def test_includes_dividends_and_capital_gains_without_filling():
    output = total_returns(history(), "VBMFX")
    assert np.isnan(output.ret.iloc[0])
    assert output.ret.iloc[1] == pytest.approx(0)
    assert output.nav_return.iloc[1] == pytest.approx(-0.1)
    assert output.ret.iloc[2] == pytest.approx(0.1)
    assert output.distribution.iloc[1] == 1


@pytest.mark.parametrize(
    "problem",
    [
        "nav_only",
        "no_events",
        "missing",
        "duplicate",
        "unsorted",
        "boundary",
        "split",
        "negative",
        "infinite",
    ],
)
def test_rejects_invalid_or_unverified_history(problem):
    frame = history()
    if problem == "nav_only":
        frame["Adj Close"] = frame.Close
    elif problem == "no_events":
        frame["Dividends"] = 0
        frame["Capital Gains"] = 0
    elif problem == "missing":
        frame.loc[1, "Adj Close"] = np.nan
    elif problem == "duplicate":
        frame.loc[1, "date"] = frame.date.iloc[0]
    elif problem == "unsorted":
        frame = frame.iloc[::-1]
    elif problem == "boundary":
        frame.loc[1, "date"] = "1997-09-11"
    elif problem == "split":
        frame.loc[1, "Stock Splits"] = 2
    elif problem == "negative":
        frame.loc[1, "Dividends"] = -1
    else:
        frame.loc[1, "Close"] = np.inf
    with pytest.raises(ValueError):
        total_returns(frame, "VBMFX")


def test_fetch_preserves_source_and_writes_verified_returns(tmp_path, monkeypatch):
    import json

    from rebal.fetch import yahoo_bond_funds as funds

    def source(ticker, directory, retries):
        path = directory / f"{ticker}.csv"
        history().to_csv(path, index=False)
        path.with_suffix(".json").write_text('{"original": true}')
        path.with_suffix(".metadata.json").write_text('{"raw_sha256": "test-hash"}')
        return path

    monkeypatch.setattr(funds, "fetch_ticker", source)
    path = funds.fetch("VBMFX", tmp_path, retries=0)
    assert pd.read_parquet(path).ret.iloc[1] == pytest.approx(0)
    metadata = json.loads(path.with_suffix(".metadata.json").read_text())
    assert metadata["raw_sha256"] == "test-hash"
    assert metadata["study_distribution_days"] == 1
    assert metadata["study_max_adjustment_error"] == pytest.approx(0)
    assert (tmp_path / "VBMFX.json").read_text() == '{"original": true}'


def test_vbtlx_does_not_require_pre_inception_coverage():
    frame = history()
    frame["date"] = ["2001-11-12", "2001-11-13", "2023-03-17"]
    output = total_returns(frame, "VBTLX")
    assert output.date.min() == pd.Timestamp("2001-11-12")
    assert np.isnan(output.ret.iloc[0])
