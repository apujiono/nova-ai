from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "message": "NOVA hidup!"}

@app.post("/ask")
def ask():
    return {"response": "Halo, aku NOVA!"}
