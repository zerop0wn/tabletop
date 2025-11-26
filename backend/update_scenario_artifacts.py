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
        
        # Get all phase IDs for this scenario
        phase_ids = db.query(ScenarioPhase.id).filter(ScenarioPhase.scenario_id == scenario.id).all()
        phase_id_list = [p[0] for p in phase_ids]
        
        if phase_id_list:
            # Delete artifact associations
            db.execute(
                delete(scenario_phase_artifacts).where(
                    scenario_phase_artifacts.c.phase_id.in_(phase_id_list)
                )
            )
            print(f"Deleted artifact associations for {len(phase_id_list)} phases")
        
        # Delete the scenario (cascade will handle phases and artifacts)
        db.delete(scenario)
        db.commit()
        print('Scenario deleted successfully. Now run seed_data.py to recreate it with team-specific artifacts.')
    else:
        print('Scenario not found')
finally:
    db.close()

