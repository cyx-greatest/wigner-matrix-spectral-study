"""Moment calculations for empirical spectra and the semicircle law."""

from math import comb

import numpy as np
import pandas as pd

from src.wigner_matrix import compute_eigenvalues, generate_wigner_real


def _validate_nonnegative_integer(value, name):
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer.")


def catalan_number(k):
    """Compute the k-th Catalan number for semicircle distribution moments.

    The Catalan number is C_k = binom(2k, k) / (k + 1). In the moment method
    for the semicircle law, the even semicircle distribution moment m_{2k}
    equals C_k.
    """
    _validate_nonnegative_integer(k, "k")
    return comb(2 * k, k) // (k + 1)


def theoretical_semicircle_moment(order):
    """Return the theoretical semicircle distribution moment of a given order.

    Odd moments of the semicircle distribution are 0, while the even moment
    m_{2k} equals the Catalan number C_k.
    """
    _validate_nonnegative_integer(order, "order")

    if order % 2 == 1:
        return 0
    return catalan_number(order // 2)


def empirical_moment(eigenvalues, order):
    """Compute the empirical moment of Wigner matrix eigenvalues.

    For eigenvalues lambda_i, the empirical moment is
    m_k^N = (1 / N) sum_i lambda_i^k, used to compare empirical spectral
    moments with the theoretical semicircle distribution moments.
    """
    _validate_nonnegative_integer(order, "order")
    values = np.asarray(eigenvalues, dtype=float).reshape(-1)

    if values.size == 0:
        raise ValueError("eigenvalues must be non-empty.")

    return float(np.mean(values**order))


def moment_errors(eigenvalues, orders):
    """Compare empirical moments with semicircle distribution moments."""
    rows = []
    for order in orders:
        empirical = empirical_moment(eigenvalues, order)
        theoretical = theoretical_semicircle_moment(order)
        rows.append(
            {
                "order": order,
                "empirical_moment": empirical,
                "theoretical_moment": theoretical,
                "absolute_error": abs(empirical - theoretical),
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "order",
            "empirical_moment",
            "theoretical_moment",
            "absolute_error",
        ],
    )


def run_moment_convergence_experiment(
    matrix_sizes, orders, num_trials=20, dist="gaussian", seed=None
):
    """Run a numerical experiment for convergence of empirical moments.

    For each matrix size N and each moment order, the experiment generates
    real symmetric Wigner matrices, computes eigenvalues, averages empirical
    moments over trials, and compares them with the corresponding semicircle
    distribution moments.
    """
    _validate_nonnegative_integer(num_trials, "num_trials")
    if num_trials == 0:
        raise ValueError("num_trials must be positive.")

    rng = np.random.default_rng(seed)
    rows = []

    for n in matrix_sizes:
        if not isinstance(n, int) or n <= 0:
            raise ValueError("matrix sizes must be positive integers.")

        for order in orders:
            _validate_nonnegative_integer(order, "order")
            trial_moments = []

            for _ in range(num_trials):
                trial_seed = int(rng.integers(0, np.iinfo(np.uint32).max))
                matrix = generate_wigner_real(n, dist=dist, seed=trial_seed)
                eigenvalues = compute_eigenvalues(matrix)
                trial_moments.append(empirical_moment(eigenvalues, order))

            mean_empirical = float(np.mean(trial_moments))
            theoretical = theoretical_semicircle_moment(order)
            rows.append(
                {
                    "n": n,
                    "order": order,
                    "mean_empirical_moment": mean_empirical,
                    "theoretical_moment": theoretical,
                    "absolute_error": abs(mean_empirical - theoretical),
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "n",
            "order",
            "mean_empirical_moment",
            "theoretical_moment",
            "absolute_error",
        ],
    )
