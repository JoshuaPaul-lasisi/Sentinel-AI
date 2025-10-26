import pandas as pd
import pytest
from src.features.feature_engineering import create_real_time_features

@pytest.fixture
def sample_data():
    transactions = pd.DataFrame({
        'transaction_id': [1, 2],
        'customer_id': [1, 2],
        'device_id': [1, 2],
        'amount': [100.0, 200.0],
        'channel': ['web', 'mobile'],
        'timestamp': pd.to_datetime(['2024-10-26 02:30:00', '2024-10-26 03:30:00']),
        'beneficiary_id': [1, 2],
        'fraud_label_id': [1, 3]
    })

    customers = pd.DataFrame({
        'customer_id': [1, 2],
        'customer_risk_level': [1, 3],
        'avg_txn_amount': [50.0, 150.0],
        'signup_date': pd.to_datetime(['2020-01-01', '2023-01-01'])
    })

    devices = pd.DataFrame({
        'device_id': [1, 2],
        'owner_customer_id': [1, 2],
        'ip_prefix': ['192.168.1', '192.168.2']
    })

    beneficiaries = pd.DataFrame({
        'beneficiary_id': [1, 2],
        'country': ['CountryA', 'CountryB']
    })

    return transactions, customers, devices, beneficiaries

def test_create_real_time_features(sample_data):
    transactions, customers, devices, beneficiaries = sample_data
    features = create_real_time_features(transactions, customers, devices, beneficiaries)

    assert features.shape[0] == transactions.shape[0]
    assert 'device_mismatch' in features.columns
    assert 'high_amount' in features.columns
    assert 'is_fraud' in features.columns
    assert features['is_fraud'].iloc[0] == 0  # Legit transaction
    assert features['is_fraud'].iloc[1] == 1  # Fraud transaction

def test_feature_engineering_shape(sample_data):
    transactions, customers, devices, beneficiaries = sample_data
    features = create_real_time_features(transactions, customers, devices, beneficiaries)

    expected_columns = [
        'transaction_id', 'customer_id', 'device_id', 'amount', 'channel',
        'timestamp', 'beneficiary_id', 'fraud_label_id', 'customer_risk_level',
        'avg_txn_amount', 'signup_date', 'owner_customer_id', 'ip_prefix',
        'beneficiary_country', 'device_mismatch', 'high_amount', 'hour',
        'day_of_week', 'is_weekend', 'odd_hour', 'customer_tenure_days',
        'is_new_customer', 'customer_historical_tx_count', 'channel_risk',
        'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos', 'ip_risk',
        'amount_to_avg_ratio', 'amount_log', 'is_fraud'
    ]

    assert all(col in features.columns for col in expected_columns)