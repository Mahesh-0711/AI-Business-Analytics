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
        .filter(Dataset.user_id == current_user.id)
        .order_by(Dataset.uploaded_at.desc())
        .all()
    )

    return {
        "user": current_user.email,
        "total_datasets": len(datasets),
        "datasets": [
            {
                "id": dataset.id,
                "filename": dataset.filename,
                "rows": dataset.rows,
                "columns": dataset.columns,
                "uploaded_at": dataset.uploaded_at
            }
            for dataset in datasets
        ]
    }