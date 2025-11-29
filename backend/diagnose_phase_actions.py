"""
Diagnostic script to check if phase-specific actions are in the database
and being returned correctly.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Game
import json

db: Session = SessionLocal()

try:
    print("=" * 60)
    print("DIAGNOSTIC: Phase-Specific Actions")
    print("=" * 60)
    print()
    
    # Check if column exists
    print("1. Checking if 'available_actions' column exists...")
    from sqlalchemy import inspect
    inspector = inspect(db.bind)
    columns = [col['name'] for col in inspector.get_columns('scenario_phases')]
    if 'available_actions' in columns:
        print("   ✓ Column 'available_actions' exists")
    else:
        print("   ❌ Column 'available_actions' DOES NOT EXIST")
        print("   → Run migration: alembic upgrade head")
        sys.exit(1)
    print()
    
    # Check Ransomware scenario
    print("2. Checking Ransomware scenario phases...")
    scenario = db.query(Scenario).filter(Scenario.name == "Ransomware Incident Response").first()
    if not scenario:
        print("   ❌ Ransomware scenario not found!")
        sys.exit(1)
    
    print(f"   ✓ Found scenario: {scenario.name} (ID: {scenario.id})")
    print()
    
    # Check each phase
    phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).order_by(ScenarioPhase.order_index).all()
    
    print("3. Checking phase data:")
    for phase in phases:
        print(f"\n   Phase {phase.order_index + 1}: {phase.name}")
        print(f"   Phase ID: {phase.id}")
        
        if phase.available_actions is None:
            print("   ❌ available_actions is NULL")
        else:
            print(f"   ✓ available_actions is set")
            print(f"   Type: {type(phase.available_actions)}")
            
            if isinstance(phase.available_actions, dict):
                if 'red' in phase.available_actions:
                    red_count = len(phase.available_actions['red'])
                    print(f"   ✓ Red team actions: {red_count} actions")
                    if red_count > 0:
                        print(f"      First action: {phase.available_actions['red'][0].get('name', 'N/A')}")
                else:
                    print("   ❌ No 'red' key in available_actions")
                
                if 'blue' in phase.available_actions:
                    blue_count = len(phase.available_actions['blue'])
                    print(f"   ✓ Blue team actions: {blue_count} actions")
                    if blue_count > 0:
                        print(f"      First action: {phase.available_actions['blue'][0].get('name', 'N/A')}")
                else:
                    print("   ❌ No 'blue' key in available_actions")
            else:
                print(f"   ⚠️  available_actions is not a dict: {type(phase.available_actions)}")
                print(f"   Value: {phase.available_actions}")
    
    print()
    print("4. Checking active games...")
    games = db.query(Game).filter(Game.status.in_(['in_progress', 'briefing'])).all()
    if games:
        for game in games:
            print(f"\n   Game ID: {game.id}")
            print(f"   Status: {game.status}")
            print(f"   Current Phase ID: {game.current_phase_id}")
            
            if game.current_phase_id:
                current_phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == game.current_phase_id).first()
                if current_phase:
                    print(f"   Current Phase: {current_phase.name} (order_index: {current_phase.order_index})")
                    if current_phase.available_actions:
                        print(f"   ✓ Phase has available_actions")
                        if isinstance(current_phase.available_actions, dict):
                            print(f"      Keys: {list(current_phase.available_actions.keys())}")
                    else:
                        print(f"   ❌ Phase has NO available_actions")
    else:
        print("   No active games found")
    
    print()
    print("=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

