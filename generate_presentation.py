import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(14, 34, 61)       # #0E223D
    TEAL = RGBColor(19, 154, 140)     # #139A8C
    LIGHT_BG = RGBColor(246, 248, 250)# #F6F8FA
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(33, 37, 41)
    MUTED_TEXT = RGBColor(108, 117, 125)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(222, 226, 230)
    GREEN_ACCENT = RGBColor(25, 135, 84)
    RED_ACCENT = RGBColor(220, 53, 69)
    LIGHT_TEAL = RGBColor(230, 246, 244)
    LIGHT_RED = RGBColor(253, 237, 237)

    def set_slide_background(slide, color=LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, title, category="EVALUASI 10 USABILITY HEURISTICS - SIAKAD UIN ANTASARI"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = TEAL

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(4)

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # ==================== SLIDE 1: COVER ====================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY)

    # Decorative Teal bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.5), Inches(0.15), Inches(4.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.color.rgb = TEAL

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(10.5), Inches(4.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TUGAS MANDIRI INTERAKSI MANUSIA & KOMPUTER"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL

    p = tf1.add_paragraph()
    p.text = "Analisis 10 Usability Heuristics & Komponen Usability pada SIAKAD"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Studi Kasus: Sistem Informasi Akademik (SIAKAD) UIN Antasari Banjarmasin"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(200, 220, 235)
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "\nOleh:\nM. GEHAN JUNIOR  |  NIM: 250104040186\nProgram Studi S1 Teknologi Informasi  •  Fakultas Dakwah dan Ilmu Komunikasi\nUniversitas Islam Negeri Antasari Banjarmasin  •  2026"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(180, 200, 220)
    p.space_before = Pt(20)

    # ==================== SLIDE 2: PENDAHULUAN ====================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Pendahuluan & Profil Sistem yang Dievaluasi", "LATAR BELAKANG EVALUASI")

    # Card 1: Profil SIAKAD
    add_card(slide2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    tbox = slide2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Profil Objek Studi"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    points = [
        ("Nama Sistem:", "SIAKAD UIN Antasari"),
        ("Alamat URL:", "siakad.uin-antasari.ac.id"),
        ("Pengguna Utama:", "Mahasiswa, Dosen Pembimbing Akademik, Bagian Akademik."),
        ("Fungsi Kunci:", "Registrasi Rencana Studi (KRS), monitoring Kartu Hasil Studi (KHS), pembayaran UKT, serta riwayat administrasi perkuliahan."),
        ("Urgensi:", "SIAKAD adalah sistem bertrafik tinggi dengan pengguna aktif ribuan mahasiswa setiap semester. Kualitas interaksi (usability) sangat menentukan efisiensi dan kepuasan mahasiswa.")
    ]
    for lbl, val in points:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_lbl = p.add_run()
        run_lbl.text = lbl + " "
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(13)
        run_lbl.font.color.rgb = NAVY
        run_val = p.add_run()
        run_val.text = val
        run_val.font.size = Pt(13)
        run_val.font.color.rgb = DARK_TEXT

    # Card 2: Metode Evaluasi
    add_card(slide2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tbox = slide2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Metode & Parameter Evaluasi"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    eval_points = [
        ("1. 10 Heuristik Usability (Jakob Nielsen)", "Metode evaluasi inspeksi antarmuka pengguna untuk mengidentifikasi kepatuhan terhadap prinsip kenyamanan dan efisiensi interaksi manusia-komputer."),
        ("2. Analisis Diterapkan & Dilanggar", "Membedah fitur riil pada SIAKAD disertai bukti tangkapan layar (screenshot), menilai aspek yang sudah berhasil dan aspek yang berpotensi menimbulkan kendala."),
        ("3. 5 Komponen Kualitas Usability", "Mengevaluasi secara holistik kelayakan sistem berdasarkan: Learnability, Efficiency, Memorability, Errors, dan Satisfaction.")
    ]
    for lbl, val in eval_points:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_lbl = p.add_run()
        run_lbl.text = lbl + "\n"
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(13)
        run_lbl.font.color.rgb = TEAL
        run_val = p.add_run()
        run_val.text = val
        run_val.font.size = Pt(12)
        run_val.font.color.rgb = DARK_TEXT

    # Helper for Heuristic Slides (Image Left or Right)
    def add_heuristic_slide(slide, title, img_filename, def_text, applied_title, applied_text, issue_title, issue_text):
        set_slide_background(slide)
        add_header(slide, title)

        # Image card on left
        img_card = add_card(slide, Inches(0.8), Inches(1.6), Inches(6.2), Inches(5.3))
        img_path = os.path.join(".", img_filename)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(0.95), Inches(1.85), width=Inches(5.9))

        # Right side cards
        # 1. Definition card
        add_card(slide, Inches(7.3), Inches(1.6), Inches(5.2), Inches(1.2), bg_color=WHITE)
        tbox = slide.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.8), Inches(1.0))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "DEFINISI PRINSIP"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = MUTED_TEXT
        p = tf.add_paragraph()
        p.text = def_text
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(3)

        # 2. Applied Card (Green accent)
        add_card(slide, Inches(7.3), Inches(3.0), Inches(5.2), Inches(1.85), bg_color=LIGHT_TEAL, border_color=TEAL)
        tbox = slide.shapes.add_textbox(Inches(7.5), Inches(3.1), Inches(4.8), Inches(1.65))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "✓ " + applied_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = GREEN_ACCENT
        p = tf.add_paragraph()
        p.text = applied_text
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(4)

        # 3. Issue / Critical Card (Red/Coral accent)
        add_card(slide, Inches(7.3), Inches(5.05), Inches(5.2), Inches(1.85), bg_color=LIGHT_RED, border_color=RED_ACCENT)
        tbox = slide.shapes.add_textbox(Inches(7.5), Inches(5.15), Inches(4.8), Inches(1.65))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "⚠ " + issue_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RED_ACCENT
        p = tf.add_paragraph()
        p.text = issue_text
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(4)

    # ==================== SLIDE 3: HEURISTIC 1 ====================
    slide3 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide3,
        "1. Visibility of System Status",
        "visibility of system status.png",
        "Sistem harus selalu memberi tahu pengguna tentang apa yang sedang terjadi melalui umpan balik (feedback) yang sesuai dan tepat waktu.",
        "Prinsip Diterapkan: Feedback Status Persetujuan Jelas",
        "Sistem menampilkan badge hijau toska bertuliskan '✓ TELAH DI-ACC' secara mencolok, total beban 23 SKS, dan nama Dosen Pembimbing Akademik. Mahasiswa mendapatkan kepastian langsung bahwa bimbingan dan KRS mereka telah tervalidasi.",
        "Catatan Kritis / Belum Diterapkan:",
        "Tidak ada informasi riwayat tanggal dan jam kapan Dosen PA menyetujui KRS, serta tidak ada indikator alur bertahap (stepper: Pengisian ➔ Menunggu ACC ➔ Selesai) untuk memantau progres secara visual."
    )

    # ==================== SLIDE 4: HEURISTIC 2 ====================
    slide4 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide4,
        "2. Match Between System and the Real World",
        "Match Between system and Real World.png",
        "Sistem harus berbicara dengan bahasa pengguna, menggunakan istilah, konsep, dan konvensi yang lumrah di dunia nyata mahasiswa.",
        "Prinsip Diterapkan: Bahasa & Metafora Akademik Familier",
        "Menu navigasi menggunakan terminologi baku perkuliahan: 'Dashboard', 'Registrasi KRS', 'Perkuliahan', 'Nilai', dan 'Pembayaran'. Penggunaan ikon seperti buku, kalender, dan piala merefleksikan objek nyata di kampus.",
        "Catatan Kritis / Belum Diterapkan:",
        "Identifikasi semester aktif ditulis dalam kode numerik sistem '20261'. Format ini membingungkan bagi mahasiswa baru dibandingkan label deskriptif seperti 'Semester Ganjil 2026/2027'."
    )

    # ==================== SLIDE 5: HEURISTIC 3 ====================
    slide5 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide5,
        "3. User Control and Freedom",
        "User Control and Freedom.png",
        "Pengguna sering salah memilih opsi dan memerlukan 'pintu darurat' (Undo/Cancel/Revisi) untuk membatalkan aksi tanpa alur berbelit-belit.",
        "Prinsip Diterapkan: Kebebasan Saat Masa Draft Pengisian",
        "Saat proses awal penyusunan rencana studi berlangsung, mahasiswa bebas memilih, menambah, atau membatalkan pilihan mata kuliah sebelum status diajukan ke Dosen PA.",
        "Prinsip Dilanggar / Tidak Diterapkan:",
        "Setelah status berubah menjadi 'PROSES REGISTRASI SELESAI' / 'TELAH DI-ACC', sistem mengunci total tanpa ada opsi 'Ajukan Revisi/Batal ACC' secara mandiri. Mahasiswa harus menemui Dosen PA atau operator akademik secara tatap muka."
    )

    # ==================== SLIDE 6: HEURISTIC 4 ====================
    slide6 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide6,
        "4. Consistency and Standards",
        "Consistency and Standards.png",
        "Pengguna tidak boleh bertanya-tanya apakah kata, situasi, atau tombol yang berbeda memiliki maksud yang sama. Patuhi konvensi desain web standar.",
        "Prinsip Diterapkan: Pola Layout & Skema Warna Konsisten",
        "Sidebar navigasi gelap di sisi kiri, navbar atas dengan tombol toggle hamburger, dan warna toska sebagai aksi utama (tombol 'Edit Profil', badge 'TELAH DI-ACC', tombol 'PRINT') diterapkan secara konsisten di semua halaman.",
        "Catatan Kritis / Inkonsistensi Visual:",
        "Terdapat redundansi pada halaman Dashboard, di mana foto profil mahasiswa dimuat dua kali (di header sidebar kiri dan di kartu biodata utama), menghabiskan ruang visual secara sia-sia."
    )

    # ==================== SLIDE 7: HEURISTIC 5 ====================
    slide7 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide7,
        "5. Error Prevention",
        "Error Prevention.png",
        "Desain yang baik secara aktif mencegah kesalahan terjadi sejak awal, bukan hanya menampilkan peringatan setelah kesalahan dibuat pengguna.",
        "Prinsip Diterapkan: Pembatasan Kuota SKS & Penguncian Data",
        "Sistem secara otomatis menghitung dan membatasi pengambilan SKS (terkunci tepat di 23 SKS), mencegah mahasiswa melanggar aturan akademik. Penguncian data pasca-ACC juga mencegah salah hapus kelas secara tak sengaja.",
        "Catatan Kritis / Belum Diterapkan:",
        "Kurangnya dialog konfirmasi bertingkat ('Apakah Anda yakin ingin menyelesaikan KRS? Data tidak dapat diubah setelah ini') sebelum penguncian, berisiko terklik tidak sengaja saat koneksi tidak stabil."
    )

    # ==================== SLIDE 8: HEURISTIC 6 ====================
    slide8 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide8,
        "6. Recognition Rather than Recall",
        "Recognition Rather than Recall.png",
        "Minimalkan beban ingatan pengguna dengan membuat opsi, objek, dan informasi terlihat jelas di antarmuka daripada memaksa pengguna mengingatnya.",
        "Prinsip Diterapkan: Menampilkan Nama Lengkap Mata Kuliah",
        "Tabel menyajikan Nama Mata Kuliah secara utuh ('Interaksi Manusia & Komputer', 'Pemrograman Web 1', dll) berdampingan dengan kode mata kuliah, kelas (TI25C), dan bobot SKS. Mahasiswa tidak perlu mengingat kode MK rumit.",
        "Catatan Kritis / Belum Diterapkan:",
        "Tabel rencana studi ini belum menampilkan informasi jadwal hari, jam, dan ruang kuliah secara terpadu, sehingga mahasiswa masih harus mengingat atau membuka halaman jadwal terpisah."
    )

    # ==================== SLIDE 9: HEURISTIC 7 ====================
    slide9 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide9,
        "7. Flexibility and Efficiency of Use",
        "Flexibility and Efficiency of Use.png",
        "Menyediakan jalan pintas (shortcuts/accelerators) agar pengguna berpengalaman dapat menyelesaikan tugas rutin dengan jauh lebih cepat.",
        "Prinsip Diterapkan: Shortcut Cetak KRS & Jadwal Terintegrasi",
        "Terdapat tombol dropdown fleksibel 'PRINT ▾' yang langsung menyediakan opsi cepat: 'PRINT KRS' dan 'PRINT JADWAL'. Mahasiswa tidak perlu berpindah ke modul jadwal terpisah untuk mengunduh jadwal mingguan.",
        "Catatan Kritis / Belum Diterapkan:",
        "Belum ada fitur pencarian instan (live search box) atau filter berdasarkan hari pada tabel rencana studi untuk mempercepat pencarian jadwal spesifik."
    )

    # ==================== SLIDE 10: HEURISTIC 8 ====================
    slide10 = prs.slides.add_slide(blank_layout)
    add_heuristic_slide(
        slide10,
        "8. Aesthetic and Minimalist Design",
        "Aesthetic and Minimalist Design.png",
        "Antarmuka tidak boleh memuat informasi berlebih atau tidak relevan yang dapat mengaburkan visibilitas data utama yang dibutuhkan pengguna.",
        "Prinsip Diterapkan: Layout Tabel Bersih & Minimalis",
        "Tabel rencana studi disajikan dalam kartu putih (white card) berlatar abu-abu netral dengan tipografi jelas dan garis pemisah tegas. Tidak ada banner promosi, animasi mengganggu, atau dekorasi yang mengaburkan data akademik.",
        "Catatan Kritis / Evaluasi Tata Letak:",
        "Pemanfaatan whitespace pada layar monitor widescreen masih belum seimbang; terdapat area kosong yang sangat luas di sebelah kanan tabel yang sebenarnya bisa dimanfaatkan untuk informasi jadwal/dosen."
    )

    # ==================== SLIDE 11: HEURISTICS 9 & 10 ====================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Analisis Kritis: Heuristik 9 & Heuristik 10", "HEURISTIK PENANGANAN ERROR & BANTUAN")

    # Heuristic 9 Card
    add_card(slide11, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tbox = slide11.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "9. Help Users Recognize, Diagnose, & Recover from Errors"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    h9_points = [
        ("Definisi:", "Pesan kesalahan harus dinyatakan dalam bahasa yang jelas (tanpa kode teknis), menunjukkan masalah secara tepat, dan menyarankan solusi konstruktif."),
        ("Prinsip Diterapkan:", "Sistem memberi indikator status peringatan jika batas SKS terlampaui atau jika ada tanggungan pembayaran UKT yang belum diselesaikan."),
        ("Prinsip Dilanggar / Kritis:", "Saat lonjakan akses serentak (war KRS), sistem kerap memunculkan halaman error baku server seperti '504 Gateway Time-out' atau '500 Internal Error' tanpa panduan solusi praktis yang menenangkan mahasiswa.")
    ]
    for lbl, val in h9_points:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_lbl = p.add_run()
        run_lbl.text = lbl + "\n"
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(12)
        run_lbl.font.color.rgb = TEAL if "Diterapkan" in lbl else (RED_ACCENT if "Dilanggar" in lbl else MUTED_TEXT)
        run_val = p.add_run()
        run_val.text = val
        run_val.font.size = Pt(11)
        run_val.font.color.rgb = DARK_TEXT

    # Heuristic 10 Card
    add_card(slide11, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tbox = slide11.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "10. Help and Documentation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    h10_points = [
        ("Definisi:", "Meskipun sistem dirancang intuitif, bantuan dan dokumentasi yang mudah dicari dan terfokus pada tugas pengguna tetap harus tersedia."),
        ("Prinsip Diterapkan:", "Tersedia informasi layanan lupa password mandiri dan kontak email institusi pada kolom pengumuman di beranda dashboard."),
        ("Prinsip Dilanggar / Kritis:", "Belum ada pusat bantuan terintegrasi (Help Center/FAQ), widget obrolan helpdesk, maupun dokumen panduan penggunaan (User Manual) yang dapat diunduh langsung di navbar sistem.")
    ]
    for lbl, val in h10_points:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_lbl = p.add_run()
        run_lbl.text = lbl + "\n"
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(12)
        run_lbl.font.color.rgb = TEAL if "Diterapkan" in lbl else (RED_ACCENT if "Dilanggar" in lbl else MUTED_TEXT)
        run_val = p.add_run()
        run_val.text = val
        run_val.font.size = Pt(11)
        run_val.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 12: 5 KOMPONEN USABILITY ====================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "Evaluasi 5 Komponen Kualitas Usability", "ANALISIS KELAYAKAN SISTEM (USABILITY COMPONENTS)")

    # Table layout
    table_card = add_card(slide12, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    
    rows = 6
    cols = 4
    left = Inches(1.0)
    top = Inches(1.8)
    width = Inches(11.333)
    height = Inches(4.8)

    table_shape = slide12.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(6.0)
    table.columns[3].width = Inches(1.333)

    headers = ["Komponen", "Indikator Evaluasi", "Temuan pada SIAKAD UIN Antasari", "Penilaian"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ("1. Learnability\n(Kemudahan Belajar)", "Seberapa mudah pengguna baru menyelesaikan tugas dasar pada kunjungan pertama?", "Menu terbagi logis (Dashboard, Registrasi, Nilai). Mahasiswa baru dapat mengisi KRS secara mandiri dalam 1–2 kali percobaan.", "BAIK"),
        ("2. Efficiency\n(Efisiensi)", "Seberapa cepat tugas dapat diselesaikan setelah pengguna mahir?", "Tugas rutin seperti cetak jadwal sangat cepat via shortcut dropdown. Namun efisiensi merosot tajam saat periode rebutan KRS akibat beban server.", "CUKUP"),
        ("3. Memorability\n(Daya Ingat)", "Seberapa mudah mengingat alur setelah lama tidak membuka sistem?", "Sangat baik. Meskipun hanya diakses intensif setiap 6 bulan (pergantian semester), pengguna langsung ingat posisi menu karena navigasi konsisten.", "SANGAT BAIK"),
        ("4. Errors\n(Toleransi Kesalahan)", "Berapa banyak kesalahan pengguna, seberapa parah, & cara pemulihannya?", "Pencegahan salah SKS sudah otomatis. Namun pemulihan salah pilih kelas pasca-ACC sulit karena sistem terkunci total tanpa fitur revisi mandiri.", "CUKUP"),
        ("5. Satisfaction\n(Kepuasan Pengguna)", "Seberapa menyenangkan antarmuka dan pengalaman pengguna secara umum?", "Pengguna merasa aman dengan adanya status 'TELAH DI-ACC' yang jelas. Tampilan tergolong formal dan bersih meski sedikit kaku.", "BAIK")
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else RGBColor(245, 248, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = cell_value
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_TEXT
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY
            elif col_idx == 3:
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
                if "SANGAT" in cell_value:
                    p.font.color.rgb = GREEN_ACCENT
                elif "BAIK" in cell_value:
                    p.font.color.rgb = TEAL
                else:
                    p.font.color.rgb = RGBColor(220, 120, 20)

    # ==================== SLIDE 13: KESIMPULAN & REKOMENDASI ====================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "Kesimpulan Kelayakan Usability & Rekomendasi Solusi", "KESIMPULAN AKHIR")

    # Conclusion Card
    add_card(slide13, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), bg_color=LIGHT_TEAL, border_color=TEAL)
    tbox = slide13.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Apakah SIAKAD 'Usable'?"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf.add_paragraph()
    p.text = "STATUS: SUDAH USABLE (LAYAK PAKAI)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_before = Pt(8)

    p = tf.add_paragraph()
    p.text = "Website SIAKAD UIN Antasari secara fundamental telah memenuhi standar usabilitas untuk mendukung tugas-tugas akademik pokok:\n" \
             "• Seluruh alur utama (registrasi rencana studi, pengecekan nilai KHS, pembayaran) berfungsi dengan efektif.\n" \
             "• Tingkat kepatuhan terhadap prinsip Heuristik Nielsen cukup tinggi, terutama pada kejelasan status sistem, penggunaan bahasa akademik yang familier, dan desain yang minimalis.\n" \
             "• Daya ingat (memorability) sistem terbukti tinggi berkat konsistensi tata letak antar semester."
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(10)

    # Recommendations Card
    add_card(slide13, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tbox = slide13.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Rekomendasi Perbaikan (Actionable Improvements)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY

    recs = [
        ("1. Fitur Pengajuan Batal/Revisi Mandiri", "Menambahkan tombol 'Ajukan Pembatalan ACC' dengan verifikasi Dosen PA sebelum batas akhir masa KRS, guna mendukung Heuristik User Control & Freedom."),
        ("2. Penanganan Error yang Lebih Informatif", "Mengganti halaman error 504 server dengan halaman kustom interaktif yang menginformasikan antrean server dan instruksi refresh berkala."),
        ("3. Pusat Dokumentasi & FAQ Terintegrasi", "Menambahkan menu ikon tanda tanya (?) di header yang berisi buku panduan PDF dan kontak helpdesk cepat."),
        ("4. Integrasi Jadwal pada Tabel KRS", "Menampilkan kolom jam perkuliahan dan ruangan kelas langsung pada tabel rencana studi.")
    ]
    for lbl, val in recs:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        run_lbl = p.add_run()
        run_lbl.text = lbl + "\n"
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(12)
        run_lbl.font.color.rgb = TEAL
        run_val = p.add_run()
        run_val.text = val
        run_val.font.size = Pt(11)
        run_val.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 14: PENUTUP ====================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, NAVY)

    tbox = slide14.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.333), Inches(3.5))
    tf14 = tbox.text_frame
    tf14.word_wrap = True

    p = tf14.paragraphs[0]
    p.text = "TERIMA KASIH"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf14.add_paragraph()
    p.text = "Sesi Tanya Jawab & Diskusi"
    p.font.size = Pt(18)
    p.font.color.rgb = TEAL
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(10)

    p = tf14.add_paragraph()
    p.text = "M. GEHAN JUNIOR  |  NIM: 250104040186\nS1 Teknologi Informasi — UIN Antasari Banjarmasin"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(180, 200, 220)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(24)

    output_path = "Presentasi_Evaluasi_Usability_SIAKAD_UIN_Antasari.pptx"
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()

