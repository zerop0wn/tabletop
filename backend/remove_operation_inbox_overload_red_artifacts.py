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
        
        # Get Red Team artifact associations for this phase
        red_associations = db.execute(
            scenario_phase_artifacts.select().where(
                scenario_phase_artifacts.c.phase_id == phase.id,
                scenario_phase_artifacts.c.team_role == 'red'
            )
        ).fetchall()
        
        if not red_associations:
            # Fallback: check artifact names if team_role is not set
            artifacts = phase.artifacts
            red_artifacts = []
            for artifact in artifacts:
                # Check if this is a Red Team artifact by name
                is_red = (
                    "Red Team" in artifact.name or 
                    "red" in artifact.name.lower()
                )
                if is_red:
                    red_artifacts.append(artifact)
            
            if red_artifacts:
                # Remove associations first
                for artifact in red_artifacts:
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
            else:
                print(f"  ⏭️  No Red Team artifacts found for this phase")
        else:
            # Remove associations and artifacts using team_role
            artifact_ids = [assoc.artifact_id for assoc in red_associations]
            
            # Remove associations
            for assoc in red_associations:
                db.execute(
                    scenario_phase_artifacts.delete().where(
                        scenario_phase_artifacts.c.phase_id == assoc.phase_id,
                        scenario_phase_artifacts.c.artifact_id == assoc.artifact_id
                    )
                )
            
            # Delete the artifacts themselves
            for artifact_id in artifact_ids:
                artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
                if artifact:
                    print(f"  🗑️  Removed association for: {artifact.name}")
                    db.delete(artifact)
                    removed_count += 1
                    print(f"  ✅ Deleted artifact: {artifact.name}")
        
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

