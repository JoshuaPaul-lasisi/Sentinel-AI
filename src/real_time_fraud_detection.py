import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load all datasets
print("📥 Loading datasets...")
transactions = pd.read_csv("data/synthetic/transactions.csv", parse_dates=['timestamp'])
customers = pd.read_csv("data/synthetic/customers.csv")
devices = pd.read_csv("data/synthetic/devices.csv")
beneficiaries = pd.read_csv("data/synthetic/beneficiaries.csv")

print(f"Transactions: {transactions.shape}")
print(f"Customers: {customers.shape}")
print(f"Devices: {devices.shape}")

def create_real_time_features(transactions, customers, devices, beneficiaries):
    """
    Create features for real-time fraud detection
    Returns: Feature DataFrame and target series
    """
    
    # Merge with customers
    df = transactions.merge(
        customers[['customer_id', 'customer_risk_level', 'avg_txn_amount', 'signup_date']],
        on='customer_id', 
        how='left'
    )
    
    # Merge with devices
    df = df.merge(
        devices[['device_id', 'owner_customer_id', 'ip_prefix']],
        on='device_id',
        how='left'
    )
    
    # Merge with beneficiaries (for future expansion)
    df = df.merge(
        beneficiaries[['beneficiary_id', 'country']].rename(columns={'country': 'beneficiary_country'}),
        on='beneficiary_id',
        how='left'
    )
    
    # ==================== CORE FEATURE ENGINEERING ====================
    
    # 1. Device mismatch (critical for ATO detection)
    df['device_mismatch'] = (df['owner_customer_id'] != df['customer_id']).astype(int)
    df['device_mismatch'] = df['device_mismatch'].fillna(1)  # Null owner = mismatch
    
    # 2. High amount flag (African context: >5x average is suspicious)
    df['high_amount'] = (df['amount'] > (5 * df['avg_txn_amount'])).astype(int)
    
    # 3. Time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # 4. Odd hours (0-5 AM or 11 PM-12 AM - common fraud times)
    df['odd_hour'] = ((df['hour'] >= 0) & (df['hour'] <= 5)) | (df['hour'] >= 23).astype(int)
    
    # 5. Customer tenure (new customers are higher risk)
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['customer_tenure_days'] = (df['timestamp'] - df['signup_date']).dt.days
    df['is_new_customer'] = (df['customer_tenure_days'] < 30).astype(int)
    
    # 6. Transaction velocity features (would be real-time in production)
    # For now, we'll calculate from historical data
    customer_tx_counts = transactions.groupby('customer_id').size()
    df['customer_historical_tx_count'] = df['customer_id'].map(customer_tx_counts).fillna(0)
    
    # 7. Channel risk encoding (USSD/mobile higher risk in Africa)
    channel_risk = {'ussd': 3, 'mobile': 2, 'agent': 2, 'web': 1, 'atm': 1}
    df['channel_risk'] = df['channel'].str.lower().map(channel_risk).fillna(1)
    
    # 8. Cyclic encoding for time features
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    # 9. IP-based features (simplified - would be real geolocation in production)
    df['ip_risk'] = df['ip_prefix'].apply(lambda x: hash(x) % 10)  # Placeholder
    
    # 10. Amount statistics
    df['amount_to_avg_ratio'] = df['amount'] / df['avg_txn_amount'].replace(0, 1)
    df['amount_log'] = np.log1p(df['amount'])
    
    # ==================== TARGET VARIABLE ====================
    df['is_fraud'] = (df['fraud_label_id'] == 3).astype(int)
    
    print(f"✅ Feature engineering complete. Final shape: {df.shape}")
    return df

# Create features
featured_data = create_real_time_features(transactions, customers, devices, beneficiaries)

def time_based_split(df, test_size_days=30):
    """
    Split data by time to prevent leakage
    Last `test_size_days` as test set
    """
    df_sorted = df.sort_values('timestamp').reset_index(drop=True)
    
    # Find cutoff date
    cutoff_date = df_sorted['timestamp'].max() - pd.Timedelta(days=test_size_days)
    
    train_mask = df_sorted['timestamp'] <= cutoff_date
    test_mask = df_sorted['timestamp'] > cutoff_date
    
    X_train = df_sorted[train_mask].drop('is_fraud', axis=1)
    X_test = df_sorted[test_mask].drop('is_fraud', axis=1)
    y_train = df_sorted[train_mask]['is_fraud']
    y_test = df_sorted[test_mask]['is_fraud']
    
    print(f"📊 Time-based split:")
    print(f"   Train: {X_train.shape[0]} transactions (until {cutoff_date})")
    print(f"   Test:  {X_test.shape[0]} transactions (after {cutoff_date})")
    print(f"   Fraud rate - Train: {y_train.mean():.3f}, Test: {y_test.mean():.3f}")
    
    return X_train, X_test, y_train, y_test

# Select final features for modeling
feature_columns = [
    'amount', 'customer_risk_level', 'device_mismatch', 'high_amount',
    'odd_hour', 'channel_risk', 'is_new_customer', 'customer_historical_tx_count',
    'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos', 'ip_risk',
    'amount_to_avg_ratio', 'amount_log'
]

# Split data
X_train, X_test, y_train, y_test = time_based_split(featured_data)

# Prepare feature matrices
X_train_feats = X_train[feature_columns]
X_test_feats = X_test[feature_columns]

def train_models(X_train, y_train):
    """
    Train XGBoost and Isolation Forest models
    """
    # Scale features for Isolation Forest
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    print("🤖 Training Isolation Forest...")
    iso_forest = IsolationForest(
        contamination=0.05,  # Expected fraud rate
        random_state=42,
        n_estimators=150,
        max_samples='auto'
    )
    iso_forest.fit(X_train_scaled)
    
    print("🤖 Training XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        scale_pos_weight=len(y_train) / sum(y_train)  # Handle class imbalance
    )
    xgb_model.fit(X_train, y_train)
    
    return iso_forest, xgb_model, scaler

# Train both models
iso_model, xgb_model, feature_scaler = train_models(X_train_feats, y_train)

def evaluate_models(iso_model, xgb_model, scaler, X_test, y_test, feature_columns):
    """
    Evaluate both models and compare performance
    """
    X_test_feats = X_test[feature_columns]
    X_test_scaled = scaler.transform(X_test_feats)
    
    # Isolation Forest predictions
    iso_scores = iso_model.decision_function(X_test_scaled)
    iso_predictions = (iso_scores < np.percentile(iso_scores, 5)).astype(int)  # Top 5% as fraud
    
    # XGBoost predictions
    xgb_probs = xgb_model.predict_proba(X_test_feats)[:, 1]
    xgb_predictions = (xgb_probs > 0.5).astype(int)
    
    print("=" * 60)
    print("🎯 MODEL EVALUATION RESULTS")
    print("=" * 60)
    
    print("\n🔍 ISOLATION FOREST:")
    print(classification_report(y_test, iso_predictions, target_names=['Legit', 'Fraud']))
    print(f"ROC-AUC: {roc_auc_score(y_test, -iso_scores):.4f}")  # Lower scores = more anomalous
    
    print("\n🔍 XGBOOST:")
    print(classification_report(y_test, xgb_predictions, target_names=['Legit', 'Fraud']))
    print(f"ROC-AUC: {roc_auc_score(y_test, xgb_probs):.4f}")
    
    # Feature importance
    print("\n📊 XGBoost Feature Importance:")
    importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': xgb_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(importance_df.head(10))
    
    return iso_scores, xgb_probs, importance_df

# Evaluate models
iso_scores, xgb_probs, feature_importance = evaluate_models(
    iso_model, xgb_model, feature_scaler, X_test, y_test, feature_columns
)

import shap

def create_shap_explainer(xgb_model, X_train_feats, feature_columns):
    """
    Create SHAP explainer for model interpretability
    """
    print("🧠 Creating SHAP explainer...")
    
    # Use smaller sample for performance
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(X_train_feats.iloc[:1000])  # Sample for demo
    
    # Summary plot
    shap.summary_plot(shap_values, X_train_feats.iloc[:1000], feature_names=feature_columns, show=False)
    
    return explainer

# Create SHAP explainer
shap_explainer = create_shap_explainer(xgb_model, X_train_feats, feature_columns)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import numpy as np

app = FastAPI(title="Sentinel AI Real-Time Fraud Detection")

class TransactionRequest(BaseModel):
    transaction_id: str
    customer_id: int
    device_id: int
    amount: float
    channel: str
    timestamp: str
    # In production, you'd have more fields from real-time lookups

class RealTimeFeatureEngine:
    """Feature engineering for real-time predictions"""
    
    def __init__(self, customers_df, devices_df, feature_columns):
        self.customers_df = customers_df.set_index('customer_id')
        self.devices_df = devices_df.set_index('device_id')
        self.feature_columns = feature_columns
        
    def engineer_features(self, transaction_data: Dict) -> np.array:
        """Engineer features in real-time"""
        customer_id = transaction_data['customer_id']
        device_id = transaction_data['device_id']
        amount = transaction_data['amount']
        channel = transaction_data['channel']
        timestamp = pd.to_datetime(transaction_data['timestamp'])
        
        # Get customer data (would be Redis cache in production)
        customer_data = self.customers_df.loc[customer_id]
        device_data = self.devices_df.loc[device_id]
        
        # Real-time feature engineering
        features = []
        
        # 1. Basic features
        features.extend([
            amount,
            customer_data['customer_risk_level'],
            int(device_data['owner_customer_id'] != customer_id),  # device_mismatch
            int(amount > (5 * customer_data['avg_txn_amount'])),   # high_amount
            int(timestamp.hour <= 5 or timestamp.hour >= 23),      # odd_hour
        ])
        
        # 2. Channel risk
        channel_risk = {'ussd': 3, 'mobile': 2, 'agent': 2, 'web': 1, 'atm': 1}
        features.append(channel_risk.get(channel.lower(), 1))
        
        # 3. Customer tenure (simplified)
        signup_date = pd.to_datetime(customer_data['signup_date'])
        tenure_days = (timestamp - signup_date).days
        features.append(int(tenure_days < 30))  # is_new_customer
        
        # 4. Historical count (would be from real-time counter)
        features.append(100)  # placeholder
        
        # 5. Time features
        hour = timestamp.hour
        dow = timestamp.dayofweek
        features.extend([
            np.sin(2 * np.pi * hour / 24),
            np.cos(2 * np.pi * hour / 24),
            np.sin(2 * np.pi * dow / 7),
            np.cos(2 * np.pi * dow / 7),
        ])
        
        # 6. IP risk (placeholder)
        features.append(hash(device_data['ip_prefix']) % 10)
        
        # 7. Amount features
        features.extend([
            amount / max(customer_data['avg_txn_amount'], 1),
            np.log1p(amount)
        ])
        
        return np.array(features).reshape(1, -1)

# Initialize feature engine
feature_engine = RealTimeFeatureEngine(customers, devices, feature_columns)

@app.post("/predict", response_model=Dict[str, Any])
async def predict_fraud(request: TransactionRequest):
    """Real-time fraud prediction endpoint"""
    try:
        # Convert to dict for feature engineering
        tx_data = request.dict()
        
        # Engineer features in real-time
        features = feature_engine.engineer_features(tx_data)
        
        # Get predictions from both models
        features_scaled = feature_scaler.transform(features)
        
        # Isolation Forest score
        iso_score = iso_model.decision_function(features_scaled)[0]
        iso_risk = max(0, min(1, (1 - (iso_score + 0.5))))  # Convert to 0-1
        
        # XGBoost prediction
        xgb_prob = xgb_model.predict_proba(features)[0, 1]
        
        # Ensemble score (weighted average)
        ensemble_score = 0.3 * iso_risk + 0.7 * xgb_prob
        
        # SHAP explanation (for high-risk transactions)
        explanation = None
        if ensemble_score > 0.7:
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
        
        return {
            "transaction_id": request.transaction_id,
            "risk_score": round(ensemble_score, 4),
            "is_high_risk": ensemble_score > 0.7,
            "model_breakdown": {
                "isolation_forest_score": round(iso_risk, 4),
                "xgboost_score": round(xgb_prob, 4)
            },
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": str(e), "risk_score": 0.5, "is_high_risk": False}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "models_loaded": True,
        "timestamp": datetime.now().isoformat()
    }

# Save all artifacts for production
def save_artifacts():
    """Save models and artifacts for deployment"""
    artifacts = {
        'xgb_model': xgb_model,
        'iso_model': iso_model,
        'scaler': feature_scaler,
        'shap_explainer': shap_explainer,
        'feature_columns': feature_columns,
        'feature_engine': feature_engine
    }
    
    joblib.dump(artifacts, 'sentinel_ai_artifacts.pkl')
    print("✅ All artifacts saved for production deployment!")

save_artifacts()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)