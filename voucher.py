from __future__ import annotations
from datetime import date, timedelta
import random
import string
from typing import Optional, Tuple


def determine_voucher(order_value: float) -> Optional[Tuple[int, int]]:
    """Return (voucher_amount, validity_days) or None if not eligible."""
    if 1000 <= order_value < 5000:
        return 100, 1
    if 5000 <= order_value < 10000:
        return 500, 5
    if order_value >= 10000:
        return 1000, 10
    return None


def generate_voucher_code(rng: random.Random | None = None) -> str:
    """Generate a voucher code in the format BDAY-XXXXXXXXXX.

    rng parameter allows deterministic testing when provided.
    """
    chooser = (rng or random).choices
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(chooser(chars, k=10))
    return f"BDAY-{random_part}"


def calculate_expiry_date(validity_days: int, *, today: date | None = None) -> date:
    base = today or date.today()
    return base + timedelta(days=validity_days)