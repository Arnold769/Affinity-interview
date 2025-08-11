# Rewarder (Minimal Flask App)

A minimal Flask app that reads a CSV of customers and order values, applies voucher rules, and returns a downloadable CSV of eligible vouchers.

## Requirements
- Python 3.9+

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running Locally
```bash
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
```
Then open http://localhost:5000 in your browser.

## Tests
```bash
pytest -q
```

## Usage
- Prepare a CSV with headers: `Customer ID, First Name, Order Value`.
- Navigate to `/` and upload the CSV.
- The app will return a CSV download with columns:
  - `Customer ID, First Name, Order Value, Voucher Code, Voucher Amount, Validity Days, Expiry Date`

## Voucher Rules
- 1000 <= Order Value < 5000 → amount 100, validity 1 day
- 5000 <= Order Value < 10000 → amount 500, validity 5 days
- Order Value >= 10000 → amount 1000, validity 10 days

## Notes
- No database or authentication; all processing is in-memory using Python's built-in `csv`.
- Voucher codes are generated as `BDAY-XXXXXXXXXX` (10 random uppercase letters/digits).