# Tool Contract: Safe File Management

## 1. Spesifikasi Tool
- **Kumpulan Tool**: `read_file`, `write_file`, `list_directory`
- **Fungsi**: Membaca, menulis, dan memeriksa struktur file proyek pada direktori kerja lokal yang diizinkan.
- **Tingkat Akses**: Local Workspace File I/O (Restricted Path).

## 2. Parameter Pemanggilan
```json
// read_file
{
  "path": { "type": "string", "required": true }
}

// write_file
{
  "path": { "type": "string", "required": true },
  "content": { "type": "string", "required": true },
  "overwrite": { "type": "boolean", "default": false }
}

// list_directory
{
  "path": { "type": "string", "default": "." },
  "depth": { "type": "integer", "default": 2 }
}
```

## 3. Kebijakan Keamanan Jalur (Path Sanitization)
- Validasi terhadap path traversal: Tolak akses di luar workspace kerja pengguna (`../..` keluar dari root).
- Jangan menimpa file yang sudah ada kecuali parameter `overwrite: true` diberikan secara sadar.
- Buat parent directory secara otomatis jika belum tersedia.
