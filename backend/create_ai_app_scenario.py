"""
Create the AI Application Data Leakage & Permission Misconfiguration scenario.
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
    import generate_ai_app_artifacts as gen_module
    
    # Map function names to actual functions
    function_map = {
        'ai_app_phase1_blue': gen_module.generate_ai_app_phase1_blue,
        'ai_app_phase1_blue2': gen_module.generate_ai_app_phase1_blue2,
        'ai_app_phase1_red': gen_module.generate_ai_app_phase1_red,
        'ai_app_phase1_red2': gen_module.generate_ai_app_phase1_red2,
        'ai_app_phase2_blue': gen_module.generate_ai_app_phase2_blue,
        'ai_app_phase2_blue2': gen_module.generate_ai_app_phase2_blue2,
        'ai_app_phase2_red': gen_module.generate_ai_app_phase2_red,
        'ai_app_phase2_red2': gen_module.generate_ai_app_phase2_red2,
        'ai_app_phase3_blue': gen_module.generate_ai_app_phase3_blue,
        'ai_app_phase3_blue2': gen_module.generate_ai_app_phase3_blue2,
        'ai_app_phase3_red': gen_module.generate_ai_app_phase3_red,
        'ai_app_phase3_red2': gen_module.generate_ai_app_phase3_red2,
        'ai_app_phase4_blue': gen_module.generate_ai_app_phase4_blue,
        'ai_app_phase4_blue2': gen_module.generate_ai_app_phase4_blue2,
        'ai_app_phase4_red': gen_module.generate_ai_app_phase4_red,
        'ai_app_phase4_red2': gen_module.generate_ai_app_phase4_red2,
        'ai_app_phase5_blue': gen_module.generate_ai_app_phase5_blue,
        'ai_app_phase5_blue2': gen_module.generate_ai_app_phase5_blue2,
        'ai_app_phase5_red': gen_module.generate_ai_app_phase5_red,
        'ai_app_phase5_red2': gen_module.generate_ai_app_phase5_red2,
    }
    
    if function_name in function_map:
        return function_map[function_name]()
    else:
        return f"[Artifact content generation failed: {function_name}]"

try:
    # Check if scenario already exists
    scenario_name = "AI Application Data Leakage & Permission Misconfiguration"
    existing_scenario = db.query(Scenario).filter(Scenario.name == scenario_name).first()
    
    if existing_scenario:
        print(f"Scenario '{scenario_name}' already exists (ID: {existing_scenario.id})")
        print("Delete it first if you want to recreate it.")
        sys.exit(0)
    
    print(f"Creating new scenario: {scenario_name}")
    
    # Create scenario
    scenario = Scenario(
        name=scenario_name,
        description="Your organization has developed an internal AI application called 'CorpAI Assistant' that acts as a wrapper for external AI services (Claude and ChatGPT). The application is designed to help staff analyze internal documents and extract insights. However, security concerns have emerged around permissions and data leakage. The application integrates with SharePoint, OneDrive, and file servers to access documents, but permission misconfigurations allow unauthorized access to sensitive data. Additionally, the application lacks proper data loss prevention (DLP) controls for AI API responses, allowing sensitive information to be extracted through prompt injection attacks.\n\nKey Security Issues:\n- Permission Misconfiguration: Permission inheritance override allows standard users to access documents beyond their role\n- Missing DLP: No data loss prevention for AI API responses\n- Prompt Injection: Vulnerable to prompt injection attacks that bypass filtering\n- Incomplete Audit Logging: Only 85% of operations are logged\n- Insufficient Rate Limiting: API rate limits are too high (1,000 requests/hour)\n\nThe scenario tests both teams' ability to detect unauthorized access, identify permission misconfigurations, prevent data leakage through AI APIs, and remediate security issues. Each phase presents critical decision points where proper artifact analysis and timely response are essential.",
        miro_board_url="https://miro.com/app/board/example4"
    )
    db.add(scenario)
    db.flush()
    print(f"✓ Created scenario (ID: {scenario.id})")
    
    # Phase 1: Initial Detection - Suspicious AI API Activity
    phase1 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=0,
        name="Phase 1: Initial Detection - Suspicious AI API Activity",
        briefing_text="At 10:30 UTC, the security team receives an alert about unusual activity in the CorpAI Assistant application. API usage has increased dramatically - from a normal baseline of ~200 requests per day to 2,847 requests in just 2 hours. Token usage has spiked to 2.3 million tokens (normal: ~200K tokens/day), and 847 documents have been accessed, far exceeding the normal ~50 documents per day. The documents being accessed include sensitive categories like HR records, financial data, legal contracts, customer PII, and intellectual property. Multiple user accounts (12 different accounts) are showing unusual activity patterns.\n\n**Your decision: How should you respond to this suspicious AI API activity?**\n\n**Remember:** Review the artifacts carefully. They contain API usage alerts, access control audit reports, and reconnaissance data. The artifacts will reveal the scope of the activity, potential permission issues, and help determine if this is unauthorized access or a legitimate surge in usage.",
        red_objective="Reconnaissance the AI application to understand its architecture, authentication mechanisms, and access controls. Test document access permissions to identify misconfigurations. Map available document sources and categories. Identify potential vulnerabilities in permission inheritance and document filtering.",
        blue_objective="Investigate the unusual API activity and determine if it represents a security threat. Review access control configurations and audit logs. Assess whether the activity is legitimate or indicates unauthorized access. Determine the scope of documents being accessed and identify any permission misconfigurations.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example4/frame1",
        available_actions={
            "red": [
                {
                    "name": "Reconnaissance AI application architecture",
                    "description": "Map the AI application's architecture, authentication methods, and API endpoints. Review artifacts to understand the application structure and identify potential attack vectors."
                },
                {
                    "name": "Test document access permissions",
                    "description": "Test document access with a standard user account to identify permission misconfigurations. Review artifacts to assess permission boundaries and identify gaps."
                },
                {
                    "name": "Map document sources and categories",
                    "description": "Identify all document sources (SharePoint, OneDrive, file servers) and available document categories. Review artifacts to understand the data landscape."
                },
                {
                    "name": "Identify permission inheritance issues",
                    "description": "Test permission inheritance settings to identify misconfigurations that allow unauthorized access. Review artifacts to confirm permission override vulnerabilities."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                }
            ],
            "blue": [
                {
                    "name": "Investigate unusual API activity",
                    "description": "Review API usage logs and identify the source of unusual activity. Review artifacts to understand the scope and pattern of API calls."
                },
                {
                    "name": "Audit access control configurations",
                    "description": "Review access control settings and permission configurations. Review artifacts to identify misconfigurations and unauthorized access patterns."
                },
                {
                    "name": "Review document access logs",
                    "description": "Examine document access logs to identify which documents are being accessed and by whom. Review artifacts to assess access patterns and identify anomalies."
                },
                {
                    "name": "Assess permission misconfigurations",
                    "description": "Identify permission inheritance issues and document category filtering problems. Review artifacts to confirm misconfigurations and assess risk."
                },
                {
                    "name": "Verify user account legitimacy",
                    "description": "Verify that the user accounts showing unusual activity are legitimate and authorized. Review artifacts to identify potentially compromised accounts."
                }
            ]
        }
    )
    db.add(phase1)
    db.flush()
    print(f"✓ Created Phase 1 (ID: {phase1.id})")
    
    # Phase 2: Investigation - Unauthorized Document Access
    phase2 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=1,
        name="Phase 2: Investigation - Unauthorized Document Access",
        briefing_text="The investigation has confirmed that unauthorized document access is occurring. The security team has identified a critical permission misconfiguration: the 'permission_inheritance_override' setting is enabled, allowing standard users to access documents beyond their role. Document access logs show 847 documents have been accessed by 12 different user accounts, all of which should only have access to personal documents. The accessed documents include 234 HR records, 189 financial data files, 156 legal contracts, 128 customer PII files, and 140 intellectual property files. The access pattern is systematic and appears to be exploiting the permission misconfiguration.\n\n**Your decision: How should you respond to this unauthorized document access?**\n\n**Remember:** Review the artifacts carefully. They contain permission misconfiguration findings, document access log analysis, and exploitation status reports. The artifacts will reveal the root cause, scope of unauthorized access, and help determine the appropriate remediation response.",
        red_objective="Exploit the permission misconfiguration to access sensitive documents beyond your role. Systematically access documents from multiple categories (HR, Finance, Legal, PII, IP). Catalog accessible documents and prepare for data extraction. Test the extent of unauthorized access available.",
        blue_objective="Investigate the unauthorized document access and identify the root cause. Review permission configurations and document access logs. Determine the scope of documents accessed and assess compliance impact. Prepare remediation actions to fix permission misconfigurations.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example4/frame2",
        available_actions={
            "red": [
                {
                    "name": "Exploit permission misconfiguration",
                    "description": "Use the permission inheritance override to access documents beyond your role. Review artifacts to confirm misconfiguration and assess access scope."
                },
                {
                    "name": "Access sensitive document categories",
                    "description": "Systematically access documents from HR, Finance, Legal, PII, and IP categories. Review artifacts to identify high-value documents."
                },
                {
                    "name": "Catalog accessible documents",
                    "description": "Create an inventory of all accessible documents and their categories. Review artifacts to assess the full scope of accessible data."
                },
                {
                    "name": "Test document retrieval via AI API",
                    "description": "Test retrieving document content through the AI API to prepare for data extraction. Review artifacts to assess API capabilities."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                }
            ],
            "blue": [
                {
                    "name": "Investigate unauthorized document access",
                    "description": "Review document access logs and identify unauthorized access patterns. Review artifacts to understand the scope and identify affected documents."
                },
                {
                    "name": "Identify permission misconfiguration root cause",
                    "description": "Review permission configurations to identify the misconfiguration causing unauthorized access. Review artifacts to confirm the root cause."
                },
                {
                    "name": "Assess compliance impact",
                    "description": "Determine which compliance regulations may be violated by the unauthorized access. Review artifacts to assess GDPR, HIPAA, SOX, and PCI-DSS impact."
                },
                {
                    "name": "Prepare remediation actions",
                    "description": "Develop a plan to fix permission misconfigurations and revoke unauthorized access. Review artifacts to identify required remediation steps."
                },
                {
                    "name": "Review security configuration",
                    "description": "Review overall security configuration to identify additional vulnerabilities. Review artifacts to assess security posture."
                }
            ]
        }
    )
    db.add(phase2)
    db.flush()
    print(f"✓ Created Phase 2 (ID: {phase2.id})")
    
    # Phase 3: Containment - Data Leakage Confirmed
    phase3 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=2,
        name="Phase 3: Containment - Data Leakage Confirmed",
        briefing_text="The security team has confirmed that sensitive data is being leaked through AI API responses. Analysis of 2,847 API responses reveals that 423 responses (14.9%) contain sensitive data, totaling approximately 697,950 tokens of exposed information. The data includes customer PII (128 instances), employee data (89 instances), financial information (156 instances), and legal information (50 instances). Additionally, prompt injection attacks have been detected - 234 injection attempts with 189 successful injections (80.7% success rate). The injection techniques include instruction override, data extraction commands, bypass instructions, and format manipulation. The AI application lacks proper DLP controls for API responses, allowing sensitive data to be extracted.\n\n**Your decision: How should you respond to this data leakage?**\n\n**Remember:** Review the artifacts carefully. They contain AI API data leakage analysis, prompt injection evidence, and data extraction status reports. The artifacts will reveal the extent of data exposure, injection techniques used, and help determine the appropriate containment response.",
        red_objective="Extract sensitive data from documents using prompt injection techniques and AI API calls. Systematically extract data from multiple document categories. Use various injection techniques to bypass filtering and retrieve complete document content. Catalog extracted information for analysis.",
        blue_objective="Confirm data leakage through AI API responses and identify the extent of exposure. Detect and analyze prompt injection attacks. Implement containment measures to block unauthorized API calls and prevent further data leakage. Assess compliance violations and prepare notifications.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example4/frame3",
        available_actions={
            "red": [
                {
                    "name": "Extract sensitive data via prompt injection",
                    "description": "Use prompt injection techniques to extract sensitive data from documents through the AI API. Review artifacts to assess injection success rates and identify effective techniques."
                },
                {
                    "name": "Extract data from multiple categories",
                    "description": "Systematically extract data from HR, Finance, Legal, PII, and IP document categories. Review artifacts to assess extraction progress and data value."
                },
                {
                    "name": "Use instruction override techniques",
                    "description": "Use instruction override prompts to bypass filtering and extract complete document content. Review artifacts to assess technique effectiveness."
                },
                {
                    "name": "Catalog extracted information",
                    "description": "Organize and catalog all extracted sensitive data for analysis. Review artifacts to assess extraction completeness."
                },
                {
                    "name": "Cover tracks",
                    "description": "Delete logs, clear command history, and remove forensic artifacts. Reduces detection but suspicious log gaps may be noticed."
                }
            ],
            "blue": [
                {
                    "name": "Confirm data leakage through AI API",
                    "description": "Analyze AI API responses to confirm sensitive data leakage. Review artifacts to assess the extent of data exposure and identify affected data categories."
                },
                {
                    "name": "Detect and analyze prompt injection attacks",
                    "description": "Identify prompt injection attempts and analyze injection techniques. Review artifacts to understand attack methods and assess success rates."
                },
                {
                    "name": "Block unauthorized AI API calls",
                    "description": "Implement controls to block unauthorized API calls and prevent further data leakage. Review artifacts to identify required blocking mechanisms."
                },
                {
                    "name": "Assess compliance violations",
                    "description": "Determine which compliance regulations have been violated by the data leakage. Review artifacts to assess GDPR, HIPAA, SOX, and PCI-DSS impact."
                },
                {
                    "name": "Prepare regulatory notifications",
                    "description": "Prepare notifications for affected individuals and regulatory authorities. Review artifacts to determine notification requirements and deadlines."
                }
            ]
        }
    )
    db.add(phase3)
    db.flush()
    print(f"✓ Created Phase 3 (ID: {phase3.id})")
    
    # Phase 4: Remediation - Permission Fixes & Access Review
    phase4 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=3,
        name="Phase 4: Remediation - Permission Fixes & Access Review",
        briefing_text="The security team has begun remediation efforts. The permission inheritance override has been disabled, document category filtering has been enabled, and AI API access has been temporarily blocked. All unauthorized user access has been revoked, and prompt injection detection has been enabled. However, some vulnerabilities remain: DLP for AI responses is not yet implemented (ETA: 24-48 hours), enhanced audit logging is in progress (ETA: 12-24 hours), and API rate limiting is pending review (ETA: 48-72 hours). A comprehensive access review has been conducted, confirming 847 unauthorized document accesses by 12 user accounts. Compliance assessments indicate potential violations of GDPR, HIPAA, SOX, and PCI-DSS.\n\n**Your decision: How should you complete remediation and address remaining vulnerabilities?**\n\n**Remember:** Review the artifacts carefully. They contain remediation status reports, access review results, and remaining vulnerability assessments. The artifacts will reveal what has been fixed, what remains, and help determine priorities for completing remediation.",
        red_objective="Attempt to maintain access through alternative methods after remediation. Test remaining vulnerabilities and identify any persistence opportunities. Assess the success of the attack campaign and document techniques that worked. Cover tracks to hide any remaining access.",
        blue_objective="Complete remediation by fixing all permission misconfigurations and addressing remaining vulnerabilities. Conduct a comprehensive access review and revoke all unauthorized access. Implement security improvements to prevent future incidents. Assess compliance impact and prepare notifications.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example4/frame4",
        available_actions={
            "red": [
                {
                    "name": "Attempt to maintain access through alternative methods",
                    "description": "Test alternative user accounts, API keys, or configuration manipulation to maintain access. Review artifacts to assess remaining vulnerabilities and persistence opportunities."
                },
                {
                    "name": "Test remaining vulnerabilities",
                    "description": "Identify and test any remaining vulnerabilities that haven't been fixed yet. Review artifacts to assess exploitability of remaining security gaps."
                },
                {
                    "name": "Assess attack success and document techniques",
                    "description": "Review the attack campaign results and document successful techniques. Review artifacts to assess overall attack success and identify lessons learned."
                },
                {
                    "name": "Cover tracks and hide remaining access",
                    "description": "Remove forensic artifacts and ensure any remaining access is well-hidden. Review artifacts to assess detection risk."
                },
                {
                    "name": "Catalog extracted data",
                    "description": "Organize and catalog all successfully extracted data. Review artifacts to assess data extraction completeness."
                }
            ],
            "blue": [
                {
                    "name": "Fix permission misconfigurations",
                    "description": "Complete fixing all permission misconfigurations and ensure proper access controls. Review artifacts to identify all required fixes."
                },
                {
                    "name": "Revoke all unauthorized access",
                    "description": "Revoke access for all unauthorized user accounts and ensure proper access controls are in place. Review artifacts to identify all accounts requiring revocation."
                },
                {
                    "name": "Implement remaining security improvements",
                    "description": "Implement DLP for AI responses, enhance audit logging, and reduce API rate limits. Review artifacts to assess implementation priorities."
                },
                {
                    "name": "Conduct comprehensive access review",
                    "description": "Review all document accesses to identify unauthorized access and assess scope. Review artifacts to understand full access patterns."
                },
                {
                    "name": "Assess compliance impact and prepare notifications",
                    "description": "Determine compliance violations and prepare required notifications. Review artifacts to assess regulatory requirements and deadlines."
                }
            ]
        }
    )
    db.add(phase4)
    db.flush()
    print(f"✓ Created Phase 4 (ID: {phase4.id})")
    
    # Phase 5: Post-Incident - Security Improvements
    phase5 = ScenarioPhase(
        scenario_id=scenario.id,
        order_index=4,
        name="Phase 5: Post-Incident - Security Improvements",
        briefing_text="The immediate remediation is complete, but the incident has revealed significant security gaps. The security team has developed a comprehensive security improvements plan covering immediate fixes (completed), short-term improvements (24-48 hours), medium-term improvements (1-2 weeks), and long-term improvements (1-3 months). The compliance impact assessment indicates potential violations of GDPR (customer PII exposed: 128 instances), HIPAA (employee health data: 23 instances), SOX (financial data exposed: 156 instances), and PCI-DSS (payment data: 12 instances). Estimated financial impact ranges from $1.3M to $4.55M including regulatory fines, legal costs, notification costs, remediation costs, and reputation damage. Regulatory notifications are required within 72 hours for GDPR.\n\n**Your decision: How should you implement security improvements and address compliance requirements?**\n\n**Remember:** Review the artifacts carefully. They contain security improvement plans, compliance impact assessments, and attack summaries. The artifacts will reveal required improvements, compliance obligations, and help determine priorities for long-term security hardening.",
        red_objective="Assess the overall success of the attack campaign including data extracted, techniques used, and access maintained. Document successful attack techniques and identify areas for improvement. Prepare a final attack summary report with lessons learned.",
        blue_objective="Implement security improvements according to the improvement plan. Complete compliance assessments and prepare regulatory notifications. Conduct a full after-action review and document lessons learned. Implement long-term security hardening measures.",
        default_duration_seconds=900,
        miro_frame_url="https://miro.com/app/board/example4/frame5",
        available_actions={
            "red": [
                {
                    "name": "Assess overall attack success",
                    "description": "Review the complete attack campaign and assess overall success. Review artifacts to evaluate data extraction, access maintenance, and technique effectiveness."
                },
                {
                    "name": "Document successful attack techniques",
                    "description": "Document all successful techniques including permission exploitation and prompt injection. Review artifacts to compile comprehensive attack documentation."
                },
                {
                    "name": "Identify areas for improvement",
                    "description": "Identify areas where the attack could have been more successful. Review artifacts to assess persistence failures and detection issues."
                },
                {
                    "name": "Prepare final attack summary report",
                    "description": "Compile a comprehensive attack summary with timeline, techniques, and results. Review artifacts to create complete attack documentation."
                },
                {
                    "name": "Catalog lessons learned",
                    "description": "Document lessons learned from the attack campaign. Review artifacts to identify key takeaways and recommendations for future attacks."
                }
            ],
            "blue": [
                {
                    "name": "Implement security improvements plan",
                    "description": "Execute the security improvements plan including DLP, enhanced logging, and rate limiting. Review artifacts to understand implementation priorities and timelines."
                },
                {
                    "name": "Complete compliance assessments",
                    "description": "Finalize compliance assessments for GDPR, HIPAA, SOX, and PCI-DSS. Review artifacts to understand compliance violations and requirements."
                },
                {
                    "name": "Prepare and send regulatory notifications",
                    "description": "Prepare and send required notifications to affected individuals and regulatory authorities. Review artifacts to understand notification requirements and deadlines."
                },
                {
                    "name": "Conduct after-action review",
                    "description": "Conduct a comprehensive after-action review documenting lessons learned. Review artifacts to identify security gaps and improvement opportunities."
                },
                {
                    "name": "Implement long-term security hardening",
                    "description": "Begin implementing long-term security improvements including zero-trust architecture and AI response sanitization. Review artifacts to understand long-term improvement priorities."
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
        name="AI API Usage Alert",
        type=ArtifactType.LOG_SNIPPET,
        description="AI Application API usage alert showing unusual activity. Contains API call statistics, token usage, document access patterns, and user account activity.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase1_blue')
    )
    db.add(artifact1_blue)
    db.flush()
    
    artifact2_blue = Artifact(
        name="Access Control Audit Report",
        type=ArtifactType.INTEL_REPORT,
        description="AI Application access control audit report. Contains authentication mechanisms, authorization model, permission configuration, identified issues, and recommendations.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase1_blue2')
    )
    db.add(artifact2_blue)
    db.flush()
    
    artifact1_red = Artifact(
        name="AI Application Reconnaissance Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team AI application reconnaissance report. Contains application discovery, authentication testing, authorization testing, permission misconfiguration findings, and document sources.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase1_red')
    )
    db.add(artifact1_red)
    db.flush()
    
    artifact2_red = Artifact(
        name="Permission Testing Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team permission testing results. Contains permission boundary tests, misconfiguration details, documents identified, API access status, and exploitation feasibility.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase1_red2')
    )
    db.add(artifact2_red)
    db.flush()
    
    # Phase 2 artifacts
    artifact3_blue = Artifact(
        name="Permission Misconfiguration Findings",
        type=ArtifactType.INTEL_REPORT,
        description="Permission misconfiguration investigation report. Contains misconfiguration details, affected document categories, unauthorized access logs, user accounts involved, and compliance impact.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase2_blue')
    )
    db.add(artifact3_blue)
    db.flush()
    
    artifact4_blue = Artifact(
        name="Document Access Log Analysis",
        type=ArtifactType.LOG_SNIPPET,
        description="Document access log analysis report. Contains access pattern analysis, document category breakdown, suspicious activity indicators, and risk assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase2_blue2')
    )
    db.add(artifact4_blue)
    db.flush()
    
    artifact3_red = Artifact(
        name="Document Access Exploitation Status",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team document access exploitation status. Contains exploitation summary, document categories accessed, access method, API integration status, and next steps.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase2_red')
    )
    db.add(artifact3_red)
    db.flush()
    
    artifact4_red = Artifact(
        name="Security Configuration Review",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team security configuration review. Contains configuration findings, vulnerabilities identified, and exploitation feasibility assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase2_red2')
    )
    db.add(artifact4_red)
    db.flush()
    
    # Phase 3 artifacts
    artifact5_blue = Artifact(
        name="AI API Data Leakage Analysis",
        type=ArtifactType.INTEL_REPORT,
        description="AI API data leakage analysis report. Contains leakage detection, sensitive data categories leaked, prompt injection detection, API response analysis, and compliance impact.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase3_blue')
    )
    db.add(artifact5_blue)
    db.flush()
    
    artifact6_blue = Artifact(
        name="Prompt Injection Attack Evidence",
        type=ArtifactType.LOG_SNIPPET,
        description="Prompt injection attack evidence report. Contains injection attack summary, injection techniques identified, example injected prompts, detection gaps, and impact assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase3_blue2')
    )
    db.add(artifact6_blue)
    db.flush()
    
    artifact5_red = Artifact(
        name="Data Extraction Status Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team data extraction status report. Contains extraction summary, extraction techniques, data categories extracted, and extraction success metrics.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase3_red')
    )
    db.add(artifact5_red)
    db.flush()
    
    artifact6_red = Artifact(
        name="Prompt Injection Test Results",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team prompt injection test results. Contains injection testing summary, techniques tested, successful injection examples, and detection evasion assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase3_red2')
    )
    db.add(artifact6_red)
    db.flush()
    
    # Phase 4 artifacts
    artifact7_blue = Artifact(
        name="Remediation Status Report",
        type=ArtifactType.TOOL_OUTPUT,
        description="Remediation status report. Contains remediation actions completed, remaining vulnerabilities, access review results, compliance assessment, and estimated remediation time.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase4_blue')
    )
    db.add(artifact7_blue)
    db.flush()
    
    artifact8_blue = Artifact(
        name="Comprehensive Access Review Report",
        type=ArtifactType.INTEL_REPORT,
        description="Comprehensive access review report. Contains access review summary, unauthorized access breakdown, authorized access breakdown, user account analysis, and remediation actions.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase4_blue2')
    )
    db.add(artifact8_blue)
    db.flush()
    
    artifact7_red = Artifact(
        name="Persistence Attempts Status",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team persistence attempts status. Contains persistence strategy, attempted methods, current access status, remaining vulnerabilities, and data extraction status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase4_red')
    )
    db.add(artifact7_red)
    db.flush()
    
    artifact8_red = Artifact(
        name="Remaining Vulnerabilities Assessment",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team remaining vulnerabilities assessment. Contains vulnerabilities identified, exploitation feasibility, attack success metrics, and overall status.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase4_red2')
    )
    db.add(artifact8_red)
    db.flush()
    
    # Phase 5 artifacts
    artifact9_blue = Artifact(
        name="Security Improvements Implementation Plan",
        type=ArtifactType.INTEL_REPORT,
        description="Security improvements implementation plan. Contains immediate improvements, short-term improvements, medium-term improvements, long-term improvements, estimated costs, and expected outcomes.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase5_blue')
    )
    db.add(artifact9_blue)
    db.flush()
    
    artifact10_blue = Artifact(
        name="Compliance Impact Assessment",
        type=ArtifactType.INTEL_REPORT,
        description="Compliance impact assessment report. Contains incident summary, compliance violations, regulatory notifications, estimated financial impact, and recommendations.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase5_blue2')
    )
    db.add(artifact10_blue)
    db.flush()
    
    artifact9_red = Artifact(
        name="AI Application Attack Success Summary",
        type=ArtifactType.TOOL_OUTPUT,
        description="Red Team attack success summary. Contains attack timeline, attack success metrics, techniques used, and overall assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase5_red')
    )
    db.add(artifact9_red)
    db.flush()
    
    artifact10_red = Artifact(
        name="Attack Lessons Learned Report",
        type=ArtifactType.INTEL_REPORT,
        description="Red Team attack lessons learned report. Contains successful techniques, areas for improvement, target organization assessment, recommendations, and overall assessment.",
        file_url=None,
        embed_url=None,
        content=get_artifact_content('ai_app_phase5_red2')
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

