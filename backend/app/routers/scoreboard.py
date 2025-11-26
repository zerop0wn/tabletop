from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Game, Team, ScoreEvent
from app.schemas import ScoreboardResponse, TeamScore

router = APIRouter()


@router.get("/{game_identifier}/scoreboard", response_model=ScoreboardResponse)
def get_scoreboard(game_identifier: str, db: Session = Depends(get_db)):
    # Try to find by audience_code first, then by ID
    game = None
    if game_identifier.isdigit():
        game = db.query(Game).filter(Game.id == int(game_identifier)).first()
    else:
        game = db.query(Game).filter(Game.audience_code == game_identifier).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get all teams for this game
    teams = db.query(Team).filter(Team.game_id == game.id).all()

    # Calculate scores for each team
    team_scores = []
    for team in teams:
        total_score = db.query(func.coalesce(func.sum(ScoreEvent.delta), 0)).filter(
            ScoreEvent.game_id == game.id,
            ScoreEvent.team_id == team.id
        ).scalar()

        team_scores.append(TeamScore(
            team_id=team.id,
            team_name=team.name,
            team_role=team.role,
            total_score=int(total_score) if total_score else 0
        ))

    current_phase_name = None
    if game.current_phase:
        current_phase_name = game.current_phase.name

    return ScoreboardResponse(
        game_id=game.id,
        scenario_name=game.scenario.name if game.scenario else "Unknown",
        current_phase_name=current_phase_name,
        phase_state=game.phase_state,
        teams=team_scores
    )

