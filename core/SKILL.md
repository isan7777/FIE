---
name: frontier-intelligence-engine
description: Universal adaptive multi-agent AI framework for high-precision software engineering, research, and complex problem-solving across all Gemini tiers.
version: 1.0.0
author: FIE Core Architecture Team
---

# FRONTIER INTELLIGENCE ENGINE (FIE) CORE SKILL

Frontier Intelligence Engine (FIE) adalah sistem modulasi inteligensi tingkat lanjut yang mengorkestrasi kapabilitas model AI (Google Gemini Flash-Lite, Flash, Pro, dan AI Studio) untuk menghasilkan deliverable teknis siap pakai.

## 1. Operasi Inti
FIE beroperasi melalui empat tahap deterministik:
1. **Analisis Konteks & Klasifikasi Tugas**: Mengidentifikasi domain utama (Coding, Debugging, Research, Architecture, Writing).
2. **Penentuan Profil Model**: Menyesuaikan anggaran token dan kedalaman langkah (Small, Medium, Large).
3. **Pendelegasian Agen Spesialis**: Memuat instruksi peran terkait dari direktori `agents/`.
4. **Verifikasi & Evaluasi Mandiri**: Menguji validitas output sebelum diserahkan kepada pengguna.

## 2. Inisialisasi Dinamis
Ketika menerima permintaan:
- Baca file `core/identity.md` untuk komitmen persona dan integritas data.
- Periksa `config/model-profiles.yaml` untuk batasan parameter model aktif.
- Pilih alur kerja yang relevan dari `workflows/`.
- Validasi hasil akhir menggunakan kriteria dalam `intelligence/verification.md`.

## 3. Kompatibilitas Model
- **Small Model (Flash-Lite / Sub-8B)**: Gunakan instruksi ringkas dari modul, minimalkan token reasoning, fokus pada penyelesaian langkah tunggal terstruktur.
- **Medium Model (Flash / 12B-30B)**: Gunakan dekomposisi modular standar, chaining agen 2 tahap, dan verifikasi dasar.
- **Large Model (Pro / Ultra)**: Aktifkan full multi-agent orchestration, audit keamanan mendalam, verifikasi komprehensif, dan analisis skenario ekstrem.
