# Engineering Playbook: Performance Engineering & Optimization

## 1. Siklus Optimasi Berbasis Pengukuran
"Premature optimization is the root of all evil" (Donald Knuth). FIE menerapkan optimasi performa berdasarkan profil metrik nyata, bukan spekulasi.

## 2. Alur Diagnosa Performa (Measure -> Profile -> Optimize -> Verify)
1. **Measure (Ukur)**: Tetapkan baseline metrik sebelum melakukan perubahan apa pun (p95 latency, throughput req/s, penggunaan memori peak).
2. **Profile (Profil)**: Gunakan alat profiling untuk melacak bottleneck sebenarnya (CPU bound, I/O bound, atau lock contention).
3. **Optimize (Optimalkan)**: Terapkan perubahan terarah pada bottleneck teratas.
4. **Verify (Verifikasi)**: Ukur kembali di bawah beban kerja yang sama. Jika tidak menghasilkan peningkatan nyata, rollback perubahan.

## 3. Strategi Efisiensi Komputasi
- **Caching**: Simpan hasil komputasi berat dengan time-to-live (TTL) dan strategi invalidasi yang jelas (Cache-Aside, Write-Through).
- **Batching & Connection Pooling**: Kurangi round-trip I/O dengan menyatukan operasi database atau HTTP yang berulang.
- **Paginasi & Streaming**: Jangan memuat ribuan baris data ke dalam memori aplikasi sekaligus; gunakan cursor pagination atau data streaming generator.
- **Algoritma Efisien**: Hindari kompleksitas $O(n^2)$ pada koleksi dinamis; manfaatkan hash-map untuk lookup $O(1)$ dan binary search untuk data terurut.
