import pytest
from datetime import datetime, timedelta
from voucher import generate_voucher_code, determine_voucher_details, create_voucher

def test_voucher_code_format():
    """Test that generated voucher codes follow the correct format."""
    code = generate_voucher_code()
    assert code.startswith('BDAY-')
    assert len(code) == 15  # BDAY- + 10 characters
    assert all(c.isalnum() for c in code[5:])  # All characters after BDAY- are alphanumeric

def test_voucher_details():
    """Test voucher amount and validity calculations."""
    # Test cases below minimum threshold
    assert determine_voucher_details(0) == (0, 0)
    assert determine_voucher_details(999) == (0, 0)
    
    # Test basic tier (100 GHS, 1 day)
    assert determine_voucher_details(1000) == (100, 1)
    assert determine_voucher_details(4999) == (100, 1)
    
    # Test premium tier (500 GHS, 5 days)
    assert determine_voucher_details(5000) == (500, 5)
    assert determine_voucher_details(9999) == (500, 5)
    
    # Test elite tier (1000 GHS, 10 days)
    assert determine_voucher_details(10000) == (1000, 10)
    assert determine_voucher_details(15000) == (1000, 10)

def test_create_voucher():
    """Test voucher creation with all fields."""
    customer_id = "1"
    first_name = "John"
    order_value = 5000
    
    voucher = create_voucher(customer_id, first_name, order_value)
    
    assert voucher is not None
    assert voucher['Customer ID'] == customer_id
    assert voucher['First Name'] == first_name
    assert voucher['Order Value'] == float(order_value)
    assert voucher['Voucher Amount'] == 500
    assert voucher['Validity Days'] == 5
    assert voucher['Voucher Code'].startswith('BDAY-')
    
    # Check expiry date format and calculation
    expiry_date = datetime.strptime(voucher['Expiry Date'], '%Y-%m-%d').date()
    expected_date = datetime.now().date() + timedelta(days=5)
    assert expiry_date == expected_date

def test_create_voucher_ineligible():
    """Test voucher creation for ineligible customer."""
    voucher = create_voucher("1", "John", 500)
    assert voucher is None
