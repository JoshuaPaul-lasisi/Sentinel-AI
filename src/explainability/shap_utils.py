import shap
import pandas as pd

def create_shap_explainer(model, X_train):
    """
    Create a SHAP explainer for the given model and training data.
    
    Parameters:
    - model: The trained model for which to create the explainer.
    - X_train: The training data used to fit the model.
    
    Returns:
    - explainer: A SHAP explainer object.
    """
    explainer = shap.TreeExplainer(model)
    return explainer

def explain_predictions(explainer, X):
    """
    Generate SHAP values for the given input data.
    
    Parameters:
    - explainer: A SHAP explainer object.
    - X: The input data for which to generate SHAP values.
    
    Returns:
    - shap_values: The SHAP values for the input data.
    """
    shap_values = explainer.shap_values(X)
    return shap_values

def plot_shap_summary(shap_values, feature_names):
    """
    Plot a summary of SHAP values.
    
    Parameters:
    - shap_values: The SHAP values to plot.
    - feature_names: The names of the features corresponding to the SHAP values.
    """
    shap.summary_plot(shap_values, feature_names=feature_names)