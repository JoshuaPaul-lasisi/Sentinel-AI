from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# Initialize FastAPI with production settings
app = FastAPI(
    title="Sentinel AI Fraud Detection API",
    description="Real-time fraud detection for African financial transactions",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for loaded models
MODELS_LOADED = False
xgb_model = None
iso_model = None
feature_scaler = None
shap_explainer = None
feature_columns = None
customers_df = None
devices_df = None

@app.on_event("startup")
async def load_models():
    """Load ML models on startup - runs once when API starts"""
    global MODELS_LOADED, xgb_model, iso_model, feature_scaler, shap_explainer, feature_columns, customers_df, devices_df
    
    try:
        # Load your pre-trained artifacts
        artifacts = joblib.load('sentinel_ai_artifacts.pkl')
        
        xgb_model = artifacts['xgb_model']
        iso_model = artifacts['iso_model']
        feature_scaler = artifacts['scaler']
        shap_explainer = artifacts['shap_explainer']
        feature_columns = artifacts['feature_columns']
        customers_df = artifacts['customers_df']
        devices_df = artifacts['devices_df']
        
        MODELS_LOADED = True
        print("ML Models loaded successfully")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        # Fallback: train simple model if artifacts not found
        await train_fallback_model()

async def train_fallback_model():
    """Train a simple fallback model if main models fail to load"""
    global MODELS_LOADED, xgb_model, feature_scaler, feature_columns
    
    try:
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
        
        # Simple fallback features
        feature_columns = ['amount', 'hour', 'is_mobile', 'is_high_amount']
        
        # Mock training data
        X_train = np.random.randn(1000, 4)
        feature_scaler = StandardScaler()
        X_scaled = feature_scaler.fit_transform(X_train)
        
        xgb_model = IsolationForest(contamination=0.05, random_state=42)
        xgb_model.fit(X_scaled)
        
        MODELS_LOADED = True
        print("Fallback model trained successfully")
        
    except Exception as e:
        print(f"Fallback model failed: {e}")

class TransactionRequest(BaseModel):
    transaction_id: str
    customer_id: int
    device_id: int
    amount: float
    channel: str
    timestamp: str
    # Optional: Add more fields as needed

class PredictionResponse(BaseModel):
    transaction_id: str
    risk_score: float
    is_high_risk: bool
    model_breakdown: Dict[str, float]
    explanation: Optional[Dict[str, Any]]
    timestamp: str
    api_version: str = "1.0.0"

class RealTimeFeatureEngine:
    """Production-ready feature engineering"""
    
    def __init__(self, customers_df, devices_df, feature_columns):
        self.customers_df = customers_df.set_index('customer_id')
        self.devices_df = devices_df.set_index('device_id')
        self.feature_columns = feature_columns
        
    def engineer_features(self, transaction_data: Dict) -> np.array:
        try:
            customer_id = transaction_data['customer_id']
            device_id = transaction_data['device_id']
            amount = transaction_data['amount']
            channel = transaction_data['channel']
            timestamp = pd.to_datetime(transaction_data['timestamp'])
            
            # Get customer data with error handling
            try:
                customer_data = self.customers_df.loc[customer_id]
                avg_txn_amount = customer_data['avg_txn_amount']
                customer_risk = customer_data['customer_risk_level']
            except KeyError:
                # New customer - use defaults
                avg_txn_amount = 1000.0
                customer_risk = 3  # Medium risk for new customers
            
            # Get device data with error handling
            try:
                device_data = self.devices_df.loc[device_id]
                device_owner = device_data['owner_customer_id']
            except KeyError:
                device_owner = None
            
            # Feature engineering
            features = []
            
            # 1. Core features
            features.extend([
                float(amount),
                float(customer_risk),
                int(device_owner != customer_id) if device_owner is not None else 1,  # device_mismatch
                int(amount > (5 * avg_txn_amount)),  # high_amount
                int(timestamp.hour <= 5 or timestamp.hour >= 23),  # odd_hour
            ])
            
            # 2. Channel encoding
            channel_risk = {'ussd': 3, 'mobile': 2, 'agent': 2, 'web': 1, 'atm': 1}
            features.append(channel_risk.get(channel.lower(), 1))
            
            # 3. Customer behavior (simplified for real-time)
            features.append(0)  # is_new_customer - would come from real-time DB
            features.append(100)  # historical_tx_count - would come from real-time counter
            
            # 4. Time features
            hour = timestamp.hour
            dow = timestamp.dayofweek
            features.extend([
                float(np.sin(2 * np.pi * hour / 24)),
                float(np.cos(2 * np.pi * hour / 24)),
                float(np.sin(2 * np.pi * dow / 7)),
                float(np.cos(2 * np.pi * dow / 7)),
            ])
            
            # 5. Additional features
            features.extend([
                5,  # ip_risk - placeholder
                float(amount / max(avg_txn_amount, 1)),  # amount_to_avg_ratio
                float(np.log1p(amount))  # amount_log
            ])
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            print(f"Feature engineering error: {e}")
            # Return safe default features
            return np.array([[1000.0, 2, 0, 0, 0, 1, 0, 100, 0, 1, 0, 1, 5, 1, 6.9]])

# Initialize feature engine after models are loaded
feature_engine = None

@app.get("/")
async def root():
    return {
        "message": "Sentinel AI Fraud Detection API",
        "status": "operational" if MODELS_LOADED else "initializing",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if MODELS_LOADED else "degraded",
        "models_loaded": MODELS_LOADED,
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_fraud(request: TransactionRequest):
    """Production fraud prediction endpoint"""
    if not MODELS_LOADED:
        raise HTTPException(status_code=503, detail="Models are still loading")
    
    try:
        # Initialize feature engine if not done
        global feature_engine
        if feature_engine is None:
            feature_engine = RealTimeFeatureEngine(customers_df, devices_df, feature_columns)
        
        # Convert to dict for feature engineering
        tx_data = request.dict()
        
        # Engineer features in real-time
        features = feature_engine.engineer_features(tx_data)
        
        # Scale features
        features_scaled = feature_scaler.transform(features)
        
        # Get predictions from both models
        iso_score = iso_model.decision_function(features_scaled)[0]
        iso_risk = max(0, min(1, (1 - (iso_score + 0.5))))
        
        xgb_prob = xgb_model.predict_proba(features)[0, 1]
        
        # Ensemble scoring
        ensemble_score = 0.3 * iso_risk + 0.7 * xgb_prob
        
        # Generate explanation for high-risk transactions
        explanation = None
        if ensemble_score > 0.7 and shap_explainer is not None:
            try:
                shap_values = shap_explainer.shap_values(features)
                top_features_idx = np.argsort(-np.abs(shap_values[0]))[:3]
                explanation = {
                    'top_risk_factors': [
                        {
                            'feature': feature_columns[i],
                            'contribution': float(shap_values[0][i]),
                            'value': float(features[0][i])
                        }
                        for i in top_features_idx
                    ]
                }
            except Exception as e:
                print(f"SHAP explanation failed: {e}")
        
        return PredictionResponse(
            transaction_id=request.transaction_id,
            risk_score=round(ensemble_score, 4),
            is_high_risk=ensemble_score > 0.7,
            model_breakdown={
                "isolation_forest_score": round(iso_risk, 4),
                "xgboost_score": round(xgb_prob, 4)
            },
            explanation=explanation,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Add monitoring endpoint
@app.get("/metrics")
async def metrics():
    return {
        "models_loaded": MODELS_LOADED,
        "feature_columns": feature_columns if feature_columns else [],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)