"""
Check artifacts for the intermediate ransomware scenario.
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact, scenario_phase_artifacts
from sqlalchemy import select

db = SessionLocal()

try:
    scenario = db.query(Scenario).filter(Scenario.name == "Ransomware Attack: Corporate Network Compromise").first()
    
    if not scenario:
        print("❌ Scenario not found")
        sys.exit(1)
    
    print("=" * 60)
    print(f"SCENARIO: {scenario.name} (ID: {scenario.id})")
    print("=" * 60)
    print()
    
    phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).order_by(ScenarioPhase.order_index).all()
    
    for phase in phases:
        print(f"Phase {phase.order_index + 1}: {phase.name} (ID: {phase.id})")
        
        # Get artifacts for this phase
        artifact_ids = db.execute(
            select(scenario_phase_artifacts.c.artifact_id, scenario_phase_artifacts.c.team_role)
            .where(scenario_phase_artifacts.c.phase_id == phase.id)
        ).all()
        
        if not artifact_ids:
            print("  ❌ No artifacts linked to this phase")
        else:
            print(f"  ✓ {len(artifact_ids)} artifact(s) linked:")
            for artifact_id, team_role in artifact_ids:
                artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
                if artifact:
                    has_content = bool(artifact.content)
                    content_length = len(artifact.content) if artifact.content else 0
                    print(f"    - {artifact.name} (ID: {artifact.id}, Team: {team_role or 'both'})")
                    print(f"      Content: {'✓' if has_content else '✗'} ({content_length} chars)")
                    if not has_content:
                        print(f"      ⚠️  WARNING: Artifact has no content!")
                else:
                    print(f"    - ❌ Artifact ID {artifact_id} not found")
        print()
    
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

