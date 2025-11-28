"""
Seed script to populate database with initial data.
Run this after migrations: python seed_data.py
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    GMUser, Scenario, ScenarioPhase, Artifact, ArtifactType,
    scenario_phase_artifacts
)
from app.auth import get_password_hash

# Note: Tables should already exist from migrations
# Do NOT call Base.metadata.create_all() here as it will fail if tables exist

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

    # Create SharePoint RCE Zero-Day Exploitation scenario
    scenario3 = db.query(Scenario).filter(Scenario.name == "SharePoint RCE Zero-Day Exploitation").first()
    if not scenario3:
        scenario3 = Scenario(
            name="SharePoint RCE Zero-Day Exploitation",
            description="A new critical Remote Code Execution (RCE) vulnerability (CVE-2024-XXXXX) has been publicly disclosed affecting SharePoint Server 2019 and SharePoint Online. The vulnerability allows unauthenticated remote code execution through specially crafted HTTP requests. Your organization runs an external-facing SharePoint site for customer document collaboration. The security team must detect, contain, and remediate the threat while the Red Team attempts to exploit the vulnerability before patches are applied.",
            miro_board_url="https://miro.com/app/board/example3"
        )
        db.add(scenario3)
        db.flush()

        # Phase 1: Vulnerability Disclosure & Initial Reconnaissance
        phase1_sp = ScenarioPhase(
            scenario_id=scenario3.id,
            order_index=0,
            name="Phase 1: Vulnerability Disclosure & Initial Reconnaissance",
            briefing_text="At 14:30 UTC, Microsoft published Security Advisory ADV240001 disclosing a critical RCE vulnerability (CVE-2024-XXXXX) affecting SharePoint Server 2019 and SharePoint Online. The vulnerability has a CVSS score of 9.8 (Critical) and is being actively exploited in the wild. Your organization's external SharePoint site (sharepoint.corp.com) is running SharePoint Server 2019 and is accessible from the internet. The security team has been notified, but no patch is available yet. Initial scans show your SharePoint server is vulnerable. The Red Team has begun reconnaissance to identify the exact version and configuration.",
            red_objective="Identify the exact SharePoint version and build number. Map the external attack surface including exposed endpoints, authentication mechanisms, and potential entry points. Test for the vulnerability without triggering security alerts. Gather information about the server configuration, installed features, and user accounts.",
            blue_objective="Monitor for exploitation attempts and reconnaissance activity. Identify any indicators of compromise (IOCs) from the vulnerability disclosure. Review SharePoint server logs for suspicious requests. Assess patch availability and prepare emergency mitigation procedures. Determine if the server is vulnerable and assess business impact.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example3/frame1"
        )
        db.add(phase1_sp)
        db.flush()

        # Phase 2: Exploitation Attempt & Initial Access
        phase2_sp = ScenarioPhase(
            scenario_id=scenario3.id,
            order_index=1,
            name="Phase 2: Exploitation Attempt & Initial Access",
            briefing_text="The Red Team has successfully exploited the RCE vulnerability and gained initial access to the SharePoint server. Security logs show suspicious HTTP POST requests to /_layouts/15/upload.aspx with unusual payload patterns. The WAF (Web Application Firewall) initially blocked some requests but allowed others through. The attacker has executed PowerShell commands on the server and established a reverse shell connection. Endpoint detection on the SharePoint server (SP-SRV-01) has flagged unusual process activity including w3wp.exe spawning cmd.exe and powershell.exe processes.",
            red_objective="Successfully exploit the RCE vulnerability to gain code execution on the SharePoint server. Establish a persistent reverse shell connection. Evade WAF and security tool detection. Begin enumeration of the server environment, installed software, network configuration, and domain membership.",
            blue_objective="Detect the exploitation attempt through log analysis and security tool alerts. Identify the attack vector and confirm RCE execution. Isolate the compromised SharePoint server from the network. Preserve forensic evidence including memory dumps and log files. Block the attacker's C2 communications.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example3/frame2"
        )
        db.add(phase2_sp)
        db.flush()

        # Phase 3: Privilege Escalation & Persistence
        phase3_sp = ScenarioPhase(
            scenario_id=scenario3.id,
            order_index=2,
            name="Phase 3: Privilege Escalation & Persistence",
            briefing_text="The attacker has successfully escalated privileges on the SharePoint server. Security logs show the attacker has accessed the SharePoint farm administrator account and modified service accounts. The attacker has created scheduled tasks, installed web shells in multiple locations (/_layouts/15/, /_catalogs/, /Style Library/), and added backdoor user accounts to the SharePoint farm administrators group. The attacker has also established persistence through WMI event subscriptions and registry modifications. Network monitoring shows the attacker is attempting to move laterally to other systems in the domain.",
            red_objective="Escalate to farm administrator privileges on the SharePoint server. Establish multiple persistence mechanisms (web shells, scheduled tasks, service modifications). Create backdoor accounts and maintain access even if discovered. Begin lateral movement reconnaissance to identify domain controllers, file servers, and other high-value targets.",
            blue_objective="Detect privilege escalation and persistence mechanisms. Identify all web shells, scheduled tasks, and backdoor accounts. Remove persistence mechanisms and revoke compromised credentials. Prevent lateral movement by isolating the SharePoint server and blocking outbound connections. Document all attacker modifications for forensic analysis.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example3/frame3"
        )
        db.add(phase3_sp)
        db.flush()

        # Phase 4: Data Access & Exfiltration
        phase4_sp = ScenarioPhase(
            scenario_id=scenario3.id,
            order_index=3,
            name="Phase 4: Data Access & Exfiltration",
            briefing_text="The attacker has gained access to SharePoint site collections and document libraries. Security monitoring shows the attacker has accessed sensitive customer documents, employee data, and confidential project files. Network traffic analysis reveals large data transfers from the SharePoint server to external IP addresses (185.220.101.45, 45.146.164.110) using encrypted connections. Approximately 120 GB of data has been exfiltrated including customer contracts, employee PII, financial documents, and intellectual property. The attacker is using SharePoint's native APIs and PowerShell scripts to systematically download documents from multiple site collections.",
            red_objective="Access and catalog sensitive data stored in SharePoint site collections. Identify high-value targets including customer data, financial records, and intellectual property. Systematically exfiltrate data using multiple methods (SharePoint APIs, PowerShell, direct file access). Maintain access while exfiltrating data. Avoid detection by security monitoring tools.",
            blue_objective="Detect unauthorized data access and exfiltration attempts. Identify which site collections and documents have been accessed. Block data exfiltration by isolating the server and blocking outbound connections. Assess the scope of data breach including what data was accessed and exfiltrated. Prepare data breach notification procedures if required by regulations.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example3/frame4"
        )
        db.add(phase4_sp)
        db.flush()

        # Phase 5: Remediation & Post-Incident
        phase5_sp = ScenarioPhase(
            scenario_id=scenario3.id,
            order_index=4,
            name="Phase 5: Remediation & Post-Incident",
            briefing_text="Microsoft has released an emergency security patch (KB5012345) for the SharePoint RCE vulnerability. The security team has identified all compromised systems and attacker modifications. The SharePoint server has been isolated, web shells removed, backdoor accounts deleted, and persistence mechanisms eliminated. The server has been patched and rebuilt from a clean backup. However, the attacker had access for 18 hours and exfiltrated 120 GB of sensitive data. The incident response team must now assess the full impact, determine if data breach notifications are required, and implement additional security controls to prevent future exploitation.",
            red_objective="Assess the success of the attack campaign including data exfiltrated, systems compromised, and persistence maintained. Document attack techniques and evasion methods that worked. Identify any remaining backdoors or access methods that weren't discovered. Prepare final attack summary report.",
            blue_objective="Complete remediation by patching all vulnerable systems and removing all attacker access. Conduct a full forensic investigation to determine the complete scope of the breach. Assess regulatory and legal obligations including data breach notifications (GDPR, CCPA, etc.). Implement additional security controls (WAF rules, network segmentation, monitoring). Create an after-action report with lessons learned and recommendations.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example3/frame5"
        )
        db.add(phase5_sp)
        db.flush()

        # Phase 1 Artifacts
        # Blue Team Artifacts
        artifact1_blue_sp = Artifact(
            name="Microsoft Security Advisory ADV240001",
            type=ArtifactType.EMAIL,
            description="Microsoft Security Advisory ADV240001 - Critical RCE Vulnerability in SharePoint\n\nCVE-2024-XXXXX\nCVSS Score: 9.8 (Critical)\nAffected Products: SharePoint Server 2019, SharePoint Online\nVulnerability Type: Remote Code Execution (RCE)\nAttack Vector: Network (unauthenticated)\n\nSummary:\nA critical remote code execution vulnerability exists in Microsoft SharePoint Server. An attacker could exploit this vulnerability by sending a specially crafted HTTP request to an affected SharePoint server. Successful exploitation could allow the attacker to execute arbitrary code in the context of the SharePoint application pool.\n\nMitigation:\nMicrosoft is working on a security update. In the meantime, consider:\n- Restricting network access to SharePoint servers\n- Implementing WAF rules to block suspicious requests\n- Monitoring for exploitation attempts\n\nStatus: Patch not yet available. Active exploitation detected in the wild.",
            file_url="/api/artifacts/files/sharepoint_advisory_phase1.txt",
            notes_for_gm="Microsoft security advisory email about the vulnerability."
        )
        db.add(artifact1_blue_sp)
        db.flush()

        artifact2_blue_sp = Artifact(
            name="SharePoint Version Detection Log",
            type=ArtifactType.LOG_SNIPPET,
            description="SharePoint Server Version Detection:\n\nServer: sharepoint.corp.com\nProduct: Microsoft SharePoint Server 2019\nVersion: 16.0.10396.20000\nBuild: 16.0.10396.20000\nPatch Level: November 2023 CU\n\nVulnerability Status: VULNERABLE\nCVE-2024-XXXXX: Affected\n\nExposed Endpoints:\n- /_layouts/15/upload.aspx (EXPOSED)\n- /_vti_bin/ (EXPOSED)\n- /_layouts/15/start.aspx (EXPOSED)\n- /_api/ (EXPOSED)\n\nAuthentication: Forms-based authentication enabled\nExternal Access: YES (internet-facing)\nWAF Protection: Enabled (Cloudflare)\n\nRecommendation: IMMEDIATE PATCHING REQUIRED",
            file_url="/api/artifacts/files/sharepoint_version_phase1.txt",
            notes_for_gm="Log showing SharePoint version and vulnerability status."
        )
        db.add(artifact2_blue_sp)
        db.flush()

        # Red Team Artifacts
        artifact1_red_sp = Artifact(
            name="Reconnaissance Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="SharePoint Reconnaissance Report:\n\nTarget: sharepoint.corp.com\nStatus: VULNERABLE\n\nVersion Information:\n- SharePoint Server 2019\n- Build: 16.0.10396.20000\n- Patch Level: November 2023 CU\n- CVE-2024-XXXXX: CONFIRMED VULNERABLE\n\nExposed Endpoints Identified:\n✓ /_layouts/15/upload.aspx\n✓ /_vti_bin/\n✓ /_api/\n✓ /_layouts/15/start.aspx\n\nAuthentication:\n- Forms-based authentication\n- No MFA requirement detected\n- Guest access enabled\n\nWAF Status:\n- Cloudflare WAF detected\n- Some rules may be bypassable\n- Testing evasion techniques\n\nVulnerability Testing:\n- RCE exploit payload prepared\n- Testing against /_layouts/15/upload.aspx\n- Ready for exploitation attempt",
            file_url="/api/artifacts/files/recon_report_phase1.txt",
            notes_for_gm="Red Team sees their reconnaissance results."
        )
        db.add(artifact1_red_sp)
        db.flush()

        artifact2_red_sp = Artifact(
            name="Vulnerability Verification Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Vulnerability Verification:\n\nCVE-2024-XXXXX Status: CONFIRMED\nTarget: sharepoint.corp.com\nExploit Path: /_layouts/15/upload.aspx\n\nTest Results:\n✓ Version confirmed vulnerable\n✓ Endpoint accessible\n✓ WAF rules identified\n✓ Payload encoding tested\n✓ Ready for exploitation\n\nNext Steps:\n- Execute RCE payload\n- Establish reverse shell\n- Begin post-exploitation",
            file_url="/api/artifacts/files/vuln_verification_phase1.txt",
            notes_for_gm="Red Team sees their vulnerability verification."
        )
        db.add(artifact2_red_sp)
        db.flush()

        # Phase 2 Artifacts
        # Blue Team Artifacts
        artifact3_blue_sp = Artifact(
            name="WAF Alert - Suspicious POST Request",
            type=ArtifactType.LOG_SNIPPET,
            description="WAF Alert Log:\n\nTime: 2024-01-15 15:42:18 UTC\nSource IP: 185.220.101.45\nTarget: sharepoint.corp.com\nRequest: POST /_layouts/15/upload.aspx\n\nAlert Details:\n- Suspicious payload pattern detected\n- Base64 encoded data in request body\n- Unusual HTTP headers\n- Request size: 8,432 bytes\n\nWAF Action: BLOCKED (initial attempts)\nWAF Action: ALLOWED (subsequent attempts after evasion)\n\nStatus: EXPLOITATION ATTEMPT DETECTED\nSeverity: CRITICAL\n\nRecommendation: Immediate server isolation required",
            file_url="/api/artifacts/files/waf_alert_phase2.txt",
            notes_for_gm="WAF logs showing exploitation attempts."
        )
        db.add(artifact3_blue_sp)
        db.flush()

        artifact4_blue_sp = Artifact(
            name="SharePoint IIS Logs - RCE Execution",
            type=ArtifactType.LOG_SNIPPET,
            description="IIS Log Excerpt - SharePoint Server:\n\n2024-01-15 15:42:25 185.220.101.45 POST /_layouts/15/upload.aspx 200 8432\n2024-01-15 15:42:26 185.220.101.45 POST /_layouts/15/upload.aspx 200 1250\n2024-01-15 15:42:28 185.220.101.45 GET /_vti_bin/ 200 512\n\nProcess Activity Detected:\n- w3wp.exe (PID 4821) spawned cmd.exe (PID 4923)\n- cmd.exe executed: powershell.exe -enc [encoded command]\n- powershell.exe (PID 4924) established outbound connection\n- Destination: 185.220.101.45:4444 (reverse shell)\n\nStatus: RCE EXPLOITATION CONFIRMED\nImpact: Code execution achieved on SP-SRV-01",
            file_url="/api/artifacts/files/iis_logs_phase2.txt",
            notes_for_gm="IIS logs showing RCE execution and process spawning."
        )
        db.add(artifact4_blue_sp)
        db.flush()

        # Red Team Artifacts
        artifact3_red_sp = Artifact(
            name="Exploitation Success Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="RCE Exploitation Status: SUCCESS\n\nTarget: sharepoint.corp.com\nVulnerability: CVE-2024-XXXXX\nExploit Path: /_layouts/15/upload.aspx\n\nExploitation Timeline:\n15:42:18 - Initial payload sent\n15:42:20 - WAF evasion successful\n15:42:25 - RCE achieved\n15:42:26 - Reverse shell established\n\nAccess Confirmed:\n✓ Code execution on SP-SRV-01\n✓ Reverse shell active (PID 4924)\n✓ Running as: IIS AppPool\\SharePoint\n✓ Network connectivity confirmed\n\nPost-Exploitation:\n- Server enumeration in progress\n- Domain membership: CORP.local\n- Privileges: Medium (IIS AppPool)\n- Next: Privilege escalation",
            file_url="/api/artifacts/files/exploit_success_phase2.txt",
            notes_for_gm="Red Team sees their successful exploitation."
        )
        db.add(artifact3_red_sp)
        db.flush()

        artifact4_red_sp = Artifact(
            name="Server Environment Enumeration",
            type=ArtifactType.TOOL_OUTPUT,
            description="Server Environment Enumeration:\n\nHostname: SP-SRV-01\nOS: Windows Server 2019\nDomain: CORP.local\nCurrent User: IIS AppPool\\SharePoint\nPrivileges: Medium (not admin)\n\nInstalled Software:\n- SharePoint Server 2019\n- SQL Server 2019 (for SharePoint DB)\n- .NET Framework 4.8\n\nNetwork Configuration:\n- IP: 10.0.5.12\n- Domain Controller: DC-01 (10.0.5.1)\n- File Servers: FS-01 (10.0.5.20), FS-02 (10.0.5.21)\n\nSharePoint Farm:\n- Farm Admin: CORP\\svc_sharepoint\n- Service Accounts: Multiple identified\n- Site Collections: 45 identified\n\nNext Steps:\n- Escalate to farm admin\n- Deploy persistence\n- Access site collections",
            file_url="/api/artifacts/files/server_enum_phase2.txt",
            notes_for_gm="Red Team sees their server enumeration results."
        )
        db.add(artifact4_red_sp)
        db.flush()

        # Phase 3 Artifacts
        # Blue Team Artifacts
        artifact5_blue_sp = Artifact(
            name="Privilege Escalation Event Logs",
            type=ArtifactType.LOG_SNIPPET,
            description="Windows Security Event Log - Privilege Escalation:\n\nEvent ID 4624: Successful logon\nAccount: CORP\\svc_sharepoint\nSource: SP-SRV-01\nLogon Type: 3 (Network)\n\nEvent ID 4672: Special privileges assigned\nAccount: CORP\\svc_sharepoint\nPrivileges: SeDebugPrivilege, SeImpersonatePrivilege\n\nEvent ID 5136: Directory service object modified\nObject: CN=SharePoint Farm Admins,OU=Groups,DC=CORP,DC=local\nModification: Member added (CORP\\backdoor_user)\n\nSharePoint ULS Logs:\n- Farm administrator account accessed\n- Service account passwords modified\n- Scheduled tasks created: 3 tasks\n- Web shells deployed: 5 locations identified\n\nStatus: PRIVILEGE ESCALATION CONFIRMED",
            file_url="/api/artifacts/files/privilege_escalation_phase3.txt",
            notes_for_gm="Event logs showing privilege escalation."
        )
        db.add(artifact5_blue_sp)
        db.flush()

        artifact6_blue_sp = Artifact(
            name="Persistence Mechanism Detection Report",
            type=ArtifactType.INTEL_REPORT,
            description="Persistence Mechanism Detection Report:\n\nWeb Shells Identified:\n1. /_layouts/15/shell1.aspx\n2. /_catalogs/masterpage/shell2.aspx\n3. /Style Library/shell3.aspx\n4. /_layouts/15/update.aspx\n5. /_catalogs/wp/shell4.aspx\n\nScheduled Tasks:\n- Task1: 'SharePointUpdate' (runs every 5 min)\n- Task2: 'SystemMaintenance' (runs hourly)\n- Task3: 'HealthCheck' (runs on startup)\n\nBackdoor Accounts:\n- CORP\\backdoor_user (added to Farm Admins)\n- CORP\\svc_temp (service account modified)\n\nWMI Event Subscriptions:\n- 2 subscriptions created for persistence\n\nRegistry Modifications:\n- HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\n- HKLM\\SYSTEM\\CurrentControlSet\\Services\n\nRecommendation: Immediate removal of all persistence mechanisms required.",
            file_url="/api/artifacts/files/persistence_detection_phase3.pdf",
            notes_for_gm="Report showing all persistence mechanisms."
        )
        db.add(artifact6_blue_sp)
        db.flush()

        # Red Team Artifacts
        artifact5_red_sp = Artifact(
            name="Privilege Escalation Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="Privilege Escalation: SUCCESS\n\nMethod: Service account credential access\nTarget Account: CORP\\svc_sharepoint\nPrivileges Obtained: Farm Administrator\n\nActions Completed:\n✓ Farm admin account accessed\n✓ Service account passwords modified\n✓ Backdoor account created: CORP\\backdoor_user\n✓ Added to SharePoint Farm Admins group\n✓ Full farm access confirmed\n\nPersistence Deployed:\n✓ Web shells: 5 locations\n✓ Scheduled tasks: 3 tasks\n✓ WMI subscriptions: 2\n✓ Registry modifications: 2\n\nLateral Movement Recon:\n- Domain Controller: DC-01 (identified)\n- File Servers: FS-01, FS-02 (identified)\n- SQL Server: SP-SQL-01 (identified)\n\nStatus: Ready for data access phase",
            file_url="/api/artifacts/files/privilege_status_phase3.txt",
            notes_for_gm="Red Team sees their privilege escalation success."
        )
        db.add(artifact5_red_sp)
        db.flush()

        artifact6_red_sp = Artifact(
            name="Persistence Deployment Report",
            type=ArtifactType.TOOL_OUTPUT,
            description="Persistence Deployment Status: COMPLETE\n\nWeb Shells Deployed:\n✓ /_layouts/15/shell1.aspx\n✓ /_catalogs/masterpage/shell2.aspx\n✓ /Style Library/shell3.aspx\n✓ /_layouts/15/update.aspx\n✓ /_catalogs/wp/shell4.aspx\n\nScheduled Tasks:\n✓ SharePointUpdate (5 min interval)\n✓ SystemMaintenance (hourly)\n✓ HealthCheck (on startup)\n\nBackdoor Accounts:\n✓ CORP\\backdoor_user (Farm Admin)\n✓ CORP\\svc_temp (service account)\n\nWMI Subscriptions: 2 active\nRegistry Persistence: 2 locations\n\nAll persistence mechanisms active. Access maintained even if primary shell discovered.",
            file_url="/api/artifacts/files/persistence_deployment_phase3.txt",
            notes_for_gm="Red Team sees their persistence deployment."
        )
        db.add(artifact6_red_sp)
        db.flush()

        # Phase 4 Artifacts
        # Blue Team Artifacts
        artifact7_blue_sp = Artifact(
            name="SharePoint Access Audit Logs",
            type=ArtifactType.LOG_SNIPPET,
            description="SharePoint Access Audit Logs:\n\nUnauthorized Access Detected:\n\nSite Collections Accessed:\n- /sites/CustomerPortal (45,000 documents)\n- /sites/HR (12,000 documents)\n- /sites/Finance (8,500 documents)\n- /sites/RD (3,200 documents)\n\nAccess Pattern:\n- User: CORP\\backdoor_user\n- Method: SharePoint REST API\n- Timeframe: 15:50 - 18:30 UTC\n- Documents Accessed: 68,700 documents\n- Documents Downloaded: ~2,100 documents\n\nSensitive Data Categories:\n- Customer PII: 15,000 records\n- Employee Data: 2,400 records\n- Financial Records: 850 files\n- Intellectual Property: 320 files\n\nStatus: UNAUTHORIZED DATA ACCESS CONFIRMED",
            file_url="/api/artifacts/files/sharepoint_access_phase4.txt",
            notes_for_gm="SharePoint audit logs showing unauthorized access."
        )
        db.add(artifact7_blue_sp)
        db.flush()

        artifact8_blue_sp = Artifact(
            name="Data Exfiltration Traffic Analysis",
            type=ArtifactType.LOG_SNIPPET,
            description="Network Traffic Analysis - Data Exfiltration:\n\nSource: SP-SRV-01 (10.0.5.12)\nDestination IPs:\n- 185.220.101.45 (port 443)\n- 45.146.164.110 (port 443)\n\nTraffic Pattern:\n- Protocol: HTTPS (encrypted)\n- Duration: 2 hours 40 minutes\n- Total Data Transferred: ~120 GB\n- Transfer Rate: ~45 GB/hour\n- Connection Type: Persistent connections\n\nData Transfer Methods:\n- SharePoint REST API calls\n- PowerShell download scripts\n- Direct file access via web shells\n\nFile Types Exfiltrated:\n- .docx, .xlsx, .pdf, .pptx\n- Database files (.mdb, .accdb)\n- Archive files (.zip, .rar)\n\nStatus: ACTIVE EXFILTRATION DETECTED\nRecommendation: Immediate network isolation required",
            file_url="/api/artifacts/files/exfiltration_traffic_phase4.txt",
            notes_for_gm="Network logs showing data exfiltration."
        )
        db.add(artifact8_blue_sp)
        db.flush()

        # Red Team Artifacts
        artifact7_red_sp = Artifact(
            name="Data Access Inventory",
            type=ArtifactType.TOOL_OUTPUT,
            description="SharePoint Data Access Inventory:\n\nSite Collections Accessed: 4\nTotal Documents: 68,700\nDocuments Downloaded: 2,100\n\nHigh-Value Data Identified:\n\n1. Customer Portal (/sites/CustomerPortal)\n   - Customer contracts: 450 files\n   - Customer PII: 15,000 records\n   - Project documents: 2,800 files\n\n2. HR Site (/sites/HR)\n   - Employee records: 2,400 records\n   - Salary information: 850 files\n   - Performance reviews: 1,200 files\n\n3. Finance Site (/sites/Finance)\n   - Financial statements: 350 files\n   - Budget documents: 500 files\n\n4. R&D Site (/sites/RD)\n   - Intellectual property: 320 files\n   - Research data: 2,880 files\n\nExfiltration Status: IN PROGRESS (120 GB / 120 GB)",
            file_url="/api/artifacts/files/data_inventory_phase4.txt",
            notes_for_gm="Red Team sees their data access inventory."
        )
        db.add(artifact7_red_sp)
        db.flush()

        artifact8_red_sp = Artifact(
            name="Data Exfiltration Progress",
            type=ArtifactType.TOOL_OUTPUT,
            description="Data Exfiltration Status: COMPLETE\n\nTotal Data Exfiltrated: 120 GB\nDuration: 2 hours 40 minutes\nTransfer Rate: ~45 GB/hour\n\nData Categories:\n✓ Customer PII: 15,000 records (25 GB)\n✓ Employee Data: 2,400 records (8 GB)\n✓ Financial Records: 850 files (35 GB)\n✓ Intellectual Property: 320 files (42 GB)\n✓ Contracts & Legal: 450 files (10 GB)\n\nExfiltration Methods:\n- SharePoint REST API: 60 GB\n- PowerShell scripts: 45 GB\n- Web shell downloads: 15 GB\n\nDestination:\n- 185.220.101.45: 70 GB\n- 45.146.164.110: 50 GB\n\nStatus: All high-value data successfully exfiltrated. Ready for remediation phase.",
            file_url="/api/artifacts/files/exfiltration_progress_phase4.txt",
            notes_for_gm="Red Team sees their exfiltration progress."
        )
        db.add(artifact8_red_sp)
        db.flush()

        # Phase 5 Artifacts
        # Blue Team Artifacts
        artifact9_blue_sp = Artifact(
            name="Patch Deployment Status",
            type=ArtifactType.TOOL_OUTPUT,
            description="SharePoint Security Patch Deployment:\n\nPatch: KB5012345 (Emergency Security Update)\nCVE: CVE-2024-XXXXX\nStatus: DEPLOYED\n\nRemediation Actions Completed:\n✓ SharePoint server isolated from network\n✓ All web shells removed (5 locations)\n✓ Scheduled tasks deleted (3 tasks)\n✓ Backdoor accounts removed (2 accounts)\n✓ WMI subscriptions removed (2 subscriptions)\n✓ Registry modifications reverted\n✓ Service account passwords reset\n✓ SharePoint server rebuilt from clean backup\n✓ Patch KB5012345 installed\n✓ Server restored to production\n\nTimeline:\n- Attack Duration: 18 hours\n- Remediation Time: 6 hours\n- Total Downtime: 24 hours\n\nStatus: REMEDIATION COMPLETE",
            file_url="/api/artifacts/files/patch_deployment_phase5.txt",
            notes_for_gm="Patch deployment and remediation status."
        )
        db.add(artifact9_blue_sp)
        db.flush()

        artifact10_blue_sp = Artifact(
            name="Data Breach Impact Assessment",
            type=ArtifactType.INTEL_REPORT,
            description="Data Breach Impact Assessment:\n\nBreach Summary:\n- Duration: 18 hours\n- Data Exfiltrated: 120 GB\n- Records Affected: 17,400+ individuals\n\nData Categories Breached:\n1. Customer PII: 15,000 records\n   - Names, addresses, email addresses\n   - Payment information (partial)\n   - Contract details\n\n2. Employee Data: 2,400 records\n   - Social Security Numbers\n   - Salary information\n   - Performance reviews\n\n3. Financial Records: 850 files\n   - Q1-Q4 2023 financials\n   - Budget forecasts\n   - Vendor contracts\n\n4. Intellectual Property: 320 files\n   - Proprietary algorithms\n   - Research data\n   - Product designs\n\nRegulatory Impact:\n- GDPR: Notification required (EU customers)\n- CCPA: Notification required (CA residents)\n- Potential HIPAA implications\n\nEstimated Cost: $2.5M - $5M (regulatory fines, notification, legal)",
            file_url="/api/artifacts/files/breach_impact_phase5.pdf",
            notes_for_gm="Data breach impact assessment report."
        )
        db.add(artifact10_blue_sp)
        db.flush()

        artifact11_blue_sp = Artifact(
            name="After-Action Report - Lessons Learned",
            type=ArtifactType.INTEL_REPORT,
            description="After-Action Report - SharePoint RCE Incident:\n\nKey Findings:\n1. Vulnerability disclosure to exploitation: 4 hours\n2. Detection time: 2 hours after exploitation\n3. Total breach duration: 18 hours\n4. Data exfiltrated: 120 GB\n\nRoot Causes:\n- External-facing SharePoint server\n- No patch available at time of disclosure\n- WAF rules insufficient to block all exploit attempts\n- Delayed detection and response\n\nRecommendations:\n1. Implement network segmentation for SharePoint\n2. Enhance WAF rules for SharePoint-specific attacks\n3. Deploy additional monitoring for SharePoint servers\n4. Establish faster patch deployment procedures\n5. Implement data loss prevention (DLP) controls\n6. Regular security assessments of external-facing systems\n\nStatus: Report submitted to management and security team",
            file_url="/api/artifacts/files/aar_phase5.pdf",
            notes_for_gm="After-action report with lessons learned."
        )
        db.add(artifact11_blue_sp)
        db.flush()

        # Red Team Artifacts
        artifact9_red_sp = Artifact(
            name="Attack Success Summary",
            type=ArtifactType.TOOL_OUTPUT,
            description="SharePoint RCE Attack Summary:\n\nTimeline:\n- Vulnerability Disclosure: 14:30 UTC\n- Reconnaissance: 14:35 - 15:40 UTC\n- Exploitation: 15:42 UTC\n- Privilege Escalation: 16:15 UTC\n- Data Exfiltration: 15:50 - 18:30 UTC\n- Remediation Detected: 08:30 UTC (next day)\n\nAttack Success Metrics:\n✓ RCE exploitation: SUCCESS\n✓ Privilege escalation: SUCCESS\n✓ Persistence deployed: 5 web shells, 3 tasks\n✓ Data accessed: 68,700 documents\n✓ Data exfiltrated: 120 GB\n✓ Access maintained: 18 hours\n\nTechniques Used:\n- CVE-2024-XXXXX RCE exploit\n- WAF evasion\n- Service account credential access\n- Web shell deployment\n- SharePoint API abuse\n\nStatus: Mission accomplished. All objectives achieved.",
            file_url="/api/artifacts/files/attack_summary_phase5.txt",
            notes_for_gm="Red Team sees their attack summary."
        )
        db.add(artifact9_red_sp)
        db.flush()

        artifact10_red_sp = Artifact(
            name="Lessons Learned Report",
            type=ArtifactType.INTEL_REPORT,
            description="Attack Lessons Learned:\n\nSuccessful Techniques:\n✓ RCE exploit worked flawlessly\n✓ WAF evasion successful (payload encoding)\n✓ Service account credential access effective\n✓ Web shell persistence maintained access\n✓ SharePoint API abuse for data access\n\nDetection Evasion:\n- WAF initially blocked but evasion worked\n- Security tools detected but too late\n- Persistence mechanisms not immediately discovered\n\nAreas for Improvement:\n- Faster lateral movement\n- Additional persistence methods\n- Better data cataloging before exfiltration\n\nOverall Assessment:\nAttack was highly successful. Target organization had:\n- External-facing vulnerable system\n- Insufficient WAF protection\n- Delayed detection and response\n- No data loss prevention\n\nRecommendation: Continue targeting external-facing SharePoint deployments.",
            file_url="/api/artifacts/files/lessons_learned_phase5.txt",
            notes_for_gm="Red Team sees their lessons learned."
        )
        db.add(artifact10_red_sp)
        db.flush()

        artifact11_red_sp = Artifact(
            name="Final Attack Report",
            type=ArtifactType.INTEL_REPORT,
            description="Final Attack Report - SharePoint RCE Exploitation:\n\nMission: Exploit SharePoint RCE vulnerability and exfiltrate sensitive data\nStatus: SUCCESS\n\nResults:\n- Systems Compromised: 1 (SP-SRV-01)\n- Privilege Level: Farm Administrator\n- Data Exfiltrated: 120 GB\n- Access Duration: 18 hours\n- Persistence: 5 web shells, 3 scheduled tasks\n\nData Value:\n- Customer PII: 15,000 records\n- Employee Data: 2,400 records\n- Financial Records: 850 files\n- Intellectual Property: 320 files\n\nEstimated Data Value: $10M+\n\nAttack Timeline:\n- Day 1, 14:30 UTC: Vulnerability disclosed\n- Day 1, 15:42 UTC: Exploitation successful\n- Day 1, 18:30 UTC: Data exfiltration complete\n- Day 2, 08:30 UTC: Remediation detected\n\nConclusion: Attack successfully completed all objectives. Target organization's security controls were insufficient to prevent or quickly detect the attack.",
            file_url="/api/artifacts/files/final_report_phase5.txt",
            notes_for_gm="Red Team sees their final attack report."
        )
        db.add(artifact11_red_sp)
        db.flush()

        # Associate artifacts with phases and team roles
        # Phase 1: Vulnerability Disclosure & Initial Reconnaissance
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_sp.id, artifact_id=artifact1_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_sp.id, artifact_id=artifact2_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_sp.id, artifact_id=artifact1_red_sp.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1_sp.id, artifact_id=artifact2_red_sp.id, team_role="red"))

        # Phase 2: Exploitation Attempt & Initial Access
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_sp.id, artifact_id=artifact3_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_sp.id, artifact_id=artifact4_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_sp.id, artifact_id=artifact3_red_sp.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2_sp.id, artifact_id=artifact4_red_sp.id, team_role="red"))

        # Phase 3: Privilege Escalation & Persistence
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_sp.id, artifact_id=artifact5_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_sp.id, artifact_id=artifact6_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_sp.id, artifact_id=artifact5_red_sp.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3_sp.id, artifact_id=artifact6_red_sp.id, team_role="red"))

        # Phase 4: Data Access & Exfiltration
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_sp.id, artifact_id=artifact7_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_sp.id, artifact_id=artifact8_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_sp.id, artifact_id=artifact7_red_sp.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4_sp.id, artifact_id=artifact8_red_sp.id, team_role="red"))

        # Phase 5: Remediation & Post-Incident
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_sp.id, artifact_id=artifact9_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_sp.id, artifact_id=artifact10_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_sp.id, artifact_id=artifact11_blue_sp.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_sp.id, artifact_id=artifact9_red_sp.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_sp.id, artifact_id=artifact10_red_sp.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5_sp.id, artifact_id=artifact11_red_sp.id, team_role="red"))

        db.commit()
        print("Created SharePoint RCE scenario with 5 phases and 22 artifacts (11 per team)")
    else:
        print("SharePoint RCE scenario already exists")


if __name__ == "__main__":
    try:
        seed_data()
        print("Seed data created successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

