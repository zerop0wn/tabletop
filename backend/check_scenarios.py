"""
Check if scenarios exist in the database and restore if needed.
"""
from app.database import SessionLocal
from app.models import Scenario

db = SessionLocal()
try:
    scenarios = db.query(Scenario).all()
    
    if scenarios:
        print(f"Found {len(scenarios)} scenario(s):")
        for scenario in scenarios:
            print(f"  - ID: {scenario.id}, Name: {scenario.name}")
    else:
        print("No scenarios found in database.")
        print("Run 'python seed_data.py' to create scenarios.")
finally:
    db.close()

