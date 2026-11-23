# Adaptive Intelligence Engine

## 1. Konsep Adaptasi Tingkat Model
Frontier Intelligence Engine tidak memaksakan instruksi berbobot besar pada model dengan kapasitas terbatas. FIE menerapkan strategi proporsional berdasarkan tiga tier model:

| Parameter | Small Model (Flash-Lite / Sub-8B) | Medium Model (Flash / 12B-30B) | Large Model (Pro / Ultra) |
| :--- | :--- | :--- | :--- |
| **Batas Target Prompt** | < 1,500 token | 1,500 - 4,000 token | Hingga 32,000+ token |
| **Gaya Instruksi** | Direktif imperatif ringkas | Terstruktur modular | Komprehensif analitis |
| **Chaining Agen** | 1 agen per langkah (Serial) | 2 agen per siklus | Mesh multi-agen terpadu |
| **Tingkat Dekomposisi**| Sangat teratomisasi | Bertahap menengah | Holistik end-to-end |
| **Alat / Function Calling** | 1 tool per panggilan | 1 - 3 tools per panggilan | Multi-tool paralel |
| **Intensitas Verifikasi** | Verifikasi sintaks cepat | Verifikasi fungsi & kontrak | Audit edge case & keamanan |

---

## 2. Strategi Khusus Model Kecil (Small Model Strategy)
Model kecil memiliki batasan dalam perhatian multi-halaman dan penalaran abstrak mendalam. Oleh karena itu:
1. **Pecah Pekerjaan Kompleks**: Jangan berikan instruksi 10 halaman sekaligus. Gunakan workflow bertahap (Planning terpisah -> Coding terpisah -> Testing terpisah).
2. **Konteks Tanpa Redundansi**: Pangkas riwayat percakapan lama; hanya sertakan ringkasan state terakhir dan skema data.
3. **Instruksi Monolitik Dilarang**: Muat hanya satu file modul spesialis yang sedang dikerjakan.
4. **Verifikasi Terfokus**: Fokuskan pada ketiadaan syntax error dan kesesuaian tipe data.
5. **Kejujuran Batas**: Jangan berasumsi model kecil dapat melakukan inferensi matematis rumit tanpa bantuan eksekusi Python.

---

## 3. Strategi Khusus Model Menengah (Medium Model Strategy)
1. Keseimbangan antara kecepatan inferensi dan ketepatan output.
2. Gunakan arsitektur multi-tahap (Architect merancang -> Coder mengeksekusi -> Tester memvalidasi).
3. Evaluasi edge-case standar pada input dan error handling.

---

## 4. Strategi Khusus Model Besar (Large Model Strategy)
1. Libatkan evaluasi keamanan mendalam (threat modeling, sanitasi input, mitigasi race condition).
2. Perencanaan arsitektur skala sistem (distribusi, caching, idempotensi).
3. Penulisan test suite otomatis komprehensif (unit, integration, dan boundary test cases).
