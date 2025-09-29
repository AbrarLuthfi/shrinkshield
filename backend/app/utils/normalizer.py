import re

_SIZE_RE = re.compile(r'(\d+(?:\.\d+)?)\s*(ml|mL|l|L|oz|OZ)\b')

def normalize_size(size_str: str) -> float | None:
    """
    Convert a human size string like '1 L', '500 mL', '16 oz' to milliliters (float).
    Returns None if we can't parse.
    """
    if not size_str:
        return None
    m = _SIZE_RE.search(size_str)
    if not m:
        return None
    qty = float(m.group(1))
    unit = m.group(2).lower()
    if unit == "l":
        qty *= 1000.0
    elif unit == "oz":
        qty *= 29.5735
    # ml stays as-is
    return qty
