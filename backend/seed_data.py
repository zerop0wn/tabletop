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

        # Phase 1: Initial Compromise - REDESIGNED with artifact-driven decision
        phase1 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=0,
            name="Phase 1: Initial Compromise",
            briefing_text="At 08:15 AM, your phishing campaign has successfully delivered emails to two departments:\n- Finance Department (WS-FIN-042): 12 emails opened, 3 links clicked\n- Marketing Department (WS-MKT-015): 8 emails opened, 2 links clicked\n\nBoth departments have users who clicked the malicious links. You now have initial access attempts on workstations in both departments:\n- **WS-FIN-042** (Finance): finance.user@corp.local clicked malicious link\n- **WS-MKT-015** (Marketing): marketing.user@corp.local clicked malicious link\n\nHowever, you have limited resources and want to focus your efforts on the target that offers the **best chance of establishing a persistent foothold without immediate detection**.\n\nYou've collected initial reconnaissance data on both targets (WS-FIN-042 and WS-MKT-015). Your decision: **Which department should you prioritize for establishing persistence?**\n\n- Option A: Focus on Finance Department (WS-FIN-042)\n- Option B: Focus on Marketing Department (WS-MKT-015)\n- Option C: Split efforts between both departments\n\n**Remember:** Review the artifacts carefully. They contain critical information about security posture, EDR coverage, and user privileges for **both WS-FIN-042 and WS-MKT-015** that will determine your success. The artifacts will reveal which target has weaker security controls and presents the better opportunity.",
            red_objective="Analyze the reconnaissance data from both departments to identify which target offers the best opportunity for establishing persistent access with minimal detection risk. Focus your initial persistence efforts on the most vulnerable target.",
            blue_objective="Review security telemetry from both departments to identify which department shows the most concerning indicators of compromise. Prioritize containment and investigation efforts on the department with the highest risk of successful attacker persistence.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame1",
            available_actions={
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
                        "description": "Disconnect WS-FIN-042 (Finance) from the network to prevent further spread. Review artifacts comparing WS-FIN-042 and WS-MKT-015 to assess risk level."
                    },
                    {
                        "name": "Isolate Marketing Department host (WS-MKT-015)",
                        "description": "Disconnect WS-MKT-015 (Marketing) from the network to prevent further spread. Review artifacts comparing WS-FIN-042 and WS-MKT-015 to assess risk level."
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

        # Phase 3: Privilege Escalation & Lateral Movement - REDESIGNED with two-host decision
        phase3 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=2,
            name="Phase 3: Privilege Escalation & Lateral Movement",
            briefing_text="You have successfully established user-level access on two workstations:\n- WS-FIN-01 (Finance Department)\n- WS-MKT-02 (Marketing Department)\n\nYour goal is to escalate to local administrator / SYSTEM privileges on at least one host to enable ransomware deployment and lateral movement. However, you have limited time and want to focus your escalation attempt where there is a **high probability of success**.\n\nYou've collected system information and vulnerability intelligence on both hosts. Your decision: **Which host should you prioritize for privilege escalation?**\n\n- Option A: Attempt privilege escalation on WS-FIN-01 using generic token-stealing and UAC bypass techniques\n- Option B: Attempt privilege escalation on WS-MKT-02 using the specific local privilege escalation exploit identified in vulnerability scans\n- Option C: Split efforts and run automated priv-esc tooling on both hosts in parallel\n\n**Remember:** Review the artifacts carefully. They contain system information, patch levels, EDR status, and vulnerability scan results that will determine your success.",
            red_objective="Analyze system information and vulnerability data from both hosts to identify which target offers the best opportunity for successful privilege escalation. Focus your escalation attempt on the host with the highest probability of success based on the evidence.",
            blue_objective="Review security telemetry and vulnerability scan data to identify which host is at greater risk of imminent privilege escalation. Prioritize containment and investigation efforts on the host with the highest risk based on the evidence.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame3",
            available_actions={
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
        )
        db.add(phase3)
        db.flush()

        # Phase 4: Data Exfiltration - REDESIGNED with two-file-server decision
        phase4 = ScenarioPhase(
            scenario_id=scenario.id,
            order_index=3,
            name="Phase 4: Data Exfiltration",
            briefing_text="You have successfully obtained domain administrator credentials and have access to multiple file servers:\n- FS-01 (Finance File Server): Contains financial records, customer PII, and proprietary research data\n- FS-02 (HR/Operations File Server): Contains employee records, HR data, and operational documents\n\nBoth servers contain valuable data, but you have limited time before defenders detect your presence. You need to prioritize which data source to exfiltrate first to maximize the value of stolen data while minimizing detection risk.\n\nYou've mapped network paths, analyzed data classification, and reviewed access logs. Your decision: **Which file server should you prioritize for data exfiltration?**\n\n- Option A: Prioritize exfiltration from FS-01 (Finance) - High-value financial and customer data\n- Option B: Prioritize exfiltration from FS-02 (HR/Operations) - Employee records and operational data\n- Option C: Exfiltrate from both servers simultaneously using parallel streams\n\n**Remember:** Review the artifacts carefully. They contain network topology, data classification, DLP policies, and monitoring coverage that will determine your success and detection risk.",
            red_objective="Analyze network topology, data classification, and monitoring coverage to identify which file server offers the best opportunity for successful data exfiltration with minimal detection. Prioritize exfiltration from the source that provides maximum value with lowest detection risk.",
            blue_objective="Review network monitoring, data loss prevention (DLP) alerts, and access logs to identify which file server is at greatest risk of data exfiltration. Prioritize containment and monitoring efforts on the server with the highest risk based on the evidence.",
            default_duration_seconds=900,
            miro_frame_url="https://miro.com/app/board/example/frame4",
            available_actions={
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

        # Create artifacts - Phase 1: Initial Compromise (REDESIGNED)
        # Blue Team Artifacts - Microsoft Defender/E5 Security Stack
        artifact1_blue = Artifact(
            name="Microsoft Defender for Endpoint - Finance Department Alert",
            type=ArtifactType.LOG_SNIPPET,
            description="""Microsoft Defender for Endpoint Alert
Alert ID: DA-2024-001234
Severity: Medium
Time: 08:17:23 UTC
Device: WS-FIN-042
User: finance.user@corp.local
Department: Finance

Alert Details:
- Alert Title: Suspicious PowerShell execution detected
- Process: powershell.exe -EncodedCommand [base64]
- Parent Process: mshta.exe
- File Hash: 7a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c
- Action Taken: BLOCKED by Defender for Endpoint
- EDR Agent Status: Active, Latest Version (10.0.26100.1)
- Defender Antivirus: Enabled, Real-time Protection: ON
- Cloud Protection: Enabled
- Last Scan: 08:00:00 UTC (Clean)

Additional Context:
- Device is fully onboarded to Microsoft Defender for Endpoint
- Advanced Threat Protection (ATP) enabled
- Automated Investigation: Triggered
- Device Risk Score: Medium (65/100)
- User has Standard User privileges (non-admin)

Recommendation: Device isolated automatically. Investigation in progress.""",
            file_url="/api/artifacts/files/defender_finance_alert_phase1.txt",
            notes_for_gm="Microsoft Defender for Endpoint alert showing Finance department has strong EDR coverage and blocked the attack."
        )
        db.add(artifact1_blue)
        db.flush()

        artifact2_blue = Artifact(
            name="Microsoft Defender for Endpoint - Marketing Department Alert",
            type=ArtifactType.LOG_SNIPPET,
            description="""Microsoft Defender for Endpoint Alert
Alert ID: DA-2024-001235
Severity: Low
Time: 08:18:45 UTC
Device: WS-MKT-015
User: marketing.user@corp.local
Department: Marketing

Alert Details:
- Alert Title: Suspicious script execution detected
- Process: wscript.exe
- Parent Process: outlook.exe
- File Hash: 8b9c4d5e6f7a8b9c0d1e2f3a4b5c6d7e
- Action Taken: DETECTED (not blocked)
- EDR Agent Status: Outdated (Version 10.0.19045.1 - Last updated: 45 days ago)
- Defender Antivirus: Enabled, Real-time Protection: ON
- Cloud Protection: Enabled (but agent outdated)
- Last Scan: 07:30:00 UTC (Clean)

Additional Context:
- Device is onboarded to Microsoft Defender for Endpoint but agent is outdated
- Advanced Threat Protection (ATP): Enabled but may have coverage gaps
- Automated Investigation: Not triggered (agent outdated)
- Device Risk Score: High (85/100) - Due to outdated agent and detection
- User has Local Administrator privileges (admin account present on device)

WARNING: Outdated EDR agent may have reduced detection capabilities. Device requires immediate attention.""",
            file_url="/api/artifacts/files/defender_marketing_alert_phase1.txt",
            notes_for_gm="Microsoft Defender alert showing Marketing department has outdated EDR agent and weaker security posture."
        )
        db.add(artifact2_blue)
        db.flush()

        artifact3_blue = Artifact(
            name="Microsoft Sentinel - Phishing Campaign Analysis",
            type=ArtifactType.INTEL_REPORT,
            description="""Microsoft Sentinel Incident Report
Incident ID: INC-2024-00156
Title: Phishing Campaign - Multiple Departments Affected
Severity: Medium
Status: Active Investigation

Summary:
Phishing emails delivered to two departments:
- Finance: 12 emails opened, 3 links clicked
- Marketing: 8 emails opened, 2 links clicked

Email Security (Microsoft Defender for Office 365):
- Finance emails: 8/12 blocked by Safe Links, 4/12 delivered
- Marketing emails: 2/8 blocked, 6/8 delivered
- Overall: 10/20 emails blocked (50% success rate)

Endpoint Response:
- Finance (WS-FIN-042): Alert generated, action BLOCKED by Defender for Endpoint
- Marketing (WS-MKT-015): Alert generated, action DETECTED (not blocked)

Risk Assessment:
- Finance Department: Medium Risk - Strong EDR coverage, blocked attack
- Marketing Department: High Risk - Outdated EDR agent, detection only (not blocked)

Recommendation: Prioritize investigation and containment of Marketing department endpoint due to higher risk score and outdated security controls.""",
            file_url="/api/artifacts/files/sentinel_phishing_analysis_phase1.txt",
            notes_for_gm="Microsoft Sentinel analysis showing Marketing department is higher risk."
        )
        db.add(artifact3_blue)
        db.flush()

        # Red Team Artifacts - Phase 1
        artifact1_red = Artifact(
            name="Finance Department Reconnaissance Report",
            type=ArtifactType.INTEL_REPORT,
            description="""Target: Finance Department (WS-FIN-042)
User: finance.user@corp.local

Initial Access Status:
✓ Email delivered: YES
✓ Link clicked: YES
✓ Payload executed: YES
✓ C2 beacon established: YES

System Information:
- OS: Windows 10 Enterprise (Build 19045)
- Domain: CORP.LOCAL
- User Privileges: Standard User (non-admin)
- EDR Agent: Microsoft Defender for Endpoint - ACTIVE, Latest Version
- Defender Status: Real-time protection ON, Cloud protection ON
- Last Security Update: 2 days ago

Security Posture Assessment:
- EDR Coverage: STRONG (latest agent, active monitoring)
- Detection Risk: HIGH (attack was BLOCKED by Defender)
- Persistence Difficulty: HIGH (requires admin for most mechanisms)
- User Privileges: LOW (standard user, limited access)

Assessment: High-value target but STRONG security controls. Attack was blocked. Establishing persistence will be difficult and high-risk.""",
            file_url="/api/artifacts/files/finance_recon_phase1.txt",
            notes_for_gm="Red Team sees Finance has strong security but was blocked."
        )
        db.add(artifact1_red)
        db.flush()

        artifact2_red = Artifact(
            name="Marketing Department Reconnaissance Report",
            type=ArtifactType.INTEL_REPORT,
            description="""Target: Marketing Department (WS-MKT-015)
User: marketing.user@corp.local

Initial Access Status:
✓ Email delivered: YES
✓ Link clicked: YES
✓ Payload executed: YES
✓ C2 beacon established: YES

System Information:
- OS: Windows 10 Enterprise (Build 18363)
- Domain: CORP.LOCAL
- User Privileges: Standard User (but local admin account present)
- EDR Agent: Microsoft Defender for Endpoint - OUTDATED (Version 19045.1, 45 days old)
- Defender Status: Real-time protection ON, but agent outdated
- Last Security Update: 45 days ago

Security Posture Assessment:
- EDR Coverage: WEAK (outdated agent, may have detection gaps)
- Detection Risk: MEDIUM (attack was DETECTED but not blocked)
- Persistence Difficulty: MEDIUM (local admin account available)
- User Privileges: MEDIUM (standard user but admin account on device)

Assessment: Medium-value target with WEAKER security controls. Attack was detected but not blocked. Outdated EDR agent provides opportunity for persistence with lower detection risk.""",
            file_url="/api/artifacts/files/marketing_recon_phase1.txt",
            notes_for_gm="Red Team sees Marketing has weaker security and better opportunity."
        )
        db.add(artifact2_red)
        db.flush()

        artifact3_red = Artifact(
            name="C2 Connection Status - Both Targets",
            type=ArtifactType.TOOL_OUTPUT,
            description="""C2 Communication Status Report

Target 1: WS-FIN-042 (Finance)
- Connection: ESTABLISHED then TERMINATED
- Server: 185.220.101.45:443
- Status: BLOCKED by Defender for Endpoint
- Last Check-in: 08:17:25 UTC (then blocked)
- Detection: HIGH - Defender blocked connection
- Persistence: FAILED - Scheduled task creation blocked

Target 2: WS-MKT-015 (Marketing)
- Connection: ACTIVE
- Server: 185.220.101.45:443
- Status: OPERATIONAL
- Last Check-in: 08:18:50 UTC (ongoing)
- Detection: MEDIUM - Detected but not blocked
- Persistence: PARTIAL - Some mechanisms successful

Recommendation: Focus persistence efforts on WS-MKT-015 (Marketing). Finance target has strong EDR and blocked our attack. Marketing target has outdated agent and better opportunity for successful persistence.""",
            file_url="/api/artifacts/files/c2_status_both_phase1.txt",
            notes_for_gm="Red Team sees Marketing target is better for persistence."
        )
        db.add(artifact3_red)
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

        # Phase 3 Artifacts - Privilege Escalation (REDESIGNED with two-host decision)
        # Blue Team Artifacts - Microsoft Defender/E5 Security Stack
        artifact5_blue = Artifact(
            name="Microsoft Defender for Endpoint - WS-FIN-01 System Information",
            type=ArtifactType.LOG_SNIPPET,
            description="""Microsoft Defender for Endpoint - Device Information
Device: WS-FIN-01
Department: Finance
Onboarding Status: Fully Onboarded

System Details:
- OS: Windows 10 Enterprise
- OS Version: 10.0.19045 Build 19045
- Install Date: 2022-06-15
- Hotfixes Installed:
  * KB5023696 (Security Update)
  * KB5026361 (Security Update)
  * KB5030219 (Security Update)
  * KB5034123 (Security Update - Latest)

Security Configuration:
- EDR Agent: Microsoft Defender for Endpoint v10.0.26100.1 (Latest)
- Defender Antivirus: Enabled, Real-time Protection: ON
- Cloud Protection: Enabled
- Last Scan: 08:00:00 UTC (Clean, no threats)
- LAPS (Local Administrator Password Solution): ENABLED
- Local Admin Account: Managed by PAM (Privileged Access Management)

User Accounts:
- fin_user: Standard User (non-admin)
- svc_fin_reports: Service Account, Local Admin (PAM-managed password)

Vulnerability Assessment:
- Critical Findings: 0
- High Findings: 0
- Medium Findings: 0
- Local Privilege Escalation Vulnerabilities: NONE DETECTED

Risk Score: Low (25/100)
Recommendation: System is fully patched and hardened. Low risk of privilege escalation.""",
            file_url="/api/artifacts/files/defender_ws-fin-01_phase3.txt",
            notes_for_gm="Defender shows WS-FIN-01 is fully patched and hardened."
        )
        db.add(artifact5_blue)
        db.flush()

        artifact6_blue = Artifact(
            name="Microsoft Defender for Endpoint - WS-MKT-02 System Information",
            type=ArtifactType.LOG_SNIPPET,
            description="""Microsoft Defender for Endpoint - Device Information
Device: WS-MKT-02
Department: Marketing
Onboarding Status: Partially Onboarded (Agent Outdated)

System Details:
- OS: Windows 10 Enterprise
- OS Version: 10.0.18363 Build 18363
- Install Date: 2019-09-03
- Hotfixes Installed:
  * KB4528760 (Security Update - OLD)
  * KB4532693 (Security Update - OLD)
  * KB5001337: NOT INSTALLED (Critical LPE patch missing)

Security Configuration:
- EDR Agent: Microsoft Defender for Endpoint v10.0.19045.1 (OUTDATED - 45 days old)
- Defender Antivirus: Enabled, Real-time Protection: ON
- Cloud Protection: Enabled (but agent outdated)
- Last Scan: 07:30:00 UTC (Clean, but scan may be incomplete)
- LAPS (Local Administrator Password Solution): NOT ENABLED
- Local Admin Account: Present (local_admin) - Password may be weak

User Accounts:
- mkt_user: Standard User (non-admin)
- local_admin: Local Administrator (weak password policy)

Vulnerability Assessment:
- Critical Findings: 1 (WIN-LPE-2022-XXXX - Unpatched Local Privilege Escalation)
- High Findings: 3
- Medium Findings: 5
- Local Privilege Escalation Vulnerabilities: DETECTED
  * CVE-2022-XXXX: Affects Windows 10 1903/1909 (Build 18362, 18363)
  * Patch Required: KB5001337 (NOT INSTALLED)
  * Exploit Availability: Public PoC available
  * Print Spooler Service: Running (vulnerable component active)

Risk Score: High (85/100)
WARNING: System is vulnerable to local privilege escalation. Outdated OS build and missing critical patch. High risk of successful privilege escalation.""",
            file_url="/api/artifacts/files/defender_ws-mkt-02_phase3.txt",
            notes_for_gm="Defender shows WS-MKT-02 is vulnerable with unpatched LPE."
        )
        db.add(artifact6_blue)
        db.flush()

        artifact7_blue = Artifact(
            name="Microsoft Sentinel - Vulnerability Scan Correlation",
            type=ArtifactType.INTEL_REPORT,
            description="""Microsoft Sentinel Incident Correlation
Incident ID: INC-2024-00234
Title: Privilege Escalation Risk Assessment

Vulnerability Scan Results (Microsoft Defender Vulnerability Management):

WS-FIN-01 (Finance):
- Overall Risk Score: Low (25/100)
- Patch Status: Fully patched through latest security updates
- LPE Vulnerabilities: 0
- EDR Coverage: Strong (latest agent)
- Recommendation: Low priority - system is hardened

WS-MKT-02 (Marketing):
- Overall Risk Score: High (85/100)
- Patch Status: Missing critical patch KB5001337
- LPE Vulnerabilities: 1 Critical (WIN-LPE-2022-XXXX)
- EDR Coverage: Weak (outdated agent, 45 days old)
- Recommendation: HIGH PRIORITY - Immediate patching required

Threat Intelligence:
- CVE-2022-XXXX has public exploit available
- Affects Windows 10 1903/1909 (Build 18362, 18363)
- Exploit combines with Print Spooler service for LPE
- WS-MKT-02 matches all vulnerability criteria

Recommendation: Prioritize containment and patching of WS-MKT-02. This system is at HIGH RISK of imminent privilege escalation.""",
            file_url="/api/artifacts/files/sentinel_vuln_correlation_phase3.txt",
            notes_for_gm="Sentinel shows WS-MKT-02 is high risk for privilege escalation."
        )
        db.add(artifact7_blue)
        db.flush()

        # Red Team Artifacts - Phase 3
        artifact5_red = Artifact(
            name="WS-FIN-01 System Information & Vulnerability Assessment",
            type=ArtifactType.TOOL_OUTPUT,
            description="""Target: WS-FIN-01 (Finance Department)

System Information Collected:
- OS: Windows 10 Enterprise Build 19045
- Install Date: 2022-06-15
- Hotfixes: KB5023696, KB5026361, KB5030219, KB5034123 (All latest)
- EDR Agent: Microsoft Defender for Endpoint v10.0.26100.1 (Latest)
- LAPS: ENABLED (Local admin passwords managed)
- Local Admin: PAM-managed (strong password, rotated)

Vulnerability Scan Results:
- Critical LPE Vulnerabilities: 0
- High Vulnerabilities: 0
- Medium Vulnerabilities: 0
- Exploitable Privilege Escalation Paths: NONE

Privilege Escalation Assessment:
- Generic token-stealing/UAC bypass: LOW SUCCESS PROBABILITY
  * Fully patched OS
  * Strong EDR monitoring
  * LAPS prevents weak local admin passwords
  * PAM-managed accounts difficult to compromise
- Estimated Success Rate: 20-30%
- Detection Risk: HIGH (strong EDR will likely detect)

Recommendation: This target is HARDENED. Privilege escalation will be difficult and high-risk. Consider alternative target.""",
            file_url="/api/artifacts/files/ws-fin-01_assessment_phase3.txt",
            notes_for_gm="Red Team sees WS-FIN-01 is hardened and difficult to escalate."
        )
        db.add(artifact5_red)
        db.flush()

        artifact6_red = Artifact(
            name="WS-MKT-02 System Information & Vulnerability Assessment",
            type=ArtifactType.TOOL_OUTPUT,
            description="""Target: WS-MKT-02 (Marketing Department)

System Information Collected:
- OS: Windows 10 Enterprise Build 18363 (OLD - 1903/1909)
- Install Date: 2019-09-03
- Hotfixes: KB4528760, KB4532693 (OLD)
- Missing Patch: KB5001337 (CRITICAL - LPE vulnerability)
- EDR Agent: Microsoft Defender for Endpoint v10.0.19045.1 (OUTDATED - 45 days old)
- LAPS: NOT ENABLED
- Local Admin: local_admin account present (weak password policy)

Vulnerability Scan Results:
- Critical LPE Vulnerabilities: 1 (WIN-LPE-2022-XXXX)
- High Vulnerabilities: 3
- Medium Vulnerabilities: 5
- Exploitable Privilege Escalation Paths: IDENTIFIED

Privilege Escalation Assessment:
- Specific LPE Exploit (CVE-2022-XXXX): HIGH SUCCESS PROBABILITY
  * OS Build 18363 matches vulnerable version
  * Missing patch KB5001337
  * Print Spooler service running (vulnerable component)
  * Public PoC available and tested
  * Outdated EDR agent may not detect modern exploits
- Estimated Success Rate: 80-90%
- Detection Risk: MEDIUM (outdated EDR, but may still detect)

Recommendation: This target is VULNERABLE. Specific LPE exploit available with high success probability. Best target for privilege escalation.""",
            file_url="/api/artifacts/files/ws-mkt-02_assessment_phase3.txt",
            notes_for_gm="Red Team sees WS-MKT-02 is vulnerable with specific LPE exploit."
        )
        db.add(artifact6_red)
        db.flush()

        artifact7_red = Artifact(
            name="Exploit Availability & Success Probability Analysis",
            type=ArtifactType.INTEL_REPORT,
            description="""Privilege Escalation Exploit Analysis

Target Comparison:

WS-FIN-01 (Finance):
- Exploit Method: Generic token-stealing/UAC bypass
- OS Build: 19045 (Latest, fully patched)
- LPE Vulnerabilities: None
- EDR Coverage: Strong (latest agent)
- Success Probability: 20-30%
- Detection Risk: HIGH
- Time to Escalate: 30-60 minutes (if successful)
- Recommendation: LOW PRIORITY - High risk, low reward

WS-MKT-02 (Marketing):
- Exploit Method: Specific LPE exploit (CVE-2022-XXXX)
- OS Build: 18363 (Vulnerable - missing KB5001337)
- LPE Vulnerabilities: 1 Critical (exploitable)
- EDR Coverage: Weak (outdated agent)
- Success Probability: 80-90%
- Detection Risk: MEDIUM
- Time to Escalate: 5-10 minutes (exploit is reliable)
- Recommendation: HIGH PRIORITY - High reward, manageable risk

Decision Matrix:
Focus escalation on WS-MKT-02. Specific exploit available with high success rate. WS-FIN-01 is hardened and low probability of success.""",
            file_url="/api/artifacts/files/exploit_analysis_phase3.txt",
            notes_for_gm="Red Team sees clear recommendation to focus on WS-MKT-02."
        )
        db.add(artifact7_red)
        db.flush()

        # Phase 4 Artifacts - Data Exfiltration (REDESIGNED with two-file-server decision)
        # Blue Team Artifacts - Microsoft Defender/E5 Security Stack
        artifact7_blue = Artifact(
            name="Microsoft Purview Data Loss Prevention - FS-01 (Finance) Monitoring",
            type=ArtifactType.LOG_SNIPPET,
            description="""Microsoft Purview Data Loss Prevention (DLP) Report
File Server: FS-01 (Finance File Server)
Monitoring Period: Last 24 hours

DLP Policy Coverage:
- Financial Data: STRONG (DLP policies active)
- Customer PII: STRONG (DLP policies active)
- Intellectual Property: STRONG (DLP policies active)
- Data Classification Labels: Applied to 95% of files

Network Monitoring:
- Microsoft Defender for Cloud Apps: ACTIVE
- Cloud App Security: Enabled
- Anomaly Detection: Enabled
- Real-time Monitoring: ACTIVE

Access Logs (Last 24 hours):
- Unusual Access Patterns: DETECTED
- Large File Transfers: DETECTED (270 GB)
- External Connections: DETECTED (185.220.101.45)
- DLP Alerts Generated: 12 HIGH-SEVERITY alerts
- Action Taken: ALERTED (investigation in progress)

Data Classification:
- Financial Records: 120 GB (High Sensitivity)
- Customer PII: 45 GB (Critical Sensitivity)
- Intellectual Property: 105 GB (Critical Sensitivity)
- Total Sensitive Data: 270 GB

Risk Assessment:
- Detection Risk: HIGH (strong DLP monitoring)
- Alert Status: MULTIPLE HIGH-SEVERITY alerts
- Investigation: ACTIVE
- Recommendation: IMMEDIATE CONTAINMENT REQUIRED

WARNING: FS-01 has strong DLP coverage and has generated multiple alerts. High detection risk.""",
            file_url="/api/artifacts/files/purview_fs-01_phase4.txt",
            notes_for_gm="Purview shows FS-01 has strong DLP and high detection risk."
        )
        db.add(artifact7_blue)
        db.flush()

        artifact8_blue = Artifact(
            name="Microsoft Purview Data Loss Prevention - FS-02 (HR/Operations) Monitoring",
            type=ArtifactType.LOG_SNIPPET,
            description="""Microsoft Purview Data Loss Prevention (DLP) Report
File Server: FS-02 (HR/Operations File Server)
Monitoring Period: Last 24 hours

DLP Policy Coverage:
- Employee Data: MEDIUM (DLP policies partially configured)
- HR Records: MEDIUM (DLP policies partially configured)
- Operational Documents: WEAK (limited DLP coverage)
- Data Classification Labels: Applied to 45% of files (many unclassified)

Network Monitoring:
- Microsoft Defender for Cloud Apps: ACTIVE
- Cloud App Security: Enabled
- Anomaly Detection: PARTIALLY ENABLED (coverage gaps)
- Real-time Monitoring: ACTIVE (but limited policy coverage)

Access Logs (Last 24 hours):
- Unusual Access Patterns: DETECTED (but fewer alerts)
- Large File Transfers: DETECTED (180 GB)
- External Connections: DETECTED (45.146.164.110)
- DLP Alerts Generated: 3 MEDIUM-SEVERITY alerts
- Action Taken: ALERTED (but lower priority due to medium severity)

Data Classification:
- Employee Records: 8.2 GB (Medium Sensitivity - many unclassified)
- HR Data: 45 GB (Medium Sensitivity)
- Operational Documents: 127 GB (Low-Medium Sensitivity - many unclassified)
- Total Sensitive Data: 180 GB (but 60% unclassified)

Risk Assessment:
- Detection Risk: MEDIUM (weaker DLP coverage, fewer alerts)
- Alert Status: MEDIUM-SEVERITY alerts (lower priority)
- Investigation: PENDING (not yet prioritized)
- Recommendation: Monitor but lower immediate priority

NOTE: FS-02 has weaker DLP coverage and fewer alerts generated. Lower detection risk but still concerning.""",
            file_url="/api/artifacts/files/purview_fs-02_phase4.txt",
            notes_for_gm="Purview shows FS-02 has weaker DLP and lower detection risk."
        )
        db.add(artifact8_blue)
        db.flush()

        artifact9_blue = Artifact(
            name="Microsoft Sentinel - Data Exfiltration Risk Correlation",
            type=ArtifactType.INTEL_REPORT,
            description="""Microsoft Sentinel Incident Correlation
Incident ID: INC-2024-00345
Title: Data Exfiltration Risk Assessment

File Server Comparison:

FS-01 (Finance):
- DLP Coverage: STRONG (95% of files classified)
- DLP Alerts: 12 HIGH-SEVERITY alerts
- Detection Risk: HIGH (strong monitoring, active investigation)
- Data Sensitivity: CRITICAL (financial, customer PII, IP)
- Network Monitoring: STRONG (Defender for Cloud Apps active)
- Recommendation: HIGH PRIORITY - Immediate containment required

FS-02 (HR/Operations):
- DLP Coverage: WEAK (45% of files classified, many unclassified)
- DLP Alerts: 3 MEDIUM-SEVERITY alerts
- Detection Risk: MEDIUM (weaker monitoring, lower priority)
- Data Sensitivity: MEDIUM (employee data, operational docs)
- Network Monitoring: ACTIVE but limited policy coverage
- Recommendation: MEDIUM PRIORITY - Monitor but lower immediate risk

Threat Intelligence:
- Both servers showing large data transfers
- FS-01: 270 GB transferred (HIGH-SEVERITY alerts)
- FS-02: 180 GB transferred (MEDIUM-SEVERITY alerts)
- External destinations: Cloud storage (Mega.nz, Dropbox)

Recommendation: Prioritize containment of FS-01 due to HIGH-SEVERITY alerts and critical data sensitivity. FS-02 requires monitoring but has lower immediate risk due to weaker DLP coverage.""",
            file_url="/api/artifacts/files/sentinel_exfiltration_risk_phase4.txt",
            notes_for_gm="Sentinel shows FS-01 is higher priority due to strong DLP alerts."
        )
        db.add(artifact9_blue)
        db.flush()

        # Red Team Artifacts - Phase 4
        artifact7_red = Artifact(
            name="FS-01 (Finance) Network Path & DLP Analysis",
            type=ArtifactType.INTEL_REPORT,
            description="""Target: FS-01 (Finance File Server)

Network Topology:
- Internal IP: 192.168.0.20
- Network Segment: Finance VLAN (isolated)
- Firewall Rules: Strict (limited outbound)
- Egress Path: Through proxy server (monitored)

Data Classification:
- Financial Records: 120 GB (High Sensitivity)
- Customer PII: 45 GB (Critical Sensitivity)
- Intellectual Property: 105 GB (Critical Sensitivity)
- Total: 270 GB of high-value data

DLP Coverage Analysis:
- Microsoft Purview DLP: ACTIVE
- Data Classification Labels: 95% of files labeled
- DLP Policies: STRONG (financial, PII, IP policies active)
- Monitoring: Real-time (Defender for Cloud Apps)
- Alert Threshold: LOW (sensitive to large transfers)

Exfiltration Risk Assessment:
- Detection Risk: HIGH
  * Strong DLP monitoring
  * 12 HIGH-SEVERITY alerts already generated
  * Real-time monitoring active
  * Investigation in progress
- Network Path: Monitored (proxy logs)
- Success Probability: 40-50% (high detection risk)
- Time to Detection: IMMINENT (alerts already generated)

Recommendation: HIGH-VALUE target but HIGH DETECTION RISK. DLP has already generated multiple alerts. Exfiltration likely to be detected and blocked.""",
            file_url="/api/artifacts/files/fs-01_analysis_phase4.txt",
            notes_for_gm="Red Team sees FS-01 has high-value data but high detection risk."
        )
        db.add(artifact7_red)
        db.flush()

        artifact8_red = Artifact(
            name="FS-02 (HR/Operations) Network Path & DLP Analysis",
            type=ArtifactType.INTEL_REPORT,
            description="""Target: FS-02 (HR/Operations File Server)

Network Topology:
- Internal IP: 192.168.0.21
- Network Segment: Operations VLAN (less isolated)
- Firewall Rules: Moderate (more permissive outbound)
- Egress Path: Direct internet access (less monitored)

Data Classification:
- Employee Records: 8.2 GB (Medium Sensitivity)
- HR Data: 45 GB (Medium Sensitivity)
- Operational Documents: 127 GB (Low-Medium Sensitivity)
- Total: 180 GB (60% unclassified, lower sensitivity)

DLP Coverage Analysis:
- Microsoft Purview DLP: PARTIALLY ACTIVE
- Data Classification Labels: 45% of files labeled (many unclassified)
- DLP Policies: WEAK (limited coverage, many gaps)
- Monitoring: Active but limited policy coverage
- Alert Threshold: MEDIUM (fewer alerts generated)

Exfiltration Risk Assessment:
- Detection Risk: MEDIUM
  * Weaker DLP monitoring
  * Only 3 MEDIUM-SEVERITY alerts generated
  * Limited policy coverage (many files unclassified)
  * Investigation pending (lower priority)
- Network Path: Less monitored (direct internet access)
- Success Probability: 70-80% (lower detection risk)
- Time to Detection: DELAYED (weaker monitoring, lower priority)

Recommendation: MEDIUM-VALUE target with LOWER DETECTION RISK. Weaker DLP coverage and fewer alerts. Better opportunity for successful exfiltration before detection.""",
            file_url="/api/artifacts/files/fs-02_analysis_phase4.txt",
            notes_for_gm="Red Team sees FS-02 has lower detection risk due to weaker DLP."
        )
        db.add(artifact8_red)
        db.flush()

        artifact9_red = Artifact(
            name="Data Exfiltration Strategy & Risk Comparison",
            type=ArtifactType.INTEL_REPORT,
            description="""Data Exfiltration Strategy Analysis

Target Comparison:

FS-01 (Finance):
- Data Value: HIGH (270 GB, critical sensitivity)
- DLP Coverage: STRONG (95% classified, active policies)
- Detection Risk: HIGH (12 HIGH-SEVERITY alerts already)
- Network Monitoring: STRONG (proxy monitored)
- Success Probability: 40-50%
- Time to Detection: IMMINENT
- Recommendation: HIGH-VALUE but HIGH-RISK. Likely to be detected and blocked.

FS-02 (HR/Operations):
- Data Value: MEDIUM (180 GB, lower sensitivity)
- DLP Coverage: WEAK (45% classified, limited policies)
- Detection Risk: MEDIUM (3 MEDIUM-SEVERITY alerts)
- Network Monitoring: MODERATE (direct internet, less monitored)
- Success Probability: 70-80%
- Time to Detection: DELAYED
- Recommendation: MEDIUM-VALUE but LOWER-RISK. Better opportunity for successful exfiltration.

Decision Matrix:
Prioritize FS-02 for exfiltration. Lower detection risk and higher success probability. FS-01 has already generated multiple HIGH-SEVERITY alerts and is likely to be blocked. FS-02 offers better opportunity to complete exfiltration before detection.""",
            file_url="/api/artifacts/files/exfiltration_strategy_phase4.txt",
            notes_for_gm="Red Team sees clear recommendation to prioritize FS-02."
        )
        db.add(artifact9_red)
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
        # Phase 1: Initial Compromise (REDESIGNED)
        # Blue Team sees: Defender alerts for both departments and Sentinel analysis
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact3_blue.id, team_role="blue"))
        # Red Team sees: reconnaissance reports for both departments and C2 status
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact3_red.id, team_role="red"))

        # Phase 2: Establishing Foothold
        # Blue Team sees: network scan and C2 traffic analysis
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact3_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_blue.id, team_role="blue"))
        # Red Team sees: recon results and persistence status
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact3_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_red.id, team_role="red"))

        # Phase 3: Privilege Escalation & Lateral Movement (REDESIGNED)
        # Blue Team sees: Defender system info for both hosts and Sentinel vulnerability correlation
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact7_blue.id, team_role="blue"))
        # Red Team sees: system assessments for both hosts and exploit analysis
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact7_red.id, team_role="red"))

        # Phase 4: Data Exfiltration (REDESIGNED)
        # Blue Team sees: Purview DLP reports for both servers and Sentinel correlation
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact9_blue.id, team_role="blue"))
        # Red Team sees: network/DLP analysis for both servers and strategy comparison
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact9_red.id, team_role="red"))

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

    # Create Tutorial Scenario
    tutorial_scenario = db.query(Scenario).filter(Scenario.name == "Tutorial: Basic Security Incident").first()
    if not tutorial_scenario:
        tutorial_scenario = Scenario(
            name="Tutorial: Basic Security Incident",
            description="A simple two-phase scenario designed to teach players how the game works. This tutorial covers the basic mechanics: reading briefings, reviewing artifacts, making decisions, and understanding team objectives. Perfect for first-time players.",
            miro_board_url="https://miro.com/app/board/tutorial"
        )
        db.add(tutorial_scenario)
        db.flush()

        # Phase 1: Initial Detection
        tutorial_phase1 = ScenarioPhase(
            scenario_id=tutorial_scenario.id,
            order_index=0,
            name="Phase 1: Initial Detection",
            briefing_text="Welcome to the Cyber Tabletop Tutorial! This scenario will walk you through how the game works.\n\n**The Situation:**\nAt 9:00 AM, your security operations center receives an alert from your email security gateway. An employee in the Marketing department clicked a suspicious link in an email. The email appeared to be from a legitimate vendor but contained a link to an external domain. Initial analysis shows the link attempted to download a file, but your email security blocked the download.\n\n**What You Need to Do:**\n1. Review the artifacts provided below\n2. Understand your team's objective\n3. Select an action that best aligns with your objective\n4. Rate how effective you think your organization would be at handling this (1-10 scale)\n5. Add any comments you'd like (optional, max 500 characters)\n6. Submit your decision\n\n**Remember:** This is a tutorial - focus on understanding the game mechanics rather than making the perfect decision.",
            red_objective="Tutorial Objective: Your goal is to establish initial access to the target network. The email link was blocked, but you may have other options. Review the artifacts to understand what happened and plan your next move. For this tutorial, focus on understanding how to read your objectives and make decisions.",
            blue_objective="Tutorial Objective: Your goal is to detect and contain the threat. The email was blocked, but you need to determine if any compromise occurred. Review the artifacts to understand what happened and decide on your response. For this tutorial, focus on understanding how to read your objectives and make decisions.",
            default_duration_seconds=600,  # 10 minutes for tutorial
            miro_frame_url="https://miro.com/app/board/tutorial/frame1"
        )
        db.add(tutorial_phase1)
        db.flush()

        # Phase 2: Response & Containment
        tutorial_phase2 = ScenarioPhase(
            scenario_id=tutorial_scenario.id,
            order_index=1,
            name="Phase 2: Response & Containment",
            briefing_text="**Phase 2: Response & Containment**\n\nGood work completing Phase 1! You've now seen how the game mechanics work.\n\n**The Situation Continues:**\nAfter reviewing the initial alert, your team has gathered more information. The email security gateway blocked the malicious download, but forensic analysis shows the user's workstation may have been compromised through a different vector. Network monitoring has detected unusual outbound connections from the Marketing department workstation.\n\n**What You Need to Do:**\n1. Review the new artifacts for this phase\n2. Consider what happened in Phase 1\n3. Make your decision for Phase 2\n4. Remember to rate your organization's effectiveness\n5. Submit your decision\n\n**Tutorial Tip:** Notice how the situation evolves between phases. Your decisions in Phase 1 may influence what happens in Phase 2. This is how the full game scenarios work!",
            red_objective="Tutorial Objective: You've successfully established a connection to the target workstation. Now you need to maintain access and avoid detection. Review the artifacts to see what the defenders have discovered and plan your next move. For this tutorial, focus on understanding how phases build upon each other.",
            blue_objective="Tutorial Objective: You've detected suspicious network activity from the Marketing workstation. You need to contain the threat and prevent further compromise. Review the artifacts to understand the full scope and decide on your containment strategy. For this tutorial, focus on understanding how phases build upon each other.",
            default_duration_seconds=600,  # 10 minutes for tutorial
            miro_frame_url="https://miro.com/app/board/tutorial/frame2"
        )
        db.add(tutorial_phase2)
        db.flush()

        # Create Tutorial Artifacts - Phase 1
        # Blue Team Artifacts
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

        # Red Team Artifacts - Phase 1
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
        # Blue Team Artifacts
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

        # Red Team Artifacts - Phase 2
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
        # Phase 1
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact1_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact2_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact1_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase1.id, artifact_id=tutorial_artifact2_red.id, team_role="red"))

        # Phase 2
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact3_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact4_blue.id, team_role="blue"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact3_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=tutorial_phase2.id, artifact_id=tutorial_artifact4_red.id, team_role="red"))

        db.commit()
        print("Created Tutorial scenario: Basic Security Incident with 2 phases and 8 artifacts (4 per team)")
    else:
        print("Tutorial scenario already exists")


if __name__ == "__main__":
    try:
        seed_data()
        print("Seed data created successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

