from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

from app.data_manager import data_manager
from app.analytics_engine import AnalyticsEngine

router = APIRouter()

REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)


@router.get("/report")
def generate_report():

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    engine = AnalyticsEngine(df)

    analytics = engine.generate_summary()

    filename = os.path.join(REPORT_FOLDER, "Business_Report.pdf")

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Business Analytics Report</b>", styles["Title"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    for key, value in analytics.items():

        story.append(
            Paragraph(f"<b>{key}</b>: {value}", styles["BodyText"])
        )

    doc.build(story)

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename="Business_Report.pdf"
    )