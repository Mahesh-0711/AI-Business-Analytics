import os
import json

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from google import genai

from app.data_manager import data_manager
from app.analytics_engine import AnalyticsEngine
from app.dependencies import get_current_user

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

# Create Gemini Client
client = genai.Client(api_key=api_key)

router = APIRouter()


@router.get("/ai-insights")
def ai_insights(
    current_user=Depends(get_current_user)
):

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    engine = AnalyticsEngine(df)

    analytics = engine.generate_summary()

    prompt = f"""
You are an experienced Business Intelligence Consultant.

Below is a business analytics summary.

{json.dumps(analytics, indent=2)}

Generate:

1. Executive Summary
2. Sales Analysis
3. Profit Analysis
4. Regional Performance
5. Category Performance
6. Payment Method Analysis
7. Risks
8. Business Recommendations

Write like a McKinsey or Deloitte consultant.

Do not mention that you are an AI.

Use professional business language.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "user": current_user.email,
        "analytics": analytics,
        "ai_analysis": response.text
    }