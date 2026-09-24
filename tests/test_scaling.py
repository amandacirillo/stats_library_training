import pandas as pd
import pytest

from statlib.scaling import min_max_scale, z_scores


def test_z_scores_centers_and_scales() -> None:
    scores = pd.Series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    result = z_scores(scores)

    assert result.mean() == pytest.approx(0.0, abs=1e-9)
    assert result.std(ddof=1) == pytest.approx(1.0)


def test_z_scores_raises_on_zero_variance() -> None:
    with pytest.raises(ValueError):
        z_scores(pd.Series([5.0, 5.0, 5.0]))


def test_min_max_scale_maps_to_unit_range() -> None:
    scores = pd.Series([10.0, 20.0, 30.0, 40.0])
    result = min_max_scale(scores)

    assert result.min() == pytest.approx(0.0)
    assert result.max() == pytest.approx(1.0)
    assert result.iloc[1] == pytest.approx(1.0 / 3.0)


def test_min_max_scale_raises_when_all_values_identical() -> None:
    with pytest.raises(ValueError):
        min_max_scale(pd.Series([7.0, 7.0, 7.0]))
