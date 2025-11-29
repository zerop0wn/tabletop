from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy as sa
from app.database import get_db
from app.models import Game, Team, Player, ScenarioPhase, PhaseDecision, DecisionStatus, PlayerVote, Artifact, scenario_phase_artifacts
from app.schemas import JoinRequest, JoinResponse, PlayerStateResponse, VotingStatusResponse, PlayerVoteResponse
from typing import Optional

router = APIRouter()


@router.post("/join", response_model=JoinResponse)
def join_game(join_data: JoinRequest, db: Session = Depends(get_db)):
    # Find team by code
    team = db.query(Team).filter(Team.code == join_data.team_code.upper()).first()
    if not team:
        raise HTTPException(status_code=404, detail="Invalid team code")

    game = db.query(Game).filter(Game.id == team.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check if player already exists for this team with same name
    existing_player = db.query(Player).filter(
        Player.game_id == game.id,
        Player.team_id == team.id,
        Player.display_name == join_data.display_name
    ).first()

    if existing_player:
        player = existing_player
    else:
        # Create new player
        player = Player(
            game_id=game.id,
            team_id=team.id,
            display_name=join_data.display_name
        )
        db.add(player)
        db.commit()
        db.refresh(player)

    return JoinResponse(
        player_id=player.id,
        team_id=team.id,
        game_id=game.id,
        team_role=team.role,
        game_basic_info={
            "scenario_name": game.scenario.name if game.scenario else "Unknown",
            "game_status": game.status.value,
        }
    )


@router.get("/games/{game_id}/player/{player_id}/state", response_model=PlayerStateResponse)
def get_player_state(game_id: int, player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id, Player.game_id == game_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    current_phase = None
    phase_briefing_text = None
    team_objective = None
    artifacts = []

    if game.current_phase_id:
        current_phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == game.current_phase_id).first()
        if current_phase:
            phase_briefing_text = current_phase.briefing_text
            # Filter artifacts by team role
            team_role = player.team.role
            # Get artifacts for this phase that are either for this team or for both teams (team_role is None)
            artifact_ids = db.execute(
                sa.select(scenario_phase_artifacts.c.artifact_id).where(
                    scenario_phase_artifacts.c.phase_id == current_phase.id
                ).where(
                    (scenario_phase_artifacts.c.team_role == team_role) | 
                    (scenario_phase_artifacts.c.team_role.is_(None))
                )
            ).scalars().all()
            artifacts = db.query(Artifact).filter(Artifact.id.in_(artifact_ids)).all() if artifact_ids else []
            if player.team.role == "red":
                team_objective = current_phase.red_objective
            else:
                team_objective = current_phase.blue_objective

    # Get decision if exists
    decision = None
    has_voted = False
    team_voting_status = None
    
    if game.current_phase_id:
        decision = db.query(PhaseDecision).filter(
            PhaseDecision.game_id == game_id,
            PhaseDecision.team_id == player.team_id,
            PhaseDecision.phase_id == game.current_phase_id
        ).first()
        
        # Check if player has voted
        vote = db.query(PlayerVote).filter(
            PlayerVote.player_id == player_id,
            PlayerVote.phase_id == game.current_phase_id
        ).first()
        has_voted = vote is not None
        
        # Get team voting status
        if game.phase_state.value == "open_for_decisions":
            team_players = db.query(Player).filter(
                Player.game_id == game_id,
                Player.team_id == player.team_id
            ).all()
            
            votes = db.query(PlayerVote).filter(
                PlayerVote.game_id == game_id,
                PlayerVote.phase_id == game.current_phase_id,
                PlayerVote.team_id == player.team_id
            ).all()
            
            vote_responses = []
            for v in votes:
                p = db.query(Player).filter(Player.id == v.player_id).first()
                vote_responses.append(PlayerVoteResponse(
                    id=v.id,
                    player_id=v.player_id,
                    player_name=p.display_name if p else "Unknown",
                    selected_action=v.selected_action,
                    effectiveness_rating=v.effectiveness_rating,
                    comments=v.comments,
                    justification=v.justification,
                    voted_at=v.voted_at
                ))
            
            team_voting_status = VotingStatusResponse(
                team_id=player.team_id,
                team_name=player.team.name,
                team_role=player.team.role,
                total_players=len(team_players),
                votes_submitted=len(votes),
                votes=vote_responses,
                all_voted=len(votes) == len(team_players) and len(team_players) > 0
            )

    return PlayerStateResponse(
        current_phase=current_phase,
        phase_state=game.phase_state,
        phase_briefing_text=phase_briefing_text,
        team_objective=team_objective,
        artifacts=artifacts,
        decision=decision,
        game_status=game.status,
        team_role=player.team.role,
        team_name=player.team.name,
        has_voted=has_voted,
        team_voting_status=team_voting_status,
    )

