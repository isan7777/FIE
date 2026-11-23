# Decision Engine & Dispatcher

## 1. Fungsi Utama Decision Engine
Decision Engine bertindak sebagai router logis sentral dalam FIE. Engine ini menganalisis query pengguna, menghitung skor kompleksitas, dan menentukan topologi eksekusi terbaik.

## 2. Matriks Klasifikasi Tugas & Routing

```
[Query Masuk]
      │
      ▼
[Analisis Intent & Domain]
      ├── 1. Software Engineering ──────► Architect -> Coder -> Tester
      ├── 2. Bug Fixing & Triage ────────► Debugger -> Coder -> Tester
      ├── 3. System Research ────────────► Researcher -> Analyst -> Writer
      ├── 4. UI/UX Design & Frontend ────► Designer -> Coder -> Tester
      └── 5. Architecture & Strategy ────► Architect -> Analyst -> Writer
```

## 3. Perhitungan Skor Kompleksitas Tugas (Complexity Scoring)

Formula Penentuan Level:
- **Tingkat 1 - Ringan (Skor 1-3)**: Tugas baris tunggal, refactoring lokal fungsi, atau kueri informasi spesifik.
  - *Aksi*: Eksekusi langsung oleh satu agen spesialis tanpa perantara berbelit.
- **Tingkat 2 - Menengah (Skor 4-7)**: Modul multi-fungsi, perancangan skema database, pembuatan endpoint API dengan dependensi eksternal.
  - *Aksi*: Alur 2 tahap (Architect membuat skema -> Coder menyelesaikan kode).
- **Tingkat 3 - Berat (Skor 8-10)**: Sistem penuh end-to-end, migrasi teknologi, orkestrasi multi-service, riset mendalam multi-dokumen.
  - *Aksi*: Alur orkestrator penuh (Orchestrator -> Architect -> Coder -> Tester -> Writer).

## 4. Mekanisme Fail-Safe & Fallback
- Jika tools eksternal (misal: pencarian web atau eksekusi kode) gagal merespons atau tidak tersedia:
  1. Catat error secara transparan.
  2. Beralih ke fallback logika offline yang mengandalkan basis pengetahuan internal.
  3. Informasikan kepada pengguna bahwa hasil dihasilkan secara offline dengan batas validitas tertentu.
