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
    import sys
    
    # Force output immediately
    sys.stderr.flush()
    sys.stdout.flush()
    
    logger = logging.getLogger(__name__)
    
    # Security: prevent directory traversal
    safe_filename = Path(filename).name
    file_path = ARTIFACTS_DIR / safe_filename
    
    # Debug output - use print to ensure it shows up
    print(f"[ARTIFACT DEBUG] Request: filename='{filename}', safe_filename='{safe_filename}'", file=sys.stderr, flush=True)
    print(f"[ARTIFACT DEBUG] ARTIFACTS_DIR: {ARTIFACTS_DIR}, exists={ARTIFACTS_DIR.exists()}", file=sys.stderr, flush=True)
    print(f"[ARTIFACT DEBUG] file_path: {file_path}, exists={file_path.exists()}", file=sys.stderr, flush=True)
    
    # Check if directory exists
    if not ARTIFACTS_DIR.exists():
        print(f"[ARTIFACT ERROR] Artifacts directory does not exist: {ARTIFACTS_DIR}", file=sys.stderr)
        # Try to create it
        try:
            ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
            print(f"[ARTIFACT DEBUG] Created artifacts directory: {ARTIFACTS_DIR}", file=sys.stderr)
        except Exception as e:
            print(f"[ARTIFACT ERROR] Failed to create artifacts directory: {e}", file=sys.stderr)
            raise HTTPException(status_code=500, detail="Artifacts directory not accessible")
    
    # List files in directory for debugging
    if ARTIFACTS_DIR.exists():
        files = list(ARTIFACTS_DIR.glob("*.txt"))
        print(f"[ARTIFACT DEBUG] Found {len(files)} .txt files in directory", file=sys.stderr)
        file_names = [f.name for f in files]
        if safe_filename in file_names:
            print(f"[ARTIFACT DEBUG] File '{safe_filename}' IS in directory listing", file=sys.stderr)
        else:
            print(f"[ARTIFACT ERROR] File '{safe_filename}' NOT in directory listing", file=sys.stderr)
            print(f"[ARTIFACT DEBUG] Available files (first 10): {file_names[:10]}", file=sys.stderr)
    
    # Double-check file existence with multiple methods
    file_exists = file_path.exists()
    file_is_file = file_path.is_file() if file_exists else False
    
    # Also try resolving the path
    try:
        resolved_path = file_path.resolve()
        resolved_exists = resolved_path.exists()
        print(f"[ARTIFACT DEBUG] Resolved path: {resolved_path}, exists={resolved_exists}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[ARTIFACT DEBUG] Could not resolve path: {e}", file=sys.stderr, flush=True)
        resolved_exists = False
    
    if not file_exists and not resolved_exists:
        print(f"[ARTIFACT ERROR] File not found: {file_path}", file=sys.stderr, flush=True)
        
        # List all files to help debug
        if ARTIFACTS_DIR.exists():
            try:
                all_files = list(ARTIFACTS_DIR.iterdir())
                all_file_names = [f.name for f in all_files if f.is_file()]
                print(f"[ARTIFACT DEBUG] All files in directory ({len(all_file_names)}): {all_file_names[:20]}", file=sys.stderr, flush=True)
                
                # Check for exact match (case-insensitive)
                matching = [f for f in all_file_names if f.lower() == safe_filename.lower()]
                if matching:
                    print(f"[ARTIFACT DEBUG] Case-insensitive match found: {matching}", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"[ARTIFACT ERROR] Could not list directory: {e}", file=sys.stderr, flush=True)
        
        # More detailed error message
        error_detail = f"File not found: {safe_filename}. "
        if ARTIFACTS_DIR.exists():
            try:
                similar_files = [f.name for f in ARTIFACTS_DIR.glob("*.txt") if safe_filename.lower() in f.name.lower() or f.name.lower() in safe_filename.lower()]
                if similar_files:
                    error_detail += f"Similar files found: {similar_files[:5]}"
            except:
                pass
        raise HTTPException(status_code=404, detail=error_detail)
    
    # Use resolved path if original doesn't exist but resolved does
    if not file_exists and resolved_exists:
        file_path = resolved_path
        print(f"[ARTIFACT DEBUG] Using resolved path: {file_path}", file=sys.stderr, flush=True)
    
    if not file_path.is_file():
        print(f"[ARTIFACT ERROR] Path exists but is not a file: {file_path}", file=sys.stderr)
        raise HTTPException(status_code=404, detail=f"File not found: {safe_filename}")
    
    file_size = file_path.stat().st_size
    print(f"[ARTIFACT DEBUG] File found, serving: {file_path} (size: {file_size} bytes)", file=sys.stderr)
    
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

