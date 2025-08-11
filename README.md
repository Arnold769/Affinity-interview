# Rewarder - Birthday Voucher Generator

A simple Flask web application that generates birthday vouchers based on customer order values.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit: http://localhost:5000

## Usage

1. Prepare a CSV file with the following columns:
   - Customer ID
   - First Name
   - Order Value

2. Upload the CSV file using the web interface.

3. The application will process the file and generate a downloadable CSV containing voucher details for eligible customers.

## Voucher Rules

- Orders between 1,000 and 4,999: 100 GHS voucher, valid for 1 day
- Orders between 5,000 and 9,999: 500 GHS voucher, valid for 5 days
- Orders 10,000 and above: 1,000 GHS voucher, valid for 10 days

## Output Format

The generated CSV will contain:
- Customer ID
- First Name
- Order Value
- Voucher Code (Format: BDAY-XXXXXXXXXX)
- Voucher Amount
- Validity Days
- Expiry Date
