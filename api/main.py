from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import pandas as pd

app = FastAPI(title="Pakistan Economic ML API")

# Base mappings to safely find models across environments
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

class PredictionRequest(BaseModel):
    remittances_usd_bn: float
    inflation_cpi_pct: float
    exports_usd_bn: float
    policy_rate_pct: float
    fdi_inflows_usd_bn: float

def load_model(target: str):
    model_path = os.path.join(MODELS_DIR, f"model_{target}.pkl")
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model for {target} not found. Ensure train_models.py is run.")
    return joblib.load(model_path)

@app.get("/metrics/{target}")
def get_metrics(target: str):
    model_data = load_model(target)
    return {
        "r2": model_data['r2'],
        "mse": model_data['mse'],
        "feature_importances": model_data['feature_importances'].tolist()
    }

@app.post("/predict/{target}")
def predict(target: str, data: PredictionRequest):
    model_data = load_model(target)
    model = model_data['model']
    
    # Feature extraction exactly as the random forest was trained
    sim_df = pd.DataFrame([[
        data.remittances_usd_bn,
        data.inflation_cpi_pct,
        data.exports_usd_bn,
        data.policy_rate_pct,
        data.fdi_inflows_usd_bn
    ]], columns=[
        'remittances_usd_bn', 'inflation_cpi_pct', 'exports_usd_bn', 'policy_rate_pct', 'fdi_inflows_usd_bn'
    ])
    
    prediction = model.predict(sim_df)[0]
    return {"prediction": float(prediction)}
