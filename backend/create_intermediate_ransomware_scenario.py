"""
Create an intermediate-level Ransomware scenario: "Ransomware Attack: Corporate Network Compromise"
This script creates a fresh scenario with 5 phases, detailed artifacts, and phase-specific actions.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact, ArtifactType
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

# Get the scenario_phase_artifacts association table
from app.models import scenario_phase_artifacts

db: Session = SessionLocal()

try:
    # Check if scenario already exists
    scenario_name = "Ransomware Attack: Corporate Network Compromise"
    existing_scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if existing_scenario:
        print(f"Scenario '{scenario_name}' already exists (ID: {existing_scenario.id})")
        print("Delete it first if you want to recreate it.")
        sys.exit(0)
    
    print(f"Creating new scenario: {scenario_name}")
    
    # Create scenario
    scenario = Scenario(
        name=scenario_name,
        description="A sophisticated ransomware attack targeting a mid-size corporation. The attack begins with a spear-phishing campaign targeting multiple departments. The attacker's goal is to establish persistence, escalate privileges, access sensitive data, and deploy ransomware across critical systems. The Blue Team must detect, contain, and remediate the attack while minimizing business disruption.\n\nKey Attack Vectors:\n- Initial Access: Spear-phishing emails with malicious attachments\n- Persistence: Multiple mechanisms tested (scheduled tasks, registry, services)\n- Privilege Escalation: Exploiting unpatched vulnerabilities on internal servers\n- Lateral Movement: Targeting file servers and database systems\n- Data Exfiltration: Stealing data before ransomware deployment\n- Ransomware Deployment: Encrypting critical systems\n\nThe scenario tests both teams' ability to analyze security artifacts, make time-sensitive decisions, and respond to an evolving threat. Each phase presents multiple viable options, but only careful artifact analysis reveals the optimal choice.",
        miro_board_url="https://miro.com/app/board/example"
    )
    db.add(scenario)
    db.flush()
    print(f"✓ Created scenario (ID: {scenario.id})")
    
    # Phase 1: Initial Access - HR vs Operations Department
    phase1 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=0,
        name="Phase 1: Initial Access - Spear-Phishing Campaign",
        briefing_text="At 08:45 AM, a spear-phishing campaign has successfully delivered emails to two departments:\n- HR Department (WS-HR-042): 12 emails opened, 4 links clicked\n- Operations Department (WS-OPS-089): 18 emails opened, 7 links clicked\n\nBoth departments have users who clicked the malicious links. Initial access attempts have been detected on workstations in both departments:\n- **WS-HR-042** (HR): hr.manager@corp.local clicked malicious link\n- **WS-OPS-089** (Operations): ops.coord@corp.local clicked malicious link\n\nSecurity monitoring has detected suspicious activity from both workstations. The security team needs to determine which department presents the highest risk and requires immediate containment.\n\nInitial reconnaissance data has been collected on both targets (WS-HR-042 and WS-OPS-089). Your decision: **Which department should you prioritize for investigation and containment?**\n\n**Remember:** Review the artifacts carefully. They contain critical information about security posture, EDR coverage, and user privileges for **both WS-HR-042 and WS-OPS-089** that will help determine the appropriate response. The artifacts will reveal which target has weaker security controls and presents the greater risk.",
        red_objective="Analyze the reconnaissance data from both departments to identify which target offers the best opportunity for establishing persistent access with minimal detection risk. Focus your initial persistence efforts on the most vulnerable target.",
        blue_objective="Review security telemetry from both departments to identify which department shows the most concerning indicators of compromise. Prioritize containment and investigation efforts on the department with the highest risk of successful attacker persistence.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame1",
        available_actions={
            "red": [
                {
                    "name": "Focus on HR Department (WS-HR-042)",
                    "description": "Prioritize establishing persistence on WS-HR-042 (HR). Review artifacts comparing WS-HR-042 and WS-OPS-089 to assess security posture and detection risk."
                },
                {
                    "name": "Focus on Operations Department (WS-OPS-089)",
                    "description": "Prioritize establishing persistence on WS-OPS-089 (Operations). Review artifacts comparing WS-HR-042 and WS-OPS-089 to assess security posture and detection risk."
                },
                {
                    "name": "Split efforts between both departments",
                    "description": "Attempt to establish persistence on both HR and Operations workstations simultaneously. Higher chance of success but also higher detection risk."
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
                    "name": "Isolate HR Department host (WS-HR-042)",
                    "description": "Disconnect WS-HR-042 (HR) from the network to prevent further spread. Review artifacts comparing WS-HR-042 and WS-OPS-089 to assess risk level."
                },
                {
                    "name": "Isolate Operations Department host (WS-OPS-089)",
                    "description": "Disconnect WS-OPS-089 (Operations) from the network to prevent further spread. Review artifacts comparing WS-HR-042 and WS-OPS-089 to assess risk level."
                },
                {
                    "name": "Isolate both hosts",
                    "description": "Disconnect both HR and Operations workstations from the network. Conservative approach but may impact business operations."
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
    )
    db.add(phase1)
    db.flush()
    print(f"✓ Created Phase 1 (ID: {phase1.id})")
    
    # Phase 2: Establishing Persistence
    phase2 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=1,
        name="Phase 2: Establishing Persistence",
        briefing_text="Initial access has been established on the target workstation. Security monitoring has detected multiple attempts to create persistence mechanisms on the compromised system.\n\nThree different persistence methods are being tested:\n- **Scheduled Tasks**: Creating scheduled tasks to run malicious code at system startup\n- **Registry Run Keys**: Modifying Windows Registry to execute code on login\n- **WMI Event Subscriptions**: Using Windows Management Instrumentation to trigger code execution\n\nSecurity systems have detected activity related to all three methods, but the attacker appears to be testing which method provides the best balance of reliability and stealth.\n\nYour decision: **Which persistence mechanism should be prioritized for removal/investigation?**\n\n**Remember:** Review the artifacts carefully. They contain information about detection capabilities, system logs, and security tool responses for each persistence method. The artifacts will reveal which method was successfully deployed and which presents the highest ongoing risk.",
        red_objective="Select the persistence method that offers the best balance of reliability, low visibility, and low detection risk. Your goal is to maintain access even if the initial compromise is discovered.",
        blue_objective="Identify which persistence mechanism was successfully deployed and prioritize its removal. Your goal is to prevent the attacker from maintaining access if the initial compromise is contained.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame2",
        available_actions={
            "red": [
                {
                    "name": "Deploy Scheduled Task",
                    "description": "Create a scheduled task that runs malicious code at system startup or on a schedule. Review artifacts to assess detection risk and reliability."
                },
                {
                    "name": "Deploy Registry Run Key",
                    "description": "Modify Windows Registry Run keys to execute code automatically on user login. Review artifacts to assess detection risk and reliability."
                },
                {
                    "name": "Deploy WMI Event Subscription",
                    "description": "Create a WMI event subscription that triggers code execution on specific system events. Review artifacts to assess detection risk and reliability."
                },
                {
                    "name": "Move laterally",
                    "description": "Attempt to move to other systems on the network before establishing persistence. Higher risk but may provide better access."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                }
            ],
            "blue": [
                {
                    "name": "Remove scheduled tasks",
                    "description": "Audit and remove suspicious scheduled tasks. Review artifacts to determine if this persistence method was deployed."
                },
                {
                    "name": "Audit and clean registry",
                    "description": "Review Windows Registry Run keys and remove suspicious entries. Review artifacts to determine if this persistence method was deployed."
                },
                {
                    "name": "Block WMI subscriptions",
                    "description": "Audit and remove WMI event subscriptions. Review artifacts to determine if this persistence method was deployed."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, memory dumps, and system artifacts for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Deploy countermeasures",
                    "description": "Implement security controls to prevent persistence mechanisms. Proactive defense but may impact system availability."
                }
            ]
        }
    )
    db.add(phase2)
    db.flush()
    print(f"✓ Created Phase 2 (ID: {phase2.id})")
    
    # Phase 3: Privilege Escalation
    phase3 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=2,
        name="Phase 3: Privilege Escalation",
        briefing_text="Persistence has been established with standard user privileges. Security monitoring indicates that the attacker is attempting to escalate privileges to gain administrative access.\n\nTwo potential targets have been identified for privilege escalation:\n- **File Server FS-PROD-01**: Production file server hosting shared documents and user data\n- **Application Server APP-DEV-02**: Development application server running internal web applications\n\nBoth servers have been scanned for vulnerabilities, and security monitoring has detected reconnaissance activity targeting both systems.\n\nYour decision: **Which server should be prioritized for containment/patching?**\n\n**Remember:** Review the artifacts carefully. They contain vulnerability scan results, patch status, and security monitoring data for both servers. The artifacts will reveal which server has exploitable vulnerabilities and which presents the highest risk for successful privilege escalation.",
        red_objective="Analyze vulnerability data to identify the target server with the best opportunity for privilege escalation. Your goal is to gain administrative access with minimal detection risk.",
        blue_objective="Review vulnerability scans and security monitoring to identify which server is at highest risk for successful privilege escalation. Your goal is to prevent the attacker from gaining administrative access.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame3",
        available_actions={
            "red": [
                {
                    "name": "Escalate on FS-PROD-01",
                    "description": "Attempt privilege escalation on File Server FS-PROD-01. Review artifacts to assess vulnerability status and detection risk."
                },
                {
                    "name": "Escalate on APP-DEV-02",
                    "description": "Attempt privilege escalation on Application Server APP-DEV-02. Review artifacts to assess vulnerability status and detection risk."
                },
                {
                    "name": "Attempt both",
                    "description": "Attempt privilege escalation on both servers simultaneously. Higher chance of success but also higher detection risk."
                },
                {
                    "name": "Move laterally",
                    "description": "Attempt to move to other systems on the network before escalating privileges. May provide better access opportunities."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                }
            ],
            "blue": [
                {
                    "name": "Isolate FS-PROD-01",
                    "description": "Disconnect File Server FS-PROD-01 from the network to prevent privilege escalation. Review artifacts to assess risk level."
                },
                {
                    "name": "Isolate APP-DEV-02",
                    "description": "Disconnect Application Server APP-DEV-02 from the network to prevent privilege escalation. Review artifacts to assess risk level."
                },
                {
                    "name": "Isolate both",
                    "description": "Disconnect both servers from the network. Conservative approach but may impact business operations."
                },
                {
                    "name": "Patch vulnerabilities",
                    "description": "Apply security patches to address known vulnerabilities. Critical defense but may require system downtime."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, memory dumps, and system artifacts for analysis. Critical for understanding the attack but takes time."
                }
            ]
        }
    )
    db.add(phase3)
    db.flush()
    print(f"✓ Created Phase 3 (ID: {phase3.id})")
    
    # Phase 4: Lateral Movement & Data Discovery
    phase4 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=3,
        name="Phase 4: Lateral Movement & Data Discovery",
        briefing_text="Privilege escalation has been successful, and the attacker now has administrative access to internal servers. Security monitoring has detected network mapping and access attempts targeting multiple data repositories.\n\nTwo critical databases have been identified as potential targets:\n- **Customer Database (DB-CUST-PROD)**: Production database containing customer information, payment data, and business records\n- **Employee Records Database (DB-HR-PROD)**: Production database containing employee personal information, payroll data, and HR records\n\nNetwork traffic analysis shows reconnaissance activity and connection attempts to both databases. Access logs indicate queries being executed against database systems.\n\nYour decision: **Which database should be prioritized for protection/access restriction?**\n\n**Remember:** Review the artifacts carefully. They contain network traffic analysis, database access logs, and network segmentation information for both databases. The artifacts will reveal which database is accessible, which shows signs of compromise, and which presents the highest ongoing risk.",
        red_objective="Analyze network mapping and access test results to identify the database with the best access opportunity and highest data value. Your goal is to access sensitive data for exfiltration.",
        blue_objective="Review access logs and network segmentation to identify which database shows signs of potential compromise. Your goal is to prevent unauthorized data access.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame4",
        available_actions={
            "red": [
                {
                    "name": "Target DB-CUST-PROD",
                    "description": "Focus on accessing the Customer Database (DB-CUST-PROD). Review artifacts to assess network access and connection success."
                },
                {
                    "name": "Target DB-HR-PROD",
                    "description": "Focus on accessing the Employee Records Database (DB-HR-PROD). Review artifacts to assess network access and connection success."
                },
                {
                    "name": "Target both",
                    "description": "Attempt to access both databases simultaneously. Higher chance of success but also higher detection risk."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Establish persistence",
                    "description": "Create additional persistence mechanisms on database servers. Ensures continued access even if initial compromise is discovered."
                }
            ],
            "blue": [
                {
                    "name": "Isolate DB-CUST-PROD",
                    "description": "Disconnect Customer Database (DB-CUST-PROD) from the network to prevent unauthorized access. Review artifacts to assess risk level."
                },
                {
                    "name": "Isolate DB-HR-PROD",
                    "description": "Disconnect Employee Records Database (DB-HR-PROD) from the network to prevent unauthorized access. Review artifacts to assess risk level."
                },
                {
                    "name": "Isolate both",
                    "description": "Disconnect both databases from the network. Conservative approach but may impact business operations."
                },
                {
                    "name": "Block database access",
                    "description": "Implement network access controls to restrict database connections. Prevents unauthorized access but may impact legitimate users."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, network traffic captures, and system artifacts for analysis. Critical for understanding the attack but takes time."
                }
            ]
        }
    )
    db.add(phase4)
    db.flush()
    print(f"✓ Created Phase 4 (ID: {phase4.id})")
    
    # Phase 5: Data Exfiltration & Ransomware Deployment
    phase5 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=4,
        name="Phase 5: Data Exfiltration & Ransomware Deployment",
        briefing_text="Access to valuable data has been confirmed from the target database. Security monitoring indicates that the attacker is attempting to exfiltrate data using multiple methods.\n\nTwo exfiltration methods are being tested:\n- **HTTPS Tunnel**: Encrypted HTTPS connections to external servers, blending with normal web traffic\n- **DNS Tunneling**: Covert data exfiltration using DNS queries, hiding data in DNS request payloads\n\nData Loss Prevention (DLP) systems have detected anomalies in network traffic patterns, and security monitoring has collected information about detection capabilities for both methods.\n\nYour decision: **Which exfiltration method should be prioritized for blocking?**\n\n**Remember:** Review the artifacts carefully. They contain DLP alert analysis, network bandwidth monitoring, and detection capability assessments for both exfiltration methods. The artifacts will reveal which method is being actively used, which has better detection coverage, and which presents the highest ongoing risk.",
        red_objective="Select the exfiltration method that offers the best balance of speed, reliability, and low detection risk. Your goal is to successfully exfiltrate data before deploying ransomware.",
        blue_objective="Identify which exfiltration method is being actively used and prioritize blocking it. Your goal is to prevent data theft and prepare for ransomware deployment.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame5",
        available_actions={
            "red": [
                {
                    "name": "Use HTTPS tunnel",
                    "description": "Exfiltrate data using encrypted HTTPS connections. Review artifacts to assess detection risk and transfer speed."
                },
                {
                    "name": "Use DNS tunneling",
                    "description": "Exfiltrate data using DNS queries with encoded payloads. Review artifacts to assess detection risk and transfer speed."
                },
                {
                    "name": "Split across both",
                    "description": "Use both HTTPS and DNS tunneling to exfiltrate data. Higher throughput but also higher detection risk."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Establish persistence",
                    "description": "Create additional persistence mechanisms. Ensures continued access even if exfiltration is discovered."
                }
            ],
            "blue": [
                {
                    "name": "Block HTTPS exfiltration",
                    "description": "Implement network controls to block suspicious HTTPS connections. Review artifacts to determine if this method is being used."
                },
                {
                    "name": "Block DNS tunneling",
                    "description": "Implement DNS filtering and monitoring to detect and block DNS tunneling. Review artifacts to determine if this method is being used."
                },
                {
                    "name": "Deploy DLP countermeasures",
                    "description": "Enhance Data Loss Prevention controls to detect and block data exfiltration. Comprehensive defense but may impact legitimate traffic."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, network traffic captures, and system artifacts for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Escalate to management",
                    "description": "Notify executive leadership and prepare for potential ransomware deployment. Important for business continuity planning."
                }
            ]
        }
    )
    db.add(phase5)
    db.flush()
    print(f"✓ Created Phase 5 (ID: {phase5.id})")
    
    # Create artifacts for Phase 1
    print("\nCreating artifacts for Phase 1...")
    
    # Red Team Artifacts - Phase 1
    hr_recon = Artifact(
        name="HR Department Reconnaissance Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Reconnaissance data collected on WS-HR-042 (HR Department). Contains security posture assessment, EDR status, and user privilege information.",
        file_url="/api/artifacts/files/hr_recon_phase1.txt",
        notes_for_gm="This artifact shows HR has strong security (latest EDR, attack was blocked). Red Team should NOT choose HR."
    )
    db.add(hr_recon)
    db.flush()
    
    ops_recon = Artifact(
        name="Operations Department Reconnaissance Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Reconnaissance data collected on WS-OPS-089 (Operations Department). Contains security posture assessment, EDR status, and user privilege information.",
        file_url="/api/artifacts/files/ops_recon_phase1.txt",
        notes_for_gm="This artifact shows Operations has weaker security (outdated EDR, attack succeeded). Red Team SHOULD choose Operations."
    )
    db.add(ops_recon)
    db.flush()
    
    c2_status = Artifact(
        name="C2 Connection Status Comparison",
        type=ArtifactType.TOOL_OUTPUT,
        description="Command and Control (C2) connection test results comparing HR and Operations workstations. Shows which target has operational C2 connectivity.",
        file_url="/api/artifacts/files/c2_status_phase1.txt",
        notes_for_gm="Shows HR blocked C2, Operations has operational C2. Confirms Operations is the better target."
    )
    db.add(c2_status)
    db.flush()
    
    # Blue Team Artifacts - Phase 1
    hr_defender = Artifact(
        name="Defender Alert - HR Department",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint alert for WS-HR-042 (HR Department). Contains detection details, EDR status, and response actions.",
        file_url="/api/artifacts/files/defender_hr_alert_phase1.txt",
        notes_for_gm="Shows HR attack was blocked, strong EDR. Blue Team should NOT prioritize HR."
    )
    db.add(hr_defender)
    db.flush()
    
    ops_defender = Artifact(
        name="Defender Alert - Operations Department",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint alert for WS-OPS-089 (Operations Department). Contains detection details, EDR status, and response actions.",
        file_url="/api/artifacts/files/defender_ops_alert_phase1.txt",
        notes_for_gm="Shows Operations attack succeeded, outdated EDR. Blue Team SHOULD prioritize Operations."
    )
    db.add(ops_defender)
    db.flush()
    
    sentinel_phishing = Artifact(
        name="Sentinel Phishing Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="Microsoft Sentinel incident analysis comparing phishing campaign impact on HR and Operations departments. Includes risk scoring and recommendations.",
        file_url="/api/artifacts/files/sentinel_phishing_phase1.txt",
        notes_for_gm="Shows Operations has higher risk score due to successful execution and outdated security. Confirms Operations is higher priority."
    )
    db.add(sentinel_phishing)
    db.flush()
    
    # Link artifacts to Phase 1
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=hr_recon.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=ops_recon.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=c2_status.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=hr_defender.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=ops_defender.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=sentinel_phishing.id, team_role="blue"))
    print("✓ Linked 6 artifacts to Phase 1")
    
    # Create artifacts for Phase 2
    print("\nCreating artifacts for Phase 2...")
    
    # Red Team Artifacts - Phase 2
    persistence_testing = Artifact(
        name="Persistence Method Testing Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Results from testing three persistence mechanisms: Scheduled Tasks, Registry Run Keys, and WMI Event Subscriptions. Includes reliability and detection risk assessment.",
        file_url="/api/artifacts/files/persistence_testing_phase2.txt",
        notes_for_gm="Shows Registry Run Key has best balance of reliability and low detection. Red Team should choose Registry."
    )
    db.add(persistence_testing)
    db.flush()
    
    detection_risk = Artifact(
        name="Detection Risk Assessment",
        type=ArtifactType.TOOL_OUTPUT,
        description="Assessment of detection risk for each persistence method based on security tool responses and system logging.",
        file_url="/api/artifacts/files/detection_risk_phase2.txt",
        notes_for_gm="Shows Registry has lowest detection risk, WMI highest. Confirms Registry is best choice."
    )
    db.add(detection_risk)
    db.flush()
    
    # Blue Team Artifacts - Phase 2
    defender_process = Artifact(
        name="Defender Process Monitoring",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint process monitoring showing detection and blocking status for each persistence method attempt.",
        file_url="/api/artifacts/files/defender_process_phase2.txt",
        notes_for_gm="Shows Registry modifications were detected but not blocked, WMI was blocked. Blue Team should focus on Registry."
    )
    db.add(defender_process)
    db.flush()
    
    system_audit = Artifact(
        name="System Audit Logs",
        type=ArtifactType.LOG_SNIPPET,
        description="Windows System audit logs showing successful modifications for each persistence method. Includes registry changes, scheduled task creation, and WMI subscription attempts.",
        file_url="/api/artifacts/files/system_audit_phase2.txt",
        notes_for_gm="Shows Registry modifications were successful and logged, WMI was blocked. Confirms Registry was deployed."
    )
    db.add(system_audit)
    db.flush()
    
    # Link artifacts to Phase 2
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=persistence_testing.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=detection_risk.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=defender_process.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=system_audit.id, team_role="blue"))
    print("✓ Linked 4 artifacts to Phase 2")
    
    # Create artifacts for Phase 3
    print("\nCreating artifacts for Phase 3...")
    
    # Red Team Artifacts - Phase 3
    fs_prod_recon = Artifact(
        name="FS-PROD-01 Reconnaissance Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Reconnaissance data collected on File Server FS-PROD-01. Contains vulnerability scan results, patch status, and exploit availability.",
        file_url="/api/artifacts/files/fs_prod_recon_phase3.txt",
        notes_for_gm="Shows FS-PROD-01 is fully patched, no known exploits. Red Team should NOT choose FS-PROD-01."
    )
    db.add(fs_prod_recon)
    db.flush()
    
    app_dev_recon = Artifact(
        name="APP-DEV-02 Reconnaissance Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Reconnaissance data collected on Application Server APP-DEV-02. Contains vulnerability scan results, patch status, and exploit availability.",
        file_url="/api/artifacts/files/app_dev_recon_phase3.txt",
        notes_for_gm="Shows APP-DEV-02 has unpatched LPE vulnerability with public exploit available. Red Team SHOULD choose APP-DEV-02."
    )
    db.add(app_dev_recon)
    db.flush()
    
    # Blue Team Artifacts - Phase 3
    vuln_scan = Artifact(
        name="Vulnerability Scan Results",
        type=ArtifactType.INTEL_REPORT,
        description="Microsoft Defender Vulnerability Management scan results for FS-PROD-01 and APP-DEV-02. Includes CVE details, patch status, and risk scoring.",
        file_url="/api/artifacts/files/vuln_scan_phase3.txt",
        notes_for_gm="Shows FS-PROD-01 patched, APP-DEV-02 has CVE-2024-XXXXX unpatched. Blue Team should prioritize APP-DEV-02."
    )
    db.add(vuln_scan)
    db.flush()
    
    sentinel_vuln = Artifact(
        name="Sentinel Vulnerability Correlation",
        type=ArtifactType.INTEL_REPORT,
        description="Microsoft Sentinel correlation of vulnerability data with exploit activity. Shows which server has active exploit attempts.",
        file_url="/api/artifacts/files/sentinel_vuln_phase3.txt",
        notes_for_gm="Shows APP-DEV-02 has high risk score and exploit activity detected. Confirms APP-DEV-02 is priority."
    )
    db.add(sentinel_vuln)
    db.flush()
    
    # Link artifacts to Phase 3
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=fs_prod_recon.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=app_dev_recon.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=vuln_scan.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=sentinel_vuln.id, team_role="blue"))
    print("✓ Linked 4 artifacts to Phase 3")
    
    # Create artifacts for Phase 4
    print("\nCreating artifacts for Phase 4...")
    
    # Red Team Artifacts - Phase 4
    network_mapping = Artifact(
        name="Network Mapping Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Network mapping and connectivity test results for DB-CUST-PROD and DB-HR-PROD. Shows network segmentation and access paths.",
        file_url="/api/artifacts/files/network_mapping_phase4.txt",
        notes_for_gm="Shows DB-CUST-PROD is isolated, DB-HR-PROD is accessible. Red Team should choose DB-HR-PROD."
    )
    db.add(network_mapping)
    db.flush()
    
    access_test = Artifact(
        name="Database Access Test Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Connection test results for both databases. Shows which database accepts connections and which is blocked.",
        file_url="/api/artifacts/files/access_test_phase4.txt",
        notes_for_gm="Shows DB-CUST-PROD blocked, DB-HR-PROD successful connection. Confirms DB-HR-PROD is accessible."
    )
    db.add(access_test)
    db.flush()
    
    # Blue Team Artifacts - Phase 4
    db_access_logs = Artifact(
        name="Database Access Logs",
        type=ArtifactType.LOG_SNIPPET,
        description="Database access logs showing connection attempts and query activity for DB-CUST-PROD and DB-HR-PROD.",
        file_url="/api/artifacts/files/db_access_logs_phase4.txt",
        notes_for_gm="Shows DB-CUST-PROD no access, DB-HR-PROD successful queries detected. Blue Team should prioritize DB-HR-PROD."
    )
    db.add(db_access_logs)
    db.flush()
    
    network_seg = Artifact(
        name="Network Segmentation Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="Microsoft Defender for Cloud network segmentation analysis showing VLAN assignments and access controls for both databases.",
        file_url="/api/artifacts/files/network_seg_phase4.txt",
        notes_for_gm="Shows DB-CUST-PROD isolated VLAN, DB-HR-PROD standard VLAN. Confirms DB-HR-PROD is less protected."
    )
    db.add(network_seg)
    db.flush()
    
    # Link artifacts to Phase 4
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=network_mapping.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=access_test.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=db_access_logs.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=network_seg.id, team_role="blue"))
    print("✓ Linked 4 artifacts to Phase 4")
    
    # Create artifacts for Phase 5
    print("\nCreating artifacts for Phase 5...")
    
    # Red Team Artifacts - Phase 5
    exfil_testing = Artifact(
        name="Exfiltration Method Testing",
        type=ArtifactType.TOOL_OUTPUT,
        description="Testing results for HTTPS tunnel and DNS tunneling exfiltration methods. Includes speed, reliability, and detection risk assessment.",
        file_url="/api/artifacts/files/exfil_testing_phase5.txt",
        notes_for_gm="Shows HTTPS well-monitored, DNS tunneling has detection gaps. Red Team should choose DNS tunneling."
    )
    db.add(exfil_testing)
    db.flush()
    
    data_transfer = Artifact(
        name="Data Transfer Analysis",
        type=ArtifactType.TOOL_OUTPUT,
        description="Analysis of data transfer capabilities for both exfiltration methods. Includes bandwidth, reliability, and detection risk comparison.",
        file_url="/api/artifacts/files/data_transfer_phase5.txt",
        notes_for_gm="Shows HTTPS faster but detected, DNS slower but more reliable with lower detection. Confirms DNS is better choice."
    )
    db.add(data_transfer)
    db.flush()
    
    # Blue Team Artifacts - Phase 5
    dlp_analysis = Artifact(
        name="DLP Alert Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="Microsoft Purview Data Loss Prevention alert analysis comparing detection capabilities for HTTPS and DNS tunneling exfiltration methods.",
        file_url="/api/artifacts/files/dlp_analysis_phase5.txt",
        notes_for_gm="Shows HTTPS well-monitored, DNS tunneling has detection gaps. Blue Team should prioritize DNS tunneling blocking."
    )
    db.add(dlp_analysis)
    db.flush()
    
    bandwidth_analysis = Artifact(
        name="Network Bandwidth Analysis",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Cloud network bandwidth analysis showing anomalies for HTTPS and DNS traffic patterns.",
        file_url="/api/artifacts/files/bandwidth_analysis_phase5.txt",
        notes_for_gm="Shows HTTPS anomalies are clear, DNS anomalies less obvious. Confirms DNS tunneling is being used and needs attention."
    )
    db.add(bandwidth_analysis)
    db.flush()
    
    # Link artifacts to Phase 5
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=exfil_testing.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=data_transfer.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=dlp_analysis.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=bandwidth_analysis.id, team_role="blue"))
    print("✓ Linked 4 artifacts to Phase 5")
    
    db.commit()
    print(f"\n✅ Successfully created scenario '{scenario_name}' with 5 phases and 22 artifacts!")
    print(f"   Scenario ID: {scenario.id}")
    print(f"   Phase IDs: {phase1.id}, {phase2.id}, {phase3.id}, {phase4.id}, {phase5.id}")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error creating scenario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

