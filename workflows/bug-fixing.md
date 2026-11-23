# Workflow: Systematic Bug Fixing & Root Cause Resolution

## 1. Tujuan Workflow
Menangani laporan cacat program, crash runtime, atau kegagalan logika secara presisi tanpa menimbulkan regresi pada bagian kode lain.

## 2. Alur Kerja Bedah Cacat (Surgical Bug Triage)

```
[Laporan Bug / Trace] ──► [DEBUGGER: Analisis RCA & Lokalisasi Masalah]
                                    │
                                    ▼
                          [CODER: Implementasi Perbaikan Minimalis]
                                    │
                                    ▼
                          [TESTER: Uji Regresi & Boundary Tests]
                                    │
                                    ▼
                          [WRITER: Catatan Rilis / Patch Note]
```

### Prosedur Operasional:
1. **Isolasi Masalah**: Debugger menganalisis stack trace dan log untuk menentukan nomor baris dan alur eksekusi pemicu error.
2. **Karakterisasi Cacat**: Tentukan apakah masalah disebabkan oleh:
   - Kesalahan tipe data atau nilai null/kosong.
   - Race condition / ketidakcocokan timing asynchronous.
   - Pelanggaran batas memori / array index out of bounds.
   - Inkonsistensi format payload eksternal.
3. **Patching**: Coder melakukan perbaikan bedah pada titik asal injeksi nilai keliru, bukan hanya menutupi baris crash dengan blok `try-except` kosong.
4. **Verifikasi**: Tester memverifikasi bahwa skenario pemicu bug berhasil ditangani dan seluruh rangkaian pengujian lama tetap lulus tanpa kendala.
