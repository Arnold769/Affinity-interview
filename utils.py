from __future__ import annotations

import csv
import io
from datetime import date, timedelta
from typing import Iterable, Tuple, List, Dict

from voucher import determine_voucher, generate_voucher_code


def map_header_to_fields(headers: list[str]) -> Tuple[str | None, str | None, str | None]:
    header_map = { (h or '').strip().lower(): (h or '') for h in headers }

    def find(*candidates: str) -> str | None:
        for c in candidates:
            if c in header_map:
                return header_map[c]
        return None

    customer_id_h = find("customer id", "id", "customer_id", "customerid")
    first_name_h = find("customer first name", "first name", "firstname", "name", "first_name")
    order_value_h = find(
        "order value",
        "orders value",
        "order amount",
        "amount",
        "total spent",
        "total_spent",
        "spent",
        "spend",
        "order_value",
        "ordervalue",
    )

    return customer_id_h, first_name_h, order_value_h


def generate_vouchers_from_csv(text: str, today: date | None = None) -> List[Dict[str, object]]:
    if today is None:
        today = date.today()

    input_stream = io.StringIO(text)
    reader = csv.reader(input_stream)

    try:
        headers = next(reader)
    except StopIteration:
        raise ValueError("CSV file is empty.")

    if not headers:
        raise ValueError("CSV appears to have no header row.")

    customer_id_h, first_name_h, order_value_h = map_header_to_fields(headers)
    if not (customer_id_h and first_name_h and order_value_h):
        raise ValueError("CSV must include columns for Customer ID, Customer First Name, and Order Value.")

    input_stream.seek(0)
    dict_reader = csv.DictReader(input_stream)

    vouchers: list[dict[str, object]] = []
    existing_codes: set[str] = set()

    for row in dict_reader:
        if not row:
            continue
        raw_id = (row.get(customer_id_h) or "").strip()
        raw_name = (row.get(first_name_h) or "").strip()
        raw_value = (row.get(order_value_h) or "").strip()

        try:
            value = float(raw_value.replace(",", "")) if raw_value != "" else None
        except ValueError:
            # Skip invalid numeric values
            continue

        rule = determine_voucher(value)
        if not rule:
            continue

        amount, validity_days = rule
        expiry_date = today + timedelta(days=validity_days)
        code = generate_voucher_code(existing_codes)

        vouchers.append(
            {
                "Customer ID": raw_id,
                "Customer First Name": raw_name,
                "Order Value": value if value is not None else "",
                "Voucher Code": code,
                "Voucher Amount": amount,
                "Validity Days": validity_days,
                "Expiry Date": expiry_date.isoformat(),
            }
        )

    return vouchers


def vouchers_to_csv(vouchers: List[Dict[str, object]]) -> str:
    output_stream = io.StringIO()
    fieldnames = [
        "Customer ID",
        "Customer First Name",
        "Order Value",
        "Voucher Code",
        "Voucher Amount",
        "Validity Days",
        "Expiry Date",
    ]
    writer = csv.DictWriter(output_stream, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(vouchers)
    return output_stream.getvalue()