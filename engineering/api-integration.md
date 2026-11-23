# Engineering Playbook: API Integration & Protocols

## 1. Standar Perancangan Kontrak API
API adalah kontrak antara penyedia dan konsumen. Kejelasan, konsistensi status code, dan validasi skema adalah prasyarat mutlak.

## 2. Praktik Terbaik RESTful API
- Gunakan kata benda jamak untuk endpoint sumber daya (misal: `/api/v1/users`, `/api/v1/projects/{id}/tasks`).
- Gunakan method HTTP sesuai semantik aslinya:
  - `GET`: Idempoten, aman, membaca data saja.
  - `POST`: Non-idempoten, membuat sumber daya baru.
  - `PUT`: Idempoten, mengganti seluruh representasi sumber daya.
  - `PATCH`: Memodifikasi sebagian atribut sumber daya.
  - `DELETE`: Menghapus sumber daya.
- Kembalikan HTTP Status Code yang tepat: `200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Entity`, `500 Internal Server Error`.

## 3. Integrasi API Pihak Ketiga (Third-Party Integration)
- Jangan pernah memanggil API eksternal secara sinkron tanpa batas waktu (selalu terapkan timeout eksplisit, misal: 5-10 detik).
- Gunakan Circuit Breaker untuk menghentikan pemanggilan terus-menerus saat layanan eksternal mengalami gangguan.
- Terapkan Webhook signature verification (HMAC SHA-256) untuk memastikan keaslian payload yang diterima.
- Simpan API Key dan kredensial eksternal di environment variables, jangan pernah di-hardcode.
