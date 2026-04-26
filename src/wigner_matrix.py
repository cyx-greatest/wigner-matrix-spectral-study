"""Generation and spectral computation utilities for real Wigner matrices."""

import numpy as np


def generate_wigner_real(n, dist="gaussian", seed=None):
    """Generate an n by n real symmetric Wigner matrix.

    The unscaled matrix has independent upper-triangular entries, with
    off-diagonal entries of mean 0 and variance 1. The returned Wigner matrix
    is normalized by 1 / sqrt(n), as used in empirical spectral distribution
    experiments for the semicircle law.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer.")

    rng = np.random.default_rng(seed)

    if dist == "gaussian":
        upper = rng.normal(loc=0.0, scale=1.0, size=(n, n))
    elif dist == "rademacher":
        upper = rng.choice([-1.0, 1.0], size=(n, n))
    elif dist == "uniform":
        upper = rng.uniform(-np.sqrt(3.0), np.sqrt(3.0), size=(n, n))
    else:
        raise ValueError("dist must be one of: 'gaussian', 'rademacher', 'uniform'.")

    matrix = np.triu(upper)
    matrix = matrix + matrix.T - np.diag(np.diag(matrix))
    return matrix / np.sqrt(n)


def compute_eigenvalues(matrix):
    """Compute all real eigenvalues of a real symmetric Wigner matrix."""
    array = np.asarray(matrix)

    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise ValueError("matrix must be a two-dimensional square array.")

    return np.linalg.eigvalsh(array)


def empirical_spectral_distribution(eigenvalues):
    """Return sorted support points of the empirical spectral distribution.

    For eigenvalues lambda_i, this represents the support points of
    L_N = (1 / N) sum_i delta_{lambda_i}; no probability measure object is
    constructed.
    """
    values = np.asarray(eigenvalues)

    if values.size == 0:
        raise ValueError("eigenvalues must be non-empty.")

    return np.sort(values.reshape(-1))
