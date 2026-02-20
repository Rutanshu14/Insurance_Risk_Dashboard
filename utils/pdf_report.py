from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def generate_boardroom_pdf(company, complaints, sentiment, risk_index, regime):

    doc = SimpleDocTemplate(f"{company}_Boardroom_Report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{company} – Boardroom Risk Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Complaints:</b> {complaints:,.0f}", styles['BodyText']))
    elements.append(Paragraph(f"<b>Negative Sentiment:</b> {sentiment:.2%}", styles['BodyText']))
    elements.append(Paragraph(f"<b>Risk Index:</b> {risk_index:,.1f}", styles['BodyText']))
    elements.append(Paragraph(f"<b>Risk Regime:</b> {regime}", styles['BodyText']))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        "Executive Insight:",
        styles['Heading2']
    ))

    elements.append(Paragraph(
        "Observed metrics indicate evolving operational and reputational dynamics. "
        "Strategic emphasis should remain on grievance resolution efficiency and "
        "customer experience stabilisation.",
        styles['BodyText']
    ))

    doc.build(elements)