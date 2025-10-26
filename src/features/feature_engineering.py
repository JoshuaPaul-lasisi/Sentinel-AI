import pandas as pd
import numpy as np

def create_features(transactions, customers, devices, beneficiaries):
    """
    Create features for fraud detection from transaction data.
    
    Parameters:
    - transactions: DataFrame containing transaction data.
    - customers: DataFrame containing customer data.
    - devices: DataFrame containing device data.
    - beneficiaries: DataFrame containing beneficiary data.
    
    Returns:
    - DataFrame with engineered features.
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
    
    # Merge with beneficiaries
    df = df.merge(
        beneficiaries[['beneficiary_id', 'country']].rename(columns={'country': 'beneficiary_country'}),
        on='beneficiary_id',
        how='left'
    )
    
    # Feature engineering
    df['device_mismatch'] = (df['owner_customer_id'] != df['customer_id']).astype(int)
    df['device_mismatch'] = df['device_mismatch'].fillna(1)
    
    df['high_amount'] = (df['amount'] > (5 * df['avg_txn_amount'])).astype(int)
    
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    df['odd_hour'] = ((df['hour'] >= 0) & (df['hour'] <= 5)) | (df['hour'] >= 23).astype(int)
    
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['customer_tenure_days'] = (df['timestamp'] - df['signup_date']).dt.days
    df['is_new_customer'] = (df['customer_tenure_days'] < 30).astype(int)
    
    customer_tx_counts = transactions.groupby('customer_id').size()
    df['customer_historical_tx_count'] = df['customer_id'].map(customer_tx_counts).fillna(0)
    
    channel_risk = {'ussd': 3, 'mobile': 2, 'agent': 2, 'web': 1, 'atm': 1}
    df['channel_risk'] = df['channel'].str.lower().map(channel_risk).fillna(1)
    
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    df['ip_risk'] = df['ip_prefix'].apply(lambda x: hash(x) % 10)
    
    df['amount_to_avg_ratio'] = df['amount'] / df['avg_txn_amount'].replace(0, 1)
    df['amount_log'] = np.log1p(df['amount'])
    
    df['is_fraud'] = (df['fraud_label_id'] == 3).astype(int)
    
    return df