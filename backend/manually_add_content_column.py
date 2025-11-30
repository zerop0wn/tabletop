"""
Manually add content column to artifacts table if migration didn't run.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='artifacts' AND column_name='content'
        """))
        
        if result.fetchone():
            print("✓ content column already exists")
        else:
            print("Adding content column to artifacts table...")
            conn.execute(text("ALTER TABLE artifacts ADD COLUMN content TEXT"))
            conn.commit()
            print("✓ content column added successfully")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

