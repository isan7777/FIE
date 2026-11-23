# Evaluation Subsystem: Coding Test Cases

## 1. Test Case C-01: LRU Cache Implementation with TTL
- **Tantangan**: Buat kelas `LRUCache` dengan kapasitas tetap, operasi $O(1)$ untuk `get` dan `put`, serta dukungan time-to-live (TTL) kadaluarsa otomatis.
- **Kriteria Keberhasilan**:
  1. Operasi get pada key kadaluarsa mengembalikan `None`.
  2. Eviction policy menghapus key paling jarang digunakan saat kapasitas penuh.
  3. Lulus uji konkurensi dasar atau thread-safety jika diminta.
- **Assertion**:
  - `cache.put("k1", "v1", ttl=1); sleep(1.1); assert cache.get("k1") is None`
  - `cache.put("k2", "v2"); cache.put("k3", "v3"); assert cache.get("k2") == "v2"`

---

## 2. Test Case C-02: Safe JSON Path Extractor with Fallback
- **Tantangan**: Buat fungsi `extract_path(data: dict, path: str, default: Any = None) -> Any` yang mampu mengekstrak path bersarang (seperti `"users.0.profile.email"`) tanpa melempar `KeyError` atau `IndexError`.
- **Kriteria Keberhasilan**:
  1. Menangani array indeks dan dictionary keys.
  2. Mengembalikan nilai `default` jika path tidak ada atau bertipe salah.
  3. Bebas dari loop tanpa akhir atau rekursi dalam tak terkendali.
- **Assertion**:
  - `assert extract_path({"a": [{"b": 42}]}, "a.0.b") == 42`
  - `assert extract_path({}, "a.0.b", default="empty") == "empty"`

---

## 3. Test Case C-03: SQL DDL Generator & Parser
- **Tantangan**: Menghasilkan DDL SQL ternormalisasi dari spesifikasi Pydantic/dataclass dengan deklarasi primary key, foreign key, dan index.
- **Kriteria Keberhasilan**:
  1. SQL sintaks valid untuk SQLite / PostgreSQL.
  2. Bebas dari kerentanan syntax injection.
