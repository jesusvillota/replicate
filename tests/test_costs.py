"""Independent synthetic checks of prices, executed trades and cost outputs."""

import json

import numpy as np
import pandas as pd
import pytest

from rebal.demo import make_panel
from rebal.exhibits import costs
from rebal.regress import dated
from rebal.signals import build, simulate_calendar, simulate_threshold


@pytest.fixture(scope="module")
def inputs():
    panel = make_panel()
    p = dated(panel)
    signals = build(p.r_es, p.r_ty, r_sp500tr=p.r_sp500tr)
    return panel, signals


def plant(signals, beta, noise=0):
    """Generate the next-day equation independently of the estimator."""
    frame = signals.copy()
    rng = np.random.default_rng(72)
    response = rng.normal(0, noise, len(frame))
    for t in range(252, len(frame) - 1):
        response[t + 1] += (
            beta * frame.calendar.iloc[t] * frame.week4.iloc[t]
            + 0.0001 * frame.momentum.iloc[t]
            + 0.02 * response[t]
        )
    frame["ret"] = response
    return frame


@pytest.fixture(scope="module")
def zero_result(inputs):
    panel, signals = inputs
    return costs.estimate(panel, plant(signals, 0), n_sims=20)


@pytest.fixture(scope="module")
def planted_result(inputs):
    panel, signals = inputs
    return costs.estimate(panel, plant(signals, -0.39), n_sims=20)


def values(result):
    return result[0].set_index("item").value


def test_paper_worked_example_is_about_five_bps():
    # A 1% weight deviation predicts a 0.39% move on 1% of the portfolio.
    portfolio_loss_per_trade = 0.0039 * 0.01
    assert costs.annual_cost(-0.39, 0.01, 12) == pytest.approx(
        portfolio_loss_per_trade * 12 * 10_000
    )
    assert costs.annual_cost(-0.39, 0.01, 12) == pytest.approx(5, abs=0.5)
    assert costs.annual_cost(-0.39, 0.02, 12) == pytest.approx(18.72)
    assert costs.annual_cost(0.39, 0.01, 12) == pytest.approx(-4.68)


def test_zero_price_impact_costs(zero_result):
    estimates = zero_result[0]
    annual = estimates.loc[estimates.unit == "bps/year"]
    impact_costs = annual.loc[
        ~annual.item.str.startswith(("utility_", "random_tracking"))
    ]
    assert np.max(np.abs(impact_costs.value)) < 0.01


def test_planted_calendar_equals_impact_size_times_twelve(inputs, planted_result):
    panel, _ = inputs
    p = dated(panel)
    trades = simulate_calendar(p.r_es, p.r_ty).trade
    selected = trades.loc["1997-09-10":"2023-03-17"]
    size = np.abs(selected[selected != 0]).mean()
    v = values(planted_result)
    assert v.calendar_impact == pytest.approx(-0.39, abs=1e-12)
    assert v.calendar_trade_size == pytest.approx(size)
    assert v.calendar == pytest.approx(0.39 * size**2 * 12 * 10_000, abs=1e-9)
    assert v.calendar_full_sample == pytest.approx(v.calendar, abs=1e-9)
    assert v.calendar_T_minus_4_impact == pytest.approx(-0.39, abs=1e-12)
    assert v.calendar_pre_2006_impact == pytest.approx(-0.39, abs=1e-12)
    assert v.calendar_post_2006_impact == pytest.approx(-0.39, abs=1e-12)


def test_random_distribution_zero_without_own_impact(zero_result, planted_result):
    assert abs(zero_result[1].cost_bps_year.mean()) < 0.01
    # Calendar controls remove the exactly planted institutional pressure.
    assert np.max(np.abs(planted_result[1].cost_bps_year)) < 1e-8
    assert np.isfinite(planted_result[1].tracking_error_bps_year).all()
    assert (planted_result[1].tracking_error_bps_year > 0).all()


def test_threshold_size_frequency_and_headline(inputs, planted_result):
    panel, _ = inputs
    p = dated(panel)
    v = values(planted_result)
    for i in (0, 10, 25):
        sim = simulate_threshold(p.r_es, p.r_ty, i / 1000).loc[
            "1997-09-10":"2023-03-17"
        ]
        executed = sim.trade.to_numpy()
        frequency = np.count_nonzero(executed) * 252 / len(sim)
        assert v[f"threshold_{i:03d}_trades"] == pytest.approx(frequency)
        assert v[f"threshold_{i:03d}_trade_size"] == pytest.approx(
            np.abs(executed[executed != 0]).mean()
        )
        expected = -v[f"threshold_{i:03d}_impact"] * 0.01**2 * frequency * 10_000
        assert v[f"threshold_{i:03d}_fixed_1pct"] == pytest.approx(expected)
    assert v.headline == pytest.approx(
        (v.calendar + v.threshold_fixed_1pct_average) / 2
    )
    assert v.dollar_cost_paper == pytest.approx(v.headline * 20e12 / 10_000)
    assert v.per_household_paper == pytest.approx(v.dollar_cost_paper / (2 / 3 * 127e6))
    assert v.dollar_cost_fed_z1 == pytest.approx(v.headline * 37.8e12 / 10_000)


def test_delta_zero_policy_is_explicit_and_keeps_raw_estimate(inputs, monkeypatch):
    panel, signals = inputs

    def impact(signals, panel, term, *args, **kwargs):
        # An unstable daily-reset slope must not be clipped or silently dropped.
        return (-8.0 if term == "thr_000" else -0.4), "test impact"

    monkeypatch.setattr(costs, "_fit", impact)
    included = costs.estimate(panel, signals, n_sims=1, delta_zero="include")
    # DEC-005: the default excludes zero from summaries, retaining its raw rows.
    excluded = costs.estimate(panel, signals, n_sims=1)
    inc, exc = values(included), values(excluded)
    for suffix in ("", "_fixed_1pct", "_impact", "_full_sample"):
        assert inc[f"threshold_000{suffix}"] == exc[f"threshold_000{suffix}"]
    assert inc.threshold_000_impact == -8.0
    fixed = np.array([inc[f"threshold_{i:03d}_fixed_1pct"] for i in range(26)])
    actual = np.array([inc[f"threshold_{i:03d}"] for i in range(26)])
    assert inc.threshold_fixed_1pct_average == pytest.approx(fixed.mean())
    assert exc.threshold_fixed_1pct_average == pytest.approx(fixed[1:].mean())
    assert exc.threshold_min == pytest.approx(actual[1:].min())
    assert exc.threshold_max == pytest.approx(actual[1:].max())
    assert exc.threshold_average == pytest.approx(actual[1:].mean())
    assert exc.headline == pytest.approx((exc.calendar + fixed[1:].mean()) / 2)
    assert exc.dollar_cost_paper == pytest.approx(exc.headline / 10_000 * 20e12)
    assert inc.headline > 2 * exc.headline
    assert "delta=0 included" in included[0].set_index("item").loc["headline", "note"]
    assert "delta=0 excluded" in excluded[0].set_index("item").loc["headline", "note"]
    for average, suffix in (
        ("threshold_full_sample_average", "_full_sample"),
        ("threshold_full_sample_fixed_1pct_average", "_fixed_1pct"),
    ):
        # The stub supplies identical conditional and interaction impacts.
        expected = np.mean([exc[f"threshold_{i:03d}{suffix}"] for i in range(1, 26)])
        assert exc[average] == pytest.approx(expected)
    assert exc.headline_full_sample == pytest.approx(exc.headline)
    monkeypatch.setattr("sys.argv", ["costs"])
    assert costs.parse_args().delta_zero == "exclude"
    monkeypatch.setattr("sys.argv", ["costs", "--delta-zero", "include"])
    assert costs.parse_args().delta_zero == "include"


def test_all_paper_items_and_finite_outputs(planted_result):
    frame, draws = planted_result
    required = {
        "calendar",
        "calendar_T_minus_4",
        "calendar_pre_2006",
        "calendar_post_2006",
        "calendar_full_sample",
        "threshold_average",
        "threshold_min",
        "threshold_max",
        "threshold_fixed_1pct_average",
        "threshold_full_sample_average",
        "headline",
        "headline_full_sample",
        "random_mean",
        "random_median",
        "random_p025",
        "random_p975",
        "random_tracking_error",
        "dollar_cost_paper",
        "per_household_paper",
        "dollar_cost_fed_z1",
        "per_household_fed_z1",
        "utility_buy_hold",
        "utility_threshold_025",
        "utility_calendar",
        "utility_threshold_minus_buy_hold",
        "utility_calendar_minus_buy_hold",
    } | {f"threshold_{i:03d}" for i in range(26)}
    assert required <= set(frame.item)
    assert list(frame.columns) == ["item", "value", "unit", "note"]
    assert frame.item.is_unique
    assert np.isfinite(frame.value).all()
    assert frame.note.str.len().min() > 0
    v = values(planted_result)
    assert v.random_p025 == pytest.approx(draws.cost_bps_year.quantile(0.025))
    assert v.random_p975 == pytest.approx(draws.cost_bps_year.quantile(0.975))


def test_returns_use_previous_close_weights():
    panel = pd.DataFrame({"r_es": [0.1, -0.2, 0.3], "r_ty": [0.01, 0.02, -0.03]})
    sim = pd.DataFrame({"w_pre": [0.99] * 3, "w_post": [0.7, 0.4, 0.9]})
    expected = np.array(
        [0.6 * 0.1 + 0.4 * 0.01, 0.7 * -0.2 + 0.3 * 0.02, 0.4 * 0.3 + 0.6 * -0.03]
    )
    np.testing.assert_allclose(costs.portfolio_returns(panel, sim), expected)


def test_utility_independent_buy_hold_path(inputs, planted_result):
    panel, _ = inputs
    p = dated(panel)
    eq, bd = p.r_es.to_numpy(), p.r_ty.to_numpy()
    equity_wealth = 0.6 * np.r_[1, np.cumprod(1 + eq[:-1])]
    bond_wealth = 0.4 * np.r_[1, np.cumprod(1 + bd[:-1])]
    start_weights = equity_wealth / (equity_wealth + bond_wealth)
    r = start_weights * eq + (1 - start_weights) * bd
    r = r[(p.index >= "1997-09-10") & (p.index <= "2023-03-17")]
    expected = 252 * (r.mean() - 1.5 * r.var(ddof=1)) * 10_000
    assert values(planted_result).utility_buy_hold == pytest.approx(expected)


def test_random_dates_reproducible_and_one_per_month(inputs, monkeypatch):
    panel, signals = inputs
    schedules = []
    real = costs.simulate_dates

    def record(eq, bd, dates):
        schedules.append(pd.DatetimeIndex(dates))
        return real(eq, bd, dates)

    monkeypatch.setattr(costs, "simulate_dates", record)
    first = costs.random_dates(panel, plant(signals, 0, noise=1e-7), n_sims=2)
    second = costs.random_dates(panel, plant(signals, 0, noise=1e-7), n_sims=2)
    pd.testing.assert_frame_equal(first, second)
    assert schedules[0].equals(schedules[2])
    assert not schedules[0].equals(schedules[1])
    for schedule in schedules:
        assert schedule.to_period("M").is_unique
        assert len(schedule) == len(pd.period_range("1997-09", "2023-03", freq="M"))
        # The selected dates include some last-week days; they are allowed.
        chosen = dated(signals).loc[schedule]
        assert chosen.week4.any()


def test_run_writes_outputs_and_lineage(inputs, monkeypatch, tmp_path):
    panel, _ = inputs
    monkeypatch.setattr(costs, "load_panel", lambda demo: panel)
    monkeypatch.setattr(costs, "output_dir", lambda kind: tmp_path)
    paths = costs.run(True, n_sims=2, end="latest", controls=True, assets=21.1e12)
    assert {p.name for p in paths} == {
        "costs.csv",
        "costs_comparison.csv",
        "figure_D5_comparison.csv",
        "figure_D5.csv",
        "figure_D5.pdf",
        "costs.metadata.json",
    }
    assert (tmp_path / "figure_D5.pdf").read_bytes().startswith(b"%PDF")
    assert len(pd.read_csv(tmp_path / "figure_D5.csv")) == 2
    metadata = json.loads((tmp_path / "costs.metadata.json").read_text())
    assert metadata["parameters"]["assets"] == 21.1e12
    assert metadata["parameters"]["controls"] is True
    assert metadata["parameters"]["delta_zero"] == "exclude"
    assert "decimal_trade_size**2" in metadata["cost_formula"]
    assert metadata["sample_end"].startswith("2023-12-29")


def test_invalid_parameters_fail(inputs):
    panel, signals = inputs
    with pytest.raises(ValueError, match="n_sims"):
        costs.random_dates(panel, signals, n_sims=0)
    with pytest.raises(ValueError, match="asset bases"):
        costs.estimate(panel, signals, assets=-1)
    with pytest.raises(ValueError, match="delta_zero"):
        costs.estimate(panel, signals, delta_zero="drop silently")


def test_planted_threshold_recovers_conditional_impact(inputs):
    panel, signals = inputs
    frame = plant(signals, 0)
    response = np.zeros(len(frame))
    for t in range(252, len(frame) - 1):
        response[t + 1] = (
            -0.4 * frame.thr_010.iloc[t]
            + 0.0001 * frame.momentum.iloc[t]
            + 0.02 * response[t]
        )
    frame["ret"] = response
    estimates, _ = costs.estimate(panel, frame, n_sims=2)
    v = estimates.set_index("item").value
    assert v.threshold_010_impact == pytest.approx(-0.4, abs=1e-12)
    expected = 0.4 * v.threshold_010_trade_size**2 * v.threshold_010_trades * 10_000
    assert v.threshold_010 == pytest.approx(expected, abs=1e-9)
    assert v.threshold_010_full_sample == pytest.approx(expected, abs=1e-9)
