from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "message": "NOVA hidup!"}

@app.post("/ask")
def ask():
    return {"response": "Halo, aku NOVA!"}
    
#Hanya jalankan server jika di lokal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
