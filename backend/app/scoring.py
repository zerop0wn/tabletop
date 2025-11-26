"""
Automated scoring system for team decisions.
Awards points based on how well selected actions align with phase objectives.
"""
from typing import Dict, List, Tuple

# Scoring configuration: (phase_order_index, team_role) -> Dict of (action_name, points)
# Points: 10 = optimal, 7 = good, 4 = acceptable, 1 = poor, 0 = counterproductive

SCORING_MATRIX: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Initial Compromise (order_index=0)
    (0, "red"): {
        "Establish persistence": 10,  # Primary objective
        "Cover tracks": 7,           # Secondary objective
        "Escalate privileges": 4,    # Too early, risky
        "Move laterally": 3,         # Too early
        "Exfiltrate data": 1,        # Way too early
    },
    (0, "blue"): {
        "Isolate host": 10,          # Primary objective
        "Collect forensic evidence": 8,  # Critical for analysis
        "Block IP address": 6,       # Good but may be too late
        "Deploy countermeasures": 5, # Good but takes time
        "Escalate to management": 4,  # Important but not immediate
    },
    
    # Phase 2: Establishing Foothold (order_index=1)
    (1, "red"): {
        "Establish persistence": 10,  # Primary objective
        "Move laterally": 9,          # Critical for network mapping
        "Escalate privileges": 7,     # Good timing
        "Cover tracks": 6,            # Secondary
        "Exfiltrate data": 2,         # Too early
    },
    (1, "blue"): {
        "Block IP address": 10,       # Primary - block C2
        "Deploy countermeasures": 8,  # Critical defense
        "Collect forensic evidence": 7, # Important
        "Isolate host": 6,            # Good but may be late
        "Escalate to management": 5,   # Coordination needed
    },
    
    # Phase 3: Privilege Escalation & Lateral Movement (order_index=2)
    (2, "red"): {
        "Escalate privileges": 10,    # Primary objective
        "Move laterally": 10,         # Primary objective
        "Cover tracks": 7,            # Important to avoid detection
        "Establish persistence": 6,    # Good but already done
        "Exfiltrate data": 4,         # Starting to prepare
    },
    (2, "blue"): {
        "Isolate host": 10,            # Isolate critical systems
        "Deploy countermeasures": 9,   # Network segmentation
        "Escalate to management": 8,    # Coordinate response
        "Collect forensic evidence": 6, # Document movement
        "Block IP address": 5,         # May be too late
    },
    
    # Phase 4: Data Exfiltration (order_index=3)
    (3, "red"): {
        "Exfiltrate data": 10,        # Primary objective
        "Cover tracks": 8,            # Hide exfiltration
        "Establish persistence": 7,    # Maintain access
        "Move laterally": 5,          # Already done
        "Escalate privileges": 4,     # Already done
    },
    (3, "blue"): {
        "Block IP address": 10,       # Stop exfiltration
        "Collect forensic evidence": 9, # Document theft
        "Escalate to management": 8,    # Breach notification
        "Deploy countermeasures": 6,   # May be too late
        "Isolate host": 5,            # May be too late
    },
    
    # Phase 5: Ransomware Deployment & Response (order_index=4)
    (4, "red"): {
        "Move laterally": 10,          # Spread encryption
        "Cover tracks": 9,            # Hide deployment
        "Establish persistence": 8,    # Maintain access
        "Exfiltrate data": 6,         # Already done
        "Escalate privileges": 5,      # Already done
    },
    (4, "blue"): {
        "Isolate host": 10,            # Contain spread
        "Deploy countermeasures": 9,   # Prevent further encryption
        "Escalate to management": 8,    # Coordinate response
        "Collect forensic evidence": 6, # Document impact
        "Block IP address": 4,         # Too late
    },
}


def get_optimal_score(phase_order_index: int, team_role: str, selected_action: str) -> int:
    """
    Get the score for a selected action based on phase and team role.
    Returns 0 if action not found in matrix.
    """
    key = (phase_order_index, team_role)
    if key not in SCORING_MATRIX:
        return 0
    
    return SCORING_MATRIX[key].get(selected_action, 0)


def calculate_team_decision_score(
    phase_order_index: int,
    team_role: str,
    selected_actions: List[str]
) -> Tuple[int, str]:
    """
    Calculate score for a team's decision.
    Returns (score, explanation)
    
    Takes the primary action (first in list) and scores it.
    """
    if not selected_actions:
        return (0, "No action selected")
    
    # Get the primary action (first in list)
    primary_action = selected_actions[0] if selected_actions else None
    
    if not primary_action or not isinstance(primary_action, str):
        return (0, "Invalid action format")
    
    score = get_optimal_score(phase_order_index, team_role, primary_action)
    
    # Determine explanation
    if score >= 9:
        explanation = f"Excellent choice: {primary_action} perfectly aligns with phase objectives"
    elif score >= 7:
        explanation = f"Good choice: {primary_action} effectively supports phase objectives"
    elif score >= 4:
        explanation = f"Acceptable choice: {primary_action} somewhat supports objectives"
    elif score >= 1:
        explanation = f"Poor choice: {primary_action} doesn't align well with phase objectives"
    else:
        explanation = f"Invalid or counterproductive action: {primary_action}"
    
    return (score, explanation)


def calculate_weighted_score(
    base_score: int,
    team_size: int,
    average_team_size: float,
    normalize: bool = False
) -> int:
    """
    Calculate weighted score accounting for team size differences.
    
    Args:
        base_score: The base score from action selection
        team_size: Number of players on this team
        average_team_size: Average team size across all teams
        normalize: If True, normalize scores. If False, use base score.
    
    Returns:
        Adjusted score
    """
    if not normalize:
        # Simple: same points regardless of team size
        return base_score
    
    # Normalize: smaller teams get slight boost, larger teams slight reduction
    # This compensates for coordination challenges
    if average_team_size == 0:
        return base_score
    
    size_ratio = team_size / average_team_size
    
    # Boost smaller teams by up to 10%, reduce larger teams by up to 5%
    if size_ratio < 1.0:
        multiplier = 1.0 + (1.0 - size_ratio) * 0.1  # Up to 10% boost
    else:
        multiplier = 1.0 - (size_ratio - 1.0) * 0.05  # Up to 5% reduction
    
    adjusted_score = int(base_score * multiplier)
    return max(1, min(10, adjusted_score))  # Clamp between 1-10

