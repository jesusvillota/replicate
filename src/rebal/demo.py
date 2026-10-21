"""uv run python3 -m rebal.demo --check

CLI Arguments:
--check: fit planted and zero-effect OLS equations and enforce a 0.05 tolerance.

Builds synthetic panel and signal contracts in memory. Reads and writes no files.
The fixtures are test inputs, with no real portfolio simulation or estimation API.
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from rich.console import Console
from scipy.signal import lfilter


def _ar1(rng: np.random.Generator, n: int, sd: float, rho: float = 0.8) -> np.ndarray:
    """Stationary zero-mean AR(1) with the requested population SD."""
    shocks = rng.normal(0, sd * np.sqrt(1 - rho**2), n + 256)
    return lfilter([1], [1, -rho], shocks)[256:]


def make_panel(
    start: str = "1996-01-02", end: str = "2023-12-29", seed: int = 0
) -> pd.DataFrame:
    """Make every daily-panel column using weekdays (not an exchange calendar)."""
    # pandas: small synthetic fixture construction and date handling only.
    dates = pd.bdate_range(start, end).as_unit("ns")
    if len(dates) < 2:
        raise ValueError("demo panel needs at least two weekdays")
    rng = np.random.default_rng(seed)
    n = len(dates)
    equity, bond = rng.normal(size=(2, n))
    r_es = 0.07 / 252 + 0.18 / np.sqrt(252) * equity
    r_ty = 0.02 / 252 + 0.06 / np.sqrt(252) * (-0.2 * equity + np.sqrt(0.96) * bond)
    rf = 0.02 / 252 + _ar1(rng, n, 0.005 / 252, 0.98)
    data = {"date": dates, "r_es": r_es, "r_ty": r_ty, "rf": rf, "rf_3m": rf.copy()}
    controls = {
        "vix": (0.20, 0.04),
        "move": (0.90, 0.15),
        "epu": (100, 20),
        "ads": (0, 0.7),
        "sentiment": (0, 0.3),
        "ra_bex": (3, 0.5),
        "unc_bex": (1, 0.2),
        "ara": (0, 1),
        "liquidity": (0, 1),
        "ivol": (0.02, 0.004),
    }
    for name, (level, sd) in controls.items():
        data[name] = level + _ar1(rng, n, sd)
    for name in (
        "mkt_rf",
        "smb",
        "hml",
        "rmw",
        "cma",
        "mom",
        "q_mkt",
        "q_me",
        "q_ia",
        "q_roe",
        "q_eg",
    ):
        data[name] = (
            r_es.copy() if name in {"mkt_rf", "q_mkt"} else rng.normal(0, 0.006, n)
        )
    for name in (
        "r_sp500tr",
        "r_agg",
        "r_acwxus",
        "r_r1k",
        "r_r2k",
        "r_r1kv",
        "r_r1kg",
        "r_mkt_french",
        "r_10y_gsw",
    ):
        base = r_ty if name in {"r_agg", "r_10y_gsw"} else r_es
        data[name] = base + rf
    return pd.DataFrame(data)


def make_signals(
    panel: pd.DataFrame,
    beta_threshold: float = -0.4,
    beta_calweek4: float = -0.3,
    seed: int = 0,
) -> pd.DataFrame:
    """Plant next-day return effects; leave the input panel unchanged.

    Auxiliary signals are synthetic placeholders, not TASK-013 signal logic.
    Demo ret deliberately replaces the panel spread to isolate planted effects.
    """
    # pandas: small synthetic fixture construction and vectorized month grouping only.
    dates = pd.to_datetime(panel["date"]).reset_index(drop=True)
    if len(dates) < 2 or dates.isna().any() or dates.dt.tz is not None:
        raise ValueError("demo signals need at least two naive dates")
    if not dates.is_monotonic_increasing or dates.duplicated().any():
        raise ValueError("demo dates must be sorted and unique")
    rng = np.random.default_rng(seed)
    n = len(dates)
    threshold = _ar1(rng, n, 0.0048, 0.61)
    calendar = _ar1(rng, n, 0.01, 0.91)
    days_left = (
        dates.groupby(dates.dt.to_period("M")).cumcount(ascending=False).to_numpy() + 1
    )
    data = {"date": dates, "ret": np.zeros(n)}
    for i in range(41):
        data[f"thr_{i:03d}"] = threshold * (0.5 + i / 25)
    data.update(threshold=threshold, calendar=calendar)
    for week in range(1, 5):
        lower, upper = {1: (15, n), 2: (10, 15), 3: (5, 10), 4: (0, 5)}[week]
        data[f"week{week}"] = ((days_left > lower) & (days_left <= upper)).astype(
            "int64"
        )
    data["days_to_month_end"] = days_left
    for name in ("mom_fast", "mom_medium", "mom_slow"):
        data[name] = np.tanh(_ar1(rng, n, 0.5))
    data["momentum"] = (data["mom_medium"] + data["mom_slow"]) / 2
    for name in ("rev_st", "rev_lt", "eom_rev"):
        data[name] = _ar1(rng, n, 0.02)
    for suffix, target in (("t86", 0.86), ("t50", 0.50), ("t70", 0.70)):
        scale = target * (1 - target) / (0.6 * 0.4)
        data[f"threshold_{suffix}"] = threshold * scale
        data[f"calendar_{suffix}"] = calendar * scale
    ret = rng.normal(0, 0.01, n)
    ret[1:] += (
        beta_threshold * threshold[:-1]
        + beta_calweek4 * (calendar * data["week4"])[:-1]
    )
    data["ret"] = ret
    return pd.DataFrame(data)


def recover_betas(signals: pd.DataFrame) -> np.ndarray:
    """Plain OLS of ret[t+1] on the two signals at t, with an intercept."""
    design = np.column_stack(
        (
            np.ones(len(signals) - 1),
            signals["threshold"].to_numpy()[:-1],
            (signals["calendar"].to_numpy() * signals["week4"].to_numpy())[:-1],
        )
    )
    return np.linalg.lstsq(design, signals["ret"].to_numpy()[1:], rcond=None)[0][1:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check synthetic planted return effects."
    )
    parser.add_argument(
        "--check", action="store_true", help="Run planted and zero-effect OLS checks."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    console = Console()
    panel = make_panel()
    if not args.check:
        console.print(
            f"Demo fixtures: {len(panel)} rows. Use --check to verify planted effects."
        )
        return
    passed = True
    for label, expected in (("planted", (-0.4, -0.3)), ("zero", (0.0, 0.0))):
        actual = recover_betas(make_signals(panel, *expected))
        ok = bool(np.all(np.abs(actual - expected) <= 0.05))
        passed &= ok
        console.print(
            f"{label}: beta_threshold={actual[0]:.6f} beta_calweek4={actual[1]:.6f} "
            f"expected={expected} {'PASS' if ok else 'FAIL'}",
            soft_wrap=True,
        )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
