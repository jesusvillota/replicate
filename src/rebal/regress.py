"""OLS and next-trading-day predictive regressions.

Uses small, in-memory statsmodels designs. See docs/methods/regressions.md and
contracts/exhibits.md for timing, covariance and tidy-output conventions.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

DEFAULT_SAMPLE = ("1997-09-10", "2023-03-17")
TABLE_COLUMNS = [
    "exhibit",
    "column",
    "term",
    "coef",
    "se",
    "t",
    "p",
    "nobs",
    "adj_r2",
    "se_type",
    "sample_start",
    "sample_end",
]


@dataclass
class RegressionResult:
    coef: pd.Series
    se: pd.Series
    t: pd.Series
    p: pd.Series
    nobs: int
    adj_r2: float
    tidy: pd.DataFrame
    covariance: pd.DataFrame
    design: pd.DataFrame

    def contrast(self, terms: Sequence[str], name: str) -> pd.DataFrame:
        """Report a coefficient sum, including all covariance cross terms."""
        weights = np.array([float(term in terms) for term in self.coef.index])
        coef = float(weights @ self.coef)
        se = float(np.sqrt(max(0, weights @ self.covariance @ weights)))
        t = coef / se if se else np.nan
        row = self.tidy.iloc[[0]].copy()
        row.loc[:, ["term", "coef", "se", "t", "p"]] = [
            name,
            coef,
            se,
            t,
            2 * norm.sf(abs(t)),
        ]
        return row


def ols(
    y: pd.Series, X: pd.DataFrame, se: str = "hc1", hac_lags: int | None = None
) -> RegressionResult:
    """Fit an intercept and named regressors with HC0, HC1 or Newey–West SEs.

    Missing/nonfinite observations are removed jointly. Pandas inputs align by
    index. HAC uses the Bartlett kernel without a small-sample correction.
    """
    if se not in {"hc0", "hc1", "hac"}:
        raise ValueError("se must be hc0, hc1 or hac")
    if hac_lags is not None and (not isinstance(hac_lags, int) or hac_lags < 0):
        raise ValueError("hac_lags must be a nonnegative integer")
    if not X.columns.is_unique or "const" in X:
        raise ValueError("regressors must have unique names and exclude const")
    # pandas: small statsmodels matrices require named, index-aligned columns.
    data = X.astype(float).copy()
    data["__outcome__"] = y
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    design = sm.add_constant(data.drop(columns="__outcome__"), has_constant="add")
    if len(design) <= design.shape[1]:
        raise ValueError("not enough complete observations for OLS")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("regression design is rank deficient")
    cov_kwds = {}
    if se == "hac":
        lags = (
            hac_lags
            if hac_lags is not None
            else int(np.floor(4 * (len(data) / 100) ** (2 / 9)))
        )
        cov_kwds = {"maxlags": lags, "kernel": "bartlett", "use_correction": False}
    fit = sm.OLS(data["__outcome__"], design).fit(
        cov_type=se.upper() if se != "hac" else "HAC",
        cov_kwds=cov_kwds,
        use_t=False,
    )
    tidy = pd.DataFrame(
        {
            "exhibit": "",
            "column": "",
            "term": fit.params.index,
            "coef": fit.params.to_numpy(),
            "se": fit.bse.to_numpy(),
            "t": fit.tvalues.to_numpy(),
            "p": fit.pvalues.to_numpy(),
            "nobs": int(fit.nobs),
            "adj_r2": fit.rsquared_adj,
            "se_type": se,
            "sample_start": "",
            "sample_end": "",
        }
    )[TABLE_COLUMNS]
    if isinstance(design.index, pd.DatetimeIndex):
        tidy["sample_start"] = design.index.min().date().isoformat()
        tidy["sample_end"] = design.index.max().date().isoformat()
    return RegressionResult(
        fit.params,
        fit.bse,
        fit.tvalues,
        fit.pvalues,
        int(fit.nobs),
        float(fit.rsquared_adj),
        tidy,
        fit.cov_params(),
        design,
    )


def dated(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate the contract date key without sorting or hiding duplicate days."""
    # pandas: contract validation and date indexing for small OLS inputs.
    result = frame.set_index("date").copy()
    result.index = pd.DatetimeIndex(result.index)
    if (
        result.index.hasnans
        or result.index.tz is not None
        or not result.index.is_unique
        or not result.index.is_monotonic_increasing
    ):
        raise ValueError("dates must be sorted, unique, nonmissing and naive")
    return result


def predictive_data(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    terms: Sequence[str],
    y: str = "ret",
    lead: int = 1,
    sample: tuple[str, str] = DEFAULT_SAMPLE,
    subset: pd.Series | np.ndarray | None = None,
) -> tuple[pd.Series, pd.DataFrame, pd.Series]:
    """Align before selecting a sample; retain dates of both sides of each pair."""
    if not isinstance(lead, int) or lead < 0:
        raise ValueError("lead must be a nonnegative integer")
    s, p = dated(signals), dated(panel)
    if not s.index.isin(p.index).all():
        raise ValueError("signal dates must belong to the panel trading calendar")
    # pandas: date alignment, interactions and missing-value masks feed statsmodels.
    data = p.join(s, how="left", rsuffix="__signal")
    for name in s.columns.intersection(p.columns):
        data[name] = data.pop(f"{name}__signal")
    design = pd.DataFrame(index=data.index)
    for term in terms:
        factors = term.split(":")
        design[term] = data[factors].prod(axis=1, skipna=False)
    response = data[y].shift(-lead)
    outcome_dates = pd.Series(data.index, index=data.index).shift(-lead)
    start, end = sample
    end_date = data.index.max() if end == "latest" else pd.Timestamp(end)
    mask = (
        (data.index >= pd.Timestamp(start))
        & (data.index <= end_date)
        & outcome_dates.between(pd.Timestamp(start), end_date)
    )
    if subset is not None:
        if not pd.api.types.is_bool_dtype(pd.Series(subset).dtype):
            raise ValueError("subset must be boolean")
        if isinstance(subset, pd.Series) and isinstance(subset.index, pd.DatetimeIndex):
            selected = subset.reindex(data.index)
        else:
            if len(subset) != len(s):
                raise ValueError("subset must have one boolean per signal date")
            selected = pd.Series(np.asarray(subset), index=s.index).reindex(data.index)
        mask &= selected.astype("boolean").fillna(False).astype(bool)
    mask &= np.isfinite(design).all(axis=1) & np.isfinite(response)
    return response.loc[mask], design.loc[mask], outcome_dates.loc[mask]


def predictive(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    terms: Sequence[str],
    y: str = "ret",
    lead: int = 1,
    sample: tuple[str, str] = DEFAULT_SAMPLE,
    subset: pd.Series | np.ndarray | None = None,
    *,
    se: str = "hc1",
    hac_lags: int | None = None,
) -> RegressionResult:
    """Regress y[t+lead] on terms[t], never shift after filtering a subset."""
    response, design, dates = predictive_data(
        signals, panel, terms, y, lead, sample, subset
    )
    result = ols(response, design, se, hac_lags)
    result.tidy["sample_start"] = dates.min().date().isoformat()
    result.tidy["sample_end"] = dates.max().date().isoformat()
    return result
