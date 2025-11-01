# Sentinel AI Fraud Detection System

## Overview
The Sentinel AI project is designed to implement a real-time fraud detection system using synthetic data. It leverages machine learning models to identify potentially fraudulent transactions and provides an API for real-time predictions.

## Project Structure (proposed)
```
sentinel-ai
├── src
│   ├── create_synthetic_data.py       # Generates synthetic data for customers, devices, transactions, and relationships.
│   ├── real_time_fraud_detection.py    # Implements the real-time fraud detection pipeline.
│   ├── api/app.py                      # FastAPI application setup with API endpoints.
│   ├── features/feature_engineering.py  # Functions for creating features necessary for fraud detection.
│   ├── models/train.py                  # Responsible for training machine learning models.
│   ├── explainability/shap_utils.py     # Utilities for SHAP to interpret model predictions.
│   ├── utils/io.py                      # Utility functions for input/output operations.
│   └── config.py                       # Configuration settings for the project.
├── tests
│   ├── test_feature_engineering.py      # Unit tests for feature engineering functions.
│   └── test_api.py                      # Tests for the FastAPI endpoints.
├── notebooks
│   └── eda.ipynb                        # Jupyter notebook for exploratory data analysis.
├── data
│   └── synthetic
│       ├── customers.csv                # Synthetic customer data.
│       ├── devices.csv                  # Synthetic device data.
│       └── transactions.csv              # Synthetic transaction data.
├── docker
│   └── Dockerfile                       # Defines the Docker image for the application.
├── requirements.txt                     # Lists the Python dependencies required for the project.
├── docker-compose.yml                   # Defines and runs multi-container Docker applications.
├── Makefile                             # Contains commands for automating tasks.
└── README.md                            # Documentation for the project.
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd sentinel-ai
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Generate synthetic data:**
   Run the following command to generate the necessary synthetic data:
   ```
   python src/create_synthetic_data.py
   ```

4. **Run the FastAPI application:**
   Start the API server with:
   ```
   uvicorn src.api.app:app --reload
   ```

5. **Access the API:**
   The API will be available at `http://localhost:8000`. You can test the endpoints using tools like Postman or curl.

## Usage
- **Real-Time Predictions:** Send a POST request to `/predict` with transaction details to get a fraud risk score.
- **Health Check:** Access the `/health` endpoint to check the status of the API.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
