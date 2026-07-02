from fastapi import APIRouter, HTTPException, Depends

from app.data_manager import data_manager
from app.analytics import calculate_kpis
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/kpis")
def get_kpis(current_user=Depends(get_current_user)):

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    return calculate_kpis(df)