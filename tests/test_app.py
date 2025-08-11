import pytest
from app import app
from io import BytesIO

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Birthday Voucher Generator' in response.data

def test_process_valid_csv(client):
    """Test processing a valid CSV file."""
    data = {
        'file': (BytesIO(b'Customer ID,First Name,Order Value\n1,John,1500\n'), 'test.csv')
    }
    response = client.post('/process', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv'
    assert 'attachment' in response.headers['Content-Disposition']

def test_process_no_file(client):
    """Test error handling when no file is uploaded."""
    response = client.post('/process')
    assert response.status_code == 400
    assert b'No file uploaded' in response.data

def test_process_empty_filename(client):
    """Test error handling when filename is empty."""
    data = {
        'file': (BytesIO(b''), '')
    }
    response = client.post('/process', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'No file selected' in response.data

def test_process_invalid_file_type(client):
    """Test error handling when file is not a CSV."""
    data = {
        'file': (BytesIO(b'test content'), 'test.txt')
    }
    response = client.post('/process', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'Please upload a CSV file' in response.data
