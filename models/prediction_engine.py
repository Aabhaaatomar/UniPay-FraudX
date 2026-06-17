class PredictionEngine:

    def __init__(self, model):
        self.model = model

    def validate_input(self, amount, txn_count, hour):

        errors = []

        if amount <= 0:
            errors.append("amount must be greater than 0")

        if txn_count < 0:
            errors.append("transaction count cannot be negative")

        if hour < 0 or hour > 23:
            errors.append("hour must be between 0 and 23")

        return errors

    def calculate_risk_score(self, amount, txn_count, hour):

        score = 0
        reasons = []

        if amount > 10000:
            score += 50
            reasons.append("high transaction amount")

        if txn_count > 10:
            score += 30
            reasons.append("high transaction velocity")

        if 0 <= hour <= 5 and amount > 4000:
            score += 20
            reasons.append("late night transaction")

        return score, reasons

    def predict(self, amount, txn_count, hour):

        errors = self.validate_input(
            amount,
            txn_count,
            hour
        )

        if errors:
            return {
                "success": False,
                "errors": errors
            }

        ml_prediction = self.model.predict(
            [[amount, txn_count, hour]]
        )[0]

        ml_proba = self.model.predict_proba(
            [[amount, txn_count, hour]]
        )[0][1]

        risk_score, reasons = self.calculate_risk_score(
            amount,
            txn_count,
            hour
        )

        final_score = (
            ml_proba * 70
            +
            risk_score * 0.30
        )

        if final_score >= 70:
            risk_level = "HIGH"
            is_fraud = True

        elif final_score >= 40:
            risk_level = "MEDIUM"
            is_fraud = bool(ml_prediction)

        else:
            risk_level = "LOW"
            is_fraud = bool(ml_prediction)
        
        if not reasons:
            reasons.append(
                "no suspicious rule triggered"
                )
        recommendation = (
            "review_transaction"
            if is_fraud
            else "allow_transaction"
            )

        return {
            "success": True,
            "prediction": is_fraud,
            "risk_score": round(final_score),
            "confidence": ml_proba * 100,
            "risk_level": risk_level,
            "reasons": reasons,
            "recommendation": recommendation
        }