from flask import Flask, render_template, request, send_file, flash
import csv
import io
from datetime import date, timedelta
import secrets
import string
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))


def determine_voucher(order_value: float):
    if order_value is None:
        return None
    if 1000 <= order_value < 5000:
        return 100, 1
    if 5000 <= order_value < 10000:
        return 500, 5
    if order_value >= 10000:
        return 1000, 10
    return None


def generate_voucher_code(existing_codes: set, customer_id: str) -> str:
    alphabet = string.ascii_uppercase + string.digits
    while True:
        random_part = ''.join(secrets.choice(alphabet) for _ in range(10))
        code = f"BDAY-{random_part}"
        if code not in existing_codes:
            existing_codes.add(code)
            return code


def normalize_headers(headers):
    normalized = {}
    for h in headers:
        key = (h or "").strip().lower()
        normalized[key] = h
    return normalized


def map_header_to_fields(headers: list[str]):
    # Map diverse possible header names to canonical keys
    header_map = {h.strip().lower(): h for h in headers}

    def find(*candidates):
        for c in candidates:
            if c in header_map:
                return header_map[c]
        return None

    customer_id_h = find("customer id", "id", "customer_id", "customerid")
    first_name_h = find(
        "customer first name",
        "first name",
        "firstname",
        "name",
        "first_name",
    )
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


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Please choose a CSV file to upload.")
        return render_template("index.html"), 400

    try:
        # Decode as UTF-8 with BOM support
        text = file.stream.read().decode("utf-8-sig")
    except Exception:
        flash("Unable to read the uploaded file. Ensure it's a valid UTF-8 CSV.")
        return render_template("index.html"), 400

    input_stream = io.StringIO(text)
    reader = csv.reader(input_stream)

    try:
        headers = next(reader)
    except StopIteration:
        flash("CSV file is empty.")
        return render_template("index.html"), 400

    if not headers:
        flash("CSV appears to have no header row.")
        return render_template("index.html"), 400

    # Map headers using original header row
    customer_id_h, first_name_h, order_value_h = map_header_to_fields(headers)

    if not (customer_id_h and first_name_h and order_value_h):
        flash(
            "CSV must include columns for Customer ID, Customer First Name, and Order Value."
        )
        return render_template("index.html"), 400

    # Prepare to read as DictReader for easier access
    input_stream.seek(0)
    dict_reader = csv.DictReader(input_stream)

    vouchers = []
    existing_codes = set()
    today = date.today()

    for row in dict_reader:
        if row is None:
            continue
        raw_id = (row.get(customer_id_h) or "").strip()
        raw_name = (row.get(first_name_h) or "").strip()
        raw_value = (row.get(order_value_h) or "").strip()

        try:
            value = float(raw_value.replace(",", "")) if raw_value != "" else None
        except ValueError:
            # skip invalid numeric values
            continue

        rule = determine_voucher(value)
        if not rule:
            # not eligible
            continue

        amount, validity_days = rule
        voucher_code = generate_voucher_code(existing_codes, raw_id)
        expiry_date = today + timedelta(days=validity_days)

        vouchers.append(
            {
                "Customer ID": raw_id,
                "Customer First Name": raw_name,
                "Order Value": value if value is not None else "",
                "Voucher Code": voucher_code,
                "Voucher Amount": amount,
                "Validity Days": validity_days,
                "Expiry Date": expiry_date.isoformat(),
            }
        )

    if not vouchers:
        flash("No eligible customers found based on the provided rules.")
        return render_template("index.html"), 200

    # Create CSV in memory
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

    output_stream.seek(0)
    filename = f"vouchers_{today.isoformat()}.csv"
    return send_file(
        io.BytesIO(output_stream.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
