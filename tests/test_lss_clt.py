"""Basic tests for two-dimensional LSS-CLT utilities."""

import numpy as np
import pandas as pd
import pytest

from src.lss_clt import (
    centered_lss_vector,
    compute_lss_mean_cov,
    linear_spectral_statistic,
    run_lss_clt_experiment,
    simulate_lss_samples,
    theoretical_lss_mean_cov,
)


def test_linear_spectral_statistic_second_power():
    """L_N(x^2) is the mean of squared Wigner matrix eigenvalues."""
    assert linear_spectral_statistic([1, 2, 3], 2) == pytest.approx(14 / 3)


def test_centered_lss_vector_shape():
    """The two-dimensional LSS vector has shape (2,)."""
    vector = centered_lss_vector(np.array([-1.0, 0.0, 1.0]))
    assert vector.shape == (2,)


def test_simulate_lss_samples_shape():
    """Small LSS-CLT simulation returns one row per Wigner matrix sample."""
    samples = simulate_lss_samples(n=5, num_samples=3, seed=0)
    assert samples.shape == (3, 2)


def test_compute_lss_mean_cov_shapes():
    """LSS-CLT sample mean vector and sample covariance matrix have correct shapes."""
    samples = np.array([[0.0, 1.0], [2.0, 3.0], [4.0, 5.0]])
    mean_vector, cov_matrix = compute_lss_mean_cov(samples)
    assert mean_vector.shape == (2,)
    assert cov_matrix.shape == (2, 2)


def test_theoretical_lss_mean_cov_shapes():
    """The thesis reference LSS-CLT mean and covariance have expected shapes."""
    mean_vector, cov_matrix = theoretical_lss_mean_cov()
    assert mean_vector.shape == (2,)
    assert cov_matrix.shape == (2, 2)


def test_run_lss_clt_experiment_small_parameters_returns_results():
    """Small LSS-CLT experiment returns samples by N and a summary table."""
    samples_by_n, summary_df = run_lss_clt_experiment(
        matrix_sizes=(5, 6),
        num_samples=3,
        seed=0,
    )
    assert set(samples_by_n) == {5, 6}
    assert all(samples.shape == (3, 2) for samples in samples_by_n.values())
    assert isinstance(summary_df, pd.DataFrame)


def test_run_lss_clt_experiment_summary_columns():
    """LSS-CLT summary table contains sample and theoretical comparison columns."""
    _, summary_df = run_lss_clt_experiment(
        matrix_sizes=(5,),
        num_samples=3,
        seed=0,
    )
    expected_columns = [
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
    ]
    assert list(summary_df.columns) == expected_columns
