import pandas as pd
import xgboost as xgb
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
import joblib

def train_models(X, y):
    """
    Train XGBoost and Isolation Forest models on the provided features and labels.
    
    Parameters:
    - X: Feature DataFrame
    - y: Target Series
    
    Returns:
    - iso_model: Trained Isolation Forest model
    - xgb_model: Trained XGBoost model
    - scaler: StandardScaler fitted on the features
    """
    # Scale features for Isolation Forest
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    iso_model = IsolationForest(contamination=0.05, random_state=42)
    iso_model.fit(X_scaled)

    # Train XGBoost
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        scale_pos_weight=len(y) / sum(y)  # Handle class imbalance
    )
    xgb_model.fit(X, y)

    return iso_model, xgb_model, scaler

def save_models(iso_model, xgb_model, scaler, filename='models.pkl'):
    """
    Save the trained models and scaler to a file.
    
    Parameters:
    - iso_model: Trained Isolation Forest model
    - xgb_model: Trained XGBoost model
    - scaler: StandardScaler fitted on the features
    - filename: Name of the file to save the models
    """
    joblib.dump({
        'iso_model': iso_model,
        'xgb_model': xgb_model,
        'scaler': scaler
    }, filename)

def load_models(filename='models.pkl'):
    """
    Load the trained models and scaler from a file.
    
    Parameters:
    - filename: Name of the file to load the models from
    
    Returns:
    - iso_model: Loaded Isolation Forest model
    - xgb_model: Loaded XGBoost model
    - scaler: Loaded StandardScaler
    """
    models = joblib.load(filename)
    return models['iso_model'], models['xgb_model'], models['scaler']