"""
Test what the API actually returns for player state.
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal
from app.models import Game, Player, ScenarioPhase, Artifact, scenario_phase_artifacts
from app.schemas import PlayerStateResponse, ArtifactResponse
from sqlalchemy import select
import json

db = SessionLocal()

try:
    # Get the latest game
    game = db.query(Game).order_by(Game.id.desc()).first()
    
    if not game:
        print("❌ No game found")
        sys.exit(1)
    
    print(f"Game ID: {game.id}")
    
    # Get a player
    player = db.query(Player).filter(Player.game_id == game.id).first()
    if not player:
        print("❌ No player found")
        sys.exit(1)
    
    print(f"Player ID: {player.id}, Team: {player.team.role}")
    print()
    
    # Replicate the API logic
    current_phase = None
    artifacts = []
    
    if game.current_phase_id:
        current_phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == game.current_phase_id).first()
        if current_phase:
            team_role = player.team.role
            artifact_ids = db.execute(
                select(scenario_phase_artifacts.c.artifact_id).where(
                    scenario_phase_artifacts.c.phase_id == current_phase.id
                ).where(
                    (scenario_phase_artifacts.c.team_role == team_role) | 
                    (scenario_phase_artifacts.c.team_role.is_(None))
                )
            ).scalars().all()
            artifacts = db.query(Artifact).filter(Artifact.id.in_(artifact_ids)).all() if artifact_ids else []
    
    print(f"Found {len(artifacts)} artifacts")
    print()
    
    # Serialize artifacts the same way the API does
    artifact_responses = [ArtifactResponse.from_orm(a) for a in artifacts]
    
    print("Artifact responses (as API would return):")
    for artifact_resp in artifact_responses:
        print(f"  - {artifact_resp.name} (ID: {artifact_resp.id})")
        print(f"    content: {'✓' if artifact_resp.content else '✗'}")
        print(f"    content length: {len(artifact_resp.content) if artifact_resp.content else 0}")
        print(f"    content preview: {artifact_resp.content[:100] if artifact_resp.content else 'None'}...")
        print()
    
    # Convert to dict to see what JSON would look like
    artifact_dicts = [a.dict() for a in artifact_responses]
    print("JSON representation (first artifact):")
    if artifact_dicts:
        print(json.dumps(artifact_dicts[0], indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

