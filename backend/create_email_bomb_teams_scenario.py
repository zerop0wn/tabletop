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
        red_objective="Monitor the email bomb campaign to ensure it successfully overwhelms the target's inbox and creates the desired psychological state (stress, anxiety, need for help). Your goal is to prepare the target for Phase 2 (Teams call impersonation) by making them vulnerable and seeking assistance.",
        blue_objective="Assess the email bomb attack and determine the appropriate response. Your goal is to protect the user, prevent follow-up attacks, and maintain business operations. Be aware that email bombs are often used as preparation for social engineering attacks.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame1",
        available_actions={
            "red": [
                {
                    "name": "Continue email bomb campaign",
                    "description": "Maintain the email bomb to keep the target's inbox overwhelmed. Review artifacts to assess delivery success and user impact."
                },
                {
                    "name": "Intensify email bomb",
                    "description": "Increase email volume to further overwhelm the target. Higher impact but may trigger stronger security responses."
                },
                {
                    "name": "Prepare Teams call",
                    "description": "Prepare for Phase 2 by setting up Teams call infrastructure and social engineering scripts. Review artifacts to assess optimal timing."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Monitor user response",
                    "description": "Monitor user behavior and email client performance to assess psychological impact. Critical for timing Phase 2."
                }
            ],
            "blue": [
                {
                    "name": "Contact user and warn about social engineering",
                    "description": "Immediately contact the user to warn them about potential follow-up social engineering attacks (phone calls, Teams calls). Review artifacts to assess attack severity."
                },
                {
                    "name": "Enhance email filtering",
                    "description": "Implement stricter email filtering rules to block additional spam emails. Review artifacts to identify suspicious sender domains."
                },
                {
                    "name": "Isolate user's email account",
                    "description": "Temporarily isolate the user's email account to prevent further email delivery. Conservative approach but may impact business operations."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather email logs, sender data, and threat intelligence for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Monitor for follow-up attacks",
                    "description": "Monitor user's account and systems for potential follow-up social engineering attempts. Proactive defense but may not stop immediate threats."
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
        red_objective="Execute the Teams call impersonation to establish trust and gain remote access to the target's system. Your goal is to convince the user you are legitimate IT support and obtain remote control via Quick Assist.",
        blue_objective="Identify this Teams call as a social engineering attack and prevent the attacker from gaining remote access. Your goal is to protect the user and terminate any unauthorized remote sessions.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame2",
        available_actions={
            "red": [
                {
                    "name": "Execute Teams call and request remote access",
                    "description": "Place the Teams call, impersonate IT support, and request remote access via Quick Assist. Review artifacts to assess user trust level and optimal timing."
                },
                {
                    "name": "Intensify social engineering",
                    "description": "Use more aggressive social engineering tactics to gain user trust. Higher success rate but may raise suspicion."
                },
                {
                    "name": "Request credentials during call",
                    "description": "Attempt to harvest credentials during the Teams call. Higher risk but may provide immediate access."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Monitor user response",
                    "description": "Monitor user behavior during the call to assess trust level and adjust social engineering tactics accordingly."
                }
            ],
            "blue": [
                {
                    "name": "Contact user and terminate remote session",
                    "description": "Immediately contact the user to verify the Teams call and instruct them to disconnect Quick Assist. Review artifacts to confirm this is a social engineering attack."
                },
                {
                    "name": "Block Quick Assist",
                    "description": "Disable or block Quick Assist to prevent unauthorized remote access. Conservative approach but may impact legitimate IT support."
                },
                {
                    "name": "Investigate caller identity",
                    "description": "Verify the caller's identity and phone number to confirm if this is legitimate IT support or an impersonation attempt. Review artifacts for caller verification data."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather Teams call logs, remote access activity, and system logs for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Monitor for credential harvesting",
                    "description": "Monitor user's account and systems for potential credential harvesting attempts. Proactive defense but may not stop immediate threats."
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
        red_objective="Harvest credentials from the target during the remote access session. Your goal is to obtain the user's corporate password and MFA code to gain full account access.",
        blue_objective="Detect and prevent credential harvesting during the remote access session. Your goal is to secure the compromised account and prevent unauthorized access.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame3",
        available_actions={
            "red": [
                {
                    "name": "Request credentials during remote session",
                    "description": "Ask the user for their password and MFA code during the Teams call, claiming it's needed for account verification. Review artifacts to assess user trust level."
                },
                {
                    "name": "Use keylogging",
                    "description": "Use keylogging capabilities to capture credentials as the user types. Lower suspicion but requires additional tools."
                },
                {
                    "name": "Deploy credential dumper",
                    "description": "Deploy a credential dumper tool to extract saved passwords from the system. Higher detection risk but may provide additional credentials."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Validate credentials",
                    "description": "Test the obtained credentials to confirm account access. Critical for proceeding to next phase."
                }
            ],
            "blue": [
                {
                    "name": "Force password reset immediately",
                    "description": "Immediately force a password reset for the compromised account and revoke all active sessions. Review artifacts to confirm credential compromise."
                },
                {
                    "name": "Disable MFA temporarily",
                    "description": "Temporarily disable MFA to prevent further MFA bypass attempts, then re-enable with a new method. Review artifacts to assess MFA compromise."
                },
                {
                    "name": "Review account activity",
                    "description": "Review all account activity (email, OneDrive, Teams) to identify what the attacker accessed. Critical for understanding the compromise."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather credential entry logs, login attempt logs, and account access logs for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Monitor for persistence",
                    "description": "Monitor the user's system and account for potential persistence mechanisms. Proactive defense but may not stop immediate threats."
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
        red_objective="Establish persistence mechanisms to maintain access even if the initial compromise is discovered. Your goal is to deploy multiple persistence methods that provide reliable long-term access with low detection risk.",
        blue_objective="Identify and remove all persistence mechanisms to prevent the attacker from maintaining long-term access. Your goal is to fully remediate the compromise and prevent re-infection.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame4",
        available_actions={
            "red": [
                {
                    "name": "Deploy scheduled task persistence",
                    "description": "Create a scheduled task that runs malicious code automatically. Review artifacts to assess detection risk and reliability."
                },
                {
                    "name": "Deploy registry persistence",
                    "description": "Modify Windows Registry to execute code on login. Review artifacts to assess detection risk and reliability."
                },
                {
                    "name": "Deploy email forwarding rule",
                    "description": "Create an email forwarding rule to exfiltrate sensitive emails. Review artifacts to assess detection risk and data value."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Deploy payloads",
                    "description": "Deploy malware payloads (PowerShell scripts, executables) for C2 communication. Higher detection risk but provides remote control."
                }
            ],
            "blue": [
                {
                    "name": "Remove all persistence mechanisms",
                    "description": "Immediately remove scheduled tasks, registry keys, email rules, and startup items. Review artifacts to identify all persistence methods."
                },
                {
                    "name": "Quarantine malware",
                    "description": "Quarantine all detected malware files (update.ps1, cred.exe, scan.exe, edgeupdate.vbs). Review artifacts to identify all malicious files."
                },
                {
                    "name": "Terminate remote session",
                    "description": "Disconnect Quick Assist session and block remote access tools. Review artifacts to confirm remote access status."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather persistence mechanism logs, malware samples, and system modification logs for analysis. Critical for understanding the attack but takes time."
                },
                {
                    "name": "Isolate device",
                    "description": "Disconnect the compromised device from the network to prevent lateral movement. Conservative approach but may impact business operations."
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
        red_objective="Establish C2 communication to gain remote control of the compromised system. Your goal is to deploy payloads, establish persistent C2 connection, and prepare for lateral movement and data exfiltration.",
        blue_objective="Detect and terminate C2 communication to prevent the attacker from maintaining remote control. Your goal is to isolate the compromised device, block C2 traffic, and prevent data exfiltration.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame5",
        available_actions={
            "red": [
                {
                    "name": "Establish C2 connection",
                    "description": "Deploy payload and establish C2 communication with external server. Review artifacts to assess network connectivity and detection risk."
                },
                {
                    "name": "Execute credential dumper",
                    "description": "Execute cred.exe to harvest additional saved credentials from the system. Review artifacts to assess detection risk and credential availability."
                },
                {
                    "name": "Scan internal network",
                    "description": "Execute scan.exe to identify vulnerable systems for lateral movement. Review artifacts to assess network access and detection risk."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Exfiltrate data",
                    "description": "Begin exfiltrating sensitive financial data via C2 connection. Higher value but increases detection risk."
                }
            ],
            "blue": [
                {
                    "name": "Isolate device immediately",
                    "description": "Immediately disconnect the compromised device from the network to prevent C2 communication and lateral movement. Review artifacts to confirm C2 activity."
                },
                {
                    "name": "Block C2 server",
                    "description": "Block the C2 server IP (185.220.101.45) at the firewall to terminate C2 communication. Review artifacts to identify C2 server address."
                },
                {
                    "name": "Terminate malicious processes",
                    "description": "Terminate all malicious processes (powershell.exe, cred.exe, scan.exe) to stop payload execution. Review artifacts to identify all malicious processes."
                },
                {
                    "name": "Investigate data exfiltration",
                    "description": "Review network traffic and system logs to determine what data was exfiltrated (2.3 MB uploaded). Critical for understanding the impact."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather C2 communication logs, network traffic captures, and payload samples for analysis. Critical for understanding the attack but takes time."
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

