from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import numpy as np
import joblib
import pandas as pd

app = FastAPI(title="Sentinel AI Real-Time Fraud Detection")

class TransactionRequest(BaseModel):
    transaction_id: str
    customer_id: int
    device_id: int
    amount: float
    channel: str
    timestamp: str

class RealTimeFeatureEngine:
    def __init__(self, customers_df, devices_df, feature_columns):
        self.customers_df = customers_df.set_index('customer_id')
        self.devices_df = devices_df.set_index('device_id')
        self.feature_columns = feature_columns
        
    def engineer_features(self, transaction_data: Dict) -> np.array:
        customer_id = transaction_data['customer_id']
        device_id = transaction_data['device_id']
        amount = transaction_data['amount']
        channel = transaction_data['channel']
        timestamp = pd.to_datetime(transaction_data['timestamp'])
        
        customer_data = self.customers_df.loc[customer_id]
        device_data = self.devices_df.loc[device_id]
        
        features = []
        
        features.extend([
            amount,
            customer_data['customer_risk_level'],
            int(device_data['owner_customer_id'] != customer_id),
            int(amount > (5 * customer_data['avg_txn_amount'])),
            int(timestamp.hour <= 5 or timestamp.hour >= 23),
        ])
        
        channel_risk = {'ussd': 3, 'mobile': 2, 'agent': 2, 'web': 1, 'atm': 1}
        features.append(channel_risk.get(channel.lower(), 1))
        
        signup_date = pd.to_datetime(customer_data['signup_date'])
        tenure_days = (timestamp - signup_date).days
        features.append(int(tenure_days < 30))
        
        features.append(100)
        
        hour = timestamp.hour
        dow = timestamp.dayofweek
        features.extend([
            np.sin(2 * np.pi * hour / 24),
            np.cos(2 * np.pi * hour / 24),
            np.sin(2 * np.pi * dow / 7),
            np.cos(2 * np.pi * dow / 7),
        ])
        
        features.append(hash(device_data['ip_prefix']) % 10)
        
        features.extend([
            amount / max(customer_data['avg_txn_amount'], 1),
            np.log1p(amount)
        ])
        
        return np.array(features).reshape(1, -1)

# Load models and artifacts
artifacts = joblib.load('sentinel_ai_artifacts.pkl')
xgb_model = artifacts['xgb_model']
iso_model = artifacts['iso_model']
feature_scaler = artifacts['scaler']
feature_columns = artifacts['feature_columns']
feature_engine = RealTimeFeatureEngine(artifacts['customers'], artifacts['devices'], feature_columns)

@app.post("/predict", response_model=Dict[str, Any])
async def predict_fraud(request: TransactionRequest):
    try:
        tx_data = request.dict()
        features = feature_engine.engineer_features(tx_data)
        features_scaled = feature_scaler.transform(features)
        
        iso_score = iso_model.decision_function(features_scaled)[0]
        iso_risk = max(0, min(1, (1 - (iso_score + 0.5))))
        
        xgb_prob = xgb_model.predict_proba(features)[0, 1]
        
        ensemble_score = 0.3 * iso_risk + 0.7 * xgb_prob
        
        return {
            "transaction_id": request.transaction_id,
            "risk_score": round(ensemble_score, 4),
            "is_high_risk": ensemble_score > 0.7,
            "model_breakdown": {
                "isolation_forest_score": round(iso_risk, 4),
                "xgboost_score": round(xgb_prob, 4)
            },
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
    except Exception as e:
        return {"error": str(e), "risk_score": 0.5, "is_high_risk": False}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "models_loaded": True,
        "timestamp": pd.Timestamp.now().isoformat()
    }