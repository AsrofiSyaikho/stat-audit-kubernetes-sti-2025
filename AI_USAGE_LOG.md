# AI Usage Log — Kelompok 3_Kubernetes

## Summary

| Member | Role          | Tools           | ~% code AI-assisted | Interpretation cells AI-assisted? |
| ------ | ------------- | --------------- | ------------------- | --------------------------------- |
| Muhammad Asrofi Syaikho | Data Engineer | Claude, Gemini | 75% | No |   
| Amila Zahira | Estimation Analyst | Claude, Gemini | 65% | No | 
| Mukgot Ega Sahputra | Inference Analyst | Claude, Gemini | 80% | No | 
| Nabila Nurfajriyasah | Hypothesis Analyst | Claude, Gemini | 85% | No | 
| Nabil Farhan Widodo | Computation Analyst | Claude, Gemini | 90% | No | 

## Per-Member Detail

### Member A — [Muhammad Asrofi Syaikho]

| #   | Task | Tool | Prompt | How output was used |
| --- | ---- | ---- | ------ | ------------------- |
| 1 | Understanding What Is EDA, What does EDA do | Gemini | "Apa itu EDA dalam konteks Machine Learning" | Output was used to structure more prompt so the model would be more accurate / less hallucinate |  
| 2 | Create code to collect PR/Issues data from github API using python | Claude | "Mengikuti pendekatan SDLC dalam konteks Machine Learning. Berperanlah sebagai data engineer yang akan collect data PR serta Issue repo kubernetes di github. lalu melakukan Cleaning Data dan EDA awal" | Output was used to collect data from kubernetes repository |  

### Member B — [Amila Zahira]

| #   | Task | Tool | Prompt | How output was used |
| --- | ---- | ---- | ------ | ------------------- |
| 1 | Menyusun struktur fungsi estimator statistik | Claude | "Create reusable estimation functions for Bernoulli, Poisson, and Beta posterior analysis" | Output digunakan sebagai kerangka awal estimator.py lalu disesuaikan dengan formula dan kebutuhan analisis project|  
| 2 | Membantu pembuatan visualisasi likelihood dan posterior | Claude | "Generate matplotlib code for likelihood and posterior distribution visualization" | Output digunakan sebagai referensi awal visualisasi pada notebook estimasi dan dimodifikasi kembali

### Member C — [Mukgot Ega Sahputra]

| #   | Task | Tool | Prompt | How output was used |
| --- | ---- | ---- | ------ | ------------------- |
| 1 | Membantu mencari tau apa itu Confidence Interval pada konteks Statistika & Probabilitas | Gemini | "Apa itu Confidence Interval dengan konteks berdasarkan dari objektif yang telah di paparkan pada file .MD" | Output digunakan untuk membantu saya memahami apa itu confidence interval agar tidak terjadinya keluar jalur objektif |  
| 2 | Membantu membuat boilerplate code untuk inference dan confidence_interval | Claude | Generate saya code python dan ipynb mengenai confidence_interval berdasarkan konteks pada file .MD dan objektif research question yang saya berikan | Output digunakan untuk membantu saya membuat file confidence_interval dan inference |

### Member D — [Nabila Nurfajriyasah]

| # | Task | Tool | Prompt | How output was used |
|---|------|------|--------|---------------------|
| 1 | Pembuatan fungsi struktural untuk Z-test | Claude | "Buatlah kode program untuk tugas Anggota D dengan menggunakan kumpulan data yang disiapkan oleh Anggota A." | digunakan sebagai kerangka awal untuk berkas hypothesis.py, di mana fungsi z_test_one_sample dan z_test_two_sample diimplementasikan secara langsung sesuai dengan spesifikasinya. |
| 2 | Memverifikasi kebenaran rumus statistik Z | Claude | "Apakah kode ini sudah benar dan sesuai?" | Digunakan untuk memastikan bahwa baik rumus matematika maupun fungsi struktural benar-benar sudah sesuai dengan yang diminta. |

### Member E — [Farhan Nabil Widodo]

| #   | Task | Tool | Prompt | How output was used |
| --- | ---- | ---- | ------ | ------------------- |
| 1   | Menentukan metode simulasi yang paling relevan untuk estimasi durasi Pull Request (PR) | Gemini | "mana yg paling cocok dari simulasi untuk notebook 1.montecarlo 2.mcmc 3.blumfilter" | Digunakan sebagai bahan pertimbangan ilmiah dalam memilih metode. Hasilnya, Monte Carlo dipilih karena sesuai dengan karakteristik data empiris, sementara MCMC dinilai terlalu kompleks dan Bloom Filter diidentifikasi tidak relevan untuk pemodelan probabilitas. |
| 2   | Mengembangkan kode program simulasi Monte Carlo beserta visualisasi distribusinya | Gemini | "buat notebook dengan montecarlo simulation" | Kode yang dihasilkan diadopsi sebagai basis komputasi untuk memprediksi risiko keterlambatan pada 1.000 PR baru melalui 10.000 kali iterasi bootstrap, sekaligus menentukan nilai interval kepercayaan 95%. |

## Group Reflection (150–300 words)

How did your group's use of AI evolve over three weeks? What did AI handle well?
Where did output need significant correction? Was there a moment you chose _not_
to use AI — and why?_(repeat for all five members)_

## Group Reflection (150–300 words)

How did your group's use of AI evolve over three weeks? What did AI handle well?
Where did output need significant correction? Was there a moment you chose _not_
to use AI — and why?
