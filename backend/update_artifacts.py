"""
Update existing artifacts to use local file paths instead of external URLs.
Run this once to migrate existing data.
"""
from app.database import SessionLocal
from app.models import Artifact

db = SessionLocal()

try:
    artifacts = db.query(Artifact).all()
    updates = {
        1: "/api/artifacts/files/email1.png",
        2: "/api/artifacts/files/siem_log.txt",
        3: "/api/artifacts/files/nmap_scan.txt",
        4: "/api/artifacts/files/ransomware.png",
        5: "/api/artifacts/files/intel_report.pdf",
    }
    
    for artifact in artifacts:
        if artifact.id in updates:
            old_url = artifact.file_url
            artifact.file_url = updates[artifact.id]
            print(f"Updated artifact {artifact.id} ({artifact.name}): {old_url} -> {artifact.file_url}")
    
    db.commit()
    print(f"Updated {len(updates)} artifacts")
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()

