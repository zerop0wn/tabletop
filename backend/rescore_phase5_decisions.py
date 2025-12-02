"""
Script to re-score Phase 5 decisions for existing games.
This updates ScoreEvents with the new Phase 5 scoring matrix.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Game, PhaseDecision, ScoreEvent, ScenarioPhase, Team, Scenario
from app.scoring import calculate_team_decision_score, calculate_weighted_score
from app.enums import DecisionStatus
from sqlalchemy import func

db: Session = SessionLocal()

try:
    # Find the intermediate ransomware scenario
    scenario = db.query(Scenario).filter(
        Scenario.name == "Ransomware Attack: Corporate Network Compromise"
    ).first()
    
    if not scenario:
        print("❌ Scenario 'Ransomware Attack: Corporate Network Compromise' not found!")
        sys.exit(1)
    
    print(f"✓ Found scenario: {scenario.name} (ID: {scenario.id})")
    
    # Find Phase 5
    phase5 = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == scenario.id,
        ScenarioPhase.order_index == 4  # Phase 5 is order_index 4
    ).first()
    
    if not phase5:
        print("❌ Phase 5 not found!")
        sys.exit(1)
    
    print(f"✓ Found Phase 5: {phase5.name} (ID: {phase5.id})")
    print()
    
    # Find all games using this scenario
    games = db.query(Game).filter(Game.scenario_id == scenario.id).all()
    
    if not games:
        print("⚠️  No games found using this scenario")
        sys.exit(0)
    
    print(f"Found {len(games)} game(s) using this scenario")
    print()
    
    updated_count = 0
    
    for game in games:
        print(f"Processing Game ID: {game.id}")
        
        # Find Phase 5 decisions for this game
        decisions = db.query(PhaseDecision).filter(
            PhaseDecision.game_id == game.id,
            PhaseDecision.phase_id == phase5.id,
            PhaseDecision.status == DecisionStatus.SCORED
        ).all()
        
        if not decisions:
            print(f"  ⏭️  No Phase 5 decisions found for this game")
            print()
            continue
        
        print(f"  Found {len(decisions)} Phase 5 decision(s)")
        
        # Get teams for team size calculation
        teams = db.query(Team).filter(Team.game_id == game.id).all()
        team_sizes = {}
        for team in teams:
            from app.models import Player
            player_count = db.query(Player).filter(Player.team_id == team.id).count()
            team_sizes[team.id] = player_count
        
        average_team_size = sum(team_sizes.values()) / len(team_sizes) if team_sizes else 1
        
        for decision in decisions:
            team = db.query(Team).filter(Team.id == decision.team_id).first()
            if not team:
                continue
            
            # Extract selected action
            selected_actions = []
            if isinstance(decision.actions, dict):
                if "selected" in decision.actions:
                    selected_actions = decision.actions["selected"]
            elif isinstance(decision.actions, list):
                selected_actions = decision.actions
            
            if not selected_actions:
                print(f"    ⚠️  Decision {decision.id}: No action found, skipping")
                continue
            
            primary_action = selected_actions[0] if selected_actions else None
            print(f"    Decision {decision.id} (Team: {team.name}, Action: {primary_action})")
            
            # Recalculate score
            try:
                base_score, explanation = calculate_team_decision_score(
                    scenario_name=scenario.name,
                    phase_order_index=phase5.order_index,
                    team_role=team.role,
                    selected_actions=selected_actions
                )
                
                final_score = calculate_weighted_score(
                    base_score=base_score,
                    team_size=team_sizes.get(team.id, 1),
                    average_team_size=average_team_size,
                    normalize=False
                )
                
                print(f"      Old score: {decision.score_awarded}, New score: {final_score}")
                
                # Update decision
                decision.score_awarded = final_score
                decision.gm_notes = f"Auto-scored (updated): {explanation}"
                
                # Delete old ScoreEvent for this decision
                old_events = db.query(ScoreEvent).filter(
                    ScoreEvent.game_id == game.id,
                    ScoreEvent.team_id == team.id,
                    ScoreEvent.phase_id == phase5.id
                ).all()
                
                for old_event in old_events:
                    db.delete(old_event)
                    print(f"      Deleted old ScoreEvent {old_event.id}")
                
                # Create new ScoreEvent
                new_event = ScoreEvent(
                    game_id=game.id,
                    team_id=team.id,
                    phase_id=phase5.id,
                    delta=int(final_score),
                    reason=f"Phase 5 auto-scored (updated): {explanation}"
                )
                db.add(new_event)
                print(f"      Created new ScoreEvent with score: {final_score}")
                
                updated_count += 1
                
            except Exception as e:
                print(f"      ❌ Error re-scoring: {e}")
                import traceback
                traceback.print_exc()
        
        print()
    
    db.commit()
    
    print("=" * 60)
    print("✅ Re-scoring Complete!")
    print("=" * 60)
    print(f"Updated: {updated_count} decision(s)")
    print()
    print("Phase 5 scores have been updated with the new scoring matrix.")
    print("The audience view should now show the correct scores.")

except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

