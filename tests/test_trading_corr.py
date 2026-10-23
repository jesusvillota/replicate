import json

import numpy as np
import pandas as pd
import pytest

from rebal.exhibits import trading_corr as tc
from rebal.io import load_signals


def test_planted_weekly_correlation_and_lag_direction():
    rng = np.random.default_rng(5028)
    dates = pd.date_range("2007-01-02", periods=1000, freq="W-TUE")
    x = rng.normal(size=len(dates))
    signals = pd.DataFrame(
        {"date": dates, "threshold": x, "calendar": rng.normal(size=len(x))}
    )
    # A position level at t changes in response to the signal at t-1.
    increments = np.r_[
        0, 0.4 * x[:-1] + np.sqrt(1 - 0.4**2) * rng.normal(size=len(x) - 1)
    ]
    positions = pd.concat(
        [
            pd.DataFrame(
                {
                    "date": dates,
                    "market": market,
                    "oi": 100,
                    "hedgers": np.cumsum(increments) * 100 if market == "equity" else 0,
                }
            )
            for market in ("equity", "bond")
        ]
    )
    trading = tc.cftc_trading(positions, "hedgers")
    aligned = tc.align_trading(trading, signals, end="latest")
    result = tc.correlations(aligned).set_index(["term", "stat"]).value
    assert result["threshold", "value"] == pytest.approx(0.4, abs=0.06)
    assert abs(result["calendar", "value"]) < 0.07
    # Wrong direction: current signals cannot explain changes ending last week.
    assert abs(pd.Series(x[2:]).corr(pd.Series(increments[1:-1]))) < 0.07
    assert (aligned.signal_date < aligned.date).all()
    assert aligned.threshold.to_numpy() == pytest.approx(x[:-1])


def test_q_scales_each_leg_by_beginning_open_interest():
    dates = pd.to_datetime(["2007-01-02", "2007-01-09", "2007-01-23"])
    positions = pd.DataFrame(
        {
            "date": list(dates) * 2,
            "market": ["equity"] * 3 + ["bond"] * 3,
            "oi": [100, 200, 300, 50, 500, 500],
            "hedgers": [10, 30, 40, 5, 10, 20],
        }
    )
    actual = tc.cftc_trading(positions, "hedgers")
    assert actual.value.iloc[1] == pytest.approx(20 / 100 - 5 / 50)
    assert np.isnan(actual.value.iloc[2])  # two-week source gap


def test_ici_never_bridges_blocks_and_removes_between_block_means():
    dates = pd.to_datetime(
        [
            "2009-01-07",
            "2009-01-14",
            "2009-01-21",
            "2009-01-28",
            "2010-01-06",
            "2010-01-13",
            "2010-01-20",
            "2010-01-27",
        ]
    )
    x = np.array([0, 1, 2, 3, 100, 101, 102, 103])
    signals = pd.DataFrame({"date": dates, "threshold": x, "calendar": x})
    flows = pd.DataFrame(
        {
            "date": dates,
            "domestic_equity": [999, 0, -1, -2, 999, 100, 99, 98],
            "taxable_bond": 0,
            "municipal_bond": 0,
        }
    )
    aligned = tc.align_trading(tc.ici_trading(flows), signals, end="latest")
    assert len(aligned) == 6
    assert not aligned.date.isin(dates[[0, 4]]).any()
    assert (aligned.date - aligned.signal_date).dt.days.eq(7).all()
    result = (
        tc.correlations(aligned, within_blocks=True).set_index(["term", "stat"]).value
    )
    assert result["threshold", "value"] == pytest.approx(-1)
    assert result["threshold", "nobs"] == 6
    assert tc.correlations(aligned).iloc[0].value > 0.99


def test_ici_uses_domestic_equity_and_both_bond_categories():
    raw = pd.DataFrame(
        {
            "date": ["2009-01-07", "2009-01-15", "2009-01-24"],
            "total_equity": 999,
            "domestic_equity": 10,
            "taxable_bond": 3,
            "municipal_bond": 2,
        }
    )
    result = tc.ici_trading(raw)
    assert result.value.tolist() == [5, 5, 5]
    assert result.block.tolist() == [0, 0, 1]


def test_ltpos_preserves_mean_daily_changes_and_uses_prior_friday():
    raw = pd.DataFrame(
        {
            "date": pd.to_datetime(["2009-01-09", "2009-01-16"] * 2),
            "period_start": pd.to_datetime(["2009-01-05", "2009-01-12"] * 2),
            "market": ["equity"] * 2 + ["bond"] * 2,
            "asset_managers": [30, 35, 10, 12],
        }
    )
    trading = tc.ltpos_trading(raw, "asset_managers")
    assert trading.value.tolist() == [20, 23]
    dates = pd.bdate_range("2009-01-01", "2009-01-16")
    signals = pd.DataFrame(
        {"date": dates, "threshold": np.arange(len(dates)), "calendar": 1}
    )
    aligned = tc.align_trading(trading, signals)
    assert aligned.threshold.tolist() == [1, 6]
    assert (
        aligned.signal_date < raw.period_start.iloc[:2].reset_index(drop=True)
    ).all()


def test_signal_sampling_is_backward_and_week_mean_is_trailing():
    dates = pd.bdate_range("2009-01-01", "2009-01-16")
    signals = pd.DataFrame(
        {"date": dates, "threshold": np.arange(len(dates)), "calendar": 1}
    )
    refs = pd.Series(pd.to_datetime(["2009-01-11", "2009-02-01"]))
    assert tc.sample_signals(signals, refs).threshold.iloc[0] == 6
    assert tc.sample_signals(signals, refs, "mean").threshold.iloc[0] == 4
    assert np.isnan(tc.sample_signals(signals, refs).threshold.iloc[1])
    with pytest.raises(ValueError, match="lag_weeks"):
        tc.align_trading(
            pd.DataFrame({"date": dates, "value": 1, "block": 0}), signals, lag_weeks=-1
        )


def test_demo_build_has_five_groups_and_no_ancerno():
    signals = load_signals(demo=True)
    frame, metadata = tc.build_figure(signals, *tc.demo_inputs(signals))
    assert list(frame.columns) == ["exhibit", "column", "term", "stat", "value"]
    assert set(frame.column) == set(tc.GROUPS)
    assert len(frame) == 20
    values = frame[frame.stat == "value"]
    assert values.value.between(-1, 1).all()
    assert (
        values[values.column.isin(["cftc_hedgers", "ltpos_asset_managers", "ici"])]
        .value.lt(-0.25)
        .all()
    )
    assert (
        values[values.column.isin(["cftc_speculators", "ltpos_leveraged_funds"])]
        .value.gt(0.25)
        .all()
    )
    assert len(metadata["ici"]["blocks"]) > 1


def test_demo_run_writes_comparison_csv_pdf_and_block_counts(tmp_path, monkeypatch):
    monkeypatch.setattr(tc, "output_dir", lambda kind: tmp_path)
    paths = tc.run(demo=True)
    assert len(paths) == 3
    assert paths[1].read_bytes().startswith(b"%PDF")
    frame = pd.read_csv(paths[0])
    assert set(frame.column) == set(tc.GROUPS)
    metadata = json.loads(paths[2].read_text())
    for block in metadata["diagnostics"]["ici"]["blocks"]:
        stats = block["statistics"]
        assert {row["term"] for row in stats} == set(tc.TERMS)
        assert all(
            row["value"] == block["source_nobs"] - 1
            for row in stats
            if row["stat"] == "nobs"
        )


@pytest.mark.parametrize(
    "contract,equity_code,suffix",
    [
        ("emini", "13874A", "ES"),
        ("large", "138741", "SP"),
    ],
)
@pytest.mark.parametrize("report", ["legacy", "tff"])
def test_source_headers_and_contract_selection(
    tmp_path, monkeypatch, contract, equity_code, suffix, report
):
    monkeypatch.setattr(tc, "public_dir", lambda source: tmp_path)
    monkeypatch.setattr(tc, "licensed_dir", lambda source: tmp_path)
    raw = pd.DataFrame(
        {"date": ["2009-01-06"] * 3, "market_code": ["043602", "13874A", "138741"]}
    )
    if report == "legacy":
        raw["Open Interest (All)"] = 100
        for prefix in ["Commercial", "Noncommercial"]:
            raw[f"{prefix} Positions-Long (All)"] = [10, 20, 30]
            raw[f"{prefix} Positions-Short (All)"] = 2
        filename = "cot_legacy.csv"
    else:
        raw["Open_Interest_All"] = 100
        for prefix in ["Dealer", "Asset_Mgr", "Lev_Money", "Other_Rept"]:
            raw[f"{prefix}_Positions_Long_All"] = [10, 20, 30]
            raw[f"{prefix}_Positions_Short_All"] = 2
        filename = "tff.csv"
    raw.to_csv(tmp_path / filename, index=False)
    pd.DataFrame(
        {
            "date": ["2009-01-09"] * 3,
            "period_start": ["2009-01-05"] * 3,
            "market": [
                "CBT 10 Year Treasury (TY)",
                "CME E-Mini S&P (ES)",
                "CME S&P (SP)",
            ],
            "asset_managers_net_change": [1, 2, 3],
            "leveraged_funds_net_change": [4, 5, 6],
        }
    ).to_csv(tmp_path / "ltpos.csv", index=False)
    pd.DataFrame({"date": ["2009-01-07"], "domestic_equity": [1]}).to_csv(
        tmp_path / "ici_weekly_flows.csv", index=False
    )
    positions, flows, _ = tc.read_inputs(contract, report)
    assert set(positions.market) == {"equity", "bond"}
    expected = 18 if equity_code == "13874A" else 28
    assert positions.loc[positions.market == "equity", "hedgers"].item() == expected
    assert positions.loc[
        positions.market == "equity", "speculators"
    ].item() == expected * (3 if report == "tff" else 1)
    assert flows.loc[flows.market == "equity", "asset_managers"].item() == (
        2 if suffix == "ES" else 3
    )


def test_missing_pairs_and_end_boundary():
    dates = pd.date_range("2009-01-07", periods=5, freq="W-WED")
    signals = pd.DataFrame(
        {"date": dates, "threshold": [0, 1, np.nan, 3, 4], "calendar": range(5)}
    )
    trading = pd.DataFrame({"date": dates, "value": [1, 2, 3, 4, 5], "block": 0})
    aligned = tc.align_trading(trading, signals, end="2009-01-28")
    assert aligned.date.max() == pd.Timestamp("2009-01-28")
    result = tc.correlations(aligned).set_index(["term", "stat"]).value
    assert result["threshold", "nobs"] == 2
    assert result["calendar", "nobs"] == 3
    assert result["threshold", "value"] == pytest.approx(1)
