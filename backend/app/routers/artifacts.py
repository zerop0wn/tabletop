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


@router.get("/debug/list")
async def list_artifact_files():
    """Debug endpoint to list all artifact files."""
    import sys
    files = []
    if ARTIFACTS_DIR.exists():
        try:
            for f in ARTIFACTS_DIR.iterdir():
                if f.is_file():
                    files.append({
                        "name": f.name,
                        "size": f.stat().st_size,
                        "exists": f.exists(),
                        "path": str(f)
                    })
        except Exception as e:
            return {"error": str(e), "artifacts_dir": str(ARTIFACTS_DIR), "dir_exists": ARTIFACTS_DIR.exists()}
    
    return {
        "artifacts_dir": str(ARTIFACTS_DIR),
        "dir_exists": ARTIFACTS_DIR.exists(),
        "file_count": len(files),
        "files": sorted(files, key=lambda x: x["name"])
    }


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
async def get_artifact_file(filename: str, db: Session = Depends(get_db)):
    """Serve artifact files from filesystem (fallback for legacy artifacts)."""
    # Security: prevent directory traversal
    safe_filename = Path(filename).name
    file_path = ARTIFACTS_DIR / safe_filename
    
    # Check if file exists
    if file_path.exists() and file_path.is_file():
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
    
    raise HTTPException(status_code=404, detail=f"File not found: {safe_filename}")


@router.get("/{artifact_id}/content")
async def get_artifact_content(artifact_id: int, db: Session = Depends(get_db)):
    """Get artifact content from database."""
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail=f"Artifact not found: {artifact_id}")
    
    # Return content from database if available
    if artifact.content:
        from fastapi.responses import Response
        return Response(
            content=artifact.content,
            media_type="text/plain",
            headers={"Content-Disposition": f'inline; filename="{artifact.name}.txt"'}
        )
    
    # Fallback to file URL if content not in database
    if artifact.file_url:
        # Try to serve from file system as fallback
        filename = artifact.file_url.split("/")[-1]
        return await get_artifact_file(filename)
    
    raise HTTPException(status_code=404, detail="Artifact content not available")

