# Engineering Playbook: AI & LLM Systems Engineering

## 1. Prinsip Rekayasa Sistem AI & LLM
Integrasi Large Language Models (LLM) ke dalam sistem produksi menuntut pengendalian determinisme, efisiensi anggaran token, validasi skema keluaran, dan mekanisme fallback yang tahan terhadap kegagalan jaringan atau halusinasi model.

## 2. Arsitektur Prompt & Manajemen Konteks
- **Modular System Instruction**: Jangan menggabungkan seluruh dokumentasi ke dalam satu prompt monolitik. Gunakan pendekatan *Progressive Disclosure* yang hanya menyuntikkan identitas inti, kontrak peran aktif, dan playbook domain yang relevan.
- **Hierarki Penempatan Konteks**:
  1. *System Invariants & Security Boundaries* ditempatkan di bagian paling awal.
  2. *Domain Playbooks & Reference Facts* ditempatkan di bagian tengah.
  3. *Task Specification & Output Schema* ditempatkan di bagian akhir dekat titik generasi token.
- **Anggaran Token Adaptif**: Sesuaikan ukuran instruksi dengan kapasitas model (`small` < 1.200 token, `medium` < 3.500 token, `large` hingga 16.000 token).

## 3. Structured Outputs & Function Calling
- Wajib mendefinisikan skema JSON / OpenAPI 3.0 yang ketat untuk setiap respons terstruktur atau deklarasi tool (`FunctionDeclaration`).
- Lakukan validasi tipe dan batas nilai pada setiap argumen `function_call` sebelum mengeksekusi fungsi lokal atau kueri database.
- Tangani kegagalan parsing JSON dengan mekanisme *self-correction retry* maksimal 2 iterasi yang menyertakan pesan error validasi skema secara spesifik.

## 4. Retrieval-Augmented Generation (RAG) & Memori Eksternal
- Gunakan penyimpanan terstruktur (seperti SQLite atau vector/BM25 hybrid index) untuk menyimpan fakta proyek jangka panjang (`fie_project_facts`) dan riwayat tugas (`fie_tasks`).
- Batasi blok konteks memori yang disuntikkan ke bawah 400-500 token per giliran dengan mengambil fakta berperingkat relevansi tertinggi.
- Terapkan redaksi otomatis terhadap kredensial sensitif (API key, token Bearer, password) sebelum menyimpan teks ke dalam basis data memori.

## 5. Keamanan & Reliabilitas LLM (AI Safety & Guardrails)
- **Prompt Injection Defense**: Pisahkan instruksi sistem dari data input pengguna yang tidak tepercaya menggunakan pembatas struktural yang tegas.
- **Sandboxed Execution**: Jangan pernah menjalankan kode yang dihasilkan LLM secara langsung di proses utama aplikasi; gunakan subprocess terisolasi dengan batas waktu (`timeout`) dan pembatasan akses path (`workspace boundary check`).
- **Offline & Degraded Fallback**: Sediakan jalur fallback deterministik ketika endpoint API LLM mengalami rate-limit, timeout, atau ketiadaan koneksi.
