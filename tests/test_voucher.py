import re
from voucher import determine_voucher, generate_voucher_code


def test_determine_voucher_ineligible_below_1000():
    assert determine_voucher(None) is None
    assert determine_voucher(0) is None
    assert determine_voucher(999.99) is None


def test_determine_voucher_100_tier():
    assert determine_voucher(1000) == (100, 1)
    assert determine_voucher(4999.99) == (100, 1)


def test_determine_voucher_500_tier():
    assert determine_voucher(5000) == (500, 5)
    assert determine_voucher(9999.99) == (500, 5)


def test_determine_voucher_1000_tier():
    assert determine_voucher(10000) == (1000, 10)
    assert determine_voucher(25000) == (1000, 10)


def test_generate_voucher_code_format_and_uniqueness():
    seen = set()
    codes = [generate_voucher_code(seen) for _ in range(100)]
    assert len(codes) == len(set(codes))  # all unique
    for code in codes:
        assert code.startswith("BDAY-")
        assert re.fullmatch(r"BDAY-[A-Z0-9]{10}", code)