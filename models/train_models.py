import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def main():
    print("Starting pre-training of ML models...")
    
    # Absolute pathing for robust execution
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "pakistan_economic_indicators_2000_2025.csv")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    
    df = pd.read_csv(DATA_PATH)
    targets = ['gdp_usd_bn', 'gdp_growth_pct', 'pkr_per_usd', 'inflation_cpi_pct']
    features = ['remittances_usd_bn', 'inflation_cpi_pct', 'exports_usd_bn', 'policy_rate_pct', 'fdi_inflows_usd_bn']

    for target_variable in targets:
        ml_df = df.dropna(subset=features + [target_variable])
        if len(ml_df) > 10:
            X = ml_df[features]
            y = ml_df[target_variable]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            
            # Save the model and its metrics
            model_path = os.path.join(MODELS_DIR, f"model_{target_variable}.pkl")
            joblib.dump({
                'model': model,
                'r2': r2,
                'mse': mse,
                'feature_importances': model.feature_importances_
            }, model_path)
            
            print(f"Successfully trained and saved model_{target_variable}.pkl (R2: {r2:.2f}, MSE: {mse:.2f})")
        else:
            print(f"Not enough data to train model for {target_variable}")

    print("Pre-training complete.")

if __name__ == "__main__":
    main()
