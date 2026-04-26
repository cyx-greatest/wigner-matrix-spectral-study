"""Basic tests for moment utilities."""

import pandas as pd
import pytest

from src.moments import (
    catalan_number,
    empirical_moment,
    moment_errors,
    run_moment_convergence_experiment,
    theoretical_semicircle_moment,
)


@pytest.mark.parametrize("k, expected", [(0, 1), (1, 1), (2, 2), (3, 5)])
def test_catalan_number_values(k, expected):
    """Catalan numbers match the values used for semicircle even moments."""
    assert catalan_number(k) == expected


@pytest.mark.parametrize(
    "order, expected",
    [(0, 1), (1, 0), (2, 1), (4, 2), (6, 5)],
)
def test_theoretical_semicircle_moment_values(order, expected):
    """Semicircle distribution moments follow Catalan numbers."""
    assert theoretical_semicircle_moment(order) == expected


def test_empirical_moment_first_order():
    """The first empirical moment is the average of eigenvalues."""
    assert empirical_moment([1, 2, 3], 1) == pytest.approx(2.0)


def test_empirical_moment_second_order():
    """The second empirical moment is the average of squared eigenvalues."""
    assert empirical_moment([1, 2, 3], 2) == pytest.approx(14 / 3)


def test_empirical_moment_empty_eigenvalues_raises():
    """An empty eigenvalue array cannot define an empirical moment."""
    with pytest.raises(ValueError):
        empirical_moment([], 2)


@pytest.mark.parametrize("order", [-1, 1.5, "2"])
def test_invalid_order_raises(order):
    """Moment order must be a non-negative integer."""
    with pytest.raises(ValueError):
        theoretical_semicircle_moment(order)


def test_moment_errors_returns_expected_columns():
    """Moment error comparison returns the expected DataFrame columns."""
    result = moment_errors([1, 2, 3], [1, 2])
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "order",
        "empirical_moment",
        "theoretical_moment",
        "absolute_error",
    ]


def test_run_moment_convergence_experiment_small_parameters():
    """Small moment convergence experiment runs and returns expected columns."""
    result = run_moment_convergence_experiment(
        matrix_sizes=[5, 8],
        orders=[2, 4],
        num_trials=2,
        seed=0,
    )
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "n",
        "order",
        "mean_empirical_moment",
        "theoretical_moment",
        "absolute_error",
    ]
    assert len(result) == 4
