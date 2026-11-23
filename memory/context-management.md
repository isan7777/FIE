# Memory Subsystem: Context Management & Compression

## 1. Tantangan Jendela Konteks
Konteks LLM terbatas oleh ukuran jendela token dan degradasi perhatian di bagian tengah (*lost in the middle*). Menjejalkan seluruh percakapan secara mentah menyebabkan inefisiensi biaya dan penurunan kualitas respon.

## 2. Strategi Manajemen Konteks FIE
- **Rolling Window Summarization**: Ketika jumlah putaran interaksi melebihi ambang batas, riwayat lama diringkas menjadi daftar poin fakta kunci (*State Ledger*).
- **Hierarchical Context Injection**:
  1. *Layer 1 (Statik)*: Master System Instruction & Persona Inti (~500 token).
  2. *Layer 2 (Spesialis Terpilih)*: Modul agen yang aktif saat ini (~800 token).
  3. *Layer 3 (Memori Proyek)*: Fakta dan keputusan teknis yang telah disepakati (~400 token).
  4. *Layer 4 (Task Sekarang)*: Instruksi pengguna dan input spesifik langkah aktif.
- **Pembersihan Token Berlebih**: Hapus percakapan basa-basi, peringatan linter yang redundan, dan output data yang tidak lagi relevan bagi langkah selanjutnya.
