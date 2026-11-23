# Research Protocol: Fact-Checking & Triangulation

## 1. Prinsip Triangulasi Fakta
Dalam FIE, satu sumber klaim tidak pernah dianggap sebagai fakta absolut kecuali berasal dari sumber primer yang otoritatif (seperti kode sumber asli atau spesifikasi formal).

## 2. Metodologi Triangulasi 3-Titik (3-Point Triangulation)
Untuk setiap klaim krusial (misal: benchmark performa, kerentanan CVE, klaim kompatibilitas):
1. **Titik 1 - Sumber Primer**: Dokumentasi rilis resmi atau spesifikasi arsitektur.
2. **Titik 2 - Bukti Empiris Eksternal**: Laporan uji independen, benchmark komunitas kredibel, atau issue tracker proyek.
3. **Titik 3 - Verifikasi Logis / Lokal**: Uji coba sintaks/perilaku langsung pada runtime jika tersedia.

## 3. Penandaan Derajat Keyakinan (Confidence Scoring)
- **High Confidence (Terbukti)**: Didukung oleh dokumentasi resmi dan verifikasi kode langsung.
- **Medium Confidence (Konsensus Terbatas)**: Didukung oleh diskusi teknis komunitas bereputasi, namun belum ada rilis resmi stabil.
- **Low Confidence / Unverified (Hipotesis)**: Klaim yang bersumber dari blog non-resmi atau opini pengguna tanpa reproduksi data. Wajib ditandai secara eksplisit kepada pengguna.
