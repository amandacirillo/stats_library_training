"""Basic descriptive statistics over a single numeric series.

This module intentionally covers only simple, well-known descriptive
statistics (mean, variance, standard error). It exists to give the
Sphinx documentation build and the packaging/CI pipeline something real
to compile and publish -- the actual proprietary scoring/psychometric
calculations this training is based on are not reproduced here.
"""
import math
from typing import Dict

import pandas as pd


def summary_stats(scores: pd.Series, ddof: int = 1) -> Dict[str, float]:
    """Compute basic descriptive statistics for a series of numeric scores.

    Args:
        scores: A pandas Series of numeric values. NaNs are dropped before
            any statistic is computed.
        ddof: Delta degrees of freedom used for the variance/standard
            deviation calculation. The default of ``1`` computes the
            sample variance; pass ``0`` for the population variance.

    Returns:
        A dict with keys ``n``, ``mean``, ``variance``, ``std_dev``, and
        ``std_error`` (the standard error of the mean).

    Raises:
        ValueError: If ``scores`` has fewer than two non-null values.

    Examples:
        >>> import pandas as pd
        >>> summary_stats(pd.Series([1.0, 2.0, 3.0, 4.0]))["mean"]
        2.5
    """
    clean = scores.dropna()
    n = len(clean)
    if n < 2:
        raise ValueError("summary_stats requires at least two non-null values")

    values = clean.to_numpy(dtype=float)
    mean = float(values.mean())
    variance = float(values.var(ddof=ddof))
    std_dev = math.sqrt(variance)
    std_error = std_dev / math.sqrt(n)

    return {
        "n": n,
        "mean": mean,
        "variance": variance,
        "std_dev": std_dev,
        "std_error": std_error,
    }


def standard_error_of_mean(scores: pd.Series, ddof: int = 1) -> float:
    """Compute the standard error of the mean for a series of scores.

    Args:
        scores: A pandas Series of numeric values. NaNs are dropped.
        ddof: Delta degrees of freedom used for the underlying variance
            calculation. See :func:`summary_stats`.

    Returns:
        The standard error of the mean as a float.
    """
    return summary_stats(scores, ddof=ddof)["std_error"]
