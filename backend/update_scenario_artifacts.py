"""
Script to update existing scenario with team-specific artifacts.
This deletes the old scenario and recreates it with team-specific artifacts.
"""
from app.database import SessionLocal
from app.models import (
    Scenario, ScenarioPhase, Artifact, scenario_phase_artifacts,
    PhaseDecision, PlayerVote, ScoreEvent
)
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
            # Delete in order to respect foreign key constraints:
            # 1. Update games to set current_phase_id to NULL (references phase_id)
            from app.models import Game
            games_updated = db.query(Game).filter(
                Game.current_phase_id.in_(phase_id_list)
            ).update({Game.current_phase_id: None}, synchronize_session=False)
            print(f"Updated {games_updated} games to remove phase references")
            
            # 2. Delete phase_decisions (references phase_id)
            phase_decisions_count = db.query(PhaseDecision).filter(
                PhaseDecision.phase_id.in_(phase_id_list)
            ).delete(synchronize_session=False)
            print(f"Deleted {phase_decisions_count} phase decisions")
            
            # 3. Delete player_votes (references phase_id)
            player_votes_count = db.query(PlayerVote).filter(
                PlayerVote.phase_id.in_(phase_id_list)
            ).delete(synchronize_session=False)
            print(f"Deleted {player_votes_count} player votes")
            
            # 4. Delete score_events (references phase_id)
            score_events_count = db.query(ScoreEvent).filter(
                ScoreEvent.phase_id.in_(phase_id_list)
            ).delete(synchronize_session=False)
            print(f"Deleted {score_events_count} score events")
            
            # 5. Delete artifact associations
            db.execute(
                delete(scenario_phase_artifacts).where(
                    scenario_phase_artifacts.c.phase_id.in_(phase_id_list)
                )
            )
            print(f"Deleted artifact associations for {len(phase_id_list)} phases")
            
            # 6. Delete phases explicitly (before deleting scenario to avoid constraint violation)
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

