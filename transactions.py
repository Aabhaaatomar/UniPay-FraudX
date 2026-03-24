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


