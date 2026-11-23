# Memory Subsystem: Persistent Project Memory (SQLite Schema)

## 1. Arsitektur Memori Eksternal FIE
FIE memanfaatkan SQLite sebagai basis penyimpanan persisten lokal yang ringan, tanpa dependensi server eksternal, dan langsung siap pakai.

## 2. Skema Relasional Tabel Memori

```sql
-- Tabel Sesi Percakapan & Status
CREATE TABLE IF NOT EXISTS fie_sessions (
    session_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    model_profile TEXT NOT NULL DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Riwayat Tugas & Status Eksekusi
CREATE TABLE IF NOT EXISTS fie_tasks (
    task_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    task_type TEXT NOT NULL,
    assigned_agent TEXT NOT NULL,
    status TEXT NOT NULL, -- PENDING, IN_PROGRESS, VERIFIED, FAILED
    input_payload TEXT,
    output_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES fie_sessions(session_id)
);

-- Tabel Fakta Proyek (Key-Value Knowledge Store)
CREATE TABLE IF NOT EXISTS fie_project_facts (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    category TEXT NOT NULL, -- ARCHITECTURE, DECISION, CREDENTIAL_SCHEMA, LIMITATION
    fact_key TEXT NOT NULL,
    fact_value TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES fie_sessions(session_id),
    UNIQUE(session_id, fact_key)
);

-- Indeks Pencarian Cepat
CREATE INDEX IF NOT EXISTS idx_tasks_session ON fie_tasks(session_id);
CREATE INDEX IF NOT EXISTS idx_facts_session ON fie_project_facts(session_id, category);
```

## 3. Protokol Pembaruan dan Penghapusan
- Pengguna dapat meminta penghapusan riwayat sesi kapan saja melalui perintah CLI atau API (`fie.memory.clear_session()`).
- Data sensitif (password asli, token rahasia) dilarang disimpan di tabel `fie_project_facts`; hanya struktur skema atau kunci referensial yang dicatat.
