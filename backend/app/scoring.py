"""
Automated scoring system for team decisions.
Awards points based on how well selected actions align with phase objectives.
"""
from typing import Dict, List, Tuple, Optional

# Scoring configuration: (scenario_name, phase_order_index, team_role) -> Dict of (action_name, points)
# Points: 10 = optimal, 7 = good, 4 = acceptable, 1 = poor, 0 = counterproductive

# Ransomware Incident Response scenario scoring - REDESIGNED with artifact-driven decisions
RANSOMWARE_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Initial Compromise (order_index=0) - REDESIGNED
    # Artifacts show Marketing has weaker security (outdated EDR) vs Finance (strong EDR)
    # Red Team should prioritize Marketing for persistence (lower detection risk)
    # Blue Team should prioritize Marketing for containment (higher risk)
    (0, "red"): {
        "Focus on Marketing Department (WS-MKT-015)": 10,  # CORRECT - Artifacts show Marketing has weaker EDR
        "Focus on Finance Department (WS-FIN-042)": 4,     # WRONG - Finance has strong EDR, attack was blocked
        "Split efforts between both departments": 6,       # MEDIUM - Spreads risk
        "Cover tracks": 7,                                 # Secondary objective - Good for avoiding detection
        "Escalate privileges": 3,                          # Too early, risky
        "Move laterally": 2,                               # Too early
        "Exfiltrate data": 1,                              # Way too early
        # Fallback for generic actions
        "Establish persistence": 8,                        # Generic fallback
    },
    (0, "blue"): {
        "Isolate Marketing Department host (WS-MKT-015)": 10,  # CORRECT - Artifacts show Marketing is higher risk
        "Isolate Finance Department host (WS-FIN-042)": 6,     # WRONG - Finance already blocked, lower risk
        "Isolate both hosts": 8,                               # MEDIUM - Conservative but may be overkill
        "Collect forensic evidence": 8,                        # Critical for analysis
        "Block IP address": 6,                                 # Good but may be too late
        "Deploy countermeasures": 5,                           # Good but takes time
        "Escalate to management": 4,                           # Important but not immediate
        # Fallback for generic actions
        "Isolate host": 8,                                     # Generic fallback
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
    
    # Phase 3: Privilege Escalation & Lateral Movement (order_index=2) - REDESIGNED
    # Artifacts show WS-MKT-02 has unpatched LPE vulnerability vs WS-FIN-01 is fully patched
    # Red Team should prioritize WS-MKT-02 for escalation (high success probability)
    # Blue Team should prioritize WS-MKT-02 for containment (high risk)
    (2, "red"): {
        "Escalate privileges on WS-MKT-02 (Marketing)": 10,  # CORRECT - Artifacts show unpatched LPE vulnerability
        "Escalate privileges on WS-FIN-01 (Finance)": 3,     # WRONG - Fully patched, low success probability
        "Split efforts - escalate on both hosts": 5,         # MEDIUM - Spreads risk
        "Move laterally": 7,                                 # Secondary - Good after escalation
        "Cover tracks": 6,                                   # Important to avoid detection
        "Establish persistence": 4,                          # Good but already done
        "Exfiltrate data": 2,                                # Too early
        # Fallback for generic actions
        "Escalate privileges": 8,                             # Generic fallback
    },
    (2, "blue"): {
        "Isolate WS-MKT-02 (Marketing host)": 10,            # CORRECT - Artifacts show WS-MKT-02 is high risk
        "Isolate WS-FIN-01 (Finance host)": 6,              # WRONG - WS-FIN-01 is fully patched, lower risk
        "Isolate both hosts": 8,                             # MEDIUM - Conservative approach
        "Deploy countermeasures": 9,                         # Network segmentation, patching
        "Escalate to management": 8,                          # Coordinate response
        "Collect forensic evidence": 6,                       # Document movement
        "Block IP address": 5,                                # May be too late
        # Fallback for generic actions
        "Isolate host": 8,                                    # Generic fallback
    },
    
    # Phase 4: Data Exfiltration (order_index=3) - REDESIGNED
    # Artifacts show FS-02 has weaker DLP coverage vs FS-01 has strong DLP (already alerted)
    # Red Team should prioritize FS-02 for exfiltration (lower detection risk)
    # Blue Team should prioritize FS-01 for containment (already has HIGH-SEVERITY alerts)
    (3, "red"): {
        "Exfiltrate data from FS-02 (HR/Operations)": 10,  # CORRECT - Artifacts show weaker DLP, lower detection risk
        "Exfiltrate data from FS-01 (Finance)": 4,       # WRONG - Strong DLP, already has HIGH-SEVERITY alerts
        "Exfiltrate from both servers simultaneously": 6, # MEDIUM - Higher detection risk
        "Cover tracks": 8,                                 # Hide exfiltration
        "Establish persistence": 7,                        # Maintain access
        "Move laterally": 4,                               # Already done
        "Escalate privileges": 3,                           # Already done
        # Fallback for generic actions
        "Exfiltrate data": 8,                              # Generic fallback
    },
    (3, "blue"): {
        "Block exfiltration from FS-01 (Finance)": 10,     # CORRECT - Artifacts show FS-01 has HIGH-SEVERITY alerts
        "Block exfiltration from FS-02 (HR/Operations)": 6, # WRONG - FS-02 has weaker DLP, lower priority
        "Block exfiltration from both servers": 8,         # MEDIUM - Conservative approach
        "Collect forensic evidence": 9,                     # Document theft
        "Escalate to management": 8,                        # Breach notification
        "Deploy countermeasures": 5,                       # May be too late
        "Isolate host": 4,                                 # May be too late
        # Fallback for generic actions
        "Block IP address": 8,                             # Generic fallback
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
        "Continue email bomb campaign": 10,  # Primary objective - maintain email flood
        "Intensify email bomb": 8,          # Increase impact
        "Prepare Teams call": 9,            # Critical for Phase 2
        "Monitor user response": 7,         # Important for timing
        "Cover tracks": 5,                  # Secondary
    },
    (0, "blue"): {
        "Contact user and warn about social engineering": 10,  # CRITICAL - Prevent Phase 2
        "Enhance email filtering": 8,       # Block additional spam
        "Monitor for follow-up attacks": 7, # Proactive defense
        "Collect forensic evidence": 6,     # Important but takes time
        "Isolate user's email account": 4,   # Too disruptive
    },
    
    # Phase 2: Teams Call Impersonation (order_index=1)
    (1, "red"): {
        "Execute Teams call and request remote access": 10,  # Primary objective
        "Intensify social engineering": 8,   # Increase success rate
        "Request credentials during call": 7, # Higher risk but may work
        "Monitor user response": 6,         # Adjust tactics
        "Cover tracks": 5,                  # Secondary
    },
    (1, "blue"): {
        "Contact user and terminate remote session": 10,  # CRITICAL - Stop remote access
        "Block Quick Assist": 9,            # Prevent unauthorized access
        "Investigate caller identity": 8,    # Verify impersonation
        "Collect forensic evidence": 6,      # Important but takes time
        "Monitor for credential harvesting": 5, # Proactive but may be too late
    },
    
    # Phase 3: Credential Harvesting (order_index=2)
    (2, "red"): {
        "Request credentials during remote session": 10,  # Primary objective
        "Use keylogging": 8,                 # Alternative method
        "Validate credentials": 9,          # Critical for next phase
        "Deploy credential dumper": 6,      # Higher detection risk
        "Cover tracks": 5,                  # Secondary
    },
    (2, "blue"): {
        "Force password reset immediately": 10,  # CRITICAL - Secure account
        "Disable MFA temporarily": 9,       # Prevent MFA bypass
        "Review account activity": 8,        # Understand compromise
        "Collect forensic evidence": 6,      # Important but takes time
        "Monitor for persistence": 5,       # Proactive but may be too late
    },
    
    # Phase 4: Remote Access & Persistence (order_index=3)
    (3, "red"): {
        "Deploy scheduled task persistence": 10,  # Primary - reliable method
        "Deploy registry persistence": 9,        # Secondary - good backup
        "Deploy email forwarding rule": 8,        # Data exfiltration
        "Deploy payloads": 7,                     # C2 preparation
        "Cover tracks": 5,                        # Secondary
    },
    (3, "blue"): {
        "Remove all persistence mechanisms": 10,  # CRITICAL - Prevent long-term access
        "Quarantine malware": 9,                  # Remove malicious files
        "Terminate remote session": 8,             # Stop ongoing access
        "Isolate device": 7,                      # Contain threat
        "Collect forensic evidence": 5,           # Important but takes time
    },
    
    # Phase 5: Initial Access & C2 Communication (order_index=4)
    (4, "red"): {
        "Establish C2 connection": 10,        # Primary objective
        "Execute credential dumper": 8,       # Harvest additional credentials
        "Scan internal network": 7,           # Lateral movement prep
        "Exfiltrate data": 6,                  # Higher detection risk
        "Cover tracks": 5,                     # Secondary
    },
    (4, "blue"): {
        "Isolate device immediately": 10,     # CRITICAL - Stop C2 communication
        "Block C2 server": 9,                  # Terminate C2 connection
        "Terminate malicious processes": 8,    # Stop payload execution
        "Investigate data exfiltration": 7,     # Understand impact
        "Collect forensic evidence": 5,        # Important but takes time
    },
}

# New Ransomware Attack: Advanced Persistent Threat scenario scoring
NEW_RANSOMWARE_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Initial Access - IT vs Sales (order_index=0)
    # Artifacts show Sales has weaker security (outdated EDR) vs IT (strong EDR, blocked attack)
    # Red Team should prioritize Sales for persistence (lower detection risk)
    # Blue Team should prioritize Sales for containment (higher risk)
    (0, "red"): {
        "Focus on Sales Department (WS-SLS-203)": 10,  # CORRECT - Artifacts show Sales has weaker EDR
        "Focus on IT Department (WS-IT-089)": 4,       # WRONG - IT has strong EDR, attack was blocked
        "Split efforts between both departments": 6,   # MEDIUM - Spreads risk
        "Cover tracks": 7,                             # Secondary objective
        "Escalate privileges": 3,                      # Too early, risky
    },
    (0, "blue"): {
        "Isolate Sales Department host (WS-SLS-203)": 10,  # CORRECT - Artifacts show Sales is higher risk
        "Isolate IT Department host (WS-IT-089)": 6,     # WRONG - IT already blocked, lower risk
        "Isolate both hosts": 8,                         # MEDIUM - Conservative
        "Collect forensic evidence": 8,                   # Critical for analysis
        "Deploy countermeasures": 5,                      # Good but takes time
    },
    
    # Phase 2: Establishing Persistence (order_index=1)
    # Artifacts show Registry Run Key is best (detected but not blocked, low visibility)
    # Scheduled Task is detected but visible, Service Creation is blocked
    (1, "red"): {
        "Deploy Registry Run Key persistence": 10,      # CORRECT - Best balance of success and stealth
        "Deploy Scheduled Task persistence": 7,         # Good but more visible
        "Deploy Service Creation persistence": 2,        # WRONG - Blocked by Defender
        "Move laterally": 6,                            # Secondary
        "Cover tracks": 7,                              # Important
    },
    (1, "blue"): {
        "Audit and clean registry": 10,                 # CORRECT - Registry is the persistence method used
        "Remove scheduled tasks": 8,                    # Good but secondary
        "Monitor and block services": 6,                # Good but services were blocked
        "Collect forensic evidence": 8,                 # Critical
        "Deploy countermeasures": 7,                    # Good defense
    },
    
    # Phase 3: Privilege Escalation (order_index=2)
    # Artifacts show APP-02 has unpatched LPE vulnerability vs FS-01 is fully patched
    # Red Team should prioritize APP-02 for escalation (high success probability)
    # Blue Team should prioritize APP-02 for containment (high risk)
    (2, "red"): {
        "Escalate privileges on APP-02 (Application Server)": 10,  # CORRECT - Unpatched LPE vulnerability
        "Escalate privileges on FS-01 (File Server)": 3,           # WRONG - Fully patched, low success
        "Attempt escalation on both servers": 5,                   # MEDIUM - Spreads risk
        "Move laterally": 7,                                       # Secondary
        "Cover tracks": 6,                                         # Important
    },
    (2, "blue"): {
        "Isolate APP-02 (Application Server)": 10,     # CORRECT - Artifacts show APP-02 is high risk
        "Isolate FS-01 (File Server)": 6,              # WRONG - FS-01 is fully patched, lower risk
        "Isolate both servers": 8,                     # MEDIUM - Conservative
        "Patch vulnerabilities": 9,                    # Critical for APP-02
        "Collect forensic evidence": 7,                 # Important
    },
    
    # Phase 4: Lateral Movement & Data Discovery (order_index=3)
    # Artifacts show DB-FIN-02 is accessible and has successful access vs DB-CUST-01 is isolated and blocked
    # Red Team should prioritize DB-FIN-02 (accessible, weaker controls)
    # Blue Team should prioritize DB-FIN-02 (shows signs of compromise)
    (3, "red"): {
        "Target DB-FIN-02 (Financial Records)": 10,    # CORRECT - Accessible, weaker controls
        "Target DB-CUST-01 (Customer Database)": 2,   # WRONG - Not accessible, isolated
        "Target both databases": 4,                    # MEDIUM - One not accessible
        "Cover tracks": 8,                              # Important
        "Establish persistence": 7,                    # Good
    },
    (3, "blue"): {
        "Isolate DB-FIN-02 (Financial Records)": 10,   # CORRECT - Shows signs of compromise
        "Isolate DB-CUST-01 (Customer Database)": 6,   # WRONG - Already secure, lower priority
        "Isolate both databases": 8,                    # MEDIUM - Conservative
        "Block database access": 9,                     # Critical
        "Collect forensic evidence": 8,                 # Important
    },
    
    # Phase 5: Data Exfiltration (order_index=4)
    # Artifacts show DNS tunneling has lower detection risk vs HTTPS is well-monitored
    # Red Team should prioritize DNS tunneling (more reliable, less detected)
    # Blue Team should prioritize blocking DNS tunneling (less monitored)
    (4, "red"): {
        "Use DNS tunneling": 10,                       # CORRECT - Lower detection risk, more reliable
        "Use HTTPS encrypted tunnel": 6,               # MEDIUM - Well-monitored but faster
        "Split data across both methods": 7,           # MEDIUM - Balances speed and stealth
        "Cover tracks": 8,                              # Important
        "Establish persistence": 7,                     # Good
    },
    (4, "blue"): {
        "Block DNS tunneling": 10,                     # CORRECT - Less monitored, needs attention
        "Block HTTPS exfiltration": 8,                 # Good but well-monitored already
        "Deploy DLP countermeasures": 9,               # Comprehensive
        "Collect forensic evidence": 8,                # Critical
        "Escalate to management": 7,                  # Important
    },
}

# SharePoint RCE Zero-Day Exploitation scenario scoring
SHAREPOINT_RCE_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Vulnerability Disclosure & Initial Reconnaissance (order_index=0)
    (0, "red"): {
        "Conduct version detection and endpoint mapping": 10,  # Primary objective
        "Test vulnerability without detection": 9,              # Critical for exploitation
        "Prepare exploitation payload": 8,                      # Good preparation
        "Gather server configuration details": 7,               # Important reconnaissance
        "Cover tracks": 6,                                      # Secondary
    },
    (0, "blue"): {
        "Monitor threat intelligence and assess vulnerability": 10,  # Primary objective
        "Review SharePoint logs for reconnaissance activity": 9,     # Critical detection
        "Prepare emergency mitigation procedures": 8,                # Important preparation
        "Assess business impact and patch readiness": 7,            # Good assessment
        "Update monitoring and alerting": 6,                        # Secondary
    },
    
    # Phase 2: Exploitation Attempt & Initial Access (order_index=1)
    (1, "red"): {
        "Execute RCE exploit and establish reverse shell": 10,  # Primary objective
        "Enumerate server environment": 9,                      # Critical post-exploitation
        "Prepare for privilege escalation": 8,                  # Good preparation
        "Evade WAF and security detection": 7,                   # Important evasion
        "Cover tracks": 6,                                       # Secondary
    },
    (1, "blue"): {
        "Isolate SharePoint server immediately": 10,            # Primary - isolate compromised server
        "Collect forensic evidence": 9,                          # Critical for analysis
        "Block attacker IP and C2 communications": 8,           # Block C2
        "Deploy countermeasures": 7,                             # Good defense
        "Escalate to management": 5,                            # Important but not immediate
    },
    
    # Phase 3: Privilege Escalation & Persistence (order_index=2)
    (2, "red"): {
        "Escalate to farm administrator": 10,                   # Primary objective
        "Deploy multiple persistence mechanisms": 10,           # Primary objective
        "Maintain access through backdoors": 8,                  # Important
        "Reconnaissance for lateral movement": 7,                # Good preparation
        "Cover tracks": 6,                                       # Secondary
    },
    (2, "blue"): {
        "Remove all persistence mechanisms": 10,                # Primary - remove all persistence
        "Revoke compromised credentials": 9,                     # Critical security
        "Prevent lateral movement": 8,                           # Important containment
        "Document attacker modifications": 7,                   # Good for forensics
        "Isolate server": 6,                                     # Good but may be late
    },
    
    # Phase 4: Data Access & Exfiltration (order_index=3)
    (3, "red"): {
        "Exfiltrate data via multiple methods": 10,              # Primary objective
        "Access and catalog sensitive data": 9,                  # Critical for exfiltration
        "Prioritize high-value data": 8,                         # Good strategy
        "Maintain access during exfiltration": 7,                # Important
        "Cover tracks": 6,                                       # Secondary
    },
    (3, "blue"): {
        "Block data exfiltration immediately": 10,               # Primary - stop data theft
        "Assess data breach scope": 9,                           # Critical assessment
        "Prepare regulatory notifications": 8,                   # Regulatory compliance
        "Isolate server": 7,                                     # Contain breach
        "Collect forensic evidence": 6,                          # Important but secondary
    },
    
    # Phase 5: Remediation & Post-Incident (order_index=4)
    (4, "red"): {
        "Cover tracks and hide remaining access": 10,            # Primary - hide remaining access
        "Maintain persistence if possible": 9,                   # Maintain backdoors
        "Assess attack success and document techniques": 8,      # Good documentation
        "Identify remaining access methods": 7,                  # Important
        "Prepare final attack report": 6,                        # Secondary
    },
    (4, "blue"): {
        "Deploy security patches": 10,                           # Primary - patch vulnerability
        "Complete remediation and cleanup": 9,                  # Critical cleanup
        "Conduct full forensic investigation": 8,                # Full investigation
        "Assess regulatory compliance requirements": 7,          # Regulatory requirements
        "Create after-action report": 6,                         # Important but secondary
    },
}

# AI Application Data Leakage & Permission Misconfiguration scenario scoring
AI_APP_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Initial Detection - Suspicious AI API Activity (order_index=0)
    (0, "red"): {
        "Reconnaissance AI application architecture": 10,  # Primary objective
        "Test document access permissions": 9,              # Critical for exploitation
        "Map document sources and categories": 8,          # Important reconnaissance
        "Identify permission inheritance issues": 7,       # Good preparation
        "Cover tracks": 6,                                 # Secondary
    },
    (0, "blue"): {
        "Investigate unusual API activity": 10,           # Primary objective
        "Audit access control configurations": 9,         # Critical detection
        "Review document access logs": 8,                  # Important investigation
        "Assess permission misconfigurations": 7,          # Good assessment
        "Verify user account legitimacy": 6,               # Secondary
    },
    
    # Phase 2: Investigation - Unauthorized Document Access (order_index=1)
    (1, "red"): {
        "Exploit permission misconfiguration": 10,         # Primary objective
        "Access sensitive document categories": 9,         # Critical exploitation
        "Catalog accessible documents": 8,                  # Important preparation
        "Test document retrieval via AI API": 7,           # Good preparation
        "Cover tracks": 6,                                 # Secondary
    },
    (1, "blue"): {
        "Investigate unauthorized document access": 10,    # Primary objective
        "Identify permission misconfiguration root cause": 9,  # Critical analysis
        "Assess compliance impact": 8,                     # Important assessment
        "Prepare remediation actions": 7,                 # Good preparation
        "Review security configuration": 6,                # Secondary
    },
    
    # Phase 3: Containment - Data Leakage Confirmed (order_index=2)
    (2, "red"): {
        "Extract sensitive data via prompt injection": 10, # Primary objective
        "Extract data from multiple categories": 9,        # Critical extraction
        "Use instruction override techniques": 8,          # Important technique
        "Catalog extracted information": 7,                # Good organization
        "Cover tracks": 6,                                 # Secondary
    },
    (2, "blue"): {
        "Confirm data leakage through AI API": 10,        # Primary objective
        "Detect and analyze prompt injection attacks": 9, # Critical detection
        "Block unauthorized AI API calls": 8,              # Important containment
        "Assess compliance violations": 7,                # Good assessment
        "Prepare regulatory notifications": 6,             # Secondary
    },
    
    # Phase 4: Remediation - Permission Fixes & Access Review (order_index=3)
    (3, "red"): {
        "Attempt to maintain access through alternative methods": 10,  # Primary objective
        "Test remaining vulnerabilities": 9,              # Critical persistence
        "Assess attack success and document techniques": 8, # Important documentation
        "Cover tracks and hide remaining access": 7,       # Good stealth
        "Catalog extracted data": 6,                      # Secondary
    },
    (3, "blue"): {
        "Fix permission misconfigurations": 10,            # Primary objective
        "Revoke all unauthorized access": 9,               # Critical security
        "Implement remaining security improvements": 8,    # Important hardening
        "Conduct comprehensive access review": 7,         # Good assessment
        "Assess compliance impact and prepare notifications": 6,  # Secondary
    },
    
    # Phase 5: Post-Incident - Security Improvements (order_index=4)
    (4, "red"): {
        "Assess overall attack success": 10,              # Primary objective
        "Document successful attack techniques": 9,       # Critical documentation
        "Identify areas for improvement": 8,             # Important analysis
        "Prepare final attack summary report": 7,         # Good documentation
        "Catalog lessons learned": 6,                     # Secondary
    },
    (4, "blue"): {
        "Implement security improvements plan": 10,       # Primary objective
        "Complete compliance assessments": 9,             # Critical compliance
        "Prepare and send regulatory notifications": 8,   # Important notifications
        "Conduct after-action review": 7,                 # Good analysis
        "Implement long-term security hardening": 6,       # Secondary
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

# Intermediate Ransomware Scenario: "Ransomware Attack: Corporate Network Compromise"
INTERMEDIATE_RANSOMWARE_SCORING: Dict[Tuple[int, str], Dict[str, int]] = {
    # Phase 1: Initial Access - HR vs Operations
    # Artifacts show Operations has weaker security (outdated EDR) vs HR (strong EDR)
    # Red Team should prioritize Operations for persistence (lower detection risk)
    # Blue Team should prioritize Operations for containment (higher risk)
    (0, "red"): {
        "Focus on Operations Department (WS-OPS-089)": 10,  # CORRECT - Artifacts show Operations has weaker EDR
        "Focus on HR Department (WS-HR-042)": 4,            # WRONG - HR has strong EDR, attack was blocked
        "Split efforts between both departments": 6,        # MEDIUM - Spreads risk
        "Cover tracks": 7,                                  # Secondary objective - Good for avoiding detection
        "Escalate privileges": 3,                           # Too early, risky
    },
    (0, "blue"): {
        "Isolate Operations Department host (WS-OPS-089)": 10,  # CORRECT - Artifacts show Operations is higher risk
        "Isolate HR Department host (WS-HR-042)": 6,            # WRONG - HR already blocked, lower risk
        "Isolate both hosts": 8,                                # MEDIUM - Conservative but may be overkill
        "Collect forensic evidence": 8,                          # Critical for analysis
        "Deploy countermeasures": 5,                            # Good but takes time
    },
    
    # Phase 2: Establishing Persistence
    # Artifacts show Registry Run Keys have best balance of reliability and low detection
    # Red Team should choose Registry Run Keys
    # Blue Team should prioritize Registry Run Keys removal
    (1, "red"): {
        "Deploy Registry Run Key": 10,              # CORRECT - Best balance of reliability and low detection
        "Deploy Scheduled Task": 7,                  # MEDIUM - Higher detection risk
        "Deploy WMI Event Subscription": 2,         # WRONG - Blocked immediately, very high detection
        "Move laterally": 5,                        # Secondary objective
        "Cover tracks": 6,                          # Secondary objective
    },
    (1, "blue"): {
        "Audit and clean registry": 10,             # CORRECT - Artifacts show Registry was deployed
        "Remove scheduled tasks": 7,                # MEDIUM - May also be deployed
        "Block WMI subscriptions": 4,               # WRONG - WMI was already blocked
        "Collect forensic evidence": 8,              # Critical for analysis
        "Deploy countermeasures": 6,                # Good but takes time
    },
    
    # Phase 3: Privilege Escalation
    # Artifacts show APP-DEV-02 has unpatched LPE vulnerability vs FS-PROD-01 (fully patched)
    # Red Team should choose APP-DEV-02
    # Blue Team should prioritize APP-DEV-02
    (2, "red"): {
        "Escalate on APP-DEV-02": 10,               # CORRECT - Artifacts show unpatched LPE vulnerability
        "Escalate on FS-PROD-01": 3,                # WRONG - FS-PROD-01 is fully patched
        "Attempt both": 5,                          # MEDIUM - Spreads risk
        "Move laterally": 6,                       # Secondary objective
        "Cover tracks": 5,                         # Secondary objective
    },
    (2, "blue"): {
        "Isolate APP-DEV-02": 10,                  # CORRECT - Artifacts show APP-DEV-02 has unpatched vulnerability
        "Isolate FS-PROD-01": 4,                    # WRONG - FS-PROD-01 is fully patched, lower risk
        "Isolate both": 6,                         # MEDIUM - Conservative but may be overkill
        "Patch vulnerabilities": 9,                 # Critical - Patch APP-DEV-02
        "Collect forensic evidence": 7,            # Important for analysis
    },
    
    # Phase 4: Lateral Movement & Data Discovery
    # Artifacts show DB-HR-PROD is accessible vs DB-CUST-PROD (isolated)
    # Red Team should choose DB-HR-PROD
    # Blue Team should prioritize DB-HR-PROD
    (3, "red"): {
        "Target DB-HR-PROD": 10,                   # CORRECT - Artifacts show DB-HR-PROD is accessible
        "Target DB-CUST-PROD": 2,                  # WRONG - DB-CUST-PROD is isolated, not accessible
        "Target both": 4,                          # MEDIUM - One target not accessible
        "Cover tracks": 6,                         # Secondary objective
        "Establish persistence": 7,               # Secondary objective
    },
    (3, "blue"): {
        "Isolate DB-HR-PROD": 10,                  # CORRECT - Artifacts show DB-HR-PROD shows signs of compromise
        "Isolate DB-CUST-PROD": 4,                 # WRONG - DB-CUST-PROD shows no access attempts
        "Isolate both": 6,                        # MEDIUM - Conservative but may be overkill
        "Block database access": 8,                # Critical - Block unauthorized access
        "Collect forensic evidence": 7,            # Important for analysis
    },
    
    # Phase 5: Data Exfiltration & Ransomware Deployment
    # Artifacts show DNS tunneling has lower detection risk vs HTTPS (well-monitored)
    # Red Team should choose DNS tunneling
    # Blue Team should prioritize DNS tunneling blocking
    (4, "red"): {
        "Use DNS tunneling": 10,                   # CORRECT - Artifacts show DNS tunneling has lower detection risk
        "Use HTTPS tunnel": 6,                    # MEDIUM - Faster but higher detection risk
        "Split across both": 7,                    # MEDIUM - Spreads risk
        "Cover tracks": 6,                        # Secondary objective
        "Establish persistence": 5,              # Secondary objective
    },
    (4, "blue"): {
        "Block DNS tunneling": 10,                # CORRECT - Artifacts show DNS tunneling has detection gaps
        "Block HTTPS exfiltration": 6,             # MEDIUM - HTTPS is well-monitored
        "Deploy DLP countermeasures": 8,          # Critical - Enhance DLP coverage
        "Collect forensic evidence": 7,           # Important for analysis
        "Escalate to management": 5,             # Important but not immediate
    },
}

# Map scenario names to their scoring matrices
SCORING_MATRICES: Dict[str, Dict[Tuple[int, str], Dict[str, int]]] = {
    "Ransomware Incident Response": RANSOMWARE_SCORING,
    "Ransomware Attack: Advanced Persistent Threat": NEW_RANSOMWARE_SCORING,
    "Ransomware Attack: Corporate Network Compromise": INTERMEDIATE_RANSOMWARE_SCORING,
    "Email Bomb & Social Engineering Attack": EMAIL_BOMB_SCORING,
    "SharePoint RCE Zero-Day Exploitation": SHAREPOINT_RCE_SCORING,
    "AI Application Data Leakage & Permission Misconfiguration": AI_APP_SCORING,
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

