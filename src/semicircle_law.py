"""Utilities related to the Wigner semicircle law."""

import numpy as np


def semicircle_density(x):
    """Evaluate the standard semicircle law density rho_sc.

    The density is rho_sc(x) = (1 / (2 pi)) sqrt(4 - x^2) on [-2, 2]
    and 0 outside this interval. This function supports scalar and vector
    inputs for spectral histogram comparisons with the semicircle law.
    """
    values = np.asarray(x, dtype=float)
    density = np.zeros_like(values, dtype=float)
    mask = (values >= -2.0) & (values <= 2.0)
    density[mask] = np.sqrt(np.maximum(4.0 - values[mask] ** 2, 0.0)) / (2.0 * np.pi)

    if np.isscalar(x):
        return float(density)
    return density


def semicircle_cdf(x):
    """Evaluate the theoretical distribution function of the semicircle law.

    This is the F_sc used to compare the empirical spectral distribution F_N
    with the semicircle law in KS distance experiments.
    """
    values = np.asarray(x, dtype=float)
    cdf = np.zeros_like(values, dtype=float)

    cdf[values >= 2.0] = 1.0
    mask = (values > -2.0) & (values < 2.0)
    inside = values[mask]
    cdf[mask] = (
        0.5
        + inside * np.sqrt(np.maximum(4.0 - inside**2, 0.0)) / (4.0 * np.pi)
        + np.arcsin(inside / 2.0) / np.pi
    )

    if np.isscalar(x):
        return float(cdf)
    return cdf


def empirical_cdf_values(eigenvalues):
    """Return sorted eigenvalues and empirical spectral distribution values.

    For n eigenvalues, the i-th sorted eigenvalue is paired with i / n,
    representing the empirical spectral distribution F_N at the sample
    support points.
    """
    values = np.asarray(eigenvalues, dtype=float).reshape(-1)

    if values.size == 0:
        raise ValueError("eigenvalues must be non-empty.")

    sorted_values = np.sort(values)
    cdf_values = np.arange(1, values.size + 1, dtype=float) / values.size
    return sorted_values, cdf_values


def ks_distance_to_semicircle(eigenvalues):
    """Compute the KS distance between F_N and the semicircle law F_sc."""
    sorted_values, empirical_values = empirical_cdf_values(eigenvalues)
    theoretical_values = semicircle_cdf(sorted_values)
    left_limits = np.arange(sorted_values.size, dtype=float) / sorted_values.size

    right_gap = np.max(np.abs(empirical_values - theoretical_values))
    left_gap = np.max(np.abs(left_limits - theoretical_values))
    return float(max(right_gap, left_gap))
