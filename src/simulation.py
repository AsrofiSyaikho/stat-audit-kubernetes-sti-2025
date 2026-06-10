"""
simulation.py — Member E

Modul komputasi statistik untuk menjalankan Simulasi Monte Carlo (Bootstrap)
terhadap durasi pengerjaan Pull Request dan perhitungan teoritis False Positive Rate (FPR) Bloom Filter.

Referensi:
    - Simulasi Monte Carlo / Resampling: Ross (2014), Simulation 5th Edition
    - Kriteria Tugas StatProb S124 (Bloom Filter FPR formula)
"""

from __future__ import annotations
import numpy as np

def monte_carlo_pr_duration(
    data: np.ndarray, 
    threshold: float = 14.0, 
    n_simulations: int = 10000, 
    sample_size: int = 100
) -> dict:
    """
    Menjalankan simulasi Monte Carlo berbasis bootstrap resampling untuk mengestimasi 
    probabilitas bahwa rata-rata durasi penyelesaian PR melebihi ambang batas (threshold) tertentu.

    Parameters
    ----------
    data          : np.ndarray — Array data empiris durasi pengerjaan PR (dalam hari).
    threshold     : float      — Ambang batas hari yang diuji (default: 14.0 hari).
    n_simulations : int        — Jumlah iterasi simulasi Monte Carlo (default: 10000).
    sample_size   : int        — Ukuran sampel acak yang ditarik per iterasi (default: 100).

    Returns
    -------
    dict dengan kunci:
        simulated_means : list  — Nilai rata-rata dari setiap iterasi simulasi.
        probability     : float — Probabilitas rata-rata durasi sampel melebihi threshold.
        threshold       : float — Ambang batas hari yang digunakan.
    """
    # Validasi input data bersih
    clean_data = data[~np.isnan(data)]
    if len(clean_data) == 0:
        raise ValueError("Data empiris kosong atau hanya berisi nilai NaN.")
        
    simulated_means = []
    success_count = 0

    # Eksekusi perulangan Monte Carlo
    for _ in range(n_simulations):
        # Bootstrap resampling: penarikan sampel acak dengan pengembalian (replacement)
        bootstrap_sample = np.random.choice(clean_data, size=sample_size, replace=True)
        sample_mean = np.mean(bootstrap_sample)
        simulated_means.append(sample_mean)
        
        if sample_mean > threshold:
            success_count += 1

    prob = float(success_count / n_simulations)

    return {
        "simulated_means": simulated_means,
        "probability": prob,
        "threshold": threshold,
        "n_simulations": n_simulations
    }

def bloom_filter_fpr(m: int, n: int, k: int) -> float:
    """
    Menghitung False Positive Rate (FPR) teoritis untuk struktur data Bloom Filter.

    Formula Wajib Kendala Tugas:
        FPR = (1 - (1 - 1/m)**n)**k

    Parameters
    ----------
    m : int — Ukuran bit array filter (kapasitas memori penyimpanan).
    n : int — Jumlah elemen yang dimasukkan (inserted elements) ke dalam filter.
    k : int — Jumlah fungsi hash yang digunakan.

    Returns
    -------
    float — Probabilitas False Positive Rate dalam rentang 0 sampai 1.
    """
    if m <= 0 or n <= 0 or k <= 0:
        raise ValueError("Nilai parameter m, n, dan k harus bilangan bulat positif > 0.")
        
    # Implementasi formula sesuai spesifikasi checklist penugasan kelompok
    fpr = (1 - (1 - 1/m)**n)**k
    return float(fpr)