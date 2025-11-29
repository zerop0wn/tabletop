"""
Create a new artifact-driven Ransomware scenario.
This script creates a fresh scenario with all phases, artifacts, and phase-specific actions.
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
    scenario_name = "Ransomware Attack: Advanced Persistent Threat"
    existing_scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if existing_scenario:
        print(f"Scenario '{scenario_name}' already exists (ID: {existing_scenario.id})")
        print("Delete it first if you want to recreate it.")
        sys.exit(0)
    
    print(f"Creating new scenario: {scenario_name}")
    
    # Create scenario
    scenario = Scenario(
        name=scenario_name,
        description="An advanced ransomware attack scenario with artifact-driven decision making. Each phase requires analyzing security artifacts to determine the correct course of action. Teams must carefully review Defender alerts, Sentinel logs, and reconnaissance data to make optimal decisions.",
        miro_board_url="https://miro.com/app/board/example"
    )
    db.add(scenario)
    db.flush()
    print(f"✓ Created scenario (ID: {scenario.id})")
    
    # Phase 1: Initial Access - IT vs Sales Department
    phase1 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=0,
        name="Phase 1: Initial Access - Email Compromise",
        briefing_text="At 09:20 AM, a phishing campaign has successfully delivered emails to two departments:\n- IT Department (WS-IT-089): 8 emails opened, 2 links clicked\n- Sales Department (WS-SLS-203): 15 emails opened, 5 links clicked\n\nBoth departments have users who clicked the malicious links. Initial access attempts have been detected on workstations in both departments:\n- **WS-IT-089** (IT): it.admin@corp.local clicked malicious link\n- **WS-SLS-203** (Sales): sales.rep@corp.local clicked malicious link\n\nSecurity monitoring has detected suspicious activity from both workstations. The security team needs to determine which department presents the highest risk and requires immediate containment.\n\nInitial reconnaissance data has been collected on both targets (WS-IT-089 and WS-SLS-203). Your decision: **Which department should you prioritize for investigation and containment?**\n\n**Remember:** Review the artifacts carefully. They contain critical information about security posture, EDR coverage, and user privileges for **both WS-IT-089 and WS-SLS-203** that will help determine the appropriate response. The artifacts will reveal which target has weaker security controls and presents the greater risk.",
        red_objective="Analyze the reconnaissance data from both departments to identify which target offers the best opportunity for establishing persistent access with minimal detection risk. Focus your initial persistence efforts on the most vulnerable target.",
        blue_objective="Review security telemetry from both departments to identify which department shows the most concerning indicators of compromise. Prioritize containment and investigation efforts on the department with the highest risk of successful attacker persistence.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame1",
        available_actions={
            "red": [
                {
                    "name": "Focus on IT Department (WS-IT-089)",
                    "description": "Prioritize establishing persistence on WS-IT-089 (IT). Review artifacts comparing WS-IT-089 and WS-SLS-203 to assess security posture and detection risk."
                },
                {
                    "name": "Focus on Sales Department (WS-SLS-203)",
                    "description": "Prioritize establishing persistence on WS-SLS-203 (Sales). Review artifacts comparing WS-IT-089 and WS-SLS-203 to assess security posture and detection risk."
                },
                {
                    "name": "Split efforts between both departments",
                    "description": "Attempt to establish persistence on both IT and Sales workstations simultaneously. Higher chance of success but also higher detection risk."
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
                    "name": "Isolate IT Department host (WS-IT-089)",
                    "description": "Disconnect WS-IT-089 (IT) from the network to prevent further spread. Review artifacts comparing WS-IT-089 and WS-SLS-203 to assess risk level."
                },
                {
                    "name": "Isolate Sales Department host (WS-SLS-203)",
                    "description": "Disconnect WS-SLS-203 (Sales) from the network to prevent further spread. Review artifacts comparing WS-IT-089 and WS-SLS-203 to assess risk level."
                },
                {
                    "name": "Isolate both hosts",
                    "description": "Disconnect both IT and Sales workstations from the network. Conservative approach but may impact business operations."
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
        briefing_text="Initial access has been established on the target workstation. Security monitoring has detected attempts to create persistence mechanisms to maintain access even if the initial entry point is discovered.\n\nSecurity analysis has identified three different persistence methods being tested, with data collected on their detection and blocking capabilities. Your decision: **Which persistence mechanism should be prioritized for removal and investigation?**\n\n**Remember:** Review the artifacts carefully. They contain information about detection rates, blocking capabilities, and visibility for each persistence method.",
        red_objective="Select the persistence mechanism that offers the best balance of reliability, low visibility, and low detection risk. The mechanism should survive reboots and be difficult for defenders to discover and remove.",
        blue_objective="Identify which persistence mechanisms have been deployed and remove them. Prioritize mechanisms that are most likely to survive reboots and maintain attacker access.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame2",
        available_actions={
            "red": [
                {
                    "name": "Deploy Scheduled Task persistence",
                    "description": "Create a scheduled task that runs your payload. Review artifacts to assess detection and blocking risk."
                },
                {
                    "name": "Deploy Registry Run Key persistence",
                    "description": "Modify the Windows registry to run your payload on startup. Review artifacts to assess detection and blocking risk."
                },
                {
                    "name": "Deploy Service Creation persistence",
                    "description": "Create a Windows service to run your payload. Review artifacts to assess detection and blocking risk."
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
                    "name": "Remove scheduled tasks",
                    "description": "Audit and remove suspicious scheduled tasks. Review artifacts to identify which persistence methods were used."
                },
                {
                    "name": "Audit and clean registry",
                    "description": "Review registry run keys and remove suspicious entries. Review artifacts to identify which persistence methods were used."
                },
                {
                    "name": "Monitor and block services",
                    "description": "Audit Windows services and block suspicious service creation. Review artifacts to identify which persistence methods were used."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, memory dumps, and system artifacts for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Deploy countermeasures",
                    "description": "Implement security controls like enhanced monitoring or network segmentation. Proactive defense but may impact system availability."
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
        briefing_text="Persistence has been established on the initial workstation with standard user privileges. Security monitoring indicates attempts to escalate privileges to access sensitive data and systems.\n\nTwo potential targets for privilege escalation have been identified:\n- **File Server FS-01**: Appears to be fully patched\n- **Application Server APP-02**: Appears to have unpatched vulnerabilities\n\nVulnerability scan results and reconnaissance data have been collected on both targets. Your decision: **Which server should be prioritized for containment and patching?**\n\n**Remember:** Review the artifacts carefully. They contain vulnerability information, patch status, and exploit availability for **both FS-01 and APP-02** that will help determine the appropriate response.",
        red_objective="Analyze vulnerability data and reconnaissance reports to identify which target offers the best opportunity for successful privilege escalation with acceptable detection risk.",
        blue_objective="Review vulnerability scan results and security telemetry to identify which server is at highest risk for privilege escalation. Prioritize containment and patching efforts.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame3",
        available_actions={
            "red": [
                {
                    "name": "Escalate privileges on FS-01 (File Server)",
                    "description": "Attempt privilege escalation on FS-01. Review artifacts comparing FS-01 and APP-02 to assess success probability and detection risk."
                },
                {
                    "name": "Escalate privileges on APP-02 (Application Server)",
                    "description": "Attempt privilege escalation on APP-02. Review artifacts comparing FS-01 and APP-02 to assess success probability and detection risk."
                },
                {
                    "name": "Attempt escalation on both servers",
                    "description": "Run privilege escalation attempts on both FS-01 and APP-02 in parallel. Higher chance of success but also higher detection risk."
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
                    "name": "Isolate FS-01 (File Server)",
                    "description": "Disconnect FS-01 from the network to prevent privilege escalation. Review artifacts comparing FS-01 and APP-02 to assess risk level."
                },
                {
                    "name": "Isolate APP-02 (Application Server)",
                    "description": "Disconnect APP-02 from the network to prevent privilege escalation. Review artifacts comparing FS-01 and APP-02 to assess risk level."
                },
                {
                    "name": "Isolate both servers",
                    "description": "Disconnect both FS-01 and APP-02 from the network. Conservative approach but may impact business operations."
                },
                {
                    "name": "Patch vulnerabilities",
                    "description": "Apply security patches to vulnerable systems. Critical for preventing escalation but takes time and may require maintenance windows."
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
        briefing_text="Privilege escalation has been successful, and access to multiple servers has been detected. Two database servers containing valuable data have been identified:\n- **DB-CUST-01** (Customer Database): Contains customer PII and records\n- **DB-FIN-02** (Financial Records): Contains financial data and records\n\nNetwork mapping and access tests have been detected on both targets. Your decision: **Which database server should be prioritized for protection and access restriction?**\n\n**Remember:** Review the artifacts carefully. They contain network topology information, access logs, and security controls for **both DB-CUST-01 and DB-FIN-02** that will help determine the appropriate response.",
        red_objective="Analyze network mapping and access test results to identify which database server offers the best opportunity for data access with acceptable detection risk.",
        blue_objective="Review access logs and network segmentation analysis to identify which database server shows signs of potential compromise. Prioritize containment and protection efforts.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame4",
        available_actions={
            "red": [
                {
                    "name": "Target DB-CUST-01 (Customer Database)",
                    "description": "Focus data access efforts on DB-CUST-01. Review artifacts comparing DB-CUST-01 and DB-FIN-02 to assess access difficulty and detection risk."
                },
                {
                    "name": "Target DB-FIN-02 (Financial Records)",
                    "description": "Focus data access efforts on DB-FIN-02. Review artifacts comparing DB-CUST-01 and DB-FIN-02 to assess access difficulty and detection risk."
                },
                {
                    "name": "Target both databases",
                    "description": "Attempt to access both DB-CUST-01 and DB-FIN-02 simultaneously. Maximizes data value but also increases detection risk."
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
                    "name": "Isolate DB-CUST-01 (Customer Database)",
                    "description": "Disconnect DB-CUST-01 from the network to prevent data access. Review artifacts comparing DB-CUST-01 and DB-FIN-02 to assess priority."
                },
                {
                    "name": "Isolate DB-FIN-02 (Financial Records)",
                    "description": "Disconnect DB-FIN-02 from the network to prevent data access. Review artifacts comparing DB-CUST-01 and DB-FIN-02 to assess priority."
                },
                {
                    "name": "Isolate both databases",
                    "description": "Disconnect both DB-CUST-01 and DB-FIN-02 from the network. Conservative approach but may impact business operations."
                },
                {
                    "name": "Block database access",
                    "description": "Implement network rules to block unauthorized database access. Proactive defense but may impact legitimate applications."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, network flow data, and access logs for analysis. Critical for understanding what data was accessed but takes time."
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
        briefing_text="Access to valuable data from the target database has been detected. Security monitoring indicates attempts to exfiltrate this data, with two exfiltration methods being tested. Data Loss Prevention (DLP) systems have collected information on their detection capabilities.\n\nYour decision: **Which exfiltration method should be prioritized for blocking and investigation?**\n\n- Option A: Encrypted HTTPS tunnel (slower but may be less detectable)\n- Option B: DNS tunneling (faster but may be more detectable)\n- Option C: Both methods being used simultaneously\n\n**Remember:** Review the artifacts carefully. They contain DLP alert analysis, network bandwidth data, and detection test results that will help determine which method presents the greater threat and requires immediate blocking.",
        red_objective="Select the exfiltration method that offers the best balance of speed, reliability, and low detection risk. The method should successfully transfer data without triggering security alerts.",
        blue_objective="Identify which exfiltration method is being used and block it. Review DLP alerts and network analysis to determine the attack vector and implement appropriate countermeasures.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame5",
        available_actions={
            "red": [
                {
                    "name": "Use HTTPS encrypted tunnel",
                    "description": "Exfiltrate data using encrypted HTTPS connections. Review artifacts to assess detection risk and blocking capabilities."
                },
                {
                    "name": "Use DNS tunneling",
                    "description": "Exfiltrate data using DNS query tunneling. Review artifacts to assess detection risk and blocking capabilities."
                },
                {
                    "name": "Split data across both methods",
                    "description": "Use both HTTPS and DNS tunneling to exfiltrate data in parallel. Maximizes speed but also increases detection risk."
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
                    "name": "Block HTTPS exfiltration",
                    "description": "Implement DLP policies to block HTTPS data exfiltration. Review artifacts to identify which method is being used."
                },
                {
                    "name": "Block DNS tunneling",
                    "description": "Implement DNS filtering to block suspicious DNS tunneling. Review artifacts to identify which method is being used."
                },
                {
                    "name": "Deploy DLP countermeasures",
                    "description": "Deploy comprehensive Data Loss Prevention controls to block all exfiltration methods. Conservative approach but may impact legitimate traffic."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather network flow data, DLP logs, and access logs for analysis. Critical for understanding what data was stolen but takes time."
                },
                {
                    "name": "Escalate to management",
                    "description": "Notify leadership and activate incident response procedures. Ensures proper coordination but may slow immediate response actions."
                }
            ]
        }
    )
    db.add(phase5)
    db.flush()
    print(f"✓ Created Phase 5 (ID: {phase5.id})")
    
    # Create Artifacts - Phase 1
    print("\nCreating Phase 1 artifacts...")
    
    artifact1_blue = Artifact(
        name="Microsoft Defender for Endpoint - IT Department Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint alert showing IT department has strong EDR coverage and blocked the attack.",
        file_url="/api/artifacts/files/defender_it_alert_phase1.txt",
        notes_for_gm="IT department has excellent security - attack was blocked."
    )
    db.add(artifact1_blue)
    db.flush()
    
    artifact2_blue = Artifact(
        name="Microsoft Defender for Endpoint - Sales Department Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint alert showing Sales department has outdated EDR agent and weaker security posture.",
        file_url="/api/artifacts/files/defender_sales_alert_phase1.txt",
        notes_for_gm="Sales department has weaker security - attack was detected but not blocked."
    )
    db.add(artifact2_blue)
    db.flush()
    
    artifact3_blue = Artifact(
        name="Microsoft Sentinel - Phishing Campaign Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="Microsoft Sentinel analysis showing Sales department is higher risk.",
        file_url="/api/artifacts/files/sentinel_phishing_analysis_new_phase1.txt",
        notes_for_gm="Sentinel analysis recommends prioritizing Sales department."
    )
    db.add(artifact3_blue)
    db.flush()
    
    artifact1_red = Artifact(
        name="IT Department Reconnaissance Report",
        type=ArtifactType.INTEL_REPORT,
        description="Red Team reconnaissance showing IT has strong security but was blocked.",
        file_url="/api/artifacts/files/it_recon_phase1.txt",
        notes_for_gm="Red Team sees IT has excellent security."
    )
    db.add(artifact1_red)
    db.flush()
    
    artifact2_red = Artifact(
        name="Sales Department Reconnaissance Report",
        type=ArtifactType.INTEL_REPORT,
        description="Red Team reconnaissance showing Sales has weaker security and better opportunity.",
        file_url="/api/artifacts/files/sales_recon_phase1.txt",
        notes_for_gm="Red Team sees Sales has weaker security."
    )
    db.add(artifact2_red)
    db.flush()
    
    artifact3_red = Artifact(
        name="C2 Connection Status - Both Targets",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team C2 status showing Sales target is better for persistence.",
        file_url="/api/artifacts/files/c2_status_comparison_phase1.txt",
        notes_for_gm="Red Team sees Sales target is operational, IT was blocked."
    )
    db.add(artifact3_red)
    db.flush()
    
    # Link Phase 1 artifacts
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact3_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact3_red.id, team_role="red"))
    print("✓ Linked Phase 1 artifacts")
    
    # Create Artifacts - Phase 2
    print("\nCreating Phase 2 artifacts...")
    
    artifact4_blue = Artifact(
        name="Microsoft Defender - Process Monitoring Report",
        type=ArtifactType.LOG_SNIPPET,
        description="Defender process monitoring showing detection capabilities for different persistence methods.",
        file_url="/api/artifacts/files/defender_process_monitoring_phase2.txt",
        notes_for_gm="Shows scheduled tasks and registry keys are detected but not blocked, services are blocked."
    )
    db.add(artifact4_blue)
    db.flush()
    
    artifact4_red = Artifact(
        name="Persistence Mechanism Detection Test Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team test results showing registry run key is best option.",
        file_url="/api/artifacts/files/persistence_test_results_phase2.txt",
        notes_for_gm="Red Team testing shows registry run key has best balance."
    )
    db.add(artifact4_red)
    db.flush()
    
    # Link Phase 2 artifacts
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_red.id, team_role="red"))
    print("✓ Linked Phase 2 artifacts")
    
    # Create Artifacts - Phase 3
    print("\nCreating Phase 3 artifacts...")
    
    artifact5_blue = Artifact(
        name="Microsoft Defender Vulnerability Management Report",
        type=ArtifactType.INTEL_REPORT,
        description="Vulnerability scan showing FS-01 is patched, APP-02 has unpatched LPE vulnerability.",
        file_url="/api/artifacts/files/vulnerability_scan_phase3.txt",
        notes_for_gm="FS-01 is secure, APP-02 has unpatched vulnerability."
    )
    db.add(artifact5_blue)
    db.flush()
    
    artifact6_blue = Artifact(
        name="Microsoft Sentinel - Vulnerability Correlation",
        type=ArtifactType.INTEL_REPORT,
        description="Sentinel correlation showing APP-02 is at high risk.",
        file_url="/api/artifacts/files/sentinel_vuln_correlation_phase3.txt",
        notes_for_gm="Sentinel identifies APP-02 as high risk."
    )
    db.add(artifact6_blue)
    db.flush()
    
    artifact5_red = Artifact(
        name="File Server FS-01 Reconnaissance Report",
        type=ArtifactType.INTEL_REPORT,
        description="Red Team recon showing FS-01 is fully patched.",
        file_url="/api/artifacts/files/fs01_recon_phase3.txt",
        notes_for_gm="Red Team sees FS-01 is secure."
    )
    db.add(artifact5_red)
    db.flush()
    
    artifact6_red = Artifact(
        name="Application Server APP-02 Reconnaissance Report",
        type=ArtifactType.INTEL_REPORT,
        description="Red Team recon showing APP-02 has unpatched LPE vulnerability.",
        file_url="/api/artifacts/files/app02_recon_phase3.txt",
        notes_for_gm="Red Team sees APP-02 has exploitable vulnerability."
    )
    db.add(artifact6_red)
    db.flush()
    
    # Link Phase 3 artifacts
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_red.id, team_role="red"))
    print("✓ Linked Phase 3 artifacts")
    
    # Create Artifacts - Phase 4
    print("\nCreating Phase 4 artifacts...")
    
    artifact7_blue = Artifact(
        name="Microsoft Sentinel - Database Access Log Analysis",
        type=ArtifactType.LOG_SNIPPET,
        description="Access logs showing DB-CUST-01 is secure, DB-FIN-02 has successful access.",
        file_url="/api/artifacts/files/database_access_logs_phase4.txt",
        notes_for_gm="DB-CUST-01 blocked access, DB-FIN-02 has successful access."
    )
    db.add(artifact7_blue)
    db.flush()
    
    artifact8_blue = Artifact(
        name="Network Segmentation Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="Network analysis showing DB-FIN-02 is less isolated.",
        file_url="/api/artifacts/files/network_segmentation_phase4.txt",
        notes_for_gm="DB-FIN-02 has weaker network segmentation."
    )
    db.add(artifact8_blue)
    db.flush()
    
    artifact7_red = Artifact(
        name="Network Mapping and Access Test Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team network mapping showing DB-FIN-02 is accessible.",
        file_url="/api/artifacts/files/network_mapping_phase4.txt",
        notes_for_gm="Red Team sees DB-FIN-02 is accessible, DB-CUST-01 is not."
    )
    db.add(artifact7_red)
    db.flush()
    
    # Link Phase 4 artifacts
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_red.id, team_role="red"))
    print("✓ Linked Phase 4 artifacts")
    
    # Create Artifacts - Phase 5
    print("\nCreating Phase 5 artifacts...")
    
    artifact9_blue = Artifact(
        name="Microsoft Purview DLP Alert Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="DLP analysis showing HTTPS is well-monitored, DNS tunneling has detection gaps.",
        file_url="/api/artifacts/files/dlp_alert_analysis_phase5.txt",
        notes_for_gm="HTTPS is well-monitored, DNS tunneling has gaps."
    )
    db.add(artifact9_blue)
    db.flush()
    
    artifact10_blue = Artifact(
        name="Network Bandwidth and Traffic Analysis",
        type=ArtifactType.LOG_SNIPPET,
        description="Bandwidth analysis showing anomalies in both methods.",
        file_url="/api/artifacts/files/bandwidth_analysis_phase5.txt",
        notes_for_gm="Both methods show anomalies, HTTPS more clearly malicious."
    )
    db.add(artifact10_blue)
    db.flush()
    
    artifact8_red = Artifact(
        name="Data Exfiltration Method Testing Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team testing showing DNS tunneling has lower detection risk.",
        file_url="/api/artifacts/files/exfiltration_test_results_phase5.txt",
        notes_for_gm="Red Team testing shows DNS tunneling is more reliable."
    )
    db.add(artifact8_red)
    db.flush()
    
    # Link Phase 5 artifacts
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact9_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact10_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact8_red.id, team_role="red"))
    print("✓ Linked Phase 5 artifacts")
    
    # Commit everything
    db.commit()
    print("\n" + "=" * 60)
    print("✓ Successfully created new Ransomware scenario!")
    print(f"  Scenario ID: {scenario.id}")
    print(f"  Scenario Name: {scenario.name}")
    print(f"  Phases: 5")
    print(f"  Total Artifacts: 10")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)
finally:
    db.close()

