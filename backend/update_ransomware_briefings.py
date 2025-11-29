"""
Update briefing texts for the new Ransomware scenario to be neutral.
This script updates existing scenarios instead of creating new ones.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase

db: Session = SessionLocal()

try:
    scenario_name = "Ransomware Attack: Advanced Persistent Threat"
    scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if not scenario:
        print(f"Scenario '{scenario_name}' not found!")
        print("Run create_new_ransomware_scenario.py first to create it.")
        sys.exit(1)
    
    print(f"Found scenario: {scenario.name} (ID: {scenario.id})")
    
    # Get all phases
    phases = db.query(ScenarioPhase).filter(ScenarioPhase.scenario_id == scenario.id).order_by(ScenarioPhase.order_index).all()
    
    if not phases:
        print("No phases found for this scenario!")
        sys.exit(1)
    
    # Updated briefing texts (neutral)
    updated_briefings = {
        0: "At 09:20 AM, a phishing campaign has successfully delivered emails to two departments:\n- IT Department (WS-IT-089): 8 emails opened, 2 links clicked\n- Sales Department (WS-SLS-203): 15 emails opened, 5 links clicked\n\nBoth departments have users who clicked the malicious links. Initial access attempts have been detected on workstations in both departments:\n- **WS-IT-089** (IT): it.admin@corp.local clicked malicious link\n- **WS-SLS-203** (Sales): sales.rep@corp.local clicked malicious link\n\nSecurity monitoring has detected suspicious activity from both workstations. The security team needs to determine which department presents the highest risk and requires immediate containment.\n\nInitial reconnaissance data has been collected on both targets (WS-IT-089 and WS-SLS-203). Your decision: **Which department should you prioritize for investigation and containment?**\n\n**Remember:** Review the artifacts carefully. They contain critical information about security posture, EDR coverage, and user privileges for **both WS-IT-089 and WS-SLS-203** that will help determine the appropriate response. The artifacts will reveal which target has weaker security controls and presents the greater risk.",
        1: "Initial access has been established on the target workstation. Security monitoring has detected attempts to create persistence mechanisms to maintain access even if the initial entry point is discovered.\n\nSecurity analysis has identified three different persistence methods being tested, with data collected on their detection and blocking capabilities. Your decision: **Which persistence mechanism should be prioritized for removal and investigation?**\n\n**Remember:** Review the artifacts carefully. They contain information about detection rates, blocking capabilities, and visibility for each persistence method.",
        2: "Persistence has been established on the initial workstation with standard user privileges. Security monitoring indicates attempts to escalate privileges to access sensitive data and systems.\n\nTwo potential targets for privilege escalation have been identified:\n- **File Server FS-01**: Appears to be fully patched\n- **Application Server APP-02**: Appears to have unpatched vulnerabilities\n\nVulnerability scan results and reconnaissance data have been collected on both targets. Your decision: **Which server should be prioritized for containment and patching?**\n\n**Remember:** Review the artifacts carefully. They contain vulnerability information, patch status, and exploit availability for **both FS-01 and APP-02** that will help determine the appropriate response.",
        3: "Privilege escalation has been successful, and access to multiple servers has been detected. Two database servers containing valuable data have been identified:\n- **DB-CUST-01** (Customer Database): Contains customer PII and records\n- **DB-FIN-02** (Financial Records): Contains financial data and records\n\nNetwork mapping and access tests have been detected on both targets. Your decision: **Which database server should be prioritized for protection and access restriction?**\n\n**Remember:** Review the artifacts carefully. They contain network topology information, access logs, and security controls for **both DB-CUST-01 and DB-FIN-02** that will help determine the appropriate response.",
        4: "Access to valuable data from the target database has been detected. Security monitoring indicates attempts to exfiltrate this data, with two exfiltration methods being tested. Data Loss Prevention (DLP) systems have collected information on their detection capabilities.\n\nYour decision: **Which exfiltration method should be prioritized for blocking and investigation?**\n\n- Option A: Encrypted HTTPS tunnel (slower but may be less detectable)\n- Option B: DNS tunneling (faster but may be more detectable)\n- Option C: Both methods being used simultaneously\n\n**Remember:** Review the artifacts carefully. They contain DLP alert analysis, network bandwidth data, and detection test results that will help determine which method presents the greater threat and requires immediate blocking."
    }
    
    # Update each phase
    for phase in phases:
        if phase.order_index in updated_briefings:
            old_briefing = phase.briefing_text
            phase.briefing_text = updated_briefings[phase.order_index]
            print(f"✓ Updated Phase {phase.order_index + 1}: {phase.name}")
            if old_briefing != updated_briefings[phase.order_index]:
                print(f"  (Briefing text changed)")
            else:
                print(f"  (Briefing text was already updated)")
        else:
            print(f"⚠ Skipped Phase {phase.order_index + 1}: {phase.name} (no update defined)")
    
    db.commit()
    print("\n" + "=" * 60)
    print("✓ Successfully updated briefing texts!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)
finally:
    db.close()

