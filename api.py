from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import logging
from typing import Optional

# Initialize FastAPI
app = FastAPI(title="Sentinel AI Fraud Detection API", version="1.0.0")

# Mock model for immediate deployment (replace with trained model later)
class MockFraudDetector:
    def predict(self, features):
        # Simple rule-based risk scoring for immediate deployment
        risk_score = 0.1  # base risk
        
        # Amount-based risk
        if features.get('amount', 0) > 10000:
            risk_score += 0.3
        if features.get('bvn_age_hours', 720) < 48:  # Fresh BVN
            risk_score += 0.4
        if features.get('device_mismatch', False):
            risk_score += 0.2
        if features.get('odd_hour', False):
            risk_score += 0.1
            
        return min(0.99, risk_score), {
            "amount_risk": 0.3 if features.get('amount', 0) > 10000 else 0,
            "bvn_timing_risk": 0.4 if features.get('bvn_age_hours', 720) < 48 else 0,
            "device_risk": 0.2 if features.get('device_mismatch', False) else 0,
            "time_risk": 0.1 if features.get('odd_hour', False) else 0
        }

# Initialize detector
detector = MockFraudDetector()

# Request/Response models
class TransactionRequest(BaseModel):
    transaction_id: str
    customer_id: int
    amount: float
    currency: str = "NGN"
    channel: str
    device_id: int
    beneficiary_id: int
    timestamp: str
    ip_address: str
    country: str
    city: str
    txn_type: str

class FraudPrediction(BaseModel):
    transaction_id: str
    risk_score: float
    recommendation: str
    explanation: dict
    features_used: list

@app.get("/")
async def root():
    return {"message": "Sentinel AI Fraud Detection API", "status": "active"}

@app.post("/predict", response_model=FraudPrediction)
async def predict_fraud(transaction: TransactionRequest):
    try:
        # Feature engineering (mimic what we'll do with real model)
        features = {
            'amount': transaction.amount,
            'bvn_age_hours': 24,  # Mock - assume fresh BVN for demo
            'device_mismatch': False,  # Mock - would check device ownership
            'odd_hour': self._is_odd_hour(transaction.timestamp),
            'channel': transaction.channel,
            'txn_type': transaction.txn_type
        }
        
        # Get prediction
        risk_score, explanation = detector.predict(features)
        
        # Determine recommendation
        if risk_score > 0.8:
            recommendation = "BLOCK"
        elif risk_score > 0.5:
            recommendation = "REVIEW"
        else:
            recommendation = "ALLOW"
        
        return FraudPrediction(
            transaction_id=transaction.transaction_id,
            risk_score=round(risk_score, 3),
            recommendation=recommendation,
            explanation=explanation,
            features_used=list(features.keys())
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

def _is_odd_hour(timestamp_str: str) -> bool:
    """Check if transaction is at odd hours (10PM - 6AM)"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        hour = dt.hour
        return hour < 6 or hour >= 22
    except:
        return False

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Sample data endpoint for frontend testing
@app.get("/sample-transaction")
async def get_sample_transaction():
    return {
        "transaction_id": "txn_001",
        "customer_id": 123,
        "amount": 15000.0,
        "currency": "NGN", 
        "channel": "mobile",
        "device_id": 45,
        "beneficiary_id": 89,
        "timestamp": "2024-01-15T03:30:00Z",  # Odd hour - high risk
        "ip_address": "192.168.1.100",
        "country": "Nigeria",
        "city": "Lagos",
        "txn_type": "transfer"
    }