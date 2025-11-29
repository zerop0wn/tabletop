"""
Diagnostic script to check why artifacts aren't showing.
Checks artifact creation, linking, and file existence.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact
from sqlalchemy import select
from app.models import scenario_phase_artifacts
from pathlib import Path

db: Session = SessionLocal()

try:
    print("=" * 60)
    print("DIAGNOSTIC: Artifacts for New Ransomware Scenario")
    print("=" * 60)
    print()
    
    # Find scenario
    scenario_name = "Ransomware Attack: Advanced Persistent Threat"
    scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if not scenario:
        print(f"❌ Scenario '{scenario_name}' not found!")
        sys.exit(1)
    
    print(f"✓ Found scenario: {scenario.name} (ID: {scenario.id})")
    print()
    
    # Check phases
    phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).order_by(ScenarioPhase.order_index).all()
    print(f"Found {len(phases)} phases")
    print()
    
    # Check artifacts for each phase
    for phase in phases:
        print(f"Phase {phase.order_index + 1}: {phase.name} (ID: {phase.id})")
        
        # Get artifact links
        artifact_links = db.execute(
            select(scenario_phase_artifacts).where(
                scenario_phase_artifacts.c.phase_id == phase.id
            )
        ).fetchall()
        
        print(f"  Artifact links in database: {len(artifact_links)}")
        
        if artifact_links:
            for link in artifact_links:
                artifact_id = link.artifact_id
                team_role = link.team_role
                artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
                
                if artifact:
                    print(f"    - Artifact ID {artifact_id}: {artifact.name}")
                    print(f"      Team Role: {team_role}")
                    print(f"      File URL: {artifact.file_url}")
                    
                    # Check if file exists
                    if artifact.file_url:
                        # Extract filename from URL
                        filename = artifact.file_url.split('/')[-1]
                        file_path = Path("/app/artifacts/files") / filename
                        if file_path.exists():
                            print(f"      ✓ File exists: {file_path}")
                        else:
                            print(f"      ❌ File NOT found: {file_path}")
                    else:
                        print(f"      ⚠️  No file_url set")
                else:
                    print(f"    ❌ Artifact ID {artifact_id} not found in artifacts table!")
        else:
            print(f"  ❌ No artifact links found for this phase!")
        
        print()
    
    # Check total artifacts
    all_artifacts = db.query(Artifact).all()
    print(f"Total artifacts in database: {len(all_artifacts)}")
    
    # Check artifact files directory
    artifacts_dir = Path("/app/artifacts/files")
    if artifacts_dir.exists():
        files = list(artifacts_dir.glob("*.txt"))
        print(f"Artifact files in /app/artifacts/files/: {len(files)}")
        if files:
            print("  Files found:")
            for f in files[:10]:  # Show first 10
                print(f"    - {f.name}")
        else:
            print("  ❌ No .txt files found in /app/artifacts/files/")
    else:
        print(f"❌ Directory /app/artifacts/files/ does not exist!")
    
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

