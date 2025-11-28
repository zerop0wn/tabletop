from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import Game, Team, ScoreEvent, Player, PlayerVote, PhaseDecision, ScenarioPhase
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

    # Calculate scores for each team and get additional data
    team_scores = []
    for team in teams:
        total_score = db.query(func.coalesce(func.sum(ScoreEvent.delta), 0)).filter(
            ScoreEvent.game_id == game.id,
            ScoreEvent.team_id == team.id
        ).scalar()

        # Get recent score events for this team (last 5)
        recent_events = db.query(ScoreEvent).filter(
            ScoreEvent.game_id == game.id,
            ScoreEvent.team_id == team.id
        ).order_by(desc(ScoreEvent.created_at)).limit(5).all()

        # Get score history (score per phase)
        score_history = []
        # Get all phases for this scenario, regardless of current phase
        if game.scenario_id:
            phases = db.query(ScenarioPhase).filter(
                ScenarioPhase.scenario_id == game.scenario_id
            ).order_by(ScenarioPhase.order_index).all()
            
            for phase in phases:
                phase_score = db.query(func.coalesce(func.sum(ScoreEvent.delta), 0)).filter(
                    ScoreEvent.game_id == game.id,
                    ScoreEvent.team_id == team.id,
                    ScoreEvent.phase_id == phase.id
                ).scalar()
                score_history.append({
                    "phase_name": phase.name,
                    "phase_order": phase.order_index,
                    "score": int(phase_score) if phase_score else 0
                })

        # Get recent decision
        recent_decision = None
        if game.current_phase_id:
            decision = db.query(PhaseDecision).filter(
                PhaseDecision.game_id == game.id,
                PhaseDecision.team_id == team.id,
                PhaseDecision.phase_id == game.current_phase_id
            ).order_by(desc(PhaseDecision.submitted_at)).first()
            
            if decision:
                selected_action = None
                if isinstance(decision.actions, dict) and "selected" in decision.actions:
                    selected_action = decision.actions["selected"][0] if decision.actions["selected"] else None
                
                recent_decision = {
                    "action": selected_action,
                    "score_awarded": decision.score_awarded,
                    "submitted_at": decision.submitted_at.isoformat() if decision.submitted_at else None
                }

        # Get all players for this team
        players = db.query(Player).filter(
            Player.game_id == game.id,
            Player.team_id == team.id
        ).all()
        team_member_names = [player.display_name for player in players]

        # Get voting status for current phase
        voting_status = None
        if game.current_phase_id and game.phase_state.value == "open_for_decisions":
            votes = db.query(PlayerVote).filter(
                PlayerVote.game_id == game.id,
                PlayerVote.phase_id == game.current_phase_id,
                PlayerVote.team_id == team.id
            ).all()
            
            voting_status = {
                "total_players": len(players),
                "votes_submitted": len(votes),
                "all_voted": len(votes) == len(players) and len(players) > 0
            }

        team_scores.append(TeamScore(
            team_id=team.id,
            team_name=team.name,
            team_role=team.role,
            total_score=int(total_score) if total_score else 0,
            team_members=team_member_names,
            recent_events=[{
                "delta": event.delta,
                "reason": event.reason,
                "created_at": event.created_at.isoformat() if event.created_at else None
            } for event in recent_events],
            score_history=score_history,
            recent_decision=recent_decision,
            voting_status=voting_status
        ))

    # Get recent score events across all teams (for feed)
    recent_global_events = db.query(ScoreEvent).filter(
        ScoreEvent.game_id == game.id
    ).order_by(desc(ScoreEvent.created_at)).limit(10).all()

    current_phase_name = None
    if game.current_phase:
        current_phase_name = game.current_phase.name

    return ScoreboardResponse(
        game_id=game.id,
        scenario_name=game.scenario.name if game.scenario else "Unknown",
        current_phase_name=current_phase_name,
        phase_state=game.phase_state,
        teams=team_scores,
        recent_events=[{
            "team_id": event.team_id,
            "team_name": next((t.name for t in teams if t.id == event.team_id), "Unknown"),
            "team_role": next((t.role for t in teams if t.id == event.team_id), "unknown"),
            "delta": event.delta,
            "reason": event.reason,
            "created_at": event.created_at.isoformat() if event.created_at else None
        } for event in recent_global_events]
    )

