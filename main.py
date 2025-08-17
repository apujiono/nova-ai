from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# 🧠 Inisialisasi memory (global list)
conversation_history = []

class Query(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "NOVA hidup!", "memory": len(conversation_history)}

@app.post("/ask")
def ask_nova(query: Query):
    global conversation_history

    # 🔹 Tambahkan pesan user ke memory
    conversation_history.append({"role": "user", "content": query.message})

    # 🔹 Kirim ke DeepSeek dengan riwayat
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": conversation_history,
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # 🔹 Tambahkan jawaban AI ke memory
        conversation_history.append({"role": "assistant", "content": reply})

        return {"response": reply}

    except Exception as e:
        return {"error": str(e), "response": "Maaf, NOVA gagal merespons."}

@app.post("/clear")
def clear_memory():
    global conversation_history
    conversation_history.clear()
    return {"status": "Memory bersih!"}
    
#Hanya jalankan server jika di lokal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
