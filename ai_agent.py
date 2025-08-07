import requests

API_KEY ="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"# Ganti dengan API key milikmu
MODEL = "meta-llama/llama-3-8b-instruct"

def tanya_ai_pertanian(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah AI pakar pertanian rawa-rawa. "
                    "Jawab hanya pertanyaan yang relevan dengan pertanian di daerah rawa. "
                    "Jika tidak relevan, katakan dengan sopan bahwa kamu hanya fokus pada pertanian rawa."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    print(response.text)  # tambahkan ini untuk lihat error dari API
    return "⚠️ Gagal menghubungi AI."

def tanya_ai_sim(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah AI pakar pembuatan SIM (Surat Izin Mengemudi) di Indonesia. "
                    "Jawab hanya pertanyaan yang berkaitan dengan prosedur, syarat, biaya, atau tahapan pembuatan SIM. "
                    "Jika ada pertanyaan di luar topik tersebut, sampaikan dengan sopan bahwa kamu hanya bisa menjawab seputar pembuatan SIM."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return "⚠️ Gagal menghubungi AI."

def tanya_ai_layanan_darurat(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah AI asisten untuk membantu masyarakat mengenai layanan darurat di Indonesia. "
    "Fokuskan jawabanmu hanya pada hal-hal terkait layanan darurat seperti: nomor telepon penting (polisi, ambulans, pemadam), prosedur dalam keadaan darurat, "
    "tindakan pertama yang harus dilakukan saat terjadi kecelakaan, kebakaran, atau bencana, dan panduan keselamatan lainnya. "
    "Jika ada pertanyaan yang tidak relevan dengan topik layanan darurat, balas dengan sopan seperti: "
    "Maaf, saya hanya dapat membantu seputar informasi dan panduan layanan darurat di Indonesia."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return "⚠️ Gagal menghubungi AI."

def tanya_ai_hukum(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten AI hukum yang membantu warga Indonesia memahami hukum, pasal, dan hak yang berlaku. "
                    "Jawabanmu harus berdasarkan hukum positif Indonesia, seperti UUD 1945, KUHP, KUHPerdata, dan UU resmi seperti UU No. 11 Tahun 2008 tentang ITE, UU No. 36 Tahun 2009 tentang Kesehatan, dan lainnya. "
                    "Sertakan referensi pasal atau undang-undang jika memungkinkan. "
                    "Jika pertanyaan tidak relevan dengan topik hukum, kamu harus membalas dengan sopan seperti: "
                    "'Maaf, saya hanya dapat membantu seputar pertanyaan yang berkaitan dengan hukum dan perundang-undangan yang berlaku di Indonesia.'"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return "⚠️ Gagal menghubungi AI."


