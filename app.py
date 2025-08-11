from flask import Flask, render_template, request, Response
import csv
import io
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)


def determine_voucher(order_value: float):
    if 1000 <= order_value < 5000:
        return 100, 1
    if 5000 <= order_value < 10000:
        return 500, 5
    if order_value >= 10000:
        return 1000, 10
    return None


def generate_voucher_code() -> str:
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=10))
    return f"BDAY-{random_part}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        try:
            content = file.stream.read().decode('utf-8', errors='ignore')
        except Exception:
            return 'Could not read file', 400

        input_stream = io.StringIO(content)
        reader = csv.DictReader(input_stream)

        required_columns = {'Customer ID', 'First Name', 'Order Value'}
        if not required_columns.issubset(reader.fieldnames or []):
            return 'Invalid CSV headers. Expected: Customer ID, First Name, Order Value', 400

        output_stream = io.StringIO()
        writer = csv.writer(output_stream)
        writer.writerow(['Customer ID', 'First Name', 'Order Value', 'Voucher Code', 'Voucher Amount', 'Validity Days', 'Expiry Date'])

        today = datetime.utcnow().date()

        for row in reader:
            try:
                customer_id = row.get('Customer ID', '').strip()
                first_name = row.get('First Name', '').strip()
                order_value_str = row.get('Order Value', '').strip()
                order_value = float(order_value_str)
            except Exception:
                continue

            result = determine_voucher(order_value)
            if result is None:
                continue

            voucher_amount, validity_days = result
            voucher_code = generate_voucher_code()
            expiry_date = today + timedelta(days=validity_days)

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
        csv_bytes = output_stream.getvalue().encode('utf-8')
        return Response(
            csv_bytes,
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=vouchers.csv'
            }
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
