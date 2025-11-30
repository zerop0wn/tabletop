"""
Test what artifacts are returned for a player in a game.
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal
from app.models import Game, Player, ScenarioPhase, Artifact, scenario_phase_artifacts
from sqlalchemy import select

db = SessionLocal()

try:
    # Get the latest game for the ransomware scenario
    scenario_id = 14  # From the check output
    game = db.query(Game).filter(Game.scenario_id == scenario_id).order_by(Game.id.desc()).first()
    
    if not game:
        print("❌ No game found for scenario")
        sys.exit(1)
    
    print(f"Game ID: {game.id}")
    print(f"Current Phase ID: {game.current_phase_id}")
    print()
    
    # Get a player
    players = db.query(Player).filter(Player.game_id == game.id).limit(1).all()
    if not players:
        print("❌ No players found in game")
        print("Create a game and join as a player first")
        sys.exit(1)
    
    player = players[0]
    print(f"Player ID: {player.id}")
    print(f"Team: {player.team.name} ({player.team.role})")
    print()
    
    if game.current_phase_id:
        phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == game.current_phase_id).first()
        print(f"Current Phase: {phase.name if phase else 'None'}")
        
        if phase:
            # Get artifacts the same way the API does
            team_role = player.team.role
            artifact_ids = db.execute(
                select(scenario_phase_artifacts.c.artifact_id).where(
                    scenario_phase_artifacts.c.phase_id == phase.id
                ).where(
                    (scenario_phase_artifacts.c.team_role == team_role) | 
                    (scenario_phase_artifacts.c.team_role.is_(None))
                )
            ).scalars().all()
            
            artifacts = db.query(Artifact).filter(Artifact.id.in_(artifact_ids)).all() if artifact_ids else []
            
            print(f"\nArtifacts returned for {team_role} team:")
            if artifacts:
                for artifact in artifacts:
                    has_content = bool(artifact.content)
                    print(f"  - {artifact.name} (ID: {artifact.id})")
                    print(f"    Content: {'✓' if has_content else '✗'}")
                    print(f"    Content length: {len(artifact.content) if artifact.content else 0} chars")
            else:
                print("  ❌ No artifacts found!")
                print(f"  Artifact IDs from join table: {artifact_ids}")
    else:
        print("Game has no current phase set")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

