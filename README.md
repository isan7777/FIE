# Frontier Intelligence Engine (FIE)

Frontier Intelligence Engine (FIE) adalah framework orkestrasi kecerdasan buatan universal model-agnostic yang dirancang untuk memaksimalkan kapabilitas model bahasa (Large, Medium, dan Small Models) dalam rekayasa perangkat lunak, riset berbasis bukti, pemecahan masalah kompleks, audit keamanan, dan otomatisasi workflow.

---

## 1. Pilar Utama FIE

1. **Adaptive Intelligence & Model Profiles**
   - Penyesuaian otomatis panjang instruksi, kedalaman dekomposisi langkah, dan alokasi token untuk profil `small` (misal: Gemini Flash-Lite), `medium` (misal: Gemini Flash), dan `large` (misal: Gemini Pro).
   - Menghindari reasoning berulang yang membuang konteks; mengutamakan eksekusi langkah demi langkah yang terarah.

2. **Specialized Multi-Agent Mesh**
   - Terdiri dari 9 agen peran terisolasi: **Orchestrator**, **Architect**, **Coder**, **Debugger**, **Researcher**, **Analyst**, **Designer**, **Tester**, dan **Writer**.
   - Dilengkapi pipeline simulasi deterministik (Sequential Agent Calling) serta siklus koreksi mandiri otonom (Autonomous Self-Correction Loop) hingga 2 iterasi.

3. **Persistent External Memory Engine**
   - SQLite external memory subsystem (`fie_sessions`, `fie_messages`, `fie_tasks`, `fie_project_facts`) dengan keyword relevance retrieval, rolling-window message tracking, dan redaksi otomatis kredensial sensitif.

4. **Self-Verification & Quality Engine**
   - Validasi sintaks AST (baik file Python murni maupun blok kode Python di dalam dokumen Markdown), deteksi fungsi kosong/stub, audit keamanan (injeksi, `shell=True`, kredensial hardcoded), serta penegakan Zero Emoji/Sticker Policy.
   - Pelaporan status transparan (`VERIFIED`, `SYNTAX_PASSED`, `UNTESTED`, `NEEDS_REVIEW`, `FAILED`).

5. **Tool Integration & Grounding Ready**
   - Dukungan function calling terstandarisasi, Google Search grounding, sandboxed local code execution, dan file management dengan proteksi path traversal.

6. **Reproducible Evaluation & Benchmark Suite**
   - Benchmark kuantitatif bawaan di empat kategori (`Coding`, `Reasoning & Logic`, `Memory & Adherence`, `Tools & Sandboxing`) untuk mengukur *correctness*, *completeness*, *efficiency*, dan *adherence*.

---

## 2. Struktur Arsitektur

```text
FRONTIER-INTELLIGENCE-ENGINE/
├── SKILL.md                   # Master Antigravity Skill definition & progressive disclosure map
├── plugin.json                # Antigravity Plugin manifest
├── pyproject.toml             # Python package build & CLI script entry point ('fie')
├── README.md                  # Gambaran umum, kapabilitas, & navigasi
├── CHANGELOG.md               # Riwayat versi dan perubahan fitur
├── LICENSE                    # Lisensi open-source (MIT License)
├── requirements.txt           # Dependensi Python minimal
├── rules/                     # Global rules & invariants (AGENTS.md)
├── core/                      # Fondasi instruksi FIE, identitas, & decision engine
├── agents/                    # Definisi & kontrak 9 agen spesialis
├── intelligence/              # Strategi pemecahan masalah, koreksi mandiri, & verifikasi
├── engineering/               # 9 Playbook teknis (Backend, Frontend, DB, Security, AI/LLM, dll.)
├── research/                  # Protokol riset primer, fact-checking, & validasi sumber
├── tools/                     # Kontrak tools (Search, Code Exec, File I/O, Functions)
├── memory/                    # Spesifikasi manajemen konteks & basis pengetahuan SQLite
├── workflows/                 # 5 Standar Operasional Prosedur (SOP) pengerjaan end-to-end
├── knowledge/                 # Prinsip rekayasa, standar kode, & dokumentasi
├── evaluation/                # Test cases, benchmark runner, & matriks evaluasi
├── config/                    # Konfigurasi YAML (settings, model profiles, permissions)
├── templates/                 # Template kode, laporan riset, & deliverable
├── docs/                      # Panduan instalasi, arsitektur, & user guide
├── fie/                       # Python Runtime Package (Orchestrator, Loader, Memory, Verifier, CLI)
└── tests/                     # Unit & integration tests untuk seluruh subsistem FIE
```

---

## 3. Memulai Cepat (Quick Start)

### 1. Prasyarat
- Python 3.10+
- (Opsional) Google Gemini API Key (`GEMINI_API_KEY`)

### 2. Instalasi
```bash
cd FRONTIER-INTELLIGENCE-ENGINE
pip install -r requirements.txt
# Opsional: instal sebagai paket CLI editable
pip install -e .
```

### 3. Menjalankan CLI FIE
```bash
# Menjalankan orkestrasi tugas dalam mode simulasi/adaptif dengan deteksi domain otomatis
python -m fie.cli run --task "Rancang REST API autentikasi JWT dengan FastAPI dan SQLite" --model-profile medium

# Memeriksa prompt kompilasi modular dengan domain spesifik
python -m fie.cli inspect-prompt --task-type coding --agent coder --domain backend --model-profile small

# Memverifikasi file kode atau dokumen Markdown terhadap rubrik AST, keamanan, dan Zero Emoji Policy
python -m fie.cli verify --file fie/core/orchestrator.py

# Menampilkan daftar seluruh modul pengetahuan, playbook, workflow, dan agen FIE
python -m fie.cli list-modules

# Mengelola memori proyek SQLite
python -m fie.cli memory --action stats
python -m fie.cli memory --action set-fact --session-id "demo" --category ARCHITECTURE --key "db" --value "SQLite WAL"
python -m fie.cli memory --action facts --session-id "demo"

# Menjalankan suite benchmark internal (all, coding, reasoning, memory, tools)
python -m fie.cli benchmark --category all

# Menjalankan pengujian unit sistem FIE
python -m unittest discover -s tests
```

---

## 4. Prinsip Integritas FIE
- **Fakta Nyata, Tanpa Halusinasi**: Tidak pernah memalsukan sitasi, URL, atau hasil eksekusi.
- **Transparansi Pengujian**: Jika kode belum diuji dalam runtime sungguhan, diberi label `UNTESTED` atau `SYNTAX_PASSED`.
- **Eksekusi Presisi**: Mengutamakan file siap produksi utuh tanpa placeholder tersembunyi.
- **Zero Emoji / Sticker Invariant**: Bebas dari polusi emoji dekoratif di dalam kode, komentar, log, maupun dokumen teknis.
- **Model-Agnostic**: Bekerja optimal dari Antigravity IDE, Google AI Studio, Gemini API, hingga CLI mandiri.
