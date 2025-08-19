from flask import Flask, render_template, request, redirect, url_for
from ai_agent import tanya_ai_pertanian  # Tambahkan import ini
from ai_agent import tanya_ai_sim  # Tambahkan import ini
from ai_agent import tanya_ai_layanan_darurat  # Tambahkan import ini
from ai_agent import tanya_ai_hukum  # Tambahkan import ini
import feedparser

app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()

    # Mapping keyword → route navbar
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

    # cek keyword ada di mapping → redirect langsung
    for key, route in keyword_mapping.items():
        if key in query:
            return redirect(route)

    # fallback kalau tidak cocok → tampilkan search.html
    return render_template("search.html", query=query, hasil=[])

# daftar RSS feed yang mau ditarik
RSS_FEEDS = {
    "Google News": "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id",
    "Kompas": "https://www.kompas.com/rss/all",
    "Detik": "https://rss.detik.com/index.php/detikcom"
}

@app.route("/")
def home():
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

    return render_template("index.html", berita=berita)

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

@app.route('/ai_online')
def ai_online():
    return render_template("ai_online.html")

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
