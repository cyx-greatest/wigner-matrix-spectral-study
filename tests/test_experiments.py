"""Basic tests for experiment entry points."""

from pathlib import Path

import pandas as pd

from src.experiments import (
    THESIS_PRESETS,
    parse_int_tuple,
    run_ks_convergence_experiment,
    run_lss_clt_experiment,
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
    assert list(result.columns) == [
        "n",
        "mean_ks_distance",
        "std_ks_distance",
        "num_trials",
        "dist",
    ]
    assert (tmp_path / "tables" / "ks_convergence.csv").exists()
    assert (tmp_path / "figures" / "ks_convergence.png").exists()


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
    """Small universality experiment saves the comparison figure."""
    output_path = run_universality_experiment(n=20, repeats=2, output_dir=tmp_path, seed=0)
    assert output_path.exists()
    assert output_path.name == "universality_comparison.png"


def test_parse_int_tuple_from_comma_separated_string():
    """Comma-separated matrix-size and order parameters parse to tuples."""
    assert parse_int_tuple("50,100,200") == (50, 100, 200)


def test_run_lss_clt_experiment_creates_summary_and_figures(tmp_path):
    """Small LSS-CLT experiment saves thesis-named summary and figures."""
    result = run_lss_clt_experiment(
        matrix_sizes=(5, 6),
        num_samples=3,
        output_dir=tmp_path,
        seed=0,
    )
    assert isinstance(result, pd.DataFrame)
    assert (tmp_path / "tables" / "lss_clt_summary.csv").exists()
    assert (tmp_path / "figures" / "lss_clt_2d_scatter.png").exists()
    assert (tmp_path / "figures" / "lss_clt_2d_mean.png").exists()
    assert (tmp_path / "figures" / "lss_clt_2d_cov.png").exists()


def test_thesis_preset_contains_literature_parameters():
    """Thesis preset stores formal parameters without running large experiments."""
    assert THESIS_PRESETS["ks"]["matrix_sizes"] == (50, 100, 200, 400, 800, 1600)
    assert THESIS_PRESETS["ks"]["num_trials"] == 20
    assert THESIS_PRESETS["universality"]["n"] == 400
    assert THESIS_PRESETS["universality"]["repeats"] == 10
    assert THESIS_PRESETS["lss_clt"]["matrix_sizes"] == (50, 100, 200, 400, 800)
    assert THESIS_PRESETS["lss_clt"]["num_trials"] == 1000
