"""
hypothesis.py — Member D
Fungsi uji hipotesis menggunakan Z-test satu sampel dan dua sampel.
Data: dataset_issues_clean.csv dan dataset_prs_clean.csv (dari Member A)
"""

import numpy as np
import pandas as pd
from scipy import stats


# ─────────────────────────────────────────────
# FUNGSI UTAMA (spesifikasi Member D)
# ─────────────────────────────────────────────

def z_test_one_sample(x_bar, mu0, sigma, n, alternative, alpha=0.05):
    """
    Uji hipotesis Z satu sampel.

    Parameters
    ----------
    x_bar       : float  — rata-rata sampel
    mu0         : float  — nilai rata-rata populasi yang diuji (H0)
    sigma       : float  — standar deviasi populasi (diketahui)
    n           : int    — ukuran sampel
    alternative : str    — 'two-sided' | 'greater' | 'less'
    alpha       : float  — tingkat signifikansi (default 0.05)

    Returns
    -------
    dict dengan kunci:
        z_stat       : float  — nilai statistik Z
        p_value      : float  — nilai p
        decision     : str    — 'Reject H0' atau 'Fail to Reject H0'
        interpretation: str   — penjelasan hasil
    """
    # Hitung statistik Z
    se = sigma / np.sqrt(n)
    z_stat = (x_bar - mu0) / se

    # Hitung p-value sesuai jenis hipotesis
    if alternative == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    elif alternative == "greater":
        p_value = 1 - stats.norm.cdf(z_stat)
    elif alternative == "less":
        p_value = stats.norm.cdf(z_stat)
    else:
        raise ValueError("alternative harus 'two-sided', 'greater', atau 'less'")

    # Keputusan
    decision = "Reject H0" if p_value < alpha else "Fail to Reject H0"

    # Interpretasi
    if decision == "Reject H0":
        interpretation = (
            f"Dengan alpha={alpha}, terdapat cukup bukti statistik untuk menolak H0 "
            f"(z={z_stat:.4f}, p={p_value:.4f}). "
            f"Rata-rata sampel ({x_bar:.4f}) berbeda signifikan dari mu0={mu0}."
        )
    else:
        interpretation = (
            f"Dengan alpha={alpha}, tidak cukup bukti statistik untuk menolak H0 "
            f"(z={z_stat:.4f}, p={p_value:.4f}). "
            f"Rata-rata sampel ({x_bar:.4f}) tidak berbeda signifikan dari mu0={mu0}."
        )

    return {
        "z_stat": round(z_stat, 4),
        "p_value": round(p_value, 4),
        "decision": decision,
        "interpretation": interpretation,
    }


def z_test_two_sample(x_bar1, x_bar2, sigma1, sigma2, n1, n2, alternative, alpha=0.05):
    """
    Uji hipotesis Z dua sampel independen.

    Parameters
    ----------
    x_bar1      : float  — rata-rata sampel 1
    x_bar2      : float  — rata-rata sampel 2
    sigma1      : float  — standar deviasi populasi sampel 1
    sigma2      : float  — standar deviasi populasi sampel 2
    n1          : int    — ukuran sampel 1
    n2          : int    — ukuran sampel 2
    alternative : str    — 'two-sided' | 'greater' | 'less'
    alpha       : float  — tingkat signifikansi (default 0.05)

    Returns
    -------
    dict dengan kunci:
        z_stat       : float  — nilai statistik Z
        p_value      : float  — nilai p
        decision     : str    — 'Reject H0' atau 'Fail to Reject H0'
        interpretation: str   — penjelasan hasil
    """
    # Hitung statistik Z dua sampel
    se = np.sqrt((sigma1 ** 2 / n1) + (sigma2 ** 2 / n2))
    z_stat = (x_bar1 - x_bar2) / se

    # Hitung p-value
    if alternative == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    elif alternative == "greater":
        p_value = 1 - stats.norm.cdf(z_stat)
    elif alternative == "less":
        p_value = stats.norm.cdf(z_stat)
    else:
        raise ValueError("alternative harus 'two-sided', 'greater', atau 'less'")

    # Keputusan
    decision = "Reject H0" if p_value < alpha else "Fail to Reject H0"

    # Interpretasi
    if decision == "Reject H0":
        interpretation = (
            f"Dengan alpha={alpha}, terdapat cukup bukti statistik untuk menolak H0 "
            f"(z={z_stat:.4f}, p={p_value:.4f}). "
            f"Terdapat perbedaan signifikan antara dua kelompok "
            f"(mean1={x_bar1:.4f} vs mean2={x_bar2:.4f})."
        )
    else:
        interpretation = (
            f"Dengan alpha={alpha}, tidak cukup bukti statistik untuk menolak H0 "
            f"(z={z_stat:.4f}, p={p_value:.4f}). "
            f"Tidak terdapat perbedaan signifikan antara dua kelompok "
            f"(mean1={x_bar1:.4f} vs mean2={x_bar2:.4f})."
        )

    return {
        "z_stat": round(z_stat, 4),
        "p_value": round(p_value, 4),
        "decision": decision,
        "interpretation": interpretation,
    }


# ─────────────────────────────────────────────
# APLIKASI KE DATA MEMBER A
# ─────────────────────────────────────────────

def load_data():
    """Memuat dataset dari Member A."""
    issues = pd.read_csv("dataset_issues_clean.csv", parse_dates=["created_at", "closed_at"])
    prs    = pd.read_csv("dataset_prs_clean.csv",    parse_dates=["created_at", "closed_at", "merged_at"])
    return issues, prs


def compute_resolution_days(issues):
    """Menghitung lama resolusi issues (hari)."""
    closed = issues.dropna(subset=["closed_at"]).copy()
    closed["created_at"] = pd.to_datetime(closed["created_at"], utc=True)
    closed["closed_at"]  = pd.to_datetime(closed["closed_at"],  utc=True)
    closed["resolution_days"] = (
        (closed["closed_at"] - closed["created_at"]).dt.total_seconds() / 86400
    )
    return closed["resolution_days"]


def compute_merge_days(prs):
    """Menghitung lama waktu merge PR (hari)."""
    merged = prs[prs["is_merged"] == 1].copy()
    merged["created_at"] = pd.to_datetime(merged["created_at"], utc=True)
    merged["merged_at"]  = pd.to_datetime(merged["merged_at"],  utc=True)
    merged["merge_days"] = (
        (merged["merged_at"] - merged["created_at"]).dt.total_seconds() / 86400
    )
    return merged["merge_days"]


def run_all_tests():
    print("=" * 65)
    print("       PENGUJIAN HIPOTESIS — Member D")
    print("       Data oleh Member A: Issues & Pull Requests")
    print("=" * 65)

    issues, prs = load_data()

    resolution_days = compute_resolution_days(issues)
    merge_days      = compute_merge_days(prs)

    # ── Statistik deskriptif ──────────────────────────────────────
    res_mean  = resolution_days.mean()
    res_std   = resolution_days.std()
    res_n     = len(resolution_days)

    merge_mean = merge_days.mean()
    merge_std  = merge_days.std()
    merge_n    = len(merge_days)

    print("\n📊 STATISTIK DESKRIPTIF")
    print(f"  Issues (closed)   : n={res_n}, mean={res_mean:.2f} hari, std={res_std:.2f}")
    print(f"  PR (merged)       : n={merge_n}, mean={merge_mean:.2f} hari, std={merge_std:.2f}")

    # ─────────────────────────────────────────────────────────────
    # UJI 1 — Z One-Sample
    # H0: rata-rata waktu resolusi issue = 30 hari
    # H1: rata-rata waktu resolusi issue > 30 hari
    # ─────────────────────────────────────────────────────────────
    print("\n" + "─" * 65)
    print("UJI 1 (One-Sample Z-Test)")
    print("H0 : Rata-rata waktu resolusi issue = 30 hari")
    print("H1 : Rata-rata waktu resolusi issue > 30 hari")
    print("─" * 65)

    result1 = z_test_one_sample(
        x_bar=res_mean,
        mu0=30,
        sigma=res_std,
        n=res_n,
        alternative="greater",
        alpha=0.05
    )
    for k, v in result1.items():
        print(f"  {k:17}: {v}")

    # ─────────────────────────────────────────────────────────────
    # UJI 2 — Z One-Sample
    # H0: rata-rata waktu merge PR = 14 hari
    # H1: rata-rata waktu merge PR ≠ 14 hari
    # ─────────────────────────────────────────────────────────────
    print("\n" + "─" * 65)
    print("UJI 2 (One-Sample Z-Test)")
    print("H0 : Rata-rata waktu merge PR = 14 hari")
    print("H1 : Rata-rata waktu merge PR ≠ 14 hari")
    print("─" * 65)

    result2 = z_test_one_sample(
        x_bar=merge_mean,
        mu0=14,
        sigma=merge_std,
        n=merge_n,
        alternative="two-sided",
        alpha=0.05
    )
    for k, v in result2.items():
        print(f"  {k:17}: {v}")

    # ─────────────────────────────────────────────────────────────
    # UJI 3 — Z Two-Sample
    # Membandingkan waktu resolusi issue vs waktu merge PR
    # H0: mean_issue = mean_pr
    # H1: mean_issue > mean_pr
    # ─────────────────────────────────────────────────────────────
    print("\n" + "─" * 65)
    print("UJI 3 (Two-Sample Z-Test)")
    print("H0 : Rata-rata waktu resolusi issue = rata-rata waktu merge PR")
    print("H1 : Rata-rata waktu resolusi issue > rata-rata waktu merge PR")
    print("─" * 65)

    result3 = z_test_two_sample(
        x_bar1=res_mean,
        x_bar2=merge_mean,
        sigma1=res_std,
        sigma2=merge_std,
        n1=res_n,
        n2=merge_n,
        alternative="greater",
        alpha=0.05
    )
    for k, v in result3.items():
        print(f"  {k:17}: {v}")

    print("\n" + "=" * 65)
    print("  Pengujian selesai.")
    print("=" * 65)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_all_tests()
