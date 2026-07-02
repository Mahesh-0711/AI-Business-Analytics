from fastapi import APIRouter, HTTPException

from app.data_manager import data_manager
from app.analytics import generate_insights

router = APIRouter()


@router.get("/insights")
def get_insights():

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    return {
        "insights": generate_insights(df)
    }