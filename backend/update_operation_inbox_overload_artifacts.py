"""
Update existing Operation Inbox Overload artifacts with generated content.
This script updates artifacts that were created with placeholder content.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact

# Import artifact generation functions
import generate_operation_inbox_overload_artifacts as gen_module

db: Session = SessionLocal()

# Map phase indices to artifact generation functions
ARTIFACT_FUNCTIONS = {
    (0, "red"): gen_module.generate_phase0_red,
    (0, "blue"): gen_module.generate_phase0_blue,
    (1, "red"): gen_module.generate_phase1_red,
    (1, "blue"): gen_module.generate_phase1_blue,
    (2, "red"): gen_module.generate_phase2_red,
    (2, "blue"): gen_module.generate_phase2_blue,
    (3, "red"): gen_module.generate_phase3_red,
    (3, "blue"): gen_module.generate_phase3_blue,
    (4, "red"): gen_module.generate_phase4_red,
    (4, "blue"): gen_module.generate_phase4_blue,
}

try:
    # Find the Operation Inbox Overload scenario
    scenario = db.query(Scenario).filter(Scenario.name == "Operation Inbox Overload").first()
    
    if not scenario:
        print("❌ Scenario 'Operation Inbox Overload' not found!")
        print("   Please create the scenario first using create_operation_inbox_overload_scenario.py")
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
    
    updated_count = 0
    
    # Update artifacts for each phase
    for phase in phases:
        print(f"Processing Phase {phase.order_index}: {phase.name}")
        
        # Get artifacts for this phase
        artifacts = phase.artifacts
        
        for artifact in artifacts:
            # Determine if this is a red or blue artifact based on name
            is_red = "Red Team" in artifact.name or "red" in artifact.name.lower()
            is_blue = "Blue Team" in artifact.name or "blue" in artifact.name.lower() or "Defender" in artifact.name
            
            team_role = None
            if is_red:
                team_role = "red"
            elif is_blue:
                team_role = "blue"
            
            if team_role:
                key = (phase.order_index, team_role)
                if key in ARTIFACT_FUNCTIONS:
                    # Check if content needs updating (placeholder or empty)
                    needs_update = (
                        not artifact.content or 
                        "TODO: implement artifact generation" in artifact.content or
                        "[Artifact content generation failed" in artifact.content
                    )
                    
                    if needs_update:
                        print(f"  📝 Updating {team_role} artifact: {artifact.name}")
                        artifact.content = ARTIFACT_FUNCTIONS[key]()
                        updated_count += 1
                    else:
                        print(f"  ⏭️  Skipping {team_role} artifact (already has content): {artifact.name}")
                else:
                    print(f"  ⚠️  No generator function for {team_role} artifact in phase {phase.order_index}")
            else:
                print(f"  ⚠️  Could not determine team role for artifact: {artifact.name}")
        
        print()
    
    db.commit()
    
    print("=" * 60)
    print("✅ Artifact Update Complete!")
    print("=" * 60)
    print(f"Updated: {updated_count} artifacts")
    print()
    print("Artifacts now have generated content.")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

