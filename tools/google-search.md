# Tool Contract: Google Search & Grounding Integration

## 1. Spesifikasi Tool
- **Nama Tool**: `google_search_grounding`
- **Fungsi**: Melakukan penelusuran fakta terkini melalui integrasi Google Search Grounding resmi Gemini API.
- **Tingkat Akses**: Read-Only / External Network.

## 2. Parameter Pemanggilan
```json
{
  "query": {
    "type": "string",
    "description": "Kata kunci pencarian spesifik (bukan pertanyaan panjang).",
    "required": true
  },
  "max_results": {
    "type": "integer",
    "description": "Jumlah sumber maksimal yang diambil (default: 5).",
    "default": 5
  }
}
```

## 3. Format Respons & Penanganan Grounding
- Tool mengembalikan array objek dengan atribut: `title`, `url`, `snippet`, dan `timestamp`.
- Jika Google Search Grounding diaktifkan via SDK (`tools=[{"google_search": {}}]`), model memanfaatkan grounding chunks secara otomatis.
- **Fallback Policy**: Jika kuota habis atau jaringan terputus, kembalikan status error `NETWORK_UNAVAILABLE` dan beralih ke offline knowledge base dengan peringatan eksplisit.
