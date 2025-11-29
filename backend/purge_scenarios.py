"""
Purge all scenarios except Tutorial, and delete all games.
This script will clean the database to start fresh.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.database import SessionLocal
from app.models import (
    Scenario, ScenarioPhase, Artifact, Game, Team, Player, 
    PlayerVote, PhaseDecision, ScoreEvent, PhaseGMNotes,
    PlayerComment, AfterActionReport
)
from app.models import scenario_phase_artifacts

db: Session = SessionLocal()

try:
    print("=" * 60)
    print("PURGING SCENARIOS AND GAMES")
    print("=" * 60)
    print()
    
    # Step 1: Delete all games (this should cascade delete related data)
    print("Step 1: Deleting all games...")
    games_count = db.query(Game).count()
    print(f"  Found {games_count} games")
    
    if games_count > 0:
        # Delete all games - cascade should handle teams, players, votes, etc.
        db.execute(delete(Game))
        db.flush()
        print(f"  ✓ Deleted {games_count} games")
    else:
        print("  ✓ No games to delete")
    
    # Step 2: Manually clean up related tables (in case cascade doesn't work)
    print("\nStep 2: Cleaning up related tables...")
    
    # Delete player votes
    votes_count = db.query(PlayerVote).count()
    if votes_count > 0:
        db.execute(delete(PlayerVote))
        db.flush()
        print(f"  ✓ Deleted {votes_count} player votes")
    
    # Delete phase decisions
    decisions_count = db.query(PhaseDecision).count()
    if decisions_count > 0:
        db.execute(delete(PhaseDecision))
        db.flush()
        print(f"  ✓ Deleted {decisions_count} phase decisions")
    
    # Delete score events
    scores_count = db.query(ScoreEvent).count()
    if scores_count > 0:
        db.execute(delete(ScoreEvent))
        db.flush()
        print(f"  ✓ Deleted {scores_count} score events")
    
    # Delete player comments
    comments_count = db.query(PlayerComment).count()
    if comments_count > 0:
        db.execute(delete(PlayerComment))
        db.flush()
        print(f"  ✓ Deleted {comments_count} player comments")
    
    # Delete GM notes
    notes_count = db.query(PhaseGMNotes).count()
    if notes_count > 0:
        db.execute(delete(PhaseGMNotes))
        db.flush()
        print(f"  ✓ Deleted {notes_count} GM notes")
    
    # Delete after action reports
    aar_count = db.query(AfterActionReport).count()
    if aar_count > 0:
        db.execute(delete(AfterActionReport))
        db.flush()
        print(f"  ✓ Deleted {aar_count} after action reports")
    
    # Delete players
    players_count = db.query(Player).count()
    if players_count > 0:
        db.execute(delete(Player))
        db.flush()
        print(f"  ✓ Deleted {players_count} players")
    
    # Delete teams
    teams_count = db.query(Team).count()
    if teams_count > 0:
        db.execute(delete(Team))
        db.flush()
        print(f"  ✓ Deleted {teams_count} teams")
    
    # Step 3: Find and keep tutorial scenario
    print("\nStep 3: Finding tutorial scenario...")
    tutorial_scenario = db.query(Scenario).filter(
        Scenario.name.like("%Tutorial%")
    ).first()
    
    tutorial_phase_ids = []
    tutorial_artifact_ids = []
    
    if tutorial_scenario:
        print(f"  ✓ Found tutorial scenario: {tutorial_scenario.name} (ID: {tutorial_scenario.id})")
        
        # Get tutorial phase IDs
        tutorial_phases = db.query(ScenarioPhase).filter(
            ScenarioPhase.scenario_id == tutorial_scenario.id
        ).all()
        tutorial_phase_ids = [p.id for p in tutorial_phases]
        print(f"  ✓ Found {len(tutorial_phase_ids)} tutorial phases")
        
        # Get tutorial artifact IDs (artifacts linked to tutorial phases)
        if tutorial_phase_ids:
            tutorial_artifact_links = db.execute(
                db.query(scenario_phase_artifacts.c.artifact_id).where(
                    scenario_phase_artifacts.c.phase_id.in_(tutorial_phase_ids)
                )
            ).scalars().all()
            tutorial_artifact_ids = list(set(tutorial_artifact_links))
            print(f"  ✓ Found {len(tutorial_artifact_ids)} tutorial artifacts")
    else:
        print("  ⚠️  No tutorial scenario found")
    
    # Step 4: Delete all scenarios except tutorial
    print("\nStep 4: Deleting non-tutorial scenarios...")
    all_scenarios = db.query(Scenario).all()
    scenarios_to_delete = [s for s in all_scenarios if s.id != (tutorial_scenario.id if tutorial_scenario else None)]
    
    print(f"  Found {len(all_scenarios)} total scenarios")
    print(f"  Will delete {len(scenarios_to_delete)} scenarios")
    
    for scenario in scenarios_to_delete:
        print(f"    - Deleting: {scenario.name} (ID: {scenario.id})")
        
        # Get phases for this scenario
        phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).all()
        phase_ids = [p.id for p in phases]
        
        # Delete artifact links for these phases
        if phase_ids:
            db.execute(
                delete(scenario_phase_artifacts).where(
                    scenario_phase_artifacts.c.phase_id.in_(phase_ids)
                )
            )
            db.flush()
        
        # Delete phases
        if phase_ids:
            db.execute(
                delete(ScenarioPhase).where(ScenarioPhase.id.in_(phase_ids))
            )
            db.flush()
        
        # Delete scenario
        db.delete(scenario)
        db.flush()
    
    print(f"  ✓ Deleted {len(scenarios_to_delete)} scenarios")
    
    # Step 5: Delete artifacts not linked to tutorial
    print("\nStep 5: Cleaning up orphaned artifacts...")
    all_artifacts = db.query(Artifact).all()
    
    if tutorial_artifact_ids:
        artifacts_to_delete = [a for a in all_artifacts if a.id not in tutorial_artifact_ids]
    else:
        artifacts_to_delete = all_artifacts
    
    print(f"  Found {len(all_artifacts)} total artifacts")
    print(f"  Will delete {len(artifacts_to_delete)} artifacts")
    
    for artifact in artifacts_to_delete:
        db.delete(artifact)
        db.flush()
    
    print(f"  ✓ Deleted {len(artifacts_to_delete)} artifacts")
    
    # Commit everything
    db.commit()
    
    print("\n" + "=" * 60)
    print("✓ PURGE COMPLETE")
    print("=" * 60)
    print()
    print("Remaining scenarios:")
    remaining_scenarios = db.query(Scenario).all()
    for scenario in remaining_scenarios:
        phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).count()
        print(f"  - {scenario.name} ({phases} phases)")
    print()
    print("You can now create new scenarios from scratch.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)
finally:
    db.close()

