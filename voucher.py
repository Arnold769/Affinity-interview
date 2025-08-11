import random
import string
from datetime import datetime, timedelta

def generate_voucher_code():
    """Generate a random 10-character voucher code."""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=10))
    return f"BDAY-{random_part}"

def determine_voucher_details(order_value):
    """Determine voucher amount and validity based on order value.
    
    Rules:
    - Orders between 1000-5000: 100 GHS voucher, valid for 1 day
    - Orders between 5000-10000: 500 GHS voucher, valid for 5 days
    - Orders 10000 and above: 1000 GHS voucher, valid for 10 days
    """
    order_value = float(order_value)
    
    if order_value >= 10000:
        return 1000, 10
    elif 5000 <= order_value < 10000:
        return 500, 5
    elif 1000 <= order_value < 5000:
        return 100, 1
    else:
        return 0, 0

def create_voucher(customer_id, first_name, order_value):
    """Create a voucher for a customer if they are eligible."""
    voucher_amount, validity_days = determine_voucher_details(order_value)
    
    if voucher_amount > 0:  # Customer is eligible for a voucher
        today = datetime.now().date()
        expiry_date = today + timedelta(days=validity_days)
        
        return {
            'Customer ID': customer_id,
            'First Name': first_name,
            'Order Value': float(order_value),
            'Voucher Code': generate_voucher_code(),
            'Voucher Amount': voucher_amount,
            'Validity Days': validity_days,
            'Expiry Date': expiry_date.strftime('%Y-%m-%d')
        }
    
    return None
