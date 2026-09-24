import pandas as pd
import pytest

from statlib.correlation import correlation_matrix, pearson_correlation


def test_pearson_correlation_perfect_positive() -> None:
    x = pd.Series([1, 2, 3, 4, 5])
    y = pd.Series([2, 4, 6, 8, 10])
    assert pearson_correlation(x, y) == pytest.approx(1.0)


def test_pearson_correlation_perfect_negative() -> None:
    x = pd.Series([1, 2, 3, 4, 5])
    y = pd.Series([10, 8, 6, 4, 2])
    assert pearson_correlation(x, y) == pytest.approx(-1.0)


def test_pearson_correlation_drops_misaligned_nans() -> None:
    x = pd.Series([1.0, 2.0, None, 4.0])
    y = pd.Series([10.0, 20.0, 30.0, None])
    # Only the first two rows have both values present.
    assert pearson_correlation(x, y) == pytest.approx(1.0)


def test_pearson_correlation_raises_on_length_mismatch() -> None:
    with pytest.raises(ValueError):
        pearson_correlation(pd.Series([1, 2, 3]), pd.Series([1, 2]))


def test_pearson_correlation_raises_on_zero_variance() -> None:
    with pytest.raises(ValueError):
        pearson_correlation(pd.Series([1, 1, 1]), pd.Series([1, 2, 3]))


def test_correlation_matrix_is_symmetric_with_unit_diagonal() -> None:
    data = pd.DataFrame({
        "a": [1, 2, 3, 4],
        "b": [4, 3, 2, 1],
        "c": [1, 3, 2, 4],
    })
    matrix = correlation_matrix(data)

    assert matrix.loc["a", "a"] == pytest.approx(1.0)
    assert matrix.loc["a", "b"] == pytest.approx(matrix.loc["b", "a"])
    assert matrix.loc["a", "b"] == pytest.approx(-1.0)
