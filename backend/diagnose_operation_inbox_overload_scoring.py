"""
Diagnostic script to check Operation Inbox Overload scoring configuration.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Game, Scenario, ScenarioPhase, PhaseDecision, Team
from app.scoring import SCORING_MATRICES, get_optimal_score
from app.enums import DecisionStatus

db: Session = SessionLocal()

try:
    print("=" * 60)
    print("Operation Inbox Overload Scoring Diagnostic")
    print("=" * 60)
    print()
    
    # Check if scenario exists
    scenario = db.query(Scenario).filter(
        Scenario.name == "Operation Inbox Overload"
    ).first()
    
    if not scenario:
        print("❌ Scenario 'Operation Inbox Overload' not found in database!")
        print()
        print("Available scenarios:")
        all_scenarios = db.query(Scenario).all()
        for s in all_scenarios:
            print(f"  - {s.name}")
        sys.exit(1)
    
    print(f"✓ Found scenario: '{scenario.name}' (ID: {scenario.id})")
    print()
    
    # Check if scoring matrix exists
    if "Operation Inbox Overload" not in SCORING_MATRICES:
        print("❌ 'Operation Inbox Overload' not found in SCORING_MATRICES!")
        print()
        print("Available scenarios in SCORING_MATRICES:")
        for name in SCORING_MATRICES.keys():
            print(f"  - {name}")
        sys.exit(1)
    
    print(f"✓ Found scoring matrix for 'Operation Inbox Overload'")
    print()
    
    scoring_matrix = SCORING_MATRICES["Operation Inbox Overload"]
    
    # Check all phases
    phases = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == scenario.id
    ).order_by(ScenarioPhase.order_index).all()
    
    print(f"Found {len(phases)} phases:")
    print()
    
    for phase in phases:
        print(f"Phase {phase.order_index}: {phase.name}")
        
        # Check Red Team actions
        red_actions = phase.available_actions.get("red", []) if phase.available_actions else []
        red_scoring = scoring_matrix.get((phase.order_index, "red"), {})
        
        print(f"  Red Team:")
        print(f"    Actions in scenario: {len(red_actions)}")
        print(f"    Actions in scoring matrix: {len(red_scoring)}")
        
        for action in red_actions:
            action_name = action.get("name", "")
            score = red_scoring.get(action_name, None)
            if score is None:
                print(f"      ❌ '{action_name}' - NOT FOUND in scoring matrix")
            else:
                print(f"      ✓ '{action_name}' - Score: {score}")
        
        # Check Blue Team actions
        blue_actions = phase.available_actions.get("blue", []) if phase.available_actions else []
        blue_scoring = scoring_matrix.get((phase.order_index, "blue"), {})
        
        print(f"  Blue Team:")
        print(f"    Actions in scenario: {len(blue_actions)}")
        print(f"    Actions in scoring matrix: {len(blue_scoring)}")
        
        for action in blue_actions:
            action_name = action.get("name", "")
            score = blue_scoring.get(action_name, None)
            if score is None:
                print(f"      ❌ '{action_name}' - NOT FOUND in scoring matrix")
            else:
                print(f"      ✓ '{action_name}' - Score: {score}")
        
        print()
    
    # Check existing games and decisions
    games = db.query(Game).filter(Game.scenario_id == scenario.id).all()
    print(f"Found {len(games)} game(s) using this scenario")
    print()
    
    for game in games:
        print(f"Game ID: {game.id}")
        
        # Check decisions
        decisions = db.query(PhaseDecision).filter(
            PhaseDecision.game_id == game.id
        ).all()
        
        print(f"  Total decisions: {len(decisions)}")
        
        for decision in decisions:
            phase = db.query(ScenarioPhase).filter(ScenarioPhase.id == decision.phase_id).first()
            team = db.query(Team).filter(Team.id == decision.team_id).first()
            
            if not phase or not team:
                continue
            
            # Extract action
            selected_actions = []
            if isinstance(decision.actions, dict):
                if "selected" in decision.actions:
                    selected_actions = decision.actions["selected"]
            elif isinstance(decision.actions, list):
                selected_actions = decision.actions
            
            primary_action = selected_actions[0] if selected_actions else "N/A"
            
            # Test scoring
            test_score = get_optimal_score(
                scenario_name=scenario.name,
                phase_order_index=phase.order_index,
                team_role=team.role,
                selected_action=primary_action
            )
            
            print(f"    Phase {phase.order_index} ({team.role}):")
            print(f"      Action: '{primary_action}'")
            print(f"      Score in DB: {decision.score_awarded}")
            print(f"      Test score: {test_score}")
            if decision.score_awarded != test_score:
                print(f"      ⚠️  MISMATCH!")
            print()
    
    print("=" * 60)
    print("Diagnostic Complete")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

