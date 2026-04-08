import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dashboard.config import COLUMN_NAMES

# Inject via environment for K8s service discovery, with local default
API_URL = os.environ.get("API_URL", "http://localhost:8000")

def render_tab(df, target_variable):
    target_name = COLUMN_NAMES.get(target_variable, target_variable)
    st.subheader("🤖 Simple ML Predictive Model")
    st.markdown(f"Using a **Random Forest Regressor** to predict **`{target_name}`** based on core economic indicators.")
    
    features = ['remittances_usd_bn', 'inflation_cpi_pct', 'exports_usd_bn', 'policy_rate_pct', 'fdi_inflows_usd_bn']
    
    try:
        metrics_response = requests.get(f"{API_URL}/metrics/{target_variable}", timeout=5)
        if metrics_response.status_code == 200:
            metrics_data = metrics_response.json()
            r2 = metrics_data['r2']
            mse = metrics_data['mse']
            importances_array = metrics_data['feature_importances']
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Model R² Score", f"{r2:.2f}")
            col_m2.metric("Mean Squared Error", f"{mse:.2f}")
            
            st.markdown("#### Feature Importances")
            importances = pd.DataFrame({'Feature': [COLUMN_NAMES.get(f, f) for f in features], 'Importance': importances_array})
            importances = importances.sort_values(by='Importance', ascending=True)
            
            fig_imp = px.bar(importances, x='Importance', y='Feature', orientation='h',
                             title=f"Drivers most impacting {target_name}",
                             labels={'Feature': 'Economic Indicator', 'Importance': 'Relative Importance'},
                             template="plotly_white", color='Importance', color_continuous_scale='Blues')
            st.plotly_chart(fig_imp, width='stretch')
    
            st.markdown("#### 🎛️ Interactive Prediction Simulator")
            st.markdown("Adjust the sliders below to see how changes in economic factors might impact the target variable.")
            sim_cols = st.columns(len(features))
            sim_inputs = {}
            
            for i, feature in enumerate(features):
                with sim_cols[i]:
                    min_val = float(df[feature].min())
                    max_val = float(df[feature].max())
                    mean_val = float(df[feature].mean())
                    val = st.slider(COLUMN_NAMES.get(feature, feature), 
                                    min_value=min_val, max_value=max_val * 1.5, value=mean_val,
                                    label_visibility="collapsed")
                    st.caption(COLUMN_NAMES.get(feature, feature))
                    sim_inputs[feature] = val
                    
            pred_response = requests.post(f"{API_URL}/predict/{target_variable}", json=sim_inputs, timeout=5)
            if pred_response.status_code == 200:
                sim_pred = pred_response.json()['prediction']
                st.success(f"### Predicted `{target_name}`: **{sim_pred:.2f}**")
            else:
                st.error("Failed to generate prediction from API.")
        else:
            st.warning("Model file not found inside API Service. Check backend logs.")
            
    except requests.exceptions.ConnectionError:
        st.error(f"🔴 **Failed to connect to ML API at {API_URL}.** \n\nEnsure the backend service container is running.")
