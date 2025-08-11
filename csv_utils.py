import csv
from io import StringIO
from typing import List, Dict, Optional
from voucher import create_voucher

class CSVValidationError(Exception):
    """Custom exception for CSV validation errors."""
    pass

def validate_csv_headers(headers: List[str]) -> None:
    """Validate that the CSV file has the required headers."""
    required_headers = {'Customer ID', 'First Name', 'Order Value'}
    missing_headers = required_headers - set(headers)
    if missing_headers:
        raise CSVValidationError(
            f"Missing required columns: {', '.join(missing_headers)}"
        )

def validate_row_data(row: Dict[str, str], row_number: int) -> None:
    """Validate individual row data."""
    # Check for empty values
    for field in ['Customer ID', 'First Name', 'Order Value']:
        if not row[field].strip():
            raise CSVValidationError(
                f"Empty {field} in row {row_number}"
            )
    
    # Validate Customer ID format
    if not row['Customer ID'].strip().isdigit():
        raise CSVValidationError(
            f"Invalid Customer ID in row {row_number}. Must be a number."
        )
    
    # Validate Order Value format
    try:
        order_value = float(row['Order Value'])
        if order_value < 0:
            raise CSVValidationError(
                f"Invalid Order Value in row {row_number}. Must be non-negative."
            )
    except ValueError:
        raise CSVValidationError(
            f"Invalid Order Value format in row {row_number}. Must be a number."
        )

def process_csv(file) -> List[Dict[str, any]]:
    """Process the input CSV and generate voucher details.
    
    Args:
        file: File object containing CSV data
        
    Returns:
        List of dictionaries containing voucher details for eligible customers
        
    Raises:
        CSVValidationError: If the CSV format is invalid or contains invalid data
    """
    try:
        # Read input CSV
        input_stream = StringIO(file.stream.read().decode("UTF-8"))
        csv_reader = csv.DictReader(input_stream)
        
        # Validate headers
        validate_csv_headers(csv_reader.fieldnames or [])
        
        # Process each row and generate vouchers
        output_data = []
        for row_number, row in enumerate(csv_reader, start=1):
            try:
                validate_row_data(row, row_number)
                voucher = create_voucher(
                    customer_id=row['Customer ID'],
                    first_name=row['First Name'],
                    order_value=row['Order Value']
                )
                if voucher:
                    output_data.append(voucher)
            except CSVValidationError as e:
                # Log the error but continue processing other rows
                print(f"Warning: {str(e)}")
                continue
                
        return output_data
        
    except UnicodeDecodeError:
        raise CSVValidationError("Invalid CSV file encoding. Please use UTF-8.")
    except csv.Error:
        raise CSVValidationError("Invalid CSV format.")

def generate_output_csv(data: List[Dict[str, any]]) -> StringIO:
    """Generate CSV file from voucher data.
    
    Args:
        data: List of dictionaries containing voucher details
        
    Returns:
        StringIO object containing the CSV data
    """
    output = StringIO()
    if not data:
        return output
        
    fieldnames = ['Customer ID', 'First Name', 'Order Value', 'Voucher Code', 
                  'Voucher Amount', 'Validity Days', 'Expiry Date']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
    output.seek(0)
    return output