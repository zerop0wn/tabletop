"""
Script to update existing scenario phases with phase-specific actions.
This updates the Ransomware Incident Response scenario phases.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase

db: Session = SessionLocal()

try:
    # Find the Ransomware scenario
    scenario = db.query(Scenario).filter(Scenario.name == "Ransomware Incident Response").first()
    
    if not scenario:
        print("Ransomware scenario not found!")
        sys.exit(1)
    
    print(f"Found scenario: {scenario.name} (ID: {scenario.id})")
    
    # Phase 1 actions
    phase1_actions = {
        "red": [
            {
                "name": "Focus on Finance Department (WS-FIN-042)",
                "description": "Prioritize establishing persistence on the Finance department workstation. Review artifacts to assess security posture and detection risk."
            },
            {
                "name": "Focus on Marketing Department (WS-MKT-015)",
                "description": "Prioritize establishing persistence on the Marketing department workstation. Review artifacts to assess security posture and detection risk."
            },
            {
                "name": "Split efforts between both departments",
                "description": "Attempt to establish persistence on both Finance and Marketing workstations simultaneously. Higher chance of success but also higher detection risk."
            },
            {
                "name": "Cover tracks",
                "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
            },
            {
                "name": "Escalate privileges",
                "description": "Gain administrator or root-level access through privilege escalation exploits. Unlocks more system capabilities but increases detection risk."
            }
        ],
        "blue": [
            {
                "name": "Isolate Finance Department host (WS-FIN-042)",
                "description": "Disconnect the Finance department workstation from the network to prevent further spread. Review artifacts to assess risk level."
            },
            {
                "name": "Isolate Marketing Department host (WS-MKT-015)",
                "description": "Disconnect the Marketing department workstation from the network to prevent further spread. Review artifacts to assess risk level."
            },
            {
                "name": "Isolate both hosts",
                "description": "Disconnect both Finance and Marketing workstations from the network. Conservative approach but may impact business operations."
            },
            {
                "name": "Collect forensic evidence",
                "description": "Gather logs, memory dumps, and system artifacts for analysis. Critical for understanding the attack but takes time and may not stop immediate threats."
            },
            {
                "name": "Deploy countermeasures",
                "description": "Implement security controls like patches, endpoint protection, or network segmentation. Proactive defense but may impact system availability."
            }
        ]
    }
    
    # Phase 3 actions
    phase3_actions = {
        "red": [
            {
                "name": "Escalate privileges on WS-FIN-01 (Finance)",
                "description": "Attempt privilege escalation on WS-FIN-01 using generic token-stealing and UAC bypass techniques. Review artifacts to assess success probability."
            },
            {
                "name": "Escalate privileges on WS-MKT-02 (Marketing)",
                "description": "Attempt privilege escalation on WS-MKT-02 using the specific local privilege escalation exploit identified in vulnerability scans. Review artifacts to assess success probability."
            },
            {
                "name": "Split efforts - escalate on both hosts",
                "description": "Run automated privilege escalation tooling on both WS-FIN-01 and WS-MKT-02 in parallel. Higher chance of success but also higher detection risk."
            },
            {
                "name": "Move laterally",
                "description": "Spread from the initial compromised system to other systems on the network. Expands attack surface but creates more forensic evidence."
            },
            {
                "name": "Cover tracks",
                "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
            }
        ],
        "blue": [
            {
                "name": "Isolate WS-FIN-01 (Finance host)",
                "description": "Disconnect WS-FIN-01 from the network to prevent privilege escalation. Review artifacts to assess risk level."
            },
            {
                "name": "Isolate WS-MKT-02 (Marketing host)",
                "description": "Disconnect WS-MKT-02 from the network to prevent privilege escalation. Review artifacts to assess risk level."
            },
            {
                "name": "Isolate both hosts",
                "description": "Disconnect both WS-FIN-01 and WS-MKT-02 from the network. Conservative approach but may impact business operations."
            },
            {
                "name": "Deploy countermeasures",
                "description": "Implement security controls like patches, network segmentation, or enhanced monitoring. Proactive defense but may impact system availability."
            },
            {
                "name": "Collect forensic evidence",
                "description": "Gather logs, memory dumps, and system artifacts for analysis. Critical for understanding the attack but takes time and may not stop immediate threats."
            }
        ]
    }
    
    # Phase 4 actions
    phase4_actions = {
        "red": [
            {
                "name": "Exfiltrate data from FS-01 (Finance)",
                "description": "Prioritize exfiltration from FS-01 containing financial records, customer PII, and proprietary research data. Review artifacts to assess detection risk."
            },
            {
                "name": "Exfiltrate data from FS-02 (HR/Operations)",
                "description": "Prioritize exfiltration from FS-02 containing employee records, HR data, and operational documents. Review artifacts to assess detection risk."
            },
            {
                "name": "Exfiltrate from both servers simultaneously",
                "description": "Exfiltrate data from both FS-01 and FS-02 using parallel streams. Maximizes data value but also increases detection risk."
            },
            {
                "name": "Cover tracks",
                "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
            },
            {
                "name": "Establish persistence",
                "description": "Create backdoors, scheduled tasks, or service accounts to maintain access even if initial entry point is discovered. High risk if detected."
            }
        ],
        "blue": [
            {
                "name": "Block exfiltration from FS-01 (Finance)",
                "description": "Block external data transfers and isolate FS-01 to prevent data exfiltration. Review artifacts to assess priority."
            },
            {
                "name": "Block exfiltration from FS-02 (HR/Operations)",
                "description": "Block external data transfers and isolate FS-02 to prevent data exfiltration. Review artifacts to assess priority."
            },
            {
                "name": "Block exfiltration from both servers",
                "description": "Block external data transfers and isolate both FS-01 and FS-02. Conservative approach but may impact business operations."
            },
            {
                "name": "Collect forensic evidence",
                "description": "Gather logs, network flow data, and access logs for analysis. Critical for understanding what data was stolen but takes time."
            },
            {
                "name": "Escalate to management",
                "description": "Notify leadership and activate incident response procedures. Ensures proper coordination but may slow immediate response actions."
            }
        ]
    }
    
    # Update phases
    phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).order_by(ScenarioPhase.order_index).all()
    
    for phase in phases:
        if phase.order_index == 0:  # Phase 1
            phase.available_actions = phase1_actions
            print(f"Updated Phase 1: {phase.name}")
        elif phase.order_index == 2:  # Phase 3
            phase.available_actions = phase3_actions
            print(f"Updated Phase 3: {phase.name}")
        elif phase.order_index == 3:  # Phase 4
            phase.available_actions = phase4_actions
            print(f"Updated Phase 4: {phase.name}")
        else:
            print(f"Skipped Phase {phase.order_index + 1}: {phase.name} (no phase-specific actions)")
    
    db.commit()
    print("\n✓ Successfully updated phase actions!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)
finally:
    db.close()

