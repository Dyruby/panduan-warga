import markdown
from markupsafe import Markup
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from ai_agent import tanya_ai_pertanian  # Tambahkan import ini
from ai_agent import tanya_ai_sim  # Tambahkan import ini
from ai_agent import tanya_ai_layanan_darurat  # Tambahkan import ini
from ai_agent import tanya_ai_hukum  # Tambahkan import ini
import feedparser
import mysql.connector
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Konfigurasi koneksi ke MySQL
load_dotenv() 

SECRET_CODE = os.getenv("SECRET_CODE", "").strip().lower()

# set secret key dari .env
app.secret_key = os.getenv("SECRET_KEY")

# cek apakah secret key berhasil dibaca
print("SECRET_KEY:", app.secret_key)

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/masukan")
def masukan():
    return render_template("masukan.html")

@app.route("/kirim", methods=["POST"])
def kirim():
    nama = request.form["nama"]
    isi = request.form["isi"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO masukan (nama, isi) VALUES (%s, %s)", (nama, isi))
    conn.commit()
    cursor.close()
    conn.close()

    # Menentukan notifikasi
    tipe = "Masukan" if "masukan" in isi.lower() else "Kritikan"
    flash(f"✅ {tipe} berhasil dikirim!", "success")

    return redirect(url_for("masukan"))  # kembali ke halaman masukan kosong

@app.route("/lihat")
def lihat():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM masukan ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("lihat.html", data=data)

# 🔹 Edit masukan
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nama = request.form["nama"]
        isi = request.form["isi"]
        cursor.execute("UPDATE masukan SET nama=%s, isi=%s WHERE id=%s", (nama, isi, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("lihat"))

    cursor.execute("SELECT * FROM masukan WHERE id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit.html", data=data)

# 🔹 Hapus masukan
@app.route("/hapus/<int:id>")
def hapus(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM masukan WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("lihat"))

@app.route("/search", methods=["GET"])
def search():
    query = (request.args.get("q") or "").strip().lower()
    user_ip = request.remote_addr

    # Mapping normal (JANGAN masukkan kata rahasia di sini)
    keyword_mapping = {
        "sim": "/panduan_sim",
        "buat sim": "/panduan_sim",
        "perpanjang sim": "/panduan_sim",
        "petani": "/panduan_bertani_di_rawa",
        "pertanian": "/panduan_bertani_di_rawa",
        "padi": "/panduan_bertani_di_rawa",
        "darurat": "/bantuan_layanan_darurat",
        "ambulans": "/bantuan_layanan_darurat",
        "polisi": "/bantuan_layanan_darurat",
        "pemadam": "/bantuan_layanan_darurat",
        "hukum": "/panduan_hukum",
        "peraturan": "/panduan_hukum",
        "uu": "/panduan_hukum",
    }

    # 1) Jika query adalah secret (yang disimpan di .env), langsung akses lihat tanpa simpan riwayat
    if SECRET_CODE and query == SECRET_CODE:
        # tidak menyimpan query ke riwayat
        # jika butuh IP-binding atau mekanisme owner, tambahkan pengecekan DB di sini
        return redirect(url_for("lihat"))

    # 2) Bukan secret → proses normal: cari di mapping lalu simpan riwayat bila ada query
    hasil = []
    if query in keyword_mapping:
        hasil.append({
            "judul": query.title(),
            "konten": f"Panduan terkait {query}",
            "link": keyword_mapping[query]
        })

    # contoh menyimpan riwayat (MySQL / SQLite sesuai implementasimu)
    if query:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO riwayat (query, waktu, ip) VALUES (%s, NOW(), %s)",
                        (query, user_ip))
        conn.commit()
        cursor.close()
        conn.close()

    return render_template("search.html", query=query, hasil=hasil)

# daftar RSS feed yang mau ditarik
RSS_FEEDS = {
    "Google News": "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id",
    "Kompas": "https://www.kompas.com/rss/all",
    "Detik": "https://rss.detik.com/index.php/detikcom"
}

@app.route("/berita_terkini")
def berita_terkini():
    berita = []

    for sumber, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # ambil 5 berita per portal
            berita.append({
                "judul": entry.title,
                "link": entry.link,
                "tanggal": entry.published if "published" in entry else "",
                "konten": entry.summary if "summary" in entry else "",
                "sumber": sumber
            })
    
    # urutkan berita dari yang terbaru (kalau ada published)
    berita = sorted(berita, key=lambda x: x["tanggal"], reverse=True)

    return render_template("berita_terkini.html", berita=berita)

# Halaman Ujian Teori
@app.route("/sim/ujian", methods=["GET", "POST"])
def sim_ujian():
    if request.method == "POST":
        kunci = ['b', 'a', 'c']  # kunci jawaban soal 1-3
        user_jawaban = [
            request.form.get("jawaban1"),
            request.form.get("jawaban2"),
            request.form.get("jawaban3")
        ]
        skor = sum([1 for i, j in zip(user_jawaban, kunci) if i == j])
        return render_template("sim_hasil.html", skor=skor, total=len(kunci))
    return render_template("sim_ujian.html")

# Halaman Hasil Ujian
@app.route("/sim/hasil")
def sim_hasil():
    return render_template("sim_hasil.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/panduan_sim')
def panduan_sim():
    return render_template("panduan_sim.html")

@app.route('/jenis_sim')
def jenis_sim():
    return render_template("jenis_sim.html")

@app.route('/pengarahan')
def pengarahan():
    return render_template("pengarahan.html")

@app.route('/hukum_sim')
def hukum_sim():
    return render_template("hukum_sim.html")

@app.route('/tutorial_sim')
def tutorial_sim():
    return render_template("tutorial_sim.html")

@app.route('/panduan_bertani')
def panduan_bertani():
    return render_template("panduan_bertani.html")

@app.route('/tanaman_nutrisi')
def tanaman_nutrisi():
    return render_template("tanaman_nutrisi.html")

@app.route('/hama_penyakit')
def hama_penyakit():
    return render_template("hama_penyakit.html")

@app.route('/harga_komunitas')
def harga_komunitas():
    return render_template("harga_komunitas.html")

@app.route('/alat_teknologi')
def alat_teknologi():
    return render_template("alat_teknologi.html")

@app.route('/bantuan_layanan_darurat')
def bantuan_layanan_darurat():
    return render_template("bantuan_layanan_darurat.html")

@app.route('/panduan_hukum')
def panduan_hukum():
    return render_template("panduan_hukum.html")

@app.route("/tentang")
def tentang():
    return render_template("tentang.html")

@app.route("/is_owner")
def is_owner():
    """
    Mengecek apakah visitor adalah owner.
    Owner = IP yang tercatat di DB.
    """
    user_ip = request.remote_addr
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM secret_codes WHERE status='active' LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return jsonify({"owner": False})

    owner_ip = row.get("owner_ip") or row.get("used_by")
    if owner_ip and owner_ip == user_ip:
        return jsonify({"owner": True})
    return jsonify({"owner": False})

@app.route("/set_secret/<code>")
def set_secret(code):
    """
    Dipanggil sekali untuk mendaftarkan owner.
    Contoh: buka http://localhost:5000/set_secret/RAHASIAKU
    """
    user_ip = request.remote_addr
    conn = get_db_connection()
    cursor = conn.cursor()

    # Nonaktifkan secret lama
    cursor.execute("UPDATE secret_codes SET status='expired' WHERE status='active'")

    # Tambahkan secret baru
    cursor.execute(
        "INSERT INTO secret_codes (code, owner_ip, status, created_at) VALUES (%s, %s, 'active', NOW())",
        (code, user_ip)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return f"Secret {code} berhasil dibuat untuk IP {user_ip}"

@app.route('/sim', methods=['GET', 'POST'])
def sim():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        raw_response = tanya_ai_sim(question)
        # Konversi Markdown → HTML
        response = Markup(markdown.markdown(raw_response))
    return render_template("sim.html", response=response)

@app.route('/petani', methods=['GET', 'POST'])
def petani():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        raw_response = tanya_ai_pertanian(question)
        # Konversi Markdown → HTML
        response = Markup(markdown.markdown(raw_response))
    return render_template("petani.html", response=response)

@app.route('/darurat', methods=['GET', 'POST'])
def darurat():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        raw_response = tanya_ai_layanan_darurat(question)
        # Konversi Markdown → HTML
        response = Markup(markdown.markdown(raw_response))
    return render_template("darurat.html", response=response)

@app.route('/hukum', methods=['GET', 'POST'])
def hukum():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        raw_response = tanya_ai_hukum(question)
        # Konversi Markdown → HTML
        response = Markup(markdown.markdown(raw_response))
    return render_template("hukum.html", response=response)

if __name__ == '__main__':
    app.run(debug=True)
