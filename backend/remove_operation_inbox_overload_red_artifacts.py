"""
Remove Red Team artifacts from Operation Inbox Overload scenario.
This script removes all Red Team artifacts and their associations.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact
from app.models import scenario_phase_artifacts

db: Session = SessionLocal()

try:
    # Find the Operation Inbox Overload scenario
    scenario = db.query(Scenario).filter(Scenario.name == "Operation Inbox Overload").first()
    
    if not scenario:
        print("❌ Scenario 'Operation Inbox Overload' not found!")
        sys.exit(1)
    
    print(f"✓ Found scenario: {scenario.name} (ID: {scenario.id})")
    print()
    
    # Get all phases for this scenario
    phases = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == scenario.id
    ).order_by(ScenarioPhase.order_index).all()
    
    if not phases:
        print("❌ No phases found for this scenario!")
        sys.exit(1)
    
    print(f"✓ Found {len(phases)} phases")
    print()
    
    removed_count = 0
    
    # Remove Red Team artifacts for each phase
    for phase in phases:
        print(f"Processing Phase {phase.order_index}: {phase.name}")
        
        # Get all artifacts for this phase
        artifacts = phase.artifacts
        
        red_artifacts = []
        for artifact in artifacts:
            # Check if this is a Red Team artifact
            is_red = (
                "Red Team" in artifact.name or 
                "red" in artifact.name.lower() or
                (hasattr(artifact, 'team_role') and artifact.team_role == 'red')
            )
            
            if is_red:
                red_artifacts.append(artifact)
        
        # Remove associations first
        for artifact in red_artifacts:
            # Remove from scenario_phase_artifacts table
            db.execute(
                scenario_phase_artifacts.delete().where(
                    scenario_phase_artifacts.c.phase_id == phase.id,
                    scenario_phase_artifacts.c.artifact_id == artifact.id
                )
            )
            print(f"  🗑️  Removed association for: {artifact.name}")
        
        # Delete the artifacts themselves
        for artifact in red_artifacts:
            db.delete(artifact)
            removed_count += 1
            print(f"  ✅ Deleted artifact: {artifact.name}")
        
        if not red_artifacts:
            print(f"  ⏭️  No Red Team artifacts found for this phase")
        
        print()
    
    db.commit()
    
    print("=" * 60)
    print("✅ Red Team Artifacts Removal Complete!")
    print("=" * 60)
    print(f"Removed: {removed_count} Red Team artifacts")
    print()
    print("All Red Team artifacts have been removed from the scenario.")
    print("Blue Team artifacts remain intact.")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

