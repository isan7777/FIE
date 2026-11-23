# Memory Subsystem: Dynamic Knowledge Base & Retrieval

## 1. Mekanisme Retrieval Berbasis Relevansi
FIE menggabungkan pencarian kata kunci terindeks dan pemfilteran kategori untuk mengambil konteks pengetahuan yang paling relevan dengan kueri pengguna saat ini tanpa harus memuat seluruh database ke dalam prompt.

## 2. Alur Pengambilan Pengetahuan (Retrieval Pipeline)

```
[Kueri Pengguna Masuk]
         │
         ▼
[Ekstraksi Entity & Intent Keywords]
         │
         ▼
[Query SQL pada fie_project_facts & fie_tasks]
         │
         ▼
[Perhitungan Skor Relevansi (BM25 / Keyword Overlap)]
         │
         ▼
[Penyusunan Blok Konteks Ringkas (< 500 token)]
         │
         ▼
[Injeksi ke Prompt Agen Spesialis Aktif]
```

## 3. Tata Kelola Pengetahuan Proyek
- Setiap kali arsitektur baru disetujui (misal: "Database utama menggunakan PostgreSQL dengan UUID v4"), fakta ini dicatat sebagai `category: ARCHITECTURE` dalam memori proyek.
- Jika pengguna kemudian menanyakan "Buat skema tabel pembayaran", engine otomatis menarik fakta arsitektur tersebut agar tipe ID yang digunakan konsisten tanpa perlu diingatkan ulang oleh pengguna.
