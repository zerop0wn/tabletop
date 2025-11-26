"""
Script to update existing scenario with team-specific artifacts.
This deletes the old scenario and recreates it with team-specific artifacts.
"""
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact, scenario_phase_artifacts
from sqlalchemy import delete

db = SessionLocal()
try:
    scenario = db.query(Scenario).filter(Scenario.name == 'Ransomware Incident Response').first()
    if scenario:
        print(f"Found scenario: {scenario.id}")
        scenario_id = scenario.id
        
        # Get all phase IDs for this scenario
        phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario_id).all()
        phase_id_list = [p.id for p in phases]
        
        if phase_id_list:
            # Delete artifact associations first
            db.execute(
                delete(scenario_phase_artifacts).where(
                    scenario_phase_artifacts.c.phase_id.in_(phase_id_list)
                )
            )
            print(f"Deleted artifact associations for {len(phase_id_list)} phases")
            
            # Delete phases explicitly (before deleting scenario to avoid constraint violation)
            for phase in phases:
                db.delete(phase)
            print(f"Deleted {len(phases)} phases")
        
        # Now delete the scenario
        db.delete(scenario)
        db.commit()
        print('Scenario deleted successfully. Now run seed_data.py to recreate it with team-specific artifacts.')
    else:
        print('Scenario not found')
finally:
    db.close()

