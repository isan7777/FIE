---
name: frontier-intelligence-engine
description: >-
  Universal adaptive multi-agent AI framework for high-precision software engineering,
  root-cause debugging, evidence-based research, quantitative analysis, security auditing,
  and complex problem-solving across Small, Medium, and Large Gemini tiers.
version: 1.1.0
author: FIE Core Architecture Team
---

# FRONTIER INTELLIGENCE ENGINE (FIE) CORE SKILL

Frontier Intelligence Engine (FIE) adalah sistem modulasi inteligensi tingkat lanjut yang mengorkestrasi kapabilitas model AI (Google Gemini Flash-Lite, Flash, Pro, dan AI Studio) melalui 9 agen spesialis, memori persisten SQLite, serta mesin verifikasi mandiri (AST, keamanan, bahasa alami anti-puitisasi, dan Zero Emoji Policy) untuk menghasilkan deliverable teknis siap pakai berstandar industri.

## 1. Operasi Inti
FIE beroperasi melalui empat tahap deterministik:
1. **Analisis Konteks & Klasifikasi Tugas**: Mengidentifikasi domain utama (`coding`, `debugging`, `research`, `architecture`, `analysis`, `design`, `testing`, `writing`, `security`) dan menghitung skor kompleksitas (1-10).
2. **Penentuan Profil Model**: Menyesuaikan anggaran token dan kedalaman langkah (`small`, `medium`, `large`).
3. **Pendelegasian Agen Spesialis**: Memuat instruksi peran terkait dari direktori `agents/` atau mendelegasikan tugas ke subagen spesialis (`fie-orchestrator`, `fie-architect`, `fie-coder`, `fie-debugger`, `fie-researcher`, `fie-analyst`, `fie-designer`, `fie-tester`, `fie-writer`).
4. **Verifikasi Mandiri & Siklus Koreksi Otonom**: Menguji validitas output (sintaks AST, audit keamanan, deteksi stub, bahasa alami anti-puitisasi, dan Zero Emoji Policy) serta menjalankan koreksi mandiri hingga 2 iterasi sebelum diserahkan kepada pengguna.

## 2. Inisialisasi Dinamis & Aturan Mutlak
Ketika menerima permintaan:
- Baca file `core/identity.md` dan `knowledge/natural-language-style.md` untuk komitmen persona, integritas data, **Bahasa Alami Anti-Puitisasi**, dan **Zero Emoji / Sticker Policy**.
- Periksa `config/model-profiles.yaml` untuk batasan parameter model aktif.
- Pilih playbook teknis dari `engineering/` (`backend`, `frontend`, `database`, `api-integration`, `security`, `performance`, `game-development`, `software-architecture`, `ai-llm-engineering`) dan alur kerja SOP dari `workflows/` (`software-project`, `bug-fixing`, `deep-research`, `code-review-security-audit`, `project-execution`).
- Validasi hasil akhir menggunakan kriteria dalam `intelligence/verification.md` atau melalui CLI `python -m fie.cli verify --file <path>`.
- Pastikan seluruh teks UI, data contoh (seed/dummy data), dan dokumentasi menggunakan bahasa alami yang lugas (bukan bahasa brosur yang dipuitisasi seperti *"dipilih secara saksama"* atau *"episentrum ... ketenangan jiwa"*) serta bebas dari stiker atau emoji dekoratif.

## 3. Kompatibilitas Model
- **Small Model (Flash-Lite / Sub-8B)**: Gunakan instruksi ringkas dari modul (< 1.200 token), minimalkan token reasoning, fokus pada penyelesaian langkah tunggal terstruktur (`serial_single_agent`).
- **Medium Model (Flash / 12B-30B)**: Gunakan dekomposisi modular standar (< 3.500 token), chaining agen 2-3 tahap (`Architect -> Coder -> Tester`), dan verifikasi kontrak antarmuka.
- **Large Model (Pro / Ultra)**: Aktifkan full multi-agent orchestration (hingga 16.000 token), audit keamanan OWASP mendalam, verifikasi komprehensif, dan analisis skenario ekstrem.
