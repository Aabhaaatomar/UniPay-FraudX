import pickle
from models.prediction_engine import PredictionEngine

model = pickle.load(
    open("fraud_model.pkl", "rb")
)

engine = PredictionEngine(model)

def test_valid_prediction():

    result = engine.predict(
        1000,
        2,
        12
    )

    assert result["success"] == True


def test_invalid_amount():

    result = engine.predict(
        -100,
        2,
        12
    )

    assert result["success"] == False


def test_high_risk_transaction():

    result = engine.predict(
        50000,
        20,
        2
    )

    assert result["prediction"] == True