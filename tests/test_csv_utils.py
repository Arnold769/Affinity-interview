import pytest
from io import StringIO, BytesIO
from csv_utils import process_csv, generate_output_csv

def create_test_file(content):
    """Helper function to create a file-like object with CSV content."""
    file = StringIO()
    file.write(content)
    file.seek(0)
    return type('TestFile', (), {'stream': BytesIO(file.getvalue().encode()), 'filename': 'test.csv'})

def test_process_csv():
    """Test CSV processing with various scenarios."""
    csv_content = (
        "Customer ID,First Name,Order Value\n"
        "1,John,500\n"
        "2,Mary,1500\n"
        "3,Peter,6000\n"
        "4,Sarah,12000\n"
    )
    
    test_file = create_test_file(csv_content)
    results = process_csv(test_file)
    
    assert len(results) == 3  # Should exclude the 500 order value
    
    # Verify first eligible customer (Mary)
    assert results[0]['Customer ID'] == '2'
    assert results[0]['First Name'] == 'Mary'
    assert results[0]['Order Value'] == 1500.0
    assert results[0]['Voucher Amount'] == 100
    assert results[0]['Validity Days'] == 1
    
    # Verify premium tier customer (Peter)
    assert results[1]['Customer ID'] == '3'
    assert results[1]['Voucher Amount'] == 500
    assert results[1]['Validity Days'] == 5
    
    # Verify elite tier customer (Sarah)
    assert results[2]['Customer ID'] == '4'
    assert results[2]['Voucher Amount'] == 1000
    assert results[2]['Validity Days'] == 10

def test_generate_output_csv():
    """Test CSV generation with sample data."""
    sample_data = [{
        'Customer ID': '1',
        'First Name': 'John',
        'Order Value': 1500.0,
        'Voucher Code': 'BDAY-1234567890',
        'Voucher Amount': 100,
        'Validity Days': 1,
        'Expiry Date': '2025-08-12'
    }]
    
    output = generate_output_csv(sample_data)
    output_str = output.getvalue()
    
    assert 'Customer ID,First Name,Order Value,Voucher Code,Voucher Amount,Validity Days,Expiry Date' in output_str
    assert '1,John,1500.0,BDAY-1234567890,100,1,2025-08-12' in output_str

def test_generate_output_csv_empty():
    """Test CSV generation with empty data."""
    output = generate_output_csv([])
    assert output.getvalue() == ''
