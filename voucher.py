from __future__ import annotations

import secrets
import string
from typing import Optional, Tuple


def determine_voucher(order_value: Optional[float]) -> Optional[Tuple[int, int]]:
    """Return (amount, validity_days) or None if not eligible.

    Rules:
    - 100 for 1000 <= value < 5000 (1 day)
    - 500 for 5000 <= value < 10000 (5 days)
    - 1000 for value >= 10000 (10 days)
    - None otherwise
    """
    if order_value is None:
        return None
    if 1000 <= order_value < 5000:
        return 100, 1
    if 5000 <= order_value < 10000:
        return 500, 5
    if order_value >= 10000:
        return 1000, 10
    return None


def generate_voucher_code(existing_codes: set[str] | None = None) -> str:
    """Generate a unique voucher code with prefix 'BDAY-'.

    Uses uppercase letters and digits for a 10-character random part.
    If existing_codes is provided, ensures uniqueness by regenerating on collision.
    """
    if existing_codes is None:
        existing_codes = set()
    alphabet = string.ascii_uppercase + string.digits
    while True:
        random_part = ''.join(secrets.choice(alphabet) for _ in range(10))
        code = f"BDAY-{random_part}"
        if code not in existing_codes:
            existing_codes.add(code)
            return code