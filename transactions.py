import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from app import db
from app.models import Transaction, Blocklist
from app.services.fraud_detector import analyze_transaction
from app.services.alert_service import create_alert

transactions_bp = Blueprint("transactions", __name__)


def _get_blocklist_values():
    return {b.value for b in Blocklist.query.all()}


def _get_known_devices(user_id):
    txns = Transaction.query.filter_by(user_id=user_id).all()
    return {t.device_id for t in txns if t.device_id}


# ─────────────────────────────────────────────
# POST /api/transactions/submit
# ─────────────────────────────────────────────
@transactions_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_transaction():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    amount = data.get("amount")
    if amount is None or float(amount) <= 0:
        return jsonify({"error": "Valid positive amount is required"}), 400

    tx = Transaction(
        user_id=user_id,
        transaction_id=str(uuid.uuid4()),
        amount=float(amount),
        currency=data.get("currency", "USD"),
        merchant=data.get("merchant"),
        merchant_category=data.get("merchant_category"),
        location=data.get("location"),
        ip_address=request.remote_addr,
        device_id=data.get("device_id"),
        payment_method=data.get("payment_method", "card"),
        status="pending",
    )
    db.session.add(tx)
    db.session.flush()  # get ID without full commit

    # Gather context for fraud analysis
    ten_min_ago = datetime.utcnow() - timedelta(minutes=10)
    recent_txns = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.created_at >= ten_min_ago,
    ).all()

    blocklist_values = _get_blocklist_values()
    known_devices = _get_known_devices(user_id)

    result = analyze_transaction(tx, recent_txns, blocklist_values, known_devices)

    tx.is_fraud = result["is_fraud"]
    tx.fraud_score = result["fraud_score"]

    if result["recommendation"] == "BLOCK":
        tx.status = "blocked"
    elif result["recommendation"] == "FLAG_FOR_REVIEW":
        tx.status = "flagged"
    else:
        tx.status = "approved"

    db.session.commit()


