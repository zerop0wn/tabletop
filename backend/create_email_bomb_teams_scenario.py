"""
Create the Email Bomb + Teams Call scenario: "Email Bomb & Social Engineering Attack"
This script creates a fresh scenario with 5 phases, detailed artifacts, and phase-specific actions.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Scenario, ScenarioPhase, Artifact, ArtifactType
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from pathlib import Path

# Get the scenario_phase_artifacts association table
from app.models import scenario_phase_artifacts

db: Session = SessionLocal()

# Helper function to get artifact content
def get_artifact_content(function_name: str) -> str:
    """Get artifact content by calling the generation function directly."""
    import generate_email_bomb_teams_artifacts as gen_module
    
    # Map function names to actual functions
    function_map = {
        'email_bomb_phase1_red': gen_module.generate_email_bomb_phase1_red,
        'email_bomb_phase1_blue': gen_module.generate_email_bomb_phase1_blue,
        'teams_call_phase2_red': gen_module.generate_teams_call_phase2_red,
        'teams_call_phase2_blue': gen_module.generate_teams_call_phase2_blue,
        'credential_harvesting_phase3_red': gen_module.generate_credential_harvesting_phase3_red,
        'credential_harvesting_phase3_blue': gen_module.generate_credential_harvesting_phase3_blue,
        'remote_access_phase4_red': gen_module.generate_remote_access_phase4_red,
        'remote_access_phase4_blue': gen_module.generate_remote_access_phase4_blue,
        'initial_access_phase5_red': gen_module.generate_initial_access_phase5_red,
        'initial_access_phase5_blue': gen_module.generate_initial_access_phase5_blue,
    }
    
    if function_name in function_map:
        return function_map[function_name]()
    else:
        return f"[Artifact content generation failed: {function_name}]"

try:
    # Check if scenario already exists
    scenario_name = "Email Bomb & Social Engineering Attack"
    existing_scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if existing_scenario:
        print(f"Scenario '{scenario_name}' already exists (ID: {existing_scenario.id})")
        print("Delete it first if you want to recreate it.")
        sys.exit(0)
    
    print(f"Creating new scenario: {scenario_name}")
    
    # Create scenario
    scenario = Scenario(
        name=scenario_name,
        description="A sophisticated social engineering attack combining email bombing with Teams call impersonation. The attack begins with an email bomb that overwhelms the victim's inbox, creating stress and anxiety. The attacker then impersonates IT support via a Teams call, convincing the victim to grant remote access and reveal credentials. This tactic has been observed in attacks linked to Black Basta ransomware and other threat actors.\n\nKey Attack Vectors:\n- Email Bomb: Overwhelming inbox with spam emails to create disruption\n- Teams Call Impersonation: Impersonating IT support to gain trust\n- Credential Harvesting: Obtaining passwords and MFA codes through social engineering\n- Remote Access: Gaining remote control via Quick Assist\n- Persistence: Establishing long-term access mechanisms\n- Initial Access: Deploying malware and establishing C2 communication\n\nThe scenario tests both teams' ability to detect social engineering tactics, respond to email floods, identify impersonation attempts, and prevent credential compromise. Each phase presents critical decision points where careful artifact analysis reveals the optimal response.",
        miro_board_url="https://miro.com/app/board/example"
    )
    db.add(scenario)
    db.flush()
    print(f"✓ Created scenario (ID: {scenario.id})")
    
    # Phase 1: Email Bomb Deployment
    phase1 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=0,
        name="Phase 1: Email Bomb Deployment",
        briefing_text="At 09:00 AM, a sophisticated email bomb attack has been launched against finance.director@corp.local. Over 800 emails have been sent to the target's inbox, with 623 emails successfully delivered (73.6% delivery rate). The email flood has overwhelmed the inbox, making it difficult for the user to find important messages.\n\nMicrosoft Defender for Office 365 has detected the email bomb and blocked 224 emails (26.4%), but the majority have been delivered. The user has reported being unable to find important financial documents and is experiencing significant productivity loss.\n\nSecurity monitoring shows:\n- 847 total emails sent in 12 minutes\n- 623 emails delivered (73.6%)\n- 224 emails blocked (26.4%)\n- Peak delivery rate: 87 emails per minute\n- User inbox: Overwhelmed and unusable\n\n**Your decision: How should you respond to this email bomb attack?**\n\n**Remember:** Review the artifacts carefully. They contain email volume analysis, sender reputation data, and user impact assessment. The artifacts will reveal the severity of the attack and help determine the appropriate response. This attack may be preparation for a follow-up social engineering attempt.",
        red_objective="Monitor the email bomb campaign effectiveness and assess user impact. Your goal is to verify the attack successfully overwhelmed the target's inbox and prepare for Phase 2 (Teams call impersonation) by ensuring the target is vulnerable and seeking assistance.",
        blue_objective="Assess the email bomb attack and determine the appropriate response. Your goal is to protect the user, prevent follow-up attacks, and maintain business operations. Be aware that email bombs are often used as preparation for social engineering attacks.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame1",
        available_actions={
            "red": [
                {
                    "name": "Monitor recipient engagement metrics",
                    "description": "Track user behavior and email client performance to assess operational effectiveness. Review artifacts to evaluate psychological impact and optimal timing for next phase."
                },
                {
                    "name": "Initialize VOIP infrastructure",
                    "description": "Prepare communication channels and support engagement protocols. Review artifacts to assess optimal timing and configuration parameters."
                },
                {
                    "name": "Maintain SMTP relay throughput",
                    "description": "Continue current email delivery operations at existing rate. Review artifacts to assess delivery metrics and infrastructure performance."
                },
                {
                    "name": "Increase message volume parameters",
                    "description": "Adjust sending rate configuration to maximize delivery throughput. Higher volume but may impact infrastructure stability and trigger security responses."
                },
                {
                    "name": "Execute log sanitization procedure",
                    "description": "Remove operational artifacts from system logs and clear command history. Reduces forensic visibility but may create suspicious gaps in audit trails."
                }
            ],
            "blue": [
                {
                    "name": "Collect EOP telemetry data",
                    "description": "Gather email logs, sender reputation data, and threat intelligence feeds for analysis. Critical for understanding attack infrastructure but time-consuming process."
                },
                {
                    "name": "Initiate user security awareness protocol",
                    "description": "Contact user to provide security guidance and threat awareness. Review artifacts to assess attack severity and user risk level."
                },
                {
                    "name": "Update transport rule policies",
                    "description": "Modify email filtering rules and sender reputation thresholds. Review artifacts to identify suspicious sender patterns and domains."
                },
                {
                    "name": "Enable enhanced monitoring protocols",
                    "description": "Deploy additional monitoring and alerting for potential follow-up activity. Proactive defense measure but may not prevent immediate threats."
                },
                {
                    "name": "Execute account isolation procedure",
                    "description": "Temporarily restrict email account access to prevent further message delivery. Conservative approach that may impact business operations."
                }
            ]
        }
    )
    db.add(phase1)
    db.flush()
    print(f"✓ Created Phase 1 (ID: {phase1.id})")
    
    # Phase 2: Teams Call Impersonation
    phase2 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=1,
        name="Phase 2: Teams Call Impersonation",
        briefing_text="At 09:18 AM, approximately 6 minutes after the email bomb peak, a Teams call was placed to finance.director@corp.local. The caller claimed to be IT support and referenced the email bomb attack, offering to help secure the account.\n\nThe caller used an external phone number (+1-555-IT-SUPPORT) but identified themselves as \"IT Support - Corp IT Department\". The call lasted 4 minutes and 32 seconds, during which the caller convinced the user to grant remote access via Quick Assist.\n\nSecurity monitoring shows:\n- External Teams call from unrecognized number\n- Caller claimed to be IT support\n- User granted remote access via Quick Assist\n- Screen share active for 3+ minutes\n- Suspicious actions observed during remote session\n\n**Your decision: How should you respond to this Teams call impersonation?**\n\n**Remember:** Review the artifacts carefully. They contain call analysis, caller verification data, and remote access activity logs. The artifacts will reveal whether this is a legitimate IT support call or a social engineering attack. The timing (immediately after email bomb) is highly suspicious.",
        red_objective="Maintain remote access session and continue social engineering to build trust. Your goal is to keep the user convinced you are legitimate IT support and maintain remote control via Quick Assist while preparing for credential harvesting.",
        blue_objective="Identify this Teams call as a social engineering attack and prevent the attacker from gaining remote access. Your goal is to protect the user and terminate any unauthorized remote sessions.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame2",
        available_actions={
            "red": [
                {
                    "name": "Monitor user response",
                    "description": "Track user behavior and trust indicators during engagement. Review artifacts to assess trust level and adjust operational tactics accordingly."
                },
                {
                    "name": "Establish remote assistance session",
                    "description": "Initiate support workflow and configure remote desktop protocol access. Review artifacts to assess user trust level and optimal engagement approach."
                },
                {
                    "name": "Intensify social engineering",
                    "description": "Apply enhanced persuasion techniques to increase user compliance. Higher success probability but may raise suspicion if tactics are too aggressive."
                },
                {
                    "name": "Execute log sanitization procedure",
                    "description": "Remove operational artifacts from system logs and clear command history. Reduces forensic visibility but may create suspicious gaps in audit trails."
                },
                {
                    "name": "Initiate credential collection workflow",
                    "description": "Begin identity verification process during active session. Higher risk approach but may provide immediate access credentials."
                }
            ],
            "blue": [
                {
                    "name": "Review Teams call logs and caller metadata",
                    "description": "Analyze call records, caller identification data, and phone number verification. Review artifacts to confirm if this is legitimate IT support or impersonation."
                },
                {
                    "name": "Terminate active remote assistance connections",
                    "description": "Immediately disconnect Quick Assist sessions and block remote access protocols. Review artifacts to confirm unauthorized remote access activity."
                },
                {
                    "name": "Disable remote support protocols",
                    "description": "Block Quick Assist and other remote assistance tools at the system level. Conservative approach that may impact legitimate IT support operations."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather Teams call logs, remote access activity logs, and system modification records. Critical for understanding the attack but time-consuming process."
                },
                {
                    "name": "Enable credential harvesting monitoring",
                    "description": "Deploy monitoring for potential credential collection attempts. Proactive defense measure but may not stop immediate threats."
                }
            ]
        }
    )
    db.add(phase2)
    db.flush()
    print(f"✓ Created Phase 2 (ID: {phase2.id})")
    
    # Phase 3: Credential Harvesting
    phase3 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=2,
        name="Phase 3: Credential Harvesting",
        briefing_text="During the Teams call and remote access session, the attacker requested the user's corporate password and MFA code, claiming it was needed to \"verify account security\". The user complied, providing their email password, Windows password, and approving an MFA request.\n\nMicrosoft Defender for Identity has detected suspicious credential entry during the remote access session. The credentials have been validated, and the attacker has successfully logged into the user's account from an external IP address.\n\nSecurity monitoring shows:\n- Password entered in visible text field during remote session\n- MFA push notification approved by user\n- Successful login from external IP (185.220.101.45)\n- Account access confirmed (email, OneDrive, Teams)\n\n**Your decision: How should you respond to this credential compromise?**\n\n**Remember:** Review the artifacts carefully. They contain credential entry detection data, login attempt logs, and account access information. The artifacts will reveal the extent of the compromise and help determine the appropriate response. Immediate action is required to secure the account.",
        red_objective="Validate obtained credentials and test account access. Your goal is to confirm the harvested credentials work and use them to gain full account access for the next phase.",
        blue_objective="Detect and prevent credential harvesting during the remote access session. Your goal is to secure the compromised account and prevent unauthorized access.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame3",
        available_actions={
            "red": [
                {
                    "name": "Execute log sanitization procedure",
                    "description": "Remove operational artifacts from system logs and clear command history. Reduces forensic visibility but may create suspicious gaps in audit trails."
                },
                {
                    "name": "Perform account verification procedure",
                    "description": "Execute identity validation workflow to obtain authentication credentials. Review artifacts to assess user trust level and session status."
                },
                {
                    "name": "Deploy authentication capture module",
                    "description": "Install keylogging capabilities to capture credentials as user types. Lower suspicion approach but requires additional tool deployment."
                },
                {
                    "name": "Initiate credential validation process",
                    "description": "Test obtained authentication artifacts to confirm account access. Critical operational step for proceeding to next phase."
                },
                {
                    "name": "Execute credential extraction utility",
                    "description": "Deploy tool to extract saved passwords from system credential stores. Higher detection risk but may provide additional authentication artifacts."
                }
            ],
            "blue": [
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather credential entry logs, login attempt records, and account access telemetry. Critical for understanding the attack but time-consuming process."
                },
                {
                    "name": "Execute credential rotation procedure",
                    "description": "Immediately force password reset and revoke all active authentication sessions. Review artifacts to confirm credential compromise."
                },
                {
                    "name": "Initiate account security remediation",
                    "description": "Reset authentication tokens and deploy account protection measures. Review artifacts to assess MFA compromise and account access status."
                },
                {
                    "name": "Review account activity logs",
                    "description": "Analyze all account activity across email, OneDrive, and Teams to identify accessed resources. Critical for understanding compromise scope."
                },
                {
                    "name": "Enable persistence mechanism monitoring",
                    "description": "Deploy monitoring for potential long-term access mechanisms. Proactive defense measure but may not stop immediate threats."
                }
            ]
        }
    )
    db.add(phase3)
    db.flush()
    print(f"✓ Created Phase 3 (ID: {phase3.id})")
    
    # Phase 4: Remote Access & Persistence
    phase4 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=3,
        name="Phase 4: Remote Access & Persistence",
        briefing_text="With remote access established and credentials obtained, the attacker has deployed multiple persistence mechanisms to maintain long-term access. Microsoft Defender for Endpoint has detected suspicious scheduled tasks, registry modifications, email forwarding rules, and startup folder items.\n\nSecurity monitoring shows:\n- Scheduled task created (\"WindowsUpdateService\")\n- Registry run key modified (\"MicrosoftEdgeUpdate\")\n- Email forwarding rule created (forwards financial emails to external address)\n- Startup folder item added (edgeupdate.vbs)\n- Malware files deployed (update.ps1, cred.exe, scan.exe)\n\n**Your decision: How should you respond to these persistence mechanisms?**\n\n**Remember:** Review the artifacts carefully. They contain persistence mechanism details, malware detection data, and system modification logs. The artifacts will reveal which persistence methods were deployed and which present the highest ongoing risk. Immediate removal is critical to prevent long-term compromise.",
        red_objective="Verify persistence mechanisms are active and test reliability. Your goal is to confirm all deployed persistence methods are functioning correctly and prepare for C2 communication setup.",
        blue_objective="Identify and remove all persistence mechanisms to prevent the attacker from maintaining long-term access. Your goal is to fully remediate the compromise and prevent re-infection.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame4",
        available_actions={
            "red": [
                {
                    "name": "Execute log sanitization procedure",
                    "description": "Remove operational artifacts from system logs and clear command history. Reduces forensic visibility but may create suspicious gaps in audit trails."
                },
                {
                    "name": "Configure scheduled task automation",
                    "description": "Create scheduled task entries to execute code automatically on system events. Review artifacts to assess detection risk and reliability."
                },
                {
                    "name": "Modify registry startup parameters",
                    "description": "Update Windows Registry run keys to execute code on user login. Review artifacts to assess detection risk and persistence reliability."
                },
                {
                    "name": "Deploy email routing configuration",
                    "description": "Create email forwarding rules to redirect sensitive messages. Review artifacts to assess detection risk and data exfiltration value."
                },
                {
                    "name": "Initialize payload deployment",
                    "description": "Deploy PowerShell scripts and executables for remote communication. Higher detection risk but provides command and control capabilities."
                }
            ],
            "blue": [
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather persistence mechanism logs, malware samples, and system modification records. Critical for understanding the attack but time-consuming process."
                },
                {
                    "name": "Execute persistence removal procedure",
                    "description": "Immediately remove scheduled tasks, registry keys, email rules, and startup items. Review artifacts to identify all persistence mechanisms."
                },
                {
                    "name": "Quarantine detected malware artifacts",
                    "description": "Isolate and remove all detected malicious files and scripts. Review artifacts to identify all malicious components."
                },
                {
                    "name": "Terminate remote access sessions",
                    "description": "Disconnect Quick Assist sessions and block remote access tools. Review artifacts to confirm remote access status."
                },
                {
                    "name": "Execute network isolation protocol",
                    "description": "Disconnect compromised device from network to prevent lateral movement. Conservative approach that may impact business operations."
                }
            ]
        }
    )
    db.add(phase4)
    db.flush()
    print(f"✓ Created Phase 4 (ID: {phase4.id})")
    
    # Phase 5: Initial Access & C2 Establishment
    phase5 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=4,
        name="Phase 5: Initial Access & C2 Communication",
        briefing_text="The attacker has successfully executed the payload and established a Command and Control (C2) connection to an external server. Microsoft Defender for Endpoint has detected C2 communication to IP address 185.220.101.45 on port 443 (HTTPS).\n\nSecurity monitoring shows:\n- C2 connection established (09:29:45 UTC)\n- Regular beacon traffic (every 5 minutes)\n- 2.3 MB data uploaded to C2 server\n- 156 KB data downloaded from C2 server\n- Payload execution confirmed (update.ps1)\n- Remote command execution capabilities active\n\n**Your decision: How should you respond to this C2 communication?**\n\n**Remember:** Review the artifacts carefully. They contain C2 communication logs, network traffic analysis, and payload execution data. The artifacts will reveal the extent of the compromise and help determine the appropriate response. Immediate containment is required to prevent data exfiltration and lateral movement.",
        red_objective="Verify C2 connection stability and execute reconnaissance commands. Your goal is to confirm the C2 channel is functional and begin network reconnaissance for lateral movement and data exfiltration.",
        blue_objective="Detect and terminate C2 communication to prevent the attacker from maintaining remote control. Your goal is to isolate the compromised device, block C2 traffic, and prevent data exfiltration.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame5",
        available_actions={
            "red": [
                {
                    "name": "Execute log sanitization procedure",
                    "description": "Remove operational artifacts from system logs and clear command history. Reduces forensic visibility but may create suspicious gaps in audit trails."
                },
                {
                    "name": "Verify C2 channel stability",
                    "description": "Test command and control connection reliability and functionality. Review artifacts to assess network connectivity and detection risk."
                },
                {
                    "name": "Execute credential extraction utility",
                    "description": "Run credential dumper tool to harvest additional saved credentials. Review artifacts to assess detection risk and credential availability."
                },
                {
                    "name": "Initiate network reconnaissance scan",
                    "description": "Execute network scanning tool to identify vulnerable systems. Review artifacts to assess network access and detection risk."
                },
                {
                    "name": "Begin data transfer operations",
                    "description": "Start exfiltrating sensitive data via established communication channel. Higher value operation but increases detection risk."
                }
            ],
            "blue": [
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather C2 communication logs, network traffic captures, and payload samples. Critical for understanding the attack but time-consuming process."
                },
                {
                    "name": "Execute network isolation protocol",
                    "description": "Immediately disconnect compromised device from network to prevent C2 communication and lateral movement. Review artifacts to confirm C2 activity."
                },
                {
                    "name": "Deploy firewall blocking rules",
                    "description": "Block C2 server IP address at network perimeter to terminate communication. Review artifacts to identify C2 server address."
                },
                {
                    "name": "Terminate malicious process execution",
                    "description": "Stop all malicious processes and payload execution. Review artifacts to identify all malicious processes."
                },
                {
                    "name": "Analyze data exfiltration patterns",
                    "description": "Review network traffic and system logs to determine exfiltrated data scope. Critical for understanding impact and breach notification requirements."
                }
            ]
        }
    )
    db.add(phase5)
    db.flush()
    print(f"✓ Created Phase 5 (ID: {phase5.id})")
    
    # Create artifacts for each phase
    phases = [phase1, phase2, phase3, phase4, phase5]
    
    # Phase 1 artifacts
    artifact1_red = Artifact(
        name="Email Bomb Campaign Status Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team email bomb campaign status report. Contains delivery statistics, user impact assessment, and readiness for Phase 2.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('email_bomb_phase1_red')
    )
    db.add(artifact1_red)
    db.flush()
    
    artifact1_blue = Artifact(
        name="Defender for Office 365 Email Bomb Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Office 365 alert for email bomb attack. Contains email volume analysis, sender reputation, and user impact assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('email_bomb_phase1_blue')
    )
    db.add(artifact1_blue)
    db.flush()
    
    # Phase 2 artifacts
    artifact2_red = Artifact(
        name="Teams Call Impersonation Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team Teams call impersonation report. Contains call execution details, social engineering tactics, and remote access establishment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('teams_call_phase2_red')
    )
    db.add(artifact2_red)
    db.flush()
    
    artifact2_blue = Artifact(
        name="Defender for Office 365 Teams Call Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Office 365 / Teams security alert. Contains call analysis, caller verification, and remote access activity detection.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('teams_call_phase2_blue')
    )
    db.add(artifact2_blue)
    db.flush()
    
    # Phase 3 artifacts
    artifact3_red = Artifact(
        name="Credential Harvesting Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team credential harvesting report. Contains credentials obtained, MFA bypass details, and account access confirmation.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('credential_harvesting_phase3_red')
    )
    db.add(artifact3_red)
    db.flush()
    
    artifact3_blue = Artifact(
        name="Defender for Identity Credential Harvesting Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Identity alert for credential harvesting. Contains credential entry detection, login attempt logs, and account access information.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('credential_harvesting_phase3_blue')
    )
    db.add(artifact3_blue)
    db.flush()
    
    # Phase 4 artifacts
    artifact4_red = Artifact(
        name="Remote Access & Persistence Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team remote access and persistence establishment report. Contains persistence mechanisms deployed, payload deployment, and system reconnaissance.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('remote_access_phase4_red')
    )
    db.add(artifact4_red)
    db.flush()
    
    artifact4_blue = Artifact(
        name="Defender for Endpoint Persistence Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint alert for persistence mechanisms. Contains scheduled task, registry, email rule, and malware detection details.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('remote_access_phase4_blue')
    )
    db.add(artifact4_blue)
    db.flush()
    
    # Phase 5 artifacts
    artifact5_red = Artifact(
        name="Initial Access & C2 Establishment Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team initial access and C2 establishment report. Contains C2 connection status, payload execution, and remote control capabilities.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('initial_access_phase5_red')
    )
    db.add(artifact5_red)
    db.flush()
    
    artifact5_blue = Artifact(
        name="Defender for Endpoint C2 Communication Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="Microsoft Defender for Endpoint alert for C2 communication. Contains C2 connection logs, network traffic analysis, and payload execution data.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('initial_access_phase5_blue')
    )
    db.add(artifact5_blue)
    db.flush()
    
    # Associate artifacts with phases (team-specific)
    # Phase 1
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_blue.id, team_role="blue"))
    
    # Phase 2
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact2_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact2_blue.id, team_role="blue"))
    
    # Phase 3
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact3_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact3_blue.id, team_role="blue"))
    
    # Phase 4
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact4_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact4_blue.id, team_role="blue"))
    
    # Phase 5
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact5_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact5_blue.id, team_role="blue"))
    
    db.commit()
    print(f"\n✓ Successfully created scenario '{scenario_name}' with {len(phases)} phases and {len(phases) * 2} artifacts")
    print(f"  Scenario ID: {scenario.id}")
    print(f"  Phase IDs: {[p.id for p in phases]}")
    
except Exception as e:
    db.rollback()
    print(f"Error creating scenario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

