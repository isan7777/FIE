# Engineering Playbook: Software Architecture & System Design

## 1. Filosofi Arsitektur FIE
Arsitektur perangkat lunak yang unggul bukanlah yang paling rumit, melainkan yang paling adaptif terhadap perubahan kebutuhan dengan tetap mempertahankan kesederhanaan, kejelasan kepemilikan data, dan kemudahan pengujian.

## 2. Pola Arsitektur Pilihan

### Modular Monolith (Rekomendasi Awal)
- Cocok untuk sebagian besar aplikasi baru dan tim berskala kecil-menengah.
- Membagi domain menjadi modul independen dengan antarmuka eksplisit.
- Menghindari overhead jaringan dan orkestrasi microservice prematur.

### Clean / Hexagonal Architecture (Ports & Adapters)
- Lapisan domain entitas terisolasi sepenuhnya dari framework eksternal dan database.
- Lapisan use case mengorkestrasi alur bisnis.
- Lapisan adapter menangani komunikasi HTTP, CLI, database driver, dan message broker.

## 3. Aturan Desain Komponen
1. **Separation of Concerns**: Jangan campurkan logika bisnis dengan manipulasi DOM atau serialisasi SQL.
2. **Dependency Inversion**: Modul level tinggi tidak boleh bergantung langsung pada modul level rendah; keduanya harus bergantung pada abstraksi/interface.
3. **Single Responsibility**: Setiap modul atau kelas hanya memiliki satu alasan untuk berubah.
4. **Idempotensi**: Rancang operasi mutasi state agar aman dipanggil berulang kali tanpa efek samping ganda.
