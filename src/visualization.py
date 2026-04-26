"""Plotting utilities for Wigner matrix spectral experiments."""

from pathlib import Path

import matplotlib
from matplotlib.patches import Ellipse

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
    ax.set_xscale("log")
    ax.legend()

    save_figure(fig, output_path)


def plot_ks_convergence(results_df, output_path):
    """Plot KS distance convergence with standard deviation error bars."""
    required_columns = {"n", "mean_ks_distance", "std_ks_distance"}
    missing_columns = required_columns.difference(results_df.columns)
    if missing_columns:
        raise ValueError(f"results_df is missing required columns: {sorted(missing_columns)}")

    ordered_df = results_df.sort_values("n")
    fig, ax = plt.subplots()
    ax.errorbar(
        ordered_df["n"],
        ordered_df["mean_ks_distance"],
        yerr=ordered_df["std_ks_distance"],
        marker="o",
        capsize=4,
        label="mean KS distance",
    )
    ax.set_xlabel("matrix size N")
    ax.set_ylabel("KS distance")
    ax.set_title("KS Distance Convergence to Semicircle Law")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    save_figure(fig, output_path)


def plot_universality_comparison(eigenvalues_by_dist, output_path, bins=60):
    """Plot universality histograms for supported Wigner entry distributions."""
    required = ("gaussian", "rademacher", "uniform")
    missing = [dist for dist in required if dist not in eigenvalues_by_dist]
    if missing:
        raise ValueError(f"missing distributions: {missing}")

    titles = {
        "gaussian": "Gaussian entries",
        "rademacher": "Rademacher entries",
        "uniform": "Uniform entries",
    }
    x_grid = np.linspace(-2.0, 2.0, 400)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, dist in zip(axes.flat[:3], required):
        values = np.asarray(eigenvalues_by_dist[dist], dtype=float).reshape(-1)
        if values.size == 0:
            raise ValueError("eigenvalue arrays must be non-empty.")
        ax.hist(values, bins=bins, density=True, alpha=0.6, label="empirical spectrum")
        ax.plot(x_grid, semicircle_density(x_grid), label="semicircle law")
        ax.set_title(titles[dist])
        ax.set_xlabel("eigenvalue")
        ax.set_ylabel("density")
        ax.legend()

    overlay_ax = axes.flat[3]
    for dist in required:
        values = np.asarray(eigenvalues_by_dist[dist], dtype=float).reshape(-1)
        overlay_ax.hist(values, bins=bins, density=True, histtype="step", label=titles[dist])
    overlay_ax.plot(x_grid, semicircle_density(x_grid), label="semicircle law")
    overlay_ax.set_title("Overlay comparison")
    overlay_ax.set_xlabel("eigenvalue")
    overlay_ax.set_ylabel("density")
    overlay_ax.legend()

    fig.suptitle("Universality Comparison with Semicircle Law")
    save_figure(fig, output_path)


def plot_lss_scatter(samples, output_path):
    """Plot samples of the two-dimensional linear spectral statistic.

    The coordinates are G_N(x^2) and G_N(x^4), as used in the thesis LSS-CLT
    numerical experiment.
    """
    values = np.asarray(samples, dtype=float)
    if values.ndim != 2 or values.shape[1] != 2 or values.shape[0] == 0:
        raise ValueError("samples must have shape (num_samples, 2).")

    fig, ax = plt.subplots()
    ax.scatter(values[:, 0], values[:, 1], alpha=0.7)
    ax.set_xlabel("G_N(x^2)")
    ax.set_ylabel("G_N(x^4)")
    ax.set_title("Two-dimensional LSS Samples")
    save_figure(fig, output_path)


def _add_covariance_ellipse(ax, mean, cov):
    """Add a covariance ellipse for two-dimensional LSS samples."""
    if cov.shape != (2, 2):
        return
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    eigenvalues = np.maximum(eigenvalues, 0.0)
    angle = np.degrees(np.arctan2(eigenvectors[1, 1], eigenvectors[0, 1]))
    width, height = 2.0 * np.sqrt(eigenvalues[1]), 2.0 * np.sqrt(eigenvalues[0])
    ellipse = Ellipse(
        xy=mean,
        width=width,
        height=height,
        angle=angle,
        fill=False,
        linestyle="--",
    )
    ax.add_patch(ellipse)


def plot_lss_2d_scatter(samples_by_n, output_path):
    """Plot two-dimensional LSS samples for multiple matrix sizes.

    Each panel shows samples of (G_N(x^2), G_N(x^4)), the sample mean point,
    and a covariance ellipse.
    """
    if not samples_by_n:
        raise ValueError("samples_by_n must be non-empty.")

    n_values = sorted(samples_by_n)
    num_panels = len(n_values)
    cols = min(2, num_panels)
    rows = int(np.ceil(num_panels / cols))
    fig_width = max(8, 8 * cols)
    fig_height = max(6, 4.8 * rows)
    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(fig_width, fig_height),
        squeeze=False,
        constrained_layout=True,
    )

    for panel_index, (ax, n) in enumerate(zip(axes.flat, n_values)):
        values = np.asarray(samples_by_n[n], dtype=float)
        if values.ndim != 2 or values.shape[1] != 2 or values.shape[0] == 0:
            raise ValueError("each samples array must have shape (num_samples, 2).")
        mean = np.mean(values, axis=0)
        cov = np.cov(values, rowvar=False) if values.shape[0] > 1 else np.zeros((2, 2))
        row_index, col_index = divmod(panel_index, cols)
        ax.scatter(values[:, 0], values[:, 1], alpha=0.3, s=14, label="samples")
        ax.scatter(mean[0], mean[1], marker="x", s=70, label="mean")
        _add_covariance_ellipse(ax, mean, cov)
        ax.set_title(f"N = {n}", pad=8)
        if row_index == rows - 1:
            ax.set_xlabel("G_N(x^2)")
        else:
            ax.set_xlabel("")
        if col_index == 0:
            ax.set_ylabel("G_N(x^4)")
        else:
            ax.set_ylabel("")
        ax.legend(loc="best", fontsize="small", frameon=True)

    for ax in axes.flat[num_panels:]:
        ax.axis("off")

    fig.suptitle("Two-dimensional LSS-CLT Samples", y=1.02)
    layout_engine = fig.get_layout_engine()
    if layout_engine is not None:
        layout_engine.set(w_pad=0.25, h_pad=0.35, hspace=0.18, wspace=0.12)
    save_figure(fig, output_path)


def plot_lss_mean_convergence(summary_df, output_path):
    """Plot LSS-CLT sample mean vector convergence by matrix size."""
    required_columns = {
        "n",
        "mean_g2",
        "mean_g4",
        "theoretical_mean_g2",
        "theoretical_mean_g4",
    }
    missing_columns = required_columns.difference(summary_df.columns)
    if missing_columns:
        raise ValueError(f"summary_df is missing required columns: {sorted(missing_columns)}")

    ordered_df = summary_df.sort_values("n")
    fig, ax = plt.subplots()
    ax.plot(ordered_df["n"], ordered_df["mean_g2"], marker="o", label="mean G_N(x^2)")
    ax.plot(ordered_df["n"], ordered_df["mean_g4"], marker="o", label="mean G_N(x^4)")
    ax.axhline(
        ordered_df["theoretical_mean_g2"].iloc[0],
        linestyle="--",
        label="theoretical mean G_N(x^2)",
    )
    ax.axhline(
        ordered_df["theoretical_mean_g4"].iloc[0],
        linestyle="--",
        label="theoretical mean G_N(x^4)",
    )
    ax.set_xlabel("matrix size N")
    ax.set_ylabel("sample mean")
    ax.set_title("LSS-CLT Sample Mean Convergence")
    ax.legend()
    save_figure(fig, output_path)


def plot_lss_cov_convergence(summary_df, output_path):
    """Plot LSS-CLT sample covariance matrix convergence by matrix size."""
    required_columns = {
        "n",
        "cov_g2_g2",
        "cov_g2_g4",
        "cov_g4_g4",
        "theoretical_cov_g2_g2",
        "theoretical_cov_g2_g4",
        "theoretical_cov_g4_g4",
    }
    missing_columns = required_columns.difference(summary_df.columns)
    if missing_columns:
        raise ValueError(f"summary_df is missing required columns: {sorted(missing_columns)}")

    ordered_df = summary_df.sort_values("n")
    fig, ax = plt.subplots()
    ax.plot(ordered_df["n"], ordered_df["cov_g2_g2"], marker="o", label="cov G_N(x^2), G_N(x^2)")
    ax.plot(ordered_df["n"], ordered_df["cov_g2_g4"], marker="o", label="cov G_N(x^2), G_N(x^4)")
    ax.plot(ordered_df["n"], ordered_df["cov_g4_g4"], marker="o", label="cov G_N(x^4), G_N(x^4)")
    ax.axhline(
        ordered_df["theoretical_cov_g2_g2"].iloc[0],
        linestyle="--",
        label="theoretical cov G_N(x^2), G_N(x^2)",
    )
    ax.axhline(
        ordered_df["theoretical_cov_g2_g4"].iloc[0],
        linestyle="--",
        label="theoretical cov G_N(x^2), G_N(x^4)",
    )
    ax.axhline(
        ordered_df["theoretical_cov_g4_g4"].iloc[0],
        linestyle="--",
        label="theoretical cov G_N(x^4), G_N(x^4)",
    )
    ax.set_xlabel("matrix size N")
    ax.set_ylabel("sample covariance")
    ax.set_title("LSS-CLT Sample Covariance Convergence")
    ax.legend()
    save_figure(fig, output_path)
