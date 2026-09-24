import pandas as pd
import pytest

from statlib.descriptive import summary_stats, standard_error_of_mean


def test_summary_stats_computes_expected_values() -> None:
    scores = pd.Series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    result = summary_stats(scores)

    assert result["n"] == 8
    assert result["mean"] == pytest.approx(5.0)
    assert result["variance"] == pytest.approx(4.5714, abs=1e-4)
    assert result["std_dev"] == pytest.approx(2.1381, abs=1e-4)
    assert result["std_error"] == pytest.approx(0.7559, abs=1e-4)


def test_summary_stats_drops_nan_values() -> None:
    scores = pd.Series([1.0, None, 3.0, None, 5.0])
    result = summary_stats(scores)
    assert result["n"] == 3
    assert result["mean"] == pytest.approx(3.0)


def test_summary_stats_population_variance_with_ddof_zero() -> None:
    scores = pd.Series([1.0, 2.0, 3.0, 4.0])
    result = summary_stats(scores, ddof=0)
    assert result["variance"] == pytest.approx(1.25)


def test_summary_stats_raises_with_fewer_than_two_values() -> None:
    with pytest.raises(ValueError):
        summary_stats(pd.Series([1.0]))


def test_standard_error_of_mean_matches_summary_stats() -> None:
    scores = pd.Series([10.0, 12.0, 14.0, 16.0, 18.0])
    assert standard_error_of_mean(scores) == pytest.approx(summary_stats(scores)["std_error"])
