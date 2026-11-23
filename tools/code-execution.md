# Tool Contract: Sandboxed Code Execution

## 1. Spesifikasi Tool
- **Nama Tool**: `execute_python_code`
- **Fungsi**: Mengeksekusi script Python dalam subprocess terisolasi untuk kalkulasi matematika presisi, validasi algoritma, atau unit testing lokal.
- **Tingkat Akses**: Local Subprocess Sandbox.

## 2. Parameter Pemanggilan
```json
{
  "code": {
    "type": "string",
    "description": "Script Python lengkap mandiri yang akan dieksekusi.",
    "required": true
  },
  "timeout_seconds": {
    "type": "integer",
    "description": "Batas waktu eksekusi dalam detik (default: 10, max: 30).",
    "default": 10
  }
}
```

## 3. Batasan Keamanan Sandbox (Safety Policy)
- Eksekusi dibatasi waktu (timeout) untuk mencegah infinite loops.
- Output dibatasi maksimal 32 KB untuk mencegah memory exhaustion.
- Dilarang mengeksekusi operasi destruktif sistem (seperti `rm -rf /` atau format partisi).
- Menangkap `stdout`, `stderr`, dan `exit_code` secara transparan.
