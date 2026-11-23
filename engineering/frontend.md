# Engineering Playbook: Modern Frontend Engineering

## 1. Standar Rekayasa Frontend
Pengembangan frontend modern menuntut kecepatan render, struktur state yang terprediksi, aksesibilitas tinggi, dan integrasi API yang tahan banting.

## 2. Prinsip Manajemen State
- **Server State vs Client State**: Bedakan data yang bersumber dari server (caching, revalidation, invalidation) dengan state antarmuka lokal murni (modal terbuka, tab aktif).
- **Single Source of Truth**: Hindari duplikasi state yang dapat memicu desinkronisasi tampilan.
- **Immutability**: Perbarui state melalui mutasi murni atau setter yang terkelola.

## 3. Optimasi Performa Rendering
- Hindari re-render yang tidak perlu dengan pemisahan komponen granular.
- Terapkan lazy loading dan dynamic imports untuk rute dan komponen besar.
- Optimalkan pemuatan gambar dengan rasio aspek eksplisit dan format modern (WebP/AVIF).
- Eliminasi Cumulative Layout Shift (CLS) dengan menyediakan placeholder dimensi elemen.

## 4. Aksesibilitas (A11y) & Desain Responsif
- Gunakan elemen HTML semantik (`<main>`, `<nav>`, `<article>`, `<button>`) daripada tumpukan `<div>` interaktif tanpa peran.
- Pastikan semua interaksi dapat diakses melalui keyboard (tab order, focus ring terlihat).
- Terapkan media queries fluid dan pendekatan Mobile-First.
