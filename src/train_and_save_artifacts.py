import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from datetime import datetime
import xgboost as xgb
import shap
import warnings
warnings.filterwarnings('ignore')

print("Loading datasets...")

# Load your synthetic data - adjust path if needed
DATA_PATH = "../data/synthetic"  # or "data" if your CSV files are in a data folder
try:
    transactions = pd.read_csv(f"{DATA_PATH}/transactions.csv", parse_dates=['timestamp'])
    customers = pd.read_csv(f"{DATA_PATH}/customers.csv")
    devices = pd.read_csv(f"{DATA_PATH}/devices.csv")
    beneficiaries = pd.read_csv(f"{DATA_PATH}/beneficiaries.csv")
    
    print(f"Transactions: {transactions.shape}")
    print(f"Customers: {customers.shape}")
    print(f"Devices: {devices.shape}")
    print(f"Beneficiaries: {beneficiaries.shape}")
    
except FileNotFoundError as e:
    print(f"Error loading files: {e}")
    print("Please make sure your CSV files are in the correct location")
    exit(1)

def create_features(transactions, customers, devices, beneficiaries):
    """Build features for fraud detection"""
    print("Engineering features...")
    
    # Merge all datasets
    df = transactions.merge(
        customers[['customer_id', 'customer_risk_level', 'avg_txn_amount', 'signup_date']],
        on='customer_id', how='left'
    ).merge(
        devices[['device_id', 'owner_customer_id', 'ip_prefix']],
        on='device_id', how='left'
    ).merge(
        beneficiaries[['beneficiary_id', 'country']].rename(columns={'country': 'beneficiary_country'}),
        on='beneficiary_id', how='left'
    )

    # Device mismatch - critical for SIM swap detection
    df['device_mismatch'] = (df['owner_customer_id'] != df['customer_id']).astype(int)
    df['device_mismatch'] = df['device_mismatch'].fillna(1)  # Null owner = mismatch

    # High amount flag - African context: >5x average is suspicious
    df['high_amount'] = (df['amount'] > (5 * df['avg_txn_amount'])).astype(int)

    # Time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['odd_hour'] = ((df['hour'] <= 5) | (df['hour'] >= 23)).astype(int)  # Late night/early morning

    # Customer tenure - new customers are higher risk
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['customer_tenure_days'] = (df['timestamp'] - df['signup_date']).dt.days
    df['is_new_customer'] = (df['customer_tenure_days'] < 30).astype(int)

    # Channel risk - USSD/mobile higher risk in Africa
    channel_risk = {'ussd': 3, 'mobile': 2, 'agent': 2, 'web': 1, 'atm': 1}
    df['channel_risk'] = df['channel'].str.lower().map(channel_risk).fillna(1)

    # Cyclic time encoding - captures periodic patterns
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

    # IP-based features - simplified geolocation risk
    df['ip_risk'] = df['ip_prefix'].apply(lambda x: hash(str(x)) % 10)

    # Amount-related features
    df['amount_to_avg_ratio'] = df['amount'] / df['avg_txn_amount'].replace(0, 1)
    df['amount_log'] = np.log1p(df['amount'])

    # Target variable
    df['is_fraud'] = (df['fraud_label_id'] == 3).astype(int)

    print(f"Feature engineering complete. Fraud rate: {df['is_fraud'].mean():.3f}")
    return df

featured_data = create_features(transactions, customers, devices, beneficiaries)
print(f"Features created. Final shape: {featured_data.shape}")

def time_based_split(df, test_days=30):
    """Split data by time to prevent data leakage"""
    print("Performing time-based split...")
    
    df = df.sort_values('timestamp').reset_index(drop=True)
    cutoff = df['timestamp'].max() - pd.Timedelta(days=test_days)
    
    train_mask = df['timestamp'] <= cutoff
    test_mask = df['timestamp'] > cutoff
    
    X_train = df.loc[train_mask]
    X_test = df.loc[test_mask]
    y_train = X_train['is_fraud']
    y_test = X_test['is_fraud']
    
    print(f"Train: {X_train.shape[0]} transactions (until {cutoff.date()})")
    print(f"Test:  {X_test.shape[0]} transactions (after {cutoff.date()})")
    print(f"Fraud rate - Train: {y_train.mean():.3f}, Test: {y_test.mean():.3f}")
    
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = time_based_split(featured_data)

feature_columns = [
    'amount', 'customer_risk_level', 'device_mismatch', 'high_amount',
    'odd_hour', 'channel_risk', 'is_new_customer',
    'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos',
    'ip_risk', 'amount_to_avg_ratio', 'amount_log'
]

print(f"Using {len(feature_columns)} features:")
for i, feat in enumerate(feature_columns, 1):
    print(f"   {i:2d}. {feat}")

X_train_feats = X_train[feature_columns]
X_test_feats = X_test[feature_columns]

print("\nTraining models...")

# Scale features for Isolation Forest
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_feats)
X_test_scaled = scaler.transform(X_test_feats)

# Train Isolation Forest (unsupervised anomaly detection)
print("Training Isolation Forest...")
iso_model = IsolationForest(
    contamination=0.05,  # Expected fraud rate
    n_estimators=150,
    random_state=42,
    verbose=1
)
iso_model.fit(X_train_scaled)
print("Isolation Forest trained!")

# Train XGBoost (supervised learning)
print("Training XGBoost...")
xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    scale_pos_weight=len(y_train) / sum(y_train),  # Handle class imbalance
    eval_metric='logloss',
    verbosity=1
)
xgb_model.fit(X_train_feats, y_train)
print("XGBoost trained!")

print("\n" + "="*50)
print("MODEL EVALUATION")
print("="*50)

# XGBoost predictions
xgb_probs = xgb_model.predict_proba(X_test_feats)[:, 1]
xgb_preds = (xgb_probs > 0.5).astype(int)

# Isolation Forest predictions
iso_scores = iso_model.decision_function(X_test_scaled)
iso_preds = (iso_scores < np.percentile(iso_scores, 5)).astype(int)  # Top 5% as anomalies

print("\nXGBOOST PERFORMANCE:")
print(f"ROC-AUC: {roc_auc_score(y_test, xgb_probs):.4f}")
print(classification_report(y_test, xgb_preds, target_names=['Legit', 'Fraud']))

print("\nISOLATION FOREST PERFORMANCE:")
print(f"ROC-AUC: {roc_auc_score(y_test, -iso_scores):.4f}")  # Lower scores = more anomalous
print(classification_report(y_test, iso_preds, target_names=['Legit', 'Fraud']))

# Feature importance
print("\nXGBOOST FEATURE IMPORTANCE:")
importance_df = pd.DataFrame({
    'feature': feature_columns,
    'importance': xgb_model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance_df.to_string(index=False))

print("\nCreating SHAP explainer...")
try:
    # Use smaller sample for performance
    explainer = shap.TreeExplainer(xgb_model)
    
    # Calculate SHAP values for a sample
    shap_sample = X_train_feats.iloc[:1000]  # Use first 1000 for demo
    shap_values = explainer.shap_values(shap_sample)
    
    print("SHAP explainer created successfully!")
    print(f"   SHAP values shape: {np.array(shap_values).shape}")
    
except Exception as e:
    print(f"SHAP explainer failed: {e}")
    explainer = None

print("\nSaving artifacts for production...")

# Prepare dataframes for real-time feature engineering
customers_for_rt = customers[['customer_id', 'avg_txn_amount', 'customer_risk_level', 'signup_date']].copy()
devices_for_rt = devices[['device_id', 'owner_customer_id', 'ip_prefix']].copy()

# Ensure signup_date is datetime
customers_for_rt['signup_date'] = pd.to_datetime(customers_for_rt['signup_date'])

artifacts = {
    'xgb_model': xgb_model,
    'iso_model': iso_model,
    'scaler': scaler,
    'shap_explainer': explainer if explainer else None,
    'feature_columns': feature_columns,
    'customers_df': customers_for_rt,
    'devices_df': devices_for_rt,
    'training_info': {
        'train_shape': X_train_feats.shape,
        'test_shape': X_test_feats.shape,
        'fraud_rate_train': y_train.mean(),
        'fraud_rate_test': y_test.mean(),
        'feature_names': feature_columns,
        'timestamp': datetime.now().isoformat()
    }
}

# Save artifacts
joblib.dump(artifacts, "sentinel_ai_artifacts.pkl")
print("Artifacts saved → sentinel_ai_artifacts.pkl")

# Verify the artifacts can be loaded
try:
    test_artifacts = joblib.load("sentinel_ai_artifacts.pkl")
    print("Artifacts verification: SUCCESS")
    print(f"Models loaded: 'xgb_model' and 'iso_model' present")
    print(f"Feature columns: {len(test_artifacts['feature_columns'])} features")
except Exception as e:
    print(f"Artifacts verification failed: {e}")

print("\n" + "="*60)
print("TRAINING COMPLETE - SUMMARY")
print("="*60)
print(f"Artifacts file: sentinel_ai_artifacts.pkl")
print(f"Models trained: XGBoost + Isolation Forest")
print(f"Features: {len(feature_columns)}")
print(f"Training data: {X_train_feats.shape[0]:,} transactions")
print(f"Test data: {X_test_feats.shape[0]:,} transactions")
print(f"XGBoost AUC: {roc_auc_score(y_test, xgb_probs):.4f}")
print(f"SHAP explainer: {'READY' if explainer is not None else 'FAILED'}")
