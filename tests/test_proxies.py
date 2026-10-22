"""Offline pricing, repair, excess-return and comparison invariants."""

import math

import numpy as np
import pandas as pd
import pytest

from rebal import proxies


def flat_curve(index, yield_percent=4.0):
    curve = pd.DataFrame(
        {f"SVENY{i:02}": yield_percent for i in range(1, 11)}, index=index
    )
    curve["SVENPY10"] = 200 * np.expm1(yield_percent / 200)
    for i in range(4):
        curve[f"BETA{i}"] = yield_percent if i == 0 else 0.0
    curve["TAU1"], curve["TAU2"] = 1.0, 2.0
    return curve


def test_zero_coupon_matches_hand_calculation_with_weekend_carry():
    dates = pd.to_datetime(["2020-01-03", "2020-01-06"])
    yields = pd.Series([4.0, 4.1], index=dates)
    rf = pd.Series(0.0001, index=dates)
    result = proxies.zero_coupon_return(yields, 10, rf)
    previous = math.exp(-10 * 0.04)
    today = math.exp(-(10 - 3 / 365.25) * 0.041)
    assert pd.isna(result.iloc[0])
    assert result.iloc[1] == pytest.approx(today / previous - 1 - 0.0001)
    assert result.iloc[1] < 0  # Higher yield lowers the held bond's price.


@pytest.mark.parametrize(
    "candidate,maturity", [(proxies.ty_zero_10, 10), (proxies.ty_zero_65, 6.5)]
)
def test_zero_candidates_age_on_sloping_curve(candidate, maturity):
    dates = pd.to_datetime(["2020-01-06", "2020-01-07"])
    curve = flat_curve(dates)
    for i in range(1, 11):
        curve[f"SVENY{i:02}"] = i / 2
    rf = pd.Series(0.0002, index=dates)
    n = maturity
    delta = 1 / 365.25
    expected = (
        math.exp(n * (n / 2 / 100) - (n - delta) * ((n - delta) / 2 / 100)) - 1 - 0.0002
    )
    assert candidate(curve, rf).iloc[1] == pytest.approx(expected)


def test_par_bond_keeps_yesterdays_coupon_when_yields_move():
    dates = pd.to_datetime(["2020-01-06", "2020-01-07"])
    curve = flat_curve(dates)
    curve.loc[dates[1], ["BETA0", "SVENPY10"]] = [5.0, 200 * math.expm1(0.05 / 2)]
    coupon = math.expm1(0.04 / 2)
    cf = [coupon] * 19 + [coupon + 1]
    previous = sum(c * math.exp(-0.04 * (i + 1) / 2) for i, c in enumerate(cf))
    today = sum(
        c * math.exp(-0.05 * ((i + 1) / 2 - 1 / 365.25)) for i, c in enumerate(cf)
    )
    result = proxies.ty_par_10(curve, pd.Series(0.0001, index=dates))
    assert previous == pytest.approx(1)
    assert result.iloc[1] == pytest.approx(today / previous - 1 - 0.0001)
    assert result.iloc[1] < -0.07


def test_fitted_yield_allows_only_inactive_missing_second_tau():
    dates = pd.bdate_range("2020-01-01", periods=2)
    curve = flat_curve(dates)
    curve["TAU2"] = np.nan
    result = proxies.fitted_yield(curve, np.ones((2, 3)))
    assert np.allclose(result, 0.04)
    curve["BETA3"] = 1.0
    assert np.isnan(proxies.fitted_yield(curve, np.ones((2, 3)))).all()


@pytest.mark.parametrize("candidate", [proxies.es_futures, proxies.ty_futures])
def test_planted_noncalendar_jump_is_removed(candidate):
    dates = pd.bdate_range("2020-01-06", periods=4)
    close = pd.Series([100.0, 101.0, 151.5, 153.015], index=dates)
    reference = pd.Series(0.01, index=dates)
    result = candidate(close, reference)
    assert result.iloc[1:].to_numpy() == pytest.approx([0.01, 0.01, 0.01])
    assert close.pct_change(fill_method=None).iloc[2] == pytest.approx(0.5)
    assert pd.isna(result.iloc[0])


def test_calendar_detects_small_roll_and_preserves_other_days():
    dates = pd.to_datetime(["2023-03-08", "2023-03-09", "2023-03-20", "2023-03-21"])
    close = pd.Series([100, 100.5, 101, 101.505], index=dates)
    reference = pd.Series(0.001, index=dates)
    flags = proxies.roll_days(close, reference, jump=0.02)
    assert flags.tolist() == [False, True, True, False]
    repaired = proxies.es_futures(close, reference)
    assert repaired.iloc[1:3].to_numpy() == pytest.approx([0.001, 0.001])
    assert repaired.iloc[3] == pytest.approx(0.005)


def test_roll_repair_does_not_create_preinception_history_or_fill_missing_reference():
    dates = pd.bdate_range("2023-03-13", periods=4)
    close = pd.Series([np.nan, np.nan, 100, 110], index=dates)
    reference = pd.Series([0.001, 0.001, 0.001, np.nan], index=dates)
    assert proxies.es_futures(close, reference).isna().all()


@pytest.mark.parametrize("candidate", [proxies.es_spy, proxies.ty_ief])
def test_cash_return_subtracts_rf(candidate):
    dates = pd.bdate_range("2020-01-06", periods=3)
    ret = pd.Series([0.01, -0.02, 0.03], index=dates)
    rf = pd.Series([0.001, 0.002, np.nan], index=dates)
    result = candidate(ret, rf)
    assert result.iloc[:2].to_numpy() == pytest.approx([0.009, -0.022])
    assert pd.isna(result.iloc[2])


def test_equity_index_subtracts_rf_once_and_futures_never_do():
    dates = pd.bdate_range("2020-01-06", periods=3)
    close = pd.Series([100, 101, 102.01], index=dates)
    rf = pd.Series(0.001, index=dates)
    assert proxies.es_total_return(close, rf).iloc[1] == pytest.approx(0.009)
    for candidate in [proxies.es_futures, proxies.ty_futures]:
        assert candidate(close, pd.Series(0.01, index=dates)).iloc[1] == pytest.approx(
            0.01
        )
    ret = close.pct_change(fill_method=None)
    pd.testing.assert_series_equal(proxies.excess_return(ret, rf, futures=True), ret)


def test_missing_quote_is_not_a_zero_return_and_invalid_maturity_fails():
    dates = pd.bdate_range("2020-01-06", periods=4)
    curve = flat_curve(dates)
    curve.iloc[1] = np.nan
    rf = pd.Series(0, index=dates)
    for candidate in [proxies.ty_zero_10, proxies.ty_zero_65, proxies.ty_par_10]:
        result = candidate(curve, rf)
        assert result.iloc[:3].isna().all()
        assert result.iloc[3] == pytest.approx(math.expm1(0.04 / 365.25))
    with pytest.raises(ValueError, match="maturity"):
        proxies.zero_coupon_return(curve.SVENY10, 0, rf)


def test_metrics_match_hand_oracle_and_keep_lead_lag_session_grid():
    dates = pd.bdate_range("2021-01-04", periods=8)
    b = pd.Series([0.01, -0.02, 0.03, np.nan, 0.01, -0.04, 0.02, 0.005], index=dates)
    p = pd.Series([0.015, -0.01, 0.05, 0.03, -0.01, -0.03, 0.01, 0.004], index=dates)
    benchmark = pd.DataFrame({"ES": b, "TY": b / 2})
    m = proxies.metric_rows({"E1": p, "T1": p / 2}, benchmark).loc["E1"]
    paired = pd.concat([p, b], axis=1).dropna()
    error = paired.iloc[:, 0] - paired.iloc[:, 1]
    assert m.n == 7
    assert m.correlation == pytest.approx(p.corr(b))
    assert m.beta == pytest.approx(paired.cov().iloc[0, 1] / paired.iloc[:, 1].var())
    assert m.tracking_error == pytest.approx(error.std(ddof=1) * math.sqrt(252))
    assert m.mean_bp_day == pytest.approx(error.mean() * 10000)
    clean = b.notna()
    assert m.lead == pytest.approx(p[clean].corr(b.shift(-1)[clean]))
    assert m.lag == pytest.approx(p[clean].corr(b.shift(1)[clean]))
    assert m.mtd_correlation == pytest.approx(
        (0.24 * p[clean].cumsum()).corr(0.24 * b[clean].cumsum())
    )


def test_month_to_date_resets_each_month():
    dates = pd.to_datetime(["2021-01-28", "2021-01-29", "2021-02-01", "2021-02-02"])
    p = pd.Series([0.01, -0.02, 0.03, -0.01], index=dates)
    b = pd.Series([0.02, -0.03, -0.02, 0.01], index=dates)
    row = proxies.metric_rows(
        {"E1": p, "T1": p / 2}, pd.DataFrame({"ES": b, "TY": b / 2})
    ).loc["E1"]
    expected = pd.Series([0.01, -0.01, 0.03, 0.02]).corr(
        pd.Series([0.02, -0.01, -0.02, -0.01])
    )
    assert row.mtd_correlation == pytest.approx(expected)


def test_demo_recovers_planted_proxy_and_zero_effect():
    data = proxies.demo_inputs()
    candidates, benchmark, _ = proxies.build_candidates(data)
    metrics = proxies.metric_rows(candidates, benchmark)
    assert len(metrics) == 8 + 15
    assert metrics.loc["T3", "correlation"] > 0.99
    assert metrics.loc["E1/T3", "correlation"] > 0.99
    assert metrics.loc["T1", "tracking_error"] > metrics.loc["T3", "tracking_error"]
    rng = np.random.default_rng(15)
    independent = pd.Series(
        rng.normal(0, 0.01, len(data["rf"])), index=data["rf"].index
    )
    zero = proxies.metric_rows({"E1": independent, "T1": candidates["T3"]}, benchmark)
    assert abs(zero.loc["E1", "correlation"]) < 0.05
    clean = benchmark.ES.notna()
    pd.testing.assert_series_equal(
        candidates["E3"].reindex(benchmark.index)[clean],
        benchmark.ES[clean],
        check_names=False,
    )


def test_demo_report_has_every_candidate_pair_and_recommendation(tmp_path):
    path = tmp_path / "comparison.md"
    metrics = proxies.write_report(
        proxies.demo_inputs(), [], "Synthetic RF", path, demo=True
    )
    text = path.read_text()
    assert "## Recommendation for DEC-001" in text
    assert "6.5-year maturity" in text
    assert "E1/T3" in text
    assert "Synthetic demo only" in text
    for candidate in metrics.index:
        assert f"| {candidate} |" in text
    for unavailable in ["E4", "T4", "T7"]:
        assert f"**{unavailable}**" in text


@pytest.mark.parametrize("french_available", [True, False])
def test_load_inputs_scales_french_rf_or_uses_lagged_dtb3(
    tmp_path, monkeypatch, french_available
):
    dates = pd.to_datetime(["2020-01-03", "2020-01-06", "2020-01-07"])
    monkeypatch.setattr(proxies, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        proxies, "licensed_dir", lambda source: tmp_path / "licensed" / source
    )
    for folder in [
        "data/public/gsw",
        "data/public/french",
        "data/public/fred",
        "licensed/crsp",
        "licensed/yahoo",
    ]:
        (tmp_path / folder).mkdir(parents=True)
    flat_curve(dates).rename_axis("date").to_csv(
        tmp_path / "data/public/gsw/feds200628.csv"
    )
    pd.DataFrame({"date": dates, "RF": [0.01, 0.02, 0.03]}).to_csv(
        tmp_path / "data/public/french/F-F_Research_Data_Factors_daily.csv", index=False
    )
    pd.DataFrame({"date": dates, "DTB3": [4.0, 8.0, 9.0]}).to_csv(
        tmp_path / "data/public/fred/DTB3.csv", index=False
    )
    if not french_available:
        (tmp_path / "data/public/french/F-F_Research_Data_Factors_daily.csv").unlink()
    pd.concat(
        [
            pd.DataFrame({"date": dates, "ticker": ticker, "ret": [0.01, 0.02, 0.03]})
            for ticker in ["SPY", "IEF"]
        ]
    ).to_parquet(tmp_path / "licensed/crsp/etf_daily.parquet", index=False)
    for ticker in ["^SP500TR", "ES=F", "ZN=F"]:
        pd.DataFrame({"date": dates, "Close": [100, 101, 102]}).to_csv(
            tmp_path / f"licensed/yahoo/{ticker}.csv", index=False
        )
    data, paths, note = proxies.load_inputs()
    assert len(paths) == 6
    if french_available:
        assert data["rf"].to_numpy() == pytest.approx([0.0001, 0.0002, 0.0003])
        assert "French" in note
    else:
        assert pd.isna(data["rf"].iloc[0])
        assert data["rf"].iloc[1] == pytest.approx(
            (1 / (1 - 0.04 * 91 / 360)) ** (3 / 91) - 1
        )
        assert data["rf"].iloc[2] == pytest.approx(
            (1 / (1 - 0.08 * 91 / 360)) ** (1 / 91) - 1
        )
        assert "lagged" in note
