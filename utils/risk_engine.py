import pandas as pd
import numpy as np

def compute_risk_metrics(df, sentiment_df):

    numeric_df = df.select_dtypes(include='number')

    complaints = df.groupby('Company')[numeric_df.columns].sum().sum(axis=1)

    negative_sentiment = sentiment_df.groupby('Company')['Sentiment'].apply(
        lambda x: (x == "Negative").mean()
    )

    risk_df = pd.DataFrame({
        "Complaints": complaints,
        "Negative Sentiment %": negative_sentiment
    })

    risk_df["Reputation Risk Index"] = (
        risk_df["Complaints"] * risk_df["Negative Sentiment %"]
    )

    risk_df["EWS Score"] = (
        risk_df["Reputation Risk Index"] /
        risk_df["Reputation Risk Index"].mean()
    )

    return risk_df