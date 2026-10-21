"""uv run python3 -m rebal.signals --demo
uv run python3 -m rebal.signals --build --timing literal --momentum all15

CLI Arguments:
--build: build from the real daily panel.
--demo: build from synthetic panel returns and run self-checks.
--timing clean|literal: same-close reset (default) or Appendix B delayed reset.
--momentum medium-slow|all15: average subfamilies (default) or all 15 signs.

Reads rebal.io.load_panel(), using r_es, r_ty and r_sp500tr. Writes the signals
contract and JSON lineage to processed_dir(), or output/demo/ in demo mode.
Processing only; descriptive exhibits live in rebal.exhibits.signals_descriptive.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from datetime import UTC, datetime

import numpy as np
import pandas as pd
from rich.console import Console

from rebal.io import load_panel
from rebal.paths import output_dir, processed_dir

DEFAULT_DELTAS = tuple(i / 1000 for i in range(41))
LOOKBACKS = {
    "mom_fast": tuple(range(1, 11)),
    "mom_medium": tuple(range(11, 21)),
    "mom_slow": (21, 42, 63, 126, 252),
}


def _inputs(r_eq: pd.Series, r_bd: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """Reject missing or misaligned inputs rather than silently dropping dates."""
    index = r_eq.index
    if (
        not isinstance(index, pd.DatetimeIndex)
        or index.empty
        or index.tz is not None
        or index.hasnans
        or not index.is_unique
        or not index.is_monotonic_increasing
        or not index.equals(index.normalize())
        or not index.equals(r_bd.index)
    ):
        raise ValueError(
            "returns need aligned, nonempty, sorted unique naive midnight dates"
        )
    eq, bd = r_eq.to_numpy(dtype=float), r_bd.to_numpy(dtype=float)
    if not np.isfinite(eq).all() or not np.isfinite(bd).all():
        raise ValueError("returns must be finite; missing returns cannot be simulated")
    if np.any(eq <= -1) or np.any(bd <= -1):
        raise ValueError("each asset return must exceed -1")
    return eq, bd


def _parameters(target: float, timing: str) -> None:
    if not np.isfinite(target) or not 0 < target < 1:
        raise ValueError("target must lie strictly between 0 and 1")
    if timing not in {"clean", "literal"}:
        raise ValueError("timing must be clean or literal")


def _days_left(index: pd.DatetimeIndex) -> np.ndarray:
    months = index.to_period("M").asi8
    ends = np.r_[np.flatnonzero(months[:-1] != months[1:]) + 1, len(index)]
    return np.repeat(ends, np.diff(np.r_[0, ends])) - np.arange(len(index))


def _simulate(
    index: pd.DatetimeIndex,
    eq: np.ndarray,
    bd: np.ndarray,
    target: float,
    timing: str,
    *,
    delta: float | None = None,
    schedule: np.ndarray | None = None,
) -> pd.DataFrame:
    """Sequential recursion: each drift depends on the preceding post-trade weight."""
    _parameters(target, timing)
    weights = np.empty((len(eq), 3), dtype=float)
    previous = target
    for t, (equity, bond) in enumerate(zip(eq, bd)):
        pre = previous * (1 + equity)
        pre /= pre + (1 - previous) * (1 + bond)
        if delta is not None:
            check = pre if timing == "clean" else previous
            rebalance = abs(check - target) >= delta
        else:
            rebalance = bool(schedule[t])
        post = target if rebalance else pre
        weights[t] = pre, post, post - pre
        previous = post
    # pandas: labeled API output around the sequential NumPy simulation.
    return pd.DataFrame(weights, index=index, columns=["w_pre", "w_post", "trade"])


def simulate_threshold(
    r_eq: pd.Series,
    r_bd: pd.Series,
    delta: float,
    target: float = 0.60,
    timing: str = "clean",
) -> pd.DataFrame:
    """Reset when deviation reaches delta; literal tests yesterday's weight."""
    eq, bd = _inputs(r_eq, r_bd)
    if not np.isfinite(delta) or delta < 0:
        raise ValueError("delta must be finite and nonnegative")
    return _simulate(r_eq.index, eq, bd, target, timing, delta=delta)


def simulate_calendar(
    r_eq: pd.Series,
    r_bd: pd.Series,
    target: float = 0.60,
    timing: str = "clean",
) -> pd.DataFrame:
    """Reset at each supplied month-end, or the following close in literal mode."""
    eq, bd = _inputs(r_eq, r_bd)
    schedule = _days_left(r_eq.index) == 1
    if timing == "literal":
        schedule = np.r_[False, schedule[:-1]]
    return _simulate(r_eq.index, eq, bd, target, timing, schedule=schedule)


def simulate_dates(
    r_eq: pd.Series, r_bd: pd.Series, dates: Iterable, target: float = 0.60
) -> pd.DataFrame:
    """Reset at the close of explicitly supplied trading dates."""
    eq, bd = _inputs(r_eq, r_bd)
    dates = pd.DatetimeIndex(dates)
    if dates.hasnans or not dates.isin(r_eq.index).all():
        raise ValueError("rebalance dates must belong to the input trading index")
    return _simulate(
        r_eq.index, eq, bd, target, "clean", schedule=r_eq.index.isin(dates)
    )


def _cumulative(values: np.ndarray, window: int) -> np.ndarray:
    result = np.full(len(values), np.nan)
    if len(values) >= window:
        windows = np.lib.stride_tricks.sliding_window_view(1 + values, window)
        result[window - 1 :] = np.prod(windows, axis=1) - 1
    return result


def _eom_reversal(index: pd.DatetimeIndex, returns: pd.Series | None) -> np.ndarray:
    """Known-to-date S&P return after fourth-Friday close; never backfill a month."""
    if returns is None:
        return np.full(len(index), np.nan)
    # pandas: date arithmetic only; return accumulation uses NumPy.
    if not index.equals(returns.index):
        raise ValueError("r_sp500tr must align with the input trading index")
    values = returns.to_numpy(dtype=float)
    if np.isinf(values).any() or np.any(values <= -1):
        raise ValueError("r_sp500tr must exceed -1, allowing NaN for missing data")
    starts = index.to_period("M").to_timestamp()
    friday = starts + pd.to_timedelta((4 - starts.dayofweek) % 7 + 21, unit="D")
    result = np.empty(len(index), dtype=float)
    anchor = False
    growth = 1.0
    for t, date in enumerate(index):
        if t == 0 or starts[t] != starts[t - 1]:
            anchor, growth = False, 1.0
        if date <= friday[t]:
            # The last supplied close on/before a holiday Friday is its anchor.
            result[t] = 0.0
            anchor, growth = True, 1.0
        else:
            growth *= 1 + values[t]
            result[t] = growth - 1 if anchor else np.nan
    return result


def build(
    r_eq: pd.Series,
    r_bd: pd.Series,
    target: float = 0.60,
    timing: str = "clean",
    deltas: Iterable[float] = DEFAULT_DELTAS,
    *,
    r_sp500tr: pd.Series | None = None,
    momentum: str = "medium-slow",
) -> pd.DataFrame:
    """Build the signals contract without shifting predictors or dropping warm-up rows.

    Custom grids must retain 0..0.025 in steps of .001; optional diagnostics above
    .025 can be omitted. The default grid produces the exact contract schema.
    Missing S&P input leaves eom_rev missing, rather than substituting futures.
    """
    eq, bd = _inputs(r_eq, r_bd)
    _parameters(target, timing)
    grid = np.asarray(tuple(deltas), dtype=float)
    if (
        grid.ndim != 1
        or not np.isfinite(grid).all()
        or np.any(grid < 0)
        or np.any(grid > 0.04)
        or not np.allclose(grid * 1000, np.round(grid * 1000), rtol=0, atol=1e-10)
    ):
        raise ValueError("deltas must be grid points from 0 to .040 in .001 steps")
    labels = np.round(grid * 1000).astype(int)
    if len(set(labels)) != len(labels) or not set(range(26)).issubset(labels):
        raise ValueError(
            "deltas must be unique and include all 26 aggregate thresholds"
        )
    if momentum not in {"medium-slow", "all15"}:
        raise ValueError("momentum must be medium-slow or all15")
    grid = np.sort(grid)
    index = r_eq.index
    spread = eq - bd
    data = {"date": index.as_unit("ns"), "ret": spread}

    def threshold(weight: float) -> np.ndarray:
        columns = []
        for delta in grid:
            simulation = _simulate(index, eq, bd, weight, timing, delta=delta)
            signal = simulation.w_pre.to_numpy() - weight
            if weight == target:
                data[f"thr_{round(delta * 1000):03d}"] = signal
            if delta <= 0.025:
                columns.append(signal)
        return np.mean(columns, axis=0)

    data["threshold"] = threshold(target)
    data["calendar"] = (
        simulate_calendar(r_eq, r_bd, target, timing).w_pre.to_numpy() - target
    )
    days_left = _days_left(index)
    for week, mask in (
        (1, days_left > 15),
        (2, (days_left >= 11) & (days_left <= 15)),
        (3, (days_left >= 6) & (days_left <= 10)),
        (4, days_left <= 5),
    ):
        data[f"week{week}"] = mask.astype("int64")
    data["days_to_month_end"] = days_left.astype("int64")
    signs = {k: np.sign(_cumulative(spread, k)) for k in range(1, 21)}
    signs.update({k: np.sign(_cumulative(spread, k)) for k in LOOKBACKS["mom_slow"]})
    for name, lookbacks in LOOKBACKS.items():
        data[name] = np.mean([signs[k] for k in lookbacks], axis=0)
    data["momentum"] = (
        (data["mom_medium"] + data["mom_slow"]) / 2
        if momentum == "medium-slow"
        else np.mean(
            [signs[k] for k in (*LOOKBACKS["mom_medium"], *LOOKBACKS["mom_slow"])],
            axis=0,
        )
    )
    data["rev_st"] = _cumulative(spread, 5)
    data["rev_lt"] = np.r_[np.full(252, np.nan), _cumulative(spread, 1008)][
        : len(index)
    ]
    data["eom_rev"] = _eom_reversal(index, r_sp500tr)
    for suffix, weight in (("t86", 0.86), ("t50", 0.50), ("t70", 0.70)):
        data[f"threshold_{suffix}"] = threshold(weight)
        data[f"calendar_{suffix}"] = (
            simulate_calendar(r_eq, r_bd, weight, timing).w_pre.to_numpy() - weight
        )
    # pandas: small, labeled contract output; core calculations use NumPy.
    return pd.DataFrame(data)


def self_checks(
    r_eq: pd.Series,
    r_bd: pd.Series,
    *,
    timing: str = "clean",
    momentum: str = "medium-slow",
) -> tuple[dict[str, bool], np.ndarray]:
    """Independent identities on demo returns, plus a controlled trade-count check."""
    eq, bd = _inputs(r_eq, r_bd)
    target = 0.60
    daily = simulate_threshold(r_eq, r_bd, 0)
    never = simulate_threshold(r_eq, r_bd, 1)
    growth_eq, growth_bd = np.cumprod(1 + eq), np.cumprod(1 + bd)
    buy_hold = target * growth_eq / (target * growth_eq + (1 - target) * growth_bd)
    calendar = simulate_calendar(r_eq, r_bd)
    small = simulate_calendar(r_eq / 10, r_bd / 10).w_pre.to_numpy() - target
    days_left = _days_left(r_eq.index)
    cumulative = np.empty(len(eq))
    growth = 1.0
    for t, ret in enumerate((eq - bd) / 10):
        growth *= 1 + ret
        cumulative[t] = growth - 1
        if days_left[t] == 1:
            growth = 1.0
    counts = np.array(
        [
            np.count_nonzero(simulate_threshold(r_eq, r_bd, delta, timing=timing).trade)
            for delta in DEFAULT_DELTAS
        ]
    )
    # Strict monotonic counts are not a theorem for arbitrary paths. Check a
    # controlled one-direction path, while reporting unmodified demo counts.
    trend = pd.Series(0.001, index=r_eq.index[:252])
    zeros = trend * 0
    trend_counts = [
        np.count_nonzero(simulate_threshold(trend, zeros, d).trade)
        for d in DEFAULT_DELTAS
    ]
    frame = build(r_eq, r_bd, timing=timing, momentum=momentum)
    literal = simulate_threshold(r_eq, r_bd, 0.011, timing="literal")
    previous = np.r_[target, literal.w_post.to_numpy()[:-1]]
    delayed = simulate_calendar(r_eq, r_bd, timing="literal")
    checks = {
        "delta=0 daily drift": np.allclose(
            daily.w_pre, target * (1 + eq) / (1 + target * eq + (1 - target) * bd)
        )
        and np.count_nonzero(daily.trade) == len(eq),
        "delta=1 buy-and-hold": not np.any(never.trade)
        and np.allclose(never.w_pre, buy_hold),
        "Calendar month-end trades": np.array_equal(
            calendar.trade != 0, days_left == 1
        ),
        "0.24 approximation": np.linalg.norm(small - 0.24 * cumulative)
        <= 0.05 * np.linalg.norm(0.24 * cumulative),
        "literal Threshold previous-weight reset": np.allclose(
            literal.w_post,
            np.where(np.abs(previous - target) >= 0.011, target, literal.w_pre),
        ),
        "literal Calendar next-close reset": np.array_equal(
            delayed.trade != 0,
            np.r_[False, days_left[:-1] == 1],
        ),
        "controlled trade counts decrease": bool(np.all(np.diff(trend_counts) <= 0)),
        "momentum bounds": all(
            np.nanmax(np.abs(frame[c])) <= 1 for c in (*LOOKBACKS, "momentum")
        ),
    }
    return checks, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build portfolio rebalancing signals.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--build", action="store_true", help="Use the real daily panel."
    )
    action.add_argument(
        "--demo", action="store_true", help="Use demo returns and run self-checks."
    )
    parser.add_argument("--timing", choices=["clean", "literal"], default="clean")
    parser.add_argument(
        "--momentum", choices=["medium-slow", "all15"], default="medium-slow"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    console = Console()
    # pandas: unpack the small date-indexed panel into the simulation API.
    panel = load_panel(demo=args.demo).set_index("date")
    frame = build(
        panel.r_es,
        panel.r_ty,
        timing=args.timing,
        momentum=args.momentum,
        r_sp500tr=panel.r_sp500tr,
    )
    destination = output_dir("demo") if args.demo else processed_dir()
    path = destination / f"signals_{args.timing}.parquet"
    frame.to_parquet(path, index=False)
    metadata = {
        "script": "rebal.signals",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "rebal.demo.make_panel"
        if args.demo
        else str(processed_dir() / "daily_panel.parquet"),
        "parameters": {
            "target": 0.60,
            "timing": args.timing,
            "momentum": args.momentum,
            "deltas": DEFAULT_DELTAS,
        },
        "rows": len(frame),
        "start": str(frame.date.min()),
        "end": str(frame.date.max()),
        "output": str(path),
    }
    path.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n")
    console.print(
        f"Wrote {len(frame)} rows, {len(frame.columns)} columns: {path}", soft_wrap=True
    )
    if args.demo:
        checks, counts = self_checks(
            panel.r_es, panel.r_ty, timing=args.timing, momentum=args.momentum
        )
        for name, passed in checks.items():
            console.print(f"{'PASS' if passed else 'FAIL'}: {name}")
        console.print(f"delta  rebalances  per_year (252 trading days; {args.timing})")
        for delta, count in zip(DEFAULT_DELTAS, counts):
            console.print(f"{delta:.3f}  {count:5d}  {count * 252 / len(panel):.3f}")
        if not all(checks.values()):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
