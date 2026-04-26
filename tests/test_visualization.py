"""Basic tests for visualization utilities."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from src.visualization import (
    plot_ks_convergence,
    plot_lss_2d_scatter,
    plot_moment_convergence,
    plot_spectral_histogram,
    plot_universality_comparison,
    save_figure,
)


def test_plot_spectral_histogram_creates_png(tmp_path):
    """Spectral histogram comparison with the semicircle law is saved as PNG."""
    output_path = tmp_path / "spectral_histogram.png"
    plot_spectral_histogram([-1.0, -0.5, 0.0, 0.5, 1.0], output_path, bins=5)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_plot_spectral_histogram_empty_raises(tmp_path):
    """An empty eigenvalue array cannot define a spectral histogram."""
    with pytest.raises(ValueError):
        plot_spectral_histogram([], tmp_path / "empty.png")


def test_plot_moment_convergence_creates_png(tmp_path):
    """Moment convergence to Catalan theoretical values is saved as PNG."""
    output_path = tmp_path / "moment_convergence.png"
    results_df = pd.DataFrame(
        {
            "n": [5, 8, 5, 8],
            "order": [2, 2, 4, 4],
            "mean_empirical_moment": [0.8, 0.9, 1.6, 1.8],
            "theoretical_moment": [1, 1, 2, 2],
        }
    )
    plot_moment_convergence(results_df, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_plot_moment_convergence_missing_columns_raises(tmp_path):
    """Moment convergence plotting requires the experiment output columns."""
    results_df = pd.DataFrame({"n": [5], "order": [2]})
    with pytest.raises(ValueError):
        plot_moment_convergence(results_df, tmp_path / "invalid.png")


def test_save_figure_creates_file(tmp_path):
    """The shared save helper writes and closes a matplotlib figure."""
    output_path = tmp_path / "figure.png"
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    save_figure(fig, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_plot_ks_convergence_creates_png(tmp_path):
    """KS convergence with standard deviation error bars is saved as PNG."""
    output_path = tmp_path / "ks_convergence.png"
    results_df = pd.DataFrame(
        {
            "n": [10, 20],
            "mean_ks_distance": [0.3, 0.2],
            "std_ks_distance": [0.05, 0.03],
        }
    )
    plot_ks_convergence(results_df, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_plot_universality_comparison_creates_png(tmp_path):
    """Universality comparison figure is saved as PNG."""
    output_path = tmp_path / "universality_comparison.png"
    eigenvalues_by_dist = {
        "gaussian": [-1.0, 0.0, 1.0],
        "rademacher": [-0.8, 0.0, 0.8],
        "uniform": [-0.9, 0.0, 0.9],
    }
    plot_universality_comparison(eigenvalues_by_dist, output_path, bins=3)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_plot_lss_2d_scatter_creates_png(tmp_path):
    """LSS-CLT scatter panels with mean and covariance ellipse are saved as PNG."""
    output_path = tmp_path / "lss_clt_2d_scatter.png"
    samples_by_n = {
        5: [[0.0, 1.0], [1.0, 2.0], [-1.0, 0.0]],
        8: [[0.5, 1.5], [1.5, 2.5], [-0.5, 0.5]],
    }
    plot_lss_2d_scatter(samples_by_n, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0
