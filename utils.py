from __future__ import annotations
import csv
import io
from datetime import datetime
from typing import Iterable, Dict

from voucher import determine_voucher, generate_voucher_code, calculate_expiry_date

REQUIRED_COLUMNS = {'Customer ID', 'First Name', 'Order Value'}


def validate_headers(fieldnames: Iterable[str] | None) -> bool:
    return REQUIRED_COLUMNS.issubset(set(fieldnames or []))


def process_csv(content: str) -> bytes:
    """Process input CSV content and return output CSV bytes.

    Input columns: Customer ID, First Name, Order Value
    Output columns: Customer ID, First Name, Order Value, Voucher Code, Voucher Amount, Validity Days, Expiry Date
    """
    input_stream = io.StringIO(content)
    reader = csv.DictReader(input_stream)

    if not validate_headers(reader.fieldnames):
        raise ValueError('Invalid CSV headers. Expected: Customer ID, First Name, Order Value')

    output_stream = io.StringIO()
    writer = csv.writer(output_stream)
    writer.writerow([
        'Customer ID', 'First Name', 'Order Value', 'Voucher Code',
        'Voucher Amount', 'Validity Days', 'Expiry Date'
    ])

    today = datetime.utcnow().date()

    for row in reader:
        try:
            customer_id = (row.get('Customer ID') or '').strip()
            first_name = (row.get('First Name') or '').strip()
            order_value_str = (row.get('Order Value') or '').strip()
            order_value = float(order_value_str)
        except Exception:
            continue

        result = determine_voucher(order_value)
        if result is None:
            continue

        voucher_amount, validity_days = result
        voucher_code = generate_voucher_code()
        expiry_date = calculate_expiry_date(validity_days, today=today)

        writer.writerow([
            customer_id,
            first_name,
            f"{order_value:.2f}",
            voucher_code,
            voucher_amount,
            validity_days,
            expiry_date.isoformat(),
        ])

    output_stream.seek(0)
    return output_stream.getvalue().encode('utf-8')