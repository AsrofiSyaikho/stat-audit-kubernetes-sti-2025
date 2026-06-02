"""
inference.py

Modul inferensi statistik untuk membangun Confidence Interval (CI)
dan Credible Interval berdasarkan hasil estimasi pada estimator.py.

Referensi:
Tsun (2020)
- Confidence Interval (p. 300)
- Bernoulli MLE (p. 254)
- Poisson MLE (p. 254)
- Beta Posterior (p. 269)
"""

from __future__ import annotations

import numpy as np

from scipy.stats import norm
from scipy.stats import beta as beta_dist

from estimator import (
    mle_bernoulli,
    mle_poisson,
    beta_posterior,
)


def confidence_interval(
    theta_hat: float,
    sigma: float,
    n: int,
    confidence: float = 0.95,
) -> dict:
    """
    Confidence Interval umum.

    Formula:
        θ̂ ± z * (σ / √n)

    Referensi:
        Tsun (2020), p. 300
    """

    if n <= 0:
        raise ValueError("n harus > 0.")

    if sigma < 0:
        raise ValueError("sigma tidak boleh negatif.")

    z = norm.ppf(1 - (1 - confidence) / 2)

    margin = z * sigma / np.sqrt(n)

    return {
        "theta_hat": float(theta_hat),
        "lower": float(theta_hat - margin),
        "upper": float(theta_hat + margin),
        "confidence": confidence,
        "margin_of_error": float(margin),
    }


def ci_bernoulli(
    data,
    confidence: float = 0.95,
) -> dict:
    """
    Confidence Interval untuk parameter Bernoulli.

    Menggunakan:
        θ̂ = mle_bernoulli(data)

    Standard Error:
        sqrt(θ̂(1-θ̂)/n)

    Referensi:
        Tsun (2020), p. 254, p. 300
    """

    p_hat = mle_bernoulli(data)

    n = len(data)

    se = np.sqrt(p_hat * (1 - p_hat) / n)

    z = norm.ppf(1 - (1 - confidence) / 2)

    margin = z * se

    return {
        "p_hat": float(p_hat),
        "lower": float(max(0.0, p_hat - margin)),
        "upper": float(min(1.0, p_hat + margin)),
        "confidence": confidence,
        "standard_error": float(se),
        "margin_of_error": float(margin),
    }


def ci_poisson(
    data,
    confidence: float = 0.95,
) -> dict:
    """
    Confidence Interval untuk parameter Poisson λ.

    Menggunakan:
        λ̂ = mle_poisson(data)

    Standard Error:
        sqrt(λ̂ / n)

    Referensi:
        Tsun (2020), p. 254, p. 300
    """

    lambda_hat = mle_poisson(data)

    n = len(data)

    se = np.sqrt(lambda_hat / n)

    z = norm.ppf(1 - (1 - confidence) / 2)

    margin = z * se

    return {
        "lambda_hat": float(lambda_hat),
        "lower": float(max(0.0, lambda_hat - margin)),
        "upper": float(lambda_hat + margin),
        "confidence": confidence,
        "standard_error": float(se),
        "margin_of_error": float(margin),
    }


def credible_interval(
    alpha: float,
    beta_param: float,
    confidence: float = 0.95,
) -> dict:
    """
    Bayesian Credible Interval
    untuk distribusi Beta(alpha, beta).

    Interval dihitung menggunakan quantile posterior:

        [ q((1-c)/2), q(1-(1-c)/2) ]

    Referensi:
        Tsun (2020), p. 269
    """

    if alpha <= 0 or beta_param <= 0:
        raise ValueError("alpha dan beta harus > 0.")

    tail = (1 - confidence) / 2

    lower = beta_dist.ppf(tail, alpha, beta_param)

    upper = beta_dist.ppf(1 - tail, alpha, beta_param)

    return {
        "alpha": alpha,
        "beta": beta_param,
        "lower": float(lower),
        "upper": float(upper),
        "confidence": confidence,
    }


def credible_interval_from_posterior(
    k: int,
    m: int,
    confidence: float = 0.95,
) -> dict:
    """
    Helper function yang langsung menggunakan
    output beta_posterior() dari estimator.py.

    Parameter:
        k = jumlah sukses
        m = total observasi

    Referensi:
        Tsun (2020), p. 269
    """

    posterior = beta_posterior(k, m)

    return credible_interval(
        alpha=posterior["alpha"],
        beta_param=posterior["beta"],
        confidence=confidence,
    )