# 📱 ScanIn - Smart Presence System

> **ScanIn** adalah sistem presensi perkuliahan mandiri berbasis web adaptif (*Mobile-First*) yang mengintegrasikan **Dynamic QR Code (Rotasi 10 Detik)**, **Validasi Geofencing Spasial (Formula Haversine, Radius ≤ 30 Meter)**, dan **Single Active Session (JWT Revocation)** untuk menghadirkan proses presensi kelas yang instan (< 2 detik), bebas antrean, dan kebal dari praktik titip absen (calo kehadiran).

---

## 👥 Identitas Tim Pengembang (Kelompok 4)

* **Program Studi:** S1 Teknologi Informasi
* **Institusi:** Universitas Islam Negeri (UIN) Antasari Banjarmasin
* **Tahun Akademik:** 2026/2027

| No | Nama Anggota | NIM | Peran Utama |
| :-: | :--- | :---: | :--- |
| 1 | **M. Gehan Junior** | 250104040186 | Project Lead & System Architecture |
| 2 | **Asnah** | 250104040137 | UI/UX Researcher & Documentation |
| 3 | **Muhammad Supian Sauri** | 250104040196 | Frontend & Interaction Design |
| 4 | **Muhammad Wildan Anshari** | 250104040170 | Software Engineering & QA |

---

## 🛡️ Tiga Pilar Pertahanan Anti-Kecurangan (*Zero-Trust Presence*)

```
┌────────────────────────────────────────────────────────────────────────┐
│                   3 LAPIS PERTAHANAN UTAMA SCANIN                      │
│                                                                        │
│   [ 1. SIAPA ANDA ]            [ 2. DI MANA ANDA ]      [ 3. KAPAN ]   │
│   Single Active Session         Geofencing GPS           Dynamic QR    │
│   (JWT Revocation)              (Radius <= 30 Meter)     (TTL 10s)     │
│   Cegah Bagi Akun ke Teman      Cegah Absen dari Kos     Cegah Foto WA │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Single Active Session & Device Cooldown (Anti-Joki Akun):**
   * Satu NIM hanya dapat aktif pada **satu perangkat fisik**. Jika akun login di perangkat lain, sesi lama otomatis terputus (*force logout*).
   * Diterapkan **Device Cooldown 30 menit** pasca-logout untuk mematikan celah satu ponsel dipakai bergantian mengabsenkan rekan sekelas.
2. **Validasi Geofencing Spasial (Anti-Absen Kos):**
   * Dosen mengunci titik koordinat bumi saat membuka sesi kelas.
   * Mahasiswa wajib berada di dalam **radius maksimal 30 meter** dari dosen (dihitung menggunakan Formula Haversine).
   * Dilengkapi deteksi **Anti-Mock GPS** untuk menyaring koordinat palsu / anomali.
3. **Dynamic QR Code Rotasi Cepat (Anti-Tangkapan Layar):**
   * Kode QR diperbarui otomatis setiap **10 detik**. Tangkapan layar yang dikirimkan via WhatsApp akan kedaluwarsa sebelum sempat dipindai.

---

## 🔄 Solusi Fleksibilitas Lapangan (*Dual-Mode Presence*)

| Mode Presensi | Kondisi Ruang Kelas | Cara Kerja Sistem |
| :--- | :--- | :--- |
| **Mode A: Proyektor (Utama)** | Kelas memiliki fasilitas proyektor aktif. | Dosen menampilkan Dynamic QR di layar proyektor $\rightarrow$ Mahasiswa membidikkan kamera ponsel langsung ke depan kelas. |
| **Mode B: Layar Mandiri (*Fallback*)** | Proyektor rusak, mati lampu, atau kelas tanpa proyektor. | Dosen mengaktifkan mode mandiri $\rightarrow$ Mahasiswa memproses kode dinamis langsung di layar ponselnya via RAM Canvas (*In-Memory Processing*). |
| **Presensi Manual (*Override*)** | Kamera HP mahasiswa pecah, baterai habis, dsb. | Dosen menandai kehadiran secara manual melalui dasbor admin setelah verifikasi fisik di kelas. |

---

## 📊 Pemodelan UML (Rekayasa Perangkat Lunak)

Sistem dimodelkan menggunakan empat diagram utama:
1. **Use Case Diagram:** Menggambarkan batasan sistem (*system boundary*), aktor primer (Mahasiswa, Dosen), aktor pendukung (Admin), serta relasi `<<include>>` validasi token dan geofencing.
2. **Activity Diagram:** Memetakan alur kerja terpisah (*swimlane*) antara aktivitas fisik mahasiswa, dosen, dan validasi 4 lapis pada backend server.
3. **Class Diagram:** Struktur relasi data domain (`User`, `Mahasiswa`, `Dosen`, `SesiPresensi`, `LogPresensi`) berpola arsitektur Boundary-Control-Entity (BCE).
4. **Sequence Diagram:** Rangkaian eksekusi pesan real-time dari pemindaian kamera hingga commit basis data dan broadcast WebSocket ke layar dosen (< 2 detik).

---

## 📂 Struktur Berkas Proyek

* `workbook.docx`: Dokumen lengkap *UI/UX Workbook* (Bab I Strategy Plane s.d. Bab VII Kesimpulan).
* `logo ScanIn.PNG`: Identitas visual dan logo aplikasi ScanIn.
* `slides_canva/`: Aset visual dan bahan presentasi pemodelan sistem.
* `Presentasi_Evaluasi_Usability_SIAKAD_UIN_Antasari.pptx`: Dokumentasi evaluasi heuristik dan usability awal.

