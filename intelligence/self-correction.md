# Intelligence Framework: Self-Correction & Feedback Loop

## 1. Siklus Koreksi Mandiri FIE
Koreksi mandiri adalah kemampuan FIE untuk mengevaluasi keluarannya sendiri, mendeteksi cacat logika, sintaks, atau inkonsistensi, dan memperbaikinya secara otonom sebelum menyerahkan artefak kepada pengguna.

## 2. Diagram Alur Koreksi (Autonomous Feedback Loop)

```
[Output Awal Terbentuk]
           │
           ▼
[Inspeksi Statis / Syntax Check] ──► (Gagal) ──► [Perbaiki Token/Sintaks] ──┐
           │                                                                 │
         (Lulus)                                                             │
           ▼                                                                 │
[Verifikasi Kontrak & Tipe Data] ──► (Gagal) ──► [Sinkronkan Interface] ────┤
           │                                                                 │
         (Lulus)                                                             │
           ▼                                                                 │
[Uji Konsistensi Konteks]       ──► (Gagal) ──► [Eliminasi Kontradiksi] ────┘
           │
         (Lulus)
           ▼
[Output Akhir Terverifikasi]
```

## 3. Aturan Batas Koreksi (Circuit Breaker)
- Batas iterasi koreksi otonom adalah **2 kali**.
- Jika setelah 2 kali perbaikan sistem masih mendeteksi kegagalan:
  1. Hentikan loop otomatis guna mencegah konsumsi token sia-sia.
  2. Laporkan secara jujur titik kegagalan, analisis penyebab kebuntuan, dan sajikan opsi keputusan kepada pengguna manusia.

## 4. Pola Anti-Regresi
- Setiap kali memperbaiki suatu bug, pastikan baris perbaikan tidak menghapus fitur yang sebelumnya sudah benar.
- Bandingkan diff perubahan untuk memastikan intervensi bersifat bedah (*surgical intervention*).
