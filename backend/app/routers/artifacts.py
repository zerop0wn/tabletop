from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
import shutil
from pathlib import Path
from app.database import get_db
from app.auth import get_current_gm
from app.models import Artifact
from app.schemas import ArtifactResponse

router = APIRouter()

# Create artifacts directory if it doesn't exist
ARTIFACTS_DIR = Path("/app/artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True, parents=True)


@router.post("/upload")
async def upload_artifact(
    file: UploadFile = File(...),
    artifact_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_gm=Depends(get_current_gm)
):
    """Upload an artifact file. If artifact_id is provided, update that artifact's file_url."""
    # Save file with a safe filename
    safe_filename = file.filename.replace(" ", "_")
    file_path = ARTIFACTS_DIR / safe_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_url = f"/api/artifacts/files/{safe_filename}"
    
    if artifact_id:
        # Update existing artifact
        artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
        if not artifact:
            raise HTTPException(status_code=404, detail="Artifact not found")
        artifact.file_url = file_url
        db.commit()
        db.refresh(artifact)
        return ArtifactResponse(
            id=artifact.id,
            name=artifact.name,
            type=artifact.type,
            description=artifact.description,
            file_url=artifact.file_url,
            embed_url=artifact.embed_url
        )
    
    # Return file info
    return {"filename": safe_filename, "file_url": file_url, "message": "File uploaded successfully"}


@router.get("/files/{filename}")
async def get_artifact_file(filename: str):
    """Serve artifact files."""
    # Security: prevent directory traversal
    safe_filename = Path(filename).name
    file_path = ARTIFACTS_DIR / safe_filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)

