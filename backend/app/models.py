from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func

from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    ocr_raw = Column(JSON, nullable=True)  # raw OCR output (JSON)
    store_name = Column(String, nullable=True)  # best-effort extracted in future
    purchase_date = Column(DateTime(timezone=True), nullable=True)  # best-effort

    lines = relationship("ReceiptLine", back_populates="receipt", cascade="all, delete-orphan")


class ReceiptLine(Base):
    __tablename__ = "receipt_lines"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="CASCADE"), index=True)
    line_text = Column(Text, nullable=False)
    # Day 4 will add: qty, size_str, size_value, size_unit, price_minor, unit_price_minor, product_id, etc.

    receipt = relationship("Receipt", back_populates="lines")
