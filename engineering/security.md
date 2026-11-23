# Engineering Playbook: Security Engineering & Threat Mitigation

## 1. Prinsip Keamanan FIE (Security by Design)
Keamanan bukanlah lapisan yang ditempelkan di akhir proyek, melainkan bagian integral dari setiap keputusan arsitektural dan implementasi kode.

## 2. Mitigasi Risiko Utama (OWASP Top 10)
- **Injection (SQL, NoSQL, OS Command)**:
  - Wajib gunakan parameter query / prepared statements untuk seluruh interaksi database.
  - Jangan pernah merangkai string raw user input ke dalam perintah sistem (`exec`, `system`, `eval`).
- **Autentikasi & Otorisasi Cacat**:
  - Terapkan hashing password dengan algoritma adaptif kuat (Argon2id atau Bcrypt).
  - Validasi token sesi atau JWT pada setiap request dengan pemeriksaan signature dan expiration.
  - Terapkan Role-Based Access Control (RBAC) pada lapisan layanan secara terpusat.
- **Cross-Site Scripting (XSS)**:
  - Lakukan sanitasi dan escaping pada seluruh output data dinamis yang dirender ke browser.
  - Terapkan header Content-Security-Policy (CSP) yang ketat.
- **Cross-Site Request Forgery (CSRF)**:
  - Gunakan cookie SameSite dan token anti-CSRF untuk request mutasi state.

## 3. Manajemen Rahasia & Kredensial
- Semua rahasia (API keys, database passwords, private keys) harus dimuat melalui Environment Variables.
- Pastikan berkas konfigurasi lokal (`.env`) selalu tercantum dalam `.gitignore`.
- Berikan prinsip *Least Privilege* pada kredensial aplikasi di level database dan cloud service.
