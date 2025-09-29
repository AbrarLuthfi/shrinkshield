# backend/app/ocr/adapter.py
from typing import Dict, List

class OCRAdapter:
    """
    Minimal OCR abstraction.
    - Today: naive text extraction (placeholder).
    - Later: swap to HuggingFace model (Donut/TrOCR) in this class.
    """

    def __init__(self):
        # put model init here when you add HF model
        pass

    def extract(self, file_bytes: bytes, mimetype: str) -> Dict:
        """
        Returns a dict:
        {
          "lines": ["raw line 1", "raw line 2", ...],
          "meta": {...}
        }
        """
        # --- placeholder extraction ---
        # For images/PDFs we don't truly OCR yet; we return a single "blob" line.
        # This keeps API plumbing working so Day 4 can focus on normalization.
        # Replace with real OCR later.
        text = f"[placeholder OCR] bytes={len(file_bytes)} mimetype={mimetype}"
        return {"lines": [text], "meta": {"engine": "stub", "mimetype": mimetype}}

