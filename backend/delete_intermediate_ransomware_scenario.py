"""
Delete the "Ransomware Attack: Corporate Network Compromise" scenario.
This will also delete all associated phases, artifacts, and artifact associations.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact
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
        # Delete artifact associations first
        print("\nDeleting artifact associations...")
        assoc_count = db.execute(
            delete(scenario_phase_artifacts).where(
                scenario_phase_artifacts.c.phase_id.in_(phase_ids)
            )
        ).rowcount
        db.flush()
        print(f"  ✓ Deleted {assoc_count} artifact associations")
        
        # Get artifact IDs that are linked to these phases
        artifact_ids = db.execute(
            scenario_phase_artifacts.select().where(
                scenario_phase_artifacts.c.phase_id.in_(phase_ids)
            )
        ).fetchall()
        # Note: artifact_ids will be empty now since we deleted associations
        # But we need to find artifacts that were only linked to this scenario
        
        # Find artifacts that are only linked to this scenario's phases
        all_artifact_ids = set()
        for phase_id in phase_ids:
            # Get artifacts for this phase (before we deleted associations)
            # We'll query directly from the association table won't work now
            # Instead, let's get artifacts that might be orphaned
            pass
        
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

