"""Basic tests for semicircle law utilities."""

from src.semicircle_law import (
    ks_distance_to_semicircle,
    semicircle_cdf,
    semicircle_density,
)


def test_semicircle_density_placeholder():
    """Placeholder test for semicircle density."""
    assert semicircle_density(0) is None


def test_semicircle_cdf_placeholder():
    """Placeholder test for semicircle CDF."""
    assert semicircle_cdf(0) is None


def test_ks_distance_to_semicircle_placeholder():
    """Placeholder test for KS distance."""
    assert ks_distance_to_semicircle([0, 1]) is None
