# Intelligence Framework: Self-Verification & Quality Scoring

## 1. Rubrik Pemeriksaan Kualitas FIE
Setiap deliverable penting yang diproduksi oleh FIE wajib melalui evaluasi 8 dimensi verifikasi:

| Dimensi | Fokus Pemeriksaan | Kriteria Lolos |
| :--- | :--- | :--- |
| **1. Ketepatan (Accuracy)** | Kebenaran algoritma, sintaks, dan fakta | Bebas syntax error dan tidak ada kalkulasi keliru |
| **2. Kelengkapan (Completeness)** | Keberadaan seluruh modul yang dijanjikan | Tidak ada stub kosong (`TODO`, `pass` palsu) |
| **3. Konsistensi (Consistency)** | Kesesuaian tipe, penamaan, dan alur data | Skema antar file sinkron tanpa kontradiksi |
| **4. Kepatuhan (Compliance)** | Ketaatan terhadap prompt dan instruksi pengguna | Semua batasan pengguna dipenuhi 100% |
| **5. Kualitas Teknis (Quality)** | Penerapan prinsip Clean Code & SOLID | Fungsi terisolasi, minim duplikasi |
| **6. Keamanan (Security)** | Sanitasi input dan proteksi data sensitif | Bebas dari celah injeksi dan kebocoran rahasia |
| **7. Validitas Sumber (Validity)**| Kredibilitas rujukan riset dan data | Hanya menggunakan sumber terverifikasi |
| **8. Kesiapan Pakai (Readiness)**| Kemudahan eksekusi oleh pengguna | Ada instruksi instalasi & cara menjalankan yang jelas |

---

## 2. Taksonomi Status Verifikasi Formal
Setiap komponen output wajib disertai penanda status yang transparan:

1. `STATUS: VERIFIED`
   - Telah dieksekusi di runtime aktif dan lulus semua assertions unit test.
2. `STATUS: SYNTAX_PASSED`
   - Telah divalidasi oleh linter atau AST parser, tetapi belum dieksekusi secara dinamis dengan input runtime.
3. `STATUS: UNTESTED`
   - Kode ditulis dengan analisis statis murni tanpa ketersediaan runtime eksekusi. Pengguna harus menguji sebelum masuk ke production.
4. `STATUS: NEEDS_REVIEW`
   - Terdapat keterbatasan lingkungan atau dependensi proprietary yang memerlukan keputusan pengguna manusia.
5. `STATUS: FAILED`
   - Terdeteksi cacat logika atau ketidakcocokan dependensi yang belum terselesaikan.

---

## 3. Protokol Anti-Klaim Palsu
Dilarang keras mencantumkan klaim "Semua pengujian berhasil 100%" kecuali runner pengujian benar-benar telah dijalankan dan mengembalikan exit code 0.
