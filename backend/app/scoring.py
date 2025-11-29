"""
Automated scoring system for team decisions.
Awards points based on how well selected actions align with phase objectives.
"""
from typing import Dict, List, Tuple, Optional

# Scoring configuration: (scenario_name, phase_order_index, team_role) -> Dict of (action_name, points)
# Points: 10 = optimal, 7 = good, 4 = acceptable, 1 = poor, 0 = counterproductive

# Ransomware Incident Response scenario scoring
RANSOMWARE_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
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

# Email Bomb & Social Engineering Attack scenario scoring
EMAIL_BOMB_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Email Bomb Deployment (order_index=0)
    (0, "red"): {
        "Establish persistence": 10,  # Deploy email bomb infrastructure
        "Cover tracks": 7,           # Make emails appear legitimate
        "Move laterally": 4,        # Too early, no access yet
        "Escalate privileges": 3,   # Too early
        "Exfiltrate data": 1,       # Way too early
    },
    (0, "blue"): {
        "Block IP address": 10,     # Block email sources
        "Collect forensic evidence": 8,  # Analyze email patterns
        "Deploy countermeasures": 7, # Email filtering rules
        "Escalate to management": 6, # Alert user before social engineering
        "Isolate host": 4,          # Too early, no compromise yet
    },
    
    # Phase 2: Social Engineering Call (order_index=1)
    (1, "red"): {
        "Establish persistence": 10,  # Establish trust and rapport
        "Cover tracks": 8,            # Appear legitimate
        "Move laterally": 4,          # Too early, no credentials yet
        "Escalate privileges": 3,     # Too early
        "Exfiltrate data": 1,         # Way too early
    },
    (1, "blue"): {
        "Escalate to management": 10, # Alert user immediately
        "Collect forensic evidence": 8, # Document call details
        "Deploy countermeasures": 6,  # User awareness training
        "Block IP address": 5,        # May not have IP yet
        "Isolate host": 3,           # Too early
    },
    
    # Phase 3: Credential Harvesting (order_index=2)
    (2, "red"): {
        "Establish persistence": 10,  # Harvest and verify credentials
        "Cover tracks": 7,            # Hide fake portal
        "Move laterally": 5,          # Starting to test access
        "Escalate privileges": 4,     # Too early
        "Exfiltrate data": 2,         # Too early
    },
    (2, "blue"): {
        "Block IP address": 10,       # Block fake portal
        "Collect forensic evidence": 9, # Document credential compromise
        "Deploy countermeasures": 8,  # Force password reset
        "Escalate to management": 7,   # Breach notification
        "Isolate host": 6,            # Isolate compromised account
    },
    
    # Phase 4: Initial Access & Privilege Escalation (order_index=3)
    (3, "red"): {
        "Escalate privileges": 10,    # Gain admin access
        "Move laterally": 9,          # Access multiple systems
        "Establish persistence": 8,    # Create backdoors
        "Cover tracks": 7,            # Hide access
        "Exfiltrate data": 4,         # Starting to prepare
    },
    (3, "blue"): {
        "Isolate host": 10,           # Isolate compromised account
        "Deploy countermeasures": 9,  # Revoke access, reset passwords
        "Collect forensic evidence": 8, # Document unauthorized access
        "Escalate to management": 7,   # Coordinate response
        "Block IP address": 6,        # May be too late
    },
    
    # Phase 5: Lateral Movement & Data Exfiltration (order_index=4)
    (4, "red"): {
        "Exfiltrate data": 10,       # Primary objective
        "Move laterally": 9,          # Access more systems
        "Cover tracks": 8,            # Hide exfiltration
        "Establish persistence": 7,    # Maintain access
        "Escalate privileges": 5,     # Already done
    },
    (4, "blue"): {
        "Block IP address": 10,       # Stop exfiltration
        "Isolate host": 9,            # Contain breach
        "Collect forensic evidence": 8, # Document data loss
        "Escalate to management": 8,    # Breach notification, compliance
        "Deploy countermeasures": 6,   # May be too late
    },
}

# SharePoint RCE Zero-Day Exploitation scenario scoring
SHAREPOINT_RCE_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Vulnerability Disclosure & Initial Reconnaissance (order_index=0)
    (0, "red"): {
        "Establish persistence": 4,      # Too early, no access yet
        "Cover tracks": 7,               # Good for stealthy recon
        "Move laterally": 2,             # Way too early
        "Escalate privileges": 3,        # Too early
        "Exfiltrate data": 1,            # Way too early
    },
    (0, "blue"): {
        "Monitor threat intelligence": 10, # Primary objective
        "Assess vulnerability": 9,       # Critical assessment
        "Review logs": 8,                # Important detection
        "Prepare mitigation": 7,         # Good preparation
        "Update monitoring": 6,          # Good but secondary
    },
    
    # Phase 2: Exploitation Attempt & Initial Access (order_index=1)
    (1, "red"): {
        "Establish persistence": 10,     # Primary objective
        "Cover tracks": 8,               # Important to evade detection
        "Move laterally": 6,            # Good but early
        "Escalate privileges": 7,        # Good timing
        "Exfiltrate data": 2,            # Too early
    },
    (1, "blue"): {
        "Isolate host": 10,              # Primary - isolate compromised server
        "Collect forensic evidence": 9,   # Critical for analysis
        "Block IP address": 8,            # Block C2 communications
        "Deploy countermeasures": 7,     # Good defense
        "Escalate to management": 5,     # Important but not immediate
    },
    
    # Phase 3: Privilege Escalation & Persistence (order_index=2)
    (2, "red"): {
        "Escalate privileges": 10,      # Primary objective
        "Establish persistence": 10,     # Primary objective
        "Cover tracks": 7,               # Important
        "Move laterally": 6,            # Good preparation
        "Exfiltrate data": 3,            # Too early
    },
    (2, "blue"): {
        "Remove persistence": 10,        # Primary - remove all persistence
        "Revoke credentials": 9,         # Critical security
        "Prevent lateral movement": 8,    # Important containment
        "Document changes": 7,           # Good for forensics
        "Isolate host": 6,               # Good but may be late
    },
    
    # Phase 4: Data Access & Exfiltration (order_index=3)
    (3, "red"): {
        "Exfiltrate data": 10,          # Primary objective
        "Cover tracks": 8,               # Hide exfiltration
        "Establish persistence": 7,       # Maintain access
        "Move laterally": 5,            # Already done
        "Escalate privileges": 4,       # Already done
    },
    (3, "blue"): {
        "Block exfiltration": 10,        # Primary - stop data theft
        "Assess data breach": 9,         # Critical assessment
        "Prepare notifications": 8,      # Regulatory compliance
        "Isolate host": 7,               # Contain breach
        "Collect forensic evidence": 6,   # Important but secondary
    },
    
    # Phase 5: Remediation & Post-Incident (order_index=4)
    (4, "red"): {
        "Cover tracks": 10,              # Hide remaining access
        "Establish persistence": 9,       # Maintain backdoors
        "Move laterally": 7,            # If not already done
        "Exfiltrate data": 5,            # Already done
        "Escalate privileges": 4,       # Already done
    },
    (4, "blue"): {
        "Deploy patches": 10,           # Primary - patch vulnerability
        "Complete remediation": 9,       # Critical cleanup
        "Conduct forensics": 8,          # Full investigation
        "Assess compliance": 7,          # Regulatory requirements
        "Create AAR": 6,                 # Important but secondary
    },
}

# Tutorial Scenario Scoring (Simple scoring for learning)
TUTORIAL_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Initial Detection (order_index=0)
    (0, "red"): {
        "Establish persistence": 8,  # Good for establishing access
        "Cover tracks": 7,           # Good for avoiding detection
        "Escalate privileges": 4,    # Too early, risky
        "Move laterally": 3,         # Too early
        "Exfiltrate data": 1,        # Way too early
    },
    (0, "blue"): {
        "Isolate host": 9,           # Excellent for containment
        "Collect forensic evidence": 8,  # Critical for analysis
        "Block IP address": 6,       # Good but may be too late
        "Deploy countermeasures": 5, # Good but takes time
        "Escalate to management": 4,  # Important but not immediate
    },
    
    # Phase 2: Response & Containment (order_index=1)
    (1, "red"): {
        "Establish persistence": 8,  # Maintain access
        "Cover tracks": 9,           # Critical to avoid detection
        "Escalate privileges": 6,    # Good timing
        "Move laterally": 5,         # Starting to explore
        "Exfiltrate data": 2,        # Too early
    },
    (1, "blue"): {
        "Isolate host": 10,          # Primary - contain the threat
        "Block IP address": 9,       # Block C2 communication
        "Collect forensic evidence": 8, # Important for analysis
        "Deploy countermeasures": 7, # Good defense
        "Escalate to management": 6,  # Coordination needed
    },
}

# Map scenario names to their scoring matrices
SCORING_MATRICES: Dict[str, Dict[Tuple[int, str], Dict[str, int]]] = {
    "Ransomware Incident Response": RANSOMWARE_SCORING,
    "Email Bomb & Social Engineering Attack": EMAIL_BOMB_SCORING,
    "SharePoint RCE Zero-Day Exploitation": SHAREPOINT_RCE_SCORING,
    "Tutorial: Basic Security Incident": TUTORIAL_SCORING,
}


def get_optimal_score(
    scenario_name: str,
    phase_order_index: int,
    team_role: str,
    selected_action: str
) -> int:
    """
    Get the score for a selected action based on scenario, phase and team role.
    Returns 0 if action not found in matrix.
    """
    # Get the appropriate scoring matrix for this scenario
    scoring_matrix = SCORING_MATRICES.get(scenario_name)
    if not scoring_matrix:
        # Fallback to ransomware scoring if scenario not found
        scoring_matrix = RANSOMWARE_SCORING
    
    key = (phase_order_index, team_role)
    if key not in scoring_matrix:
        return 0
    
    return scoring_matrix[key].get(selected_action, 0)


def calculate_team_decision_score(
    scenario_name: str,
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
    
    score = get_optimal_score(scenario_name, phase_order_index, team_role, primary_action)
    
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

