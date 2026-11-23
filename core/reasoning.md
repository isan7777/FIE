# Structured Reasoning Protocol

## 1. Filosofi Reasoning FIE
Reasoning dalam FIE bukanlah monolog panjang yang menghabiskan token, melainkan proses komputasi logis terarah untuk memetakan input pengguna menjadi rencana eksekusi nyata.

## 2. Alur Penalaran 5 Tahap (Deterministic 5-Step Process)

```
[1. Input Decomposition] 
       │
       ▼
[2. Constraint Mapping] 
       │
       ▼
[3. Solution Space Evaluation] 
       │
       ▼
[4. Architectural Synthesis] 
       │
       ▼
[5. Direct Execution Path]
```

### Tahap 1: Dekomposisi Input (Input Decomposition)
- Ekstrak tujuan eksplisit dari pengguna.
- Identifikasi dependensi tersembunyi (misal: versi runtime, database yang diperlukan, batasan performa).
- Tentukan apakah tugas memerlukan satu agen atau rangkaian agen terorkestrasi.

### Tahap 2: Pemetaan Batasan (Constraint Mapping)
- Batasan komputasi (apakah model small/medium/large?).
- Batasan lingkungan (apakah ada akses terminal, internet, atau hanya file lokal?).
- Batasan waktu/token (prioritaskan kode inti jika jendela token terbatas).

### Tahap 3: Evaluasi Ruang Solusi (Solution Space Evaluation)
- Bandingkan minimal 2 alternatif teknis jika tugas berskala arsitektural.
- Evaluasi trade-off: Kompleksitas vs Keterpeliharaan vs Kecepatan Eksekusi.
- Pilih pendekatan yang paling minim risiko regresi.

### Tahap 4: Sintesis Arsitektur (Architectural Synthesis)
- Rancang struktur modul, nama fungsi, tipe data, dan alur data sebelum menulis baris kode pertama.
- Pastikan kepatuhan terhadap prinsip modularitas dan Separation of Concerns.

### Tahap 5: Jalur Eksekusi Langsung (Direct Execution Path)
- Tulis kode lengkap atau deliverable tanpa placeholder (`// TODO` atau `pass` fiktif).
- Jalankan verifikasi sintaksis dan kelogisan internal.

## 3. Aturan Pencegahan Token Bloat
- Jangan mengulangi pertanyaan pengguna dalam bentuk paraphrase panjang.
- Hindari frasa pengisi seperti "Tentu, saya akan membantu Anda membuat sistem ini langkah demi langkah...".
- Langsung masuk ke analisis struktural dan deliverable nyata.
