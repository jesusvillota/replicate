"""Hand calculations for the Figure 1 available-case, asset-weighted means."""

import numpy as np
import pandas as pd
import pytest

from rebal.exhibits import pension


@pytest.fixture
def plans():
    return pd.DataFrame(
        [
            (1, 2003, 100, 0.4, 0.5),
            (2, 2003, 300, 0.8, np.nan),
            (3, 2003, 200, np.nan, 0.8),
            (1, 2004, 200, 0.6, 0.7),
            (2, 2004, 200, 0.4, 0.5),
        ],
        columns=pension.FIELDS,
    )


def test_weighting_missing_fields_counts_and_comparison(plans):
    yearly = pension.yearly_allocations(plans, end=2004)
    assert yearly.actual_share.tolist() == pytest.approx([0.7, 0.5])
    assert yearly.target_share.tolist() == pytest.approx([0.7, 0.6])
    assert yearly.plan_count.tolist() == [3, 2]
    assert yearly.actual_plan_count.tolist() == [2, 2]
    assert yearly.target_plan_count.tolist() == [2, 2]
    assert yearly.actual_missing_count.tolist() == [1, 0]
    assert yearly.target_missing_count.tolist() == [1, 0]
    assert yearly.invalid_assets_count.tolist() == [0, 0]
    values = pension.comparison_values(yearly)
    assert values.value.tolist() == pytest.approx([0.5, 0.7, 0.65])
    from rebal.paths import REPO_ROOT

    targets = pd.read_csv(REPO_ROOT / "docs/results/targets.csv")
    keys = ["exhibit", "column", "term", "stat"]
    pd.testing.assert_frame_equal(
        values[keys],
        targets.loc[targets.exhibit == "figure_1", keys].reset_index(drop=True),
    )


@pytest.mark.parametrize("assets", [np.nan, 0, -1, np.inf])
def test_invalid_assets_are_excluded_and_counted(plans, assets):
    plans["MktAssets_net"] = plans.MktAssets_net.astype(float)
    plans.loc[0, "MktAssets_net"] = assets
    yearly = pension.yearly_allocations(plans, end=2003).iloc[0]
    assert yearly.invalid_assets_count == 1
    assert yearly.actual_plan_count == yearly.target_plan_count == 1
    assert yearly.actual_share == pytest.approx(0.8)
    assert yearly.target_share == pytest.approx(0.8)


def test_equal_weights_and_reported_zero(plans):
    plans.loc[0, "EQTotal_Actl"] = 0
    yearly = pension.yearly_allocations(plans, end=2003).iloc[0]
    assert yearly.actual_share == pytest.approx(0.6)
    equal = pension.yearly_allocations(plans, end=2003, weighting="equal").iloc[0]
    assert equal.actual_share == pytest.approx(0.4)
    assert equal.target_share == pytest.approx(0.65)


def test_empty_year_and_missing_series_are_gaps(plans):
    plans.loc[plans.fy == 2004, "EQTotal_Trgt"] = np.nan
    yearly = pension.yearly_allocations(plans, end=2005)
    assert yearly.plan_count.tolist() == [3, 2, 0]
    assert yearly.target_plan_count.tolist() == [2, 0, 0]
    assert np.isnan(yearly.target_share.iloc[1])
    assert yearly.loc[2, ["actual_share", "target_share"]].isna().all()
    assert pension.comparison_values(yearly).value.iloc[2] == pytest.approx(0.7)


@pytest.mark.parametrize("effect", [0.025, 0.0])
def test_demo_planted_gap_and_zero_effect(effect):
    yearly = pension.yearly_allocations(pension.make_demo_allocations(effect))
    np.testing.assert_allclose(
        yearly.actual_share - yearly.target_share,
        effect * np.cos(np.pi * np.arange(20)),
        atol=1e-15,
    )
    assert yearly.plan_count.tolist() == [2, 2] + [3] * 18
    assert pension.comparison_values(yearly).value.tolist() == pytest.approx(
        [0.65 - effect, 0.65 + effect, 0.65]
    )


def test_outputs_are_plotted_values(tmp_path, monkeypatch):
    monkeypatch.setattr(pension, "output_dir", lambda kind: tmp_path)
    outputs = pension.run(demo=True)
    assert len(outputs) == 4 and all(path.is_file() for path in outputs)
    yearly = pd.read_csv(tmp_path / "figure_1_yearly.csv")
    pd.testing.assert_frame_equal(
        pd.read_csv(tmp_path / "figure_1.csv"), pension.comparison_values(yearly)
    )
    figure = pension.plot_allocations(yearly, demo=True)
    for line, field in zip(
        figure.axes[0].lines, ["actual_share", "target_share"], strict=True
    ):
        np.testing.assert_allclose(line.get_xdata(), yearly.fy)
        np.testing.assert_allclose(line.get_ydata(), yearly[field])
    assert (tmp_path / "figure_1.pdf").read_bytes().startswith(b"%PDF-")
    figure.clear()


def test_invalid_inputs(plans):
    with pytest.raises(ValueError, match="Duplicate"):
        pension.yearly_allocations(pd.concat([plans, plans]))
    plans.loc[0, "EQTotal_Actl"] = 65
    with pytest.raises(ValueError, match="fractions"):
        pension.yearly_allocations(plans)
    with pytest.raises(ValueError, match="start"):
        pension.yearly_allocations(plans, start=2022, end=2003)


def test_source_coverage_validation(plans, tmp_path, monkeypatch):
    monkeypatch.setattr(pension, "public_dir", lambda source: tmp_path)
    plans.to_csv(tmp_path / "ppd_allocations.csv", index=False)
    coverage = pd.DataFrame(
        {"date": ["2003-12-31", "2004-12-31"], "plan_count": [3, 2]}
    )
    coverage.to_csv(tmp_path / "ppd_coverage.csv", index=False)
    pd.testing.assert_frame_equal(pension.load_allocations(), plans)
    coverage.loc[0, "plan_count"] = 4
    coverage.to_csv(tmp_path / "ppd_coverage.csv", index=False)
    with pytest.raises(ValueError, match="coverage"):
        pension.load_allocations()
