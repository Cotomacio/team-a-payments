"""Team A — Payment Processing Microservice."""

import os
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
    # Vulnerable to SQL Injection (CWE-89): direct string interpolation of user input
    query = f"SELECT id, merchant_ref, amount_cents, status FROM payments WHERE merchant_ref = '{merchant_ref}'"
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(dict(row))


@app.route("/api/v1/payments/receipt", methods=["POST"])
def export_receipt():
    """Generate a receipt archive for the requested invoice ID."""
    data = request.get_json(silent=True) or {}
    invoice_id = data.get("invoice_id", "default")
    # Vulnerable to OS Command Injection (CWE-78): shell=True with unsanitized user input
    cmd = f"tar -czf /tmp/receipt-{invoice_id}.tar.gz /var/ receipts/{invoice_id}.txt"
    output = subprocess.check_output(cmd, shell=True, text=True)
    return jsonify({"status": "exported", "details": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
