# Tool Contract: External HTTP / REST API Integration

## 1. Spesifikasi Tool
- **Nama Tool**: `http_request`
- **Fungsi**: Melakukan panggilan HTTP terisolasi ke API eksternal (GET, POST, PUT, DELETE) dengan penanganan header dan batas timeout aman.
- **Tingkat Akses**: External Network / Scoped Endpoint.

## 2. Parameter Pemanggilan
```json
{
  "url": { "type": "string", "required": true },
  "method": { "type": "string", "enum": ["GET", "POST", "PUT", "DELETE"], "default": "GET" },
  "headers": { "type": "object", "default": {} },
  "json_body": { "type": "object", "default": null },
  "timeout": { "type": "integer", "default": 10 }
}
```

## 3. Protokol Keamanan & Redaksi Kredensial
- Header sensitif (`Authorization`, `X-Api-Key`) dilarang dicatat dalam file log publik.
- Mengembalikan response status, headers, dan body dalam format JSON yang bersih.
- Menolak request ke IP lokal private/intranet yang tidak sah (mencegah SSRF terhadap `127.0.0.1` atau `169.254.169.254`) kecuali diizinkan secara eksplisit oleh konfigurasi.
