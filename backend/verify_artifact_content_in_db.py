"""
Verify artifact content is actually in the database.
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal
from app.models import Artifact
from sqlalchemy import text

db = SessionLocal()

try:
    # Check specific artifacts from the test
    artifact_ids = [137, 138, 139]
    
    for artifact_id in artifact_ids:
        # Query directly with SQL to see raw database value
        result = db.execute(
            text("SELECT id, name, content IS NULL as content_is_null, LENGTH(content) as content_length FROM artifacts WHERE id = :id"),
            {"id": artifact_id}
        ).first()
        
        if result:
            print(f"Artifact ID {artifact_id} ({result.name}):")
            print(f"  Content is NULL: {result.content_is_null}")
            print(f"  Content length: {result.content_length}")
            
            # Also check via ORM
            artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
            if artifact:
                print(f"  ORM content is None: {artifact.content is None}")
                print(f"  ORM content length: {len(artifact.content) if artifact.content else 0}")
                # Force refresh from database
                db.refresh(artifact)
                print(f"  After refresh - content is None: {artifact.content is None}")
                print(f"  After refresh - content length: {len(artifact.content) if artifact.content else 0}")
            print()
        else:
            print(f"Artifact ID {artifact_id} not found")
            print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

