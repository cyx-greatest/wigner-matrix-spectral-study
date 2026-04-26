"""Experiment entry points for Wigner matrix spectral studies."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.lss_clt import run_lss_clt_experiment as run_lss_clt_simulation
from src.moments import run_moment_convergence_experiment
from src.semicircle_law import ks_distance_to_semicircle
from src.visualization import (
    plot_ks_convergence,
    plot_lss_2d_scatter,
    plot_lss_cov_convergence,
    plot_lss_mean_convergence,
    plot_lss_scatter,
    plot_moment_convergence,
    plot_spectral_histogram,
    plot_universality_comparison,
)
from src.wigner_matrix import compute_eigenvalues, generate_wigner_real


def parse_int_tuple(value):
    """Parse comma-separated positive integer parameters for experiments."""
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


THESIS_PRESETS = {
    "ks": {
        "matrix_sizes": (50, 100, 200, 400, 800, 1600),
        "num_trials": 20,
        "dist": "gaussian",
    },
    "moments": {
        "matrix_sizes": (50, 100, 200, 400, 800, 1600),
        "orders": (2, 4, 6),
        "num_trials": 20,
        "dist": "gaussian",
    },
    "universality": {
        "n": 400,
        "repeats": 10,
        "distributions": ("gaussian", "rademacher", "uniform"),
        "seed": 42,
    },
    "lss_clt": {
        "matrix_sizes": (50, 100, 200, 400, 800),
        "num_trials": 1000,
        "dist": "gaussian",
    },
}


def run_semicircle_experiment(
    n=500,
    dist="gaussian",
    output_dir="results/figures",
    seed=None,
):
    """Run the spectral histogram and semicircle law density experiment."""
    output_dir = Path(output_dir)
    output_path = output_dir / "semicircle_histogram.png"

    matrix = generate_wigner_real(n, dist=dist, seed=seed)
    eigenvalues = compute_eigenvalues(matrix)
    plot_spectral_histogram(eigenvalues, output_path)

    return output_path


def run_ks_convergence_experiment(
    matrix_sizes=(50, 100, 200, 400),
    num_trials=10,
    dist="gaussian",
    output_dir="results",
    seed=None,
):
    """Run the KS distance experiment for convergence to the semicircle law.

    For each matrix size N, this experiment compares the empirical spectral
    distribution of real symmetric Wigner matrices with the theoretical
    semicircle distribution using the KS distance.
    """
    output_dir = Path(output_dir)
    table_dir = output_dir / "tables"
    figure_dir = output_dir / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)
    rows = []

    for n in matrix_sizes:
        distances = []
        for _ in range(num_trials):
            trial_seed = int(rng.integers(0, np.iinfo(np.uint32).max))
            matrix = generate_wigner_real(n, dist=dist, seed=trial_seed)
            eigenvalues = compute_eigenvalues(matrix)
            distances.append(ks_distance_to_semicircle(eigenvalues))

        rows.append(
            {
                "n": n,
                "mean_ks_distance": float(np.mean(distances)),
                "std_ks_distance": float(np.std(distances, ddof=1)) if len(distances) > 1 else 0.0,
                "num_trials": num_trials,
                "dist": dist,
            }
        )

    results_df = pd.DataFrame(
        rows,
        columns=["n", "mean_ks_distance", "std_ks_distance", "num_trials", "dist"],
    )
    results_df.to_csv(table_dir / "ks_convergence.csv", index=False)
    plot_ks_convergence(results_df, figure_dir / "ks_convergence.png")
    return results_df


def run_moment_experiment(
    matrix_sizes=(50, 100, 200, 400),
    orders=(2, 4, 6),
    num_trials=10,
    dist="gaussian",
    output_dir="results",
    seed=None,
):
    """Run moment convergence and Catalan number verification experiment."""
    output_dir = Path(output_dir)
    table_dir = output_dir / "tables"
    figure_dir = output_dir / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    results_df = run_moment_convergence_experiment(
        matrix_sizes=matrix_sizes,
        orders=orders,
        num_trials=num_trials,
        dist=dist,
        seed=seed,
    )
    results_df.to_csv(table_dir / "moment_convergence.csv", index=False)
    plot_moment_convergence(results_df, figure_dir / "moment_convergence.png")
    return results_df


def run_universality_experiment(
    n=500,
    repeats=1,
    distributions=("gaussian", "rademacher", "uniform"),
    output_dir="results/figures",
    seed=None,
):
    """Run the numerical universality experiment for the semicircle law."""
    output_dir = Path(output_dir)
    rng = np.random.default_rng(seed)
    eigenvalues_by_dist = {}

    for dist in distributions:
        eigenvalue_samples = []
        for _ in range(repeats):
            trial_seed = int(rng.integers(0, np.iinfo(np.uint32).max))
            matrix = generate_wigner_real(n, dist=dist, seed=trial_seed)
            eigenvalue_samples.append(compute_eigenvalues(matrix))
        eigenvalues_by_dist[dist] = np.concatenate(eigenvalue_samples)

    output_path = output_dir / "universality_comparison.png"
    plot_universality_comparison(eigenvalues_by_dist, output_path)
    return output_path


def run_lss_clt_experiment(
    matrix_sizes=(50, 100, 200),
    num_samples=200,
    dist="gaussian",
    output_dir="results",
    seed=None,
):
    """Run and save the chapter 5 two-dimensional LSS-CLT experiment.

    This entry corresponds to the thesis chapter 5 numerical experiment design
    for the central limit theorem of two-dimensional linear spectral statistics
    of Wigner matrices.
    """
    output_dir = Path(output_dir)
    table_dir = output_dir / "tables"
    figure_dir = output_dir / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    samples_by_n, summary_df = run_lss_clt_simulation(
        matrix_sizes=matrix_sizes,
        num_samples=num_samples,
        dist=dist,
        seed=seed,
    )
    summary_df.to_csv(table_dir / "lss_clt_summary.csv", index=False)

    max_n = max(samples_by_n)
    plot_lss_scatter(samples_by_n[max_n], figure_dir / "lss_clt_scatter.png")
    plot_lss_2d_scatter(samples_by_n, figure_dir / "lss_clt_2d_scatter.png")
    plot_lss_mean_convergence(summary_df, figure_dir / "lss_clt_2d_mean.png")
    plot_lss_cov_convergence(summary_df, figure_dir / "lss_clt_2d_cov.png")

    return summary_df


def main():
    """Command-line interface for Wigner matrix spectral experiments."""
    parser = argparse.ArgumentParser(
        description="Run Wigner matrix spectral distribution experiments."
    )
    parser.add_argument(
        "--experiment",
        choices=["semicircle", "ks", "moments", "universality", "lss_clt"],
        required=True,
    )
    parser.add_argument("--n", type=int, default=500)
    parser.add_argument("--matrix-sizes", type=parse_int_tuple, default=(50, 100, 200, 400))
    parser.add_argument("--orders", type=parse_int_tuple, default=(2, 4, 6))
    parser.add_argument("--num-trials", type=int, default=10)
    parser.add_argument("--dist", default="gaussian")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--preset", choices=["thesis"], default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.experiment == "semicircle":
        run_semicircle_experiment(
            n=args.n,
            dist=args.dist,
            output_dir=args.output_dir or "results/figures",
            seed=args.seed,
        )
    elif args.experiment == "ks":
        preset = THESIS_PRESETS["ks"] if args.preset == "thesis" else {}
        run_ks_convergence_experiment(
            matrix_sizes=preset.get("matrix_sizes", args.matrix_sizes),
            num_trials=preset.get("num_trials", args.num_trials),
            dist=preset.get("dist", args.dist),
            output_dir=args.output_dir or "results",
            seed=args.seed,
        )
    elif args.experiment == "moments":
        preset = THESIS_PRESETS["moments"] if args.preset == "thesis" else {}
        run_moment_experiment(
            matrix_sizes=preset.get("matrix_sizes", args.matrix_sizes),
            orders=preset.get("orders", args.orders),
            num_trials=preset.get("num_trials", args.num_trials),
            dist=preset.get("dist", args.dist),
            output_dir=args.output_dir or "results",
            seed=args.seed,
        )
    elif args.experiment == "universality":
        preset = THESIS_PRESETS["universality"] if args.preset == "thesis" else {}
        run_universality_experiment(
            n=preset.get("n", args.n),
            repeats=preset.get("repeats", 1),
            distributions=preset.get("distributions", ("gaussian", "rademacher", "uniform")),
            output_dir=args.output_dir or "results/figures",
            seed=preset.get("seed", args.seed),
        )
    else:
        preset = THESIS_PRESETS["lss_clt"] if args.preset == "thesis" else {}
        run_lss_clt_experiment(
            matrix_sizes=preset.get("matrix_sizes", args.matrix_sizes),
            num_samples=preset.get("num_trials", args.num_trials),
            dist=preset.get("dist", args.dist),
            output_dir=args.output_dir or "results",
            seed=args.seed,
        )


if __name__ == "__main__":
    main()
