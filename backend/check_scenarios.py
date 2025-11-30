"""
Check what scenarios exist in the database.
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal
from app.models import Scenario

db = SessionLocal()

try:
    scenarios = db.query(Scenario).all()
    
    print("=" * 60)
    print("SCENARIOS IN DATABASE")
    print("=" * 60)
    print()
    
    if not scenarios:
        print("No scenarios found in database")
    else:
        for scenario in scenarios:
            print(f"ID: {scenario.id}")
            print(f"Name: {scenario.name}")
            print(f"Description: {scenario.description[:100] if scenario.description else 'None'}...")
            print(f"Phases: {len(scenario.phases)}")
            print()
    
    print("=" * 60)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
