from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from collections import Counter
import secrets
from app.database import get_db
from app.auth import get_current_gm
from app.models import Game, Scenario, ScenarioPhase, Team, GameStatus, PhaseState, Player, PlayerVote, PhaseDecision, DecisionStatus, ScoreEvent
from app.schemas import GameCreate, GameResponse
from app.scoring import calculate_team_decision_score, calculate_weighted_score

router = APIRouter()


def generate_team_code() -> str:
    return secrets.token_urlsafe(8).upper()[:8]


@router.post("", response_model=GameResponse)
def create_game(game_data: GameCreate, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    # Verify scenario exists
    scenario = db.query(Scenario).filter(Scenario.id == game_data.scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Generate unique codes
    red_code = generate_team_code()
    blue_code = generate_team_code()
    audience_code = secrets.token_urlsafe(16)

    # Create game
    game = Game(
        scenario_id=game_data.scenario_id,
        status=GameStatus.LOBBY,
        gm_id=current_gm.id,
        red_team_code=red_code,
        blue_team_code=blue_code,
        audience_code=audience_code,
        settings=game_data.settings or {},
        phase_state=PhaseState.NOT_STARTED,
    )
    db.add(game)
    db.flush()

    # Create default teams
    red_team = Team(game_id=game.id, name="Red", code=red_code, role="red")
    blue_team = Team(game_id=game.id, name="Blue 1", code=blue_code, role="blue")
    db.add(red_team)
    db.add(blue_team)
    db.commit()
    db.refresh(game)

    return game


@router.get("", response_model=List[GameResponse])
def list_games(db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    games = db.query(Game).filter(Game.gm_id == current_gm.id).order_by(Game.created_at.desc()).all()
    return games


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.gm_id != current_gm.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return game


@router.post("/{game_id}/start")
def start_game(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.gm_id != current_gm.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get first phase
    first_phase = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == game.scenario_id,
        ScenarioPhase.order_index == 0
    ).first()

    if not first_phase:
        raise HTTPException(status_code=400, detail="Scenario has no phases")

    game.status = GameStatus.IN_PROGRESS
    game.current_phase_id = first_phase.id
    game.phase_state = PhaseState.BRIEFING
    db.commit()

    return {"message": "Game started", "current_phase_id": first_phase.id}


@router.post("/{game_id}/phase/open_for_decisions")
def open_for_decisions(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.phase_state != PhaseState.BRIEFING:
        raise HTTPException(status_code=400, detail=f"Cannot open decisions in state: {game.phase_state}")

    game.phase_state = PhaseState.OPEN_FOR_DECISIONS
    db.commit()
    return {"message": "Phase opened for decisions"}


@router.post("/{game_id}/phase/lock_decisions")
def lock_decisions(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game.current_phase_id:
        raise HTTPException(status_code=400, detail="No current phase")

    # Get current phase
    current_phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == game.current_phase_id).first()
    if not current_phase:
        raise HTTPException(status_code=404, detail="Current phase not found")

    # Aggregate votes for all teams before locking
    teams = db.query(Team).filter(Team.game_id == game_id).all()
    for team in teams:
        # Get all players in team
        players = db.query(Player).filter(
            Player.game_id == game_id,
            Player.team_id == team.id
        ).all()
        
        if not players:
            continue
        
        # Get all votes for this team and phase
        votes = db.query(PlayerVote).filter(
            PlayerVote.game_id == game_id,
            PlayerVote.phase_id == game.current_phase_id,
            PlayerVote.team_id == team.id
        ).all()
        
        if votes:
            # Aggregate votes - count votes per action
            action_counts = Counter(vote.selected_action for vote in votes)
            winning_action = action_counts.most_common(1)[0][0] if action_counts else None
            
            # Get all justifications
            justifications = [v.justification for v in votes if v.justification]
            combined_justification = "\n\n".join(justifications) if justifications else "Team vote"
            
            # Check if decision already exists
            existing_decision = db.query(PhaseDecision).filter(
                PhaseDecision.game_id == game_id,
                PhaseDecision.team_id == team.id,
                PhaseDecision.phase_id == game.current_phase_id
            ).first()
            
            if not existing_decision:
                # Create decision from aggregated votes
                decision = PhaseDecision(
                    game_id=game_id,
                    team_id=team.id,
                    phase_id=game.current_phase_id,
                    actions={"selected": [winning_action], "vote_counts": dict(action_counts)},
                    free_text_justification=combined_justification,
                    status=DecisionStatus.SUBMITTED
                )
                db.add(decision)
    
    db.flush()  # Ensure decisions are in database before scoring
    
    # Get all decisions for this phase and auto-score them
    decisions = db.query(PhaseDecision).filter(
        PhaseDecision.game_id == game_id,
        PhaseDecision.phase_id == current_phase.id,
        PhaseDecision.status == DecisionStatus.SUBMITTED
    ).all()
    
    # Calculate average team size for weighting
    team_sizes = {}
    for team in teams:
        player_count = db.query(Player).filter(Player.team_id == team.id).count()
        team_sizes[team.id] = player_count
    
    average_team_size = sum(team_sizes.values()) / len(team_sizes) if team_sizes else 1
    
    # Auto-score each decision
    for decision in decisions:
        # Get team role
        team = db.query(Team).filter(Team.id == decision.team_id).first()
        if not team:
            continue
        
        # Extract selected action from decision.actions
        selected_actions = []
        if isinstance(decision.actions, dict):
            if "selected" in decision.actions:
                selected_actions = decision.actions["selected"]
            elif isinstance(decision.actions, list):
                selected_actions = decision.actions
        elif isinstance(decision.actions, list):
            selected_actions = decision.actions
        
        # Get scenario name for scoring
        scenario = db.query(Scenario).filter(Scenario.id == game.scenario_id).first()
        scenario_name = scenario.name if scenario else "Ransomware Incident Response"
        
        # Calculate base score
        base_score, explanation = calculate_team_decision_score(
            scenario_name=scenario_name,
            phase_order_index=current_phase.order_index,
            team_role=team.role,
            selected_actions=selected_actions
        )
        
        # Apply team size weighting (set normalize=True to enable, False to disable)
        final_score = calculate_weighted_score(
            base_score=base_score,
            team_size=team_sizes.get(team.id, 1),
            average_team_size=average_team_size,
            normalize=False  # Set to True to enable team size normalization
        )
        
        # Update decision
        decision.score_awarded = final_score
        decision.gm_notes = f"Auto-scored: {explanation}"
        decision.status = DecisionStatus.SCORED
        
        # Create score event
        score_event = ScoreEvent(
            game_id=game_id,
            team_id=decision.team_id,
            phase_id=current_phase.id,
            delta=final_score,
            reason=f"Phase {current_phase.order_index + 1} auto-scored: {explanation}"
        )
        db.add(score_event)

    game.phase_state = PhaseState.DECISION_LOCK
    db.commit()
    return {"message": "Decisions locked and auto-scored"}


@router.post("/{game_id}/phase/resolve")
def resolve_phase(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    game.phase_state = PhaseState.RESOLUTION
    db.commit()
    return {"message": "Phase in resolution"}


@router.post("/{game_id}/phase/complete_and_next")
def complete_and_next(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game.current_phase_id:
        raise HTTPException(status_code=400, detail="No current phase")

    # Get current phase
    current_phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == game.current_phase_id).first()
    if not current_phase:
        raise HTTPException(status_code=400, detail="Current phase not found")

    # Find next phase
    next_phase = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == game.scenario_id,
        ScenarioPhase.order_index > current_phase.order_index
    ).order_by(ScenarioPhase.order_index).first()

    if next_phase:
        game.current_phase_id = next_phase.id
        game.phase_state = PhaseState.BRIEFING
    else:
        # No more phases, end game
        game.status = GameStatus.FINISHED
        game.phase_state = PhaseState.COMPLETE

    db.commit()
    return {"message": "Phase completed", "next_phase_id": next_phase.id if next_phase else None}


@router.post("/{game_id}/end")
def end_game(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    game.status = GameStatus.FINISHED
    game.phase_state = PhaseState.COMPLETE
    db.commit()
    return {"message": "Game ended"}


@router.delete("/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db), current_gm=Depends(get_current_gm)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game or game.gm_id != current_gm.id:
        raise HTTPException(status_code=404, detail="Game not found")

    # Delete related records in the correct order to avoid foreign key violations
    # 1. Delete player votes (references players)
    db.query(PlayerVote).filter(PlayerVote.game_id == game_id).delete()
    
    # 2. Delete phase decisions (references game, team, phase)
    db.query(PhaseDecision).filter(PhaseDecision.game_id == game_id).delete()
    
    # 3. Delete score events (references game, team, phase)
    db.query(ScoreEvent).filter(ScoreEvent.game_id == game_id).delete()
    
    # 4. Delete the game (cascade will handle teams and players)
    db.delete(game)
    db.commit()
    return {"message": "Game deleted"}

