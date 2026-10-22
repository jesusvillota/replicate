"""CFTC source preservation and market/period validation."""

import csv
import io
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import pytest

from rebal.fetch import cftc
from rebal.fetch.common import summarize


def test_panel_summary_checks_dates_within_market(tmp_path, capsys):
    path = tmp_path / "panel.csv"
    pd.DataFrame({"date": ["2023-01-03"] * 2, "market": ["A", "B"]}).to_csv(
        path, index=False
    )
    summarize(path, "date", key_cols=("market",))
    assert "rows=2" in capsys.readouterr().out
    with pytest.raises(ValueError, match="duplicate dates"):
        summarize(path, "date")
    pd.DataFrame(
        {"date": ["2023-01-03", "2023-01-03 12:00"], "market": ["A", "A"]}
    ).to_csv(path, index=False)
    with pytest.raises(ValueError):
        summarize(path, "date", key_cols=("market",))


@pytest.mark.parametrize(
    "report,name,date_col,code_col,when",
    [
        (
            "cot_legacy",
            "Market and Exchange Names",
            "As of Date in Form YYYY-MM-DD",
            "CFTC Contract Market Code",
            "1997-01-07",
        ),
        (
            "tff",
            "Market_and_Exchange_Names",
            "Report_Date_as_YYYY-MM-DD",
            "CFTC_Contract_Market_Code",
            "6/13/2006 12:00:00 AM",
        ),
    ],
)
def test_zip_parser_preserves_codes_columns_and_values(
    tmp_path, report, name, date_col, code_col, when
):
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow([name, date_col, code_col, " source field "])
    writer.writerow(["10-YEAR U.S. TREASURY NOTES", when, "043602 ", "00012"])
    writer.writerow(["S&P 500 STOCK INDEX", when, "138741", "."])
    writer.writerow(["CORN", when, "002602", "123"])
    path = tmp_path / "history.zip"
    with ZipFile(path, "w") as archive:
        archive.writestr("Annual.TXT", stream.getvalue())
    result = cftc.read_markets(path, report)
    assert list(result.market_code) == ["043602", "138741"]
    assert result.iloc[0][code_col] == "043602 "
    assert list(result["source field"]) == ["00012", "."]
    assert list(result.columns) == [
        "date",
        "market_code",
        name,
        date_col,
        code_col,
        "source field",
    ]
    assert result.date.iloc[0] == (
        "1997-01-07" if report == "cot_legacy" else "2006-06-13"
    )


def test_market_code_name_mismatch_fails(tmp_path):
    path = tmp_path / "wrong.zip"
    with ZipFile(path, "w") as archive:
        archive.writestr(
            "annual.txt",
            "Market and Exchange Names,As of Date in Form YYYY-MM-DD,CFTC Contract Market Code\nCORN,2023-01-03,043602\n",
        )
    with pytest.raises(ValueError, match="unexpected market name"):
        cftc.read_markets(path, "cot_legacy")


def test_committed_positioning_preserves_published_subset():
    directory = Path(__file__).resolve().parents[1] / "data/public/cftc"
    for report, names in {
        "cot_legacy": ["deacot1997.zip", "deacot2023.zip"],
        "tff": ["fin_fut_txt_2006_2016.zip", "fut_fin_txt_2023.zip"],
    }.items():
        actual = pd.read_csv(
            directory / f"{report}.csv", dtype=str, keep_default_na=False
        )
        for name in names:
            expected = (
                cftc.read_markets(directory / name, report)
                .sort_values(["date", "market_code"])
                .reset_index(drop=True)
            )
            subset = actual.loc[
                actual.date.between(expected.date.min(), expected.date.max())
            ].reset_index(drop=True)
            pd.testing.assert_frame_equal(subset, expected)
        cftc.validate_report(actual, report, int(actual.date.max()[:4]))
        with pytest.raises(ValueError, match="duplicate"):
            cftc.validate_report(
                pd.concat([actual, actual.iloc[:1]]), report, int(actual.date.max()[:4])
            )
        with pytest.raises(ValueError, match="incomplete years"):
            cftc.validate_report(
                actual.loc[~actual.date.str.startswith("2023")],
                report,
                int(actual.date.max()[:4]),
            )


def test_ltpos_values_and_periods_match_original():
    directory = Path(__file__).resolve().parents[1] / "data/public/cftc"
    tidy = pd.read_csv(directory / "ltpos.csv")
    assert len(tidy) == 750
    assert tidy.groupby("market").size().eq(125).all()
    assert tidy.period_start.min() == "2009-01-05"
    assert tidy.date.max() == "2011-05-27"
    assert not tidy.duplicated(["market", "date"]).any()
    with (directory / "lgtraderpos-csv.csv").open(newline="") as source:
        raw = list(csv.reader(source))
    for offset in (324, 336, 348, 384, 396, 408):
        market = raw[0][offset]
        actual = (
            tidy.loc[tidy.market == market].sort_values("date").reset_index(drop=True)
        )
        for i, row in enumerate(raw[3:]):
            assert actual.date[i] == pd.to_datetime(row[offset + 1]).strftime(
                "%Y-%m-%d"
            )
            for group, col in zip(
                ("dealers", "asset_managers", "leveraged_funds", "other_reportables"),
                (2, 4, 6, 8),
                strict=True,
            ):
                buys, sells = (
                    float(x.replace(",", ""))
                    for x in row[offset + col : offset + col + 2]
                )
                assert actual[f"{group}_buys"][i] == buys
                assert actual[f"{group}_sells"][i] == sells
                assert actual[f"{group}_net_change"][i] == buys - sells


def test_all_public_cftc_files_below_limit():
    directory = Path(__file__).resolve().parents[1] / "data/public/cftc"
    assert all(path.stat().st_size < 20_000_000 for path in directory.iterdir())
