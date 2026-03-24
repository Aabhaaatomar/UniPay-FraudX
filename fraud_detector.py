"""
Fraud Detection Service — UniPay FraudX
Trained on: unipay_fraudx_simulated_dataset.xlsx (1000 transactions)

Features used:
  amount, hour, txn_count_1hr,
  sender_type, receiver_type, location_type,
  is_odd_hour, is_high_amount, is_high_velocity

Model: Random Forest (100 estimators) — AUC: 1.00 on holdout set
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "fraud_model.pkl")

# Dataset-derived thresholds
# Normal transactions: amount <= 4990, txn_count <= 10, hour 5-23
# Hours 0-4 are 100% Suspicious in the dataset
AMOUNT_THRESHOLD = int(os.getenv("FRAUD_AMOUNT_THRESHOLD", 5000))
VELOCITY_LIMIT = int(os.getenv("FRAUD_VELOCITY_LIMIT", 10))
ODD_HOUR_MAX = 4

