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
# Files are stored in /app/artifacts/files/ to match URLs like /api/artifacts/files/{filename}
ARTIFACTS_DIR = Path("/app/artifacts/files")
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
    import logging
    logger = logging.getLogger(__name__)
    
    # Security: prevent directory traversal
    safe_filename = Path(filename).name
    file_path = ARTIFACTS_DIR / safe_filename
    
    # Debug logging
    logger.info(f"Artifact request: filename='{filename}', safe_filename='{safe_filename}'")
    logger.info(f"ARTIFACTS_DIR: {ARTIFACTS_DIR}, exists={ARTIFACTS_DIR.exists()}")
    logger.info(f"file_path: {file_path}, exists={file_path.exists()}, is_file={file_path.is_file() if file_path.exists() else 'N/A'}")
    
    # Check if directory exists
    if not ARTIFACTS_DIR.exists():
        logger.error(f"Artifacts directory does not exist: {ARTIFACTS_DIR}")
        # Try to create it
        try:
            ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created artifacts directory: {ARTIFACTS_DIR}")
        except Exception as e:
            logger.error(f"Failed to create artifacts directory: {e}")
            raise HTTPException(status_code=500, detail="Artifacts directory not accessible")
    
    # List files in directory for debugging
    if ARTIFACTS_DIR.exists():
        files = list(ARTIFACTS_DIR.glob("*.txt"))
        logger.info(f"Found {len(files)} .txt files in directory")
        if safe_filename in [f.name for f in files]:
            logger.info(f"File '{safe_filename}' is in the directory listing")
        else:
            logger.warning(f"File '{safe_filename}' NOT in directory listing. Available files: {[f.name for f in files[:5]]}")
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        # Try absolute path
        abs_path = file_path.resolve()
        logger.error(f"Absolute path: {abs_path}, exists={abs_path.exists()}")
        raise HTTPException(status_code=404, detail=f"File not found: {safe_filename}")
    
    if not file_path.is_file():
        logger.error(f"Path exists but is not a file: {file_path}")
        raise HTTPException(status_code=404, detail=f"File not found: {safe_filename}")
    
    logger.info(f"File found, serving: {file_path} (size: {file_path.stat().st_size} bytes)")
    
    # Determine media type based on file extension
    media_type = None
    if safe_filename.endswith('.txt'):
        media_type = 'text/plain'
    elif safe_filename.endswith('.png'):
        media_type = 'image/png'
    elif safe_filename.endswith('.jpg') or safe_filename.endswith('.jpeg'):
        media_type = 'image/jpeg'
    elif safe_filename.endswith('.pdf'):
        media_type = 'application/pdf'
    
    return FileResponse(
        file_path,
        media_type=media_type,
        filename=safe_filename
    )

