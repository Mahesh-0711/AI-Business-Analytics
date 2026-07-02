import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.analytics import load_dataset, clean_data
from app.data_manager import data_manager
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Dataset, User

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = load_dataset(filepath)

    df = clean_data(df)

    data_manager.set_data(df)

    dataset = Dataset(
        user_id=current_user.id,
        filename=file.filename,
        filepath=filepath,
        rows=int(len(df)),
        columns=int(len(df.columns))
    )

    db.add(dataset)

    db.commit()

    db.refresh(dataset)

    return {
        "status": "success",
        "filename": file.filename,
        "rows": int(len(df)),
        "columns": int(len(df.columns))
    }