# Knowledge Base: Core Engineering Principles

## 1. Fondasi Rekayasa Perangkat Lunak FIE

### SOLID Principles
1. **Single Responsibility (SRP)**: Sebuah komponen atau modul hanya bertanggung jawab atas satu fungsionalitas spesifik.
2. **Open/Closed (OCP)**: Entitas software harus terbuka untuk perluasan (ekstensi), namun tertutup untuk modifikasi langsung.
3. **Liskov Substitution (LSP)**: Subkelas harus dapat menggantikan kelas induk tanpa merusak perilaku sistem.
4. **Interface Segregation (ISP)**: Klien tidak boleh dipaksa bergantung pada antarmuka yang tidak mereka gunakan.
5. **Dependency Inversion (DIP)**: Modul tingkat tinggi tidak boleh bergantung pada detail implementasi tingkat rendah; keduanya bergantung pada abstraksi.

### DRY (Don't Repeat Yourself) & Pragmatisme
- Hindari duplikasi logika bisnis krusial di beberapa tempat terpisah.
- Waspadai abstraksi prematur: jika dua potongan kode hanya kebetulan mirip namun melayani domain bisnis berbeda, duplikasi ringan lebih baik daripada kopling yang salah (*wrong abstraction*).

### KISS & YAGNI
- **KISS (Keep It Simple, Stupid)**: Solusi paling sederhana yang memenuhi semua kriteria pengujian adalah solusi terbaik.
- **YAGNI (You Aren't Gonna Need It)**: Jangan membangun fitur, abstraksi, atau plugin spekulatif sebelum kebutuhan konkret muncul.
