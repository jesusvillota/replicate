"""Guard sample boundaries, index identity, raw preservation and rate recovery."""

import hashlib
import json
from datetime import date
from unittest.mock import Mock

import pandas as pd
import pytest
from yfinance.exceptions import YFRateLimitError

from rebal.fetch import msci, yahoo


def history(dates=("1997-09-10", "2023-03-17")):
    return pd.DataFrame(
        {
            "Open": 100,
            "High": 103,
            "Low": 99,
            "Close": 101,
            "Adj Close": 98.5,
            "Volume": 42,
        },
        index=pd.DatetimeIndex(dates, tz="America/New_York"),
    )


def test_yahoo_retains_raw_and_distinct_prices_after_rate_limit(
    tmp_path, monkeypatch, capsys
):
    raw = b'{ "chart": {"original":true} }\n'
    attempts = []

    def ticker(symbol, session):
        def read(**kwargs):
            attempts.append(kwargs)
            if len(attempts) <= 2:
                raise YFRateLimitError()
            session.raw = raw
            return history()

        return Mock(history=read)

    monkeypatch.setattr(yahoo.yf, "Ticker", ticker)
    wait = Mock()
    monkeypatch.setattr(yahoo, "sleep", wait)
    path = yahoo.fetch_ticker("^SP500TR", tmp_path)
    assert path.with_suffix(".json").read_bytes() == raw
    output = pd.read_csv(path)
    assert output["date"].tolist() == ["1997-09-10", "2023-03-17"]
    assert output["Close"].tolist() == [101, 101]
    assert output["Adj Close"].tolist() == [98.5, 98.5]
    assert [call.args[0] for call in wait.call_args_list] == [1, 2]
    assert all(options["auto_adjust"] is False for options in attempts)
    assert all(options["period"] == "max" for options in attempts)
    metadata = json.loads(path.with_suffix(".metadata.json").read_text())
    assert metadata["raw_sha256"] == hashlib.sha256(raw).hexdigest()
    assert (
        sum(line.startswith("OK ") for line in capsys.readouterr().out.splitlines())
        == 1
    )


def test_yahoo_rate_limit_exhaustion_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(
        yahoo.yf,
        "Ticker",
        Mock(return_value=Mock(history=Mock(side_effect=YFRateLimitError()))),
    )
    monkeypatch.setattr(yahoo, "sleep", Mock())
    with pytest.raises(YFRateLimitError):
        yahoo.fetch_ticker("^SP500TR", tmp_path, retries=1)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    "ticker,dates",
    [
        ("^SP500TR", ("1997-09-11", "2023-03-17")),
        ("^SP500TR", ("1997-09-10", "2023-03-16")),
        ("ES=F", ("2002-01-01", "2023-03-17")),
        ("ZN=F", ("2002-01-01", "2023-03-17")),
        ("^MOVE", ("2023-03-17", "2023-03-17")),
        ("^MOVE", ("2023-03-17", "2023-03-16")),
    ],
)
def test_yahoo_rejects_missing_boundaries_and_bad_dates(ticker, dates):
    with pytest.raises(ValueError):
        yahoo.validate_history(history(dates), ticker)


@pytest.mark.parametrize("column", ["Close", "Adj Close"])
def test_yahoo_rejects_missing_price(column):
    frame = history()
    frame.loc[frame.index[0], column] = float("nan")
    with pytest.raises(ValueError, match="missing Close or Adj Close"):
        yahoo.validate_history(frame, "^SP500TR")


def workbook():
    return pd.DataFrame(
        [
            [None, None],
            ["Index Level :", "Net"],
            ["Currency :", "USD"],
            ["Date", msci.INDEX_NAME],
            ["Sep 10, 1997", "100.125"],
            ["Sep 11, 1997", "101.250"],
            [None, None],
            ["Copyright MSCI Inc.", None],
        ]
    )


def test_msci_parses_levels_and_excludes_license(monkeypatch, tmp_path):
    monkeypatch.setattr(msci.pd, "read_excel", lambda *args, **kwargs: workbook())
    frame = msci.parse_workbook(
        tmp_path / "raw.xls", date(1997, 1, 1), date(2023, 3, 17)
    )
    assert frame[msci.STEM].tolist() == [100.125, 101.25]
    assert frame.date.dt.strftime("%Y-%m-%d").tolist() == ["1997-09-10", "1997-09-11"]


@pytest.mark.parametrize(
    "row,value",
    [
        (1, "Gross"),
        (2, "EUR"),
        (3, "WORLD ex USA Standard (Large+Mid Cap)"),
        (4, "not a number"),
        (5, None),
    ],
)
def test_msci_rejects_wrong_identity_or_bad_level(row, value, monkeypatch, tmp_path):
    sheet = workbook()
    sheet.iloc[row, 1] = value
    monkeypatch.setattr(msci.pd, "read_excel", lambda *args, **kwargs: sheet)
    with pytest.raises(ValueError):
        msci.parse_workbook(tmp_path / "raw.xls", date(1997, 1, 1), date(2023, 3, 17))


@pytest.mark.parametrize(
    "dates",
    [
        ["Sep 10, 1997", "Sep 10, 1997"],
        ["Sep 11, 1997", "Sep 10, 1997"],
        ["bad date", "Sep 11, 1997"],
        ["Sep 10, 1996", "Sep 11, 1997"],
    ],
)
def test_msci_rejects_bad_dates(dates, monkeypatch, tmp_path):
    sheet = workbook()
    sheet.iloc[4:6, 0] = dates
    monkeypatch.setattr(msci.pd, "read_excel", lambda *args, **kwargs: sheet)
    with pytest.raises(ValueError):
        msci.parse_workbook(tmp_path / "raw.xls", date(1997, 1, 1), date(2023, 3, 17))
