from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    ocr_raw = Column(JSONB)  # optional

    # ---- relationships (names MUST match back_populates on the child) ----
    lines = relationship(
        "ReceiptLine",
        back_populates="receipt",
        cascade="all, delete-orphan",
    )
    products = relationship(
        "ProductLine",
        back_populates="receipt",
        cascade="all, delete-orphan",
    )


class ReceiptLine(Base):
    __tablename__ = "receipt_lines"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="CASCADE"), index=True, nullable=False)
    line_text = Column(String, nullable=False)

    # must point back to Receipt.lines
    receipt = relationship("Receipt", back_populates="lines")


class ProductLine(Base):
    __tablename__ = "product_lines"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="CASCADE"), index=True, nullable=False)
    name = Column(String, nullable=False)
    raw_size = Column(String)
    normalized_size_ml = Column(Numeric)     # or Float if you prefer
    price = Column(Numeric)                  # or Float
    unit_price_per_ml = Column(Numeric)      # or Float

    # must point back to Receipt.products
    receipt = relationship("Receipt", back_populates="products")

