"""
Delete the "Ransomware Attack: Corporate Network Compromise" scenario.
This will also delete all associated phases, artifacts, and artifact associations.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from app.database import SessionLocal
from app.models import (
    Scenario, ScenarioPhase, Artifact, Game, Team, Player,
    PlayerVote, PhaseDecision, ScoreEvent, PhaseGMNotes, AfterActionReport
)
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
    
    # First, find and delete games using this scenario
    print("\nChecking for games using this scenario...")
    games_using_phases = db.query(Game).filter(Game.current_phase_id.in_(phase_ids)).all() if phase_ids else []
    games_using_scenario = db.query(Game).filter(Game.scenario_id == scenario.id).all()
    all_affected_games = list(set(games_using_phases + games_using_scenario))
    
    if all_affected_games:
        game_ids = [g.id for g in all_affected_games]
        print(f"  Found {len(all_affected_games)} game(s) using this scenario")
        print("  Deleting games and related data...")
        
        # Delete in correct order to respect foreign key constraints
        # Delete player votes
        votes_count = db.query(PlayerVote).filter(PlayerVote.game_id.in_(game_ids)).count()
        if votes_count > 0:
            db.execute(delete(PlayerVote).where(PlayerVote.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {votes_count} player votes")
        
        # Delete phase decisions
        decisions_count = db.query(PhaseDecision).filter(PhaseDecision.game_id.in_(game_ids)).count()
        if decisions_count > 0:
            db.execute(delete(PhaseDecision).where(PhaseDecision.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {decisions_count} phase decisions")
        
        # Delete score events
        scores_count = db.query(ScoreEvent).filter(ScoreEvent.game_id.in_(game_ids)).count()
        if scores_count > 0:
            db.execute(delete(ScoreEvent).where(ScoreEvent.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {scores_count} score events")
        
        # Delete GM notes
        notes_count = db.query(PhaseGMNotes).filter(PhaseGMNotes.game_id.in_(game_ids)).count()
        if notes_count > 0:
            db.execute(delete(PhaseGMNotes).where(PhaseGMNotes.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {notes_count} GM notes")
        
        # Delete after action reports
        aar_count = db.query(AfterActionReport).filter(AfterActionReport.game_id.in_(game_ids)).count()
        if aar_count > 0:
            db.execute(delete(AfterActionReport).where(AfterActionReport.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {aar_count} after action reports")
        
        # Delete players
        players_count = db.query(Player).filter(Player.game_id.in_(game_ids)).count()
        if players_count > 0:
            db.execute(delete(Player).where(Player.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {players_count} players")
        
        # Delete teams
        teams_count = db.query(Team).filter(Team.game_id.in_(game_ids)).count()
        if teams_count > 0:
            db.execute(delete(Team).where(Team.game_id.in_(game_ids)))
            db.flush()
            print(f"    ✓ Deleted {teams_count} teams")
        
        # Delete games
        db.execute(delete(Game).where(Game.id.in_(game_ids)))
        db.flush()
        print(f"    ✓ Deleted {len(all_affected_games)} games")
    else:
        print("  ✓ No games using this scenario")
    
    if phase_ids:
        # Delete artifact associations
        print("\nDeleting artifact associations...")
        assoc_count = db.execute(
            delete(scenario_phase_artifacts).where(
                scenario_phase_artifacts.c.phase_id.in_(phase_ids)
            )
        ).rowcount
        db.flush()
        print(f"  ✓ Deleted {assoc_count} artifact associations")
        
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
    
    assoc_count = assoc_count if phase_ids else 0
    
    print(f"\n✅ Successfully deleted scenario '{scenario_name}'")
    if all_affected_games:
        print(f"   Deleted {len(all_affected_games)} game(s) using this scenario")
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

