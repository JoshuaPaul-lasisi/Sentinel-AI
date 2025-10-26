import pandas as pd
import os
import joblib

def load_csv(file_path):
    """Load a CSV file into a DataFrame."""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

def save_csv(dataframe, file_path):
    """Save a DataFrame to a CSV file."""
    dataframe.to_csv(file_path, index=False)

def load_model(model_path):
    """Load a machine learning model from a file."""
    return joblib.load(model_path)

def save_model(model, model_path):
    """Save a machine learning model to a file."""
    joblib.dump(model, model_path)