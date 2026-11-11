# PANDUAN PEMAHAMAN DIAGRAM UML & NASKAH PRESENTASI SCANIN
**Mata Kuliah:** Rekayasa Perangkat Lunak (RPL) & Interaksi Manusia dan Komputer (IMK)  
**Kelompok 4:**  
1. M. Gehan Junior  
2. Asnah  
3. Muhammad Supian Sauri  
4. Muhammad Wildan Anshari  

---

## DAFTAR ISI
1. [BAGIAN I: BEDAH TEKNIS DAN PEMAHAMAN 4 DIAGRAM UML](#bagian-i-bedah-teknis-dan-pemahaman-4-diagram-uml)
   - [1. Use Case Diagram: Batasan Sistem & Otorisasi](#1-use-case-diagram-batasan-sistem--otorisasi)
   - [2. Activity Diagram: Logika Alur Bisnis & 4 Titik Validasi](#2-activity-diagram-logika-alur-bisnis--4-titik-validasi)
   - [3. Class Diagram: Struktur Domain Data & Relasi BCE](#3-class-diagram-struktur-domain-data--relasi-bce)
   - [4. Sequence Diagram: Interaksi Objek & Pembuktian Kinerja N1](#4-sequence-diagram-interaksi-objek--pembuktian-kinerja-n1)
   - [5. Matriks Konsistensi Antar-Diagram](#5-matriks-konsistensi-antar-diagram)
2. [BAGIAN II: NASKAH LENGKAP BACAAN PRESENTASI (WORD-FOR-WORD SCRIPT)](#bagian-ii-naskah-lengkap-bacaan-presentasi-word-for-word-script)
   - [Slide 1: Pembuka & Identitas Tim](#slide-1-pembuka--identitas-tim)
   - [Slide 2: Latar Belakang Masalah Presensi](#slide-2-latar-belakang-masalah-presensi)
   - [Slide 3: Solusi Aplikasi ScanIn](#slide-3-solusi-aplikasi-scanin)
   - [Slide 4–5: Use Case Diagram & Batasan Fungsional](#slide-45-use-case-diagram--batasan-fungsional)
   - [Slide 6–7: Activity Diagram & 4 Gerbang Validasi](#slide-67-activity-diagram--4-gerbang-validasi)
   - [Slide 8–9: Class Diagram & Struktur Relasi Objek](#slide-89-class-diagram--struktur-relasi-objek)
   - [Slide 10: Sequence Diagram & Pengujian Kinerja 1.4 Detik](#slide-10-sequence-diagram--pengujian-kinerja-14-detik)
   - [Slide 11: Matriks Konsistensi Arsitektur](#slide-11-matriks-konsistensi-arsitektur)
   - [Slide 12: Penutup & Membuka Sesi Tanya Jawab](#slide-12-penutup--membuka-sesi-tanya-jawab)
3. [BAGIAN III: BANK JAWABAN TANYA JAWAB DOSEN (KILLER DEFENSE Q&A)](#bagian-iii-bank-jawaban-tanya-jawab-dosen-killer-defense-qa)

---

# BAGIAN I: BEDAH TEKNIS DAN PEMAHAMAN 4 DIAGRAM UML

### 1. Use Case Diagram: Batasan Sistem & Otorisasi
* **Fungsi Utama:** Mendefinisikan ruang lingkup (*system boundary*) dan interaksi pengguna eksternal terhadap layanan inti ScanIn.
* **Elemen Teknis:**
  * **System Boundary (`Sistem Presensi ScanIn`):** Kotak pembatas yang memisahkan apa yang dikerjakan oleh sistem dan apa yang berada di luar sistem (aktor).
  * **Aktor Primer Mahasiswa:** Menginisiasi transaksi presensi (`Pindai Dynamic QR`) dan melihat riwayat kehadiran pribadi. Mahasiswa tidak diberi hak membuka sesi kelas maupun mengubah status kehadiran.
  * **Aktor Primer Dosen:** Pemegang kendali kelas. Membuka sesi perkuliahan, memilih mode tampilan (Proyektor vs HP Mandiri), melakukan presensi manual (*override* saat mahasiswa terkendala perangkat), dan memantau rekap.
  * **Aktor Sekunder Admin BAAK:** Mengelola akun sistem dan mengekspor rekapitulasi ke format Excel.
  * **Relasi `<<include>>` (Ketergantungan Wajib):**
    * Use Case *Pindai QR Presensi* secara otomatis mewajibkan (*include*) eksekusi dua validasi keamanan:
      1. `Validasi Geofencing Spasial (Radius <= 30m)`
      2. `Validasi Dynamic QR (Rotasi TTL 10 Detik)`
    * Artinya: Tidak ada presensi yang dapat dicatat tanpa melalui kedua validasi ini.

---

### 2. Activity Diagram: Logika Alur Bisnis & 4 Titik Validasi
* **Fungsi Utama:** Menggambarkan aliran proses bisnis dan percabangan keputusan (*decision nodes*) dari saat dosen memulai kelas hingga mahasiswa tercatat hadir.
* **Elemen Teknis:**
  * **Pemisahan Swimlane (3 Kolom Horisontal):**
    1. *Swimlane Dosen:* Mengunci koordinat GPS ruang kelas, memilih mode (Proyektor atau Layar Mandiri), dan memicu penayangan Dynamic QR yang berotasi otomatis tiap 10 detik.
    2. *Swimlane Mahasiswa:* Membuka aplikasi web, mengaktifkan sensor geolokasi ponsel, dan memindai QR code.
    3. *Swimlane Server & Basis Data:* Menjalankan logika validasi token, verifikasi sesi aktif, dan komit data ke tabel log.
  * **4 Titik Keputusan Kritis (Decision Diamonds):**
    * *Titik 1 (Geofencing GPS):* Menghitung jarak Haversine antara koordinat mahasiswa dan dosen. Jika $> 30\text{ meter}$, alur langsung dihentikan (*Presensi Ditolak*).
    * *Titik 2 (Masa Aktif Token QR):* Mengecek apakah token kedaluwarsa ($> 10\text{ detik}$). Jika lewat, diminta memindai ulang token yang baru.
    * *Titik 3 (Validasi Single Active Session):* Memastikan akun mahasiswa tidak sedang aktif di perangkat lain secara bersamaan.
    * *Titik 4 (Commit Basis Data):* Jika seluruh syarat terpenuhi, sistem melakukan commit atomik status `HADIR` dan mengirim sinyal WebSocket ke dashboard dosen.

---

### 3. Class Diagram: Struktur Domain Data & Relasi BCE
* **Fungsi Utama:** Memodelkan struktur statis objek, enkapsulasi data (atribut privat `-` dan metode publik `+`), serta relasi antar-entitas.
* **Elemen Teknis:**
  * **Pola Desain Boundary-Control-Entity (BCE):**
    * *Boundary:* Antarmuka pemindai dan dasbor (`PresensiUI`).
    * *Control:* Pengendali logika bisnis (`PresensiController`).
    * *Entity:* Objek basis data persisten (`User`, `Mahasiswa`, `Dosen`, `SesiPresensi`, `LogPresensi`).
  * **Hierarki Pewarisan (*Inheritance* / Generalisasi):**
    * Kelas `Mahasiswa` dan `Dosen` mewarisi kelas induk `User` (`nimNip`, `passwordHash`, `activeSessionId`, `lastDeviceId`). Hal ini menerapkan prinsip *Don't Repeat Yourself (DRY)*.
  * **Relasi Komposisi (`◆──`):**
    * Relasi antara `SesiPresensi` dan `LogPresensi` menggunakan garis komposisi berlian hitam pekat (`◆──`).
    * *Makna Semantik:* Keberadaan `LogPresensi` sangat bergantung secara eksklusif pada keberadaan `SesiPresensi`. Jika sesi kelas tidak pernah dibuka atau dibatalkan, baris log kehadiran tidak dapat eksis secara independen.
  * **Multiplisitas:**
    * `1` Dosen membuka `0..*` SesiPresensi.
    * `1` SesiPresensi menampung `0..*` LogPresensi.
    * `1` Mahasiswa memiliki `0..*` LogPresensi.

---

### 4. Sequence Diagram: Interaksi Objek & Pembuktian Kinerja N1
* **Fungsi Utama:** Memvalidasi aspek temporal (urutan waktu pesan dan metode) antara pengguna, antarmuka, server, dan basis data, serta membuktikan pencapaian target non-fungsional N1 ($< 2\text{ detik}$).
* **Elemen Teknis:**
  * **5 Lifeline Horizontal:** Mahasiswa $\rightarrow$ Web UI $\rightarrow$ Server API ScanIn $\rightarrow$ Basis Data MySQL $\rightarrow$ Dosen (Layar Proyektor).
  * **Fragmen Kombinasi Alternatif (`alt`):**
    * *Blok Gagal:* Jika jarak GPS $> 30\text{m}$ atau terdeteksi *Fake GPS*, server membalas dengan kode HTTP 403 Forbidden dalam waktu $\mathbf{0.3\text{ detik}}$ (fail-fast principle).
    * *Blok Sukses:* Jika lolos radius $\le 30\text{m}$, kamera aktif $\rightarrow$ memindai token dinamis ($< 1\text{ detik}$) $\rightarrow$ verifikasi server $\rightarrow$ eksekusi `INSERT INTO log_presensi` $\rightarrow$ konfirmasi centang hijau ke HP mahasiswa ($\mathbf{1.4\text{ detik}}$) $\rightarrow$ broadcast WebSocket ke layar dosen.
  * **Bukti Kinerja N1:** Total waktu komputasi dari scan hingga tersimpan di database adalah **1.4 detik**, memenuhi target rekayasa perangkat lunak $N1 < 2\text{ detik}$.

---

### 5. Matriks Konsistensi Antar-Diagram
Keempat diagram tidak dibuat terpisah secara acak, melainkan saling mengunci:
1. Aturan *Dynamic QR 10 Detik* & *Geofencing 30m* pada **Use Case** diuji alur percabangannya di **Activity Diagram**.
2. Parameter lokasi dan token didefinisikan tipe datanya di **Class Diagram** (`latDosen: float`, `tokenTTL: int`).
3. Seluruh interaksi tersebut dieksekusi secara terukur urutan milidetiknya di **Sequence Diagram**.

---

# BAGIAN II: NASKAH LENGKAP BACAAN PRESENTASI (WORD-FOR-WORD SCRIPT)

> *Gunakan naskah ini sebagai panduan lisan saat berbicara di depan proyektor. Tanda dalam kurung kurawal `[Isyarat]` adalah panduan gestur.*

---

### Slide 1: Pembuka & Identitas Tim
> *"Assalamu’alaikum Warahmatullahi Wabarakatuh.  
> Selamat pagi/siang kepada Ibu Wifda Muna Fatihia dan Bapak Surya Eka Priyatna selaku dosen pengampu, serta rekan-rekan mahasiswa sekalian.  
> 
> Kami dari **Kelompok 4** yang beranggotakan M. Gehan Junior, Asnah, Muhammad Supian Sauri, dan Muhammad Wildan Anshari, hari ini akan mempresentasikan hasil perancangan arsitektur dan pemodelan UML untuk aplikasi yang kami kembangkan, yaitu **ScanIn: Sistem Presensi Mahasiswa Berbasis Dynamic QR Code dan Geofencing**.* `[Klik Slide Selanjutnya]`"

---

### Slide 2: Latar Belakang Masalah Presensi
> *"Bapak dan Ibu dosen serta rekan-rekan,  
> Permasalahan presensi manual di perguruan tinggi hingga hari ini masih menyisakan empat celah besar:  
> 1. Pertama, tingginya angka **kecurangan titip absen**, di mana tanda tangan lembar kertas sangat mudah dipalsukan oleh rekan mahasiswa.  
> 2. Kedua, presensi kertas menyita **10 hingga 15 menit waktu berharga perkuliahan**.  
> 3. Ketiga, rekapitulasi data tidak berjalan secara *real-time*, sehingga dosen tidak dapat melihat persentase kehadiran seketika.  
> 4. Dan keempat, risiko hilangnya berkas fisik atau kesalahan transkrip data ke sistem akademik.* `[Klik Slide Selanjutnya]`"

---

### Slide 3: Solusi Aplikasi ScanIn
> *"Untuk memecahkan masalah tersebut secara tuntas, kami menghadirkan **ScanIn**.  
> ScanIn bukan sekadar aplikasi presensi QR biasa, melainkan sistem verifikasi berlapis dengan empat pilar inovasi:  
> 1. **Dynamic QR Code:** Kode QR berotasi otomatis setiap **10 detik**. Ini mematikan celah titip absen melalui tangkapan layar atau *screenshot*.  
> 2. **Geofencing GPS Presisi:** Mahasiswa wajib berada dalam radius maksimal **30 meter** dari lokasi dosen.  
> 3. **Dual-Mode Presensi:** ScanIn dirancang adaptif. Dapat menayangkan QR di proyektor kelas, atau langsung di layar HP dosen jika ruang kelas tidak memiliki fasilitas LCD proyektor.  
> 4. **Efisiensi Kinerja Tinggi (Kebutuhan N1):** Seluruh proses dari scan hingga data tersimpan di basis data tuntas dalam waktu **di bawah 2 detik**.* `[Klik Slide Selanjutnya]`"

---

### Slide 4–5: Use Case Diagram & Batasan Fungsional
> *`[Arahkan tangan ke gambar Use Case Diagram]`*  
> *"Selanjutnya, mari kita masuk ke pemodelan UML pertama, yaitu **Use Case Diagram**.  
> Diagram ini mendefinisikan batas sistem (*system boundary*) dan hak akses pengguna.  
> 
> Di sisi kiri, kita memiliki dua aktor utama:  
> * **Mahasiswa** sebagai inisiator proses presensi dan pemantau riwayat pribadi.  
> * Dan **Dosen** sebagai otoritas kelas yang membuka sesi perkuliahan, memilih mode tampilan, dan memiliki hak khusus untuk melakukan *Presensi Manual* sebagai mekanisme cadangan jika ada mahasiswa yang mengalami gangguan perangkat.  
> 
> Perhatikan pada relasi panah putus-putus berlabel **`<<include>>`**.  
> Dalam perancangan ini, Use Case *Pindai QR Presensi* secara mutlak mewajibkan eksekusi dua aturan validasi: yaitu *Validasi Geofencing Spasial 30 Meter* dan *Validasi Dynamic QR 10 Detik*. Artinya, secara arsitektural, sistem menolak pencatatan presensi tanpa melalui dua lapis keamanan ini.* `[Klik Slide Selanjutnya]`"

---

### Slide 6–7: Activity Diagram & 4 Gerbang Validasi
> *`[Arahkan pandangan ke 3 kolom Activity Diagram]`*  
> *"Beralih ke **Activity Diagram**, kami membagi proses bisnis menjadi 3 jalur kolaborasi atau *swimlane*: Dosen, Mahasiswa, dan Sistem Server.  
> 
> Alur dimulai saat Dosen membuka sesi kuliah dan mengunci koordinat GPS ruang kelas. Dosen memilih apakah menggunakan Mode Proyektor atau Mode Layar HP, lalu sistem mulai merotasi Dynamic QR tiap 10 detik.  
> 
> Saat Mahasiswa memindai QR, perhatikan empat titik keputusan kritis (*decision diamonds*):  
> 1. **Gerbang Pertama:** Sistem memeriksa radius GPS. Jika mahasiswa berada di luar jangkauan 30 meter, presensi seketika digagalkan.  
> 2. **Gerbang Kedua:** Sistem memeriksa usia token QR. Jika token sudah melewati 10 detik, mahasiswa diminta memindai ulang.  
> 3. **Gerbang Ketiga:** Sistem memvalidasi *Single Active Session* agar akun yang sama tidak dapat digunakan secara paralel di dua perangkat berbeda.  
> 4. Jika seluruh gerbang lolos, server melakukan *commit* data kehadiran secara atomik ke basis data, dan dasbor dosen langsung ter-update secara *real-time*.* `[Klik Slide Selanjutnya]`"

---

### Slide 8–9: Class Diagram & Struktur Relasi Objek
> *`[Tunjukkan struktur 4 kolom Class Diagram]`*  
> *"Berikutnya adalah **Class Diagram** yang memodelkan arsitektur data sistem menggunakan pendekatan *Boundary-Control-Entity (BCE)*.  
> 
> Ada tiga poin arsitektur penting pada diagram ini:  
> 1. **Prinsip Generalisasi (Pewarisan):** Kelas `Mahasiswa` dan `Dosen` diturunkan dari kelas induk `User`. Atribut keamanan seperti `nimNip`, `passwordHash`, dan `activeSessionId` cukup dikelola secara terpusat pada kelas induk.  
> 2. **Kelas SesiPresensi:** Kelas ini memegang peran krusial karena menyimpan koordinat jangkar GPS dosen, mode tampilan yang aktif, dan token acak dengan parameter `tokenTTL` bernilai 10 detik.  
> 3. **Relasi Komposisi Kuat (Simbol Berlian Hitam ◆──):** Relasi antara `SesiPresensi` dan `LogPresensi` dimodelkan sebagai komposisi. Secara semantik RPL, catatan kehadiran (*LogPresensi*) tidak boleh berdiri sendiri tanpa adanya sesi kelas yang sah. Jika sebuah sesi kuliah dibatalkan, maka integritas log terkait tetap terlindungi secara hierarkis.* `[Klik Slide Selanjutnya]`"

---

### Slide 10: Sequence Diagram & Pengujian Kinerja 1.4 Detik
> *`[Arahkan fokus ke garis alur Sequence Diagram]`*  
> *"Diagram ke-4 adalah **Sequence Diagram**, yang membuktikan aspek dinamis interaksi antar-objek dan pemenuhan kebutuhan non-fungsional N1 terkait kecepatan sistem.  
> 
> Pada diagram ini terdapat blok alternatif atau fragmen **`alt`**:  
> * **Skenario Gagal:** Jika jarak GPS mahasiswa melebihi 30 meter, server merespons pesan penolakan dalam waktu **0.3 detik**. Pendekatan *fail-fast* ini menghemat beban server dan kuota internet mahasiswa.  
> * **Skenario Sukses:** Ketika lokasi valid, kamera memindai kode QR dalam waktu kurang dari 1 detik, server memvalidasi masa berlaku token, lalu mengeksekusi perintah SQL `INSERT` ke basis data.  
> 
> **Poin Pembuktian Kinerja:**  
> Seluruh alur transaksi sukses—mulai dari bidikan kamera hingga munculnya centang hijau di ponsel mahasiswa—tercatat tuntas dalam waktu **1.4 detik**. Hal ini membuktikan secara ilmiah bahwa sistem ScanIn sukses melampaui standar kinerja N1, yaitu di bawah batas toleransi 2 detik.* `[Klik Slide Selanjutnya]`"

---

### Slide 11: Matriks Konsistensi Arsitektur
> *"Sebagai rangkuman teknis, Slide 11 memperlihatkan **Matriks Konsistensi Antar-Diagram**.  
> Seluruh diagram kami tidak berdiri sendiri, melainkan saling mengunci tanpa kontradiksi:  
> * Parameter *10 Detik* dan *30 Meter* pada Use Case terbukti diuji pada Activity Diagram, didefinisikan tipe datanya pada Class Diagram, dan diukur kecepatannya pada Sequence Diagram.  
> * Hak akses pengguna terisolasi dengan aman berkat *Single Active Session*.  
> * Serta sistem memiliki fleksibilitas operasional tinggi berkat dukungan *Dual-Mode* dan fitur *Presensi Manual*.* `[Klik Slide Selanjutnya]`"

---

### Slide 12: Penutup & Membuka Sesi Tanya Jawab
> *"Demikian presentasi dari Kelompok 4 mengenai Pemodelan UML Aplikasi ScanIn.  
> Kami percaya bahwa integrasi antara Dynamic QR 10 detik, Geofencing 30 meter, dan arsitektur BCE yang tangguh akan mampu menciptakan ekosistem presensi kampus yang cepat, akurat, dan berintegritas tinggi.  
> 
> Terima kasih atas perhatian Bapak dan Ibu dosen serta rekan-rekan sekalian.  
> Waktu dan tempat kami persilakan untuk sesi tanya jawab, saran, serta diskusi.  
> Wassalamu’alaikum Warahmatullahi Wabarakatuh."*

---

# BAGIAN III: BANK JAWABAN TANYA JAWAB DOSEN (KILLER DEFENSE Q&A)

### Pertanyaan 1: "Bagaimana jika mahasiswa di dalam kelas men-screenshot QR code lalu mengirimkannya via WhatsApp ke temannya yang masih di kos?"
> **Jawaban Telak:**  
> *"Izin menjawab, Bapak/Ibu. Skenario tersebut telah kami antisipasi dengan **keamanan berlapis (*defense-in-depth*)**:  
> 1. Pertama, kode QR di layar hanya berlaku selama **10 detik**. Waktu untuk mengambil screenshot, membuka WhatsApp, mengirim gambar, dan membuka pesan di sisi penerima rata-rata memakan waktu 8–15 detik, sehingga token hampir pasti sudah kedaluwarsa saat dicoba.  
> 2. Kedua dan yang paling mutlak: ScanIn menerapkan **Geofencing GPS radius 30 meter**. Sekalipun mahasiswa di kos berhasil menerima gambar QR dalam waktu 3 detik, server akan langsung menolak permintaannya pada tahap awal karena koordinat GPS ponselnya terdeteksi berada di luar ruang kelas."*

---

### Pertanyaan 2: "Bagaimana jika mahasiswa menggunakan aplikasi Fake GPS / Mock Location untuk memalsukan posisinya?"
> **Jawaban Telak:**  
> *"Izin menjawab, Bapak/Ibu. Aplikasi Web ScanIn memanfaatkan HTML5 Geolocation API yang membaca data sensor gabungan (GPS + Wi-Fi SSID kampus + Cell Tower).  
> Selain itu, pada sistem operasi Android modern, browser dapat mendeteksi flag `isMockProvider` atau atribut akurasi GPS yang abnormal (misalnya akurasi 0.0 meter yang tidak wajar pada sensor fisik). Jika terdeteksi anomali, server ScanIn langsung mengklasifikasikan transaksi tersebut sebagai percobaan kecurangan dan memblokir presensi."*

---

### Pertanyaan 3: "Bagaimana jika dosen mengajar di ruang kelas terpencil yang tidak ada proyektornya?"
> **Jawaban Telak:**  
> *"Izin menjawab, Bapak/Ibu. Itulah alasan kami merancang fitur **Dual-Mode Presensi**:  
> Dosen dapat memilih **Mode Mandiri**, di mana Dynamic QR ditampilkan langsung pada layar smartphone dosen. Mahasiswa cukup berbaris teratur dan memindai QR langsung dari layar HP dosen di meja depan. Dengan demikian, ketiadaan fasilitas LCD proyektor tidak menjadi penghambat berjalannya presensi digital."*

---

### Pertanyaan 4: "Bagaimana jika ada mahasiswa yang baterai HP-nya habis atau kuota internetnya mendadak tidak ada?"
> **Jawaban Telak:**  
> *"Izin menjawab, Bapak/Ibu. Sistem kami tidak mengabaikan kondisi darurat di lapangan. Di Use Case Diagram dan Class Diagram, kami telah menyematkan fitur **Presensi Manual (Override) oleh Dosen**.  
> Dosen memiliki wewenang administratif di dasbornya untuk menandai kehadiran mahasiswa tersebut secara manual setelah memverifikasi keberadaan fisiknya di dalam kelas, sehingga mahasiswa tidak dirugikan karena kendala teknis perangkat."*
