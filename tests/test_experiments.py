"""Basic tests for experiment entry points."""

from pathlib import Path

import pandas as pd

from src.experiments import (
    parse_int_tuple,
    run_ks_convergence_experiment,
    run_moment_experiment,
    run_semicircle_experiment,
    run_universality_experiment,
)


def test_run_semicircle_experiment_creates_png(tmp_path):
    """Small semicircle law histogram experiment generates a figure."""
    output_path = run_semicircle_experiment(n=20, output_dir=tmp_path, seed=0)
    assert isinstance(output_path, Path)
    assert output_path.exists()
    assert output_path.name == "semicircle_histogram.png"


def test_run_ks_convergence_experiment_returns_expected_columns(tmp_path):
    """Small KS convergence experiment returns the expected result table."""
    result = run_ks_convergence_experiment(
        matrix_sizes=(10, 15),
        num_trials=2,
        output_dir=tmp_path,
        seed=0,
    )
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["n", "mean_ks_distance", "num_trials", "dist"]
    assert (tmp_path / "ks_convergence.csv").exists()


def test_run_moment_experiment_creates_csv_and_png(tmp_path):
    """Small moment convergence experiment saves a table and a figure."""
    result = run_moment_experiment(
        matrix_sizes=(10, 15),
        orders=(2, 4),
        num_trials=2,
        output_dir=tmp_path,
        seed=0,
    )
    assert isinstance(result, pd.DataFrame)
    assert (tmp_path / "tables" / "moment_convergence.csv").exists()
    assert (tmp_path / "figures" / "moment_convergence.png").exists()


def test_run_universality_experiment_creates_multiple_png_files(tmp_path):
    """Small universality experiment saves one spectral figure per distribution."""
    output_paths = run_universality_experiment(n=20, output_dir=tmp_path, seed=0)
    assert set(output_paths) == {"gaussian", "rademacher", "uniform"}
    for output_path in output_paths.values():
        assert output_path.exists()
        assert output_path.suffix == ".png"


def test_parse_int_tuple_from_comma_separated_string():
    """Comma-separated matrix-size and order parameters parse to tuples."""
    assert parse_int_tuple("50,100,200") == (50, 100, 200)
