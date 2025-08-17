from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="NOVA AI", version="0.1")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("sk-f0d23eb257be4732807676997a82c6bb")  # Harus di-set di Railway

class Query(BaseModel):
    message: str
    history: list = []

@app.post("/ask")
def ask_nova(query: Query):
    if not API_KEY:
        return {"error": "API key not set"}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "1application/json"
    }

    messages = query.history + [{"role": "user", "content": query.message}]

    payload = {
        "model": "deepseek-chat",
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
        return {"error": str(e), "response": "NOVA sedang offline."}

@app.get("/")
def home():
    return {"status": "NOVA siap membantu!", "api_key_set": API_KEY is not None}
    
@app.get("/")
def home():
    return {"status": "OK", "message": "NOVA AI is alive!"}
