"""Basic tests for Wigner matrix utilities."""

from src.wigner_matrix import compute_eigenvalues, generate_wigner_real


def test_generate_wigner_real_placeholder():
    """Placeholder test for Wigner matrix generation."""
    assert generate_wigner_real(2) is None


def test_compute_eigenvalues_placeholder():
    """Placeholder test for eigenvalue computation."""
    assert compute_eigenvalues([[1, 0], [0, 1]]) is None
