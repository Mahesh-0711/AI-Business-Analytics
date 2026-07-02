import os
import json

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google import genai

from app.data_manager import data_manager
from app.analytics_engine import AnalyticsEngine
from app.dependencies import get_current_user

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=api_key)

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat_with_data(
    request: ChatRequest,
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
You are an expert Business Intelligence Analyst.

Dataset Analytics:

{json.dumps(analytics, indent=2)}

User Question:

{request.question}

Instructions:

1. Answer only using the provided analytics.
2. If the answer cannot be determined, clearly say so.
3. Keep the answer under 200 words.
4. Use professional business language.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "user": current_user.email,
        "question": request.question,
        "answer": response.text
    }