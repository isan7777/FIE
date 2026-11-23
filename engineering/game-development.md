# Engineering Playbook: Game Development & Real-Time Systems

## 1. Arsitektur Game & Sistem Real-Time
Pengembangan game menuntut manajemen alur frame deterministik, penggunaan memori terkendali, dan pemisahan logika simulasi dari render grafik.

## 2. Pola Arsitektur Inti Game
- **Game Loop Deterministik**:
  - `ProcessInput()` -> `UpdatePhysics(fixedDeltaTime)` -> `UpdateGameLogic(deltaTime)` -> `Render()`.
  - Pisahkan physics tick dari rendering tick untuk mencegah simulasi fluktuatif pada frame rate berbeda.
- **Entity Component System (ECS)** vs **Component-Based Pattern**:
  - Untuk entitas berskala ribuan: gunakan arsitektur data-oriented (ECS) untuk memaksimalkan cache CPU.
  - Untuk game skala menengah: gunakan hierarki Game Object / Component dengan komposisi terisolasi.
- **State Machine (FSM)**:
  - Kelola status karakter (Idle, Run, Jump, Attack, Dead) melalui Finite State Machine atau Hierarchical State Machine untuk mencegah konflik transisi animasi.

## 3. Manajemen Alokasi Memori & Garbage Collection
- Hindari instansiasi objek dinamis (`new`) berulang kali di dalam loop per frame (`Update()`).
- Terapkan **Object Pooling** untuk peluru, partikel, musuh, dan efek audio yang sering muncul dan hancur.
- Periksa konsumsi tekstur dan model 3D untuk menjaga batas memori VRAM target platform (Mobile vs Desktop).
