import pickle
import numpy as np


def load_model(file_path="fraud_model.pkl"):
    try:
        with open(file_path, "rb") as f:
            model_data = pickle.load(f)

        print("Model loaded successfully")
        return model_data["model"], model_data["features"]

    except Exception as e:
        print("Error loading model:", e)
        return None, None


def predict_fraud(model, features, amount, txn_count, hour):
    try:
        # Arrange input in correct feature order
        input_data = np.array([[amount, txn_count, hour]])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        result = "🚨 Fraud Transaction" if prediction == 1 else "✅ Normal Transaction"

        return {
            "prediction": int(prediction),
            "result": result,
            "fraud_probability": round(float(probability), 4)
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    model, features = load_model()

    if model:
        # Example test input
        result = predict_fraud(model, features, amount=5000, txn_count=10, hour=2)
        print("\nPrediction Result:\n", result)
