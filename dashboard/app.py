import sys
import os
# Add the project root to sys.path so 'dashboard.X' absolute imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from dashboard.config import CUSTOM_CSS
from dashboard.data_loader import load_data
from dashboard.components import render_sidebar, render_kpis
from dashboard.views import macro_trends, correlation, ml_predictions

st.set_page_config(page_title="Pakistan Economic Dashboard", page_icon="📈", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

df = load_data()

if df is not None:
    st.markdown('<h1 class="main-header">🇵🇰 Pakistan Economic & Remittances Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive Analysis of Macroeconomic Indicators (2000 - 2025)</p>', unsafe_allow_html=True)

    selected_years, target_variable = render_sidebar(df)
    
    # Filter data
    filtered_df = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

    render_kpis(filtered_df)

    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["🌍 Macro Trends", "🔄 Correlation Analysis", "🤖 ML Project"])

    with tab1:
        macro_trends.render_tab(filtered_df)

    with tab2:
        correlation.render_tab(df)

    with tab3:
        ml_predictions.render_tab(df, target_variable)
else:
    st.stop()
