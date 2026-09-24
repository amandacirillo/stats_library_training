"""Correlation utilities between one or more numeric series."""
import pandas as pd


def pearson_correlation(x: pd.Series, y: pd.Series) -> float:
    """Compute the Pearson product-moment correlation coefficient.

    Args:
        x: First numeric series.
        y: Second numeric series, aligned index-for-index with ``x``.

    Returns:
        The Pearson correlation coefficient between ``x`` and ``y`` as a
        float in the range ``[-1.0, 1.0]``.

    Raises:
        ValueError: If ``x`` and ``y`` are not the same length, or if
            either has zero variance (making the correlation undefined).

    Examples:
        >>> import pandas as pd
        >>> pearson_correlation(pd.Series([1, 2, 3]), pd.Series([2, 4, 6]))
        1.0
    """
    if len(x) != len(y):
        raise ValueError("x and y must be the same length")

    aligned = pd.DataFrame({"x": x.values, "y": y.values}).dropna()
    if aligned["x"].std() == 0 or aligned["y"].std() == 0:
        raise ValueError("correlation is undefined when a series has zero variance")

    return float(aligned["x"].corr(aligned["y"]))


def correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """Compute a pairwise Pearson correlation matrix for a DataFrame's columns.

    Args:
        data: A DataFrame of numeric columns.

    Returns:
        A square DataFrame of pairwise Pearson correlation coefficients,
        indexed and columned by ``data``'s column names.
    """
    return data.corr(method="pearson")
