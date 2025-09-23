from dotenv import load_dotenv
import os
import requests

# 🔑 Ambil API Key dari .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-3-8b-instruct"

# 🛠️ Fungsi umum untuk memanggil API
def call_ai(system_prompt, query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Error {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "⚠️ Waktu koneksi habis, coba lagi."
    except Exception as e:
        return f"⚠️ Terjadi kesalahan: {str(e)}"

# 🌾 Pertanian
def tanya_ai_pertanian(query):
    system_prompt = (
        "Kamu adalah AI pakar pertanian rawa-rawa. "
        "Jawab hanya pertanyaan yang relevan dengan pertanian di daerah rawa. "
        "Jika tidak relevan, katakan dengan sopan bahwa kamu hanya fokus pada pertanian rawa. "
        "Jawablah dengan bahasa Indonesia yang ringkas, akurat, dan jelas."
    )
    return call_ai(system_prompt, query)

# 🪪 SIM
def tanya_ai_sim(query):
    system_prompt = (
        "Kamu adalah AI pakar pembuatan SIM (Surat Izin Mengemudi) di Indonesia. "
        "Fokus hanya pada prosedur, syarat, biaya, atau tahapan pembuatan dan perpanjangan SIM. "
        "Jika ada pertanyaan di luar topik tersebut, balas dengan sopan bahwa kamu hanya bisa menjawab seputar SIM. "
        "Jawablah dengan bahasa Indonesia yang jelas, ringkas, akurat, dan gunakan poin bila perlu."
    )
    return call_ai(system_prompt, query)

# 🚨 Layanan Darurat
def tanya_ai_layanan_darurat(query):
    system_prompt = (
        "Kamu adalah AI asisten untuk membantu masyarakat mengenai layanan darurat di Indonesia. "
        "Fokus hanya pada: nomor telepon penting (polisi, ambulans, pemadam), prosedur dalam keadaan darurat, "
        "tindakan pertama saat kecelakaan, kebakaran, bencana, serta panduan keselamatan lainnya. "
        "Jika pertanyaan tidak relevan, balas dengan sopan bahwa kamu hanya dapat membantu seputar layanan darurat. "
        "Jawablah dengan bahasa Indonesia yang singkat, padat, dan jelas."
    )
    return call_ai(system_prompt, query)

# ⚖️ Hukum
def tanya_ai_hukum(query):
    system_prompt = (
        "Kamu adalah AI asisten hukum untuk warga Indonesia. "
        "Jawabanmu harus berdasarkan hukum positif Indonesia: UUD 1945, KUHP, KUHPerdata, dan undang-undang resmi "
        "seperti UU ITE, UU Kesehatan, dll. Sertakan referensi pasal atau undang-undang bila memungkinkan. "
        "Jika pertanyaan tidak relevan, balas dengan sopan bahwa kamu hanya menjawab seputar hukum di Indonesia. "
        "Gunakan bahasa Indonesia formal, jelas, dan akurat."
    )
    return call_ai(system_prompt, query)
