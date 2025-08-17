from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Hanya untuk lokal, di Railway nggak perlu
load_dotenv()

app = FastAPI(title="NOVA AI - Personal Assistant", version="0.1")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("sk-f0d23eb257be4732807676997a82c6bb")

class Query(BaseModel):
    message: str
    history: list = []  # format: [{"role": "user"|"assistant", "content": "..." }]

@app.post("/ask")
def ask_nova(query: Query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Gabungkan riwayat + pesan terbaru
    messages = query.history + [{"role": "user", "content": query.message}]

    payload = {
        "model": "deepseek-chat",  # model utama mereka
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return {"response": reply}
    except Exception as e:
        return {"error": str(e), "response": "Maaf, NOVA sedang error."}

# Health check
@app.get("/")
def home():
    return {"status": "NOVA AI siap melayani!"}
