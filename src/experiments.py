"""Experiment entry points for Wigner matrix spectral studies."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.moments import run_moment_convergence_experiment
from src.semicircle_law import ks_distance_to_semicircle
from src.visualization import plot_moment_convergence, plot_spectral_histogram
from src.wigner_matrix import compute_eigenvalues, generate_wigner_real


def parse_int_tuple(value):
    """Parse comma-separated positive integer parameters for experiments."""
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


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
    output_dir="results/tables",
    seed=None,
):
    """Run the KS distance experiment for convergence to the semicircle law.

    For each matrix size N, this experiment compares the empirical spectral
    distribution of real symmetric Wigner matrices with the theoretical
    semicircle distribution using the KS distance.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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
                "num_trials": num_trials,
                "dist": dist,
            }
        )

    results_df = pd.DataFrame(
        rows,
        columns=["n", "mean_ks_distance", "num_trials", "dist"],
    )
    results_df.to_csv(output_dir / "ks_convergence.csv", index=False)
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
    distributions=("gaussian", "rademacher", "uniform"),
    output_dir="results/figures",
    seed=None,
):
    """Run the numerical universality experiment for the semicircle law."""
    output_dir = Path(output_dir)
    output_paths = {}
    rng = np.random.default_rng(seed)

    for dist in distributions:
        trial_seed = int(rng.integers(0, np.iinfo(np.uint32).max))
        matrix = generate_wigner_real(n, dist=dist, seed=trial_seed)
        eigenvalues = compute_eigenvalues(matrix)
        output_path = output_dir / f"universality_{dist}.png"
        plot_spectral_histogram(eigenvalues, output_path)
        output_paths[dist] = output_path

    return output_paths


def run_lss_clt_experiment():
    """Run the chapter 5 two-dimensional LSS-CLT experiment.

    This entry corresponds to the thesis chapter 5 numerical experiment design
    for the central limit theorem of two-dimensional linear spectral statistics
    of Wigner matrices. It will be implemented in a later step.
    """
    raise NotImplementedError("LSS-CLT experiment will be implemented later.")


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
        run_ks_convergence_experiment(
            matrix_sizes=args.matrix_sizes,
            num_trials=args.num_trials,
            dist=args.dist,
            output_dir=args.output_dir or "results/tables",
            seed=args.seed,
        )
    elif args.experiment == "moments":
        run_moment_experiment(
            matrix_sizes=args.matrix_sizes,
            orders=args.orders,
            num_trials=args.num_trials,
            dist=args.dist,
            output_dir=args.output_dir or "results",
            seed=args.seed,
        )
    elif args.experiment == "universality":
        run_universality_experiment(
            n=args.n,
            distributions=("gaussian", "rademacher", "uniform"),
            output_dir=args.output_dir or "results/figures",
            seed=args.seed,
        )
    else:
        run_lss_clt_experiment()


if __name__ == "__main__":
    main()
