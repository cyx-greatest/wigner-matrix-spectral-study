"""Plotting utilities for Wigner matrix spectral experiments."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.semicircle_law import semicircle_density


def save_figure(fig, output_path):
    """Save a matplotlib figure for numerical experiments and close it."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_spectral_histogram(eigenvalues, output_path, bins=60):
    """Plot the empirical spectral histogram with the semicircle law density.

    This corresponds to the numerical comparison between the eigenvalue
    histogram of a Wigner matrix and the semicircle law density rho_sc.
    """
    values = np.asarray(eigenvalues, dtype=float).reshape(-1)

    if values.size == 0:
        raise ValueError("eigenvalues must be non-empty.")

    fig, ax = plt.subplots()
    ax.hist(values, bins=bins, density=True, alpha=0.6, label="empirical spectrum")

    x_grid = np.linspace(-2.0, 2.0, 400)
    ax.plot(x_grid, semicircle_density(x_grid), label="semicircle law")

    ax.set_xlabel("eigenvalue")
    ax.set_ylabel("density")
    ax.set_title("Spectral Histogram and Semicircle Law")
    ax.legend()

    save_figure(fig, output_path)


def plot_moment_convergence(results_df, output_path):
    """Plot empirical moment convergence to semicircle distribution moments.

    The input is the table returned by the moment convergence experiment, where
    empirical moments m_k^N are compared with theoretical semicircle moments:
    odd moments are 0 and even moments are Catalan numbers.
    """
    required_columns = {
        "n",
        "order",
        "mean_empirical_moment",
        "theoretical_moment",
    }
    missing_columns = required_columns.difference(results_df.columns)
    if missing_columns:
        raise ValueError(f"results_df is missing required columns: {sorted(missing_columns)}")

    fig, ax = plt.subplots()

    for order in sorted(results_df["order"].unique()):
        order_df = results_df[results_df["order"] == order].sort_values("n")
        ax.plot(
            order_df["n"],
            order_df["mean_empirical_moment"],
            marker="o",
            label=f"empirical order {order}",
        )
        theoretical_value = order_df["theoretical_moment"].iloc[0]
        ax.axhline(
            theoretical_value,
            linestyle="--",
            label=f"theoretical order {order}",
        )

    ax.set_xlabel("matrix size N")
    ax.set_ylabel("moment")
    ax.set_title("Moment Convergence to Semicircle Moments")
    ax.legend()

    save_figure(fig, output_path)


def plot_lss_scatter(samples, output_path):
    """Plot LSS sample scatter and save it to disk."""
    pass
