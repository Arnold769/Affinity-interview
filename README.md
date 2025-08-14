# Birthday Voucher Generator

A Flask web application that generates birthday vouchers based on customer order values. Built for Affinity Ghana Savings & Loans Limited assessment.

## Features

- CSV file upload for customer data processing
- Automatic voucher generation based on order value tiers
- Unique voucher code generation (BDAY-XXXXXXXXXX format)
- Downloadable CSV output with voucher details
- Modern, responsive web interface
- Comprehensive input validation
- Production-ready error handling and logging

## Voucher Rules

| Order Value Range | Voucher Amount | Validity Period |
|------------------|----------------|-----------------|
| 1,000 - 4,999    | 100 GHS        | 1 day          |
| 5,000 - 9,999    | 500 GHS        | 5 days         |
| 10,000+          | 1,000 GHS      | 10 days        |

## Technical Requirements

- Python 3.9+
- Flask 3.0.2
- pytest (for running tests)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Arnold769/Affinity-interview.git
   cd Affinity-interview
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and visit:
   ```
   http://localhost:5001
   ```

## Testing

Run the test suite:
```bash
pytest
```

## Input Format

The application expects a CSV file with the following columns:
- Customer ID
- First Name
- Order Value

Example:
```csv
Customer ID,First Name,Order Value
1,John,1500
2,Mary,6000
3,Peter,12000
```

## Output Format

The generated CSV will contain:
- Customer ID
- First Name
- Order Value
- Voucher Code
- Voucher Amount
- Validity Days
- Expiry Date

## Project Structure

```
.
├── app.py              # Flask application and routes
├── voucher.py         # Voucher generation logic
├── csv_utils.py       # CSV processing utilities
├── requirements.txt   # Project dependencies
├── templates/         # HTML templates
│   └── index.html    # Upload form and interface
└── tests/            # Test suite
    ├── test_app.py
    ├── test_csv_utils.py
    └── test_voucher.py
```

## Production Considerations

- The application includes logging for production monitoring
- Input validation and error handling are implemented
- Tests cover core functionality and edge cases
- The interface is responsive and user-friendly

## Author

Arnold Aryeequaye