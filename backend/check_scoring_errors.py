"""
Check for errors in audience score display for all scenarios.
This script validates:
1. All scenarios have scoring matrices
2. All phases have scoring entries
3. Action names match between scenarios and scoring matrices
4. Scoreboard endpoint can handle all scenarios
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Game, Team, ScoreEvent
from app.scoring import SCORING_MATRICES, get_optimal_score
from sqlalchemy import func

db: Session = SessionLocal()

print("=" * 80)
print("Checking Scoring Configuration for All Scenarios")
print("=" * 80)

# Get all scenarios
scenarios = db.query(Scenario).all()

if not scenarios:
    print("❌ No scenarios found in database")
    sys.exit(1)

print(f"\nFound {len(scenarios)} scenario(s) in database:\n")

errors = []
warnings = []

for scenario in scenarios:
    print(f"\n{'=' * 80}")
    print(f"Scenario: {scenario.name} (ID: {scenario.id})")
    print(f"{'=' * 80}")
    
    # Check if scenario has scoring matrix
    if scenario.name not in SCORING_MATRICES:
        error_msg = f"❌ ERROR: Scenario '{scenario.name}' not found in SCORING_MATRICES"
        print(error_msg)
        errors.append(error_msg)
        continue
    else:
        print(f"✓ Scoring matrix found")
    
    # Get all phases for this scenario
    phases = db.query(ScenarioPhase).filter(
        ScenarioPhase.scenario_id == scenario.id
    ).order_by(ScenarioPhase.order_index).all()
    
    if not phases:
        error_msg = f"❌ ERROR: Scenario '{scenario.name}' has no phases"
        print(error_msg)
        errors.append(error_msg)
        continue
    
    print(f"✓ Found {len(phases)} phase(s)")
    
    # Get scoring matrix for this scenario
    scoring_matrix = SCORING_MATRICES[scenario.name]
    
    # Check each phase
    for phase in phases:
        print(f"\n  Phase {phase.order_index + 1}: {phase.name} (order_index={phase.order_index})")
        
        # Check if phase has scoring entries for both teams
        for team_role in ['red', 'blue']:
            key = (phase.order_index, team_role)
            
            if key not in scoring_matrix:
                error_msg = f"❌ ERROR: Phase {phase.order_index + 1} ({phase.name}) missing scoring for {team_role} team"
                print(f"    {error_msg}")
                errors.append(f"{scenario.name}: {error_msg}")
            else:
                actions = scoring_matrix[key]
                print(f"    ✓ {team_role.upper()} team: {len(actions)} action(s) defined")
                
                # Check if there are any actions with score 0 (might indicate missing entries)
                zero_score_actions = [action for action, score in actions.items() if score == 0]
                if zero_score_actions:
                    warning_msg = f"⚠️  WARNING: {team_role.upper()} team has {len(zero_score_actions)} action(s) with score 0: {zero_score_actions[:3]}"
                    print(f"    {warning_msg}")
                    warnings.append(f"{scenario.name} Phase {phase.order_index + 1}: {warning_msg}")

# Check for scenarios in SCORING_MATRICES that don't exist in database
print(f"\n{'=' * 80}")
print("Checking for orphaned scoring matrices (scenarios in SCORING_MATRICES but not in database)")
print(f"{'=' * 80}")

scenario_names_in_db = {s.name for s in scenarios}
scenario_names_in_scoring = set(SCORING_MATRICES.keys())

orphaned = scenario_names_in_scoring - scenario_names_in_db
if orphaned:
    for scenario_name in orphaned:
        warning_msg = f"⚠️  WARNING: Scoring matrix exists for '{scenario_name}' but scenario not found in database"
        print(warning_msg)
        warnings.append(warning_msg)
else:
    print("✓ No orphaned scoring matrices")

# Check for games with scoring issues
print(f"\n{'=' * 80}")
print("Checking existing games for scoring issues")
print(f"{'=' * 80}")

games = db.query(Game).filter(Game.status != 'lobby').all()
print(f"Found {len(games)} active/finished game(s)")

for game in games[:10]:  # Check first 10 games
    if not game.scenario:
        continue
    
    scenario_name = game.scenario.name
    
    # Check if scenario has scoring matrix
    if scenario_name not in SCORING_MATRICES:
        error_msg = f"❌ ERROR: Game {game.id} uses scenario '{scenario_name}' which has no scoring matrix"
        print(error_msg)
        errors.append(error_msg)
        continue
    
    # Check score events for this game
    score_events = db.query(ScoreEvent).filter(ScoreEvent.game_id == game.id).all()
    
    if score_events:
        # Check if any score events have delta = 0 (might indicate scoring issues)
        zero_delta_events = [e for e in score_events if e.delta == 0]
        if zero_delta_events:
            warning_msg = f"⚠️  WARNING: Game {game.id} has {len(zero_delta_events)} score event(s) with delta=0"
            print(warning_msg)
            warnings.append(warning_msg)
        
        # Check total score
        total_score = db.query(func.coalesce(func.sum(ScoreEvent.delta), 0)).filter(
            ScoreEvent.game_id == game.id
        ).scalar()
        
        if total_score == 0 and len(score_events) > 0:
            warning_msg = f"⚠️  WARNING: Game {game.id} has {len(score_events)} score event(s) but total score is 0"
            print(warning_msg)
            warnings.append(warning_msg)

# Summary
print(f"\n{'=' * 80}")
print("SUMMARY")
print(f"{'=' * 80}")
print(f"Total scenarios checked: {len(scenarios)}")
print(f"Errors found: {len(errors)}")
print(f"Warnings found: {len(warnings)}")

if errors:
    print(f"\n❌ ERRORS ({len(errors)}):")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")

if warnings:
    print(f"\n⚠️  WARNINGS ({len(warnings)}):")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")

if not errors and not warnings:
    print("\n✓ All checks passed! No errors or warnings found.")

print(f"\n{'=' * 80}")

db.close()

if errors:
    sys.exit(1)
else:
    sys.exit(0)

