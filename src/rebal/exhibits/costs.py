"""uv run python3 -m rebal.exhibits.costs --demo --n-sims 100
uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5

CLI Arguments:
--demo: synthetic panel and simulated signals, with outputs under output/demo/.
--n-sims: random monthly schedules (default 10,000, also in demo).
--seed: random-date seed (default 16).
--end: inclusive sample end, or latest (default 2023-03-17).
--controls: include the five macro controls from equation (4).
--assets: paper public equity/debt dollar base (default 20e12).
--fed-assets: Fed year-end 2022 retirement total (default 37.8e12).
--delta-zero: exclude (default) or include zero in Threshold summaries.

Reads rebal.io panel/signals and simulates portfolio trades. Writes costs.csv
(item,value,unit,note), figure_D5.csv (one cost and tracking error per draw),
figure_D5.pdf and JSON lineage. Positive costs denote losses, in annual bps.
See docs/methods/costs.md for regression choices and scaling sources.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from rich.console import Console

from rebal.comparison_exports import cost_rows, figure_rows, write_comparison
from rebal.io import load_panel, load_signals
from rebal.paths import output_dir
from rebal.regress import DEFAULT_SAMPLE, dated, predictive
from rebal.signals import build, simulate_calendar, simulate_dates, simulate_threshold

EXHIBITS = ["costs", "figure_D5"]
CONTROLS = ["vix", "move", "epu", "ads", "sentiment"]


def annual_cost(impact: float, size: float, trades: float) -> float:
    """Slope times signal size gives price impact; weight by the share traded.

    Both return and weight use decimals. The paper's -0.39 slope and 1% trade
    imply a 0.39% price move on 1% of the portfolio: 4.68 bps over 12 trades.
    """
    return -impact * size**2 * trades * 10_000


def portfolio_returns(panel: pd.DataFrame, simulation: pd.DataFrame) -> np.ndarray:
    """Apply yesterday's post-trade weight to today's simple asset returns."""
    weights = np.r_[0.6, simulation.w_post.to_numpy()[:-1]]
    return weights * panel.r_es.to_numpy() + (1 - weights) * panel.r_ty.to_numpy()


def _fit(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    term: str,
    subset: pd.Series,
    sample: tuple[str, str],
    controls: bool,
    *,
    interaction: bool = False,
) -> tuple[float, str]:
    # pandas: small named regression designs use the shared statsmodels toolkit.
    frame = signals.copy()
    if term == "calendar":
        terms = ["threshold", "calendar", "momentum", "ret"]
    else:
        terms = [term, "calendar", "week4", "calendar:week4", "momentum", "ret"]
    if controls:
        terms += CONTROLS
    if interaction:
        frame["active"] = subset.to_numpy(dtype=int)
        # delta=0 is always active; omit duplicate dummy and slope in that case.
        if not subset.all():
            terms += ["active", f"{term}:active"]
        fit = predictive(frame, panel, terms, sample=sample)
        impact = float(fit.coef[term])
        if f"{term}:active" in fit.coef:
            impact += float(fit.coef[f"{term}:active"])
    else:
        fit = predictive(frame, panel, terms, sample=sample, subset=subset)
        impact = float(fit.coef[term])
    note = (
        f"HC1; n={fit.nobs}; outcome {fit.tidy.sample_start.iloc[0]}"
        f"..{fit.tidy.sample_end.iloc[0]}"
    )
    return impact, note


def random_dates(
    panel: pd.DataFrame,
    signals: pd.DataFrame,
    *,
    n_sims: int = 10_000,
    seed: int = 16,
    sample: tuple[str, str] = DEFAULT_SAMPLE,
    controls: bool = False,
) -> pd.DataFrame:
    """Uniform independent day per observed month, including the final week."""
    if n_sims < 1:
        raise ValueError("n_sims must be positive")
    p, s = dated(panel), dated(signals)
    stop = p.index.max() if sample[1] == "latest" else pd.Timestamp(sample[1])
    in_sample = (p.index >= sample[0]) & (p.index <= stop)
    positions = np.flatnonzero(in_sample)
    if not len(positions):
        raise ValueError("random dates need a nonempty sample")
    months = p.index[positions].to_period("M").asi8
    groups = np.split(positions, np.flatnonzero(months[:-1] != months[1:]) + 1)
    rng = np.random.default_rng(seed)
    baseline = portfolio_returns(p, simulate_calendar(p.r_es, p.r_ty))[in_sample]
    rows = []
    for draw in range(n_sims):
        chosen = np.array([rng.choice(group) for group in groups])
        simulation = simulate_dates(p.r_es, p.r_ty, p.index[chosen])
        # pandas: label a simulation-specific predictor and event subset for OLS.
        frame = s.copy()
        frame["random_signal"] = simulation.w_pre - 0.6
        terms = [
            "random_signal",
            "threshold",
            "calendar",
            "week4",
            "calendar:week4",
            "momentum",
            "ret",
        ] + (CONTROLS if controls else [])
        fit = predictive(
            frame.reset_index(),
            panel,
            terms,
            sample=sample,
            subset=pd.Series(p.index.isin(p.index[chosen]), index=p.index),
        )
        size = float(np.mean(np.abs(simulation.trade.to_numpy()[chosen])))
        difference = portfolio_returns(p, simulation)[in_sample] - baseline
        rows.append(
            {
                "simulation": draw + 1,
                "cost_bps_year": annual_cost(float(fit.coef.random_signal), size, 12),
                "tracking_error_bps_year": float(
                    np.std(difference, ddof=1) * np.sqrt(252) * 10_000
                ),
            }
        )
    # pandas: final small simulation output table.
    return pd.DataFrame(rows)


def estimate(
    panel: pd.DataFrame,
    signals: pd.DataFrame,
    *,
    n_sims: int = 10_000,
    seed: int = 16,
    end: str = DEFAULT_SAMPLE[1],
    controls: bool = False,
    assets: float = 20e12,
    fed_assets: float = 37.8e12,
    delta_zero: str = "exclude",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute paper §3.8 estimates; retain the entire history before sampling."""
    if not np.isfinite([assets, fed_assets]).all() or min(assets, fed_assets) <= 0:
        raise ValueError("asset bases must be finite and positive")
    if delta_zero not in {"include", "exclude"}:
        raise ValueError("delta_zero must be include or exclude")
    p, s = dated(panel), dated(signals)
    if not p.index.equals(s.index):
        raise ValueError("costs require signals on the full panel trading calendar")
    stop = p.index.max() if end == "latest" else pd.Timestamp(end)
    sample = (DEFAULT_SAMPLE[0], stop.date().isoformat())
    mask = (p.index >= sample[0]) & (p.index <= stop)
    if mask.sum() < 252:
        raise ValueError("costs need at least 252 sample trading days")
    rows: list[dict] = []

    def add(item: str, value: float, unit: str, note: str) -> None:
        rows.append({"item": item, "value": float(value), "unit": unit, "note": note})

    def report(
        prefix: str, impact: float, size: float, frequency: float, note: str
    ) -> float:
        cost = annual_cost(impact, size, frequency)
        add(f"{prefix}_impact", impact, "decimal return / weight", note)
        add(
            f"{prefix}_trade_size",
            size,
            "decimal weight",
            "Mean absolute executed trade",
        )
        add(
            f"{prefix}_trades",
            frequency,
            "trades/year",
            "Calendar=12; Threshold=count / (sample days/252)",
        )
        add(prefix, cost, "bps/year", note)
        return cost

    cal = simulate_calendar(p.r_es, p.r_ty)
    active = s.week4.astype(bool)
    impact, note = _fit(signals, panel, "calendar", active, sample, controls)
    trades = cal.trade.to_numpy()
    selected = mask & (trades != 0)
    size = float(np.mean(np.abs(trades[selected])))
    calendar_size = size
    calendar = report("calendar", impact, calendar_size, 12, note)
    alternative, note = _fit(
        signals, panel, "calendar", active, sample, controls, interaction=True
    )
    report("calendar_full_sample", alternative, size, 12, note)

    # T is the last trading day; T-4 has inclusive days_to_month_end equal to 5.
    early_days = s.days_to_month_end.to_numpy() == 5
    early = simulate_dates(p.r_es, p.r_ty, p.index[early_days])
    early_size = float(np.mean(np.abs(early.trade.to_numpy()[mask & early_days])))
    early_impact, note = _fit(
        signals, panel, "calendar", s.days_to_month_end == 5, sample, controls
    )
    report("calendar_T_minus_4", early_impact, early_size, 12, note)
    for name, lower, upper in (
        ("calendar_pre_2006", sample[0], "2005-12-31"),
        ("calendar_post_2006", "2007-01-01", sample[1]),
    ):
        dates = mask & (p.index >= lower) & (p.index <= upper)
        if not dates.any():
            raise ValueError(f"{name} needs observations; choose an end after 2007")
        beta, note = _fit(signals, panel, "calendar", active, (lower, upper), controls)
        subsize = float(np.mean(np.abs(trades[dates & (trades != 0)])))
        report(name, beta, subsize, 12, note + "; exclude transition year 2006")

    threshold_costs, fixed_costs, full_costs, full_fixed = [], [], [], []
    for i in range(26):
        delta, term = i / 1000, f"thr_{i:03d}"
        simulation = simulate_threshold(p.r_es, p.r_ty, delta)
        active = s[term].abs() >= delta
        beta, note = _fit(signals, panel, term, active, sample, controls)
        selected = mask & active.to_numpy()
        size = float(np.mean(np.abs(simulation.trade.to_numpy()[selected])))
        frequency = float(
            np.count_nonzero(simulation.trade.to_numpy()[mask]) * 252 / mask.sum()
        )
        cost = report(
            f"threshold_{i:03d}", beta, size, frequency, note + f"; delta={delta}"
        )
        fixed = annual_cost(beta, 0.01, frequency)
        add(
            f"threshold_{i:03d}_fixed_1pct",
            fixed,
            "bps/year",
            "Same impact and frequency; fixed 1% trade",
        )
        threshold_costs.append(cost)
        fixed_costs.append(fixed)
        beta_full, note = _fit(
            signals, panel, term, active, sample, controls, interaction=True
        )
        full_costs.append(annual_cost(beta_full, size, frequency))
        full_fixed.append(annual_cost(beta_full, 0.01, frequency))
        add(
            f"threshold_{i:03d}_full_sample",
            full_costs[-1],
            "bps/year",
            note + "; base slope + active interaction",
        )
    # Preserve every per-delta estimate, even when zero is excluded from summaries.
    # DEC-005 excludes zero by default; explicit inclusion is a sensitivity check.
    start = 0 if delta_zero == "include" else 1
    grid_note = (
        "Equal mean over all 26 deltas, 0..2.5%; delta=0 included"
        if start == 0
        else "Equal mean over 25 deltas, 0.1..2.5%; delta=0 excluded"
    )
    for item, values in (
        ("threshold_average", threshold_costs),
        ("threshold_fixed_1pct_average", fixed_costs),
        ("threshold_full_sample_average", full_costs),
        ("threshold_full_sample_fixed_1pct_average", full_fixed),
    ):
        add(item, np.mean(values[start:]), "bps/year", grid_note)
    add("threshold_min", min(threshold_costs[start:]), "bps/year", grid_note)
    add("threshold_max", max(threshold_costs[start:]), "bps/year", grid_note)
    headline = (calendar + np.mean(fixed_costs[start:])) / 2
    add(
        "headline",
        headline,
        "bps/year",
        "Mean of Calendar and fixed-1%-size Threshold average; " + grid_note,
    )
    add(
        "headline_full_sample",
        (annual_cost(alternative, calendar_size, 12) + np.mean(full_fixed[start:])) / 2,
        "bps/year",
        "Full-sample interaction alternative; " + grid_note,
    )

    draws = random_dates(
        panel, signals, n_sims=n_sims, seed=seed, sample=sample, controls=controls
    )
    values = draws.cost_bps_year.to_numpy()
    for item, value in (
        ("random_mean", np.mean(values)),
        ("random_median", np.median(values)),
        ("random_p025", np.quantile(values, 0.025)),
        ("random_p975", np.quantile(values, 0.975)),
    ):
        add(
            item,
            value,
            "bps/year",
            f"{n_sims} monthly schedules; seed={seed}; positive=loss",
        )
    add(
        "random_tracking_error",
        np.mean(draws.tracking_error_bps_year),
        "bps/year",
        "Mean annualized SD of daily return difference vs monthly Calendar",
    )
    add(
        "random_simulations",
        n_sims,
        "count",
        "One uniform trading day per month; week4 allowed",
    )

    for name, base in (("paper", assets), ("fed_z1", fed_assets)):
        dollars = headline / 10_000 * base
        add(f"assets_{name}", base, "USD", "D27; see docs/methods/costs.md")
        add(f"dollar_cost_{name}", dollars, "USD/year", "headline / 10000 * assets")
        add(
            f"per_household_{name}",
            dollars / (2 / 3 * 127e6),
            "USD/household/year",
            "Two-thirds of 127M households",
        )
    add("households", 127e6, "households", "Census 2022; paper D27")
    add("household_participation", 2 / 3, "fraction", "SCF; paper D27")

    utilities = {}
    for name, simulation in (
        ("buy_hold", simulate_dates(p.r_es, p.r_ty, [])),
        ("threshold_025", simulate_threshold(p.r_es, p.r_ty, 0.025)),
        ("calendar", cal),
    ):
        returns = portfolio_returns(p, simulation)[mask]
        utilities[name] = float(
            252 * (np.mean(returns) - 0.5 * 3 * np.var(returns, ddof=1)) * 10_000
        )
        add(
            f"utility_{name}",
            utilities[name],
            "bps/year",
            "Gross arithmetic mean-variance utility; gamma=3",
        )
    add(
        "utility_threshold_minus_buy_hold",
        utilities["threshold_025"] - utilities["buy_hold"],
        "bps/year",
        "Footnote 36; gross utility difference",
    )
    add(
        "utility_calendar_minus_buy_hold",
        utilities["calendar"] - utilities["buy_hold"],
        "bps/year",
        "Footnote 36; gross utility difference",
    )
    return pd.DataFrame(rows, columns=["item", "value", "unit", "note"]), draws


def plot_distribution(draws: pd.DataFrame, path: Path, demo: bool) -> None:
    """Render only the saved simulation data, without recomputing estimates."""
    figure = Figure(figsize=(8, 4.8), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    values = draws.cost_bps_year.to_numpy()
    axis.hist(values, bins=50, color="#386b95", alpha=0.85)
    axis.axvline(
        np.mean(values), color="#b23a2a", label=f"Mean = {np.mean(values):.2f} bps"
    )
    axis.axvline(0, color="black", linewidth=0.7)
    axis.set(
        xlabel="Annual cost (bps; positive = loss)",
        ylabel="Simulations",
        title="Random monthly rebalancing" + (" — synthetic demo" if demo else ""),
    )
    axis.legend()
    figure.savefig(path)
    figure.clear()


def run(demo: bool, **kwargs) -> list[Path]:
    panel = load_panel(demo=demo)
    if demo:
        p = dated(panel)
        signals = build(p.r_es, p.r_ty, r_sp500tr=p.r_sp500tr)
    else:
        signals = load_signals()
    costs, draws = estimate(panel, signals, **kwargs)
    tables = output_dir("demo" if demo else "tables")
    figures = output_dir("demo" if demo else "figures")
    csv, plotted, pdf = (
        tables / "costs.csv",
        figures / "figure_D5.csv",
        figures / "figure_D5.pdf",
    )
    costs.to_csv(csv, index=False)
    draws.to_csv(plotted, index=False)
    plot_distribution(draws, pdf, demo)
    canonical = [
        write_comparison(csv, cost_rows(costs)),
        write_comparison(plotted, figure_rows("figure_D5", draws)),
    ]
    metadata = tables / "costs.metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "script": "rebal.exhibits.costs",
                "created_utc": datetime.now(UTC).isoformat(),
                "source": "rebal.io demo panel; actual rebal.signals.build simulations"
                if demo
                else "rebal.io daily_panel and signals_clean",
                "parameters": {
                    "n_sims": 10_000,
                    "seed": 16,
                    "end": DEFAULT_SAMPLE[1],
                    "controls": False,
                    "assets": 20e12,
                    "fed_assets": 37.8e12,
                    "delta_zero": "exclude",
                    **kwargs,
                },
                "cost_formula": "-slope * decimal_trade_size**2 * trades_per_year * 10000",
                "sample_start": DEFAULT_SAMPLE[0],
                "sample_end": str(
                    min(
                        pd.Timestamp(kwargs.get("end", DEFAULT_SAMPLE[1])),
                        panel.date.max(),
                    )
                )
                if kwargs.get("end") != "latest"
                else str(panel.date.max()),
                "outputs": [str(path) for path in (csv, plotted, pdf, *canonical)],
            },
            indent=2,
        )
        + "\n"
    )
    return [csv, plotted, pdf, *canonical, metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate rebalancing costs and Figure D.5."
    )
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--n-sims", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=16)
    parser.add_argument("--end", default=DEFAULT_SAMPLE[1])
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--assets", type=float, default=20e12)
    parser.add_argument("--fed-assets", type=float, default=37.8e12)
    parser.add_argument(
        "--delta-zero",
        choices=["include", "exclude"],
        default="exclude",
        help="Threshold summary grid; per-delta rows always retain zero (default: exclude).",
    )
    args = parser.parse_args()
    if args.n_sims < 1:
        parser.error("--n-sims must be positive")
    return args


def main() -> None:
    args = vars(parse_args())
    for path in run(**args):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
