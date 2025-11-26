"""
Script to update existing scenario with team-specific artifacts.
This deletes the old scenario and recreates it with team-specific artifacts.

Deletion order respects all foreign key constraints:
1. player_votes references: player_id, phase_id, game_id, team_id
2. phase_decisions references: phase_id, game_id, team_id
3. score_events references: phase_id, game_id, team_id
4. players references: game_id, team_id
5. teams references: game_id
6. games references: scenario_id, current_phase_id
7. scenario_phase_artifacts references: phase_id, artifact_id
8. scenario_phases references: scenario_id
9. scenario
"""
from app.database import SessionLocal
from app.models import (
    Scenario, ScenarioPhase, Artifact, scenario_phase_artifacts,
    PhaseDecision, PlayerVote, ScoreEvent, Game, Team, Player
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
        
        # Get all games that reference this scenario
        games = db.query(Game).filter(Game.scenario_id == scenario_id).all()
        game_ids = [g.id for g in games]
        
        if game_ids:
            # Get all teams and players for these games
            teams = db.query(Team).filter(Team.game_id.in_(game_ids)).all()
            team_ids = [t.id for t in teams]
            players = db.query(Player).filter(Player.game_id.in_(game_ids)).all()
            player_ids = [p.id for p in players]
            
            # Step 1: Update games to set current_phase_id to NULL (references phase_id)
            games_updated = db.query(Game).filter(
                Game.current_phase_id.in_(phase_id_list)
            ).update({Game.current_phase_id: None}, synchronize_session=False)
            print(f"Updated {games_updated} games to remove phase references")
            
            # Step 2: Delete player_votes FIRST (references player_id, phase_id, game_id, team_id)
            # Must be deleted before players
            if player_ids:
                player_votes_count = db.query(PlayerVote).filter(
                    PlayerVote.player_id.in_(player_ids)
                ).delete(synchronize_session=False)
                print(f"Deleted {player_votes_count} player votes")
            
            # Also delete any player_votes that reference these phases (in case player_ids is empty)
            if phase_id_list:
                player_votes_count2 = db.query(PlayerVote).filter(
                    PlayerVote.phase_id.in_(phase_id_list)
                ).delete(synchronize_session=False)
                if player_votes_count2 > 0:
                    print(f"Deleted {player_votes_count2} additional player votes by phase")
            
            # Step 3: Delete phase_decisions (references phase_id, game_id, team_id)
            if phase_id_list:
                phase_decisions_count = db.query(PhaseDecision).filter(
                    PhaseDecision.phase_id.in_(phase_id_list)
                ).delete(synchronize_session=False)
                print(f"Deleted {phase_decisions_count} phase decisions")
            
            # Step 4: Delete score_events (references phase_id, game_id, team_id)
            if phase_id_list:
                score_events_count = db.query(ScoreEvent).filter(
                    ScoreEvent.phase_id.in_(phase_id_list)
                ).delete(synchronize_session=False)
                print(f"Deleted {score_events_count} score events")
            
            # Step 5: Delete players (references game_id, team_id)
            if player_ids:
                players_count = db.query(Player).filter(
                    Player.id.in_(player_ids)
                ).delete(synchronize_session=False)
                print(f"Deleted {players_count} players")
            
            # Step 6: Delete teams (references game_id)
            if team_ids:
                teams_count = db.query(Team).filter(
                    Team.id.in_(team_ids)
                ).delete(synchronize_session=False)
                print(f"Deleted {teams_count} teams")
            
            # Step 7: Delete games (references scenario_id)
            games_count = db.query(Game).filter(
                Game.id.in_(game_ids)
            ).delete(synchronize_session=False)
            print(f"Deleted {games_count} games")
        
        # Step 8: Delete artifact associations (references phase_id, artifact_id)
        if phase_id_list:
            db.execute(
                delete(scenario_phase_artifacts).where(
                    scenario_phase_artifacts.c.phase_id.in_(phase_id_list)
                )
            )
            print(f"Deleted artifact associations for {len(phase_id_list)} phases")
        
        # Step 9: Delete phases (references scenario_id)
        if phases:
            for phase in phases:
                db.delete(phase)
            print(f"Deleted {len(phases)} phases")
        
        # Step 10: Delete scenario
        db.delete(scenario)
        db.commit()
        print('Scenario deleted successfully. Now run seed_data.py to recreate it with team-specific artifacts.')
    else:
        print('Scenario not found')
finally:
    db.close()
