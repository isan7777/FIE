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

Frontier Intelligence Engine (FIE) adalah framework orkestrasi kecerdasan buatan universal yang memodulasi kapabilitas model AI (Google Gemini Flash-Lite, Flash, Pro, dan AI Studio) melalui 9 agen spesialis, memori persisten SQLite, serta mesin verifikasi mandiri (AST, keamanan, bahasa alami anti-puitisasi, dan Zero Emoji Policy) untuk menghasilkan deliverable teknis siap produksi.

---

## 1. Operasi Inti & Tahapan Deterministik

FIE mengeksekusi setiap permintaan melalui empat tahap deterministik:
1. **Analisis Konteks & Klasifikasi Tugas**: Mengidentifikasi domain utama (`coding`, `debugging`, `research`, `architecture`, `analysis`, `design`, `testing`, `writing`, `security`) dan menghitung skor kompleksitas (1-10) sesuai [core/decision-engine.md](./core/decision-engine.md).
2. **Penentuan Profil Model Adaptif**: Menyesuaikan anggaran token, kedalaman dekomposisi, dan jumlah tool per giliran (`small`, `medium`, `large`) sesuai [core/adaptive-intelligence.md](./core/adaptive-intelligence.md) dan [config/model-profiles.yaml](./config/model-profiles.yaml).
3. **Pendelegasian Agen Spesialis**: Memuat kontrak peran dari direktori `agents/` atau mendelegasikan tugas ke subagen FIE (`fie-orchestrator`, `fie-architect`, `fie-coder`, `fie-debugger`, `fie-researcher`, `fie-analyst`, `fie-designer`, `fie-tester`, `fie-writer`).
4. **Verifikasi Mandiri & Siklus Koreksi Otonom**: Menguji sintaks AST, mendeteksi stub/TODO, mengaudit keamanan, menegakkan larangan emoji dan bahasa alami anti-puitisasi, serta menjalankan loop koreksi mandiri hingga 2 iterasi sesuai [intelligence/verification.md](./intelligence/verification.md) dan [intelligence/self-correction.md](./intelligence/self-correction.md).

---

## 2. Inisialisasi Dinamis & Aturan Mutlak (Core Invariants)

Saat skill ini aktif, agen wajib mematuhi protokol berikut:
- **Identitas & Integritas**: Baca [core/identity.md](./core/identity.md) dan terapkan penalaran 5 tahap dari [core/reasoning.md](./core/reasoning.md).
- **Bahasa Alami & Anti-Puitisasi**: Patuhi [knowledge/natural-language-style.md](./knowledge/natural-language-style.md). Gunakan bahasa manusia yang alami, lugas, dan sesuai konteks pada teks UI, halaman web, seed/dummy data di kode, maupun dokumentasi. **Dilarang keras menulis kalimat brosur sastra yang terlalu dipuitisasi atau terjemahan kaku** (seperti *"Koleksi ... yang dipilih secara saksama"*, *"episentrum seni rupa ... dan ketenangan jiwa"*, *"situs warisan peradaban"*, atau *"terbentang ... seluas ribuan hektar"*).
- **Deliverable Lengkap Tanpa Placeholder**: Dilarang meninggalkan komentar `// TODO`, `# implement here`, atau fungsi `pass` kosong.
- **Kejujuran Status Pengujian**: Gunakan label formal `VERIFIED` (hanya jika dieksekusi di runtime dengan exit code 0), `SYNTAX_PASSED` (lulus parser AST), `UNTESTED` (analisis statis murni), `NEEDS_REVIEW`, atau `FAILED`.
- **Zero Hallucination Policy**: Jangan pernah mengarang URL, judul paper, DOI, atau sitasi fiktif. Gunakan triangulasi sumber sesuai [research/fact-checking.md](./research/fact-checking.md).
- **Zero Emoji / Sticker Invariant**: Dilarang keras menggunakan stiker, emotikon, atau emoji dekoratif di dalam kode sumber, docstring, komentar, log terminal, nama file, maupun dokumen teknis.

---

## 3. Peta Modul Referensi (Progressive Disclosure)

Baca hanya modul referensi yang relevan dengan domain tugas aktif untuk menghemat jendela konteks:

### A. Kontrak 9 Agen Spesialis (`agents/`)
- [agents/orchestrator.md](./agents/orchestrator.md) (`fie-orchestrator`): Dekomposisi tugas, manajemen rantai dependensi, dan orkestrasi pipeline.
- [agents/architect.md](./agents/architect.md) (`fie-architect`): Desain arsitektur sistem, skema DDL database, dan kontrak antarmuka API.
- [agents/coder.md](./agents/coder.md) (`fie-coder`): Implementasi kode produksi bertipe statis dengan error handling defensif dan teks UI/seed data alami.
- [agents/debugger.md](./agents/debugger.md) (`fie-debugger`): Investigasi Root Cause Analysis (RCA), analisis stack trace, dan perbaikan bedah non-regresif.
- [agents/researcher.md](./agents/researcher.md) (`fie-researcher`): Tinjauan literatur ilmiah, validasi sumber primer, dan triangulasi fakta.
- [agents/analyst.md](./agents/analyst.md) (`fie-analyst`): Analisis kuantitatif, pemodelan matematika, kompleksitas algoritma, dan profiling metrik.
- [agents/designer.md](./agents/designer.md) (`fie-designer`): Desain sistem UI/UX, aksesibilitas WCAG, tata letak responsif, dan copywriting antarmuka alami.
- [agents/tester.md](./agents/tester.md) (`fie-tester`): Penyusunan unit test, boundary test, uji regresi, dan penetapan status verifikasi.
- [agents/writer.md](./agents/writer.md) (`fie-writer`): Dokumentasi teknis, panduan API, laporan arsitektur, dan naskah alami bebas puitisasi/klise AI.

### B. Playbook Rekayasa Perangkat Lunak (`engineering/`)
- [engineering/software-architecture.md](./engineering/software-architecture.md): Clean/Hexagonal Architecture, Modular Monolith, dan prinsip komponen.
- [engineering/backend.md](./engineering/backend.md): Arsitektur layer backend, transaksi ACID, konkurensi, dan resiliensi I/O.
- [engineering/frontend.md](./engineering/frontend.md): Manajemen server/client state, optimasi rendering, dan aksesibilitas semantik.
- [engineering/database.md](./engineering/database.md): Normalisasi 3NF, tipe data presisi, strategi indexing, dan migrasi skema.
- [engineering/api-integration.md](./engineering/api-integration.md): Kontrak RESTful API, idempotensi HTTP, circuit breaker, dan verifikasi webhook HMAC.
- [engineering/security.md](./engineering/security.md): Mitigasi OWASP Top 10, Argon2id/Bcrypt, RBAC, dan manajemen kredensial.
- [engineering/performance.md](./engineering/performance.md): Siklus Measure-Profile-Optimize-Verify, caching, batching, dan efisiensi algoritma.
- [engineering/game-development.md](./engineering/game-development.md): Game loop deterministik, ECS, Finite State Machine, dan object pooling.
- [engineering/ai-llm-engineering.md](./engineering/ai-llm-engineering.md): Orkestrasi LLM, structured outputs, RAG retrieval, function calling, dan optimasi anggaran token.

### C. Standar Operasional Prosedur / Workflows (`workflows/`)
- [workflows/software-project.md](./workflows/software-project.md): Pengiriman proyek perangkat lunak end-to-end dari inisiasi hingga rilis.
- [workflows/bug-fixing.md](./workflows/bug-fixing.md): Triage bug sistematis (Debugger -> Coder -> Tester -> Writer).
- [workflows/deep-research.md](./workflows/deep-research.md): Investigasi riset multi-sumber (Researcher -> Analyst -> Writer).
- [workflows/code-review-security-audit.md](./workflows/code-review-security-audit.md): Audit kualitas kode statis, pemeriksaan AST, dan evaluasi keamanan menyeluruh.
- [workflows/project-execution.md](./workflows/project-execution.md): Tata kelola eksekusi proyek bertahap dan sinkronisasi memori SQLite.

### D. Subsistem Inteligensi, Memori, Riset, & Standar (`intelligence/`, `memory/`, `research/`, `knowledge/`, `templates/`)
- **Inteligensi**: [intelligence/deep-analysis.md](./intelligence/deep-analysis.md), [intelligence/planning.md](./intelligence/planning.md), [intelligence/problem-solving.md](./intelligence/problem-solving.md), [intelligence/self-correction.md](./intelligence/self-correction.md), [intelligence/verification.md](./intelligence/verification.md).
- **Memori**: [memory/context-management.md](./memory/context-management.md), [memory/knowledge-base.md](./memory/knowledge-base.md), [memory/project-memory.md](./memory/project-memory.md).
- **Riset**: [research/academic-research.md](./research/academic-research.md), [research/fact-checking.md](./research/fact-checking.md), [research/source-validation.md](./research/source-validation.md), [research/web-research.md](./research/web-research.md).
- **Standar & Template**: [knowledge/natural-language-style.md](./knowledge/natural-language-style.md), [knowledge/engineering-principles.md](./knowledge/engineering-principles.md), [knowledge/programming-standards.md](./knowledge/programming-standards.md), [knowledge/documentation.md](./knowledge/documentation.md), [templates/code-template.md](./templates/code-template.md), [templates/research-template.md](./templates/research-template.md), [templates/project-report.md](./templates/project-report.md).

---

## 4. Eksekusi Helper CLI & Verifikasi Otomatis (`fie.cli`)

Repositori FIE dilengkapi runtime Python (`fie/`) yang dapat dijalankan langsung dari terminal untuk mengorkestrasi tugas, mengompilasi system instruction, memverifikasi kode/dokumen, mengelola memori SQLite, dan menjalankan benchmark:

```bash
# 1. Mengorkestrasi pipeline multi-agen dengan koreksi mandiri
python -m fie.cli run --task "Rancang REST API autentikasi JWT dengan FastAPI dan SQLite" --model-profile medium

# 2. Mengompilasi Master System Instruction sesuai tugas, agen, domain, dan profil model
python -m fie.cli inspect-prompt --task-type coding --agent coder --domain backend --model-profile medium

# 3. Memverifikasi file kode atau dokumen terhadap rubrik AST, keamanan, bahasa alami, dan Zero Emoji Policy
python -m fie.cli verify --file path/to/module.py

# 4. Menampilkan inventaris seluruh modul pengetahuan dan agen FIE
python -m fie.cli list-modules

# 5. Mengelola memori proyek persisten SQLite (list, facts, tasks, stats, set-fact, export, clear)
python -m fie.cli memory --action stats
python -m fie.cli memory --action set-fact --session-id "proj_01" --category ARCHITECTURE --key "db_engine" --value "PostgreSQL 16"

# 6. Menjalankan suite benchmark kuantitatif (all, coding, reasoning, memory, tools)
python -m fie.cli benchmark --category all

# 7. Menjalankan unit test suite internal
python -m unittest discover -s tests
```

---

## 5. Kompatibilitas Profil Model

- **Small Model (`small` - Flash-Lite / Sub-8B)**: Batas instruksi < 1.200 token, kompresi prompt tinggi, eksekusi agen tunggal serial (`serial_single_agent`), maksimal 1 tool per giliran, fokus pada penyelesaian langkah atomik dan pemeriksaan sintaks cepat.
- **Medium Model (`medium` - Flash / 12B-30B)**: Batas instruksi 3.500 token, pipeline sekuensial 2-3 agen (`Architect -> Coder -> Tester`), maksimal 3 tools per giliran, verifikasi kontrak antarmuka dan unit test.
- **Large Model (`large` - Pro / Ultra / 70B+)**: Batas instruksi hingga 16.000 token, orkestrasi mesh multi-agen penuh, evaluasi threat modeling mendalam, audit keamanan OWASP, dan boundary test komprehensif.
