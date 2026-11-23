# Installation & Environment Setup Guide

Panduan resmi instalasi dan konfigurasi **Frontier Intelligence Engine (FIE)**.

---

## 1. Prasyarat Sistem
- **Python**: Versi 3.10, 3.11, 3.12, atau 3.13+.
- **Sistem Operasi**: Windows, Linux, atau macOS.
- **SQLite3**: Bawaan standar instalasi Python standard library.

---

## 2. Langkah Instalasi

### Langkah A: Clone atau Siapkan Direktori
```bash
cd C:\Users\acer\Downloads\Installer\Projects\FRONTIER-INTELLIGENCE-ENGINE
```

### Langkah B: Buat Virtual Environment (Direkomendasikan)
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Langkah C: Instalasi Dependensi
```bash
pip install -r requirements.txt
```

---

## 3. Konfigurasi Google Gemini API (Opsional)
FIE dapat dijalankan dalam mode simulasi offline deterministik tanpa API key, atau terhubung langsung dengan Google Gemini API:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSyYourApiKeyHere..."

# Linux / macOS
export GEMINI_API_KEY="AIzaSyYourApiKeyHere..."
```

---

## 4. Verifikasi Instalasi
Jalankan test suite internal untuk memastikan semua modul berfungsi:
```bash
python -m unittest discover -s tests
```
Jika seluruh pengujian mengembalikan `OK`, FIE siap digunakan sepenuhnya.
