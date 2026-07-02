from fastapi import APIRouter, HTTPException, Depends

from app.data_manager import data_manager
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "numeric_columns": list(
            df.select_dtypes(include="number").columns
        ),
        "categorical_columns": list(
            df.select_dtypes(exclude="number").columns
        ),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    }