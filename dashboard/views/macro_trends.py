import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dashboard.config import COLUMN_NAMES

def render_tab(filtered_df):
    st.subheader("Economic Trends Over Time")
    
    col_fig1, col_fig2 = st.columns(2)
    
    with col_fig1:
        fig_gdp = px.line(filtered_df, x='year', y=['gdp_usd_bn', 'remittances_usd_bn', 'exports_usd_bn'], 
                          title="GDP, Remittances & Exports (USD Bn)",
                          labels=COLUMN_NAMES,
                          template="plotly_white", line_shape='spline')
        fig_gdp.for_each_trace(lambda t: t.update(name=COLUMN_NAMES.get(t.name, t.name)))
        fig_gdp.update_layout(hovermode="x unified")
        st.plotly_chart(fig_gdp, width='stretch')

    with col_fig2:
        fig_pkr = px.area(filtered_df, x='year', y='pkr_per_usd', 
                          title="Exchange Rate Trend (PKR per USD)",
                          labels=COLUMN_NAMES,
                          template="plotly_white", color_discrete_sequence=['#ef4444'])
        st.plotly_chart(fig_pkr, width='stretch')

    st.subheader("Inflation & Policy Rate")
    fig_rates = go.Figure()
    fig_rates.add_trace(go.Bar(x=filtered_df['year'], y=filtered_df['inflation_cpi_pct'], name='Inflation CPI (%)', marker_color='#f59e0b'))
    fig_rates.add_trace(go.Scatter(x=filtered_df['year'], y=filtered_df['policy_rate_pct'], name='Policy Rate (%)', line=dict(color='#2563eb', width=3)))
    fig_rates.update_layout(title="Inflation vs State Bank Policy Rate", 
                            xaxis_title="Year", yaxis_title="Percentage (%)",
                            template="plotly_white", barmode='group', hovermode="x unified")
    st.plotly_chart(fig_rates, width='stretch')
