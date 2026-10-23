"""uv run python3 -m rebal.exhibits --all --demo --only table_6a table_6b table_6c figure_6
uv run python3 -m rebal.exhibits.strategy --demo --cal-reversal lag4 --end latest

CLI Arguments:
--demo: use planted synthetic returns and write output/demo/.
--end: inclusive endpoint (default 2023-03-17), or latest.
--cal-reversal: previous-week4 (default) or lag4 interpretation of Cal_{-4}.
--equity-cost-bps / --bond-cost-bps: one-way costs (defaults 1 / 0.5 bp).
--se: heteroskedasticity-consistent standard errors, hc1 (default) or hc0.
--timing: signal file suffix (default clean).

Reads docs/contracts/daily_panel.md and signals.md. Writes Table 6 A-C CSVs,
Figure 6 PDF and plotted CSV, and strategy.metadata.json per exhibits.md.
Methods, units and the demo-only spread substitution: docs/methods/strategy.md.
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
from scipy.stats import skew

from rebal.comparison_exports import figure_rows, strategy_rows, write_comparison
from rebal.io import load_panel, load_signals
from rebal.paths import output_dir
from rebal.regress import DEFAULT_SAMPLE, TABLE_COLUMNS, dated, ols

EXHIBITS = ["table_6a", "table_6b", "table_6c", "figure_6"]
FACTOR_MODELS = {
    "CAPM": ["mkt_rf"],
    "C4": ["mkt_rf", "smb", "hml", "mom"],
    "FF5": ["mkt_rf", "smb", "hml", "rmw", "cma"],
    "HXZ": ["q_mkt", "q_me", "q_ia", "q_roe"],
}
REGIMES = ["ivol", "liquidity", "vix", "move", "epu"]
REVERSALS = ["previous-week4", "lag4"]


def weights(
    signals: pd.DataFrame, cal_reversal: str = "previous-week4"
) -> pd.DataFrame:
    """Build unbounded weights on the full trading calendar, before sample cuts."""
    if cal_reversal not in REVERSALS:
        raise ValueError(f"cal_reversal must be one of {REVERSALS}")
    s = dated(signals)
    # pandas: small daily date indexing; arithmetic and monthly lookup use NumPy.
    months = s.index.to_period("M").asi8
    first = np.r_[True, months[1:] != months[:-1]]
    week4 = s.week4.to_numpy() == 1
    calendar = s.calendar.to_numpy(dtype=float)
    reference = np.full(len(s), np.nan)
    if cal_reversal == "previous-week4":
        unique_months, first_week4 = np.unique(months[week4], return_index=True)
        lookup = dict(zip(unique_months, calendar[week4][first_week4]))
        reference[first] = [lookup.get(month - 1, np.nan) for month in months[first]]
    else:
        reference[4:] = calendar[:-4]
    cal = np.where(week4, -np.sign(calendar), 0.0)
    cal[first] = np.sign(reference[first])
    cal[~np.isfinite(s.week4.to_numpy(dtype=float))] = np.nan
    threshold = -s.threshold.to_numpy(dtype=float) / 0.015
    return pd.DataFrame(
        {
            "threshold_weight": threshold,
            "calendar_weight": cal,
            "weight": (threshold + cal) / 2,
        },
        index=s.index,
    )


def strategy_data(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    demo: bool = False,
    end: str = DEFAULT_SAMPLE[1],
    cal_reversal: str = "previous-week4",
    equity_cost_bps: float = 1.0,
    bond_cost_bps: float = 0.5,
) -> pd.DataFrame:
    """Pair weight/controls at t with returns/factors at the actual next panel day."""
    costs = np.array([equity_cost_bps, bond_cost_bps])
    if not np.isfinite(costs).all() or (costs < 0).any():
        raise ValueError("costs must be finite and nonnegative")
    s, p = dated(signals), dated(panel)
    if not s.index.isin(p.index).all():
        raise ValueError("signal dates must belong to the panel trading calendar")
    # pandas: small daily time series aligned by contract dates for named OLS inputs.
    s = s.reindex(p.index)
    if demo:
        # The demo contract plants effects in ret, independently of panel returns.
        p["r_es"] = p.r_ty + s.ret
    w = weights(s.reset_index(), cal_reversal)
    frame = p.shift(-1)
    frame[REGIMES] = p[REGIMES]  # conditioning information is known at t
    frame = frame.join(w)
    frame["strategy"] = (frame.r_es - frame.r_ty) * frame.weight
    frame["threshold_piece"] = (frame.r_es - frame.r_ty) * frame.threshold_weight
    frame["calendar_piece"] = (frame.r_es - frame.r_ty) * frame.calendar_weight
    position = w.weight.to_numpy()
    frame["turnover"] = 2 * np.abs(position - np.r_[0.0, position[:-1]])
    frame["strategy_net_costs"] = (
        frame.strategy - frame.turnover / 2 * (equity_cost_bps + bond_cost_bps) / 10000
    )
    frame["signal_date"] = p.index
    frame["date"] = pd.Series(p.index, index=p.index).shift(-1)
    stop = p.index.max() if end == "latest" else pd.Timestamp(end)
    if pd.isna(stop) or stop < pd.Timestamp(DEFAULT_SAMPLE[0]):
        raise ValueError("end must be on or after the sample start")
    mask = (
        (frame.index >= DEFAULT_SAMPLE[0])
        & frame.date.between(DEFAULT_SAMPLE[0], stop)
        & np.isfinite(frame.strategy)
    )
    frame = frame.loc[mask].set_index("date")
    if len(frame) < 3:
        raise ValueError("strategy needs at least three complete sample returns")
    return frame


def descriptive_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Panel A, plus costs, crisis exclusion and each standalone component."""
    # pandas: final display assembly and date selection for a small daily series.
    crisis = ((frame.index >= "2008-09-01") & (frame.index <= "2009-03-31")) | (
        (frame.index >= "2020-03-01") & (frame.index <= "2020-03-31")
    )
    series = {
        name: frame[name]
        for name in (
            "strategy",
            "r_es",
            "r_ty",
            "strategy_net_costs",
            "threshold_piece",
            "calendar_piece",
        )
    }
    series["strategy_ex_crises"] = frame.loc[~crisis, "strategy"]
    rows = []
    for name, values in series.items():
        values = values[np.isfinite(values)]
        returns = values.to_numpy()
        if len(returns) < 3:
            raise ValueError(f"{name} needs at least three finite observations")
        mean, vol = np.mean(returns) * 252, np.std(returns, ddof=1) * np.sqrt(252)
        rows.append(
            {
                "asset": name,
                "mean_pct_pa": mean * 100,
                "volatility_pct_pa": vol * 100,
                "sharpe": mean / vol if vol else np.nan,
                "skewness": skew(returns, bias=False) if vol else np.nan,
                "nobs": len(returns),
                "sample_start": values.index.min().date().isoformat(),
                "sample_end": values.index.max().date().isoformat(),
            }
        )
    return pd.DataFrame(rows)


def _annualized_row(result, exhibit: str, column: str) -> pd.DataFrame:
    row = result.tidy.loc[result.tidy.term == "const"].copy()
    row["exhibit"], row["column"], row["term"] = (
        exhibit,
        column,
        "alpha" if exhibit == "table_6b" else "mean",
    )
    row[["coef", "se"]] *= 252 * 100
    return row[TABLE_COLUMNS]


def factor_alphas(frame: pd.DataFrame, se: str = "hc1") -> pd.DataFrame:
    """Panel B: same-day factors explain realized excess strategy returns."""
    # pandas: named, small statsmodels designs and final contract table assembly.
    return pd.concat(
        [
            _annualized_row(
                ols(frame.strategy, frame[factors], se=se), "table_6b", model
            )
            for model, factors in FACTOR_MODELS.items()
        ],
        ignore_index=True,
    )


def regime_means(
    frame: pd.DataFrame, se: str = "hc1"
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Panel C: one full-sample median per t-dated control; ties join low."""
    # pandas: named intercept-only OLS designs and final contract table assembly.
    rows, medians = [], {}
    for control in REGIMES:
        values = frame[control].to_numpy(dtype=float)
        finite = np.isfinite(values)
        if not finite.any():
            raise ValueError(f"no finite regime observations for {control}")
        median = float(np.median(values[finite]))
        medians[control] = median
        for label, mask in (("H", values > median), ("L", values <= median)):
            y = frame.loc[finite & mask, "strategy"]
            result = ols(y, pd.DataFrame(index=y.index), se=se)
            rows.append(_annualized_row(result, "table_6c", f"{control}:{label}"))
    return pd.concat(rows, ignore_index=True), medians


def cumulative_gains(frame: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    """Figure data: scale daily strategy returns once, then sum log1p gains."""
    values = frame[["strategy", "r_es", "r_ty"]].to_numpy(dtype=float).copy()
    vol = np.std(values[:, 0], ddof=1)
    if vol <= 0 or not np.isfinite(values).all():
        raise ValueError("figure needs finite returns and positive strategy volatility")
    scale = float(np.std(values[:, 1], ddof=1) / vol)
    values[:, 0] *= scale
    if (values <= -1).any():
        raise ValueError("Figure 6 log gains require every scaled return > -1")
    # pandas: label the final plotted NumPy arrays.
    plotted = pd.DataFrame(
        np.cumsum(np.log1p(values), axis=0),
        index=frame.index,
        columns=["strategy_log_gain", "r_es_log_gain", "r_ty_log_gain"],
    )
    return plotted.reset_index(), scale


def plot_gains(plotted: pd.DataFrame, path: Path, demo: bool) -> None:
    figure = Figure(figsize=(10, 5), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    for name, label in (
        ("strategy", "Strategy (equity volatility)"),
        ("r_es", "S&P 500"),
        ("r_ty", "10-year Treasury"),
    ):
        axis.plot(plotted.date, plotted[f"{name}_log_gain"], label=label, linewidth=0.9)
    axis.axhline(0, color="black", linewidth=0.5)
    axis.set(
        xlabel="Date",
        ylabel="Cumulative log gain",
        title="Front-running strategy" + (" — synthetic demo" if demo else ""),
    )
    axis.grid(alpha=0.2)
    axis.legend()
    figure.savefig(path)
    figure.clear()


def run(
    demo: bool = False,
    *,
    end: str = DEFAULT_SAMPLE[1],
    cal_reversal: str = "previous-week4",
    equity_cost_bps: float = 1.0,
    bond_cost_bps: float = 0.5,
    se: str = "hc1",
    timing: str = "clean",
) -> list[Path]:
    frame = strategy_data(
        load_signals(demo=demo, timing=timing),
        load_panel(demo=demo),
        demo=demo,
        end=end,
        cal_reversal=cal_reversal,
        equity_cost_bps=equity_cost_bps,
        bond_cost_bps=bond_cost_bps,
    )
    table_c, medians = regime_means(frame, se)
    tables = {
        "table_6a": descriptive_table(frame),
        "table_6b": factor_alphas(frame, se),
        "table_6c": table_c,
    }
    plotted, scale = cumulative_gains(frame)
    destination = output_dir("demo" if demo else "tables")
    figures = output_dir("demo" if demo else "figures")
    outputs = []
    for exhibit, table in tables.items():
        path = destination / f"{exhibit}.csv"
        table.to_csv(path, index=False)
        outputs.extend([path, write_comparison(path, strategy_rows(exhibit, table))])
    csv, pdf = figures / "figure_6.csv", figures / "figure_6.pdf"
    plotted.to_csv(csv, index=False)
    plot_gains(plotted, pdf, demo)
    outputs += [csv, pdf, write_comparison(csv, figure_rows("figure_6", plotted))]
    metadata = destination / "strategy.metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "module": __name__,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "inputs": ["rebal.io.load_panel", "rebal.io.load_signals"],
                "demo_returns": "r_es = r_ty + signals.ret" if demo else None,
                "parameters": {
                    "end": end,
                    "cal_reversal": cal_reversal,
                    "equity_cost_bps": equity_cost_bps,
                    "bond_cost_bps": bond_cost_bps,
                    "se": se,
                    "timing": timing,
                },
                "sample_start": frame.index.min().date().isoformat(),
                "sample_end": frame.index.max().date().isoformat(),
                "nobs": len(frame),
                "regime_medians_at_t": medians,
                "strategy_volatility_scale": scale,
                "cost_source": "Harvey et al. (2018), PDF p. 5; see docs/methods/strategy.md",
                "outputs": [str(path) for path in outputs],
            },
            indent=2,
        )
        + "\n"
    )
    return outputs + [metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build front-running strategy exhibits."
    )
    parser.add_argument(
        "--demo", action="store_true", help="Use planted synthetic inputs."
    )
    parser.add_argument(
        "--end", default=DEFAULT_SAMPLE[1], help="Inclusive ISO end or latest."
    )
    parser.add_argument("--cal-reversal", choices=REVERSALS, default="previous-week4")
    parser.add_argument(
        "--equity-cost-bps", type=float, default=1.0, help="One-way equity cost in bp."
    )
    parser.add_argument(
        "--bond-cost-bps", type=float, default=0.5, help="One-way bond cost in bp."
    )
    parser.add_argument("--se", choices=["hc0", "hc1"], default="hc1")
    parser.add_argument("--timing", default="clean", help="Signal filename suffix.")
    args = parser.parse_args()
    costs = np.array([args.equity_cost_bps, args.bond_cost_bps])
    if not np.isfinite(costs).all() or (costs < 0).any():
        parser.error("costs must be finite and nonnegative")
    return args


def main() -> None:
    for path in run(**vars(parse_args())):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
