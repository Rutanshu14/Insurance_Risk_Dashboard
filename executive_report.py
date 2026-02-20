import io
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_executive_report(company, risk_df):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', fontSize=20, spaceAfter=20)
    heading = ParagraphStyle('Heading', fontSize=14, spaceAfter=10)

    elements = []

    elements.append(Paragraph(f"{company} — Executive Consulting Report", title_style))

    # ---------------- METRICS SNAPSHOT ----------------
    row = risk_df.loc[company]

    elements.append(Paragraph("Key Risk Indicators", heading))
    elements.append(Paragraph(
        f"""
        Complaints: {row['Complaints']:,.0f}<br/>
        Negative Sentiment: {row['Negative Sentiment %']:.2%}<br/>
        Reputation Risk Index: {row['Reputation Risk Index']:,.1f}<br/>
        Risk Regime Score: {row['EWS Score']:,.2f}
        """,
        styles['Normal']
    ))

    elements.append(Spacer(1, 20))

    # ---------------- HEATMAP 🔥 ----------------
    heatmap_img = "heatmap.png"

    plt.figure()
    sns.heatmap(
        risk_df[["Complaints", "Negative Sentiment %", "Reputation Risk Index"]],
        cmap="RdYlGn_r"
    )
    plt.title("Cross-Insurer Risk Heatmap")
    plt.tight_layout()
    plt.savefig(heatmap_img)
    plt.close()

    elements.append(Paragraph("Industry Risk Comparison", heading))
    elements.append(Image(heatmap_img, width=450, height=220))

    elements.append(Spacer(1, 20))

    # ---------------- SENTIMENT CHART 🔥 ----------------
    sentiment_img = "sentiment_chart.png"

    plt.figure()
    risk_df["Negative Sentiment %"].plot(kind="bar")
    plt.title("Negative Sentiment Distribution")
    plt.tight_layout()
    plt.savefig(sentiment_img)
    plt.close()

    elements.append(Paragraph("Sentiment Intelligence", heading))
    elements.append(Image(sentiment_img, width=450, height=220))

    doc.build(elements)

    buffer.seek(0)
    return buffer