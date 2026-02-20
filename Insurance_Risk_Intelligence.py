import streamlit as st
import pandas as pd
import plotly.express as px

from utils.risk_engine import compute_risk_metrics
from utils.executive_report import generate_executive_report

st.set_page_config(layout="wide")

# ---------------- SESSION STATE ----------------
if "entered" not in st.session_state:
    st.session_state.entered = False

# ---------------- HIDE STREAMLIT UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- GLOBAL UI ----------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #F5F7FA, #FFFFFF);
}

/* LANDING PAGE */
.landing-container {
    padding: 80px 40px;
    border-radius: 28px;
    background: linear-gradient(135deg, #020024, #090979, #00C6FF);
    color: white;
    text-align: center;
    margin-top: 40px;
}

.landing-title {
    font-size: 48px;
    font-weight: 700;
}

.landing-subtitle {
    font-size: 20px;
    opacity: 0.9;
}

/* DASHBOARD */
.hero {
    padding: 50px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0E4C92, #08306B);
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.glass-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.05);
}

.story-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border-left: 6px solid #0E4C92;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LANDING PAGE 🔥 ----------------
if not st.session_state.entered:

    st.markdown("""
    <div class="landing-container">
        <div class="landing-title">
            Insurance Risk Intelligence Platform
        </div>
        <div class="landing-subtitle">
            Integrated Complaint • Sentiment • Early Warning Analytics
        </div>
        <br><br>
        <div style="font-size:18px;">
            Predict Risk • Detect Signals • Protect Reputation
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)

    col1.markdown("📊 **Risk Diagnostics**<br>Complaint & servicing variability modelling", unsafe_allow_html=True)
    col2.markdown("🚨 **Early Warning System**<br>Forward-looking instability detection", unsafe_allow_html=True)
    col3.markdown("💬 **Sentiment Intelligence**<br>Behavioural risk pressure analysis", unsafe_allow_html=True)

    st.write("")
    st.write("")

    if st.button("Enter Intelligence Platform 🔥"):
        st.session_state.entered = True
        st.rerun()

# ---------------- MAIN DASHBOARD ----------------
else:

    df = pd.read_csv("data/insurers.csv")
    sentiment_df = pd.read_csv("data/sentiment.csv")

    risk_df = compute_risk_metrics(df, sentiment_df)

    # HERO (Different from Landing)
    st.markdown("""
    <div class="hero">
        <h1>Insurance Risk Intelligence Platform</h1>
        <p>Integrated Complaint • Sentiment • Early Warning Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI STRIP
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Complaints", f"{risk_df['Complaints'].sum():,.0f}")
    col2.metric("Negative Sentiment", f"{risk_df['Negative Sentiment %'].mean():.2%}")
    col3.metric("Reputation Risk Index", f"{risk_df['Reputation Risk Index'].mean():,.1f}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # COMPANY SELECTION
    st.subheader("🎯 Insurer Risk Diagnostic")

    selected_company = st.selectbox("Select Insurer", risk_df.index)

    complaints = risk_df.loc[selected_company,'Complaints']
    sentiment = risk_df.loc[selected_company,'Negative Sentiment %']
    risk_index = risk_df.loc[selected_company,'Reputation Risk Index']
    ews_score = risk_df.loc[selected_company,'EWS Score']

    col1, col2, col3 = st.columns(3)

    col1.metric("Complaints", f"{complaints:,.0f}")
    col2.metric("Negative Sentiment", f"{sentiment:.2%}")
    col3.metric("Risk Index", f"{risk_index:,.1f}")

    st.divider()

    # RISK REGIME
    if ews_score > 1.25:
        regime = "🔴 Elevated Risk"
    elif ews_score > 0.75:
        regime = "🟡 Watchlist"
    else:
        regime = "🟢 Stable"

    st.metric("Risk Regime", regime)

    st.divider()

    # EWS CHART
    st.subheader("🚨 Early Warning System")

    ews_fig = px.bar(
        risk_df,
        x=risk_df.index,
        y="EWS Score",
        color="EWS Score",
        color_continuous_scale="RdYlGn_r"
    )

    st.plotly_chart(ews_fig, use_container_width=True)

    st.divider()

    # EXECUTIVE REPORT
    st.subheader("📄 Executive Consulting Report")

    report = generate_executive_report(selected_company, risk_df)

    st.download_button(
        label="Download Executive Report",
        data=report,
        file_name=f"{selected_company}_Executive_Report.pdf",
        mime="application/pdf"
    )