"""Hodrick (1992) 1B covariance for overlapping predictive regressions.

OLS coefficients come from rebal.regress. The covariance uses demeaned
one-period returns and reverse sums of regressors under the no-predictability
null. See docs/methods/horizons.md for the formula and endpoint treatment.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from rebal.regress import RegressionResult, ols


def hodrick(
    y: pd.Series,
    X: pd.DataFrame,
    one_period: pd.Series,
    horizon: int,
) -> RegressionResult:
    """Fit y[t] = sum(r[t+1:t+h]) on X[t] with Hodrick 1B errors.

    one_period has the full ordered trading calendar as its index. Missing
    origins remain holes in that calendar, never compressed into adjacent days.
    Only one-period returns contributing to retained outcomes enter the meat.
    """
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    calendar = one_period.index
    if (
        not calendar.is_unique
        or not calendar.is_monotonic_increasing
        or calendar.hasnans
    ):
        raise ValueError("one_period calendar must be sorted, unique and nonmissing")
    result = ols(y, X, se="hc0")
    positions = calendar.get_indexer(result.design.index)
    if (positions < 0).any() or (positions + horizon >= len(calendar)).any():
        raise ValueError("each origin needs its full future horizon in one_period")
    design = result.design.to_numpy()
    reverse = np.zeros((len(calendar), design.shape[1]))
    for step in range(1, horizon + 1):
        np.add.at(reverse, positions + step, design)
    used = reverse[:, 0] > 0
    returns = one_period.to_numpy(dtype=float)[used]
    if not np.isfinite(returns).all():
        raise ValueError("one_period returns within retained horizons must be finite")
    scores = reverse[used] * (returns - returns.mean())[:, None]
    bread = np.linalg.inv(design.T @ design)
    covariance = bread @ (scores.T @ scores) @ bread
    covariance = (covariance + covariance.T) / 2
    # pandas: named covariance and tidy inference for the small OLS result.
    names = result.coef.index
    result.covariance = pd.DataFrame(covariance, index=names, columns=names)
    result.se = pd.Series(np.sqrt(np.maximum(np.diag(covariance), 0)), index=names)
    result.t = result.coef / result.se
    result.p = pd.Series(2 * norm.sf(np.abs(result.t)), index=names)
    for name in ("se", "t", "p"):
        result.tidy[name] = getattr(result, name).to_numpy()
    result.tidy["se_type"] = "hodrick_1b"
    return result
