from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy.special import gammaln


def _to_1d_numeric_array(data: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(data), dtype=float)
    if arr.size == 0:
        raise ValueError("data tidak boleh kosong.")
    if arr.ndim != 1:
        raise ValueError("data harus 1 dimensi.")
    return arr


def mle_bernoulli(data):
    """
    Estimator MLE untuk parameter Bernoulli.

    Formula: θ_hat = (1/n) * sum_{i=1..n} x_i.
    Definisi ini mengikuti penurunan MLE Bernoulli pada Tsun (2020), p. 45.
    """
    x = _to_1d_numeric_array(data)
    if not np.isin(x, [0.0, 1.0]).all():
        raise ValueError("data Bernoulli harus bernilai 0/1.")
    return float(np.mean(x))


def mle_poisson(data):
    """
    Estimator MLE untuk parameter Poisson.

    Formula: lambda_hat = (1/n) * sum_{i=1..n} x_i.
    Definisi ini mengikuti penurunan MLE Poisson pada Tsun (2020), p. 62.
    """
    x = _to_1d_numeric_array(data)
    if (x < 0).any() or not np.allclose(x, np.round(x)):
        raise ValueError("data Poisson harus bilangan cacah non-negatif.")
    return float(np.mean(x))


def beta_posterior(k, m):
    """
    Posterior Beta-Bernoulli dengan prior Beta(1, 1).

    Formula: alpha = k + 1, beta = (m - k) + 1,
    mean = alpha / (alpha + beta),
    mode = (alpha - 1) / (alpha + beta - 2) untuk alpha > 1 dan beta > 1.
    Definisi ini mengikuti pembahasan conjugate prior Beta-Bernoulli pada Tsun (2020), p. 89.
    """
    if m <= 0:
        raise ValueError("m harus > 0.")
    if k < 0 or k > m:
        raise ValueError("k harus berada pada rentang 0..m.")

    alpha = float(k + 1)
    beta = float(m - k + 1)
    mean = alpha / (alpha + beta)
    mode = (alpha - 1) / (alpha + beta - 2) if alpha > 1 and beta > 1 else None

    return {
        "α": alpha,
        "β": beta,
        "alpha": alpha,
        "beta": beta,
        "mode": mode,
        "mean": mean,
    }


def log_likelihood_bernoulli(theta, k, n):
    """
    Log-likelihood Bernoulli untuk k sukses dari n observasi.

    Formula: l(theta) = k * log(theta) + (n-k) * log(1-theta), dengan 0 < theta < 1.
    Definisi ini mengikuti formulasi likelihood Bernoulli pada Tsun (2020), p. 47.
    """
    if n <= 0:
        raise ValueError("n harus > 0.")
    if k < 0 or k > n:
        raise ValueError("k harus berada pada rentang 0..n.")
    if theta <= 0 or theta >= 1:
        return float(-np.inf)
    return float(k * np.log(theta) + (n - k) * np.log(1 - theta))


def log_likelihood_poisson(theta, data):
    """
    Log-likelihood Poisson untuk sampel independen.

    Formula: l(theta) = sum_i [-theta + x_i * log(theta) - log(x_i!)] untuk theta > 0.
    Definisi ini mengikuti formulasi likelihood Poisson pada Tsun (2020), p. 64.
    """
    x = _to_1d_numeric_array(data)
    if (x < 0).any() or not np.allclose(x, np.round(x)):
        raise ValueError("data Poisson harus bilangan cacah non-negatif.")
    if theta <= 0:
        return float(-np.inf)
    ll = np.sum(-theta + x * np.log(theta) - gammaln(x + 1))
    return float(ll)