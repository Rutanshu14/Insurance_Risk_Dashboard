import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils.risk_engine import compute_risk_metrics
from utils.executive_report import generate_executive_report

st.set_page_config(
    page_title="Insurance Risk Intelligence",
    layout="wide"
)

# ---------------- HIDE STREAMLIT UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

.hero {
    padding: 45px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0E4C92, #08306B);
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.glass-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/insurers.csv")
sentiment_df = pd.read_csv("data/sentiment.csv")

risk_df = compute_risk_metrics(df, sentiment_df)

# ---------------- SIDEBAR NAVIGATION 🔥 ----------------
st.sidebar.markdown("## Insurance Risk Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Summary",
        "Risk Heatmap",
        "Regime Classification",
        "Probability Forecast",
        "Company Comparison",
        "Regulator View"
    ]
)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
gnostic">
    <h1>Insurance Risk Intelligence Platform</h1>
    <p>Integrated Complaint • Sentiment • Early Warning Analytics</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# ✅ EXECUTIVE SUMMARY
# =====================================================
if page == "Executive Summary":

    st.subheader("📊 Executive Summary")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Complaints", f"{risk_df['Complaints'].sum():,.0f}")
    col2.metric("Negative Sentiment", f"{risk_df['Negative Sentiment %'].mean():.2%}")
    col3.metric("Reputation Risk Index", f"{risk_df['Reputation Risk Index'].mean():,.1f}")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# ✅ RISK HEATMAP 🔥
# =====================================================
elif page == "Risk Heatmap":

    st.subheader("🔥 Cross-Insurer Risk Heatmap")

    heatmap_cols = ["Complaints", "Negative Sentiment %", "Reputation Risk Index"]

    fig, ax = plt.subplots()

    sns.heatmap(
        risk_df[heatmap_cols],
        cmap="RdYlGn_r",
        ax=ax
    )

    ax.set_title("Industry Risk Profile")

    st.pyplot(fig)

# =====================================================
# ✅ REGIME CLASSIFICATION 🚦
# =====================================================
elif page == "Regime Classification":

    st.subheader("🚦 Risk Regime Classification")

    regime_df = risk_df.copy()

    regime_df["Regime"] = regime_df["EWS Score"].apply(
        lambda x: "Elevated Risk" if x > 1.25
        else "Watchlist" if x > 0.75
        else "Stable"
    )

    regime_fig = px.bar(
        regime_df,
        x=regime_df.index,
        y="EWS Score",
        color="Regime",
        color_discrete_map={
            "Stable": "green",
            "Watchlist": "orange",
            "Elevated Risk": "red"
        }
    )

    st.plotly_chart(regime_fig, use_container_width=True)

# =====================================================
# ✅ PROBABILITY FORECAST 📈
# =====================================================
elif page == "Probability Forecast":

    st.subheader("📈 Probability Forecast")

    st.info("Forecast simulation (placeholder for Prophet / ML model)")

    forecast_values = risk_df["Reputation Risk Index"] + np.random.normal(0, 5, len(risk_df))

    forecast_fig = px.line(
        x=risk_df.index,
        y=forecast_values,
        markers=True
    )

    st.plotly_chart(forecast_fig, use_container_width=True)

# =====================================================
# ✅ COMPANY COMPARISON 📊
# =====================================================
elif page == "Company Comparison":

    st.subheader("📊 Company Comparison")

    comparison_metric = st.selectbox(
        "Select Metric",
        ["Complaints", "Negative Sentiment %", "Reputation Risk Index"]
    )

    comp_fig = px.bar(
        risk_df,
        x=risk_df.index,
        y=comparison_metric,
        color=comparison_metric,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(comp_fig, use_container_width=True)

# =====================================================
# ✅ REGULATOR VIEW 🏛
# =====================================================
elif page == "Regulator View":

    st.subheader("🏛 Regulator Risk Monitoring View")

    high_risk = risk_df[risk_df["EWS Score"] > 1.25]

    st.markdown("### 🔴 Elevated Risk Insurers")

    st.dataframe(high_risk)

    st.markdown("### 📄 Generate Industry Report")

    report = generate_executive_report("Industry Overview", risk_df)

    st.download_button(
        label="Download Industry Report",
        data=report,
        file_name="Industry_Risk_Report.pdf",
        mime="application/pdf"
    )