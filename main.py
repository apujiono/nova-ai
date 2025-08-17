from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "message": "NOVA hidup!"}

conversation_history = []
@app.post("/ask")
def ask():
    return {"response": "Halo, aku NOVA!"}
def ask_nova(query: Query):
    global conversation_history

    # Simpan input user
    conversation_history.append({"role": "user", "content": query.message})

    try:
        response = get_ai_response(query.message, conversation_history)
        # Simpan jawaban AI
        conversation_history.append({"role": "assistant", "content": response})
        return {"response": response}
    except Exception as e:
        return {"error": str(e)
    
#Hanya jalankan server jika di lokal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
