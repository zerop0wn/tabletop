"""
Migration script to update existing ransomware scenario to enhanced 5-phase version.
This will update the existing scenario or create it if it doesn't exist.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    Scenario, ScenarioPhase, Artifact, ArtifactType,
    scenario_phase_artifacts
)

# Create tables
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()


def migrate_scenario():
    from app.models import Game, PhaseDecision
    
    # Find or create scenario
    scenario = db.query(Scenario).filter(Scenario.name == "Ransomware Incident Response").first()
    
    if scenario:
        # Clear current_phase_id from any active games to avoid foreign key violations
        print("Found existing scenario, updating...")
        active_games = db.query(Game).filter(
            Game.scenario_id == scenario.id,
            Game.current_phase_id.isnot(None)
        ).all()
        
        for game in active_games:
            print(f"Clearing current_phase_id from game {game.id}")
            game.current_phase_id = None
            game.phase_state = "not_started"
        
        db.flush()
        
        # Get existing phases sorted by order_index
        existing_phases = sorted(scenario.phases, key=lambda p: p.order_index)
        
        # Phase data for the new scenario
        phase_data = [
            {
                "name": "Phase 1: Initial Compromise",
                "briefing_text": "At 08:15 AM, a user in the Finance department reported receiving a suspicious email. The email appeared to be from a legitimate vendor but contained a link to an external domain. The user clicked the link and downloaded what appeared to be an invoice PDF. Within minutes, the endpoint detection system flagged unusual process activity on the user's workstation (WS-FIN-042). Initial analysis shows a PowerShell script executed with encoded commands. The security team needs to determine the scope of the initial compromise and prevent further spread.",
                "red_objective": "Successfully establish initial access on the compromised workstation without triggering alerts. Begin reconnaissance to identify network topology, user accounts, and system configurations. Avoid detection by security tools.",
                "blue_objective": "Identify the initial entry point and contain the threat. Determine what malware was downloaded and executed. Isolate the compromised workstation to prevent lateral movement. Collect forensic evidence for analysis.",
                "default_duration_seconds": 900,
            },
            {
                "name": "Phase 2: Establishing Foothold",
                "briefing_text": "The attacker has successfully established a foothold on the initial system. Security monitoring shows the malware has created scheduled tasks for persistence and is actively scanning the internal network. Network traffic analysis reveals connections to an external C2 server (185.220.101.45) and internal scanning activity targeting port 445 (SMB) and 3389 (RDP) on multiple systems. The SIEM has generated alerts for unusual network activity from WS-FIN-042. The attacker appears to be mapping the network and identifying potential targets.",
                "red_objective": "Establish multiple persistence mechanisms (scheduled tasks, registry keys, service creation). Map the network topology and identify high-value targets (domain controllers, file servers, backup systems). Maintain C2 communication while evading detection. Identify user accounts with elevated privileges.",
                "blue_objective": "Detect and remove persistence mechanisms. Identify all systems the attacker has scanned or attempted to access. Block C2 communications and identify the attacker's network footprint. Determine the attacker's reconnaissance objectives and protect high-value assets.",
                "default_duration_seconds": 900,
            },
            {
                "name": "Phase 3: Privilege Escalation & Lateral Movement",
                "briefing_text": "The situation has escalated. The attacker has successfully obtained domain administrator credentials through credential harvesting and pass-the-hash techniques. Security logs show successful authentication to the domain controller (DC-01) and multiple file servers (FS-01, FS-02). The attacker has moved laterally to systems containing sensitive data including customer PII, financial records, and intellectual property. Backup systems (BACKUP-01) have also been accessed. The attacker is now in a position to access critical systems and data.",
                "red_objective": "Successfully escalate to domain administrator privileges. Move laterally to critical systems including domain controllers, file servers, and backup systems. Maintain access to multiple systems to ensure redundancy. Identify and catalog sensitive data for exfiltration. Avoid detection while moving through the network.",
                "blue_objective": "Detect privilege escalation attempts and successful lateral movement. Isolate critical systems (domain controllers, file servers, backups) from the compromised network segment. Revoke compromised credentials and force password resets. Prevent access to backup systems to preserve recovery options. Document the attacker's movement for forensic analysis.",
                "default_duration_seconds": 900,
            },
            {
                "name": "Phase 4: Data Exfiltration",
                "briefing_text": "Network monitoring has detected large-scale data transfers from internal file servers to external IP addresses. Analysis shows approximately 450 GB of data has been exfiltrated over the past 6 hours, including customer databases, financial records, employee PII, and proprietary research data. The data is being transferred to cloud storage services (Mega.nz, Dropbox) using encrypted connections. The attacker appears to be preparing for the final phase of the attack. Meanwhile, security teams have been working to contain the threat, but the attacker maintains access through multiple persistence mechanisms.",
                "red_objective": "Complete exfiltration of sensitive data including customer databases, financial records, and intellectual property. Maintain access to critical systems. Prepare for ransomware deployment by identifying encryption targets. Ensure data exfiltration completes before detection. Preserve access for post-encryption activities.",
                "blue_objective": "Detect and stop ongoing data exfiltration. Block external data transfers and identify what data has been stolen. Preserve forensic evidence of the exfiltration. Notify legal and compliance teams about potential data breach. Assess regulatory requirements (GDPR, CCPA) for breach notification. Prepare incident response communications.",
                "default_duration_seconds": 900,
            },
            {
                "name": "Phase 5: Ransomware Deployment & Response",
                "briefing_text": "The attack has reached its final stage. At 14:30, ransomware (identified as LockBit 3.0 variant) began encrypting systems across the network. Over 200 systems have been encrypted including file servers, application servers, and workstations. A ransom note has been displayed on affected systems demanding 50 Bitcoin (approximately $1.2M USD) for decryption keys and a promise not to publish stolen data. Critical business systems are offline. The backup system (BACKUP-01) was also encrypted, but offsite backups from 36 hours ago remain intact. The organization must decide on response strategy while business operations are severely impacted.",
                "red_objective": "Successfully deploy ransomware across critical systems. Ensure encryption of file servers, databases, and backup systems. Deliver ransom note and establish communication channel for negotiation. Maintain access to monitor victim response. Prepare to publish stolen data if ransom is not paid within deadline (72 hours).",
                "blue_objective": "Contain the spread of encryption to prevent further system compromise. Assess the scope of encrypted systems and data loss. Evaluate backup integrity and recovery options. Determine if decryption is possible without paying ransom. Coordinate with law enforcement and incident response partners. Make decision on ransom payment considering business impact, legal implications, and likelihood of recovery. Initiate recovery procedures if backups are viable.",
                "default_duration_seconds": 1200,
            },
        ]
        
        # Update existing phases or create new ones
        phases = []
        for i, phase_info in enumerate(phase_data):
            if i < len(existing_phases):
                # Update existing phase
                phase = existing_phases[i]
                phase.order_index = i
                phase.name = phase_info["name"]
                phase.briefing_text = phase_info["briefing_text"]
                phase.red_objective = phase_info["red_objective"]
                phase.blue_objective = phase_info["blue_objective"]
                phase.default_duration_seconds = phase_info["default_duration_seconds"]
                phases.append(phase)
                print(f"Updated phase {i+1}: {phase.name}")
            else:
                # Create new phase
                phase = ScenarioPhase(
                    scenario_id=scenario.id,
                    order_index=i,
                    name=phase_info["name"],
                    briefing_text=phase_info["briefing_text"],
                    red_objective=phase_info["red_objective"],
                    blue_objective=phase_info["blue_objective"],
                    default_duration_seconds=phase_info["default_duration_seconds"],
                    miro_frame_url=f"https://miro.com/app/board/example/frame{i+1}"
                )
                db.add(phase)
                db.flush()
                phases.append(phase)
                print(f"Created phase {i+1}: {phase.name}")
        
        # Remove artifact associations from all phases
        for phase in phases:
            db.execute(
                scenario_phase_artifacts.delete().where(
                    scenario_phase_artifacts.c.phase_id == phase.id
                )
            )
        
        db.flush()
        
        # Update scenario description
        scenario.description = "A realistic multi-phase ransomware attack scenario based on real-world tactics. The attack follows the typical kill chain: initial access through phishing, establishing persistence, privilege escalation, data exfiltration, and finally ransomware deployment."
    else:
        # Create new scenario
        scenario = Scenario(
            name="Ransomware Incident Response",
            description="A realistic multi-phase ransomware attack scenario based on real-world tactics. The attack follows the typical kill chain: initial access through phishing, establishing persistence, privilege escalation, data exfiltration, and finally ransomware deployment.",
            miro_board_url="https://miro.com/app/board/example"
        )
        db.add(scenario)
        db.flush()
        print("Created new scenario")

        # Create phases (only if scenario is new)
        phase1 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=0,
            name="Phase 1: Initial Compromise",
            briefing_text="At 08:15 AM, a user in the Finance department reported receiving a suspicious email. The email appeared to be from a legitimate vendor but contained a link to an external domain. The user clicked the link and downloaded what appeared to be an invoice PDF. Within minutes, the endpoint detection system flagged unusual process activity on the user's workstation (WS-FIN-042). Initial analysis shows a PowerShell script executed with encoded commands. The security team needs to determine the scope of the initial compromise and prevent further spread.",
            red_objective="Successfully establish initial access on the compromised workstation without triggering alerts. Begin reconnaissance to identify network topology, user accounts, and system configurations. Avoid detection by security tools.",
            blue_objective="Identify the initial entry point and contain the threat. Determine what malware was downloaded and executed. Isolate the compromised workstation to prevent lateral movement. Collect forensic evidence for analysis.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame1"
        )
        db.add(phase1)
        db.flush()

        phase2 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=1,
            name="Phase 2: Establishing Foothold",
            briefing_text="The attacker has successfully established a foothold on the initial system. Security monitoring shows the malware has created scheduled tasks for persistence and is actively scanning the internal network. Network traffic analysis reveals connections to an external C2 server (185.220.101.45) and internal scanning activity targeting port 445 (SMB) and 3389 (RDP) on multiple systems. The SIEM has generated alerts for unusual network activity from WS-FIN-042. The attacker appears to be mapping the network and identifying potential targets.",
            red_objective="Establish multiple persistence mechanisms (scheduled tasks, registry keys, service creation). Map the network topology and identify high-value targets (domain controllers, file servers, backup systems). Maintain C2 communication while evading detection. Identify user accounts with elevated privileges.",
            blue_objective="Detect and remove persistence mechanisms. Identify all systems the attacker has scanned or attempted to access. Block C2 communications and identify the attacker's network footprint. Determine the attacker's reconnaissance objectives and protect high-value assets.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame2"
        )
        db.add(phase2)
        db.flush()

        phase3 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=2,
            name="Phase 3: Privilege Escalation & Lateral Movement",
            briefing_text="The situation has escalated. The attacker has successfully obtained domain administrator credentials through credential harvesting and pass-the-hash techniques. Security logs show successful authentication to the domain controller (DC-01) and multiple file servers (FS-01, FS-02). The attacker has moved laterally to systems containing sensitive data including customer PII, financial records, and intellectual property. Backup systems (BACKUP-01) have also been accessed. The attacker is now in a position to access critical systems and data.",
            red_objective="Successfully escalate to domain administrator privileges. Move laterally to critical systems including domain controllers, file servers, and backup systems. Maintain access to multiple systems to ensure redundancy. Identify and catalog sensitive data for exfiltration. Avoid detection while moving through the network.",
            blue_objective="Detect privilege escalation attempts and successful lateral movement. Isolate critical systems (domain controllers, file servers, backups) from the compromised network segment. Revoke compromised credentials and force password resets. Prevent access to backup systems to preserve recovery options. Document the attacker's movement for forensic analysis.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame3"
        )
        db.add(phase3)
        db.flush()

        phase4 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=3,
            name="Phase 4: Data Exfiltration",
            briefing_text="Network monitoring has detected large-scale data transfers from internal file servers to external IP addresses. Analysis shows approximately 450 GB of data has been exfiltrated over the past 6 hours, including customer databases, financial records, employee PII, and proprietary research data. The data is being transferred to cloud storage services (Mega.nz, Dropbox) using encrypted connections. The attacker appears to be preparing for the final phase of the attack. Meanwhile, security teams have been working to contain the threat, but the attacker maintains access through multiple persistence mechanisms.",
            red_objective="Complete exfiltration of sensitive data including customer databases, financial records, and intellectual property. Maintain access to critical systems. Prepare for ransomware deployment by identifying encryption targets. Ensure data exfiltration completes before detection. Preserve access for post-encryption activities.",
            blue_objective="Detect and stop ongoing data exfiltration. Block external data transfers and identify what data has been stolen. Preserve forensic evidence of the exfiltration. Notify legal and compliance teams about potential data breach. Assess regulatory requirements (GDPR, CCPA) for breach notification. Prepare incident response communications.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame4"
        )
        db.add(phase4)
        db.flush()

        phase5 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=4,
            name="Phase 5: Ransomware Deployment & Response",
            briefing_text="The attack has reached its final stage. At 14:30, ransomware (identified as LockBit 3.0 variant) began encrypting systems across the network. Over 200 systems have been encrypted including file servers, application servers, and workstations. A ransom note has been displayed on affected systems demanding 50 Bitcoin (approximately $1.2M USD) for decryption keys and a promise not to publish stolen data. Critical business systems are offline. The backup system (BACKUP-01) was also encrypted, but offsite backups from 36 hours ago remain intact. The organization must decide on response strategy while business operations are severely impacted.",
            red_objective="Successfully deploy ransomware across critical systems. Ensure encryption of file servers, databases, and backup systems. Deliver ransom note and establish communication channel for negotiation. Maintain access to monitor victim response. Prepare to publish stolen data if ransom is not paid within deadline (72 hours).",
            blue_objective="Contain the spread of encryption to prevent further system compromise. Assess the scope of encrypted systems and data loss. Evaluate backup integrity and recovery options. Determine if decryption is possible without paying ransom. Coordinate with law enforcement and incident response partners. Make decision on ransom payment considering business impact, legal implications, and likelihood of recovery. Initiate recovery procedures if backups are viable.",
            default_duration_seconds=1200,
            miro_frame_url="https://miro.com/app/board/example/frame5"
        )
        db.add(phase5)
        db.flush()
        
        phases = [phase1, phase2, phase3, phase4, phase5]

    # Create or update artifacts
    artifacts_data = [
        {
            "name": "Phishing Email Screenshot",
            "type": ArtifactType.EMAIL,
            "description": "Screenshot of the phishing email received by Finance user. Email appears to be from 'vendor-support@legitmate-vendor.com' (note the typo: 'legitmate' instead of 'legitimate'). Subject: 'URGENT: Invoice Payment Required - Action Needed'. Contains link to external domain 'secure-invoice-download[.]tk'.",
            "file_url": "/api/artifacts/files/phishing_email_phase1.png",
            "notes_for_gm": "Classic phishing email with typosquatting domain. Shows urgency tactics. Upload screenshot of realistic phishing email."
        },
        {
            "name": "EDR Alert: Suspicious PowerShell Execution",
            "type": ArtifactType.LOG_SNIPPET,
            "description": "Endpoint Detection and Response alert from WS-FIN-042 showing PowerShell execution with encoded commands. Process: powershell.exe -EncodedCommand [base64 string]. Parent process: mshta.exe. Timestamp: 08:17:23. File hash: 7a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c",
            "file_url": "/api/artifacts/files/edr_alert_phase1.txt",
            "notes_for_gm": "EDR log showing encoded PowerShell execution. Should show suspicious process tree."
        },
        {
            "name": "Network Scan Results",
            "type": ArtifactType.TOOL_OUTPUT,
            "description": "Nmap scan output showing internal network reconnaissance. Scans originated from WS-FIN-042 targeting 192.168.0.0/24 subnet. Shows open ports 445 (SMB), 3389 (RDP), 5985 (WinRM) on multiple systems. Identified targets include DC-01, FS-01, FS-02, BACKUP-01.",
            "file_url": "/api/artifacts/files/nmap_scan_phase2.txt",
            "notes_for_gm": "Network scan output showing internal reconnaissance. Should show port scans and identified systems."
        },
        {
            "name": "C2 Traffic Analysis",
            "type": ArtifactType.LOG_SNIPPET,
            "description": "Network traffic logs showing communication with C2 server 185.220.101.45. Connections established on port 443 (HTTPS) with unusual patterns: long-lived connections, periodic small data transfers. DNS queries to 'update-check[.]tk' resolved to C2 IP. Traffic encrypted but shows beaconing pattern every 300 seconds.",
            "file_url": "/api/artifacts/files/c2_traffic_phase2.txt",
            "notes_for_gm": "Network logs showing C2 communication patterns. Should show beaconing behavior."
        },
        {
            "name": "Privilege Escalation Evidence",
            "type": ArtifactType.LOG_SNIPPET,
            "description": "Windows Security Event Log showing successful privilege escalation. Event ID 4624: Successful logon with domain admin credentials (DOMAIN\\svc_backup) from WS-FIN-042 to DC-01. Event ID 4672: Special privileges assigned. Followed by Event ID 5145: Network share accessed (\\DC-01\\SYSVOL). Credentials appear to have been harvested from memory dump.",
            "file_url": "/api/artifacts/files/privilege_escalation_phase3.txt",
            "notes_for_gm": "Windows event logs showing privilege escalation and lateral movement."
        },
        {
            "name": "Lateral Movement Indicators",
            "type": ArtifactType.LOG_SNIPPET,
            "description": "SIEM correlation showing lateral movement pattern. Multiple successful authentications from WS-FIN-042 to FS-01, FS-02, BACKUP-01 using pass-the-hash technique. SMB file access logs show enumeration of shared folders and access to sensitive directories including '\\FS-01\\Finance', '\\FS-02\\HR\\PII', '\\FS-01\\R&D\\Proprietary'.",
            "file_url": "/api/artifacts/files/lateral_movement_phase3.txt",
            "notes_for_gm": "Logs showing lateral movement and file access patterns."
        },
        {
            "name": "Data Exfiltration Traffic Analysis",
            "type": ArtifactType.LOG_SNIPPET,
            "description": "Network flow analysis showing large data transfers. Outbound connections from FS-01 and FS-02 to external IPs (185.220.101.45, 45.146.164.110) on port 443. Total data transferred: ~450 GB over 6 hours. Traffic patterns indicate use of cloud storage APIs (Mega.nz, Dropbox). Files transferred include .db, .xlsx, .pdf, .docx extensions. Transfer rate: ~75 GB/hour.",
            "file_url": "/api/artifacts/files/exfiltration_traffic_phase4.txt",
            "notes_for_gm": "Network logs showing data exfiltration patterns and volumes."
        },
        {
            "name": "Data Classification Report",
            "type": ArtifactType.INTEL_REPORT,
            "description": "Data classification analysis of exfiltrated data. Categories identified: Customer PII (125,000 records), Employee data (2,400 records), Financial records (Q1-Q4 financials), Intellectual property (proprietary algorithms, research data), Legal documents (contracts, NDAs). Estimated regulatory impact: GDPR violation potential, CCPA notification required, potential HIPAA implications if healthcare data included.",
            "file_url": "/api/artifacts/files/data_classification_phase4.pdf",
            "notes_for_gm": "Report showing what data was stolen and regulatory implications."
        },
        {
            "name": "Ransomware Note Screenshot",
            "type": ArtifactType.SCREENSHOT,
            "description": "Screenshot of LockBit 3.0 ransom note displayed on encrypted systems. Message: 'YOUR FILES HAVE BEEN ENCRYPTED. To decrypt your files, you must pay 50 BTC to address [Bitcoin address]. You have 72 hours to pay. After that, the price doubles. We have also exfiltrated your data. If you do not pay, we will publish it on our leak site. Contact us at: [Tor .onion address]'.",
            "file_url": "/api/artifacts/files/ransomware_note_phase5.png",
            "notes_for_gm": "Screenshot of realistic ransomware note. Should show Bitcoin address and deadline."
        },
        {
            "name": "Encryption Impact Assessment",
            "type": ArtifactType.INTEL_REPORT,
            "description": "Assessment of encrypted systems and business impact. Systems encrypted: 200+ endpoints including 15 file servers, 8 application servers, 150 workstations, backup system (BACKUP-01). Critical systems affected: ERP system (offline), email server (partial), customer portal (offline). Offsite backups from 36 hours ago are intact. Estimated recovery time: 48-72 hours if using backups, 2-3 weeks if paying ransom and receiving decryption keys. Business impact: $500K/day in lost revenue.",
            "file_url": "/api/artifacts/files/impact_assessment_phase5.pdf",
            "notes_for_gm": "Report showing business impact and recovery options."
        },
        {
            "name": "Backup System Status",
            "type": ArtifactType.TOOL_OUTPUT,
            "description": "Backup system status report. BACKUP-01 (onsite): Encrypted, last backup 2 hours before encryption. Offsite backup location: Intact, last successful backup 36 hours ago. Backup coverage: 95% of critical systems, 80% of user data. Recovery point objective (RPO): 36 hours. Recovery time objective (RTO): 48 hours if offsite backups used.",
            "file_url": "/api/artifacts/files/backup_status_phase5.txt",
            "notes_for_gm": "Backup status showing recovery options."
        },
    ]

    artifacts = []
    for art_data in artifacts_data:
        # Check if artifact exists by name
        existing = db.query(Artifact).filter(Artifact.name == art_data["name"]).first()
        if existing:
            # Update existing artifact
            existing.type = art_data["type"]
            existing.description = art_data["description"]
            existing.file_url = art_data["file_url"]
            existing.notes_for_gm = art_data["notes_for_gm"]
            artifacts.append(existing)
        else:
            # Create new artifact
            artifact = Artifact(**art_data)
            db.add(artifact)
            db.flush()
            artifacts.append(artifact)

    # Associate artifacts with phases (use the phases list)
    # Phase 1: Initial Compromise
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[0].id, artifact_id=artifacts[0].id))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[0].id, artifact_id=artifacts[1].id))

    # Phase 2: Establishing Foothold
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[1].id, artifact_id=artifacts[2].id))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[1].id, artifact_id=artifacts[3].id))

    # Phase 3: Privilege Escalation & Lateral Movement
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[2].id, artifact_id=artifacts[4].id))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[2].id, artifact_id=artifacts[5].id))

    # Phase 4: Data Exfiltration
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[3].id, artifact_id=artifacts[6].id))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[3].id, artifact_id=artifacts[7].id))

    # Phase 5: Ransomware Deployment & Response
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[4].id, artifact_id=artifacts[8].id))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[4].id, artifact_id=artifacts[9].id))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phases[4].id, artifact_id=artifacts[10].id))

    db.commit()
    print(f"Successfully migrated scenario with 5 phases and {len(artifacts)} artifacts")
    for i, phase in enumerate(phases, 1):
        print(f"Phase {i}: {phase.name}")


if __name__ == "__main__":
    try:
        migrate_scenario()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

