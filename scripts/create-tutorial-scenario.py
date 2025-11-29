#!/usr/bin/env python3
"""
Manually create the Tutorial scenario in the database.
This script can be run directly to ensure the tutorial scenario exists.
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    Scenario, ScenarioPhase, Artifact, ArtifactType,
    scenario_phase_artifacts
)
from app.auth import get_password_hash

db: Session = SessionLocal()

try:
    # Check if tutorial scenario exists
    tutorial_scenario = db.query(Scenario).filter(Scenario.name == "Tutorial: Basic Security Incident").first()
    
    if tutorial_scenario:
        print(f"Tutorial scenario already exists (ID: {tutorial_scenario.id})")
        print(f"  Phases: {len(tutorial_scenario.phases)}")
        sys.exit(0)
    
    print("Creating Tutorial scenario...")
    
    # Create scenario
    tutorial_scenario = Scenario(
        name="Tutorial: Basic Security Incident",
        description="A simple two-phase scenario designed to teach players how the game works. This tutorial covers the basic mechanics: reading briefings, reviewing artifacts, making decisions, and understanding team objectives. Perfect for first-time players.",
        miro_board_url="https://miro.com/app/board/tutorial"
    )
    db.add(tutorial_scenario)
    db.flush()
    print(f"  Created scenario (ID: {tutorial_scenario.id})")

    # Phase 1: Initial Detection
    tutorial_phase1 = ScenarioPhase(
        scenario_id=tutorial_scenario.id,
        order_index=0,
        name="Phase 1: Initial Detection",
        briefing_text="Welcome to the Cyber Tabletop Tutorial! This scenario will walk you through how the game works.\n\n**The Situation:**\nAt 9:00 AM, your security operations center receives an alert from your email security gateway. An employee in the Marketing department clicked a suspicious link in an email. The email appeared to be from a legitimate vendor but contained a link to an external domain. Initial analysis shows the link attempted to download a file, but your email security blocked the download.\n\n**What You Need to Do:**\n1. Review the artifacts provided below\n2. Understand your team's objective\n3. Select an action that best aligns with your objective\n4. Rate how effective you think your organization would be at handling this (1-10 scale)\n5. Add any comments you'd like (optional, max 500 characters)\n6. Submit your decision\n\n**Remember:** This is a tutorial - focus on understanding the game mechanics rather than making the perfect decision.",
        red_objective="Tutorial Objective: Your goal is to establish initial access to the target network. The email link was blocked, but you may have other options. Review the artifacts to understand what happened and plan your next move. For this tutorial, focus on understanding how to read your objectives and make decisions.",
        blue_objective="Tutorial Objective: Your goal is to detect and contain the threat. The email was blocked, but you need to determine if any compromise occurred. Review the artifacts to understand what happened and decide on your response. For this tutorial, focus on understanding how to read your objectives and make decisions.",
        default_duration_seconds=600,
        miro_frame_url="https://miro.com/app/board/tutorial/frame1"
    )
    db.add(tutorial_phase1)
    db.flush()
    print(f"  Created Phase 1 (ID: {tutorial_phase1.id})")

    # Phase 2: Response & Containment
    tutorial_phase2 = ScenarioPhase(
        scenario_id=tutorial_scenario.id,
        order_index=1,
        name="Phase 2: Response & Containment",
        briefing_text="**Phase 2: Response & Containment**\n\nGood work completing Phase 1! You've now seen how the game mechanics work.\n\n**The Situation Continues:**\nAfter reviewing the initial alert, your team has gathered more information. The email security gateway blocked the malicious download, but forensic analysis shows the user's workstation may have been compromised through a different vector. Network monitoring has detected unusual outbound connections from the Marketing department workstation.\n\n**What You Need to Do:**\n1. Review the new artifacts for this phase\n2. Consider what happened in Phase 1\n3. Make your decision for Phase 2\n4. Remember to rate your organization's effectiveness\n5. Submit your decision\n\n**Tutorial Tip:** Notice how the situation evolves between phases. Your decisions in Phase 1 may influence what happens in Phase 2. This is how the full game scenarios work!",
        red_objective="Tutorial Objective: You've successfully established a connection to the target workstation. Now you need to maintain access and avoid detection. Review the artifacts to see what the defenders have discovered and plan your next move. For this tutorial, focus on understanding how phases build upon each other.",
        blue_objective="Tutorial Objective: You've detected suspicious network activity from the Marketing workstation. You need to contain the threat and prevent further compromise. Review the artifacts to understand the full scope and decide on your containment strategy. For this tutorial, focus on understanding how phases build upon each other.",
        default_duration_seconds=600,
        miro_frame_url="https://miro.com/app/board/tutorial/frame2"
    )
    db.add(tutorial_phase2)
    db.flush()
    print(f"  Created Phase 2 (ID: {tutorial_phase2.id})")

    # Create Tutorial Artifacts - Phase 1
    tutorial_artifact1_blue = Artifact(
        name="Email Security Alert",
        type=ArtifactType.EMAIL,
        description="Email Security Gateway Alert:\n\nAlert ID: ESG-2024-TUT-001\nTimestamp: 09:00:15 UTC\nUser: marketing.user@company.local\nSubject: 'URGENT: Invoice Payment Required'\nFrom: vendor-support@legitimate-vendor.com\n\nAction Taken: BLOCKED\nReason: Suspicious link detected\nLink: http://secure-invoice-download[.]tk/invoice.pdf\n\nStatus: Email quarantined, download blocked\nUser Notified: Yes\n\nThis is a tutorial artifact. In real scenarios, you would see actual email screenshots or logs.",
        file_url="/api/artifacts/files/tutorial_email_alert.txt",
        notes_for_gm="Tutorial artifact showing email security alert. Simple and clear for learning."
    )
    db.add(tutorial_artifact1_blue)
    db.flush()

    tutorial_artifact2_blue = Artifact(
        name="User Workstation Status",
        type=ArtifactType.LOG_SNIPPET,
        description="Workstation Status Report:\n\nHostname: WS-MKT-015\nUser: marketing.user@company.local\nDepartment: Marketing\nLast Login: 08:45:00 UTC\n\nCurrent Status:\n- Endpoint Protection: Active\n- Last Scan: 08:00:00 UTC (Clean)\n- Network Connections: Normal\n- Running Processes: No anomalies detected\n\nNote: Initial scan shows no malware detected. Further investigation recommended.\n\nThis is a tutorial artifact. In real scenarios, you would see detailed system logs.",
        file_url="/api/artifacts/files/tutorial_workstation_status.txt",
        notes_for_gm="Tutorial artifact showing workstation status. Simple for learning."
    )
    db.add(tutorial_artifact2_blue)
    db.flush()

    tutorial_artifact1_red = Artifact(
        name="Phishing Campaign Status",
        type=ArtifactType.TOOL_OUTPUT,
        description="Phishing Campaign Status:\n\nCampaign: Invoice Payment Phish\nTarget: Company Marketing Department\nMethod: Email with malicious link\n\nResults:\n- Emails Sent: 50\n- Emails Opened: 12\n- Links Clicked: 3\n- Downloads Blocked: 3\n\nStatus: Initial email link was blocked by target's email security.\n\nNext Steps:\n- Alternative access methods available\n- Consider secondary payload delivery\n- Maintain persistence through other vectors\n\nThis is a tutorial artifact. In real scenarios, you would see actual attack tool outputs.",
        file_url="/api/artifacts/files/tutorial_phish_status.txt",
        notes_for_gm="Tutorial artifact showing phishing campaign status. Simple for learning."
    )
    db.add(tutorial_artifact1_red)
    db.flush()

    tutorial_artifact2_red = Artifact(
        name="Target Information",
        type=ArtifactType.INTEL_REPORT,
        description="Target Reconnaissance Report:\n\nTarget: Company Marketing Department\nInitial Vector: Email phishing\n\nTarget Information:\n- Email Security: Active (blocked initial attempt)\n- Endpoint Protection: Present\n- Network Segmentation: Unknown\n\nAssessment:\n- Initial email link blocked\n- Alternative access methods needed\n- Target appears security-aware\n\nRecommendation:\n- Try alternative delivery method\n- Consider social engineering\n- Prepare backup access vectors\n\nThis is a tutorial artifact. In real scenarios, you would see detailed reconnaissance data.",
        file_url="/api/artifacts/files/tutorial_target_info.txt",
        notes_for_gm="Tutorial artifact showing target information. Simple for learning."
    )
    db.add(tutorial_artifact2_red)
    db.flush()

    # Phase 2 Artifacts
    tutorial_artifact3_blue = Artifact(
        name="Network Traffic Analysis",
        type=ArtifactType.LOG_SNIPPET,
        description="Network Traffic Analysis Report:\n\nHostname: WS-MKT-015\nTime Range: 09:00:00 - 09:15:00 UTC\n\nSuspicious Activity Detected:\n- Outbound Connection: 185.220.101.45:443\n- Protocol: HTTPS\n- Duration: 12 minutes\n- Data Transferred: 2.3 MB\n- Connection Pattern: Unusual (not typical user behavior)\n\nAnalysis:\n- Destination IP not in whitelist\n- Connection established shortly after email alert\n- Encrypted traffic (cannot inspect payload)\n\nRecommendation: Investigate further, consider isolating workstation.\n\nThis is a tutorial artifact. In real scenarios, you would see detailed network logs.",
        file_url="/api/artifacts/files/tutorial_network_traffic.txt",
        notes_for_gm="Tutorial artifact showing network traffic analysis. Simple for learning."
    )
    db.add(tutorial_artifact3_blue)
    db.flush()

    tutorial_artifact4_blue = Artifact(
        name="Incident Response Checklist",
        type=ArtifactType.INTEL_REPORT,
        description="Incident Response Checklist:\n\nCurrent Status: Investigation Phase\n\nCompleted:\n✓ Email alert reviewed\n✓ Workstation identified\n✓ Initial scan completed\n\nIn Progress:\n- Network traffic analysis\n- Forensic investigation\n\nNext Steps:\n- [ ] Isolate affected workstation\n- [ ] Collect forensic evidence\n- [ ] Determine scope of compromise\n- [ ] Notify management\n- [ ] Document incident\n\nThis is a tutorial artifact. In real scenarios, you would see actual incident response procedures.",
        file_url="/api/artifacts/files/tutorial_ir_checklist.txt",
        notes_for_gm="Tutorial artifact showing incident response checklist. Simple for learning."
    )
    db.add(tutorial_artifact4_blue)
    db.flush()

    tutorial_artifact3_red = Artifact(
        name="Access Confirmation",
        type=ArtifactType.TOOL_OUTPUT,
        description="Access Status Report:\n\nTarget: WS-MKT-015\nAccess Method: Alternative delivery (USB drop + social engineering)\nStatus: ACCESS ESTABLISHED\n\nConnection Details:\n- C2 Server: 185.220.101.45:443\n- Beacon Interval: 300 seconds\n- Last Check-in: 09:12:00 UTC\n- Connection: Stable\n\nSystem Information:\n- OS: Windows 10 Enterprise\n- Domain: COMPANY.LOCAL\n- User Privileges: Standard User\n\nCurrent Status:\n- Persistence: Established\n- Detection: Not detected (yet)\n- Next Phase: Maintain access, escalate privileges\n\nThis is a tutorial artifact. In real scenarios, you would see actual C2 tool outputs.",
        file_url="/api/artifacts/files/tutorial_access_confirm.txt",
        notes_for_gm="Tutorial artifact showing access confirmation. Simple for learning."
    )
    db.add(tutorial_artifact3_red)
    db.flush()

    tutorial_artifact4_red = Artifact(
        name="Defender Activity Report",
        type=ArtifactType.INTEL_REPORT,
        description="Defender Activity Assessment:\n\nTarget Response:\n- Email Security: Blocked initial attempt\n- Endpoint Protection: Active\n- Network Monitoring: Detecting unusual traffic\n\nDefender Actions Observed:\n- Email alert generated\n- Workstation scan initiated\n- Network traffic analysis in progress\n\nAssessment:\n- Defenders are aware of initial email\n- Network monitoring may detect C2 connection\n- Time to detection: ~15 minutes\n\nRecommendation:\n- Maintain low profile\n- Prepare for potential isolation\n- Have backup access methods ready\n\nThis is a tutorial artifact. In real scenarios, you would see detailed defender intelligence.",
        file_url="/api/artifacts/files/tutorial_defender_activity.txt",
        notes_for_gm="Tutorial artifact showing defender activity. Simple for learning."
    )
    db.add(tutorial_artifact4_red)
    db.flush()

    # Associate artifacts with phases
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact1_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact2_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact1_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact2_red.id, team_role="red"))

    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact3_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact4_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact3_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact4_red.id, team_role="red"))

    db.commit()
    print("✓ Tutorial scenario created successfully!")
    print(f"  Scenario ID: {tutorial_scenario.id}")
    print(f"  Phases: 2")
    print(f"  Artifacts: 8 (4 per team)")
    
except Exception as e:
    print(f"❌ Error creating tutorial scenario: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
    sys.exit(1)
finally:
    db.close()

