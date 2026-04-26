"""Linear spectral statistics and CLT experiment utilities."""

import numpy as np
import pandas as pd

from src.wigner_matrix import compute_eigenvalues, generate_wigner_real


def _validate_positive_integer(value, name):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer.")


def linear_spectral_statistic(eigenvalues, power):
    """Compute L_N(x^power) for Wigner matrix eigenvalues.

    This is the linear spectral statistic used in the two-dimensional LSS-CLT
    experiment, where L_N(f) = (1 / N) sum_i f(lambda_i).
    """
    values = np.asarray(eigenvalues, dtype=float).reshape(-1)

    if values.size == 0:
        raise ValueError("eigenvalues must be non-empty.")
    _validate_positive_integer(power, "power")

    return float(np.mean(values**power))


def centered_lss_vector(eigenvalues):
    """Compute the two-dimensional centered linear spectral statistic vector.

    The vector is G_N = (G_N(x^2), G_N(x^4))^T with
    G_N(x^2) = N(L_N(x^2) - 1) and G_N(x^4) = N(L_N(x^4) - 2), using the
    semicircle moments S(x^2)=1 and S(x^4)=2.
    """
    values = np.asarray(eigenvalues, dtype=float).reshape(-1)

    if values.size == 0:
        raise ValueError("eigenvalues must be non-empty.")

    n = values.size
    g2 = n * (linear_spectral_statistic(values, 2) - 1.0)
    g4 = n * (linear_spectral_statistic(values, 4) - 2.0)
    return np.array([g2, g4], dtype=float)


def simulate_lss_samples(n, num_samples, dist="gaussian", seed=None):
    """Simulate samples for the two-dimensional Wigner matrix LSS-CLT.

    Each sample is the vector (G_N(x^2), G_N(x^4)) computed from one real
    symmetric Wigner matrix.
    """
    _validate_positive_integer(n, "n")
    _validate_positive_integer(num_samples, "num_samples")

    rng = np.random.default_rng(seed)
    samples = np.empty((num_samples, 2), dtype=float)

    for sample_index in range(num_samples):
        trial_seed = int(rng.integers(0, np.iinfo(np.uint32).max))
        matrix = generate_wigner_real(n, dist=dist, seed=trial_seed)
        eigenvalues = compute_eigenvalues(matrix)
        samples[sample_index] = centered_lss_vector(eigenvalues)

    return samples


def compute_lss_mean_cov(samples):
    """Compute the sample mean vector and sample covariance matrix for LSS-CLT."""
    values = np.asarray(samples, dtype=float)

    if values.ndim != 2 or values.shape[1] != 2 or values.shape[0] == 0:
        raise ValueError("samples must have shape (num_samples, 2).")

    mean_vector = np.mean(values, axis=0)
    if values.shape[0] == 1:
        cov_matrix = np.zeros((2, 2), dtype=float)
    else:
        cov_matrix = np.cov(values, rowvar=False)
    return mean_vector, cov_matrix


def theoretical_lss_mean_cov():
    """Return the theoretical reference mean vector and covariance matrix.

    These are the thesis reference values for the two-dimensional linear
    spectral statistics central limit theorem experiment.
    """
    mean = np.array([0.0, 1.0])
    cov = np.array([[4.0, 16.0], [16.0, 72.0]])
    return mean, cov


def run_lss_clt_experiment(
    matrix_sizes=(50, 100, 200),
    num_samples=200,
    dist="gaussian",
    seed=None,
):
    """Run the two-dimensional LSS-CLT numerical experiment.

    For each matrix dimension N, this computes samples of
    (G_N(x^2), G_N(x^4)), then records the sample mean vector and sample
    covariance matrix together with the theoretical reference values.
    """
    _validate_positive_integer(num_samples, "num_samples")

    rng = np.random.default_rng(seed)
    theoretical_mean, theoretical_cov = theoretical_lss_mean_cov()
    samples_by_n = {}
    rows = []

    for n in matrix_sizes:
        _validate_positive_integer(n, "n")
        trial_seed = int(rng.integers(0, np.iinfo(np.uint32).max))
        samples = simulate_lss_samples(
            n=n,
            num_samples=num_samples,
            dist=dist,
            seed=trial_seed,
        )
        mean_vector, cov_matrix = compute_lss_mean_cov(samples)
        samples_by_n[n] = samples
        rows.append(
            {
                "n": n,
                "mean_g2": mean_vector[0],
                "mean_g4": mean_vector[1],
                "cov_g2_g2": cov_matrix[0, 0],
                "cov_g2_g4": cov_matrix[0, 1],
                "cov_g4_g4": cov_matrix[1, 1],
                "theoretical_mean_g2": theoretical_mean[0],
                "theoretical_mean_g4": theoretical_mean[1],
                "theoretical_cov_g2_g2": theoretical_cov[0, 0],
                "theoretical_cov_g2_g4": theoretical_cov[0, 1],
                "theoretical_cov_g4_g4": theoretical_cov[1, 1],
            }
        )

    summary_df = pd.DataFrame(
        rows,
        columns=[
            "n",
            "mean_g2",
            "mean_g4",
            "cov_g2_g2",
            "cov_g2_g4",
            "cov_g4_g4",
            "theoretical_mean_g2",
            "theoretical_mean_g4",
            "theoretical_cov_g2_g2",
            "theoretical_cov_g2_g4",
            "theoretical_cov_g4_g4",
        ],
    )
    return samples_by_n, summary_df
