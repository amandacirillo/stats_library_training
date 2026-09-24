"""Rescaling utilities for a single numeric series."""
import pandas as pd


def z_scores(scores: pd.Series, ddof: int = 1) -> pd.Series:
    """Convert a series of raw scores into z-scores (standard scores).

    Args:
        scores: A pandas Series of numeric values.
        ddof: Delta degrees of freedom used for the standard deviation
            calculation. Defaults to ``1`` (sample standard deviation).

    Returns:
        A Series the same shape as ``scores``, where each value has been
        replaced by ``(value - mean) / std_dev``.

    Raises:
        ValueError: If the standard deviation of ``scores`` is zero.
    """
    std_dev = scores.std(ddof=ddof)
    if std_dev == 0:
        raise ValueError("z_scores is undefined when the series has zero variance")
    return (scores - scores.mean()) / std_dev


def min_max_scale(scores: pd.Series) -> pd.Series:
    """Rescale a series of scores to the ``[0.0, 1.0]`` range.

    Args:
        scores: A pandas Series of numeric values.

    Returns:
        A Series the same shape as ``scores``, linearly rescaled so its
        minimum value maps to ``0.0`` and its maximum maps to ``1.0``.

    Raises:
        ValueError: If every value in ``scores`` is identical (making the
            range zero).
    """
    lo, hi = scores.min(), scores.max()
    if hi == lo:
        raise ValueError("min_max_scale is undefined when all values are identical")
    return (scores - lo) / (hi - lo)
