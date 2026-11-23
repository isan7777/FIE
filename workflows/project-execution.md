# Workflow: General Project Execution & Governance

## 1. Tujuan Workflow
Menjamin tata kelola eksekusi proyek secara menyeluruh, mencakup manajemen status, pembatasan token, dan kriteria rilis artefak.

## 2. Siklus Tata Kelola Eksekusi
1. **Kick-off & Pemetaan State**:
   - Periksa SQLite memory untuk memuat konteks sesi sebelumnya (jika ada).
   - Catat tujuan proyek dalam tabel `fie_tasks`.
2. **Eksekusi Fase Bertahap**:
   - Jangan jalankan semua tugas sekaligus dalam model kecil.
   - Selesaikan per fase, simpan checkpoint ke memory, lalu lanjutkan ke fase berikutnya.
3. **Penyimpanan Artefak & Snapshot**:
   - Simpan file yang dihasilkan ke sistem direktori kerja lokal.
   - Catat metadata file dalam memory eksternal.
4. **Verifikasi Akhir & Checklist Serah Terima**:
   - Pastikan semua checklist keberhasilan terpenuhi.
   - Perbarui changelog dan laporkan deliverable secara utuh.
