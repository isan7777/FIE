# Frontier Intelligence Engine (FIE)

Frontier Intelligence Engine (FIE) adalah framework orkestrasi kecerdasan buatan universal model-agnostic yang dirancang untuk memaksimalkan kapabilitas model bahasa (Large, Medium, dan Small Models) dalam rekayasa perangkat lunak, riset berbasis bukti, pemecahan masalah kompleks, dan otomatisasi workflow.

---

## 1. Pilar Utama FIE

1. **Adaptive Intelligence & Model Profiles**
   - Penyesuaian otomatis panjang instruksi, kedalaman dekomposisi langkah, dan alokasi token untuk profil `small` (misal: Gemini Flash-Lite), `medium` (misal: Gemini Flash), dan `large` (misal: Gemini Pro).
   - Menghindari reasoning berulang yang membuang konteks; mengutamakan eksekusi langkah demi langkah yang terarah.

2. **Specialized Multi-Agent Mesh**
   - Terdiri dari 9 agen peran terisolasi: **Orchestrator**, **Architect**, **Coder**, **Debugger**, **Researcher**, **Analyst**, **Designer**, **Tester**, dan **Writer**.
   - Dilengkapi pipeline simulasi deterministik (Sequential Agent Calling) untuk runtime model yang tidak mendukung native multi-agent.

3. **Persistent External Memory Engine**
   - SQLite external memory subsystem dengan full-text indexing, session summaries, project key-value facts, dan task tracking historis.

4. **Self-Verification & Quality Engine**
   - Validasi sintaks AST, kelengkapan kode, audit keamanan, pemeriksaan fakta, serta penegakan Zero Emoji/Sticker Policy.
   - Pelaporan status transparan (`VERIFIED`, `SYNTAX_PASSED`, `UNTESTED`, `NEEDS_REVIEW`).

5. **Tool Integration & Grounding Ready**
   - Dukungan function calling terstandarisasi, Google Search grounding, sandboxed local code execution, dan file management yang aman.

6. **Reproducible Evaluation & Benchmark Suite**
   - Benchmark bawaan untuk mengukur *correctness*, *completeness*, *efficiency*, *instruction adherence*, dan *context retention* pada berbagai model.

---

## 2. Struktur Arsitektur

```text
FRONTIER-INTELLIGENCE-ENGINE/
├── README.md                  # Gambaran umum, kapabilitas, & navigasi
├── CHANGELOG.md               # Riwayat versi dan perubahan fitur
├── LICENSE                    # Lisensi open-source (MIT License)
├── requirements.txt           # Dependensi Python minimal
├── core/                      # Fondasi instruksi FIE, identitas, & decision engine
├── agents/                    # Definisi & kontrak 9 agen spesialis
├── intelligence/              # Strategi pemecahan masalah & verifikasi mandiri
├── engineering/               # Panduan teknis arsitektur, backend, frontend, game, dll.
├── research/                  # Protokol riset primer, fact-checking, & validasi sumber
├── tools/                     # Kontrak tools (Search, Code Exec, File I/O, Functions)
├── memory/                    # Spesifikasi manajemen konteks & basis pengetahuan
├── workflows/                 # Standar Operasional Prosedur (SOP) pengerjaan end-to-end
├── knowledge/                 # Prinsip rekayasa, standar kode, & dokumentasi
├── evaluation/                # Test cases, benchmark runner, & matriks evaluasi
├── config/                    # Konfigurasi YAML (settings, model profiles, permissions)
├── templates/                 # Template kode, laporan riset, & deliverable
├── docs/                      # Panduan instalasi, arsitektur, & user guide
├── fie/                       # Python Runtime Package (Orchestrator, Loader, Memory, Tools)
└── tests/                     # Unit & integration tests untuk runtime FIE
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
```

### 3. Menjalankan CLI FIE
```bash
# Menjalankan orkestrasi tugas dalam mode simulasi/adaptif
python -m fie.cli run --task "Rancang REST API autentikasi JWT dengan FastAPI dan SQLite" --model-profile medium

# Memeriksa prompt kompilasi modular
python -m fie.cli inspect-prompt --task-type coding --model-profile small

# Menjalankan suite benchmark internal
python -m fie.cli benchmark --category coding

# Menjalankan pengujian sistem FIE
python -m unittest discover -s tests
```

---

## 4. Prinsip Integritas FIE
- **Fakta Nyata, Tanpa Halusinasi**: Tidak pernah memalsukan sitasi, URL, atau hasil eksekusi.
- **Transparansi Pengujian**: Jika kode belum diuji dalam runtime sungguhan, diberi label `UNTESTED`.
- **Eksekusi Presisi**: Mengutamakan file siap produksi utuh tanpa placeholder tersembunyi.
- **Zero Emoji / Sticker Invariant**: Bebas dari polusi emoji dekoratif di dalam kode, komentar, log, maupun dokumen teknis.
- **Model-Agnostic**: Bekerja optimal dari Google AI Studio, Gemini API, hingga CLI mandiri.
