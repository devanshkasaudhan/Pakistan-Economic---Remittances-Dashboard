import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    try:
        # Load from the new relative 'data' folder
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_PATH = os.path.join(BASE_DIR, "data", "pakistan_economic_indicators_2000_2025.csv")
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
