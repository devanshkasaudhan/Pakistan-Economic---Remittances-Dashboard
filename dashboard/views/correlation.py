import streamlit as st
import plotly.express as px
from dashboard.config import COLUMN_NAMES

def render_tab(df):
    st.subheader("Correlation: How Remittances Impact Other Drivers")
    
    y_var = st.selectbox("Select Y-Axis Variable", ['trade_balance_usd_bn', 'pkr_per_usd', 'gdp_growth_pct', 'inflation_cpi_pct'],
                         format_func=lambda x: COLUMN_NAMES.get(x, x))
    
    fig_scatter = px.scatter(df, x='remittances_usd_bn', y=y_var, 
                             size='gdp_usd_bn', color='decade', hover_name='year',
                             title=f"Remittances vs {COLUMN_NAMES.get(y_var, y_var)}",
                             labels=COLUMN_NAMES,
                             trendline="ols", template="plotly_white",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_scatter, width='stretch')

    st.markdown("**Note:** Bubble size represents GDP in USD Billion. Trendlines show General OLS Regression.")
