# Evaluation Subsystem: Reasoning & Logic Test Cases

## 1. Test Case R-01: Resource Allocation & Dependency Graph (Topological Sort)
- **Tantangan**: Diberikan graf dependensi tugas dengan durasi waktu dan kapasitas pekerja paralel maksimal $K$, tentukan jadwal waktu penyelesaian tercepat (Critical Path Method) dan deteksi adanya siklus dependensi (deadlock).
- **Kriteria Keberhasilan**:
  1. Mendeteksi circular dependency secara akurat.
  2. Menghitung Makespan total secara presisi.

---

## 2. Test Case R-02: Cryptographic Key Rollover State Transition
- **Tantangan**: Rancang mesin status (state machine) untuk proses rollover asymmetric key tanpa waktu henti (zero downtime). Status mencakup: `GENERATED`, `ACTIVE_SIGN_VERIFY`, `ACTIVE_VERIFY_ONLY`, `RETIRED`, `REVOKED`.
- **Kriteria Keberhasilan**:
  1. Mencegah transisi ilegal (misal: dari `REVOKED` kembali ke `ACTIVE`).
  2. Menjamin pesan yang ditandatangani sebelum batas waktu tetap dapat diverifikasi.

---

## 3. Test Case R-03: Multi-Source Contradiction Resolution
- **Tantangan**: Diberikan tiga teks laporan rilis dengan tanggal berbeda yang menyebutkan batas parameter API yang berbeda. Tentukan nilai parameter mana yang benar pada versi saat ini dan jelaskan mengapa dua nilai lainnya sudah usang.
- **Kriteria Keberhasilan**:
  1. Mengidentifikasi rilis versi terbaru berdasarkan semver.
  2. Menolak data rilis usang secara logis dengan pembuktian kronologis.
