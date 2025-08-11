from flask import Flask, render_template, request, send_file, flash
import io
import os
import secrets

from utils import generate_vouchers_from_csv, vouchers_to_csv

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Please choose a CSV file to upload.")
        return render_template("index.html"), 400

    try:
        text = file.stream.read().decode("utf-8-sig")
    except Exception:
        flash("Unable to read the uploaded file. Ensure it's a valid UTF-8 CSV.")
        return render_template("index.html"), 400

    try:
        vouchers = generate_vouchers_from_csv(text)
    except ValueError as e:
        flash(str(e))
        return render_template("index.html"), 400

    if not vouchers:
        flash("No eligible customers found based on the provided rules.")
        return render_template("index.html"), 200

    csv_text = vouchers_to_csv(vouchers)
    return send_file(
        io.BytesIO(csv_text.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="vouchers.csv",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
