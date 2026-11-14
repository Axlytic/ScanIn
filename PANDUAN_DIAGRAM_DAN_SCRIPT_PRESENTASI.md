# BUKU PANDUAN PEMAHAMAN DIAGRAM UML & SKRIP PRESENTASI SISTEM SCANIN
**Mata Kuliah:** Integrasi Rekayasa Perangkat Lunak (RPL) & Interaksi Manusia dan Komputer (IMK)  
**Kelompok 4:**
1. M. Gehan Junior
2. Asnah
3. Muhammad Supian Sauri
4. Muhammad Wildan Anshari  

---

## DAFTAR ISI
1. [Ringkasan Eksekutif & Filosofi Sistem ScanIn](#1-ringkasan-eksekutif--filosofi-sistem-scanin)
2. [Bedah Komprehensif 4 Pemodelan UML](#2-bedah-komprehensif-4-pemodelan-uml)
   - [2.1 Use Case Diagram: Aktor & Batasan Sistem](#21-use-case-diagram-aktor--batasan-sistem)
   - [2.2 Activity Diagram: Alur Kerja & 4 Titik Validasi](#22-activity-diagram-alur-kerja--4-titik-validasi)
   - [2.3 Class Diagram: Struktur Domain Data & Relasi](#23-class-diagram-struktur-domain-data--relasi)
   - [2.4 Sequence Diagram: Kronologi Interaksi & Kinerja 1.4 Detik](#24-sequence-diagram-kronologi-interaksi--kinerja-14-detik)
3. [Matriks Konsistensi Antar-Diagram](#3-matriks-konsistensi-antar-diagram)
4. [Skrip Bacaan Presentasi Lengkap (Slide 1 s.d. 12)](#4-skrip-bacaan-presentasi-lengkap-slide-1-sd-12)
5. [Antisipasi Tanya Jawab Kritis Dosen (Defense Kit)](#5-antisipasi-tanya-jawab-kritis-dosen-defense-kit)

---

## 1. RINGKASAN EKSEKUTIF & FILOSOFI SISTEM SCANIN

### 1.1 Masalah Utama
Sistem presensi konvensional di perguruan tinggi (kertas paraf manual dan QR statis) memiliki kelemahan fatal:
1. **Inefisiensi Waktu:** Memakan waktu 10–15 menit di awal kuliah hanya untuk memanggil atau mengedarkan lembar presensi.
2. **Kecurangan Masif (Titip Absen):** Mahasiswa di luar kampus dapat menitipkan tanda tangan atau meminta tangkapan layar (*screenshot*) QR code yang diteruskan via grup chat (WhatsApp/Telegram).
3. **Keterbatasan Fasilitas:** Tidak semua ruang perkuliahan dilengkapi LCD proyektor yang siap pakai.

### 1.2 Tiga Pilar Solusi ScanIn
ScanIn dirancang dengan arsitektur web modern yang mengintegrasikan tiga lapis pengamanan:
1. **Dynamic QR Code (Rotasi TTL 10 Detik):** Token dienkripsi berbasis *timestamp* dan di-refresh secara otomatis setiap 10 detik via WebSocket. Tangkapan layar yang dikirim ke grup chat akan kedaluwarsa sebelum sempat dipindai.
2. **Geofencing GPS Spasial (Radius $\le 30$ Meter):** Lokasi mahasiswa dihitung terhadap koordinat GPS dosen pengampu menggunakan algoritma *Haversine*. Mahasiswa di luar kelas otomatis ditolak sistem.
3. **Dual-Mode Presensi (Fleksibilitas Ruang Kelas):**
   - *Mode Proyektor:* Ditayangkan di layar lebar untuk ruang kelas besar.
   - *Mode Mandiri (Layar HP Dosen):* QR ditampilkan langsung di layar ponsel dosen untuk kelas praktikum atau ruangan tanpa LCD proyektor.
4. **Single Active Session & Fallback:** Satu akun mahasiswa hanya boleh aktif di satu perangkat (*device fingerprint*), serta tersedia fitur *Presensi Manual oleh Dosen* jika terjadi kendala baterai/kuota pada mahasiswa.

---

## 2. BEDAH KOMPREHENSIF 4 PEMODELAN UML

### 2.1 USE CASE DIAGRAM: Aktor & Batasan Sistem

#### A. Aktor Sistem
1. **Mahasiswa:** Aktor primer yang melakukan login dan memindai Dynamic QR untuk mencatat kehadiran.
2. **Dosen Pengampu:** Aktor pengendali kelas yang membuka sesi, memilih mode tampilan, mengunci koordinat GPS, memantau rekap langsung, dan melakukan presensi manual (*override*).
3. **Admin BAAK / Jurusan:** Aktor manajerial yang mengelola master data dan mengekspor rekapitulasi kehadiran (format Excel).

#### B. Fitur Utama & Relasi `<<include>>`
- **Login Mahasiswa & Dosen:** Wajib melewati verifikasi *Single Active Session* agar satu akun tidak dapat digunakan bersamaan di perangkat lain.
- **Buka Sesi Kelas (`<<include>> Pilih Mode Presensi`):** Saat dosen membuka sesi presensi, sistem secara otomatis memaksa pemilihan mode tampilan (*Proyektor* atau *Layar Mandiri HP*) dan mengunci koordinat GPS dosen sebagai titik jangkar (*anchor point*).
- **Pindai Dynamic QR Presensi:**
  - `<<include>> Validasi Radius Spasial (<= 30m):` Memastikan mahasiswa berada di dalam kelas sebelum pemindaian disetujui.
  - `<<include>> Validasi Dynamic QR (TTL 10s):` Memverifikasi keabsahan token dinamis yang tidak boleh berusia lebih dari 10 detik.
- **Presensi Manual (Override):** Memfasilitasi mahasiswa yang memiliki kendala teknis (kamera rusak, kuota habis) agar tidak dirugikan secara akademis.

---

### 2.2 ACTIVITY DIAGRAM: Alur Kerja & 4 Titik Validasi

Activity Diagram memodelkan aliran aktivitas dari awal sesi dibuka hingga data kehadiran tercatat ke basis data, dibagi ke dalam **3 Swimlane Partisipan**:

#### A. Swimlane 1: Dosen Pengampu (Inisiasi Sesi)
1. Dosen menekan tombol *Buka Sesi Presensi*.
2. Browser dosen mengakses sensor GPS untuk mengunci koordinat kelas.
3. Dosen memilih mode tampilan (*Proyektor* atau *Layar Mandiri*).
4. Mesin generator QR mulai memancarkan token dinamis dengan rotasi tiap 10 detik.

#### B. Swimlane 2: Mahasiswa (Akses & Pemindaian)
1. Mahasiswa membuka Web App ScanIn di peramban ponsel.
2. Sistem secara otomatis meminta izin sensor GPS mahasiswa.
3. **[Titik Validasi 1 - Geofencing]:** Apakah jarak mahasiswa terhadap GPS dosen $\le 30$ meter?
   - *Jika Tidak:* Presensi langsung ditolak dengan pesan: *"Di Luar Jangkauan Kelas"*.
   - *Jika Ya:* Antarmuka kamera pemindai aktif.
4. Mahasiswa mengarahkan kamera ke layar Dynamic QR.
5. **[Titik Validasi 2 - Token Expiry]:** Apakah token QR masih berlaku ($\le 10$ detik)?
   - *Jika Tidak:* Presensi ditolak dengan pesan: *"Token Kedaluwarsa, Silakan Scan Ulang"*.
   - *Jika Ya:* Payload presensi terenkripsi dikirim ke server.

#### C. Swimlane 3: Server & Basis Data (Verifikasi Akhir)
1. **[Titik Validasi 3 - Single Active Session]:** Apakah akun mahasiswa terdeteksi login di perangkat lain? Jika ya, ditolak.
2. **[Titik Validasi 4 - Integritas Database]:** Server mencatat *timestamp*, *device fingerprint*, dan status `HADIR` ke tabel `log_presensi`.
3. Layar ponsel mahasiswa menampilkan centang hijau sukses hadir.
4. Dashboard dosen secara otomatis memperbarui (*live update*) angka persentase kehadiran mahasiswa secara *real-time*.

---

### 2.3 CLASS DIAGRAM: Struktur Domain Data & Relasi

Class Diagram disusun berdasarkan arsitektur **Boundary-Control-Entity (BCE)** untuk memastikan pemisahan tanggung jawab yang modular dan *maintainable*.

#### A. Rincian Kelas
1. **User (Induk Abstract):**
   - Atribut: `idUser`, `nimNip`, `passwordHash`, `activeSessionId`, `lastDeviceId`, `lastLogoutAt`.
   - Operasi: `login()`, `logout()`, `verifySession()`.
2. **Mahasiswa (Spesialisasi / Inheritance dari User):**
   - Atribut Tambahan: `prodi`, `semester`.
   - Operasi: `scanQRProyektor()`, `scanQRMandiri()`, `lihatRiwayatPresensi()`.
3. **Dosen (Spesialisasi / Inheritance dari User):**
   - Atribut Tambahan: `nidn`, `fakultas`.
   - Operasi: `bukaSesiPresensi()`, `tutupSesi()`, `presensiManual()`, `pantauDashboard()`.
4. **SesiPresensi (Entitas Sesi):**
   - Atribut: `idSesi`, `kodeKelas`, `latDosen`, `longDosen`, `modePresensi`, `currentToken`, `tokenTTL (10s)`.
   - Operasi: `generateNextToken()`, `validasiRadius(latMhs, longMhs)`.
5. **LogPresensi (Entitas Transaksi):**
   - Atribut: `idLog`, `waktuPresensi`, `statusKehadiran`, `jarakMeters`, `deviceFingerprint`.
   - Operasi: `simpanLog()`, `verifikasiIntegritas()`.

#### B. Hubungan Antar-Kelas (Kardinalitas)
- **Inheritance:** `Mahasiswa` dan `Dosen` mewarisi seluruh kapabilitas autentikasi dari kelas induk `User`.
- **Asosiasi (1 ke 0..*):** 1 `Dosen` dapat membuka banyak `SesiPresensi`.
- **Komposisi (1 ke 0..* - Diamond Hitam ◆):** 1 `SesiPresensi` memiliki banyak `LogPresensi`. Jika sesi perkuliahan dihapus, maka seluruh log transaksi presensi pada sesi tersebut ikut terhapus (*strong lifecycle dependency*).
- **Asosiasi (1 ke 0..*):** 1 `Mahasiswa` memiliki banyak catatan di `LogPresensi`.

---

### 2.4 SEQUENCE DIAGRAM: Kronologi Interaksi & Kinerja 1.4 Detik

Sequence diagram memvisualisasikan interaksi pesan antar-objek secara horizontal dalam tiga tahapan pengamanan dan 15 aliran pesan yang tuntas dalam **1.4 detik**.

#### A. Aktor & Lifeline
1. `Mahasiswa` (Aktor Pengguna Mandiri)
2. `Web Mahasiswa (Klien)` (Boundary / Client UI)
3. `Server ScanIn (API)` (Control / Backend API)
4. `Basis Data MySQL` (Entity / Database Storage)
5. `Dosen (Proyektor)` (Aktor Penerima Siaran Live WebSocket)

#### B. Kronologi 15 Aliran Pesan Terurut
* **Inisiasi Sesi:** Dosen membuka kelas, mengunci titik koordinat GPS kelas, dan Dynamic QR mulai berotasi via proyektor (TTL 10s).
* **Tahap 1: Validasi Radius Spasial Geofencing (<= 30 Meter)**
  - **Pesan 1:** Mahasiswa mengklik menu presensi kelas di peramban ponsel.
  - **Pesan 2:** Web Mahasiswa membaca sensor GPS internal (`latitude`, `longitude`, `accuracy`).
  - **Pesan 3:** Web Mahasiswa mengirimkan koordinat via HTTP POST `/api/validate-location`.
  - **Pesan 4:** Server ScanIn menghitung jarak menggunakan formula Haversine terhadap GPS Dosen.
  - **Percabangan ALT:**
    - *Cabang Gagal (Jarak > 30m / Mock GPS):* **Pesan 5a:** Server melempar HTTP 403 penolakan kilat (**0.3 detik**) &rarr; **Pesan 6a:** Web menampilkan layar merah *Akses Ditolak*.
    - *Cabang Lolos (Jarak <= 30m):* **Pesan 5b:** Server mengembalikan HTTP 200 koordinat sah &rarr; **Pesan 6b:** Web mengaktifkan kamera pemindai di browser (< 1 detik).
* **Tahap 2: Pemindaian Dynamic QR & Verifikasi Keamanan Server**
  - **Pesan 7:** Mahasiswa membidik kamera ke layar proyektor kelas.
  - **Pesan 8:** Web mengirimkan payload token + NIM + DeviceID via HTTP POST `/api/submit-presence`.
  - **Pesan 9:** Server ScanIn mendekripsi token dan memvalidasi usia token (&le; 10 detik).
  - **Pesan 10:** Server memvalidasi token JWT dan device fingerprint untuk memastikan *Single Active Session*.
* **Tahap 3: Persistensi Basis Data & Penyiaran Real-Time (Total 1.4 Detik)**
  - **Pesan 11:** Server mengeksekusi perintah SQL `INSERT INTO log_presensi VALUES (nim, id_sesi, 'HADIR', NOW())`.
  - **Pesan 12:** Basis Data MySQL mengonfirmasi transaksi berhasil (*Commit Success* dalam waktu 0.1s).
  - **Pesan 13:** Server mengembalikan respons HTTP 200 OK ke Web Mahasiswa.
  - **Pesan 14:** Antarmuka ponsel menampilkan animasi centang hijau *Kehadiran Berhasil Tercatat*.
  - **Pesan 15:** Server secara instan menembakkan sinyal *Broadcast Live WebSocket* ke laptop dosen sehingga nama mahasiswa langsung bertambah di daftar hadir proyektor kelas tanpa refresh halaman.

---

## 3. MATRIKS KONSISTENSI ANTAR-DIAGRAM

| Fitur / Parameter | Use Case Diagram | Activity Diagram | Class Diagram | Sequence Diagram |
|:---|:---|:---|:---|:---|
| **Dynamic QR (TTL 10 Detik)** | Masuk sebagai relasi `<<include>>` pada use case scan. | Diuji pada *Titik Validasi 2* (evaluasi usia token). | Didefinisikan pada atribut `currentToken` & `tokenTTL` di kelas `SesiPresensi`. | Divalidasi pada *Pesan 6* oleh Server ScanIn. |
| **Geofencing Spasial ($\le 30\text{m}$)** | Masuk sebagai relasi `<<include>>` validasi radius. | Diuji pada *Titik Validasi 1* sebelum kamera dibuka. | Dihitung melalui method `validasiRadius()` di kelas `SesiPresensi`. | Dievaluasi pada *Pesan 2 & 3* sebelum izin scan diberikan. |
| **Dual-Mode Presensi** | Ditentukan dosen pada saat membuka sesi kelas. | Dosen memilih cabang *Mode Proyektor* atau *Mode Mandiri*. | Disimpan pada atribut `modePresensi` di kelas `SesiPresensi`. | Menentukan target penayangan QR (*Note over D, Srv*). |
| **Single Active Session** | Melindungi titik masuk use case login. | Diuji pada *Titik Validasi 3* di server. | Divalidasi via atribut `activeSessionId` di kelas `User`. | Diverifikasi bersamaan dengan validasi token presensi. |
| **Presensi Manual** | Use Case alternatif khusus untuk Dosen Pengampu. | Cabang jalur darurat jika mahasiswa kendala teknis. | Method `presensiManual()` di kelas `Dosen`. | Operasi *override* langsung ke database oleh dosen. |

---

## 4. SKRIP BACAAN PRESENTASI LENGKAP (SLIDE 1 s.d. 12)

Gunakan naskah berikut saat presentasi di depan dosen penguji. Naskah ini dirancang dengan intonasi percaya diri, bahasa akademis yang lugas, dan arahan pointer visual ke layar slide.

---

### SLIDE 1: COVER PRESENTASI
* **Estimasi Waktu:** 30 Detik  
* **Fokus Layar:** Tunjukkan judul ScanIn dan nama Kelompok 4.  
* **Skrip Pembicara:**  
> *"Assalamu’alaikum Warahmatullahi Wabarakatuh. Selamat pagi/siang kepada Bapak/Ibu Dosen pengampu dan rekan-rekan sekalian.  
> Kami dari **Kelompok 4** yang beranggotakan M. Gehan Junior, Asnah, Muhammad Supian Sauri, dan Muhammad Wildan Anshari.  
> Pada kesempatan kali ini, kami akan mempresentasikan hasil analisis dan pemodelan perangkat lunak untuk sistem **ScanIn: Sistem Presensi Mahasiswa Berbasis Dynamic QR Code dan Geofencing Spasial**.  
> Sistem ini kami rancang untuk memecahkan problematika klasik presensi perkuliahan dengan mengedepankan efisiensi waktu, kejujuran data, dan fleksibilitas fasilitas ruang kelas. Mari kita masuk ke latar belakang permasalahan."*

---

### SLIDE 2 & 3: LATAR BELAKANG, MASALAH, & SOLUSI
* **Estimasi Waktu:** 1 Menit  
* **Fokus Layar:** Tunjukkan kontras antara metode lama (kertas/QR statis) dengan ScanIn.  
* **Skrip Pembicara:**  
> *"Bapak/Ibu Dosen, selama ini kita sering menyaksikan proses presensi menggunakan kertas paraf keliling yang memakan waktu 10 hingga 15 menit, mengganggu konsentrasi belajar, dan sangat rentan praktik titip absen. Beberapa kampus mulai beralih menggunakan QR Code, namun sayangnya QR Code yang digunakan mayoritas masih berkarakter statis. Akibatnya, mahasiswa di kelas cukup memfoto QR tersebut dan membagikannya ke grup WhatsApp, sehingga mahasiswa yang masih berada di kos atau di luar kampus tetap bisa melakukan presensi.  
> Masalah ketiga adalah heterogenitas fasilitas kampus: tidak semua ruang kuliah memiliki proyektor LCD yang siap digunakan setiap saat.  
> Dari permasalahan ini, **ScanIn** hadir membawa tiga pilar solusi utama:  
> Pertama, **Dynamic QR Code dengan rotasi tiap 10 detik**.  
> Kedua, **Geofencing GPS dengan radius presisi maksimal 30 meter**.  
> Dan ketiga, **Fitur Dual-Mode**, yang memungkinkan presensi berjalan baik di kelas berproyektor maupun ruang praktikum tanpa proyektor. Sekarang mari kita telaah bagaimana sistem ini dimodelkan secara terstruktur."*

---

### SLIDE 4 s.d. 6: USE CASE DIAGRAM (Slide 7 di Canva)
* **Estimasi Waktu:** 1.5 Menit  
* **Fokus Layar:** Arahkan pointer ke 3 kolom: Aktor (Kiri), Fitur Utama (Tengah), Aturan Validasi (Kanan).  
* **Skrip Pembicara:**  
> *"Bapak/Ibu Dosen, pada slide ini kami menampilkan **Use Case Diagram** dari ScanIn.  
> Diagram ini kami bagi secara horizontal ke dalam tiga kluster utama untuk memudahkan pembacaan:  
> Di sebelah kiri, terdapat **tiga Aktor**: Mahasiswa, Dosen Pengampu, dan Admin BAAK.  
> Di kolom tengah, terdapat **Use Case Fitur Utama**. Perhatikan bahwa use case nomor 1, yaitu Login, dibentengi oleh aturan *Single Active Session*. Artinya, mahasiswa tidak dapat meminjamkan akunnya kepada orang lain karena satu akun terikat pada satu perangkat aktif.  
> Ketika Dosen membuka sesi perkuliahan pada use case nomor 2, sistem secara otomatis mengeksekusi relasi **<<include>>** menuju aturan pemilihan mode: apakah menggunakan proyektor kelas atau layar mandiri HP dosen.  
> Sementara itu, ketika mahasiswa memindai QR pada use case nomor 3, terdapat dua relasi **<<include>>** mutlak yang harus dipenuhi: sistem wajib memvalidasi radius spasial $\le 30$ meter dan memvalidasi keaslian token dinamis berumur 10 detik.  
> Dosen juga dibekali Use Case nomor 4, yaitu **Presensi Manual**, sebagai jaring pengaman darurat jika ada mahasiswa yang kehabisan daya baterai atau paket data di kelas."*

---

### SLIDE 7 & 8: ACTIVITY DIAGRAM (Slide 8 di Canva)
* **Estimasi Waktu:** 1.5 Menit  
* **Fokus Layar:** Tunjukkan aliran 3 Swimlane (Dosen $\rightarrow$ Mahasiswa $\rightarrow$ Server). Tunjukkan 4 titik belah ketupat keputusan (*decision diamond*).  
* **Skrip Pembicara:**  
> *"Beralih ke **Activity Diagram**, di sini kami memodelkan alur kerja sistem secara horizontal yang terbagi ke dalam **tiga swimlane**: Dosen, Mahasiswa, dan Server.  
> Alur diawali dari swimlane Dosen yang membuka sesi kuliah dan mengunci koordinat GPS ruang kelas sebagai titik jangkar. Dosen memilih mode tampilan, lalu sistem mulai merotasikan QR Code setiap 10 detik.  
> Selanjutnya, perhatikan swimlane Mahasiswa. Ketika mahasiswa membuka aplikasi web ScanIn, sistem langsung melakukan **Titik Validasi Pertama**, yaitu mengecek radius GPS mahasiswa. Jika mahasiswa berada di luar radius 30 meter, sistem langsung menolak dan proses terhenti.  
> Jika lolos, kamera aktif dan mahasiswa memindai QR Code. Di sinilah terjadi **Titik Validasi Kedua**: sistem mengecek apakah token QR masih berusia di bawah 10 detik. Jika token kedaluwarsa, mahasiswa diminta scan ulang.  
> Terakhir, data dikirim ke swimlane Server untuk melewati **Titik Validasi Ketiga**, yaitu pengecekan *Single Active Session*. Jika tidak ada login ganda, server langsung menyimpan status HADIR ke database.  
> Tampilan HP mahasiswa langsung memunculkan centang hijau, dan secara bersamaan dashboard dosen ter-update secara real-time. Alur ini menjamin tidak ada celah titip absen yang lolos."*

---

### SLIDE 9: CLASS DIAGRAM (Slide 9 di Canva)
* **Estimasi Waktu:** 1.5 Menit  
* **Fokus Layar:** Tunjukkan relasi Inheritance User ke Mahasiswa/Dosen, lalu Komposisi ke Sesi dan Log.  
* **Skrip Pembicara:**  
> *"Slide berikutnya menyajikan **Class Diagram** yang kami rancang menggunakan pola arsitektur **Boundary-Control-Entity (BCE)**.  
> Pada kolom pertama, kami memiliki kelas induk abstract bernama **User** yang menyimpan atribut autentikasi dasar seperti `idUser`, `nimNip`, dan `activeSessionId`.  
> Melalui konsep *Inheritance* atau pewarisan, kelas User diturunkan menjadi dua spesialisasi: kelas **Mahasiswa** yang memiliki atribut program studi dan operasi pemindaian QR, serta kelas **Dosen** yang memiliki NIDN dan wewenang untuk membuka sesi serta melakukan presensi manual.  
> Relasi kunci yang ingin kami tekankan ada pada hubungan antara kelas **Dosen** dengan kelas **SesiPresensi**, di mana satu dosen dapat membuka banyak sesi kelas.  
> Di dalam kelas `SesiPresensi`, tersimpan atribut penting seperti koordinat lintang-bujur dosen, mode presensi yang dipilih, serta algoritma `validasiRadius()`.  
> Perhatikan simbol belah ketupat hitam antara `SesiPresensi` dan `LogPresensi`. Ini melambangkan relasi **Komposisi murni**. Artinya, keberadaan data catatan kehadiran diikat secara erat pada sesi kuliah yang aktif. Jika sesi kuliah dihapus, seluruh log presensi di dalamnya ikut terhapus secara berurutan (*cascading delete*). Ini menjamin konsistensi integritas basis data kami."*

---

### SLIDE 10: SEQUENCE DIAGRAM & KINERJA SISTEM (Slide 10 di Canva)
* **Estimasi Waktu:** 1.5 Menit  
* **Fokus Layar:** Tunjukkan diagram widescreen teks putih di atas latar navy / dark blue. Tunjukkan alur total 1.4 detik.  
* **Skrip Pembicara (Pembedahan Komponen demi Komponen):**  
> *"Bapak dan Ibu Dosen, mari kita bedah visual **Sequence Diagram** di layar yang mendokumentasikan interaksi 15 pesan antar-komponen serta membuktikan tolok ukur kinerja sistem yang tuntas hanya dalam **1.4 detik**.  
> Di bagian paling atas terdapat **lima garis hidup (*lifelines*)**: Mahasiswa, Web Klien di peramban, Server API ScanIn, Basis Data MySQL, dan Layar Proyektor Dosen. Garis putus-putus ke bawah menandakan linimasa waktu, sedangkan kotak tebal menandakan durasi aktif pemrosesan.  
> Sesi kuliah diawali saat Dosen mengunci titik GPS kelas dan sistem langsung merotasikan Dynamic QR dengan masa aktif 10 detik ke proyektor.  
> Masuk ke **Tahap 1 (Blok Biru Muda - Validasi Geofencing Spasial)**: Pada Pesan 1 dan 2, peramban membaca sensor GPS internal dan mengirim koordinat ke server via Pesan 3. Server menghitung formula Haversine pada Pesan 4.  
> Perhatikan kotak percabangan **alt**: jika mahasiswa berada di luar radius 30 meter atau terdeteksi Mock/Fake GPS, server langsung melontarkan HTTP 403 penolakan kilat pada Pesan 5a dalam waktu hanya **0.3 detik**.  
> Namun jika berada di dalam radius, pada Pesan 5b dan 6b peramban langsung mengaktifkan kamera pemindai dalam waktu di bawah 1 detik.  
> Selanjutnya pada **Tahap 2 (Blok Kuning - Verifikasi Keamanan Server)**: Mahasiswa membidik layar pada Pesan 7, dan payload token dikirim pada Pesan 8. Di internal server, Pesan 9 dan 10 memverifikasi bahwa token tidak kedaluwarsa (&le; 10 detik) dan akun mahasiswa tidak dipakai ganda melalui validasi Single Active Session.  
> Puncaknya pada **Tahap 3 (Blok Hijau - Persistensi & WebSocket)**: tepat pada detik ke-1.1, server mengeksekusi INSERT ke MySQL pada Pesan 11 dan menerima konfirmasi commit pada Pesan 12.  
> Pada Pesan 13 dan 14, mahasiswa menerima HTTP 200 dengan animasi centang hijau. Dan tepat di Pesan 15, server memancarkan sinyal **live WebSocket broadcast** ke laptop dosen sehingga nama mahasiswa langsung muncul di proyektor kelas secara real-time tanpa me-refresh halaman.  
> Seluruh siklus kronologis ini membuktikan kinerja arsitektur ScanIn yang sangat cepat, aman, dan tanpa latensi."*

---

### SLIDE 11: MATRIKS KONSISTENSI & KESIMPULAN
* **Estimasi Waktu:** 1 Menit  
* **Fokus Layar:** Tunjukkan 3 pilar konsistensi: Keamanan, Integritas Peran, dan Fleksibilitas.  
* **Skrip Pembicara:**  
> *"Sebagai rangkuman keterpaduan pemodelan, Slide 11 ini menyajikan **Matriks Konsistensi 4 Diagram UML**.  
> Kami memastikan tidak ada diskoneksi logika di antara diagram yang kami buat:  
> Parameter keamanan *Dynamic QR 10 Detik* dan *Radius GPS 30 Meter* yang kami canangkan di Use Case Diagram, diuji alur logikanya di Activity Diagram, dimodelkan struktur datanya pada Class Diagram, dan dieksekusi secara instan pada Sequence Diagram.  
> Pembagian peran pengguna juga konsisten sejak login hingga pencatatan transaksi di database.  
> Dan fleksibilitas Dual-Mode memastikan sistem ini dapat diimplementasikan secara realistis di seluruh ruang kelas kampus kita.  
> Dengan pemodelan UML yang solid ini, tim pengembang memiliki acuan cetak biru yang presisi untuk melanjutkan ke tahap pengkodean dan pengujian."*

---

### SLIDE 12: PENUTUP & PEMBUKAAN TANYA JAWAB
* **Estimasi Waktu:** 30 Detik  
* **Fokus Layar:** Slide Thank You. Tatap mata dosen penguji secara santai dan terbuka.  
* **Skrip Pembicara:**  
> *"Demikian presentasi dari Kelompok 4 mengenai Pemodelan UML Sistem ScanIn. Kami meyakini sistem ini dapat memberikan kontribusi nyata bagi efisiensi dan integritas akademik di lingkungan perkuliahan.  
> Selanjutnya, kami membuka ruang seluas-luasnya untuk sesi diskusi, tanya jawab, kritik, serta masukan yang membangun dari Bapak/Ibu Dosen penguji dan rekan-rekan sekalian.  
> Terima kasih atas perhatiannya. Wassalamu’alaikum Warahmatullahi Wabarakatuh."*

---

## 5. ANTISIPASI TANYA JAWAB KRITIS DOSEN (DEFENSE KIT)

Berikut adalah jawaban akademis jika dosen menguji pemahaman teknis tim Anda:

### Pertanyaan 1: *"Bagaimana jika mahasiswa memfoto layar QR lalu mengirimkannya via WhatsApp ke temannya di luar kampus?"*
* **Jawaban:**  
> *"Pertanyaan yang sangat bagus, Bapak/Ibu. Skenario tersebut telah kami mitigasi melalui dua lapis pengamanan independen (*Two-Factor Verification*).  
> Pertama, QR Code di-generate dinamis menggunakan enkripsi timestamp dengan masa kedaluwarsa (TTL) hanya 10 detik. Waktu 10 detik tersebut secara teknis tidak cukup untuk memfoto, mengunggah ke WhatsApp, diunduh oleh teman, dan dipindai di ponsel lain.  
> Kedua dan yang paling utama, sistem kami memiliki lapisan Geofencing GPS. Sekalipun token berhasil dikirim, ponsel teman yang berada di luar radius 30 meter dari GPS dosen akan langsung ditolak pada tahap pembukaan kamera sebelum pemindaian sempat terjadi."*

### Pertanyaan 2: *"Bagaimana jika mahasiswa menggunakan aplikasi Fake GPS / Mock Location?"*
* **Jawaban:**  
> *"Di sisi klien peramban (Web API Geolocation), HTML5 Geolocation menyediakan atribut `isMockLocation` dan `accuracy` dalam satuan meter. Pada backend ScanIn, kami menerapkan filter: jika `isMock` bernilai true, atau nilai akurasi GPS terlalu rendah/tidak konsisten (> 20 meter), server akan menolak akses dan meminta mahasiswa melakukan kalibrasi sensor GPS fisik."*

### Pertanyaan 3: *"Mengapa memilih pola Boundary-Control-Entity (BCE) pada Class Diagram?"*
* **Jawaban:**  
> *"Pola BCE kami terapkan untuk mematuhi prinsip Single Responsibility Principle. Kelas Boundary mengurus antarmuka pengguna, kelas Control memproses aturan bisnis presensi, dan kelas Entity menangani persistensi data. Manfaat utamanya adalah keterpisahan logika: jika di masa mendatang kampus ingin mengubah tampilan UI atau beralih dari aplikasi Web ke aplikasi Mobile Flutter, logika keamanan (Control) dan skema database (Entity) tidak perlu dirombak ulang."*

### Pertanyaan 4: *"Bagaimana jika ruang kelas tidak memiliki proyektor, atau proyektornya rusak?"*
* **Jawaban:**  
> *"Inilah keunggulan fitur Dual-Mode pada ScanIn. Jika ruang kelas tidak memiliki proyektor, dosen cukup memilih 'Mode Mandiri'. Sistem akan memancarkan Dynamic QR langsung pada layar smartphone atau laptop pribadi dosen. Mahasiswa dapat bergantian memindai QR di meja dosen. Jika ada mahasiswa yang smartphone-nya kehabisan baterai, dosen dapat mengeksekusi use case Presensi Manual secara instan."*

### Pertanyaan 5: *"Mengapa relasi antara SesiPresensi dan LogPresensi adalah Komposisi, bukan Agregasi?"*
* **Jawaban:**  
> *"Karena LogPresensi memiliki ketergantungan hidup yang mutlak (*strong lifecycle dependency*) terhadap SesiPresensi. Suatu transaksi presensi tidak memiliki makna logis jika sesi perkuliahan induknya tidak pernah ada. Secara implementasi database, jika sebuah sesi perkuliahan dihapus, seluruh data log presensi pada sesi tersebut harus ikut terhapus (*ON DELETE CASCADE*) demi menjaga integritas relasional basis data."*

---
*Dokumen ini disusun sebagai panduan resmi dan bahan ujian Kelompok 4 untuk mata kuliah RPL & IMK.*

  