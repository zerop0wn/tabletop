"""
Create the Operation Inbox Overload scenario: "Operation Inbox Overload"
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

# Helper function to get artifact content (placeholder - implement artifact generation later)
def get_artifact_content(function_name: str) -> str:
    """Get artifact content by calling the generation function directly."""
    # TODO: Create artifact generation module similar to generate_email_bomb_teams_artifacts.py
    # For now, return placeholder
    return f"[Artifact content for {function_name} - TODO: implement artifact generation]"

try:
    # Check if scenario already exists
    scenario_name = "Operation Inbox Overload"
    existing_scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if existing_scenario:
        print(f"Scenario '{scenario_name}' already exists (ID: {existing_scenario.id})")
        print("Delete it first if you want to recreate it.")
        sys.exit(0)
    
    print(f"Creating new scenario: {scenario_name}")
    
    # Create scenario
    scenario = Scenario(
        name=scenario_name,
        description="A sophisticated email bomb attack followed by callback social engineering via Teams. The attacker floods the target's inbox with believable emails from look-alike IT domains, creating panic and driving the user to seek help. The attacker then impersonates IT support via Teams to gain remote access, harvest credentials, and establish persistence. This scenario focuses on identity and endpoint containment decisions, with 'Disable account' and 'Isolate host' as critical Blue Team responses.",
        miro_board_url="https://miro.com/app/board/example"
    )
    db.add(scenario)
    db.flush()
    print(f"✓ Created scenario (ID: {scenario.id})")
    
    # Phase 0: Email Flood Disruption
    phase0 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=0,
        name="Phase 0: Email Flood Disruption",
        briefing_text="At 09:00 AM, a coordinated email flood attack has been launched against finance.director@corp.local. Over 1,200 emails have been delivered in the past 30 minutes, overwhelming the inbox. The emails appear to be from IT support domains (it-support@corp-it.local, helpdesk@corp-support.net) but analysis shows they're from look-alike domains designed to appear legitimate.\n\nMicrosoft Defender for Office 365 has detected the email flood and blocked some messages, but the majority have been delivered. The user cannot find important emails and is experiencing significant disruption.\n\nSecurity monitoring shows:\n- 1,247 total emails sent in 30 minutes\n- 892 emails delivered (71.5%)\n- 355 emails blocked (28.5%)\n- Emails from look-alike IT domains (no suspicious links)\n- User inbox: Overwhelmed and unusable\n\n**Your decision: How should you respond to this email flood?**\n\n**Remember:** Review the artifacts carefully. They contain email volume analysis, sender domain analysis, and user impact assessment. The artifacts will reveal whether this is a simple spam flood or preparation for a follow-up social engineering callback attack.",
        red_objective="Create believable inbox overload using look-alike IT domains without suspicious links. Your goal is to make the emails appear legitimate enough to avoid immediate spam filtering while creating enough disruption to drive the user to seek help.",
        blue_objective="Assess the email flood and determine the appropriate containment response. Your goal is to protect the user, prevent follow-up attacks, and maintain business operations. Be aware that email floods are often used as preparation for callback social engineering attacks.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame0",
        available_actions={
            "red": [
                {
                    "name": "Use look-alike IT domain without links",
                    "description": "Send emails from domains that closely resemble legitimate IT support domains, but without any links or attachments. Review artifacts to assess delivery success and believability."
                },
                {
                    "name": "Vary sender display name and timing",
                    "description": "Use different sender display names and vary timing patterns to improve deliverability and avoid pattern detection. Review artifacts to assess stealth effectiveness."
                },
                {
                    "name": "Send from generic/free mailbox",
                    "description": "Use generic or free email services to send the flood. Lower credibility but easier to set up. Review artifacts to assess delivery rates."
                },
                {
                    "name": "Include suspicious links in email body",
                    "description": "Include links in the email body to increase engagement. Higher risk of triggering phishing detection engines. Review artifacts to assess detection risk."
                }
            ],
            "blue": [
                {
                    "name": "Purge messages and block sending domain",
                    "description": "Immediately purge all messages from the flood and block the sending domains at the transport rule level. Review artifacts to identify all sending domains."
                },
                {
                    "name": "Notify affected users about suspicious emails",
                    "description": "Send security awareness notifications to affected users warning about the email flood. Important for user awareness but may not prevent immediate follow-up attacks."
                },
                {
                    "name": "Block sender address only",
                    "description": "Block individual sender email addresses. Easy to bypass by using different addresses. Review artifacts to assess effectiveness."
                },
                {
                    "name": "Do nothing and continue monitoring",
                    "description": "Continue monitoring the situation without taking action. Allows the attack to continue and may enable follow-up social engineering."
                }
            ]
        }
    )
    db.add(phase0)
    db.flush()
    print(f"✓ Created Phase 0 (ID: {phase0.id})")
    
    # Phase 1: Panic Driven Help-Seeking
    phase1 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=1,
        name="Phase 1: Panic Driven Help-Seeking",
        briefing_text="At 09:35 AM, approximately 5 minutes after the email flood peak, the user has reached out for help. They've sent a Teams message to IT support asking about the email issue. The user is frustrated and needs immediate assistance to access important emails.\n\nSecurity monitoring shows:\n- User sent Teams message to IT support channel\n- User expressing urgency and frustration\n- User asking for immediate help\n- No legitimate IT support ticket created\n\n**Your decision: How should you respond to this help-seeking behavior?**\n\n**Remember:** Review the artifacts carefully. They contain user communication patterns, timing analysis, and context about the email flood. The artifacts will reveal whether this is legitimate user frustration or if an attacker is preparing to impersonate IT support.",
        red_objective="Establish contact with the user and position yourself as the fastest path to help. Your goal is to build trust and prepare for the callback impersonation by making the user believe you are legitimate IT support.",
        blue_objective="Provide proactive communication to prevent the user from falling for callback social engineering. Your goal is to warn users about the attack and prevent them from trusting unsolicited IT support contacts.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame1",
        available_actions={
            "red": [
                {
                    "name": "Send Teams DM first, then place a call",
                    "description": "Send a Teams direct message to the user first to establish contact, then place a call. Review artifacts to assess optimal timing and trust-building approach."
                },
                {
                    "name": "Call user directly with no prior context",
                    "description": "Call the user directly without prior Teams contact. Faster but may be more suspicious. Review artifacts to assess user receptiveness."
                },
                {
                    "name": "Send additional email claiming IT will call",
                    "description": "Send an email to the user claiming IT support will call them. Adds noise and may reduce trust. Review artifacts to assess effectiveness."
                },
                {
                    "name": "Send Teams message with external support link",
                    "description": "Send a Teams message with a link to an external support portal. High risk of triggering security detection. Review artifacts to assess detection risk."
                }
            ],
            "blue": [
                {
                    "name": "Send org-wide Teams broadcast about phishing/callback",
                    "description": "Send an organization-wide Teams broadcast warning about the email flood and potential callback social engineering attacks. Review artifacts to assess attack scope and urgency."
                },
                {
                    "name": "Reset user password only",
                    "description": "Reset the user's password as a precautionary measure. Addresses identity risk but doesn't address user awareness. Review artifacts to assess necessity."
                },
                {
                    "name": "Disable user account preemptively",
                    "description": "Temporarily disable the user account to prevent compromise. Strong containment but may be heavy-handed at this early stage. Review artifacts to assess risk level."
                },
                {
                    "name": "Do nothing and continue monitoring",
                    "description": "Continue monitoring without taking action. Allows the attack to progress and may enable successful callback. Review artifacts to assess risk."
                }
            ]
        }
    )
    db.add(phase1)
    db.flush()
    print(f"✓ Created Phase 1 (ID: {phase1.id})")
    
    # Phase 2: Teams Impersonation Callback
    phase2 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=2,
        name="Phase 2: Teams Impersonation Callback",
        briefing_text="At 09:42 AM, a Teams call was placed to finance.director@corp.local. The caller claimed to be IT support responding to the email issue. The caller used an external phone number but identified themselves as 'IT Support - Corp IT Department'.\n\nThe call lasted 6 minutes, during which the caller convinced the user to share their screen to 'show the email issue'. The user granted screen share access via Teams.\n\nSecurity monitoring shows:\n- External Teams call from unrecognized number\n- Caller claimed to be IT support\n- User granted screen share access\n- Screen share active for 4+ minutes\n- Caller viewing user's email client and settings\n\n**Your decision: How should you respond to this Teams impersonation callback?**\n\n**Remember:** Review the artifacts carefully. They contain call analysis, caller verification data, and screen share activity logs. The artifacts will reveal whether this is legitimate IT support or a social engineering attack. The timing (immediately after email flood) is highly suspicious.",
        red_objective="Maintain the screen share session and build trust with the user. Your goal is to convince the user you are legitimate IT support and prepare for credential harvesting in the next phase.",
        blue_objective="Identify this Teams call as a social engineering attack and prevent the attacker from gaining further access. Your goal is to protect the user and terminate any unauthorized screen share sessions.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame2",
        available_actions={
            "red": [
                {
                    "name": "Ask user to share screen to show the issue",
                    "description": "Request the user to share their screen so you can see the email issue. Review artifacts to assess user trust level and optimal approach."
                },
                {
                    "name": "Provide fake ticket number and internal jargon",
                    "description": "Use fake ticket numbers and internal IT jargon to build credibility. Good for trust but doesn't provide direct access. Review artifacts to assess effectiveness."
                },
                {
                    "name": "Ask user directly for MFA reset code",
                    "description": "Directly ask the user for their MFA reset code. Higher risk but may provide immediate access. Review artifacts to assess user receptiveness."
                },
                {
                    "name": "Ask user to install remote support tool",
                    "description": "Ask the user to install a remote support tool. Highly suspicious and may trigger user suspicion. Review artifacts to assess detection risk."
                }
            ],
            "blue": [
                {
                    "name": "Disable user account immediately",
                    "description": "Immediately disable the user account to prevent further compromise. Review artifacts to confirm this is a social engineering attack."
                },
                {
                    "name": "Validate caller via Teams tenant and internal directory",
                    "description": "Verify the caller's identity through Teams tenant data and internal directory. Review artifacts for caller verification information."
                },
                {
                    "name": "Allow screen share with external caller",
                    "description": "Allow the screen share to continue while monitoring. Exposes sensitive information to the attacker. Review artifacts to assess risk."
                },
                {
                    "name": "Monitor call and collect more evidence only",
                    "description": "Continue monitoring the call without taking action. Gives the attacker time to proceed with their attack. Review artifacts to assess risk."
                }
            ]
        }
    )
    db.add(phase2)
    db.flush()
    print(f"✓ Created Phase 2 (ID: {phase2.id})")
    
    # Phase 3: MFA Reset Attempt & Endpoint Foothold
    phase3 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=3,
        name="Phase 3: MFA Reset Attempt & Endpoint Foothold",
        briefing_text="During the screen share session, the attacker guided the user to navigate to Security and Privacy settings. The user has approved an MFA reset request, and the attacker now has access to the user's account.\n\nMicrosoft Defender for Identity has detected the MFA reset and suspicious account access. The attacker has successfully logged into the user's account from an external IP address and is accessing email, OneDrive, and Teams.\n\nSecurity monitoring shows:\n- MFA reset approved by user during screen share\n- Successful login from external IP (185.220.101.45)\n- Account access confirmed (email, OneDrive, Teams)\n- Active session from unrecognized device\n\n**Your decision: How should you respond to this MFA compromise and account takeover?**\n\n**Remember:** Review the artifacts carefully. They contain MFA reset detection data, login attempt logs, and account access information. The artifacts will reveal the extent of the compromise and help determine whether to focus on identity containment (disable account) or endpoint containment (isolate host).",
        red_objective="Maintain access to the compromised account and establish a foothold on the endpoint. Your goal is to use the account access to deploy persistence mechanisms and prepare for long-term access.",
        blue_objective="Contain both the identity compromise and any endpoint foothold. Your goal is to secure the compromised account and prevent the attacker from maintaining access to systems or data.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame3",
        available_actions={
            "red": [
                {
                    "name": "Trick user into approving MFA reset prompt",
                    "description": "Guide the user to approve an MFA reset prompt during the screen share. Review artifacts to assess user trust level and session status."
                },
                {
                    "name": "Ask user to navigate to Security and Privacy settings",
                    "description": "Direct the user to navigate to account security settings. Good step toward MFA reset but doesn't provide immediate access. Review artifacts to assess progress."
                },
                {
                    "name": "Access SharePoint/OneDrive from compromised session",
                    "description": "Access SharePoint and OneDrive data using the compromised account session. Gets data but doesn't provide long-term control. Review artifacts to assess data value."
                },
                {
                    "name": "Attempt to install malicious support application",
                    "description": "Try to install a malicious application on the user's device. High chance of user suspicion and detection. Review artifacts to assess detection risk."
                }
            ],
            "blue": [
                {
                    "name": "Isolate host in Defender for Endpoint",
                    "description": "Immediately isolate the user's host device in Defender for Endpoint. Stops active hands-on-keyboard access and preserves evidence. Review artifacts to confirm endpoint compromise."
                },
                {
                    "name": "Disable user account",
                    "description": "Immediately disable the user account to prevent further account access. Strong identity containment but doesn't address endpoint risk. Review artifacts to assess compromise scope."
                },
                {
                    "name": "Revoke active sessions only",
                    "description": "Revoke all active authentication sessions for the account. Better than nothing but doesn't address endpoint or long-term persistence. Review artifacts to assess effectiveness."
                },
                {
                    "name": "Take no action until more logs are collected",
                    "description": "Continue collecting logs without taking containment action. Allows the attacker to proceed with their attack. Review artifacts to assess risk."
                }
            ]
        }
    )
    db.add(phase3)
    db.flush()
    print(f"✓ Created Phase 3 (ID: {phase3.id})")
    
    # Phase 4: Persistence vs Containment
    phase4 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=4,
        name="Phase 4: Persistence vs Containment",
        briefing_text="With account access established, the attacker is attempting to create persistence mechanisms to maintain long-term access. Microsoft Defender for Office 365 has detected suspicious mailbox rules, app password creation attempts, and conditional access policy changes.\n\nSecurity monitoring shows:\n- App password creation attempt detected\n- Mailbox forwarding rule creation attempt\n- Conditional access policy modification attempt\n- Token refresh attempts from external IP\n\n**Your decision: How should you respond to these persistence attempts?**\n\n**Remember:** Review the artifacts carefully. They contain persistence mechanism detection data, token activity logs, and policy change records. The artifacts will reveal which persistence methods are being attempted and which present the highest ongoing risk. Full token revocation and conditional access blocking is required to break all persistence.",
        red_objective="Establish persistence mechanisms that survive account password resets and session revocations. Your goal is to create app passwords, mailbox rules, or other mechanisms that provide long-term access even if the account is secured.",
        blue_objective="Break all persistence mechanisms and harden the account against future compromise. Your goal is to revoke all tokens, block conditional access, and ensure the attacker cannot regain access even if they have credentials.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example/frame4",
        available_actions={
            "red": [
                {
                    "name": "Create app password for IMAP/legacy auth",
                    "description": "Create an app password that bypasses MFA for IMAP or legacy authentication protocols. Review artifacts to assess detection risk and persistence reliability."
                },
                {
                    "name": "Create mailbox forwarding rule to external address",
                    "description": "Create an email forwarding rule that sends all emails to an external address. Good for long-term data exfiltration. Review artifacts to assess detection risk."
                },
                {
                    "name": "Perform one-time data exfiltration only",
                    "description": "Exfiltrate data in a single operation without establishing persistence. Gets data but doesn't provide long-term access. Review artifacts to assess data value."
                },
                {
                    "name": "Attempt another MFA reset after being blocked",
                    "description": "Try to perform another MFA reset after previous attempts were blocked. Noisy and likely to fail. Review artifacts to assess success probability."
                }
            ],
            "blue": [
                {
                    "name": "Full token revoke and add Conditional Access block",
                    "description": "Revoke all authentication tokens and add a conditional access policy block for the account. Breaks all persistence and hardens future access. Review artifacts to identify all tokens and access methods."
                },
                {
                    "name": "Disable user account only",
                    "description": "Disable the user account to stop immediate abuse. Good containment but doesn't address token-based persistence or policy hardening. Review artifacts to assess persistence scope."
                },
                {
                    "name": "Reset user password only",
                    "description": "Reset the user's password. Addresses credential-based access but leaves tokens and app passwords active. Review artifacts to assess token activity."
                },
                {
                    "name": "Enable extra logging and auditing only",
                    "description": "Enable additional logging and auditing without taking containment action. Observation only, doesn't stop the attack. Review artifacts to assess risk."
                }
            ]
        }
    )
    db.add(phase4)
    db.flush()
    print(f"✓ Created Phase 4 (ID: {phase4.id})")
    
    # Create artifacts for each phase (placeholder - implement artifact generation later)
    phases = [phase0, phase1, phase2, phase3, phase4]
    
    # Create placeholder artifacts for each phase
    for phase_idx, phase in enumerate(phases):
        # Red Team artifact
        artifact_red = Artifact(
            name=f"Phase {phase_idx} Red Team Report",
            type=ArtifactType.TOOL_OUTPUT,
            description=f"Red Team operational report for Phase {phase_idx}.",
            file_url=None,
            embed_url=None,
            content=get_artifact_content(f'phase{phase_idx}_red')
        )
        db.add(artifact_red)
        db.flush()
        
        # Blue Team artifact
        artifact_blue = Artifact(
            name=f"Phase {phase_idx} Blue Team Alert",
            type=ArtifactType.LOG_SNIPPET,
            description=f"Microsoft Defender alert for Phase {phase_idx}.",
            file_url=None,
            embed_url=None,
            content=get_artifact_content(f'phase{phase_idx}_blue')
        )
        db.add(artifact_blue)
        db.flush()
        
        # Associate artifacts with phases
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase.id, artifact_id=artifact_red.id, team_role="red"))
        db.execute(scenario_phase_artifacts.insert().values(phase_id=phase.id, artifact_id=artifact_blue.id, team_role="blue"))
    
    db.commit()
    print(f"\n✓ Successfully created scenario '{scenario_name}' with {len(phases)} phases")
    print(f"  Scenario ID: {scenario.id}")
    print(f"  Phase IDs: {[p.id for p in phases]}")
    
except Exception as e:
    db.rollback()
    print(f"Error creating scenario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

