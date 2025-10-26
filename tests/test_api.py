import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "models_loaded": True,
        "timestamp": response.json()["timestamp"]
    }

def test_predict_fraud():
    test_transaction = {
        "transaction_id": "TXN_TEST_001",
        "customer_id": 1,
        "device_id": 1,
        "amount": 75000.0,
        "channel": "mobile",
        "timestamp": "2024-10-26 02:30:00"
    }
    
    response = client.post("/predict", json=test_transaction)
    assert response.status_code == 200
    assert "risk_score" in response.json()
    assert "is_high_risk" in response.json()
    assert response.json()["transaction_id"] == test_transaction["transaction_id"]