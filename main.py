from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Sentinel AI API Running", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict_fraud():
    return {
        "risk_score": 0.75,
        "recommendation": "REVIEW",
        "explanation": {"test": "API is working"}
    }