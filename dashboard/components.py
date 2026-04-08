import streamlit as st
from dashboard.config import COLUMN_NAMES

def render_sidebar(df):
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/32/Flag_of_Pakistan.svg", width=150)
        st.markdown("### 📊 Control Panel")
        
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        
        selected_years = st.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))
        
        st.markdown("### 🔍 Model Configuration")
        target_variable = st.selectbox(
            "Select Target Variable for ML Prediction",
            options=['gdp_usd_bn', 'gdp_growth_pct', 'pkr_per_usd', 'inflation_cpi_pct'],
            format_func=lambda x: COLUMN_NAMES.get(x, x)
        )
        
        st.markdown("---")
        st.markdown("Developed with Streamlit & Plotly")
        
        return selected_years, target_variable

def render_kpis(filtered_df):
    st.markdown("### 📈 Key Performance Indicators (Latest Year)")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    latest_year_data = filtered_df[filtered_df['year'] == filtered_df['year'].max()].iloc[0]
    prev_year_data = filtered_df[filtered_df['year'] == filtered_df['year'].max() - 1].iloc[0] if len(filtered_df) > 1 else latest_year_data

    def get_delta(current, prev):
        if prev == 0: return "0%"
        return f"{((current - prev) / abs(prev)) * 100:.1f}%"

    with kpi_col1:
        st.metric(label="GDP (USD Billion)", value=f"${latest_year_data['gdp_usd_bn']:.1f}B", delta=get_delta(latest_year_data['gdp_usd_bn'], prev_year_data['gdp_usd_bn']))
    with kpi_col2:
        st.metric(label="Remittances (USD Billion)", value=f"${latest_year_data['remittances_usd_bn']:.1f}B", delta=get_delta(latest_year_data['remittances_usd_bn'], prev_year_data['remittances_usd_bn']))
    with kpi_col3:
        delta_inflation = round(latest_year_data['inflation_cpi_pct'] - prev_year_data['inflation_cpi_pct'], 1)
        st.metric(label="Inflation CPI (%)", value=f"{latest_year_data['inflation_cpi_pct']}%", delta=f"{delta_inflation}%", delta_color="inverse")
    with kpi_col4:
        st.metric(label="Exchange Rate (PKR/USD)", value=f"Rs {latest_year_data['pkr_per_usd']:.1f}", delta=get_delta(latest_year_data['pkr_per_usd'], prev_year_data['pkr_per_usd']), delta_color="inverse")

    st.markdown("---")
