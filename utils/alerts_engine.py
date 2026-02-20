def generate_alerts(df):

    alerts = []

    if df['Loss Ratio'].mean() > 1:
        alerts.append("Loss Ratio Breach — Profitability Risk")

    if df['Solvency Ratio'].mean() < 1.5:
        alerts.append("Solvency Pressure — Capital Adequacy Concern")

    if not alerts:
        alerts.append("No Material Risk Alerts")

    return alerts