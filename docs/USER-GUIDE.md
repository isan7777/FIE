# Frontier Intelligence Engine (FIE) User Guide

## 1. Panduan Penggunaan CLI
FIE menyediakan antarmuka baris perintah (CLI) yang intuitif untuk mengorkestrasi tugas, menginspeksi prompt kompilasi, dan menjalankan benchmark.

### A. Mengorkestrasi Tugas Nyata
```bash
# Menjalankan tugas dengan profil model default (medium)
python -m fie.cli run --task "Rancang skema database e-commerce lengkap dengan SQLite DDL"

# Menggunakan profil Small Model (eksekusi sangat teratomisasi dan hemat token)
python -m fie.cli run --task "Perbaiki fungsi rekursif yang mengalami RecursionError" --model-profile small

# Menggunakan profil Large Model (analisis mendalam arsitektural)
python -m fie.cli run --task "Rancang arsitektur sistem pembayaran mikro dengan proteksi double-spending" --model-profile large
```

### B. Menginspeksi Kompilasi Prompt Modular
Lihat bagaimana prompt dikemas secara dinamis untuk jenis tugas dan profil model tertentu tanpa harus mengeksekusi LLM:
```bash
python -m fie.cli inspect-prompt --task-type coding --model-profile small
```

### C. Menjalankan Internal Benchmark
Bandingkan performa evaluasi sistem:
```bash
# Jalankan seluruh benchmark
python -m fie.cli benchmark --category all

# Jalankan benchmark kategori coding
python -m fie.cli benchmark --category coding
```

### D. Manajemen Memori SQLite
Periksa atau hapus memori sesi proyek:
```bash
# Melihat daftar fakta memori sesi aktif
python -m fie.cli memory --action list

# Menghapus memori sesi
python -m fie.cli memory --action clear --session-id "default_session"
```

---

## 2. Penggunaan Bersama Google AI Studio
1. Buka [Google AI Studio](https://aistudio.google.com/).
2. Buat Prompt Baru -> Pilih Model (misal: Gemini 2.5 Flash atau Gemini 1.5 Pro).
3. Di bagian **System Instructions**, tempelkan hasil kompilasi prompt modular dari:
   ```bash
   python -m fie.cli inspect-prompt --task-type coding --model-profile medium
   ```
4. Tambahkan Tools bawaan Google Search Grounding atau Code Execution di panel samping AI Studio jika diinginkan.
5. Jalankan interaksi dengan jaminan struktur dan keandalan FIE.
