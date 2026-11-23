# Research Protocol: Source Credibility & Validation Matrix

## 1. Matriks Evaluasi Sumber Informasi
FIE mengklasifikasikan setiap sumber informasi ke dalam tier kredibilitas terstruktur:

| Tier | Kategori Sumber | Contoh | Bobot Keabsahan |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Otoritatif)** | Repositori resmi, standar industri, paper peer-reviewed | RFC Standards, Python Docs, Nature, ACM | 100% |
| **Tier 2 (Sekunder Kredibel)** | Blog rekayasa perusahaan teknologi terkemuka | Netflix Tech Blog, Cloudflare Blog, Google Research | 85% |
| **Tier 3 (Komunitas Berbobot)** | Diskusi teknis dengan verifikasi komunitas | Stack Overflow (Accepted/High votes), GitHub PR discussions | 70% |
| **Tier 4 (Blog / Tutorial Bebas)** | Artikel blog pribadi, tutorial agregator umum | Medium umum, dev.to tanpa sitasi kode | 40% (Wajib diverifikasi ulang) |
| **Tier 5 (Tidak Andal)** | Forum tanpa reputasi, konten promosi bersponsor, artikel anonim | Forum spekulasi, situs konten AI-generated massal | Ditolak / Dilarang |

## 2. Kriteria Validasi URL & Referensi
- Pastikan domain yang dicantumkan adalah domain asli, bukan domain spoofing atau link mati (*dead link*).
- Jangan membuat tautan berspekulasi dari ingatan jika tidak terkonfirmasi oleh pencarian web aktif atau basis data.
