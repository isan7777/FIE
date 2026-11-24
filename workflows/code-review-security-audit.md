# Workflow: Comprehensive Code Review & Security Audit

## 1. Tujuan Workflow
Menjalankan audit kualitas kode, pemeriksaan arsitektur, analisis kerentanan keamanan (OWASP), dan verifikasi kelengkapan implementasi secara sistematis sebelum kode dinyatakan siap produksi.

## 2. Alur Orkestrasi Audit

```
[Kode Sumber / PR] ──► [ARCHITECT: Evaluasi Struktur, Coupling, & Kontrak]
                                  │
                                  ▼
                       [DEBUGGER: Audit Keamanan, Edge Cases, & Potensi Bug]
                                  │
                                  ▼
                       [TESTER: Verifikasi AST, Unit Tests, & Zero Emoji Policy]
                                  │
                                  ▼
                       [WRITER: Laporan Audit Terstruktur & Rekomendasi Patch]
```

## 3. Prosedur Operasional Standar
1. **Inspeksi Otomatis Awal**:
   - Jalankan `python -m fie.cli verify --file <target_file>` untuk memeriksa validitas sintaks AST, mendeteksi fungsi kosong (`pass`), komentar placeholder (`TODO`/`FIXME`), pola berbahaya (`eval`, `exec`, `shell=True`, kredensial hardcoded), serta pelanggaran Zero Emoji Policy.
2. **Audit Arsitektur & Keterpeliharaan (Architect)**:
   - Periksa kepatuhan terhadap prinsip SOLID, Separation of Concerns, dan ketiadaan circular dependencies.
   - Pastikan kontrak input/output memiliki anotasi tipe statis yang lengkap.
3. **Audit Keamanan & Ketahanan Runtime (Debugger)**:
   - Periksa sanitasi batas input, proteksi path traversal, parameterized SQL queries, dan penanganan eksepsi spesifik (tidak ada bare `except: pass`).
   - Evaluasi potensi race condition, kebocoran resource (file/koneksi tidak ditutup), dan ketiadaan timeout pada panggilan jaringan/subprocess.
4. **Verifikasi Pengujian (Tester)**:
   - Jalankan suite unit test dan boundary test yang relevan.
   - Tetapkan status verifikasi formal (`VERIFIED`, `SYNTAX_PASSED`, `NEEDS_REVIEW`, atau `FAILED`) beserta grade kualitas (`S`, `A`, `B`, atau `F`).
