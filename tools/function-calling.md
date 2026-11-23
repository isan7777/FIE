# Tool Contract: Structured Function Calling & Tool Registry

## 1. Arsitektur Function Calling FIE
FIE mengadopsi spesifikasi OpenAPI 3.0 / JSON Schema untuk seluruh pendaftaran function calling. Hal ini memastikan kompatibilitas penuh dengan Gemini API (`types.Tool`, `FunctionDeclaration`) serta framework model-agnostic lainnya.

## 2. Struktur Deklarasi Fungsi Terstandarisasi
```json
{
  "name": "calculate_hash",
  "description": "Menghitung digest hash SHA-256 dari string input.",
  "parameters": {
    "type": "OBJECT",
    "properties": {
      "input_string": {
        "type": "STRING",
        "description": "Teks sumber yang akan di-hash."
      }
    },
    "required": ["input_string"]
  }
}
```

## 3. Protokol Penanganan Function Calling di Runtime
1. Model mengembalikan kandidat `function_call` dengan `name` dan `args`.
2. FIE Tool Dispatcher memvalidasi tipe argumen terhadap skema.
3. FIE memeriksa permissions (`config/tool-permissions.yaml`).
4. Tool dieksekusi secara lokal atau remote.
5. Hasil dikemas dalam `function_response` dan dikirimkan kembali ke model untuk sintesis jawaban akhir.
