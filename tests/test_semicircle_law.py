"""Basic tests for semicircle law utilities."""

import numpy as np
import pytest

from src.semicircle_law import (
    empirical_cdf_values,
    ks_distance_to_semicircle,
    semicircle_cdf,
    semicircle_density,
)


def test_semicircle_density_at_zero():
    """The standard semicircle law density at 0 equals 1 / pi."""
    assert semicircle_density(0) == pytest.approx(1.0 / np.pi)


@pytest.mark.parametrize("x", [-2, 2])
def test_semicircle_density_at_edges(x):
    """The semicircle law density vanishes at the spectral edges."""
    assert semicircle_density(x) == pytest.approx(0.0)


@pytest.mark.parametrize("x", [-3, 3])
def test_semicircle_density_outside_support(x):
    """The semicircle law density is 0 outside [-2, 2]."""
    assert semicircle_density(x) == pytest.approx(0.0)


def test_semicircle_density_array_input():
    """Array input returns vectorized semicircle law density values."""
    density = semicircle_density(np.array([-3.0, 0.0, 3.0]))
    assert isinstance(density, np.ndarray)
    assert np.array_equal(density[[0, 2]], np.array([0.0, 0.0]))
    assert density[1] == pytest.approx(1.0 / np.pi)


def test_semicircle_cdf_at_left_edge():
    """The semicircle law CDF equals 0 at -2."""
    assert semicircle_cdf(-2) == pytest.approx(0.0)


def test_semicircle_cdf_at_right_edge():
    """The semicircle law CDF equals 1 at 2."""
    assert semicircle_cdf(2) == pytest.approx(1.0)


def test_semicircle_cdf_at_zero():
    """The semicircle law CDF equals 0.5 at 0."""
    assert semicircle_cdf(0) == pytest.approx(0.5)


def test_empirical_cdf_values_returns_sorted_values_and_steps():
    """Empirical spectral distribution values pair sorted eigenvalues with i / n."""
    sorted_values, cdf_values = empirical_cdf_values(np.array([1.0, -1.0, 0.5]))
    assert np.array_equal(sorted_values, np.array([-1.0, 0.5, 1.0]))
    assert np.allclose(cdf_values, np.array([1 / 3, 2 / 3, 1.0]))


def test_empirical_cdf_values_empty_raises():
    """An empty eigenvalue array cannot define an empirical spectral distribution."""
    with pytest.raises(ValueError):
        empirical_cdf_values(np.array([]))


def test_ks_distance_to_semicircle_is_nonnegative():
    """The KS distance between F_N and F_sc is nonnegative."""
    distance = ks_distance_to_semicircle(np.array([-1.0, 0.0, 1.0]))
    assert isinstance(distance, float)
    assert distance >= 0.0
