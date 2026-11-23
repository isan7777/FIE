# Workflow: End-to-End Software Project Delivery

## 1. Tujuan Workflow
Panduan operasional standar untuk membangun proyek perangkat lunak dari inisiasi kebutuhan hingga artefak produksi yang siap dieksekusi.

## 2. Tahapan Eksekusi Terorkestrasi

```
[Tahap 1: Inisiasi & Analisis] ──► ORCHESTRATOR
       │
       ▼
[Tahap 2: Desain Arsitektur]   ──► ARCHITECT
       │
       ▼
[Tahap 3: Desain UI/UX & Data] ──► DESIGNER / ARCHITECT
       │
       ▼
[Tahap 4: Implementasi Kode]   ──► CODER
       │
       ▼
[Tahap 5: Pengujian & Linter]  ──► TESTER
       │
       ▼
[Tahap 6: Dokumentasi & Rilis] ──► WRITER
```

### Prosedur Detail Tiap Tahap:
1. **Inisiasi**: Orchestrator memeriksa kebutuhan pengguna, mencatat batasan platform, dan memilih profil model (`small`/`medium`/`large`).
2. **Arsitektur**: Architect menyusun diagram komponen, kontrak data, dan struktur direktori proyek.
3. **Desain Interaksi**: Designer menetapkan struktur antarmuka dan alur pengguna (jika mencakup frontend).
4. **Coding**: Coder menulis implementasi file per file dari modul fondasi hingga controller. Tidak meninggalkan placeholder.
5. **Testing**: Tester membuat suite pengujian dan melakukan verifikasi sintaks serta unit testing. Menandai status pengujian secara eksplisit.
6. **Dokumentasi**: Writer menyusun README panduan instalasi, konfigurasi environment, dan cara menjalankan aplikasi.
