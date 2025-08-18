from flask import Flask, render_template, request, redirect, url_for
from ai_agent import tanya_ai_pertanian  # Tambahkan import ini
from ai_agent import tanya_ai_sim  # Tambahkan import ini
from ai_agent import tanya_ai_layanan_darurat  # Tambahkan import ini
from ai_agent import tanya_ai_hukum  # Tambahkan import ini

app = Flask(__name__)

panduan_data = [
    {
        "judul": "Cara Membuat SIM",
        "link": "/panduan_sim",
        "konten": "Langkah-langkah membuat SIM: siapkan KTP, daftar di Satpas terdekat, ikuti tes teori dan praktik."
    },
    {
        "judul": "Tips Bertani di Rawa",
        "link": "/panduan_bertani_di_rawa",
        "konten": "Petani di rawa sebaiknya memilih bibit padi unggul yang tahan genangan air..."
    },
    {
        "judul": "Nomor Darurat Penting",
        "link": "/bantuan_layanan_darurat",
        "konten": "Polisi 110, Ambulans 118/119, Pemadam Kebakaran 113."
    }
]


berita_data = [
    {"judul": "Perpanjangan SIM Online Resmi Dibuka", 
     "isi": "Sekarang warga bisa memperpanjang SIM secara online tanpa harus antri panjang di kantor...",
     "tanggal": "18 Agustus 2025"},
    {"judul": "Layanan Darurat 24 Jam Diperkuat", 
     "isi": "Pemerintah menambah petugas darurat untuk respon lebih cepat di daerah terpencil.",
     "tanggal": "15 Agustus 2025"}
]

# 🏠 Beranda
@app.route("/")
def home():
    return render_template("index.html", berita=berita_data)

# 🔍 Fitur Pencarian
@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    hasil = [p for p in panduan_data if query in p["judul"].lower()]
    return render_template("search.html", query=query, hasil=hasil)

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

@app.route('/panduan_bertani_di_rawa')
def panduan_bertani_di_rawa():
    return render_template("panduan_bertani_di_rawa.html")

@app.route('/bantuan_layanan_darurat')
def bantuan_layanan_darurat():
    return render_template("bantuan_layanan_darurat.html")

@app.route('/panduan_hukum')
def panduan_hukum():
    return render_template("panduan_hukum.html")

@app.route('/sim', methods=['GET', 'POST'])
def sim():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        response = tanya_ai_sim(question)
    return render_template("sim.html", response=response)

@app.route('/petani', methods=['GET', 'POST'])
def petani():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        response = tanya_ai_pertanian(question)
    return render_template("petani.html", response=response)

@app.route('/darurat', methods=['GET', 'POST'])
def darurat():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        response = tanya_ai_layanan_darurat(question)
    return render_template("darurat.html", response=response)

@app.route('/hukum', methods=['GET', 'POST'])
def hukum():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        response = tanya_ai_hukum(question)
    return render_template("hukum.html", response=response)

if __name__ == '__main__':
    app.run(debug=True)
