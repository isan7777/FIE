# Engineering Playbook: Database Architecture & Data Modeling

## 1. Prinsip Pemodelan Data
Data adalah aset paling persisten dalam suatu sistem. Kesalahan desain skema database jauh lebih sulit diperbaiki daripada kesalahan kode logika aplikasi.

## 2. Standar Desain Relasional (SQL)
- **Normalisasi**: Terapkan bentuk normal ketiga (3NF) secara default untuk menjamin integritas data dan meminimalkan anomali pembaruan. Lakukan denormalisasi selektif hanya jika terbukti dibutuhkan oleh metrik query berat.
- **Tipe Data Spesifik**: Hindari penggunaan kolom teks generik (`VARCHAR(255)`) untuk data numerik, tanggal, atau boolean. Gunakan tipe data bawaan yang tepat (`INTEGER`, `TIMESTAMPTZ`, `BOOLEAN`, `UUID`).
- **Integritas Referensial**: Terapkan foreign key constraints dengan aturan aksi yang jelas (`ON DELETE CASCADE` atau `ON DELETE RESTRICT`).

## 3. Strategi Indexing & Optimasi Query
- Berikan index pada kolom yang sering digunakan dalam klausul `WHERE`, `JOIN`, dan `ORDER BY`.
- Pahami trade-off index: setiap index mempercepat pembacaan data tetapi memperlambat operasi penulisan (`INSERT`/`UPDATE`).
- Evaluasi query execution plan (`EXPLAIN ANALYZE`) untuk menghindari pemindaian tabel penuh (Full Table Scan) pada tabel besar.

## 4. Manajemen Migrasi Skema
- Semua perubahan skema harus terdokumentasi dalam berkas migrasi berurutan (up/down migrations) yang version-controlled.
- Migrasi harus dapat diuji kembali secara idempotensial pada lingkungan staging sebelum diterapkan ke production.
