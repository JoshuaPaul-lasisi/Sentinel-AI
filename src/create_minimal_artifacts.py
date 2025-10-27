import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

print("Creating minimal working artifacts...")

# Just create the essential structure
artifacts = {
    'feature_columns': [
        'amount', 'customer_risk_level', 'device_mismatch', 'high_amount',
        'odd_hour', 'channel_risk', 'is_new_customer'
    ],
    'scaler': StandardScaler(),
    'dummy_model': True  # Mark as dummy for now
}

# Create simple scaler fit
dummy_data = np.random.randn(100, 7)
artifacts['scaler'].fit(dummy_data)

# Save with maximum compatibility
joblib.dump(artifacts, "sentinel_ai_artifacts_working.pkl", protocol=4, compress=('gzip', 3))

print("Minimal artifacts saved: sentinel_ai_artifacts_working.pkl")

# Verify
test = joblib.load("sentinel_ai_artifacts_working.pkl")
print("Load test successful!")
print(f"Features: {test['feature_columns']}")