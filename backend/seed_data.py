"""
Seed script to populate database with initial data.
Run this after migrations: python seed_data.py
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    GMUser, Scenario, ScenarioPhase, Artifact, ArtifactType,
    scenario_phase_artifacts
)
from app.auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()


def seed_data():
    # Create GM user
    try:
        gm = db.query(GMUser).filter(GMUser.username == "admin").first()
        if not gm:
            password = "admin123"
            # Ensure password is not too long for bcrypt
            if len(password.encode('utf-8')) > 72:
                password = password[:72]
            gm = GMUser(
                username="admin",
                password_hash=get_password_hash(password)
            )
            db.add(gm)
            db.commit()
            print("Created GM user: admin / admin123")
        else:
            print("GM user already exists")
    except Exception as e:
        print(f"Error creating GM user: {e}")
        db.rollback()
        raise

    # Create scenario
    scenario = db.query(Scenario).filter(Scenario.name == "Ransomware Incident Response").first()
    if not scenario:
        scenario = Scenario(
            name="Ransomware Incident Response",
            description="A realistic multi-phase ransomware attack scenario based on real-world tactics. The attack follows the typical kill chain: initial access through phishing, establishing persistence, privilege escalation, data exfiltration, and finally ransomware deployment.",
            miro_board_url="https://miro.com/app/board/example"
        )
        db.add(scenario)
        db.flush()

        # Phase 1: Initial Compromise
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

        # Phase 2: Establishing Foothold
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

        # Phase 3: Privilege Escalation & Lateral Movement
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

        # Phase 4: Data Exfiltration
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

        # Phase 5: Ransomware Deployment & Response
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

        # Create artifacts - Phase 1
        # Blue Team Artifacts
        artifact1_blue = Artifact(
            name="Phishing Email Screenshot",
            type=ArtifactType.EMAIL,
            description="Screenshot of the phishing email received by Finance user. Email appears to be from 'vendor-support@legitmate-vendor.com' (note the typo: 'legitmate' instead of 'legitimate'). Subject: 'URGENT: Invoice Payment Required - Action Needed'. Contains link to external domain 'secure-invoice-download[.]tk'.",
            file_url="/api/artifacts/files/phishing_email_phase1.png",
            notes_for_gm="Classic phishing email with typosquatting domain. Shows urgency tactics. Upload screenshot of realistic phishing email."
        )
        db.add(artifact1_blue)
        db.flush()

        artifact2_blue = Artifact(
            name="EDR Alert: Suspicious PowerShell Execution",
            type=ArtifactType.LOG_SNIPPET,
            description="Endpoint Detection and Response alert from WS-FIN-042 showing PowerShell execution with encoded commands. Process: powershell.exe -EncodedCommand [base64 string]. Parent process: mshta.exe. Timestamp: 08:17:23. File hash: 7a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c",
            file_url="/api/artifacts/files/edr_alert_phase1.txt",
            notes_for_gm="EDR log showing encoded PowerShell execution. Should show suspicious process tree."
        )
        db.add(artifact2_blue)
        db.flush()

        # Red Team Artifacts
        artifact1_red = Artifact(
            name="Initial Access Confirmation",
            type=ArtifactType.TOOL_OUTPUT,
            description="Payload successfully executed on target workstation WS-FIN-042. User: finance.user@corp.local. Initial beacon established to C2 server 185.220.101.45. System information collected: Windows 10 Enterprise, Domain: CORP.LOCAL, User privileges: Standard User. Persistence mechanisms deployed: Scheduled task 'UpdateCheck', Registry run key. Ready for privilege escalation.",
            file_url="/api/artifacts/files/initial_access_phase1.txt",
            notes_for_gm="Red Team sees successful compromise confirmation and system info."
        )
        db.add(artifact1_red)
        db.flush()

        artifact2_red = Artifact(
            name="C2 Connection Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="C2 Communication Status: ACTIVE\nServer: 185.220.101.45:443\nBeacon Interval: 300 seconds\nLast Check-in: 08:17:25 UTC\nConnection: Stable\nEncryption: TLS 1.3\nCommands Received: Download payload, Enumerate system, Create persistence\nStatus: Operational - No detection alerts triggered",
            file_url="/api/artifacts/files/c2_status_phase1.txt",
            notes_for_gm="Red Team sees their C2 connection status and successful commands."
        )
        db.add(artifact2_red)
        db.flush()

        # Phase 2 Artifacts
        # Blue Team Artifacts
        artifact3_blue = Artifact(
            name="Network Scan Results",
            type=ArtifactType.TOOL_OUTPUT,
            description="Nmap scan output showing internal network reconnaissance. Scans originated from WS-FIN-042 targeting 192.168.0.0/24 subnet. Shows open ports 445 (SMB), 3389 (RDP), 5985 (WinRM) on multiple systems. Identified targets include DC-01, FS-01, FS-02, BACKUP-01.",
            file_url="/api/artifacts/files/nmap_scan_phase2.txt",
            notes_for_gm="Network scan output showing internal reconnaissance. Should show port scans and identified systems."
        )
        db.add(artifact3_blue)
        db.flush()

        artifact4_blue = Artifact(
            name="C2 Traffic Analysis",
            type=ArtifactType.LOG_SNIPPET,
            description="Network traffic logs showing communication with C2 server 185.220.101.45. Connections established on port 443 (HTTPS) with unusual patterns: long-lived connections, periodic small data transfers. DNS queries to 'update-check[.]tk' resolved to C2 IP. Traffic encrypted but shows beaconing pattern every 300 seconds.",
            file_url="/api/artifacts/files/c2_traffic_phase2.txt",
            notes_for_gm="Network logs showing C2 communication patterns. Should show beaconing behavior."
        )
        db.add(artifact4_blue)
        db.flush()

        # Red Team Artifacts
        artifact3_red = Artifact(
            name="Network Reconnaissance Results",
            type=ArtifactType.TOOL_OUTPUT,
            description="Network mapping completed. Discovered 4 high-value targets:\n- DC-01 (192.168.0.10): Domain Controller, ports 445/3389/5985 open\n- FS-01 (192.168.0.20): File Server, shares: Finance, R&D\n- FS-02 (192.168.0.21): File Server, shares: HR, PII\n- BACKUP-01 (192.168.0.30): Backup Server, accessible via SMB\nPersistence mechanisms verified: 3 scheduled tasks active, 2 registry keys set. C2 communication stable. Ready for privilege escalation phase.",
            file_url="/api/artifacts/files/recon_results_phase2.txt",
            notes_for_gm="Red Team sees their successful reconnaissance results."
        )
        db.add(artifact3_red)
        db.flush()

        artifact4_red = Artifact(
            name="Persistence Status Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="Persistence Mechanisms Status:\n✓ Scheduled Task: UpdateCheck (runs every 5 minutes)\n✓ Registry Run Key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\n✓ Service Creation: Attempted (requires admin)\n✓ WMI Event Subscription: Created\nAll persistence mechanisms active. System will maintain access even after reboot. No security tools detected persistence mechanisms.",
            file_url="/api/artifacts/files/persistence_status_phase2.txt",
            notes_for_gm="Red Team sees their successful persistence deployment."
        )
        db.add(artifact4_red)
        db.flush()

        # Phase 3 Artifacts
        # Blue Team Artifacts
        artifact5_blue = Artifact(
            name="Privilege Escalation Evidence",
            type=ArtifactType.LOG_SNIPPET,
            description="Windows Security Event Log showing successful privilege escalation. Event ID 4624: Successful logon with domain admin credentials (DOMAIN\\svc_backup) from WS-FIN-042 to DC-01. Event ID 4672: Special privileges assigned. Followed by Event ID 5145: Network share accessed (\\DC-01\\SYSVOL). Credentials appear to have been harvested from memory dump.",
            file_url="/api/artifacts/files/privilege_escalation_phase3.txt",
            notes_for_gm="Windows event logs showing privilege escalation and lateral movement."
        )
        db.add(artifact5_blue)
        db.flush()

        artifact6_blue = Artifact(
            name="Lateral Movement Indicators",
            type=ArtifactType.LOG_SNIPPET,
            description="SIEM correlation showing lateral movement pattern. Multiple successful authentications from WS-FIN-042 to FS-01, FS-02, BACKUP-01 using pass-the-hash technique. SMB file access logs show enumeration of shared folders and access to sensitive directories including '\\FS-01\\Finance', '\\FS-02\\HR\\PII', '\\FS-01\\R&D\\Proprietary'.",
            file_url="/api/artifacts/files/lateral_movement_phase3.txt",
            notes_for_gm="Logs showing lateral movement and file access patterns."
        )
        db.add(artifact6_blue)
        db.flush()

        # Red Team Artifacts
        artifact5_red = Artifact(
            name="Credential Harvesting Success",
            type=ArtifactType.TOOL_OUTPUT,
            description="Credential Harvesting Report:\n✓ Domain Admin Credentials Obtained: CORP\\svc_backup\nMethod: Memory dump (lsass.exe)\nTechnique: Pass-the-Hash\nPrivileges: Domain Admin, Backup Operator, Local Admin on all systems\nAccess Verified:\n  - DC-01: SUCCESS (Domain Controller access)\n  - FS-01: SUCCESS (File server access)\n  - FS-02: SUCCESS (File server access)\n  - BACKUP-01: SUCCESS (Backup system access)\nAll target systems accessible. Ready for data collection phase.",
            file_url="/api/artifacts/files/credential_success_phase3.txt",
            notes_for_gm="Red Team sees their successful credential harvesting."
        )
        db.add(artifact5_red)
        db.flush()

        artifact6_red = Artifact(
            name="Lateral Movement Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Lateral Movement Status Report:\nSystems Compromised:\n1. DC-01: Domain Controller - FULL ACCESS\n   - SYSVOL accessed\n   - Group Policy enumeration complete\n2. FS-01: File Server - FULL ACCESS\n   - Finance share: 1,234 files enumerated\n   - R&D share: 156 files enumerated\n3. FS-02: File Server - FULL ACCESS\n   - HR share: 856 files enumerated\n   - PII directory: 342 files enumerated\n4. BACKUP-01: Backup Server - FULL ACCESS\n   - Backup catalog accessed\n   - 2,109 backup files identified\nAll critical systems under control. No detection alerts.",
            file_url="/api/artifacts/files/lateral_status_phase3.txt",
            notes_for_gm="Red Team sees their successful lateral movement."
        )
        db.add(artifact6_red)
        db.flush()

        # Phase 4 Artifacts
        # Blue Team Artifacts
        artifact7_blue = Artifact(
            name="Data Exfiltration Traffic Analysis",
            type=ArtifactType.LOG_SNIPPET,
            description="Network flow analysis showing large data transfers. Outbound connections from FS-01 and FS-02 to external IPs (185.220.101.45, 45.146.164.110) on port 443. Total data transferred: ~450 GB over 6 hours. Traffic patterns indicate use of cloud storage APIs (Mega.nz, Dropbox). Files transferred include .db, .xlsx, .pdf, .docx extensions. Transfer rate: ~75 GB/hour.",
            file_url="/api/artifacts/files/exfiltration_traffic_phase4.txt",
            notes_for_gm="Network logs showing data exfiltration patterns and volumes."
        )
        db.add(artifact7_blue)
        db.flush()

        artifact8_blue = Artifact(
            name="Data Classification Report",
            type=ArtifactType.INTEL_REPORT,
            description="Data classification analysis of exfiltrated data. Categories identified: Customer PII (125,000 records), Employee data (2,400 records), Financial records (Q1-Q4 financials), Intellectual property (proprietary algorithms, research data), Legal documents (contracts, NDAs). Estimated regulatory impact: GDPR violation potential, CCPA notification required, potential HIPAA implications if healthcare data included.",
            file_url="/api/artifacts/files/data_classification_phase4.pdf",
            notes_for_gm="Report showing what data was stolen and regulatory implications."
        )
        db.add(artifact8_blue)
        db.flush()

        # Red Team Artifacts
        artifact7_red = Artifact(
            name="Data Exfiltration Progress",
            type=ArtifactType.TOOL_OUTPUT,
            description="Data Exfiltration Status: IN PROGRESS\n\nTarget Systems:\n- FS-01: 270 GB transferred (60% complete)\n- FS-02: 180 GB transferred (100% complete)\n\nData Categories Collected:\n✓ Customer Databases: 45 GB (125,000 records)\n✓ Financial Records: 120 GB (Q1-Q4 2023, Q1 2024)\n✓ Employee PII: 8.2 GB (2,400 records)\n✓ Intellectual Property: 105 GB (algorithms, research)\n✓ Legal Documents: 85 GB (contracts, NDAs)\n\nUpload Status:\n- Mega.nz: 270 GB uploaded\n- Dropbox: 180 GB uploaded\nTotal: 450 GB / 450 GB (100%)\n\nExfiltration complete. Ready for encryption phase.",
            file_url="/api/artifacts/files/exfiltration_progress_phase4.txt",
            notes_for_gm="Red Team sees their exfiltration progress and success."
        )
        db.add(artifact7_red)
        db.flush()

        artifact8_red = Artifact(
            name="Stolen Data Inventory",
            type=ArtifactType.INTEL_REPORT,
            description="Stolen Data Inventory:\n\nHigh-Value Data:\n- Customer PII: 125,000 records (estimated value: $50/record = $6.25M)\n- Financial Records: Complete Q1-Q4 2023, Q1 2024\n- Employee Data: 2,400 records with SSNs, salaries\n- Intellectual Property: Proprietary algorithms, research data\n- Legal Documents: Contracts, NDAs, compliance records\n\nTotal Data Value: $50+ million\nLeverage: High - can threaten publication if ransom not paid\nStatus: All data successfully exfiltrated and verified",
            file_url="/api/artifacts/files/stolen_data_inventory_phase4.txt",
            notes_for_gm="Red Team sees their inventory of stolen data."
        )
        db.add(artifact8_red)
        db.flush()

        # Phase 5 Artifacts
        # Blue Team Artifacts
        artifact9_blue = Artifact(
            name="Ransomware Note Screenshot",
            type=ArtifactType.SCREENSHOT,
            description="Screenshot of LockBit 3.0 ransom note displayed on encrypted systems. Message: 'YOUR FILES HAVE BEEN ENCRYPTED. To decrypt your files, you must pay 50 BTC to address [Bitcoin address]. You have 72 hours to pay. After that, the price doubles. We have also exfiltrated your data. If you do not pay, we will publish it on our leak site. Contact us at: [Tor .onion address]'.",
            file_url="/api/artifacts/files/ransomware_note_phase5.png",
            notes_for_gm="Screenshot of realistic ransomware note. Should show Bitcoin address and deadline."
        )
        db.add(artifact9_blue)
        db.flush()

        artifact10_blue = Artifact(
            name="Encryption Impact Assessment",
            type=ArtifactType.INTEL_REPORT,
            description="Assessment of encrypted systems and business impact. Systems encrypted: 200+ endpoints including 15 file servers, 8 application servers, 150 workstations, backup system (BACKUP-01). Critical systems affected: ERP system (offline), email server (partial), customer portal (offline). Offsite backups from 36 hours ago are intact. Estimated recovery time: 48-72 hours if using backups, 2-3 weeks if paying ransom and receiving decryption keys. Business impact: $500K/day in lost revenue.",
            file_url="/api/artifacts/files/impact_assessment_phase5.pdf",
            notes_for_gm="Report showing business impact and recovery options."
        )
        db.add(artifact10_blue)
        db.flush()

        artifact11_blue = Artifact(
            name="Backup System Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Backup system status report. BACKUP-01 (onsite): Encrypted, last backup 2 hours before encryption. Offsite backup location: Intact, last successful backup 36 hours ago. Backup coverage: 95% of critical systems, 80% of user data. Recovery point objective (RPO): 36 hours. Recovery time objective (RTO): 48 hours if offsite backups used.",
            file_url="/api/artifacts/files/backup_status_phase5.txt",
            notes_for_gm="Backup status showing recovery options."
        )
        db.add(artifact11_blue)
        db.flush()

        # Red Team Artifacts
        artifact9_red = Artifact(
            name="Encryption Deployment Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Ransomware Deployment Status: SUCCESS\n\nSystems Encrypted:\n✓ File Servers: 15/15 (100%)\n✓ Application Servers: 8/8 (100%)\n✓ Workstations: 150/150 (100%)\n✓ Backup System: BACKUP-01 (ENCRYPTED)\n✓ Domain Controllers: 2/2 (100%)\n\nTotal Systems Encrypted: 200+\nEncryption Rate: 100%\nRansom Note Deployed: YES\nBitcoin Address: [REDACTED]\nDeadline: 72 hours from deployment\n\nAll critical systems encrypted. Victim has no access to backups. Maximum leverage achieved.",
            file_url="/api/artifacts/files/encryption_status_phase5.txt",
            notes_for_gm="Red Team sees their successful encryption deployment."
        )
        db.add(artifact9_red)
        db.flush()

        artifact10_red = Artifact(
            name="Negotiation Status",
            type=ArtifactType.INTEL_REPORT,
            description="Ransom Negotiation Status:\n\nDemand: 50 BTC (~$1.2M USD)\nDeadline: 72 hours\nCommunication Channel: Tor .onion address\n\nVictim Response:\n- Initial contact: PENDING\n- Counter-offer: PENDING\n- Payment status: PENDING\n\nLeverage Points:\n✓ All systems encrypted\n✓ Backups encrypted\n✓ Data exfiltrated (450 GB)\n✓ Business operations halted\n✓ Data publication threat available\n\nStatus: Waiting for victim response. Ready to negotiate or publish data.",
            file_url="/api/artifacts/files/negotiation_status_phase5.txt",
            notes_for_gm="Red Team sees their negotiation position."
        )
        db.add(artifact10_red)
        db.flush()

        artifact11_red = Artifact(
            name="Attack Summary Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="Attack Summary - Mission Accomplished\n\nTimeline:\n- Initial Access: 08:15 UTC (Phishing)\n- Persistence: 08:17 UTC (Scheduled tasks)\n- Privilege Escalation: 10:45 UTC (Domain admin)\n- Lateral Movement: 10:46-11:30 UTC (4 systems)\n- Data Exfiltration: 11:00-17:00 UTC (450 GB)\n- Encryption: 14:30 UTC (200+ systems)\n\nResults:\n✓ 200+ systems encrypted\n✓ 450 GB data exfiltrated\n✓ All backups encrypted\n✓ Business operations halted\n✓ Maximum leverage achieved\n\nStatus: Awaiting ransom payment or data publication decision.",
            file_url="/api/artifacts/files/attack_summary_phase5.txt",
            notes_for_gm="Red Team sees their complete attack summary."
        )
        db.add(artifact11_red)
        db.flush()

        # Associate artifacts with phases and team roles
        # Phase 1: Initial Compromise
        # Blue Team sees: phishing email and EDR alert
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_blue.id, team_role="blue"))
        # Red Team sees: access confirmation and C2 status
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_red.id, team_role="red"))

        # Phase 2: Establishing Foothold
        # Blue Team sees: network scan and C2 traffic analysis
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact3_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_blue.id, team_role="blue"))
        # Red Team sees: recon results and persistence status
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact3_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_red.id, team_role="red"))

        # Phase 3: Privilege Escalation & Lateral Movement
        # Blue Team sees: privilege escalation logs and lateral movement indicators
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_blue.id, team_role="blue"))
        # Red Team sees: credential success and lateral movement status
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_red.id, team_role="red"))

        # Phase 4: Data Exfiltration
        # Blue Team sees: exfiltration traffic analysis and data classification
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_blue.id, team_role="blue"))
        # Red Team sees: exfiltration progress and stolen data inventory
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_red.id, team_role="red"))

        # Phase 5: Ransomware Deployment & Response
        # Blue Team sees: ransom note, impact assessment, and backup status
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact9_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact10_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact11_blue.id, team_role="blue"))
        # Red Team sees: encryption status, negotiation status, and attack summary
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact9_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact10_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact11_red.id, team_role="red"))

        db.commit()
        print("Created scenario with 5 phases and 22 artifacts (11 per team)")
    else:
        print("Scenario already exists")

    # Create Email Bomb & Social Engineering scenario
    scenario2 = db.query(Scenario).filter(Scenario.name == "Email Bomb & Social Engineering Attack").first()
    if not scenario2:
        scenario2 = Scenario(
            name="Email Bomb & Social Engineering Attack",
            description="A sophisticated social engineering attack combining email bombing with IT support impersonation. The attacker floods the target's inbox with thousands of emails, then calls posing as IT support to 'help' resolve the issue. This creates urgency and trust, allowing the attacker to harvest credentials and gain unauthorized access to sensitive systems and data.",
            miro_board_url="https://miro.com/app/board/example2"
        )
        db.add(scenario2)
        db.flush()

        # Phase 1: Email Bomb Deployment
        phase1_eb = ScenarioPhase(
            scenario_id=scenario2.id,
            order_index=0,
            name="Phase 1: Email Bomb Deployment",
            briefing_text="At 09:15 AM, a senior executive's inbox began receiving an unusually high volume of emails. Within 30 minutes, over 8,000 emails flooded the inbox, rendering it nearly unusable. The emails appear to be from various sources - newsletters, marketing campaigns, subscription confirmations - but analysis shows they're all originating from a coordinated attack infrastructure. The executive cannot access critical emails, and the email system is experiencing performance degradation. Meanwhile, security monitoring has detected the unusual email volume spike.",
            red_objective="Successfully deploy email bomb attack to overwhelm target inbox. Ensure emails appear legitimate and diverse to avoid immediate spam filtering. Monitor delivery success rate. Create sense of urgency and confusion. Prepare for follow-up social engineering call by researching target's IT support procedures and contact information.",
            blue_objective="Detect the email bomb attack early through volume monitoring and pattern analysis. Identify the attack infrastructure and email sources. Alert the target user before they fall for social engineering. Implement email filtering rules to block further emails. Document the attack for security awareness training.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example2/frame1"
        )
        db.add(phase1_eb)
        db.flush()

        # Phase 2: Social Engineering Call (IT Support Impersonation)
        phase2_eb = ScenarioPhase(
            scenario_id=scenario2.id,
            order_index=1,
            name="Phase 2: Social Engineering Call",
            briefing_text="At 09:45 AM, just 30 minutes after the email bomb began, the executive received a phone call from someone claiming to be from IT Support. The caller identified themselves as 'Mike from IT' and said they noticed the email issue affecting the executive's account. They offered to help resolve it immediately. The caller sounded professional, referenced the email problem, and asked the executive to verify their identity by providing their username. Security logs show no legitimate IT support ticket was created for this issue, and the phone number doesn't match known IT support contacts.",
            red_objective="Successfully impersonate IT support and establish trust with the target. Use the email bomb as pretext to create urgency. Guide the target to a fake support portal or credential entry page. Maintain professional demeanor and follow established IT support procedures to appear legitimate. Avoid raising suspicion while gathering information.",
            blue_objective="Detect the suspicious support call through monitoring and user reporting. Verify that no legitimate IT support ticket exists. Identify social engineering indicators (urgency, unsolicited contact, credential requests). Alert the user before they provide credentials. Document the social engineering attempt for security awareness.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example2/frame2"
        )
        db.add(phase2_eb)
        db.flush()

        # Phase 3: Credential Harvesting
        phase3_eb = ScenarioPhase(
            scenario_id=scenario2.id,
            order_index=2,
            name="Phase 3: Credential Harvesting",
            briefing_text="The executive, frustrated with the email issue and trusting the 'IT support' caller, followed instructions to access a 'secure support portal' at support-corp-help[.]tk. The portal requested the executive's corporate username and password to 'verify identity and restore email access.' The executive provided credentials. Security monitoring now shows authentication attempts from an unknown IP address (203.0.113.45) using the executive's credentials. The fake support portal has logged the credentials and the attacker is testing them against various corporate systems.",
            red_objective="Successfully harvest credentials through the fake support portal. Verify credentials work against corporate systems. Test access to email, file shares, and other resources. Establish persistence mechanisms if possible. Avoid triggering security alerts while testing credentials.",
            blue_objective="Detect credential compromise through authentication monitoring and anomaly detection. Identify failed login attempts from suspicious IPs. Detect password change or reset attempts. Immediately force password reset and revoke all active sessions. Investigate the fake support portal and block access. Alert the user about credential compromise.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example2/frame3"
        )
        db.add(phase3_eb)
        db.flush()

        # Phase 4: Initial Access & Privilege Escalation
        phase4_eb = ScenarioPhase(
            scenario_id=scenario2.id,
            order_index=3,
            name="Phase 4: Initial Access & Privilege Escalation",
            briefing_text="The attacker has successfully logged into the executive's email account from IP address 203.0.113.45. Security logs show the attacker is accessing sensitive emails, including confidential business communications, financial reports, and customer data. The attacker is also attempting to access file shares and attempting to escalate privileges by searching for administrator credentials in emails. The executive's account has access to several critical systems including customer relationship management (CRM) and financial systems. The attacker appears to be mapping the executive's access and identifying high-value targets.",
            red_objective="Successfully access the compromised email account and other systems. Search emails for sensitive information, credentials, and access details. Attempt to escalate privileges by finding administrator credentials or access methods. Map the executive's access to critical systems. Identify valuable data for exfiltration. Avoid detection while exploring systems.",
            blue_objective="Detect unauthorized access to the executive's account. Identify what systems and data the attacker has accessed. Revoke compromised credentials and force password reset. Isolate the compromised account from critical systems. Monitor for privilege escalation attempts. Document the attacker's access for forensic analysis.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example2/frame4"
        )
        db.add(phase4_eb)
        db.flush()

        # Phase 5: Lateral Movement & Data Exfiltration
        phase5_eb = ScenarioPhase(
            scenario_id=scenario2.id,
            order_index=4,
            name="Phase 5: Lateral Movement & Data Exfiltration",
            briefing_text="The situation has escalated significantly. The attacker has used the executive's credentials to access multiple systems including the CRM database, financial records, and customer data. Network monitoring shows the attacker is moving laterally to other systems and exfiltrating data. Analysis indicates approximately 2.5 GB of sensitive data has been transferred to external servers, including customer PII, financial records, and confidential business communications. The attacker is also attempting to maintain persistent access by creating forwarding rules in the executive's email and accessing backup systems. Security teams are working to contain the breach, but the attacker maintains access through the compromised credentials.",
            red_objective="Successfully move laterally to critical systems using the executive's access. Access and exfiltrate sensitive data including customer information, financial records, and business intelligence. Create persistence mechanisms (email forwarding, backup access) to maintain access. Exfiltrate data before detection. Cover tracks by deleting logs and evidence where possible.",
            blue_objective="Detect lateral movement and data exfiltration through network monitoring and access logs. Identify what data has been accessed and exfiltrated. Block ongoing exfiltration attempts. Revoke all compromised credentials and reset passwords. Remove persistence mechanisms (email forwarding rules, etc.). Assess data loss for compliance reporting (GDPR, CCPA). Prepare breach notification if required.",
            default_duration_seconds=1200,
            miro_frame_url="https://miro.com/app/board/example2/frame5"
        )
        db.add(phase5_eb)
        db.flush()

        # Create artifacts for Email Bomb scenario
        # Phase 1 Artifacts
        # Blue Team Artifacts
        artifact1_blue_eb = Artifact(
            name="Email Server Volume Alert",
            type=ArtifactType.LOG_SNIPPET,
            description="Email server monitoring alert showing massive volume spike. User: executive@corp.local received 8,247 emails in 30 minutes. Normal baseline: 50-100 emails/day. Emails from 200+ different domains, all appearing to be legitimate newsletters and marketing emails. Server performance degraded. Pattern suggests coordinated email bomb attack.",
            file_url="/api/artifacts/files/email_volume_alert_phase1.txt",
            notes_for_gm="Email server log showing volume spike and pattern analysis."
        )
        db.add(artifact1_blue_eb)
        db.flush()

        artifact2_blue_eb = Artifact(
            name="Email Header Analysis",
            type=ArtifactType.TOOL_OUTPUT,
            description="Analysis of email headers from the email bomb. All emails contain similar patterns: X-Originating-IP addresses from cloud hosting providers (AWS, Azure), SPF records show 'softfail' or 'neutral', DKIM signatures missing or invalid. Email subjects are diverse (newsletters, confirmations, marketing) but all sent within 30-minute window. Sender addresses appear legitimate but domains are newly registered or compromised.",
            file_url="/api/artifacts/files/email_header_analysis_phase1.txt",
            notes_for_gm="Email header analysis showing attack infrastructure."
        )
        db.add(artifact2_blue_eb)
        db.flush()

        # Red Team Artifacts
        artifact1_red_eb = Artifact(
            name="Email Bomb Deployment Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Email Bomb Deployment Report:\nTarget: executive@corp.local\nEmails Sent: 8,247\nDelivery Success Rate: 94.2%\nTime Window: 30 minutes\nEmail Types: Newsletters (45%), Marketing (30%), Confirmations (15%), Other (10%)\nInfrastructure: 200+ sending domains, cloud hosting providers\nStatus: SUCCESS - Target inbox overwhelmed\nNext Step: Initiate support call within 30-60 minutes",
            file_url="/api/artifacts/files/email_bomb_status_phase1.txt",
            notes_for_gm="Red Team sees their successful email bomb deployment."
        )
        db.add(artifact1_red_eb)
        db.flush()

        artifact2_red_eb = Artifact(
            name="Target Research & Call Script",
            type=ArtifactType.INTEL_REPORT,
            description="Target Research Summary:\nTarget: Senior Executive\nRole: VP of Operations\nIT Support Contact: Internal helpdesk (ext. 5555)\nSupport Hours: 8 AM - 6 PM EST\nSupport Portal: support.corp.local\nCall Script Prepared:\n- Identify as 'Mike from IT Support'\n- Reference email issue\n- Offer immediate assistance\n- Guide to support portal\nStatus: Ready for Phase 2",
            file_url="/api/artifacts/files/call_script_phase1.txt",
            notes_for_gm="Red Team sees their research and call script."
        )
        db.add(artifact2_red_eb)
        db.flush()

        # Phase 2 Artifacts
        # Blue Team Artifacts
        artifact3_blue_eb = Artifact(
            name="Support Call Log",
            type=ArtifactType.LOG_SNIPPET,
            description="Phone system log showing incoming call to executive's extension. Caller ID: +1-555-0123 (not in known IT support contact list). Call duration: 12 minutes. Call recorded. Transcript shows caller identified as 'Mike from IT Support', referenced email issue, asked user to verify identity. No legitimate IT support ticket exists for this issue. Security team notified.",
            file_url="/api/artifacts/files/support_call_log_phase2.txt",
            notes_for_gm="Phone system log showing suspicious support call."
        )
        db.add(artifact3_blue_eb)
        db.flush()

        artifact4_blue_eb = Artifact(
            name="Social Engineering Indicators Report",
            type=ArtifactType.INTEL_REPORT,
            description="Social Engineering Analysis:\nIndicators:\n- Unsolicited contact (no ticket)\n- Urgency created (email issue)\n- Identity verification request\n- Caller ID doesn't match IT support\n- Timing suspicious (30 min after email bomb)\nRisk Level: HIGH\nRecommendation: Alert user immediately, verify no credentials provided",
            file_url="/api/artifacts/files/se_indicators_phase2.txt",
            notes_for_gm="Social engineering detection report."
        )
        db.add(artifact4_blue_eb)
        db.flush()

        # Red Team Artifacts
        artifact3_red_eb = Artifact(
            name="Support Call Success Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="Social Engineering Call Report:\nTarget: Executive\nCall Duration: 12 minutes\nOutcome: SUCCESS\nTrust Established: YES\nTarget Agreed to: Access support portal\nPortal URL Provided: support-corp-help.tk\nNext Step: Credential harvesting via portal\nStatus: Target is proceeding to portal",
            file_url="/api/artifacts/files/call_success_phase2.txt",
            notes_for_gm="Red Team sees their successful social engineering call."
        )
        db.add(artifact3_red_eb)
        db.flush()

        artifact4_red_eb = Artifact(
            name="Fake Support Portal Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Fake Support Portal Status:\nURL: support-corp-help.tk\nStatus: OPERATIONAL\nSSL Certificate: Valid (Let's Encrypt)\nDesign: Matches corporate IT portal\nLogin Form: Active\nCredential Capture: Ready\nVisitor Tracking: Active\nStatus: Waiting for target to access portal",
            file_url="/api/artifacts/files/portal_status_phase2.txt",
            notes_for_gm="Red Team sees their fake portal status."
        )
        db.add(artifact4_red_eb)
        db.flush()

        # Phase 3 Artifacts
        # Blue Team Artifacts
        artifact5_blue_eb = Artifact(
            name="Authentication Anomaly Alert",
            type=ArtifactType.LOG_SNIPPET,
            description="Authentication monitoring alert: Multiple failed login attempts detected for executive@corp.local from IP 203.0.113.45 (unknown, not in corporate network). Attempts targeting: Email (OWA), VPN, File Shares, CRM system. Pattern suggests credential testing. User's password was changed 2 hours ago through 'support portal' - but no legitimate support ticket exists. Risk: CREDENTIALS COMPROMISED",
            file_url="/api/artifacts/files/auth_anomaly_phase3.txt",
            notes_for_gm="Authentication logs showing credential compromise."
        )
        db.add(artifact5_blue_eb)
        db.flush()

        artifact6_blue_eb = Artifact(
            name="Fake Portal Analysis",
            type=ArtifactType.INTEL_REPORT,
            description="Fake Support Portal Analysis:\nDomain: support-corp-help.tk\nRegistration: 3 days ago (newly registered)\nHosting: Cloud provider (AWS)\nSSL: Valid certificate (Let's Encrypt)\nDesign: Cloned from legitimate IT portal\nFunctionality: Captures credentials, logs all input\nAccess Logs: Show executive accessed portal\nRecommendation: Block domain, force password reset immediately",
            file_url="/api/artifacts/files/portal_analysis_phase3.txt",
            notes_for_gm="Analysis of the fake support portal."
        )
        db.add(artifact6_blue_eb)
        db.flush()

        # Red Team Artifacts
        artifact5_red_eb = Artifact(
            name="Credential Harvesting Success",
            type=ArtifactType.TOOL_OUTPUT,
            description="Credential Harvesting Report:\nTarget: executive@corp.local\nCredentials Captured: SUCCESS\nUsername: executive@corp.local\nPassword: [REDACTED]\nPortal Access: Confirmed\nCredential Testing:\n- Email (OWA): SUCCESS\n- VPN: SUCCESS\n- File Shares: SUCCESS\n- CRM: SUCCESS\nAll systems accessible. Ready for Phase 4.",
            file_url="/api/artifacts/files/credential_success_phase3.txt",
            notes_for_gm="Red Team sees their successful credential harvest."
        )
        db.add(artifact5_red_eb)
        db.flush()

        artifact6_red_eb = Artifact(
            name="Access Verification Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="Access Verification Report:\nSystems Accessible:\n✓ Email (OWA): Full access\n✓ VPN: Connected\n✓ File Shares: Read/Write access\n✓ CRM System: Full access\n✓ Financial Systems: Read access\nAccount Privileges: Executive-level\nPersistence: Email forwarding rule created\nStatus: All systems operational, ready for data collection",
            file_url="/api/artifacts/files/access_verification_phase3.txt",
            notes_for_gm="Red Team sees their verified access."
        )
        db.add(artifact6_red_eb)
        db.flush()

        # Phase 4 Artifacts
        # Blue Team Artifacts
        artifact7_blue_eb = Artifact(
            name="Unauthorized Access Alert",
            type=ArtifactType.LOG_SNIPPET,
            description="Security alert: Unauthorized access detected. User executive@corp.local logged into email from IP 203.0.113.45 (external, not corporate). Access pattern shows: Reading confidential emails, searching for 'password', 'credentials', 'admin', accessing file shares, attempting CRM access. User's location: Corporate office (legitimate), but access from external IP suggests account compromise. Immediate action required.",
            file_url="/api/artifacts/files/unauthorized_access_phase4.txt",
            notes_for_gm="Security alert showing unauthorized access."
        )
        db.add(artifact7_blue_eb)
        db.flush()

        artifact8_blue_eb = Artifact(
            name="Privilege Escalation Attempt Log",
            type=ArtifactType.LOG_SNIPPET,
            description="Privilege escalation attempt detected. Attacker searching executive's email for: 'administrator password', 'service account', 'API key', 'database credentials'. Multiple file share access attempts to admin directories. Attempted access to backup systems. All escalation attempts logged. User account has executive privileges but not domain admin - attacker seeking higher-level access.",
            file_url="/api/artifacts/files/privilege_escalation_phase4.txt",
            notes_for_gm="Logs showing privilege escalation attempts."
        )
        db.add(artifact8_blue_eb)
        db.flush()

        # Red Team Artifacts
        artifact7_red_eb = Artifact(
            name="Email Access & Intelligence Gathering",
            type=ArtifactType.TOOL_OUTPUT,
            description="Email Intelligence Report:\nEmails Accessed: 1,247\nSensitive Emails Found:\n- Financial reports: 23\n- Customer data: 45\n- Business strategy: 12\n- Credential references: 8 (no admin creds found)\nHigh-Value Targets Identified:\n- CRM database access\n- Customer PII\n- Financial records\n- Business intelligence\nStatus: Intelligence gathering complete, ready for exfiltration",
            file_url="/api/artifacts/files/email_intel_phase4.txt",
            notes_for_gm="Red Team sees their email intelligence gathering."
        )
        db.add(artifact7_red_eb)
        db.flush()

        artifact8_red_eb = Artifact(
            name="System Access Map",
            type=ArtifactType.TOOL_OUTPUT,
            description="System Access Map:\nSystems Under Control:\n1. Email (OWA): Full access, forwarding enabled\n2. File Shares: \\FS-01\\Executive, \\FS-01\\Finance\n3. CRM System: Read/Write access\n4. Financial Portal: Read access\nData Identified:\n- Customer database: 45,000 records\n- Financial records: Q1-Q4\n- Business documents: 2,100 files\nPrivilege Escalation: Attempted, no admin creds found\nStatus: Ready for data exfiltration",
            file_url="/api/artifacts/files/system_map_phase4.txt",
            notes_for_gm="Red Team sees their system access map."
        )
        db.add(artifact8_red_eb)
        db.flush()

        # Phase 5 Artifacts
        # Blue Team Artifacts
        artifact9_blue_eb = Artifact(
            name="Lateral Movement Detection",
            type=ArtifactType.LOG_SNIPPET,
            description="Lateral movement detected. Attacker using executive credentials to access: CRM database (customer records), Financial systems (Q4 reports), File shares (confidential documents). Network monitoring shows data transfers to external IP 198.51.100.45. Transfer volume: ~2.5 GB over 2 hours. Traffic encrypted (HTTPS) but pattern suggests data exfiltration. Multiple systems accessed in sequence.",
            file_url="/api/artifacts/files/lateral_movement_phase5.txt",
            notes_for_gm="Logs showing lateral movement."
        )
        db.add(artifact9_blue_eb)
        db.flush()

        artifact10_blue_eb = Artifact(
            name="Data Exfiltration Analysis",
            type=ArtifactType.INTEL_REPORT,
            description="Data Exfiltration Analysis:\nVolume: 2.5 GB\nTime Period: 2 hours\nDestination: 198.51.100.45\nData Types: Customer PII, financial records, business documents\nSystems Accessed: CRM, File Shares, Email\nData Classification:\n- Customer PII: 45,000 records (HIGH RISK)\n- Financial Data: Q4 reports (CONFIDENTIAL)\n- Business Intelligence: Strategic documents (PROPRIETARY)\nRegulatory Impact: GDPR, CCPA violation potential\nRecommendation: Immediate containment and breach assessment",
            file_url="/api/artifacts/files/exfiltration_analysis_phase5.txt",
            notes_for_gm="Data exfiltration analysis report."
        )
        db.add(artifact10_blue_eb)
        db.flush()

        artifact11_blue_eb = Artifact(
            name="Persistence Mechanisms Found",
            type=ArtifactType.TOOL_OUTPUT,
            description="Persistence Mechanisms Detected:\n1. Email Forwarding Rule: All emails forwarded to attacker@external.com\n2. Backup System Access: Attempted access to backup credentials\n3. Calendar Access: Attacker monitoring executive's calendar\n4. Contact List Access: Attacker copied executive's contacts\nActions Taken:\n- Removed email forwarding rule\n- Revoked backup access\n- Reset all credentials\n- Isolated account from critical systems",
            file_url="/api/artifacts/files/persistence_found_phase5.txt",
            notes_for_gm="Persistence mechanisms that were found and removed."
        )
        db.add(artifact11_blue_eb)
        db.flush()

        # Red Team Artifacts
        artifact9_red_eb = Artifact(
            name="Data Exfiltration Progress",
            type=ArtifactType.TOOL_OUTPUT,
            description="Data Exfiltration Status: IN PROGRESS\n\nData Collected:\n- Customer Database: 45,000 records (1.8 GB)\n- Financial Records: Q4 reports (450 MB)\n- Business Documents: 2,100 files (250 MB)\n\nUpload Status:\n- Destination: 198.51.100.45\n- Transferred: 2.5 GB / 2.5 GB (100%)\n- Encryption: AES-256\n- Status: COMPLETE\n\nPersistence Maintained:\n✓ Email forwarding active\n✓ Backup access attempted\n✓ Calendar monitoring active",
            file_url="/api/artifacts/files/exfiltration_progress_phase5.txt",
            notes_for_gm="Red Team sees their exfiltration progress."
        )
        db.add(artifact9_red_eb)
        db.flush()

        artifact10_red_eb = Artifact(
            name="Stolen Data Inventory",
            type=ArtifactType.INTEL_REPORT,
            description="Stolen Data Inventory:\n\nHigh-Value Data:\n- Customer PII: 45,000 records\n  * Names, addresses, phone numbers\n  * Email addresses\n  * Purchase history\n  * Estimated value: $2.25M\n\n- Financial Records: Q4 2023\n  * Revenue reports\n  * Budget forecasts\n  * Vendor contracts\n  * Estimated value: $5M+\n\n- Business Intelligence:\n  * Strategic plans\n  * Market analysis\n  * Competitive intelligence\n  * Estimated value: $10M+\n\nTotal Estimated Value: $17M+\nStatus: All data successfully exfiltrated",
            file_url="/api/artifacts/files/stolen_data_inventory_phase5.txt",
            notes_for_gm="Red Team sees their stolen data inventory."
        )
        db.add(artifact10_red_eb)
        db.flush()

        artifact11_red_eb = Artifact(
            name="Attack Summary Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="Attack Summary - Mission Accomplished\n\nTimeline:\n- Email Bomb: 09:15 UTC (8,247 emails)\n- Support Call: 09:45 UTC (12 minutes)\n- Credential Harvest: 10:00 UTC\n- Initial Access: 10:15 UTC\n- Data Exfiltration: 10:30-12:30 UTC (2.5 GB)\n\nResults:\n✓ Email bomb successful\n✓ Social engineering successful\n✓ Credentials harvested\n✓ Full system access obtained\n✓ 2.5 GB data exfiltrated\n✓ Persistence mechanisms deployed\n\nStatus: Attack complete, data secured, persistence maintained",
            file_url="/api/artifacts/files/attack_summary_phase5.txt",
            notes_for_gm="Red Team sees their complete attack summary."
        )
        db.add(artifact11_red_eb)
        db.flush()

        # Associate artifacts with phases and team roles
        # Phase 1: Email Bomb Deployment
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_eb.id, artifact_id=artifact1_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_eb.id, artifact_id=artifact2_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_eb.id, artifact_id=artifact1_red_eb.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_eb.id, artifact_id=artifact2_red_eb.id, team_role="red"))

        # Phase 2: Social Engineering Call
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_eb.id, artifact_id=artifact3_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_eb.id, artifact_id=artifact4_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_eb.id, artifact_id=artifact3_red_eb.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_eb.id, artifact_id=artifact4_red_eb.id, team_role="red"))

        # Phase 3: Credential Harvesting
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_eb.id, artifact_id=artifact5_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_eb.id, artifact_id=artifact6_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_eb.id, artifact_id=artifact5_red_eb.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_eb.id, artifact_id=artifact6_red_eb.id, team_role="red"))

        # Phase 4: Initial Access & Privilege Escalation
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_eb.id, artifact_id=artifact7_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_eb.id, artifact_id=artifact8_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_eb.id, artifact_id=artifact7_red_eb.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_eb.id, artifact_id=artifact8_red_eb.id, team_role="red"))

        # Phase 5: Lateral Movement & Data Exfiltration
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_eb.id, artifact_id=artifact9_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_eb.id, artifact_id=artifact10_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_eb.id, artifact_id=artifact11_blue_eb.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_eb.id, artifact_id=artifact9_red_eb.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_eb.id, artifact_id=artifact10_red_eb.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_eb.id, artifact_id=artifact11_red_eb.id, team_role="red"))

        db.commit()
        print("Created Email Bomb scenario with 5 phases and 22 artifacts (11 per team)")
    else:
        print("Email Bomb scenario already exists")


if __name__ == "__main__":
    try:
        seed_data()
        print("Seed data created successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

