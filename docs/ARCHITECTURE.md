# Frontier Intelligence Engine (FIE) System Architecture

## 1. Ikhtisar Arsitektur Tingkat Tinggi
FIE dirancang dengan prinsip **Separation of Concerns**, **Model-Agnostic Modularity**, dan **Defensive Execution**.

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface / CLI                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Decision Engine & Master Orchestrator          │
│   (Task Classifier -> Complexity Scorer -> Agent Planner)   │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌──────────────────────────────┐ ┌────────────────────────────┐
│   Adaptive Model Profiler    │ │   Modular Prompt Loader    │
│  (Small / Medium / Large)    │ │  (Agents, Skills, SOPs)    │
└──────────────┬───────────────┘ └─────────────┬──────────────┘
               │                               │
               └───────────────┬───────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Specialized Agent Execution Mesh              │
│  [Architect] ──► [Coder] ──► [Debugger] ──► [Tester] ...   │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌──────────────────────────────┐ ┌────────────────────────────┐
│    External Memory Engine    │ │   Tool & Sandbox Engine    │
│  (SQLite Sessions, Facts,    │ │  (Python Exec, Safe Files, │
│   Task Ledgers, BM25 Index)  │ │   HTTP Client, Grounding)  │
└──────────────────────────────┘ └────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                Self-Verification Engine                     │
│  (AST Syntax Parser, Contract Checker, Security Auditor)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Lapisan Inti FIE
1. **Core & Decision Layer (`core/`, `fie/core/`)**:
   - `loader.py`: Mengkompilasi subset instruksi yang relevan secara dinamis agar model kecil tidak kelebihan beban token.
   - `orchestrator.py`: Mengatur alur penugasan agen dan transfer state artefak.
   - `adaptive.py`: Memetakan batasan model dan anggaran token.
2. **Specialist Agents (`agents/`)**:
   - Kontrak 9 agen mandiri dengan input, output, dan kriteria inspeksi formal.
3. **External Memory Subsystem (`memory/`, `fie/memory/`)**:
   - Basis data SQLite lokal untuk menyimpan sesi percakapan, fakta proyek terindeks, dan status riwayat pekerjaan.
4. **Tool Sandbox (`tools/`, `fie/tools/`)**:
   - Eksekusi kode subprocess aman dengan batas waktu dan proteksi path traversal.
5. **Self-Verification Engine (`intelligence/`, `fie/verification/`)**:
   - Evaluasi kelayakan sebelum output dinyatakan selesai (`VERIFIED`, `SYNTAX_PASSED`, `UNTESTED`).
