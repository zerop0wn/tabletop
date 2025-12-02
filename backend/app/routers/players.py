from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
import sqlalchemy as sa
from app.database import get_db
from app.models import Game, Team, Player, ScenarioPhase, PhaseDecision, DecisionStatus, PlayerVote, Artifact, scenario_phase_artifacts, ScoreEvent
from app.schemas import JoinRequest, JoinResponse, PlayerStateResponse, VotingStatusResponse, PlayerVoteResponse, PlayerReportCardResponse, PhaseReportCardEntry
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
            # Debug: Log artifacts found
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Phase {current_phase.id}: Found {len(artifacts)} artifacts for {player.team.role} team")
            for artifact in artifacts:
                logger.info(f"  - {artifact.name} (ID: {artifact.id}): content={bool(artifact.content)}, content_len={len(artifact.content) if artifact.content else 0}")
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

    # Get phase-specific actions if available
    available_actions = None
    if current_phase:
        try:
            if current_phase.available_actions:
                team_role_key = player.team.role
                
                if isinstance(current_phase.available_actions, dict) and team_role_key in current_phase.available_actions:
                    available_actions = current_phase.available_actions[team_role_key]
                    # Ensure it's a list of dicts with name and description
                    if available_actions and isinstance(available_actions, list):
                        available_actions = [
                            {
                                "name": action.get("name", "") if isinstance(action, dict) else str(action),
                                "description": action.get("description", "") if isinstance(action, dict) else ""
                            }
                            for action in available_actions
                        ]
        except Exception as e:
            # Log error but don't fail the request
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error extracting available_actions: {e}", exc_info=True)
            available_actions = None
    
    # Debug: Verify artifacts have content before returning
    import logging
    logger = logging.getLogger(__name__)
    for artifact in artifacts:
        logger.info(f"Returning artifact {artifact.id} ({artifact.name}): content={bool(artifact.content)}, content_len={len(artifact.content) if artifact.content else 0}")
        # Force load content if it's not loaded (lazy loading issue)
        if hasattr(artifact, 'content'):
            _ = artifact.content  # Access to ensure it's loaded
    
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
        available_actions=available_actions,
    )


@router.get("/games/{game_id}/player/{player_id}/report-card", response_model=PlayerReportCardResponse)
def get_player_report_card(game_id: int, player_id: int, db: Session = Depends(get_db)):
    """Get a summary report card for a player showing their actions and effectiveness across all phases"""
    player = db.query(Player).filter(Player.id == player_id, Player.game_id == game_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get all phases for this scenario, ordered by order_index
    phases = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == game.scenario_id
    ).order_by(ScenarioPhase.order_index).all()

    phase_entries = []
    total_score = 0
    effectiveness_ratings = []

    for phase in phases:
        # Get player's vote for this phase
        player_vote = db.query(PlayerVote).filter(
            PlayerVote.player_id == player_id,
            PlayerVote.phase_id == phase.id,
            PlayerVote.game_id == game_id
        ).first()

        # Get team's decision for this phase
        team_decision = db.query(PhaseDecision).filter(
            PhaseDecision.game_id == game_id,
            PhaseDecision.team_id == player.team_id,
            PhaseDecision.phase_id == phase.id
        ).first()

        # Get score for this phase
        phase_score = db.query(func.coalesce(func.sum(ScoreEvent.delta), 0)).filter(
            ScoreEvent.game_id == game_id,
            ScoreEvent.team_id == player.team_id,
            ScoreEvent.phase_id == phase.id
        ).scalar() or 0

        total_score += int(phase_score)

        # Extract team decision action
        team_decision_action = None
        if team_decision and team_decision.actions:
            if isinstance(team_decision.actions, dict):
                if "selected" in team_decision.actions:
                    selected = team_decision.actions["selected"]
                    if isinstance(selected, list) and len(selected) > 0:
                        team_decision_action = selected[0]
                    elif isinstance(selected, str):
                        team_decision_action = selected

        # Collect effectiveness rating
        if player_vote and player_vote.effectiveness_rating is not None:
            effectiveness_ratings.append(player_vote.effectiveness_rating)

        phase_entries.append(PhaseReportCardEntry(
            phase_id=phase.id,
            phase_name=phase.name,
            phase_order=phase.order_index,
            player_vote=player_vote.selected_action if player_vote else None,
            player_effectiveness_rating=player_vote.effectiveness_rating if player_vote else None,
            player_comments=player_vote.comments if player_vote else None,
            team_decision=team_decision_action,
            score_received=int(phase_score),
            max_possible_score=10  # Most scenarios use 0-10 scale
        ))

    # Calculate average effectiveness rating
    average_effectiveness_rating = None
    if effectiveness_ratings:
        average_effectiveness_rating = sum(effectiveness_ratings) / len(effectiveness_ratings)

    return PlayerReportCardResponse(
        player_id=player.id,
        player_name=player.display_name,
        team_id=player.team_id,
        team_name=player.team.name,
        team_role=player.team.role,
        game_id=game.id,
        scenario_name=game.scenario.name if game.scenario else "Unknown",
        total_score=total_score,
        average_effectiveness_rating=average_effectiveness_rating,
        phases=phase_entries,
        game_completed_at=game.updated_at if game.status.value == "finished" else None
    )

