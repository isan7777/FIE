# Knowledge Base: Unified Programming Standards

## 1. Standar Mutu Kode FIE
Kode yang dihasilkan oleh FIE wajib memenuhi standar produksi industri terlepas dari bahasa pemrograman yang dipilih.

## 2. Standar Bahasa Spesifik

### Python (PEP 8 & Modern Python 3.10+)
- Wajib menggunakan Type Hints (`typing.Optional`, `list[str]`, `dict[str, Any]`, dsb.).
- Gunakan `pathlib.Path` untuk manipulasi file path lintas platform (hindari concatenasi string path manual).
- Gunakan context manager (`with open(...)`, `with sqlite3.connect(...)`) untuk menjamin pelepasan sumber daya.
- Pydantic atau Dataclasses untuk pemodelan data terstruktur.

### TypeScript / JavaScript (Modern ES2022+)
- Strict Type Checking (`strict: true` di tsconfig).
- Hindari penggunaan `any`; gunakan `unknown` dengan type narrowing atau interfaces konkret.
- Async/Await dengan penanganan `try/catch` eksplisit; hindari raw floating promises.

### SQL (ANSI SQL & SQLite / Postgres)
- Kata kunci SQL ditulis dalam HURUF KAPITAL (`SELECT`, `INSERT INTO`, `WHERE`, `JOIN`).
- Nama tabel dalam bentuk jamak snake_case (`users`, `task_records`).
- Wajib gunakan parameterized queries (`?` di SQLite, `$1` di Postgres) demi proteksi terhadap SQL Injection.

## 3. Konvensi Penamaan Variabel & Fungsi
- Nama variabel harus mendeskripsikan isi secara jelas (`user_account_id` alih-alih `uacc`).
- Fungsi harus berupa kata kerja yang menjelaskan aksi (`validate_token()`, `fetch_project_by_id()`).
- Konstanta ditulis dalam `UPPER_SNAKE_CASE`.
