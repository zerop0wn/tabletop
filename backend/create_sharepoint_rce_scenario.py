"""
Create the SharePoint RCE Zero-Day Exploitation scenario.
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
    import generate_sharepoint_rce_artifacts as gen_module
    
    # Map function names to actual functions
    function_map = {
        'sharepoint_phase1_blue': gen_module.generate_sharepoint_phase1_blue,
        'sharepoint_phase1_blue2': gen_module.generate_sharepoint_phase1_blue2,
        'sharepoint_phase1_red': gen_module.generate_sharepoint_phase1_red,
        'sharepoint_phase1_red2': gen_module.generate_sharepoint_phase1_red2,
        'sharepoint_phase2_blue': gen_module.generate_sharepoint_phase2_blue,
        'sharepoint_phase2_blue2': gen_module.generate_sharepoint_phase2_blue2,
        'sharepoint_phase2_red': gen_module.generate_sharepoint_phase2_red,
        'sharepoint_phase2_red2': gen_module.generate_sharepoint_phase2_red2,
        'sharepoint_phase3_blue': gen_module.generate_sharepoint_phase3_blue,
        'sharepoint_phase3_blue2': gen_module.generate_sharepoint_phase3_blue2,
        'sharepoint_phase3_red': gen_module.generate_sharepoint_phase3_red,
        'sharepoint_phase3_red2': gen_module.generate_sharepoint_phase3_red2,
        'sharepoint_phase4_blue': gen_module.generate_sharepoint_phase4_blue,
        'sharepoint_phase4_blue2': gen_module.generate_sharepoint_phase4_blue2,
        'sharepoint_phase4_red': gen_module.generate_sharepoint_phase4_red,
        'sharepoint_phase4_red2': gen_module.generate_sharepoint_phase4_red2,
        'sharepoint_phase5_blue': gen_module.generate_sharepoint_phase5_blue,
        'sharepoint_phase5_blue2': gen_module.generate_sharepoint_phase5_blue2,
        'sharepoint_phase5_red': gen_module.generate_sharepoint_phase5_red,
        'sharepoint_phase5_red2': gen_module.generate_sharepoint_phase5_red2,
    }
    
    if function_name in function_map:
        return function_map[function_name]()
    else:
        return f"[Artifact content generation failed: {function_name}]"

try:
    # Check if scenario already exists
    scenario_name = "SharePoint RCE Zero-Day Exploitation"
    existing_scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if existing_scenario:
        print(f"Scenario '{scenario_name}' already exists (ID: {existing_scenario.id})")
        print("Delete it first if you want to recreate it.")
        sys.exit(0)
    
    print(f"Creating new scenario: {scenario_name}")
    
    # Create scenario
    scenario = Scenario(
        name=scenario_name,
        description="A new critical Remote Code Execution (RCE) vulnerability (CVE-2024-XXXXX) has been publicly disclosed affecting SharePoint Server 2019 and SharePoint Online. The vulnerability allows unauthenticated remote code execution through specially crafted HTTP requests. Your organization runs an external-facing SharePoint site for customer document collaboration. The security team must detect, contain, and remediate the threat while the Red Team attempts to exploit the vulnerability before patches are applied.\n\nKey Attack Vectors:\n- Vulnerability Disclosure: Microsoft Security Advisory published\n- Initial Reconnaissance: Version detection and endpoint mapping\n- RCE Exploitation: Unauthenticated code execution via crafted HTTP requests\n- Privilege Escalation: Gaining farm administrator access\n- Persistence: Web shells, scheduled tasks, backdoor accounts\n- Data Exfiltration: Accessing and stealing sensitive SharePoint documents\n- Remediation: Patching, cleanup, and breach assessment\n\nThe scenario tests both teams' ability to respond to zero-day vulnerabilities, detect exploitation attempts, contain compromises, and remediate security incidents. Each phase presents critical decision points where timely response and proper artifact analysis are essential.",
        miro_board_url="https://miro.com/app/board/example3"
    )
    db.add(scenario)
    db.flush()
    print(f"✓ Created scenario (ID: {scenario.id})")
    
    # Phase 1: Vulnerability Disclosure & Initial Reconnaissance
    phase1 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=0,
        name="Phase 1: Vulnerability Disclosure & Initial Reconnaissance",
        briefing_text="At 14:30 UTC, Microsoft published Security Advisory ADV240001 disclosing a critical RCE vulnerability (CVE-2024-XXXXX) affecting SharePoint Server 2019 and SharePoint Online. The vulnerability has a CVSS score of 9.8 (Critical) and is being actively exploited in the wild. Your organization's external SharePoint site (sharepoint.corp.com) is running SharePoint Server 2019 and is accessible from the internet. The security team has been notified, but no patch is available yet. Initial scans show your SharePoint server is vulnerable. The Red Team has begun reconnaissance to identify the exact version and configuration.\n\n**Your decision: How should you respond to this vulnerability disclosure?**\n\n**Remember:** Review the artifacts carefully. They contain the Microsoft security advisory, version detection results, and reconnaissance data. The artifacts will reveal the severity of the vulnerability, your server's vulnerability status, and potential attack indicators.",
        red_objective="Identify the exact SharePoint version and build number. Map the external attack surface including exposed endpoints, authentication mechanisms, and potential entry points. Test for the vulnerability without triggering security alerts. Gather information about the server configuration, installed features, and user accounts.",
        blue_objective="Monitor for exploitation attempts and reconnaissance activity. Identify any indicators of compromise (IOCs) from the vulnerability disclosure. Review SharePoint server logs for suspicious requests. Assess patch availability and prepare emergency mitigation procedures. Determine if the server is vulnerable and assess business impact.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example3/frame1",
        available_actions={
            "red": [
                {
                    "name": "Conduct version detection and endpoint mapping",
                    "description": "Identify the exact SharePoint version and map all exposed endpoints. Review artifacts to assess vulnerability status and identify optimal exploit paths."
                },
                {
                    "name": "Test vulnerability without detection",
                    "description": "Test the RCE vulnerability carefully to confirm exploitability while avoiding security alerts. Review artifacts to assess detection risk."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Prepare exploitation payload",
                    "description": "Prepare the RCE exploit payload and test WAF evasion techniques. Review artifacts to assess WAF bypass feasibility."
                },
                {
                    "name": "Gather server configuration details",
                    "description": "Collect information about server configuration, authentication methods, and network setup. Critical for planning exploitation."
                }
            ],
            "blue": [
                {
                    "name": "Monitor threat intelligence and assess vulnerability",
                    "description": "Review the Microsoft security advisory and assess if your SharePoint server is vulnerable. Review artifacts to determine vulnerability status and patch availability."
                },
                {
                    "name": "Review SharePoint logs for reconnaissance activity",
                    "description": "Examine SharePoint server logs and WAF logs for suspicious reconnaissance attempts. Review artifacts to identify potential attack indicators."
                },
                {
                    "name": "Prepare emergency mitigation procedures",
                    "description": "Develop and prepare mitigation procedures including WAF rules, network restrictions, and monitoring enhancements. Review artifacts to understand required mitigations."
                },
                {
                    "name": "Assess business impact and patch readiness",
                    "description": "Evaluate the business impact of taking the server offline and prepare for emergency patching when available. Review artifacts to understand patch timeline."
                },
                {
                    "name": "Update monitoring and alerting",
                    "description": "Enhance monitoring and alerting for SharePoint-specific attack patterns. Review artifacts to identify indicators to monitor."
                }
            ]
        }
    )
    db.add(phase1)
    db.flush()
    print(f"✓ Created Phase 1 (ID: {phase1.id})")
    
    # Phase 2: Exploitation Attempt & Initial Access
    phase2 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=1,
        name="Phase 2: Exploitation Attempt & Initial Access",
        briefing_text="The Red Team has successfully exploited the RCE vulnerability and gained initial access to the SharePoint server. Security logs show suspicious HTTP POST requests to /_layouts/15/upload.aspx with unusual payload patterns. The WAF (Web Application Firewall) initially blocked some requests but allowed others through. The attacker has executed PowerShell commands on the server and established a reverse shell connection. Endpoint detection on the SharePoint server (SP-SRV-01) has flagged unusual process activity including w3wp.exe spawning cmd.exe and powershell.exe processes.\n\n**Your decision: How should you respond to this exploitation and initial access?**\n\n**Remember:** Review the artifacts carefully. They contain WAF alerts, IIS logs showing RCE execution, and process activity. The artifacts will reveal the attack vector, confirm code execution, and help determine the appropriate containment response.",
        red_objective="Successfully exploit the RCE vulnerability to gain code execution on the SharePoint server. Establish a persistent reverse shell connection. Evade WAF and security tool detection. Begin enumeration of the server environment, installed software, network configuration, and domain membership.",
        blue_objective="Detect the exploitation attempt through log analysis and security tool alerts. Identify the attack vector and confirm RCE execution. Isolate the compromised SharePoint server from the network. Preserve forensic evidence including memory dumps and log files. Block the attacker's C2 communications.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example3/frame2",
        available_actions={
            "red": [
                {
                    "name": "Execute RCE exploit and establish reverse shell",
                    "description": "Exploit the RCE vulnerability to gain code execution and establish a reverse shell connection. Review artifacts to assess WAF evasion success and connection stability."
                },
                {
                    "name": "Enumerate server environment",
                    "description": "Gather information about the server environment, installed software, network configuration, and domain membership. Review artifacts to assess enumeration progress."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Evade WAF and security detection",
                    "description": "Use payload encoding and evasion techniques to bypass WAF rules and avoid security tool detection. Review artifacts to assess detection risk."
                },
                {
                    "name": "Prepare for privilege escalation",
                    "description": "Identify service accounts and privilege escalation opportunities. Review artifacts to assess privilege escalation feasibility."
                }
            ],
            "blue": [
                {
                    "name": "Isolate SharePoint server immediately",
                    "description": "Disconnect the compromised SharePoint server from the network to prevent further compromise and lateral movement. Review artifacts to confirm exploitation and determine isolation urgency."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather logs, memory dumps, and system artifacts for forensic analysis. Review artifacts to identify what evidence to collect."
                },
                {
                    "name": "Block attacker IP and C2 communications",
                    "description": "Block the attacker's source IP address and C2 server to terminate the reverse shell connection. Review artifacts to identify IP addresses to block."
                },
                {
                    "name": "Deploy countermeasures",
                    "description": "Implement additional WAF rules, network restrictions, and security controls. Review artifacts to identify required countermeasures."
                },
                {
                    "name": "Escalate to management",
                    "description": "Notify leadership and activate incident response procedures. Important for coordination but may slow immediate response."
                }
            ]
        }
    )
    db.add(phase2)
    db.flush()
    print(f"✓ Created Phase 2 (ID: {phase2.id})")
    
    # Phase 3: Privilege Escalation & Persistence
    phase3 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=2,
        name="Phase 3: Privilege Escalation & Persistence",
        briefing_text="The attacker has successfully escalated privileges on the SharePoint server. Security logs show the attacker has accessed the SharePoint farm administrator account and modified service accounts. The attacker has created scheduled tasks, installed web shells in multiple locations (/_layouts/15/, /_catalogs/, /Style Library/), and added backdoor user accounts to the SharePoint farm administrators group. The attacker has also established persistence through WMI event subscriptions and registry modifications. Network monitoring shows the attacker is attempting to move laterally to other systems in the domain.\n\n**Your decision: How should you respond to privilege escalation and persistence?**\n\n**Remember:** Review the artifacts carefully. They contain event logs showing privilege escalation, persistence mechanism detection reports, and attacker status updates. The artifacts will reveal all persistence mechanisms deployed and help determine the appropriate remediation response.",
        red_objective="Escalate to farm administrator privileges on the SharePoint server. Establish multiple persistence mechanisms (web shells, scheduled tasks, service modifications). Create backdoor accounts and maintain access even if discovered. Begin lateral movement reconnaissance to identify domain controllers, file servers, and other high-value targets.",
        blue_objective="Detect privilege escalation and persistence mechanisms. Identify all web shells, scheduled tasks, and backdoor accounts. Remove persistence mechanisms and revoke compromised credentials. Prevent lateral movement by isolating the SharePoint server and blocking outbound connections. Document all attacker modifications for forensic analysis.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example3/frame3",
        available_actions={
            "red": [
                {
                    "name": "Escalate to farm administrator",
                    "description": "Gain farm administrator privileges by accessing service account credentials. Review artifacts to assess privilege escalation success and access level."
                },
                {
                    "name": "Deploy multiple persistence mechanisms",
                    "description": "Install web shells, create scheduled tasks, and establish backdoor accounts. Review artifacts to assess persistence deployment success."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Reconnaissance for lateral movement",
                    "description": "Identify domain controllers, file servers, and other high-value targets for lateral movement. Review artifacts to assess network topology."
                },
                {
                    "name": "Maintain access through backdoors",
                    "description": "Ensure backdoor accounts and persistence mechanisms remain active. Review artifacts to assess access maintenance."
                }
            ],
            "blue": [
                {
                    "name": "Remove all persistence mechanisms",
                    "description": "Identify and remove all web shells, scheduled tasks, WMI subscriptions, and registry modifications. Review artifacts to identify all persistence mechanisms."
                },
                {
                    "name": "Revoke compromised credentials",
                    "description": "Reset service account passwords and remove backdoor accounts from SharePoint farm administrators. Review artifacts to identify compromised accounts."
                },
                {
                    "name": "Prevent lateral movement",
                    "description": "Isolate the SharePoint server and block outbound connections to prevent lateral movement. Review artifacts to assess lateral movement risk."
                },
                {
                    "name": "Document attacker modifications",
                    "description": "Document all attacker modifications for forensic analysis and incident reporting. Review artifacts to identify all changes."
                },
                {
                    "name": "Isolate server",
                    "description": "Disconnect the server from the network to contain the threat. Good containment but may be late if persistence already established."
                }
            ]
        }
    )
    db.add(phase3)
    db.flush()
    print(f"✓ Created Phase 3 (ID: {phase3.id})")
    
    # Phase 4: Data Access & Exfiltration
    phase4 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=3,
        name="Phase 4: Data Access & Exfiltration",
        briefing_text="The attacker has gained access to SharePoint site collections and document libraries. Security monitoring shows the attacker has accessed sensitive customer documents, employee data, and confidential project files. Network traffic analysis reveals large data transfers from the SharePoint server to external IP addresses (185.220.101.45, 45.146.164.110) using encrypted connections. Approximately 120 GB of data has been exfiltrated including customer contracts, employee PII, financial documents, and intellectual property. The attacker is using SharePoint's native APIs and PowerShell scripts to systematically download documents from multiple site collections.\n\n**Your decision: How should you respond to data access and exfiltration?**\n\n**Remember:** Review the artifacts carefully. They contain SharePoint access audit logs, network traffic analysis showing exfiltration, and data inventory reports. The artifacts will reveal what data was accessed, how much was exfiltrated, and help determine regulatory notification requirements.",
        red_objective="Access and catalog sensitive data stored in SharePoint site collections. Identify high-value targets including customer data, financial records, and intellectual property. Systematically exfiltrate data using multiple methods (SharePoint APIs, PowerShell, direct file access). Maintain access while exfiltrating data. Avoid detection by security monitoring tools.",
        blue_objective="Detect unauthorized data access and exfiltration attempts. Identify which site collections and documents have been accessed. Block data exfiltration by isolating the server and blocking outbound connections. Assess the scope of data breach including what data was accessed and exfiltrated. Prepare data breach notification procedures if required by regulations.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example3/frame4",
        available_actions={
            "red": [
                {
                    "name": "Access and catalog sensitive data",
                    "description": "Identify and catalog high-value data in SharePoint site collections. Review artifacts to assess data access success and identify valuable targets."
                },
                {
                    "name": "Exfiltrate data via multiple methods",
                    "description": "Systematically exfiltrate data using SharePoint APIs, PowerShell scripts, and web shells. Review artifacts to assess exfiltration progress and detection risk."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                },
                {
                    "name": "Maintain access during exfiltration",
                    "description": "Ensure persistence mechanisms remain active while exfiltrating data. Review artifacts to assess access maintenance."
                },
                {
                    "name": "Prioritize high-value data",
                    "description": "Focus on exfiltrating the most valuable data first (customer PII, financial records, IP). Review artifacts to identify high-value targets."
                }
            ],
            "blue": [
                {
                    "name": "Block data exfiltration immediately",
                    "description": "Isolate the server and block outbound connections to stop data exfiltration. Review artifacts to confirm exfiltration and determine blocking urgency."
                },
                {
                    "name": "Assess data breach scope",
                    "description": "Determine what data was accessed and exfiltrated, including data categories and record counts. Review artifacts to assess breach scope."
                },
                {
                    "name": "Prepare regulatory notifications",
                    "description": "Prepare data breach notifications for GDPR, CCPA, and other regulatory requirements. Review artifacts to determine notification requirements."
                },
                {
                    "name": "Isolate server",
                    "description": "Disconnect the server from the network to contain the breach. Good containment but may be late if exfiltration already occurred."
                },
                {
                    "name": "Collect forensic evidence",
                    "description": "Gather access logs, network traffic captures, and system artifacts for forensic analysis. Important but may not stop immediate exfiltration."
                }
            ]
        }
    )
    db.add(phase4)
    db.flush()
    print(f"✓ Created Phase 4 (ID: {phase4.id})")
    
    # Phase 5: Remediation & Post-Incident
    phase5 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=4,
        name="Phase 5: Remediation & Post-Incident",
        briefing_text="Microsoft has released an emergency security patch (KB5012345) for the SharePoint RCE vulnerability. The security team has identified all compromised systems and attacker modifications. The SharePoint server has been isolated, web shells removed, backdoor accounts deleted, and persistence mechanisms eliminated. The server has been patched and rebuilt from a clean backup. However, the attacker had access for 18 hours and exfiltrated 120 GB of sensitive data. The incident response team must now assess the full impact, determine if data breach notifications are required, and implement additional security controls to prevent future exploitation.\n\n**Your decision: How should you complete remediation and post-incident activities?**\n\n**Remember:** Review the artifacts carefully. They contain patch deployment status, data breach impact assessments, and attack summaries. The artifacts will reveal the full scope of the breach and help determine regulatory and legal obligations.",
        red_objective="Assess the success of the attack campaign including data exfiltrated, systems compromised, and persistence maintained. Document attack techniques and evasion methods that worked. Identify any remaining backdoors or access methods that weren't discovered. Prepare final attack summary report.",
        blue_objective="Complete remediation by patching all vulnerable systems and removing all attacker access. Conduct a full forensic investigation to determine the complete scope of the breach. Assess regulatory and legal obligations including data breach notifications (GDPR, CCPA, etc.). Implement additional security controls (WAF rules, network segmentation, monitoring). Create an after-action report with lessons learned and recommendations.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example3/frame5",
        available_actions={
            "red": [
                {
                    "name": "Assess attack success and document techniques",
                    "description": "Review the attack campaign results and document successful techniques. Review artifacts to assess overall attack success."
                },
                {
                    "name": "Cover tracks and hide remaining access",
                    "description": "Remove forensic artifacts and ensure any remaining backdoors are well-hidden. Review artifacts to assess detection risk."
                },
                {
                    "name": "Maintain persistence if possible",
                    "description": "Ensure any remaining persistence mechanisms remain active and undetected. Review artifacts to assess persistence status."
                },
                {
                    "name": "Prepare final attack report",
                    "description": "Document all attack activities, techniques used, and results achieved. Review artifacts to compile attack summary."
                },
                {
                    "name": "Identify remaining access methods",
                    "description": "Catalog any backdoors or access methods that may not have been discovered. Review artifacts to assess remaining access."
                }
            ],
            "blue": [
                {
                    "name": "Deploy security patches",
                    "description": "Apply the emergency security patch (KB5012345) to all vulnerable SharePoint servers. Review artifacts to confirm patch availability and deployment status."
                },
                {
                    "name": "Complete remediation and cleanup",
                    "description": "Remove all persistence mechanisms, revoke compromised credentials, and rebuild compromised systems. Review artifacts to identify all required remediation steps."
                },
                {
                    "name": "Conduct full forensic investigation",
                    "description": "Perform comprehensive forensic analysis to determine the complete scope of the breach. Review artifacts to assess breach impact."
                },
                {
                    "name": "Assess regulatory compliance requirements",
                    "description": "Determine regulatory and legal obligations including data breach notifications. Review artifacts to assess compliance requirements."
                },
                {
                    "name": "Create after-action report",
                    "description": "Document lessons learned, recommendations, and security improvements. Important for future prevention but secondary to immediate remediation."
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
    artifact1_blue = Artifact(
        name="Microsoft Security Advisory ADV240001",
        type=ArtifactType.EMAIL,
        description="Microsoft Security Advisory ADV240001 - Critical RCE Vulnerability in SharePoint. Contains vulnerability details, CVSS score, affected products, mitigation guidance, and patch status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase1_blue')
    )
    db.add(artifact1_blue)
    db.flush()
    
    artifact2_blue = Artifact(
        name="SharePoint Version Detection Report",
        type=ArtifactType.LOG_SNIPPET,
        description="SharePoint Server version detection report. Contains server information, vulnerability status, exposed endpoints, authentication configuration, and risk assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase1_blue2')
    )
    db.add(artifact2_blue)
    db.flush()
    
    artifact1_red = Artifact(
        name="SharePoint Reconnaissance Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team SharePoint reconnaissance report. Contains version information, exposed endpoints, authentication analysis, WAF status, and vulnerability testing results.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase1_red')
    )
    db.add(artifact1_red)
    db.flush()
    
    artifact2_red = Artifact(
        name="Vulnerability Verification Status",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team vulnerability verification report. Contains vulnerability status, target information, test results, exploit path details, and WAF evasion status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase1_red2')
    )
    db.add(artifact2_red)
    db.flush()
    
    # Phase 2 artifacts
    artifact3_blue = Artifact(
        name="WAF Alert - Suspicious POST Request",
        type=ArtifactType.LOG_SNIPPET,
        description="Cloudflare WAF alert log. Contains suspicious request details, WAF actions, rule effectiveness, and recommendations.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase2_blue')
    )
    db.add(artifact3_blue)
    db.flush()
    
    artifact4_blue = Artifact(
        name="SharePoint IIS Logs - RCE Execution",
        type=ArtifactType.LOG_SNIPPET,
        description="IIS log excerpt showing RCE exploitation. Contains request logs, process activity, network connections, and exploitation confirmation.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase2_blue2')
    )
    db.add(artifact4_blue)
    db.flush()
    
    artifact3_red = Artifact(
        name="RCE Exploitation Success Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team RCE exploitation success report. Contains exploitation timeline, access confirmation, and post-exploitation status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase2_red')
    )
    db.add(artifact3_red)
    db.flush()
    
    artifact4_red = Artifact(
        name="Server Environment Enumeration",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team server environment enumeration report. Contains hostname, OS, domain, installed software, network configuration, and SharePoint farm details.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase2_red2')
    )
    db.add(artifact4_red)
    db.flush()
    
    # Phase 3 artifacts
    artifact5_blue = Artifact(
        name="Privilege Escalation Event Logs",
        type=ArtifactType.LOG_SNIPPET,
        description="Windows Security Event Log showing privilege escalation. Contains successful logon events, special privileges assigned, directory service modifications, and SharePoint ULS logs.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase3_blue')
    )
    db.add(artifact5_blue)
    db.flush()
    
    artifact6_blue = Artifact(
        name="Persistence Mechanism Detection Report",
        type=ArtifactType.INTEL_REPORT,
        description="Persistence mechanism detection report. Contains web shells, scheduled tasks, backdoor accounts, WMI subscriptions, and registry modifications.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase3_blue2')
    )
    db.add(artifact6_blue)
    db.flush()
    
    artifact5_red = Artifact(
        name="Privilege Escalation Status",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team privilege escalation status report. Contains escalation method, privileges obtained, actions completed, persistence deployed, and lateral movement reconnaissance.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase3_red')
    )
    db.add(artifact5_red)
    db.flush()
    
    artifact6_red = Artifact(
        name="Persistence Deployment Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team persistence deployment report. Contains web shells, scheduled tasks, backdoor accounts, WMI subscriptions, and registry persistence.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase3_red2')
    )
    db.add(artifact6_red)
    db.flush()
    
    # Phase 4 artifacts
    artifact7_blue = Artifact(
        name="SharePoint Access Audit Logs",
        type=ArtifactType.LOG_SNIPPET,
        description="SharePoint access audit logs showing unauthorized access. Contains site collections accessed, access patterns, documents accessed, and sensitive data categories.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase4_blue')
    )
    db.add(artifact7_blue)
    db.flush()
    
    artifact8_blue = Artifact(
        name="Data Exfiltration Traffic Analysis",
        type=ArtifactType.LOG_SNIPPET,
        description="Network traffic analysis showing data exfiltration. Contains source/destination IPs, traffic patterns, data transfer methods, file types, and exfiltration status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase4_blue2')
    )
    db.add(artifact8_blue)
    db.flush()
    
    artifact7_red = Artifact(
        name="SharePoint Data Access Inventory",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team SharePoint data access inventory. Contains site collections accessed, document counts, high-value data identified, and exfiltration status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase4_red')
    )
    db.add(artifact7_red)
    db.flush()
    
    artifact8_red = Artifact(
        name="Data Exfiltration Progress Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team data exfiltration progress report. Contains total data exfiltrated, data categories, exfiltration methods, destinations, and completion status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase4_red2')
    )
    db.add(artifact8_red)
    db.flush()
    
    # Phase 5 artifacts
    artifact9_blue = Artifact(
        name="SharePoint Security Patch Deployment Status",
        type=ArtifactType.TOOL_OUTPUT,
        description="SharePoint security patch deployment status. Contains patch information, remediation actions completed, timeline, and deployment status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase5_blue')
    )
    db.add(artifact9_blue)
    db.flush()
    
    artifact10_blue = Artifact(
        name="Data Breach Impact Assessment",
        type=ArtifactType.INTEL_REPORT,
        description="Data breach impact assessment report. Contains breach summary, data categories breached, regulatory impact, and estimated costs.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase5_blue2')
    )
    db.add(artifact10_blue)
    db.flush()
    
    artifact9_red = Artifact(
        name="SharePoint RCE Attack Success Summary",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team attack success summary. Contains timeline, attack success metrics, techniques used, and overall mission status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase5_red')
    )
    db.add(artifact9_red)
    db.flush()
    
    artifact10_red = Artifact(
        name="Final Attack Report",
        type=ArtifactType.INTEL_REPORT,
        description="Red Team final attack report. Contains mission status, results, data value, attack timeline, and conclusions.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('sharepoint_phase5_red2')
    )
    db.add(artifact10_red)
    db.flush()
    
    # Associate artifacts with phases (team-specific)
    # Phase 1
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact1_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase1.id, artifact_id=artifact2_red.id, team_role="red"))
    
    # Phase 2
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact3_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact3_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase2.id, artifact_id=artifact4_red.id, team_role="red"))
    
    # Phase 3
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact5_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase3.id, artifact_id=artifact6_red.id, team_role="red"))
    
    # Phase 4
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact7_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase4.id, artifact_id=artifact8_red.id, team_role="red"))
    
    # Phase 5
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact9_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact10_blue.id, team_role="blue"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact9_red.id, team_role="red"))
    db.execute(scenario_phase_artifacts.insert().values(phase_id=phase5.id, artifact_id=artifact10_red.id, team_role="red"))
    
    db.commit()
    print(f"\n✓ Successfully created scenario '{scenario_name}' with {len(phases)} phases and {len(phases) * 4} artifacts")
    print(f"  Scenario ID: {scenario.id}")
    print(f"  Phase IDs: {[p.id for p in phases]}")
    
except Exception as e:
    db.rollback()
    print(f"Error creating scenario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

