"""Basic tests for Wigner matrix utilities."""

import numpy as np
import pytest

from src.wigner_matrix import (
    compute_eigenvalues,
    empirical_spectral_distribution,
    generate_wigner_real,
)


def test_generate_wigner_real_shape():
    """Generated Wigner matrix has shape (n, n)."""
    n = 8
    matrix = generate_wigner_real(n, seed=0)
    assert matrix.shape == (n, n)


def test_generate_wigner_real_is_symmetric():
    """Generated real Wigner matrix is symmetric."""
    matrix = generate_wigner_real(10, seed=1)
    assert np.allclose(matrix, matrix.T)


def test_generate_wigner_real_same_seed_is_reproducible():
    """The same seed gives the same Wigner matrix."""
    first = generate_wigner_real(6, seed=2)
    second = generate_wigner_real(6, seed=2)
    assert np.array_equal(first, second)


@pytest.mark.parametrize("dist", ["gaussian", "rademacher", "uniform"])
def test_generate_wigner_real_supported_distributions(dist):
    """Supported entry distributions can generate real Wigner matrices."""
    matrix = generate_wigner_real(5, dist=dist, seed=3)
    assert matrix.shape == (5, 5)
    assert np.allclose(matrix, matrix.T)


def test_generate_wigner_real_invalid_distribution_raises():
    """Unsupported entry distributions raise ValueError."""
    with pytest.raises(ValueError):
        generate_wigner_real(4, dist="unsupported")


@pytest.mark.parametrize("n", [0, -1])
def test_generate_wigner_real_invalid_n_raises(n):
    """Non-positive matrix sizes raise ValueError."""
    with pytest.raises(ValueError):
        generate_wigner_real(n)


def test_compute_eigenvalues_returns_real_values_with_length_n():
    """Eigenvalue computation returns n real eigenvalues."""
    n = 7
    matrix = generate_wigner_real(n, seed=4)
    eigenvalues = compute_eigenvalues(matrix)
    assert eigenvalues.shape == (n,)
    assert np.isrealobj(eigenvalues)


def test_compute_eigenvalues_non_square_raises():
    """Non-square inputs cannot define a square Wigner spectrum."""
    with pytest.raises(ValueError):
        compute_eigenvalues(np.ones((2, 3)))


def test_empirical_spectral_distribution_returns_sorted_values():
    """Empirical spectral distribution support points are sorted."""
    eigenvalues = np.array([0.5, -1.0, 0.0, 2.0])
    support = empirical_spectral_distribution(eigenvalues)
    assert np.array_equal(support, np.array([-1.0, 0.0, 0.5, 2.0]))


def test_empirical_spectral_distribution_empty_raises():
    """An empty eigenvalue array cannot define an empirical spectrum."""
    with pytest.raises(ValueError):
        empirical_spectral_distribution(np.array([]))
