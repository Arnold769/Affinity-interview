import logging
from flask import Flask, render_template, request, send_file
from io import StringIO, BytesIO
from csv_utils import process_csv, generate_output_csv, CSVValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Render the main page with file upload form."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Process uploaded CSV file and generate vouchers.
    
    Returns:
        On success: CSV file download with voucher details
        On error: Error message with appropriate HTTP status code
    """
    try:
        # Validate file presence
        if 'file' not in request.files:
            logger.warning('No file uploaded')
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            logger.warning('No file selected')
            return 'No file selected', 400
        
        # Validate file type
        if not file.filename.endswith('.csv'):
            logger.warning('Invalid file type uploaded')
            return 'Please upload a CSV file', 400
        
        # Process the CSV file and generate vouchers
        logger.info(f'Processing file: {file.filename}')
        output_data = process_csv(file)
        
        if not output_data:
            logger.info('No eligible customers found in the uploaded file')
            return 'No eligible customers found in the uploaded file', 400
        
        # Generate output CSV
        output = generate_output_csv(output_data)
        
        # Convert to binary mode for send_file
        binary_output = BytesIO()
        binary_output.write(output.getvalue().encode('utf-8'))
        binary_output.seek(0)
        
        logger.info(f'Successfully generated vouchers for {len(output_data)} customers')
        return send_file(
            binary_output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='vouchers.csv'
        )
        
    except CSVValidationError as e:
        logger.error(f'CSV validation error: {str(e)}')
        return str(e), 400
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return 'An unexpected error occurred', 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)