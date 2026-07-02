from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Dataset, User

router = APIRouter()


@router.get("/my-datasets")
def my_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    datasets = (
        db.query(Dataset)
        .filter(
            Dataset.user_id == current_user.id
        )
        .all()
    )

    return [
        {
            "id": item.id,
            "filename": item.filename,
            "rows": item.rows,
            "columns": item.columns,
            "uploaded_at": item.uploaded_at
        }
        for item in datasets
    ]