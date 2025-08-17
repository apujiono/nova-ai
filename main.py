from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# 🔐 Izinkan frontend (browser) akses API
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📁 Serve file statis dari folder 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🧠 Memory percakapan
conversation_history = []

class Query(BaseModel):
    message: str

# 🏠 Halaman utama
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ask")
def ask_nova(query: Query):
    global conversation_history
    conversation_history.append({"role": "user", "content": query.message})

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
        conversation_history.append({"role": "assistant", "content": reply})
        return {"response": reply}
    except Exception as e:
        return {"error": str(e), "response": "NOVA sedang offline."}

@app.post("/clear")
def clear_memory():
    global conversation_history
    conversation_history.clear()
    return {"status": "Memory bersih!"}
    
#Hanya jalankan server jika di lokal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
