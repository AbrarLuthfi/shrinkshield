# backend/app/ocr/adapter.py
from typing import Dict, List

class OCRAdapter:
    """
    Minimal OCR abstraction.
    - Today: naive text extraction (placeholder).
    - Later: swap to HuggingFace model (Donut/TrOCR) in this class.
    """

    def extract_lines(self, content: bytes) -> List[Dict]:
        # Day-4: structured items
        return [
            {"name": "Distilled Water", "size": "1 L",     "price": 1.29},
            {"name": "Sparkling Water", "size": "500 mL",  "price": 0.99},
        ]

    def __init__(self):
        # put model init here when you add HF model
        pass


    def extract(self, content: bytes, mimetype: str) -> Dict[str, List[str]]:
        # still keep a Day-3 style stub for compatibility
        return {"lines": ["Distilled Water 1 L $1.29", "Sparkling Water 500 mL $0.99"]}
