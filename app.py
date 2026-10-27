"""Team A — Payment Processing Microservice."""

import os
import re
import sqlite3
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = os.environ.get("PAYMENTS_DB", "/tmp/payments.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/v1/payments/lookup", methods=["GET"])
def lookup_payment():
    """Look up a payment record by external merchant reference."""
    merchant_ref = request.args.get("merchant_ref", "")
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, merchant_ref, amount_cents, status FROM payments WHERE merchant_ref = ?"
    cursor.execute(query, (merchant_ref,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(dict(row))


@app.route("/api/v1/payments/receipt", methods=["POST"])
def export_receipt():
    """Generate a receipt archive for the requested invoice ID."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        data = {}
    invoice_id = data.get("invoice_id", "default")
    if invoice_id is None:
        invoice_id = "default"
    if isinstance(invoice_id, int):
        invoice_id = str(invoice_id)
    if not isinstance(invoice_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", invoice_id):
        return jsonify({"error": "Invalid invoice_id"}), 400
    cmd = [
        "tar",
        "-czf",
        f"/tmp/receipt-{invoice_id}.tar.gz",
        "/var/",
        f"receipts/{invoice_id}.txt",
    ]
    output = subprocess.check_output(cmd, text=True)
    return jsonify({"status": "exported", "details": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
