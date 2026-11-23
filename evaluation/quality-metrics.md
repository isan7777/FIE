# Evaluation Subsystem: Quality Metrics & Benchmark Rubrics

## 1. Rumus Perhitungan Metrik Kuantitatif

$$\text{Final Benchmark Score} = (0.35 \times \text{Correctness}) + (0.25 \times \text{Completeness}) + (0.20 \times \text{Adherence}) + (0.20 \times \text{Efficiency})$$

### Rincian Komponen:
1. **Correctness ($C$)**:
   $$\frac{\text{Jumlah Test Case yang Lulus}}{\text{Total Test Case}} \times 100\%$$
2. **Completeness ($K$)**:
   $$\frac{\text{Fitur / Modul yang Berfungsi Penuh}}{\text{Total Modul yang Diminta}} \times 100\%$$
3. **Adherence ($A$)**:
   $$\frac{\text{Batasan Teknis yang Ditaati}}{\text{Total Batasan}} \times 100\%$$
4. **Efficiency ($E$)**:
   Rasio pemanfaatan token: Penalti diberikan untuk setiap 1.000 token teks pengisi (filler/monolog berulang) yang tidak menghasilkan kode atau data relevan.

## 2. Kategori Ambang Batas Kelulusan (Pass Tiers)
- **Grade S (Production Ready)**: Skor Akhir $\ge 95\%$ (Bebas cacat, performa tinggi).
- **Grade A (Robust Standard)**: Skor Akhir $85\% - 94\%$ (Siap pakai dengan penyesuaian minor).
- **Grade B (Usable with Review)**: Skor Akhir $70\% - 84\%$ (Memerlukan review manual pada kasus batas).
- **Grade F (Unsatisfactory)**: Skor Akhir $< 70\%$ (Gagal pengujian kritis atau terjadi regresi).
