from flask import Flask, render_template, request, Response

from utils import process_csv

app = Flask(__name__)


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

        try:
            csv_bytes = process_csv(content)
        except ValueError as e:
            return str(e), 400

        return Response(
            csv_bytes,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=vouchers.csv'}
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
