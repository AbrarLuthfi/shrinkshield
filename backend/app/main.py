from fastapi import FastAPI

app = FastAPI(title="ShrinkShield API")

@app.get("/health")
def health():
    return {"status": "ok", "message": "ShrinkShield backend is running 🚀"}
