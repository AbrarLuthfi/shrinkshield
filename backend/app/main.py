from fastapi import FastAPI
from sqlalchemy import text
from .db import Base, engine, SessionLocal, ping_db
from . import models

app = FastAPI(title="ShrinkShield API")

@app.get("/health")
def health():
    return {"status": "ok", "message": "ShrinkShield backend is running 🚀"}

@app.get("/db/ping")
def db_ping():
    ping_db()
    return {"db": "ok"}

@app.post("/db/sample-user")
def create_sample_user():
    """Insert a demo user to prove writes work."""
    with SessionLocal() as s:
        s.execute(text("INSERT INTO users (email, created_at) VALUES (:e, NOW())"),
                  {"e": "demo@example.com"})
        s.commit()
    return {"created": True}
