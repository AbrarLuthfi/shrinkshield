from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session


from .db import Base, engine, SessionLocal, ping_db
from . import models
from .models import Receipt, ReceiptLine
from .ocr import OCRAdapter

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ocr = OCRAdapter()

@app.post("/receipts", response_model=dict)
async def upload_receipt(file: UploadFile = File(...)):
    """
    Accept an image/PDF, run OCR (stub), persist raw OCR & lines.
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    # Run OCR (stub for now)
    ocr_out = ocr.extract(content, file.content_type or "application/octet-stream")
    lines: List[str] = ocr_out.get("lines", [])

    # Persist
    with SessionLocal() as db:
        receipt = Receipt(
            filename=file.filename,
            mimetype=file.content_type or "application/octet-stream",
            ocr_raw=ocr_out,
        )
        db.add(receipt)
        db.flush()  # get receipt.id

        for ln in lines:
            db.add(ReceiptLine(receipt_id=receipt.id, line_text=ln))

        db.commit()
        db.refresh(receipt)

        return {"id": receipt.id, "filename": receipt.filename, "lines": len(lines)}

@app.get("/receipts", response_model=List[dict])
def list_receipts():
    with SessionLocal() as db:
        rows = db.query(Receipt).order_by(Receipt.id.desc()).limit(50).all()
        return [
            {
                "id": r.id,
                "filename": r.filename,
                "uploaded_at": r.uploaded_at,
                "mimetype": r.mimetype,
            }
            for r in rows
        ]

@app.get("/receipts/{receipt_id}", response_model=dict)
def get_receipt(receipt_id: int):
    with SessionLocal() as db:
        r = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Not found")
        lines = db.query(ReceiptLine).filter(ReceiptLine.receipt_id == receipt_id).all()
        return {
            "id": r.id,
            "filename": r.filename,
            "uploaded_at": r.uploaded_at,
            "mimetype": r.mimetype,
            "ocr_raw": r.ocr_raw,
            "lines": [x.line_text for x in lines],
        }
