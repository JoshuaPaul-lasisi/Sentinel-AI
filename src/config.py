import os

class Config:
    """Configuration settings for the project."""
    
    # File paths
    DATA_DIR = os.path.join("data", "synthetic")
    CUSTOMERS_CSV = os.path.join(DATA_DIR, "customers.csv")
    DEVICES_CSV = os.path.join(DATA_DIR, "devices.csv")
    TRANSACTIONS_CSV = os.path.join(DATA_DIR, "transactions.csv")
    
    # Model parameters
    XGBOOST_PARAMS = {
        'n_estimators': 200,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42,
    }
    
    ISOLATION_FOREST_PARAMS = {
        'contamination': 0.05,
        'random_state': 42,
        'n_estimators': 150,
        'max_samples': 'auto',
    }
    
    # Other settings
    SEED = 42
    LOGGING_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL