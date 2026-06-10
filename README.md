# Statistical Health Audit — kubernetes/kubernetes
> **Final Group Assignment | Probability & Statistics | STI 2025**

## Project Description
Repositori ini berisi audit statistik menyeluruh terhadap proyek open-source `kubernetes/kubernetes`, platform orchestration container paling populer di dunia. Audit ini menerapkan teknik statistik dari Minggu 11–14 (estimasi, inferensi, uji hipotesis, dan simulasi komputasional).

---

## Research Questions

### 1. Estimation Layer  
Berapa estimasi probabilitas sebuah issue yang masuk memiliki label bug, dan berapa rata-rata harian frekuensi Pull Request (PR) baru yang dibuka di repositori Kubernetes?

### 2. Inference / Testing Layer  
Apakah terdapat perbedaan waktu penyelesaian (*time-to-close*) yang signifikan secara statistik antara issue yang berlabel bug dengan issue yang non-bug?

### 3. Simulation Layer  
Berapa probabilitas sebuah Pull Request (PR) baru akan membutuhkan waktu lebih dari 14 hari sampai akhirnya berhasil di-merge?

---

## Findings

> Akan diisi setelah semua layer selesai pada 10 Juni 2026

---


## How-to-Run

### 1. Clone Repositori
```bash
git clone https://github.com/stat-audit-kubernetes-sti-2025.git
cd stat-audit-kubernetes-sti-2025
```

### 2. Install Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Notebook 
```bash
jupyter notebook
```

## Team Table

| Anggota | Peran | Notebook |
|---------|-------|----------|
| Muhammad Asrofi Syaikho - 1519625049 | Data Engineer (Member A) | `01_eda.ipynb` |
| Amila Zahira - 1519625003 | Estimation Analyst (Member B) | `02_estimation.ipynb` |
| Mukgot Ega Sahputra - 1519625002 | Inference Analyst (Member C) | `03_confidence_interval.ipynb` |
| Nabila Nurfajriyasah - 1519625045 | Hypothesis Analyst (Member D) | `04_hypothesis_testing.ipynb` |
| Farhan Nabil Widodo - 1519625067 | Computation Analyst (Member E) | `05_simulation.ipynb` |