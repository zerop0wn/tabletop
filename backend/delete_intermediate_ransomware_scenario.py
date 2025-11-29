"""
Delete the "Ransomware Attack: Corporate Network Compromise" scenario.
This will also delete all associated phases, artifacts, and artifact associations.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact, Game
from app.models import scenario_phase_artifacts

db: Session = SessionLocal()

try:
    scenario_name = "Ransomware Attack: Corporate Network Compromise"
    
    print(f"Looking for scenario: '{scenario_name}'...")
    scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if not scenario:
        print(f"❌ Scenario '{scenario_name}' not found.")
        sys.exit(0)
    
    print(f"✓ Found scenario (ID: {scenario.id})")
    print(f"  Name: {scenario.name}")
    
    # Get all phase IDs for this scenario
    phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).all()
    phase_ids = [p.id for p in phases]
    print(f"  Phases: {len(phases)}")
    
    if phase_ids:
        # First, check for games that reference these phases
        print("\nChecking for games using this scenario...")
        games_using_phases = db.query(Game).filter(Game.current_phase_id.in_(phase_ids)).all()
        games_using_scenario = db.query(Game).filter(Game.scenario_id == scenario.id).all()
        all_affected_games = list(set(games_using_phases + games_using_scenario))
        
        if all_affected_games:
            print(f"  Found {len(all_affected_games)} game(s) using this scenario")
            print("  Setting current_phase_id to NULL for affected games...")
            for game in all_affected_games:
                if game.current_phase_id in phase_ids:
                    game.current_phase_id = None
            db.flush()
            print(f"  ✓ Updated {len(all_affected_games)} game(s)")
        else:
            print("  ✓ No games using this scenario")
        
        # Delete artifact associations first
        print("\nDeleting artifact associations...")
        assoc_count = db.execute(
            delete(scenario_phase_artifacts).where(
                scenario_phase_artifacts.c.phase_id.in_(phase_ids)
            )
        ).rowcount
        db.flush()
        print(f"  ✓ Deleted {assoc_count} artifact associations")
        
        # Delete phases
        print("\nDeleting phases...")
        for phase in phases:
            db.delete(phase)
        db.flush()
        print(f"  ✓ Deleted {len(phases)} phases")
    
    # Delete the scenario
    print("\nDeleting scenario...")
    db.delete(scenario)
    db.commit()
    
    print(f"\n✅ Successfully deleted scenario '{scenario_name}'")
    print(f"   Deleted {len(phases)} phases")
    print(f"   Deleted {assoc_count} artifact associations")
    print("\nNote: Artifact files on disk were not deleted.")
    print("      Artifact database records were not deleted (they may be used by other scenarios).")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error deleting scenario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

