from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from collections import Counter
from app.database import get_db
from app.auth import get_current_gm
from app.models import Game, Player, PhaseDecision, Team, ScoreEvent, PhaseState, DecisionStatus, PlayerVote
from app.schemas import VoteSubmit, DecisionSubmit, DecisionResponse, DecisionScore, VotingStatusResponse, PlayerVoteResponse

router = APIRouter()


@router.post("/{game_id}/phases/{phase_id}/votes", response_model=PlayerVoteResponse)
def submit_vote(
    game_id: int,
    phase_id: int,
    vote_data: VoteSubmit,
    db: Session = Depends(get_db)
):
    # Verify player exists and belongs to game
    player = db.query(Player).filter(
        Player.id == vote_data.player_id,
        Player.game_id == game_id
    ).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Verify game and phase
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.current_phase_id != phase_id:
        raise HTTPException(status_code=400, detail="Phase mismatch")

    if game.phase_state != PhaseState.OPEN_FOR_DECISIONS:
        raise HTTPException(status_code=400, detail=f"Cannot submit vote in state: {game.phase_state}")

    # Check if vote already exists
    existing_vote = db.query(PlayerVote).filter(
        PlayerVote.player_id == vote_data.player_id,
        PlayerVote.phase_id == phase_id
    ).first()

    if existing_vote:
        # Update existing vote
        existing_vote.selected_action = vote_data.selected_action
        existing_vote.effectiveness_rating = vote_data.effectiveness_rating
        existing_vote.comments = vote_data.comments[:500] if vote_data.comments else None  # Enforce 500 char limit
        existing_vote.justification = vote_data.justification  # Keep for backward compatibility
        db.commit()
        db.refresh(existing_vote)
    else:
        # Create new vote
        vote = PlayerVote(
            game_id=game_id,
            team_id=player.team_id,
            phase_id=phase_id,
            player_id=vote_data.player_id,
            selected_action=vote_data.selected_action,
            effectiveness_rating=vote_data.effectiveness_rating,
            comments=vote_data.comments[:500] if vote_data.comments else None,  # Enforce 500 char limit
            justification=vote_data.justification  # Keep for backward compatibility
        )
        db.add(vote)
        db.commit()
        db.refresh(vote)
        existing_vote = vote

    # Check if all players have voted, if so, aggregate votes into decision
    _check_and_aggregate_votes(game_id, phase_id, player.team_id, db)

    return PlayerVoteResponse(
        id=existing_vote.id,
        player_id=existing_vote.player_id,
        player_name=player.display_name,
        selected_action=existing_vote.selected_action,
        effectiveness_rating=existing_vote.effectiveness_rating,
        comments=existing_vote.comments,
        justification=existing_vote.justification,
        voted_at=existing_vote.voted_at
    )


def _check_and_aggregate_votes(game_id: int, phase_id: int, team_id: int, db: Session):
    """Check if all players have voted and aggregate votes into a PhaseDecision"""
    # Get all players in the team
    team_players = db.query(Player).filter(
        Player.game_id == game_id,
        Player.team_id == team_id
    ).all()
    
    if not team_players:
        return
    
    # Get all votes for this phase from this team
    votes = db.query(PlayerVote).filter(
        PlayerVote.game_id == game_id,
        PlayerVote.phase_id == phase_id,
        PlayerVote.team_id == team_id
    ).all()
    
    # Check if all players have voted
    voted_player_ids = {vote.player_id for vote in votes}
    all_player_ids = {player.id for player in team_players}
    
    if voted_player_ids == all_player_ids and len(voted_player_ids) > 0:
        # Aggregate votes - count votes per action
        action_counts = Counter(vote.selected_action for vote in votes)
        winning_action = action_counts.most_common(1)[0][0] if action_counts else None
        
        # Get all justifications
        justifications = [v.justification for v in votes if v.justification]
        combined_justification = "\n\n".join(justifications) if justifications else "Team vote"
        
        # Check if decision already exists
        existing_decision = db.query(PhaseDecision).filter(
            PhaseDecision.game_id == game_id,
            PhaseDecision.team_id == team_id,
            PhaseDecision.phase_id == phase_id
        ).first()
        
        if not existing_decision:
            # Create decision from aggregated votes
            decision = PhaseDecision(
                game_id=game_id,
                team_id=team_id,
                phase_id=phase_id,
                actions={"selected": [winning_action], "vote_counts": dict(action_counts)},
                free_text_justification=combined_justification,
                status=DecisionStatus.SUBMITTED
            )
            db.add(decision)
            db.commit()


@router.get("/{game_id}/phases/{phase_id}/voting-status", response_model=List[VotingStatusResponse])
def get_voting_status(
    game_id: int,
    phase_id: int,
    db: Session = Depends(get_db)
):
    """Get voting status for all teams in the current phase"""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.current_phase_id != phase_id:
        raise HTTPException(status_code=400, detail="Phase mismatch")
    
    teams = db.query(Team).filter(Team.game_id == game_id).all()
    status_list = []
    
    for team in teams:
        # Get all players in team
        players = db.query(Player).filter(
            Player.game_id == game_id,
            Player.team_id == team.id
        ).all()
        
        # Get all votes for this team and phase
        votes = db.query(PlayerVote).filter(
            PlayerVote.game_id == game_id,
            PlayerVote.phase_id == phase_id,
            PlayerVote.team_id == team.id
        ).all()
        
        vote_responses = []
        for vote in votes:
            player = db.query(Player).filter(Player.id == vote.player_id).first()
            vote_responses.append(PlayerVoteResponse(
                id=vote.id,
                player_id=vote.player_id,
                player_name=player.display_name if player else "Unknown",
                selected_action=vote.selected_action,
                effectiveness_rating=vote.effectiveness_rating,
                comments=vote.comments,
                justification=vote.justification,
                voted_at=vote.voted_at
            ))
        
        status_list.append(VotingStatusResponse(
            team_id=team.id,
            team_name=team.name,
            total_players=len(players),
            votes_submitted=len(votes),
            votes=vote_responses,
            all_voted=len(votes) == len(players) and len(players) > 0
        ))
    
    return status_list


@router.post("/{game_id}/phases/{phase_id}/decisions", response_model=DecisionResponse)
def submit_decision(
    game_id: int,
    phase_id: int,
    decision_data: DecisionSubmit,
    db: Session = Depends(get_db)
):
    # Legacy endpoint - kept for backwards compatibility but should use votes instead
    raise HTTPException(status_code=400, detail="Please use /votes endpoint for team voting")


@router.get("/{game_id}/phases/{phase_id}/decisions", response_model=List[DecisionResponse])
def get_decisions(
    game_id: int,
    phase_id: int,
    db: Session = Depends(get_db),
    current_gm=Depends(get_current_gm)
):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    decisions = db.query(PhaseDecision).filter(
        PhaseDecision.game_id == game_id,
        PhaseDecision.phase_id == phase_id
    ).all()
    return decisions


@router.post("/{game_id}/phases/{phase_id}/decisions/{decision_id}/score")
def score_decision(
    game_id: int,
    phase_id: int,
    decision_id: int,
    score_data: DecisionScore,
    db: Session = Depends(get_db),
    current_gm=Depends(get_current_gm)
):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    decision = db.query(PhaseDecision).filter(
        PhaseDecision.id == decision_id,
        PhaseDecision.game_id == game_id,
        PhaseDecision.phase_id == phase_id
    ).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    decision.score_awarded = score_data.score_awarded
    decision.gm_notes = score_data.gm_notes
    decision.status = DecisionStatus.SCORED

    # Create score event
    score_event = ScoreEvent(
        game_id=game_id,
        team_id=decision.team_id,
        phase_id=phase_id,
        delta=score_data.score_awarded,
        reason=f"Phase {phase_id} decision scored"
    )
    db.add(score_event)
    db.commit()

    return {"message": "Decision scored", "decision_id": decision_id}

