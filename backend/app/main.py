from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session


from .db import Base, engine, SessionLocal, ping_db
from . import models
from .models import Receipt, ReceiptLine, ProductLine
from .ocr.adapter import OCRAdapter
from .utils.normalizer import normalize_size


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


@app.post("/receipts", response_model=dict)
async def upload_receipt(file: UploadFile = File(...)):
    """
    Accept an image/PDF, run OCR (stub), persist raw OCR & structured product lines.
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    # --- Run OCR (stub) ---
    ocr = OCRAdapter()

    # For Day 3 you had ocr.extract(...) that returned {"lines": [...]}
    # For Day 4 we use a stub that returns structured lines:
    # [{"name":"Distilled Water","size":"1 L","price":1.29}, ...]
    parsed_lines = ocr.extract_lines(content)  # accept bytes in your stub

    # OPTIONAL: if you still want to keep a human-readable "raw lines" list
    raw_lines = [f"{ln['name']} {ln['size']} ${ln['price']}" for ln in parsed_lines]

    # --- Persist everything in one transaction ---
    with SessionLocal() as db:
        # 1) Save the receipt
        receipt = Receipt(
            filename=file.filename,
            mimetype=file.content_type or "application/octet-stream",
            ocr_raw={"lines": raw_lines},  # keep raw list for /receipts/{id}
        )
        db.add(receipt)
        db.flush()              # <-- get receipt.id

        # 2) Keep Day-3 behavior (optional): store raw lines
        for ln_text in raw_lines:
            db.add(ReceiptLine(receipt_id=receipt.id, line_text=ln_text))

        # 3) Day-4 behavior: normalize & store structured product lines
        for ln in parsed_lines:
            size_ml = normalize_size(ln["size"]) if ln.get("size") else None
            unit = (ln["price"] / size_ml) if (size_ml and ln.get("price") is not None) else None

            db.add(ProductLine(
                receipt_id=receipt.id,
                name=ln["name"],
                raw_size=ln["size"],
                normalized_size_ml=size_ml,
                price=ln["price"],
                unit_price_per_ml=unit,
            ))

        db.commit()
        db.refresh(receipt)

    return {"id": receipt.id, "filename": receipt.filename, "lines": len(parsed_lines)}


@app.get("/receipts/{receipt_id}", response_model=dict)
def get_receipt(receipt_id: int):
    with SessionLocal() as db:
        r = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Not found")

        raw_lines = db.query(ReceiptLine).filter(ReceiptLine.receipt_id == receipt_id).all()
        products = db.query(ProductLine).filter(ProductLine.receipt_id == receipt_id).all()

        return {
            "id": r.id,
            "filename": r.filename,
            "uploaded_at": r.uploaded_at,
            "mimetype": r.mimetype,
            "ocr_raw": r.ocr_raw,
            "lines": [x.line_text for x in raw_lines],
            "products": [
                {
                    "name": p.name,
                    "raw_size": p.raw_size,
                    "size_ml": p.normalized_size_ml,
                    "price": p.price,
                    "unit_price_per_ml": p.unit_price_per_ml,
                }
                for p in products
            ],
        }

