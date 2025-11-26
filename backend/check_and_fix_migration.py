"""
Check if team_role column exists and add it if missing.
"""
from app.database import SessionLocal, engine
from sqlalchemy import inspect, text

db = SessionLocal()
try:
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('scenario_phase_artifacts')]
    
    print(f"Current columns in scenario_phase_artifacts: {columns}")
    
    if 'team_role' not in columns:
        print("team_role column is missing. Adding it now...")
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE scenario_phase_artifacts ADD COLUMN team_role VARCHAR"))
            conn.commit()
        print("team_role column added successfully!")
    else:
        print("team_role column already exists.")
finally:
    db.close()

