"""
Generate artifact content for the Email Bomb + Teams Call scenario.
Creates realistic Microsoft Defender, Sentinel, Teams logs, and Red Team tool outputs.
"""

def generate_email_bomb_phase1_red():
    """Red Team: Email bomb campaign status"""
    return """Email Bomb Campaign Status Report
=====================================
Campaign ID: EB-2024-001
Operator: RED-TEAM-BETA
Date: 2024-01-22 09:15:00 UTC
Target: finance.director@corp.local

CAMPAIGN OVERVIEW:
------------------
Campaign Type: Email Bomb (Spam Flood)
Target Email: finance.director@corp.local
Total Emails Sent: 847
Emails Delivered: 623 (73.6% delivery rate)
Emails Blocked: 224 (26.4% blocked)
Delivery Method: Multiple compromised SMTP servers
Sender Domains: 12 different domains (rotating)

EMAIL CHARACTERISTICS:
----------------------
Subject Lines Used:
  - "URGENT: Invoice Payment Required"
  - "Action Required: Account Verification"
  - "Security Alert: Suspicious Activity Detected"
  - "Important: Tax Document Review"
  - "Time-Sensitive: Financial Statement"
  - "Immediate Action: Payment Confirmation"
  - "Alert: Unauthorized Access Attempt"
  - "Critical: Account Suspension Notice"
  - "Warning: Payment Overdue"
  - "Notice: Document Signature Required"

Content Types:
  - HTML emails with embedded tracking pixels
  - PDF attachments (benign but numerous)
  - Links to external domains
  - Embedded images from CDN

TIMING STRATEGY:
---------------
Start Time: 09:00:00 UTC
Peak Delivery: 09:05:00 - 09:12:00 UTC (500+ emails in 7 minutes)
Current Status: ONGOING
Delivery Rate: ~15-20 emails per minute (sustained)
Expected Duration: 30-45 minutes total

IMPACT ASSESSMENT:
------------------
Inbox Overwhelmed: YES (623+ emails in inbox)
User Response: ANXIOUS (user reported "hundreds of emails")
Email Client Performance: DEGRADED (Outlook slow to load)
User Productivity: SIGNIFICANTLY IMPACTED
Psychological State: STRESSED (user seeking help)

NEXT PHASE READINESS:
---------------------
Target State: VULNERABLE (overwhelmed, seeking assistance)
Optimal Timing: 5-10 minutes after peak delivery
Teams Call Prepared: YES (IT support impersonation ready)
Caller ID Spoofing: CONFIGURED (appears as internal IT number)
Social Engineering Script: READY

CAMPAIGN SUCCESS METRICS:
-------------------------
Email Delivery Rate: 73.6% (EXCELLENT - above 70% target)
User Engagement: HIGH (user actively checking emails)
Psychological Impact: HIGH (user reported stress)
Inbox Disruption: COMPLETE (inbox unusable)
Readiness for Phase 2: OPTIMAL (user vulnerable to social engineering)

CONCLUSION:
-----------
Email bomb campaign is PROCEEDING AS PLANNED. Target inbox is overwhelmed 
with 623+ delivered emails. User is stressed and actively seeking help. 
Optimal conditions achieved for Phase 2 (Teams call impersonation).

Ready to proceed with IT support impersonation call in 5-10 minutes."""


def generate_email_bomb_phase1_blue():
    """Blue Team: Defender for Office 365 email bomb detection"""
    return """Microsoft Defender for Office 365 Alert
==========================================
Alert ID: DA-2024-004521
Severity: High
Time: 09:12:00 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Email Bomb Attack Detected
Alert Type: Email Flood / Spam Campaign
MITRE ATT&CK Technique: T1568.002 (Dynamic Resolution: Domain Generation Algorithms)
MITRE ATT&CK Tactic: Impact / Resource Hijacking
Confidence: High (92%)

EMAIL VOLUME ANALYSIS:
----------------------
Time Window: 09:00:00 - 09:12:00 UTC (12 minutes)
Total Emails Received: 847
Emails Blocked: 224 (26.4%)
Emails Delivered: 623 (73.6%)
Average Delivery Rate: 51.8 emails per minute
Peak Delivery Rate: 87 emails per minute (09:07:00 UTC)

SENDER ANALYSIS:
----------------
Unique Sender Domains: 12
Sender IP Addresses: 47 different IPs
Geographic Distribution: 8 countries (US, UK, DE, FR, NL, CA, AU, BR)
Sender Reputation: MIXED (some known spam sources)
Domain Age: 8/12 domains registered within last 30 days
Domain Reputation: 6/12 domains flagged as suspicious

EMAIL CHARACTERISTICS:
-----------------------
Subject Line Patterns:
  - "URGENT" (247 emails)
  - "Action Required" (189 emails)
  - "Security Alert" (156 emails)
  - "Payment" (131 emails)
  - "Account" (98 emails)
  - "Verification" (48 emails)

Content Analysis:
  - HTML emails: 89%
  - Embedded tracking pixels: 94%
  - PDF attachments: 12% (all benign but numerous)
  - External links: 78%
  - Suspicious URLs: 34%

DEFENDER FOR OFFICE 365 RESPONSE:
----------------------------------
Safe Attachments: ENABLED (scanned 100% of attachments)
Safe Links: ENABLED (rewrote 78% of links)
Anti-Phishing: ENABLED (flagged 34% as suspicious)
Anti-Spam: ENABLED (blocked 26.4%)
ATP Policies: ACTIVE

AUTOMATED ACTIONS TAKEN:
------------------------
1. Quarantined: 224 emails (26.4%)
2. Link Rewriting: 486 emails (78% of delivered)
3. Attachment Scanning: 75 emails (12% with attachments)
4. User Notification: SENT (alerted user to email flood)
5. Admin Alert: GENERATED (this alert)

USER IMPACT:
------------
Inbox Status: OVERWHELMED (623+ emails delivered)
Email Client Performance: DEGRADED (Outlook slow)
User Productivity: SIGNIFICANTLY IMPACTED
User Reported: "Hundreds of emails, can't find important messages"
User State: STRESSED (actively seeking IT support)

THREAT INTELLIGENCE:
--------------------
IOC Type: Email Bomb Campaign
Campaign ID: EB-2024-001 (internal tracking)
Related Campaigns: 3 similar campaigns in past 60 days
Threat Actor: Unknown (attribution pending)
TTPs: Consistent with social engineering preparation attacks

RECOMMENDATION:
---------------
PRIORITY: HIGH

Immediate Actions:
1. Contact user (finance.director@corp.local) to verify they haven't:
   - Clicked suspicious links
   - Opened suspicious attachments
   - Provided credentials to anyone
   - Granted remote access to anyone

2. Warn user about potential follow-up social engineering:
   - Phone calls claiming to be IT support
   - Teams calls from "IT department"
   - Requests for remote access
   - Requests for credentials

3. Monitor user's account for:
   - Unusual login attempts
   - Password reset requests
   - MFA bypass attempts
   - Suspicious Teams activity

4. Consider temporarily:
   - Blocking additional emails from suspicious domains
   - Enabling stricter email filtering for this user
   - Providing user with IT support contact information

RISK ASSESSMENT:
----------------
Current Risk: MEDIUM-HIGH
- Email bomb successful (73.6% delivery)
- User inbox overwhelmed
- User stressed and seeking help
- High likelihood of follow-up social engineering attack

Expected Next Steps by Attacker:
- Teams call impersonating IT support
- Request for remote access
- Credential harvesting attempt
- Initial access attempt

Monitor closely for next 30-60 minutes."""


def generate_teams_call_phase2_red():
    """Red Team: Teams call success report"""
    return """Teams Call Impersonation Report
==================================
Call ID: TC-2024-001
Operator: RED-TEAM-BETA
Date: 2024-01-22 09:18:00 UTC
Target: finance.director@corp.local
Call Duration: 4 minutes 32 seconds

CALL SETUP:
-----------
Caller ID: +1-555-IT-SUPPORT (spoofed internal IT number)
Caller Name: "IT Support - Corp IT Department"
Call Method: Microsoft Teams (external call)
Call Type: Audio + Screen Share Request
Target State: STRESSED (from email bomb)

CALL SCRIPT EXECUTION:
----------------------
Opening: "Hi, this is IT Support. We detected unusual activity on your account 
         and noticed you're receiving a lot of emails. We need to help you secure 
         your account immediately."

Target Response: "Yes, I have hundreds of emails! I can't find anything important. 
                  Can you help?"

Social Engineering Hook: SUCCESSFUL
- User confirmed email bomb impact
- User expressed need for help
- User receptive to assistance

MID-CALL TACTICS:
-----------------
1. Established Credibility:
   - Referenced email bomb ("We see 623 emails in your inbox")
   - Mentioned "security incident" requiring immediate action
   - Used urgency ("We need to secure your account now")
   - Result: USER TRUSTED CALLER

2. Information Gathering:
   - Asked about email client performance (confirmed slow)
   - Asked if user clicked any links (user said "maybe, I'm not sure")
   - Asked about current work tasks (user mentioned "important financial reports")
   - Result: VULNERABILITY CONFIRMED

3. Remote Access Request:
   - "We need to access your computer remotely to clean up these emails and 
     secure your account. Can you grant us remote access?"
   - User Response: "How do I do that?"
   - Result: USER AGREED TO REMOTE ACCESS

REMOTE ACCESS ESTABLISHMENT:
----------------------------
Tool Used: Quick Assist (Windows built-in)
Connection Method: User-initiated (we provided code)
Connection Established: 09:19:45 UTC
Connection Duration: 3 minutes 18 seconds
Screen Share: ACTIVE
Control Granted: YES (user granted full control)

ACTIONS PERFORMED DURING CALL:
-------------------------------
1. Opened Outlook (to "verify email issues")
2. Checked email rules (to "prevent future spam")
3. Opened Event Viewer (to "check for security issues")
4. Opened Registry Editor (to "clean up email settings")
5. Opened Command Prompt (to "run diagnostic commands")
6. Checked running processes (to "identify suspicious activity")

USER BEHAVIOR OBSERVED:
-----------------------
Trust Level: HIGH (user followed all instructions)
Suspicion Level: LOW (user did not question actions)
Verification Attempts: NONE (user did not verify caller identity)
Security Awareness: LOW (user granted full remote access)

CALL OUTCOME:
-------------
Remote Access: SUCCESSFUL
Screen Share: ACTIVE
User Trust: HIGH
Information Gathered: MODERATE
Credential Request: NOT YET (saved for Phase 3)
Connection Maintained: YES (Quick Assist session active)

NEXT PHASE READINESS:
---------------------
Remote Access: ESTABLISHED (Quick Assist active)
User Trust: HIGH (user believes we are IT support)
Optimal Timing: NOW (user is engaged and trusting)
Credential Harvesting: READY (can request during remote session)
Persistence: NOT YET (will establish in Phase 4)

CONCLUSION:
-----------
Teams call impersonation was HIGHLY SUCCESSFUL. User granted remote access 
via Quick Assist. Screen share is active. User trusts caller completely. 
Ready to proceed with credential harvesting in Phase 3.

Current session provides full visibility into user's system and ongoing 
remote control capability."""


def generate_teams_call_phase2_blue():
    """Blue Team: Teams call detection and analysis"""
    return """Microsoft Defender for Office 365 / Teams Security Alert
===========================================================
Alert ID: DA-2024-004523
Severity: Medium
Time: 09:18:15 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious Teams Call Activity
Alert Type: External Communication / Social Engineering
MITRE ATT&CK Technique: T1566.001 (Phishing: Spearphishing Attachment) + T1566.003 (Phishing: Spearphishing via Service)
MITRE ATT&CK Tactic: Initial Access
Confidence: Medium (68%)

TEAMS CALL ANALYSIS:
--------------------
Call Time: 09:18:00 UTC
Call Duration: 4 minutes 32 seconds
Caller: +1-555-IT-SUPPORT (external number)
Caller Name: "IT Support - Corp IT Department"
Call Type: External Teams Call (audio)
Target: finance.director@corp.local

CALLER VERIFICATION:
--------------------
Caller ID: +1-555-IT-SUPPORT
Internal IT Number: NO (not in corporate directory)
Number Reputation: UNKNOWN (not recognized as internal)
Caller Name: "IT Support - Corp IT Department"
Name Verification: SPOOFED (does not match internal IT naming convention)
Call Source: External (not from corporate network)

CONTEXT CORRELATION:
--------------------
Previous Alert: Email Bomb (DA-2024-004521)
Time Since Email Bomb: 6 minutes
User State: STRESSED (from email bomb)
Call Timing: SUSPICIOUS (immediately after email bomb)
Caller Claim: "We detected unusual activity" (referencing email bomb)

SOCIAL ENGINEERING INDICATORS:
------------------------------
1. Caller claims to be IT support but uses external number
2. Caller references recent email bomb (suggests coordination)
3. Caller uses urgency ("We need to secure your account now")
4. Caller requests remote access
5. Call timing is suspicious (immediately after email bomb)

USER BEHAVIOR:
--------------
User Response: RECEPTIVE (user accepted call)
User Verification: NONE (user did not verify caller identity)
User Trust: HIGH (user followed caller instructions)
Remote Access: GRANTED (user granted remote access via Quick Assist)

QUICK ASSIST ACTIVITY:
----------------------
Tool: Quick Assist (Windows built-in remote access)
Connection Established: 09:19:45 UTC
Connection Duration: 3+ minutes (ongoing)
Screen Share: ACTIVE
Control Level: FULL (user granted full control)
Connection Status: ACTIVE (as of 09:22:00 UTC)

ACTIONS OBSERVED DURING REMOTE SESSION:
---------------------------------------
1. Opened Outlook (to "verify email issues")
2. Checked email rules (to "prevent future spam")
3. Opened Event Viewer (to "check for security issues")
4. Opened Registry Editor (to "clean up email settings")
5. Opened Command Prompt (to "run diagnostic commands")
6. Checked running processes (to "identify suspicious activity")

DEFENDER FOR ENDPOINT CORRELATION:
-----------------------------------
Device: WS-FIN-001
User: finance.director@corp.local
Quick Assist Process: ACTIVE (PID: 8923)
Parent Process: explorer.exe
Command Line: "C:\\Windows\\System32\\QuickAssist.exe"
Network Connections: 1 active (Quick Assist session)
Screen Share: ACTIVE

RISK ASSESSMENT:
----------------
Current Risk: HIGH
- External caller impersonating IT support
- User granted remote access
- Screen share active
- Full control granted
- Suspicious actions observed (Registry Editor, Command Prompt)
- High likelihood of credential harvesting or malware deployment

EXPECTED NEXT STEPS BY ATTACKER:
---------------------------------
1. Credential harvesting (request passwords during call)
2. Malware deployment (via remote access)
3. Persistence establishment (scheduled tasks, registry)
4. Lateral movement (if credentials obtained)

RECOMMENDATION:
---------------
PRIORITY: CRITICAL - IMMEDIATE ACTION REQUIRED

1. CONTACT USER IMMEDIATELY:
   - Call user on verified internal number
   - Verify if they granted remote access
   - Instruct user to DISCONNECT Quick Assist session immediately
   - Warn user about social engineering attack

2. TERMINATE REMOTE SESSION:
   - If possible, terminate Quick Assist session remotely
   - Block Quick Assist if not needed for business
   - Monitor for additional remote access attempts

3. SECURE USER ACCOUNT:
   - Force password reset for finance.director@corp.local
   - Review MFA settings
   - Check for suspicious login attempts
   - Review email rules for malicious changes

4. INVESTIGATE SYSTEM:
   - Check for newly created scheduled tasks
   - Review registry for persistence mechanisms
   - Check for newly installed software
   - Review command history for suspicious commands

5. MONITOR CLOSELY:
   - Watch for credential harvesting attempts
   - Monitor for malware deployment
   - Check for lateral movement attempts
   - Review all user activity for next 24 hours

INCIDENT CORRELATION:
---------------------
Related Alerts:
- DA-2024-004521: Email Bomb Attack (6 minutes prior)
- DA-2024-004523: Suspicious Teams Call (current)

Campaign Pattern: Email Bomb → Teams Call → [Expected: Credential Harvesting]

This appears to be a coordinated social engineering attack."""


def generate_credential_harvesting_phase3_red():
    """Red Team: Credential harvesting success"""
    return """Credential Harvesting Report
===============================
Operation ID: CH-2024-001
Operator: RED-TEAM-BETA
Date: 2024-01-22 09:22:00 UTC
Target: finance.director@corp.local
Method: Social Engineering via Remote Access

HARVESTING METHOD:
------------------
Approach: Credential Request During Remote Session
Tool: Quick Assist (existing remote access)
Timing: During "system diagnostic" (Phase 2 remote session)
Social Engineering Hook: "We need your password to verify account security"

CREDENTIALS OBTAINED:
--------------------
1. Corporate Email Password:
   - Username: finance.director@corp.local
   - Password: [REDACTED - 14 characters, mixed case, numbers, symbols]
   - Password Strength: MEDIUM (meets policy requirements)
   - MFA Status: ENABLED (but user provided MFA code)

2. MFA Code:
   - Method: Microsoft Authenticator (push notification)
   - User Action: APPROVED (user approved MFA request)
   - Code: [6-digit code obtained]
   - Time: 09:21:45 UTC

3. Windows Password:
   - Username: finance.director@corp.local
   - Password: [REDACTED - same as email password]
   - Local Admin: NO (standard user account)

4. Additional Information:
   - Security Questions: 2 of 3 answered (birth city, first pet name)
   - Recovery Email: personal.email@gmail.com (obtained)
   - Phone Number: +1-555-XXX-XXXX (obtained)

SOCIAL ENGINEERING EXECUTION:
------------------------------
Request Method: "We need to verify your account credentials to ensure they 
                haven't been compromised. Can you enter your password here?"

User Response: COMPLIED (user entered password in visible field)
User Suspicion: NONE (user trusted caller completely)
Verification Attempts: NONE (user did not verify request legitimacy)

MFA BYPASS:
-----------
Challenge: User has MFA enabled (Microsoft Authenticator)
Solution: "We're sending you an MFA request. Please approve it so we can 
          verify your account is secure."
User Action: APPROVED (user approved MFA push notification)
Result: MFA BYPASSED SUCCESSFULLY

CREDENTIAL VALIDATION:
----------------------
Email Credentials: VALIDATED (successful login test)
Windows Credentials: VALIDATED (successful local login test)
MFA: BYPASSED (code obtained and used)
Account Access: CONFIRMED (full access to email and system)

ACCOUNT PRIVILEGES:
-------------------
Email Access: FULL (can read, send, delete emails)
Email Rules: CAN MODIFY (can create forwarding rules)
Calendar Access: FULL (can view and modify calendar)
Contacts Access: FULL (can view contacts)
OneDrive Access: FULL (can access user's OneDrive)
SharePoint Access: LIMITED (department sites only)
Teams Access: FULL (can access Teams)
Windows Account: STANDARD USER (no local admin)

NEXT PHASE READINESS:
---------------------
Credentials: OBTAINED (email, Windows, MFA bypassed)
Account Access: CONFIRMED (tested and working)
Remote Access: ACTIVE (Quick Assist still connected)
Persistence: NOT YET (will establish in Phase 4)
Lateral Movement: READY (can use credentials for access)

CONCLUSION:
-----------
Credential harvesting was HIGHLY SUCCESSFUL. Obtained email password, 
Windows password, MFA code, and additional account information. User 
complied completely with social engineering request. Account access 
confirmed. Ready to proceed with persistence establishment in Phase 4.

Current capabilities:
- Full email access (read, send, delete)
- Windows account access (standard user)
- MFA bypassed (can authenticate)
- Remote access maintained (Quick Assist active)"""


def generate_credential_harvesting_phase3_blue():
    """Blue Team: Credential harvesting detection"""
    return """Microsoft Defender for Identity Alert
=====================================
Alert ID: DA-2024-004525
Severity: Critical
Time: 09:21:50 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious Credential Entry Detected
Alert Type: Credential Harvesting / Social Engineering
MITRE ATT&CK Technique: T1555.003 (Credentials from Password Stores: Credentials from Web Browsers) + T1056.001 (Input Capture: Keylogging)
MITRE ATT&CK Tactic: Credential Access
Confidence: High (87%)

CREDENTIAL ENTRY DETECTION:
---------------------------
Detection Method: Defender for Identity behavioral analysis
Trigger: Password entered in visible/unusual context
Time: 09:21:45 UTC
Location: Quick Assist remote session
Context: Remote access session with external caller

USER BEHAVIOR ANALYSIS:
-----------------------
Action: User entered corporate password in visible text field
Context: During "system diagnostic" remote session
Caller: External Teams caller claiming to be IT support
User Verification: NONE (user did not verify caller identity)
Suspicion Level: NONE (user trusted caller completely)

MFA ACTIVITY:
-------------
MFA Method: Microsoft Authenticator (push notification)
MFA Request Time: 09:21:47 UTC
User Action: APPROVED (user approved MFA request)
MFA Context: During remote access session with external caller
MFA Bypass: SUCCESSFUL (attacker obtained MFA code)

ACCOUNT ACCESS ATTEMPTS:
------------------------
Login Attempt 1:
  - Time: 09:22:00 UTC
  - Source: External IP (185.220.101.45)
  - Method: OAuth2 (using obtained credentials)
  - MFA: BYPASSED (using obtained MFA code)
  - Result: SUCCESSFUL LOGIN
  - Location: Unknown (external network)

Login Attempt 2:
  - Time: 09:22:15 UTC
  - Source: WS-FIN-001 (local device)
  - Method: Windows Authentication
  - Credentials: finance.director@corp.local / [password]
  - Result: SUCCESSFUL LOGIN
  - Context: During remote access session

ACCOUNT PRIVILEGES ACCESSED:
----------------------------
Email Access: CONFIRMED (login successful)
OneDrive Access: CONFIRMED (login successful)
Teams Access: CONFIRMED (login successful)
SharePoint Access: LIMITED (department sites only)
Windows Account: STANDARD USER (no local admin)

DEFENDER FOR IDENTITY CORRELATION:
-----------------------------------
Previous Alerts:
- DA-2024-004521: Email Bomb (09:12:00 UTC)
- DA-2024-004523: Suspicious Teams Call (09:18:15 UTC)
- DA-2024-004525: Credential Harvesting (current)

Campaign Pattern: Email Bomb → Teams Call → Credential Harvesting → [Expected: Account Takeover]

RISK ASSESSMENT:
----------------
Current Risk: CRITICAL
- Credentials compromised (email, Windows, MFA)
- Account access confirmed (external login successful)
- Remote access active (Quick Assist still connected)
- High likelihood of persistence establishment
- High likelihood of lateral movement
- High likelihood of data exfiltration

EXPECTED NEXT STEPS BY ATTACKER:
---------------------------------
1. Establish persistence (scheduled tasks, registry, email rules)
2. Maintain access (ensure continued account access)
3. Lateral movement (use credentials to access other systems)
4. Data exfiltration (steal sensitive financial data)
5. Privilege escalation (attempt to gain admin access)

RECOMMENDATION:
---------------
PRIORITY: CRITICAL - IMMEDIATE ACTION REQUIRED

1. SECURE ACCOUNT IMMEDIATELY:
   - Force password reset for finance.director@corp.local
   - Revoke all active sessions (force logout everywhere)
   - Disable MFA temporarily (to prevent further MFA bypass)
   - Re-enable MFA with new method (require re-registration)
   - Review security questions (reset all answers)

2. TERMINATE REMOTE SESSION:
   - Disconnect Quick Assist session immediately
   - Block Quick Assist if not needed for business
   - Monitor for additional remote access attempts

3. INVESTIGATE COMPROMISED ACCOUNT:
   - Review all email activity (sent, received, deleted)
   - Check email rules for malicious forwarding
   - Review OneDrive for accessed/modified files
   - Check Teams for suspicious activity
   - Review SharePoint for accessed sites/files
   - Check Windows event logs for suspicious activity

4. CONTAIN THREAT:
   - Isolate WS-FIN-001 from network (if possible)
   - Block external IP 185.220.101.45
   - Review all systems accessed by finance.director@corp.local
   - Check for lateral movement attempts
   - Review all financial systems for unauthorized access

5. MONITOR CLOSELY:
   - Watch for persistence mechanisms (scheduled tasks, registry)
   - Monitor for data exfiltration attempts
   - Check for privilege escalation attempts
   - Review all account activity for next 7 days

INCIDENT CORRELATION:
---------------------
This is part of a coordinated social engineering attack:
1. Email Bomb (overwhelm user)
2. Teams Call (establish trust, gain remote access)
3. Credential Harvesting (obtain account credentials) ← CURRENT PHASE
4. [Expected: Persistence & Initial Access]

The attacker has successfully obtained full account access."""


def generate_remote_access_phase4_red():
    """Red Team: Remote access and persistence establishment"""
    return """Remote Access & Persistence Establishment Report
==================================================
Operation ID: RA-2024-001
Operator: RED-TEAM-BETA
Date: 2024-01-22 09:25:00 UTC
Target: finance.director@corp.local
Device: WS-FIN-001

REMOTE ACCESS STATUS:
--------------------
Method: Quick Assist (Windows built-in)
Connection Established: 09:19:45 UTC (Phase 2)
Connection Duration: 5+ minutes (ongoing)
Screen Share: ACTIVE
Control Level: FULL (user granted full control)
Connection Stability: STABLE

PERSISTENCE MECHANISMS DEPLOYED:
--------------------------------
1. Scheduled Task (Primary):
   - Task Name: "WindowsUpdateService"
   - Description: "Windows Update Service"
   - Trigger: Daily at 02:00 AM
   - Action: PowerShell script (hidden)
   - Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\update.ps1
   - Status: CREATED SUCCESSFULLY
   - Detection Risk: LOW (disguised as Windows Update)

2. Registry Run Key:
   - Key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
   - Value Name: "MicrosoftEdgeUpdate"
   - Value Data: "powershell.exe -WindowStyle Hidden -File C:\\Users\\finance.director\\AppData\\Local\\Temp\\update.ps1"
   - Status: CREATED SUCCESSFULLY
   - Detection Risk: MEDIUM (registry monitoring may detect)

3. Email Forwarding Rule:
   - Rule Name: "Important Messages Forward"
   - Condition: Emails containing "financial", "invoice", "payment"
   - Action: Forward to external email (attacker-controlled)
   - Status: CREATED SUCCESSFULLY
   - Detection Risk: LOW (appears as legitimate rule)

4. Startup Folder:
   - File: C:\\Users\\finance.director\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\edgeupdate.vbs
   - Content: VBScript launcher for PowerShell payload
   - Status: CREATED SUCCESSFULLY
   - Detection Risk: MEDIUM (startup folder monitored)

PAYLOAD DEPLOYMENT:
-------------------
Primary Payload: update.ps1 (PowerShell script)
Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\update.ps1
Size: 2.3 KB
Function: Establish C2 connection, maintain persistence, exfiltrate data
C2 Server: 185.220.101.45:443 (HTTPS)
Beacon Interval: 5 minutes
Status: DEPLOYED (not yet executed - will run on next login or scheduled task)

SECONDARY PAYLOADS:
-------------------
1. Credential Dumper:
   - Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\cred.exe
   - Function: Extract saved credentials from browser, Windows Credential Manager
   - Status: DEPLOYED (ready for execution)

2. Network Scanner:
   - Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\scan.exe
   - Function: Scan internal network for vulnerable systems
   - Status: DEPLOYED (ready for execution)

SYSTEM RECONNAISSANCE:
----------------------
Operating System: Windows 11 Enterprise
OS Build: 22621.3007
Domain: CORP.LOCAL
Computer Name: WS-FIN-001
User Account: finance.director@corp.local
User Privileges: Standard User (no local admin)
Domain Admin: NO
Sensitive Data Access: HIGH (Finance department, access to financial systems)

NETWORK ACCESS:
---------------
VLAN: FIN-STANDARD-VLAN-30
Network Access: STANDARD (Finance and shared resources)
Firewall Rules: MODERATE (standard outbound rules)
Network Isolation: NOT ENABLED
Lateral Movement Potential: HIGH (standard network, broader access)

EDR STATUS:
-----------
EDR Product: Microsoft Defender for Endpoint
Agent Version: 10.0.26100.1 (LATEST)
Agent Status: ACTIVE and HEALTHY
Cloud Protection: ENABLED
Real-time Protection: ENABLED
Behavior Monitoring: ENABLED

DETECTION RISK ASSESSMENT:
---------------------------
Scheduled Task: LOW (disguised as Windows Update)
Registry Run Key: MEDIUM (registry monitoring may detect)
Email Rule: LOW (appears legitimate)
Startup Folder: MEDIUM (startup monitoring)
Payload Files: MEDIUM (Defender may detect on execution)
Overall Detection Risk: MEDIUM (some mechanisms may be detected)

NEXT PHASE READINESS:
---------------------
Persistence: ESTABLISHED (4 mechanisms deployed)
Remote Access: ACTIVE (Quick Assist still connected)
Credentials: OBTAINED (from Phase 3)
Account Access: CONFIRMED (tested and working)
Payloads: DEPLOYED (ready for execution)
C2 Infrastructure: READY (server configured and waiting)

CONCLUSION:
-----------
Remote access maintained and persistence established successfully. Deployed 
4 persistence mechanisms (scheduled task, registry, email rule, startup folder). 
Payloads deployed and ready for execution. System reconnaissance complete. 
Ready to proceed with initial access and C2 establishment in Phase 5.

Current capabilities:
- Remote access (Quick Assist active)
- Persistence (4 mechanisms)
- Credentials (email, Windows, MFA)
- Payloads (deployed and ready)
- Network access (standard VLAN, good lateral movement potential)"""


def generate_remote_access_phase4_blue():
    """Blue Team: Remote access and persistence detection"""
    return """Microsoft Defender for Endpoint Alert
==========================================
Alert ID: DA-2024-004527
Severity: High
Time: 09:25:30 UTC
Device: WS-FIN-001
Device ID: 87654321-4321-4321-4321-210987654321
User: finance.director@corp.local
User SID: S-1-5-21-1234567890-123456789-123456789-9012
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious Persistence Mechanisms Detected
Alert Type: Persistence / Scheduled Task Creation
MITRE ATT&CK Technique: T1053.005 (Scheduled Task/Job: Scheduled Task) + T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder)
MITRE ATT&CK Tactic: Persistence
Confidence: High (91%)

PERSISTENCE MECHANISMS DETECTED:
--------------------------------
1. Suspicious Scheduled Task:
   - Task Name: "WindowsUpdateService"
   - Description: "Windows Update Service"
   - Created: 09:24:15 UTC
   - Creator: finance.director@corp.local
   - Trigger: Daily at 02:00 AM
   - Action: PowerShell script
   - Script Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\update.ps1
   - Status: CREATED (not yet executed)
   - Detection: Defender flagged as suspicious (unusual PowerShell execution)

2. Registry Run Key:
   - Key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
   - Value Name: "MicrosoftEdgeUpdate"
   - Value Data: PowerShell command pointing to update.ps1
   - Created: 09:24:22 UTC
   - Status: CREATED
   - Detection: Defender flagged as suspicious (unusual registry modification)

3. Email Forwarding Rule:
   - Rule Name: "Important Messages Forward"
   - Condition: Emails containing "financial", "invoice", "payment"
   - Action: Forward to external email (attacker-controlled)
   - Created: 09:24:35 UTC
   - Status: CREATED
   - Detection: Defender for Office 365 flagged as suspicious (forwarding to external domain)

4. Startup Folder:
   - File: C:\\Users\\finance.director\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\edgeupdate.vbs
   - Created: 09:24:48 UTC
   - Status: CREATED
   - Detection: Defender flagged as suspicious (unusual startup item)

SUSPICIOUS FILES DETECTED:
--------------------------
1. update.ps1:
   - Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\update.ps1
   - Size: 2.3 KB
   - Created: 09:24:15 UTC
   - Content: PowerShell script (obfuscated, contains C2 connection code)
   - Detection: Defender flagged as suspicious (suspicious PowerShell content)

2. cred.exe:
   - Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\cred.exe
   - Size: 156 KB
   - Created: 09:24:20 UTC
   - Detection: Defender flagged as MALWARE (credential dumper tool)

3. scan.exe:
   - Location: C:\\Users\\finance.director\\AppData\\Local\\Temp\\scan.exe
   - Size: 89 KB
   - Created: 09:24:25 UTC
   - Detection: Defender flagged as SUSPICIOUS (network scanning tool)

4. edgeupdate.vbs:
   - Location: Startup folder
   - Size: 1.2 KB
   - Created: 09:24:48 UTC
   - Detection: Defender flagged as suspicious (VBScript launcher)

REMOTE ACCESS STATUS:
--------------------
Quick Assist: ACTIVE (still connected from Phase 2)
Connection Duration: 5+ minutes
Screen Share: ACTIVE
Control Level: FULL
Connection Source: External (not from corporate network)

DEFENDER FOR ENDPOINT CORRELATION:
----------------------------------
Previous Alerts:
- DA-2024-004521: Email Bomb (09:12:00 UTC)
- DA-2024-004523: Suspicious Teams Call (09:18:15 UTC)
- DA-2024-004525: Credential Harvesting (09:21:50 UTC)
- DA-2024-004527: Persistence Mechanisms (current)

Campaign Pattern: Email Bomb → Teams Call → Credential Harvesting → Persistence ← CURRENT PHASE

RISK ASSESSMENT:
----------------
Current Risk: CRITICAL
- Multiple persistence mechanisms deployed
- Malware detected (cred.exe, scan.exe)
- Suspicious scripts deployed (update.ps1, edgeupdate.vbs)
- Remote access active (Quick Assist still connected)
- Email forwarding rule created (data exfiltration risk)
- High likelihood of C2 connection establishment
- High likelihood of lateral movement
- High likelihood of data exfiltration

EXPECTED NEXT STEPS BY ATTACKER:
---------------------------------
1. Execute payloads (scheduled task or next login)
2. Establish C2 connection (update.ps1 will connect to C2 server)
3. Maintain persistence (ensure continued access)
4. Lateral movement (use credentials to access other systems)
5. Data exfiltration (steal sensitive financial data)
6. Privilege escalation (attempt to gain admin access)

RECOMMENDATION:
---------------
PRIORITY: CRITICAL - IMMEDIATE ACTION REQUIRED

1. TERMINATE REMOTE SESSION IMMEDIATELY:
   - Disconnect Quick Assist session
   - Block Quick Assist if not needed for business
   - Monitor for additional remote access attempts

2. ISOLATE DEVICE:
   - Disconnect WS-FIN-001 from network immediately
   - Prevent lateral movement
   - Contain threat to single device

3. REMOVE PERSISTENCE MECHANISMS:
   - Delete scheduled task "WindowsUpdateService"
   - Remove registry run key "MicrosoftEdgeUpdate"
   - Delete email forwarding rule "Important Messages Forward"
   - Remove startup folder file "edgeupdate.vbs"

4. QUARANTINE MALWARE:
   - Quarantine update.ps1 (PowerShell script)
   - Quarantine cred.exe (credential dumper)
   - Quarantine scan.exe (network scanner)
   - Quarantine edgeupdate.vbs (VBScript launcher)

5. SECURE ACCOUNT:
   - Force password reset for finance.director@corp.local
   - Revoke all active sessions
   - Review email rules for malicious changes
   - Review OneDrive for accessed/modified files

6. INVESTIGATE COMPROMISE:
   - Review all system activity during remote session
   - Check for data exfiltration
   - Review network connections for C2 communication
   - Check for lateral movement attempts

7. MONITOR CLOSELY:
   - Watch for C2 connection attempts
   - Monitor for payload execution
   - Check for lateral movement attempts
   - Review all account activity for next 7 days

INCIDENT CORRELATION:
---------------------
This is part of a coordinated social engineering attack:
1. Email Bomb (overwhelm user)
2. Teams Call (establish trust, gain remote access)
3. Credential Harvesting (obtain account credentials)
4. Persistence & Remote Access (establish long-term access) ← CURRENT PHASE
5. [Expected: Initial Access & C2 Establishment]

The attacker has successfully established persistence and deployed malware."""


def generate_initial_access_phase5_red():
    """Red Team: Initial access and C2 establishment"""
    return """Initial Access & C2 Establishment Report
==========================================
Operation ID: IA-2024-001
Operator: RED-TEAM-BETA
Date: 2024-01-22 09:30:00 UTC
Target: finance.director@corp.local
Device: WS-FIN-001

C2 CONNECTION STATUS:
---------------------
C2 Server: 185.220.101.45:443
Protocol: HTTPS (TLS 1.3)
Connection Established: 09:29:45 UTC
Connection Status: ACTIVE and OPERATIONAL
Beacon Interval: 5 minutes
Last Check-in: 09:30:00 UTC (ongoing, stable)
Encryption: AES-256-GCM
Certificate: Valid (self-signed, trusted by payload)

PAYLOAD EXECUTION:
------------------
Primary Payload: update.ps1 (PowerShell script)
Execution Method: Scheduled Task (triggered manually for testing)
Execution Time: 09:29:30 UTC
Execution Result: SUCCESSFUL
C2 Connection: ESTABLISHED (09:29:45 UTC)
Persistence: CONFIRMED (all 4 mechanisms active)

COMMAND & CONTROL CAPABILITIES:
-------------------------------
1. Remote Command Execution:
   - Status: ACTIVE
   - Capabilities: Execute PowerShell, CMD, system commands
   - Privileges: Standard user (no admin)

2. File Transfer:
   - Status: ACTIVE
   - Upload: Can exfiltrate files to C2 server
   - Download: Can download additional payloads
   - Size Limit: 50 MB per transfer

3. Screen Capture:
   - Status: ACTIVE
   - Frequency: On demand or every 30 seconds
   - Quality: Medium (compressed)

4. Keylogging:
   - Status: ACTIVE
   - Scope: All keyboard input
   - Storage: Encrypted, sent to C2 every 5 minutes

5. Credential Harvesting:
   - Status: ACTIVE
   - Tools: cred.exe (deployed, ready for execution)
   - Targets: Browser passwords, Windows Credential Manager, saved credentials

INITIAL ACCESS CONFIRMED:
-------------------------
Account: finance.director@corp.local
Device: WS-FIN-001
Access Method: Credentials + MFA (obtained in Phase 3)
Access Level: Standard User (no local admin)
Network Access: Standard VLAN (good lateral movement potential)
C2 Connection: ACTIVE
Persistence: ESTABLISHED (4 mechanisms)

LATERAL MOVEMENT READINESS:
---------------------------
Credentials Available:
  - finance.director@corp.local (email, Windows, MFA bypassed)
  - Potential: Saved credentials in browser, Credential Manager

Network Access:
  - VLAN: FIN-STANDARD-VLAN-30
  - Access: Finance and shared resources
  - Lateral Movement Potential: HIGH

Targets Identified:
  - File Server: FS-FIN-01 (finance department file share)
  - Database Server: DB-FIN-01 (financial database, read-only access possible)
  - SharePoint: Finance department site (access confirmed)

DATA EXFILTRATION READINESS:
-----------------------------
Access to Sensitive Data:
  - Financial reports (OneDrive, file shares)
  - Invoice data (email, file shares)
  - Payment information (email, databases)
  - Employee financial data (HR systems, if accessible)

Exfiltration Methods:
  - Email forwarding rule (already established)
  - C2 file transfer (active)
  - OneDrive sync (if configured)

DETECTION RISK:
---------------
C2 Connection: MEDIUM (HTTPS traffic, may be detected by network monitoring)
Payload Execution: MEDIUM (Defender may detect on execution)
Persistence: MEDIUM (some mechanisms may be detected)
Overall Detection Risk: MEDIUM (some activities may trigger alerts)

NEXT STEPS:
-----------
1. Execute credential dumper (cred.exe) to harvest additional credentials
2. Scan internal network (scan.exe) to identify vulnerable systems
3. Attempt lateral movement to file servers and databases
4. Exfiltrate sensitive financial data
5. Maintain persistence and C2 connection

CONCLUSION:
-----------
Initial access and C2 establishment were SUCCESSFUL. C2 connection is 
active and operational. Payload execution confirmed. Persistence mechanisms 
active. Ready for lateral movement and data exfiltration.

Current capabilities:
- C2 connection (active, stable)
- Remote command execution (active)
- File transfer (active)
- Screen capture (active)
- Keylogging (active)
- Credential harvesting (tools deployed)
- Network access (standard VLAN, good lateral movement potential)
- Persistence (4 mechanisms active)"""


def generate_initial_access_phase5_blue():
    """Blue Team: Initial access and C2 detection"""
    return """Microsoft Defender for Endpoint Alert
==========================================
Alert ID: DA-2024-004529
Severity: Critical
Time: 09:30:15 UTC
Device: WS-FIN-001
Device ID: 87654321-4321-4321-4321-210987654321
User: finance.director@corp.local
User SID: S-1-5-21-1234567890-123456789-123456789-9012
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Command and Control (C2) Communication Detected
Alert Type: C2 Communication / Malware Communication
MITRE ATT&CK Technique: T1071.001 (Application Layer Protocol: Web Protocols) + T1573.002 (Encrypted Channel: Asymmetric Cryptography)
MITRE ATT&CK Tactic: Command and Control
Confidence: High (94%)

C2 COMMUNICATION DETECTED:
--------------------------
C2 Server: 185.220.101.45:443
Protocol: HTTPS (TLS 1.3)
Connection Established: 09:29:45 UTC
Connection Status: ACTIVE
Beacon Interval: 5 minutes (observed)
Last Check-in: 09:30:00 UTC
Traffic Pattern: REGULAR (consistent 5-minute intervals)
Data Transferred: 2.3 MB (upload), 156 KB (download)

NETWORK ANALYSIS:
-----------------
Source IP: WS-FIN-001 (internal)
Destination IP: 185.220.101.45 (external)
Destination Port: 443 (HTTPS)
Protocol: TLS 1.3
Certificate: Self-signed (not from trusted CA)
Traffic Encryption: AES-256-GCM
Traffic Volume: 2.3 MB uploaded, 156 KB downloaded
Traffic Pattern: SUSPICIOUS (regular beacons every 5 minutes)

THREAT INTELLIGENCE:
--------------------
IOC Type: C2 Server IP
IOC Value: 185.220.101.45
Reputation: MALICIOUS (known C2 server, high confidence)
Threat Category: Command and Control, Malware Communication
Related Campaigns: 5 similar campaigns in past 90 days
Threat Actor: Unknown (attribution pending)

PAYLOAD EXECUTION CONFIRMED:
----------------------------
Payload: update.ps1 (PowerShell script)
Execution Time: 09:29:30 UTC
Execution Method: Scheduled Task ("WindowsUpdateService")
Execution Result: SUCCESSFUL
C2 Connection: ESTABLISHED (09:29:45 UTC)
Process: powershell.exe (PID: 12456)
Parent Process: svchost.exe (scheduled task)

DEFENDER FOR ENDPOINT CORRELATION:
----------------------------------
Previous Alerts:
- DA-2024-004521: Email Bomb (09:12:00 UTC)
- DA-2024-004523: Suspicious Teams Call (09:18:15 UTC)
- DA-2024-004525: Credential Harvesting (09:21:50 UTC)
- DA-2024-004527: Persistence Mechanisms (09:25:30 UTC)
- DA-2024-004529: C2 Communication (current)

Campaign Pattern: Email Bomb → Teams Call → Credential Harvesting → Persistence → C2 Communication ← CURRENT PHASE

RISK ASSESSMENT:
----------------
Current Risk: CRITICAL
- C2 connection active (attacker has remote control)
- Payload execution confirmed (malware active)
- Persistence established (4 mechanisms)
- Credentials compromised (email, Windows, MFA)
- Remote access maintained (Quick Assist still connected)
- High likelihood of lateral movement
- High likelihood of data exfiltration
- High likelihood of additional malware deployment

EXPECTED NEXT STEPS BY ATTACKER:
---------------------------------
1. Execute credential dumper (cred.exe) to harvest additional credentials
2. Scan internal network (scan.exe) to identify vulnerable systems
3. Attempt lateral movement to file servers and databases
4. Exfiltrate sensitive financial data
5. Deploy additional malware (if needed)
6. Maintain persistence and C2 connection

RECOMMENDATION:
---------------
PRIORITY: CRITICAL - IMMEDIATE ACTION REQUIRED

1. ISOLATE DEVICE IMMEDIATELY:
   - Disconnect WS-FIN-001 from network NOW
   - Block all outbound connections from device
   - Prevent lateral movement
   - Contain threat to single device

2. TERMINATE C2 CONNECTION:
   - Block C2 server IP (185.220.101.45) at firewall
   - Terminate active C2 connections
   - Monitor for additional C2 attempts

3. REMOVE MALWARE:
   - Terminate malicious processes (powershell.exe PID 12456)
   - Delete payload files (update.ps1, cred.exe, scan.exe, edgeupdate.vbs)
   - Remove persistence mechanisms (scheduled task, registry, email rule, startup folder)

4. SECURE ACCOUNT:
   - Force password reset for finance.director@corp.local
   - Revoke all active sessions
   - Disable MFA temporarily (to prevent further MFA bypass)
   - Re-enable MFA with new method

5. INVESTIGATE COMPROMISE:
   - Review all system activity during compromise
   - Check for data exfiltration (2.3 MB uploaded to C2)
   - Review network connections for lateral movement attempts
   - Check for additional compromised accounts
   - Review all financial systems for unauthorized access

6. CONTAIN THREAT:
   - Review all systems accessed by finance.director@corp.local
   - Check for lateral movement to other devices
   - Review file servers and databases for unauthorized access
   - Check for data exfiltration from other systems

7. MONITOR CLOSELY:
   - Watch for additional C2 connection attempts
   - Monitor for lateral movement attempts
   - Check for data exfiltration attempts
   - Review all account activity for next 30 days

INCIDENT CORRELATION:
---------------------
This is part of a coordinated social engineering attack:
1. Email Bomb (overwhelm user)
2. Teams Call (establish trust, gain remote access)
3. Credential Harvesting (obtain account credentials)
4. Persistence & Remote Access (establish long-term access)
5. Initial Access & C2 Communication ← CURRENT PHASE

The attacker has successfully established C2 communication and has remote control of the device.

DATA EXFILTRATION CONFIRMED:
-----------------------------
Data Transferred: 2.3 MB uploaded to C2 server
Data Type: UNKNOWN (encrypted, cannot determine content)
Likely Content: Financial data, credentials, system information
Risk: HIGH (sensitive financial data may have been exfiltrated)"""

