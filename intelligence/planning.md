# Intelligence Framework: Dynamic Strategic Planning

## 1. Prinsip Perencanaan FIE
Rencana yang efektif bukanlah daftar statis yang kaku, melainkan pohon eksekusi dinamis yang mampu menyesuaikan diri dengan umpan balik runtime dan penemuan teknis baru.

## 2. Struktur Rencana Proyek (Work Breakdown Structure)

Setiap rencana yang disusun oleh FIE wajib memiliki elemen berikut:
1. **Milestone Utama**: Hasil besar yang dapat diverifikasi secara mandiri.
2. **Task Atomik**: Unit kerja terkecil yang dapat diselesaikan oleh satu agen dalam satu putaran konteks.
3. **Prasyarat & Dependensi**: Kondisi yang harus terpenuhi sebelum task dimulai.
4. **Kriteria Selesai (Definition of Done)**: Kondisi nyata yang menandai penyelesaian tugas (misal: "file `api/routes.py` dibuat dan lulus uji syntax").
5. **Rencana Kontingensi**: Langkah mitigasi jika terjadi kegagalan tak terduga.

## 3. Matriks Alokasi Sumber Daya & Token
- Untuk tugas berprioritas tinggi (core business logic), alokasikan kuota token reasoning dan verifikasi maksimal.
- Untuk tugas utilitas boilerplate, gunakan template standar ringkas untuk menghemat jendela konteks.

## 4. Mekanisme Dynamic Re-Planning
Jika dalam eksekusi ditemukan kendala struktural (misal: library yang direncanakan tidak kompatibel dengan versi Python aktif):
- Hentikan eksekusi sementara.
- Catat anomali sebagai fakta baru dalam state memori.
- Perbarui pohon rencana (re-plan) dengan alternatif yang valid sebelum melanjutkan.
