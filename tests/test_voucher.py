import re
import random
from datetime import date

import pytest

from voucher import determine_voucher, calculate_expiry_date, generate_voucher_code


def test_determine_voucher_boundaries():
    assert determine_voucher(999.99) is None
    assert determine_voucher(1000) == (100, 1)
    assert determine_voucher(4999.99) == (100, 1)

    assert determine_voucher(5000) == (500, 5)
    assert determine_voucher(9999.99) == (500, 5)

    assert determine_voucher(10000) == (1000, 10)
    assert determine_voucher(15000) == (1000, 10)


def test_calculate_expiry_date():
    base = date(2024, 2, 27)
    assert calculate_expiry_date(1, today=base) == date(2024, 2, 28)
    assert calculate_expiry_date(2, today=base) == date(2024, 2, 29)  # leap year handling
    assert calculate_expiry_date(3, today=base) == date(2024, 3, 1)


def test_generate_voucher_code_format_and_determinism():
    rng = random.Random(123)
    code = generate_voucher_code(rng)
    assert re.fullmatch(r"BDAY-[A-Z0-9]{10}", code)

    # Deterministic with seed
    rng2 = random.Random(123)
    assert generate_voucher_code(rng2) == code


def test_generate_voucher_code_uniqueness():
    codes = {generate_voucher_code() for _ in range(2000)}
    # Low collision probability; ensure no duplicates in this sample
    assert len(codes) == 2000