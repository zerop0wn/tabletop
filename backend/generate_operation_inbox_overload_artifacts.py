"""
Generate artifact content for the Operation Inbox Overload scenario.
Creates realistic Microsoft Defender, Teams logs, and Red Team tool outputs.
"""

def generate_phase0_red():
    """Red Team: Email flood campaign status"""
    return """Email Flood Campaign Status Report
=====================================
Campaign ID: EFO-2024-003
Operator: RED-TEAM-GAMMA
Date: 2024-01-22 09:30:00 UTC
Target: finance.director@corp.local

CAMPAIGN OVERVIEW:
------------------
Campaign Type: Email Flood (Look-Alike IT Domain)
Target Email: finance.director@corp.local
Total Emails Sent: 1,247
Emails Delivered: 892 (71.5% delivery rate)
Emails Blocked: 355 (28.5% blocked)
Delivery Method: Multiple look-alike IT domains
Sender Domains: 
  - it-support@corp-it.local (primary)
  - helpdesk@corp-support.net (secondary)
  - support@corp-it-services.com (tertiary)
  - tech@corp-it-help.net (backup)

EMAIL CHARACTERISTICS:
----------------------
Subject Lines Used:
  - "IT Support: Email System Maintenance Notice"
  - "Helpdesk: Inbox Configuration Update Required"
  - "IT Services: Email Client Optimization Alert"
  - "Support: Mailbox Storage Warning"
  - "Tech Support: Email Filter Settings Change"
  - "IT Department: Email Security Policy Update"
  - "Helpdesk: Outlook Sync Issue Resolution"
  - "IT Support: Email Delivery Status Report"

Content Strategy:
  - NO LINKS (critical for avoiding phishing detection)
  - NO ATTACHMENTS (reduces security scanning)
  - Professional IT support language
  - Legitimate-looking sender display names
  - Varied timing patterns to avoid rate limiting

TIMING STRATEGY:
---------------
Start Time: 09:00:00 UTC
Peak Delivery: 09:05:00 - 09:25:00 UTC (700+ emails in 20 minutes)
Current Status: ONGOING
Delivery Rate: ~30-40 emails per minute (sustained)
Expected Duration: 30-45 minutes total

IMPACT ASSESSMENT:
------------------
Inbox Overwhelmed: YES (892+ emails in inbox)
User Response: FRUSTRATED (user cannot find important emails)
Email Client Performance: SEVERELY DEGRADED (Outlook unresponsive)
User Productivity: COMPLETELY IMPACTED
Psychological State: STRESSED (user actively seeking help)
User Communication: User sent Teams message to IT support at 09:35 AM

NEXT PHASE READINESS:
---------------------
Target State: VULNERABLE (overwhelmed, seeking assistance, frustrated)
Optimal Timing: 5-10 minutes after user reaches out (09:40-09:45 AM)
Teams Call Prepared: YES (IT support impersonation ready)
Caller ID Configuration: CONFIGURED (appears as internal IT support)
Social Engineering Script: READY (email flood context established)
Trust Building: OPTIMAL (user believes emails are from IT)

CAMPAIGN SUCCESS METRICS:
-------------------------
Email Delivery Rate: 71.5% (EXCELLENT - above 70% target)
User Engagement: HIGH (user actively checking emails, seeking help)
Psychological Impact: HIGH (user reported frustration, seeking assistance)
Inbox Disruption: COMPLETE (inbox unusable, user cannot find emails)
Look-Alike Domain Effectiveness: EXCELLENT (no links = low detection)
Readiness for Phase 1: OPTIMAL (user vulnerable to callback social engineering)

CONCLUSION:
-----------
Email flood campaign is PROCEEDING AS PLANNED. Target inbox is overwhelmed 
with 892+ delivered emails from look-alike IT domains. User is frustrated, 
seeking help, and has reached out to IT support via Teams. Optimal conditions 
achieved for Phase 1 (Panic Driven Help-Seeking).

Ready to proceed with Teams DM and callback impersonation in 5-10 minutes."""


def generate_phase0_blue():
    """Blue Team: Defender for Office 365 email flood detection"""
    return """Microsoft Defender for Office 365 Alert
==========================================
Alert ID: DA-2024-005234
Severity: High
Time: 09:25:00 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Email Flood Attack Detected
Alert Type: Email Bomb / Spam Flood Campaign
Detection Method: Volume-based anomaly detection
Risk Score: 78/100

EMAIL VOLUME ANALYSIS:
---------------------
Total Emails Received: 1,247
Emails Delivered: 892 (71.5%)
Emails Blocked: 355 (28.5%)
Time Window: 30 minutes (09:00 - 09:30 UTC)
Peak Delivery Rate: 87 emails per minute (09:05 - 09:12 UTC)
Average Delivery Rate: 29.7 emails per minute

SENDER DOMAIN ANALYSIS:
-----------------------
Primary Sender Domains:
  1. corp-it.local (423 emails, 33.9%)
  2. corp-support.net (387 emails, 31.0%)
  3. corp-it-services.com (298 emails, 23.9%)
  4. corp-it-help.net (139 emails, 11.1%)

Domain Reputation:
  - corp-it.local: NEW DOMAIN (registered 14 days ago)
  - corp-support.net: NEW DOMAIN (registered 12 days ago)
  - corp-it-services.com: NEW DOMAIN (registered 18 days ago)
  - corp-it-help.net: NEW DOMAIN (registered 10 days ago)

Look-Alike Domain Analysis:
  - All domains closely resemble legitimate IT support domains
  - Domain names designed to appear as internal IT services
  - No previous email history from these domains
  - SPF records: Present but minimal (pass-through configuration)

EMAIL CONTENT ANALYSIS:
-----------------------
Subject Line Patterns:
  - "IT Support" (34% of emails)
  - "Helpdesk" (28% of emails)
  - "IT Services" (22% of emails)
  - "Tech Support" (16% of emails)

Content Characteristics:
  - NO SUSPICIOUS LINKS (critical finding)
  - NO ATTACHMENTS
  - Professional IT support language
  - Legitimate-looking sender display names
  - Varied timing patterns

Phishing Detection:
  - Link Analysis: NO LINKS DETECTED (unusual for phishing)
  - Attachment Analysis: NO ATTACHMENTS
  - Content Analysis: Professional language, no obvious phishing indicators
  - Sender Analysis: Look-alike domains, but no malicious links

USER IMPACT ASSESSMENT:
----------------------
Inbox Status: OVERWHELMED (892+ emails)
Email Client Performance: SEVERELY DEGRADED
User Productivity: COMPLETELY IMPACTED
User Response: User sent Teams message to IT support at 09:35 AM
User State: FRUSTRATED, SEEKING HELP

THREAT ASSESSMENT:
------------------
Attack Type: Email Flood / Spam Bomb
Primary Objective: Inbox Disruption
Secondary Objective: LIKELY - Preparation for callback social engineering
Risk Level: HIGH

Why This Is Suspicious:
  1. Look-alike IT domains (appears as legitimate IT support)
  2. NO LINKS (unusual for phishing - suggests callback attack)
  3. User seeking help (vulnerable to social engineering)
  4. Timing: Email flood followed by user reaching out for help
  5. Professional language (designed to appear legitimate)

RECOMMENDED ACTIONS:
--------------------
1. IMMEDIATE: Purge all messages from flood domains
2. IMMEDIATE: Block sending domains at transport rule level
3. CRITICAL: Notify user about email flood and potential callback attack
4. CRITICAL: Warn user NOT to trust unsolicited IT support calls
5. Monitor for follow-up social engineering attempts (Teams calls, etc.)

CONCLUSION:
-----------
This email flood attack is HIGHLY SUSPICIOUS. The combination of look-alike 
IT domains, no links, and user seeking help suggests this is preparation for 
a callback social engineering attack. The attacker wants the user to believe 
the emails are from IT support, making them vulnerable to a follow-up Teams 
call impersonation.

IMMEDIATE ACTION REQUIRED: Contain the email flood AND warn user about 
potential callback social engineering."""


def generate_phase1_red():
    """Red Team: Help-seeking engagement and trust building"""
    return """Teams Impersonation Preparation Report
==========================================
Campaign ID: EFO-2024-003
Phase: 1 - Panic Driven Help-Seeking
Operator: RED-TEAM-GAMMA
Date: 2024-01-22 09:38:00 UTC
Target: finance.director@corp.local

USER ENGAGEMENT STATUS:
-----------------------
User Communication: Teams message sent to IT support channel at 09:35 AM
Message Content: "I'm getting hundreds of emails and can't find anything. 
                  Can someone help me fix this?"
User Tone: FRUSTRATED, URGENT, SEEKING IMMEDIATE HELP
Response Time: User reached out 5 minutes after email flood peak
Trust Level: HIGH (user believes emails are from IT support)

TRUST BUILDING STRATEGY:
-----------------------
Phase 0 Success: Email flood created believable IT support context
User Perception: User believes emails are from legitimate IT support
Optimal Approach: Position as fastest path to help
Timing: User is actively seeking help (optimal vulnerability window)

NEXT STEPS - TRUST BUILDING:
----------------------------
1. Send Teams DM first (establish contact, build rapport)
2. Reference the email flood (show awareness of user's problem)
3. Position as IT support responding to their request
4. Then place a call (escalate to voice for higher trust)

ALTERNATIVE APPROACHES:
----------------------
Direct Call (No Prior Contact):
  - Faster but more suspicious
  - Lower success rate (user may not answer)
  - Higher risk of user suspicion

Email Follow-Up:
  - Adds noise, may reduce trust
  - User already overwhelmed with emails
  - Less effective for building rapport

External Link:
  - HIGH RISK - may trigger security detection
  - User may be suspicious of external links
  - Counterproductive to trust building

OPTIMAL STRATEGY:
----------------
Send Teams DM first, then place a call:
  - Establishes contact in familiar platform (Teams)
  - Builds rapport before voice contact
  - References user's problem (shows awareness)
  - Positions as legitimate IT support
  - Then escalates to voice for higher trust
  - Success Rate: HIGH (optimal trust-building sequence)

CURRENT STATUS:
--------------
User State: VULNERABLE (frustrated, seeking help, trusts IT support)
Trust Level: HIGH (user believes emails are from IT)
Optimal Timing: NOW (user actively seeking help)
Teams DM Prepared: YES (script ready, impersonation identity configured)
Call Prepared: YES (caller ID spoofed, social engineering script ready)

READINESS FOR PHASE 2:
---------------------
Trust Building: OPTIMAL (user vulnerable, seeking help)
Contact Method: Teams DM → Call (optimal sequence)
Timing: IMMEDIATE (user actively seeking help)
Success Probability: HIGH (optimal conditions achieved)

CONCLUSION:
-----------
User has reached out for help via Teams, indicating high vulnerability. 
Optimal strategy is to send Teams DM first to establish contact and build 
trust, then place a call. This trust-building sequence maximizes success 
probability for Phase 2 (Teams Impersonation Callback).

Ready to proceed with Teams DM and callback in next 2-5 minutes."""


def generate_phase1_blue():
    """Blue Team: User help-seeking behavior analysis"""
    return """Microsoft Teams Security Alert
==========================================
Alert ID: TS-2024-001892
Severity: Medium
Time: 09:36:00 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: User Help-Seeking Behavior After Email Flood
Alert Type: Potential Social Engineering Target
Detection Method: User communication pattern analysis
Risk Score: 65/100

USER COMMUNICATION ANALYSIS:
----------------------------
Communication Channel: Microsoft Teams
Message Recipient: IT Support Channel
Message Time: 09:35:00 UTC (5 minutes after email flood peak)
Message Content: "I'm getting hundreds of emails and can't find anything. 
                  Can someone help me fix this?"
User Tone: FRUSTRATED, URGENT, SEEKING IMMEDIATE HELP

TIMING ANALYSIS:
---------------
Email Flood Peak: 09:05 - 09:25 UTC
User Help Request: 09:35:00 UTC
Time Gap: 10 minutes after peak, 5 minutes after flood completion
Pattern: User reached out IMMEDIATELY after email flood
Risk Indicator: HIGH (user vulnerable to callback social engineering)

CONTEXT ANALYSIS:
----------------
Email Flood Context:
  - 892+ emails delivered from look-alike IT domains
  - User inbox overwhelmed
  - User cannot find important emails
  - User believes emails are from IT support (look-alike domains)

User Psychological State:
  - FRUSTRATED (inbox unusable)
  - URGENT (needs immediate help)
  - TRUSTING (believes emails are from IT support)
  - VULNERABLE (actively seeking help)

THREAT ASSESSMENT:
------------------
Primary Risk: Callback Social Engineering Attack
Attack Vector: Teams call impersonation
Timing: IMMEDIATE (user actively seeking help)
Success Probability: HIGH (user vulnerable, trusting, seeking help)

Why This Is High Risk:
  1. User reached out IMMEDIATELY after email flood
  2. User believes emails are from IT support (look-alike domains)
  3. User is frustrated and seeking immediate help
  4. User is vulnerable to unsolicited IT support contact
  5. Timing suggests coordinated attack (email flood → callback)

RECOMMENDED ACTIONS:
--------------------
1. CRITICAL: Send org-wide Teams broadcast warning about email flood and 
   potential callback social engineering
2. CRITICAL: Warn users NOT to trust unsolicited IT support calls
3. IMMEDIATE: Notify user about email flood and potential callback attack
4. Monitor for Teams calls from external numbers claiming to be IT support
5. Consider preemptive account security measures if risk is high

ALTERNATIVE ACTIONS:
-------------------
Reset User Password Only:
  - Addresses identity risk but doesn't address user awareness
  - User may still fall for callback if not warned
  - Risk: MEDIUM (partial mitigation)

Disable User Account Preemptively:
  - Strong containment but heavy-handed at this early stage
  - May impact business operations
  - Risk: LOW (overly cautious)

Do Nothing and Continue Monitoring:
  - Allows attack to progress
  - User may fall for callback social engineering
  - Risk: HIGH (insufficient mitigation)

OPTIMAL ACTION:
--------------
Send org-wide Teams broadcast about phishing/callback:
  - Proactive communication prevents callback success
  - Warns all users, not just affected user
  - Preempts attacker's social engineering attempt
  - Low business impact
  - Risk: LOW (optimal mitigation)

CONCLUSION:
-----------
User help-seeking behavior after email flood indicates HIGH RISK for callback 
social engineering attack. User is frustrated, trusting, and actively seeking 
help - optimal conditions for attacker to impersonate IT support via Teams call.

IMMEDIATE ACTION REQUIRED: Proactive communication to prevent callback 
social engineering success."""


def generate_phase2_red():
    """Red Team: Teams call impersonation execution"""
    return """Teams Impersonation Callback Report
==========================================
Campaign ID: EFO-2024-003
Phase: 2 - Teams Impersonation Callback
Operator: RED-TEAM-GAMMA
Date: 2024-01-22 09:45:00 UTC
Target: finance.director@corp.local

CALL EXECUTION STATUS:
----------------------
Call Initiated: 09:42:00 UTC
Call Duration: 6 minutes
Caller Identity: "IT Support - Corp IT Department"
Caller Number: External number (spoofed to appear internal)
Call Type: Microsoft Teams Voice Call
User Response: ANSWERED (user expecting IT support call)

TRUST BUILDING SUCCESS:
----------------------
Phase 1 Success: Teams DM sent at 09:40 AM, user responded positively
User Trust Level: HIGH (user believes caller is legitimate IT support)
Caller Credibility: ESTABLISHED (referenced email flood, user's problem)
Social Engineering: SUCCESSFUL (user granted screen share access)

SCREEN SHARE STATUS:
--------------------
Screen Share Requested: 09:43:00 UTC
Screen Share Granted: 09:43:15 UTC (user approved immediately)
Screen Share Duration: 4+ minutes (ongoing)
Screen Share Access: FULL (user's entire screen visible)
Current View: User's email client and account settings

WHAT WE CAN SEE:
----------------
1. User's email client (Outlook) - inbox overwhelmed with emails
2. User's account settings - Security and Privacy tab visible
3. User's Teams interface - active conversations visible
4. User's desktop - file explorer, other applications visible
5. User's browser - multiple tabs open, some with sensitive data

NEXT STEPS - CREDENTIAL HARVESTING:
------------------------------------
Current Objective: Guide user to Security and Privacy settings
Next Objective: Trick user into approving MFA reset
End Goal: Full account takeover with MFA bypass

ALTERNATIVE APPROACHES:
----------------------
Provide Fake Ticket Number and Internal Jargon:
  - Builds credibility but doesn't provide direct access
  - Good for trust but no immediate account access
  - Success Rate: MEDIUM (trust building, no access)

Ask User Directly for MFA Reset Code:
  - Higher risk but may provide immediate access
  - More suspicious, user may refuse
  - Success Rate: LOW-MEDIUM (higher suspicion)

Ask User to Install Remote Support Tool:
  - Highly suspicious, may trigger user suspicion
  - High detection risk
  - Success Rate: LOW (high suspicion)

OPTIMAL STRATEGY:
----------------
Ask user to share screen to show the issue:
  - Provides visibility into user's settings and account
  - Builds trust (shows we're helping with email issue)
  - Allows us to guide user to Security and Privacy settings
  - Enables us to see MFA reset prompts
  - Success Rate: HIGH (optimal for credential harvesting)

CURRENT STATUS:
--------------
Screen Share: ACTIVE (full access to user's screen)
User Trust: HIGH (user believes we're legitimate IT support)
Account Visibility: FULL (can see user's account settings)
MFA Reset Preparation: READY (can guide user to approve reset)
Timing: OPTIMAL (user vulnerable, trusting, screen share active)

READINESS FOR PHASE 3:
---------------------
Screen Share Access: ACTIVE (can guide user through MFA reset)
User Trust: HIGH (user will follow our guidance)
Account Settings: VISIBLE (can see Security and Privacy tab)
MFA Reset Readiness: OPTIMAL (can trick user into approving reset)
Success Probability: HIGH (optimal conditions achieved)

CONCLUSION:
-----------
Teams impersonation callback is PROCEEDING AS PLANNED. User has granted 
screen share access and trusts us as legitimate IT support. We can see user's 
account settings and are ready to guide user through MFA reset process.

Ready to proceed with MFA reset attempt in next 2-3 minutes."""


def generate_phase2_blue():
    """Blue Team: Teams call impersonation detection"""
    return """Microsoft Teams Security Alert
==========================================
Alert ID: TS-2024-002156
Severity: Critical
Time: 09:43:00 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious Teams Call with Screen Share
Alert Type: Potential Social Engineering Attack
Detection Method: Call analysis and caller verification
Risk Score: 92/100

CALL ANALYSIS:
--------------
Call Time: 09:42:00 UTC
Call Duration: 6 minutes (ongoing)
Caller Identity: "IT Support - Corp IT Department"
Caller Number: External number (not in internal directory)
Call Type: Microsoft Teams Voice Call
User Response: ANSWERED, GRANTED SCREEN SHARE ACCESS

CALLER VERIFICATION:
--------------------
Caller Number: +1-555-XXX-XXXX (external number)
Internal Directory Check: NOT FOUND (caller not in internal directory)
Teams Tenant Check: NOT FOUND (caller not in organization's Teams tenant)
Caller ID Spoofing: LIKELY (number appears internal but is external)
Legitimate IT Support: NO (caller not verified as internal IT support)

SCREEN SHARE ANALYSIS:
----------------------
Screen Share Requested: 09:43:00 UTC
Screen Share Granted: 09:43:15 UTC (user approved immediately)
Screen Share Duration: 4+ minutes (ongoing)
Screen Share Access: FULL (user's entire screen visible)
Risk Level: CRITICAL (attacker can see sensitive data and guide user actions)

CONTEXT ANALYSIS:
----------------
Email Flood Context:
  - User received 892+ emails from look-alike IT domains
  - User reached out for help via Teams at 09:35 AM
  - User believes emails are from IT support

Call Timing:
  - Call placed 7 minutes after user reached out for help
  - Call placed immediately after Teams DM from "IT Support"
  - Pattern: Email flood → User help request → Teams DM → Call
  - Risk Indicator: HIGH (coordinated social engineering attack)

THREAT ASSESSMENT:
------------------
Attack Type: Callback Social Engineering via Teams Impersonation
Attack Vector: Screen share access + social engineering
Primary Objective: Credential harvesting (likely MFA reset)
Risk Level: CRITICAL (user has granted screen share, attacker can see sensitive data)

Why This Is Critical:
  1. Caller not verified as internal IT support
  2. External number spoofed to appear internal
  3. Screen share granted (attacker can see sensitive data)
  4. Timing suggests coordinated attack (email flood → callback)
  5. User trusts caller (believes caller is legitimate IT support)

RECOMMENDED ACTIONS:
--------------------
1. CRITICAL: Disable user account immediately to prevent further compromise
2. CRITICAL: Terminate screen share session if possible
3. Monitor for MFA reset attempts or account access changes
4. Collect forensic evidence (call logs, screen share activity)
5. Notify user about social engineering attack

ALTERNATIVE ACTIONS:
-------------------
Validate Caller via Teams Tenant and Internal Directory:
  - Good verification but less disruptive
  - Takes time, attacker may proceed with attack
  - Risk: MEDIUM (partial mitigation, may be too late)

Allow Screen Share with External Caller:
  - Exposes sensitive information to attacker
  - Allows attacker to guide user through account changes
  - Risk: HIGH (insufficient mitigation)

Monitor Call and Collect More Evidence Only:
  - Gives attacker time to proceed with attack
  - User may approve MFA reset or provide credentials
  - Risk: CRITICAL (insufficient mitigation, attack proceeds)

OPTIMAL ACTION:
--------------
Disable user account immediately:
  - Strong containment prevents further compromise
  - Stops attacker from gaining account access
  - Prevents MFA reset or credential harvesting
  - Risk: LOW (optimal mitigation)

CONCLUSION:
-----------
Suspicious Teams call with screen share access indicates CRITICAL RISK for 
credential harvesting attack. Caller is not verified as internal IT support, 
and user has granted full screen share access. This is likely a coordinated 
social engineering attack following the email flood.

IMMEDIATE ACTION REQUIRED: Disable user account to prevent credential 
harvesting and account takeover."""


def generate_phase3_red():
    """Red Team: MFA reset and account takeover"""
    return """MFA Reset and Account Takeover Report
==========================================
Campaign ID: EFO-2024-003
Phase: 3 - MFA Reset Attempt & Endpoint Foothold
Operator: RED-TEAM-GAMMA
Date: 2024-01-22 09:50:00 UTC
Target: finance.director@corp.local

MFA RESET STATUS:
----------------
MFA Reset Requested: 09:48:00 UTC (during screen share)
MFA Reset Approved: 09:48:15 UTC (user approved immediately)
MFA Reset Completed: 09:48:30 UTC
Account Access: SUCCESSFUL (full account takeover achieved)

ACCOUNT ACCESS CONFIRMED:
-------------------------
Login Time: 09:48:45 UTC
Login IP: 185.220.101.45 (external IP)
Login Device: Unrecognized device (new browser session)
Account Access: FULL (email, OneDrive, Teams, SharePoint)
Session Status: ACTIVE (ongoing)

WHAT WE CAN ACCESS:
-------------------
1. Email: Full inbox access, can read/send emails
2. OneDrive: Full file access, can download/upload files
3. Teams: Full access to conversations and channels
4. SharePoint: Full access to shared documents and sites
5. Account Settings: Can modify security settings, create app passwords

ENDPOINT FOOTHOLD STATUS:
------------------------
Current Objective: Establish endpoint persistence
Endpoint Access: NOT YET ESTABLISHED (account access only)
Next Step: Deploy persistence mechanism on user's device
Risk: User device may have EDR (Defender for Endpoint)

NEXT STEPS - PERSISTENCE:
-------------------------
Current Objective: Create app password or mailbox forwarding rule
Next Objective: Establish long-term access that survives password resets
End Goal: Maintain access even if account is secured

ALTERNATIVE APPROACHES:
----------------------
Ask User to Navigate to Security and Privacy Settings:
  - Good step toward MFA reset but doesn't provide immediate access
  - User may become suspicious
  - Success Rate: MEDIUM (preparation, no immediate access)

Access SharePoint/OneDrive from Compromised Session:
  - Gets data but doesn't provide long-term control
  - No persistence mechanism
  - Success Rate: MEDIUM (data access, no persistence)

Attempt to Install Malicious Support Application:
  - High chance of user suspicion and detection
  - EDR may detect malicious application
  - Success Rate: LOW (high detection risk)

OPTIMAL STRATEGY:
----------------
Trick user into approving MFA reset prompt:
  - Provides full account takeover
  - Bypasses MFA protection
  - Enables long-term access
  - Success Rate: HIGH (optimal for account takeover)

CURRENT STATUS:
--------------
Account Access: ACTIVE (full account takeover achieved)
MFA Bypassed: YES (MFA reset approved, new MFA method configured)
Session Status: ACTIVE (logged in from external IP)
Endpoint Access: NOT YET ESTABLISHED (account access only)
Persistence Readiness: READY (can create app passwords, mailbox rules)

READINESS FOR PHASE 4:
---------------------
Account Takeover: COMPLETE (full account access achieved)
MFA Bypassed: YES (new MFA method configured)
Persistence Preparation: READY (can create app passwords, mailbox rules)
Long-Term Access: POSSIBLE (can establish persistence mechanisms)
Success Probability: HIGH (optimal conditions achieved)

CONCLUSION:
-----------
MFA reset and account takeover is COMPLETE. User approved MFA reset during 
screen share, and we now have full account access. We can access email, 
OneDrive, Teams, and SharePoint. Ready to establish persistence mechanisms 
for long-term access.

Ready to proceed with persistence establishment in next 2-3 minutes."""


def generate_phase3_blue():
    """Blue Team: MFA reset and account compromise detection"""
    return """Microsoft Defender for Identity Alert
==========================================
Alert ID: DI-2024-003478
Severity: Critical
Time: 09:49:00 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious MFA Reset and Account Access
Alert Type: Account Takeover / Credential Compromise
Detection Method: MFA reset detection + suspicious login
Risk Score: 95/100

MFA RESET DETECTION:
--------------------
MFA Reset Time: 09:48:15 UTC
MFA Reset Method: User-approved reset (during screen share session)
MFA Reset Context: Screen share active, external caller guiding user
MFA Reset Approval: User approved immediately (no verification)
Risk Indicator: CRITICAL (MFA reset during suspicious screen share)

SUSPICIOUS LOGIN DETECTION:
---------------------------
Login Time: 09:48:45 UTC (30 seconds after MFA reset)
Login IP: 185.220.101.45 (external IP, not in whitelist)
Login Device: Unrecognized device (new browser session)
Login Location: Unknown location (geolocation mismatch)
Account Access: FULL (email, OneDrive, Teams, SharePoint)
Session Status: ACTIVE (ongoing)

ACCOUNT COMPROMISE CONFIRMED:
------------------------------
Compromise Method: MFA reset during screen share social engineering
Compromise Time: 09:48:15 UTC (MFA reset approved)
Account Access: FULL (attacker has full account control)
Data at Risk: Email, OneDrive files, Teams conversations, SharePoint documents
Risk Level: CRITICAL (full account takeover confirmed)

ENDPOINT RISK ASSESSMENT:
-------------------------
Endpoint Compromise: UNKNOWN (account access confirmed, endpoint status unclear)
Defender for Endpoint Status: ACTIVE (endpoint protection enabled)
Endpoint Isolation: NOT YET ISOLATED (endpoint may be compromised)
Risk: HIGH (attacker may have endpoint access via account)

THREAT ASSESSMENT:
------------------
Attack Type: Account Takeover via MFA Reset Social Engineering
Attack Vector: Screen share + MFA reset approval
Primary Objective: Account access and data exfiltration
Secondary Objective: Endpoint foothold and persistence
Risk Level: CRITICAL (full account takeover, potential endpoint compromise)

Why This Is Critical:
  1. MFA reset approved during suspicious screen share
  2. Immediate login from external IP after MFA reset
  3. Full account access confirmed (email, OneDrive, Teams, SharePoint)
  4. Endpoint may be compromised (attacker may have device access)
  5. Data exfiltration risk is HIGH (attacker can access all data)

RECOMMENDED ACTIONS:
--------------------
1. CRITICAL: Isolate host in Defender for Endpoint (stops active access + preserves evidence)
2. CRITICAL: Disable user account (prevents further account abuse)
3. Monitor for data exfiltration attempts (OneDrive, SharePoint, email)
4. Collect forensic evidence (login logs, MFA reset logs, screen share activity)
5. Revoke all active sessions (terminate attacker's session)

ALTERNATIVE ACTIONS:
-------------------
Disable User Account Only:
  - Strong identity containment but doesn't address endpoint risk
  - Endpoint may still be compromised
  - Risk: MEDIUM (partial mitigation)

Revoke Active Sessions Only:
  - Better than nothing but doesn't address endpoint or persistence
  - Attacker may have established persistence mechanisms
  - Risk: MEDIUM (insufficient mitigation)

Take No Action Until More Logs Are Collected:
  - Allows attacker to proceed with data exfiltration and persistence
  - Endpoint may be compromised
  - Risk: CRITICAL (insufficient mitigation, attack proceeds)

OPTIMAL ACTION:
--------------
Isolate host in Defender for Endpoint:
  - Stops active hands-on-keyboard access
  - Preserves evidence for forensic analysis
  - Prevents endpoint compromise and lateral movement
  - Addresses both identity and endpoint risk
  - Risk: LOW (optimal mitigation)

CONCLUSION:
-----------
MFA reset and account takeover is CONFIRMED. Attacker has full account access 
and may have endpoint access. This is a CRITICAL security incident requiring 
immediate containment of both identity and endpoint.

IMMEDIATE ACTION REQUIRED: Isolate host in Defender for Endpoint to stop 
active access and preserve evidence."""


def generate_phase4_red():
    """Red Team: Persistence establishment"""
    return """Persistence Establishment Report
==========================================
Campaign ID: EFO-2024-003
Phase: 4 - Persistence vs Containment
Operator: RED-TEAM-GAMMA
Date: 2024-01-22 09:55:00 UTC
Target: finance.director@corp.local

PERSISTENCE STATUS:
------------------
Account Access: ACTIVE (full account takeover achieved)
MFA Bypassed: YES (new MFA method configured)
Session Status: ACTIVE (logged in from external IP)
Persistence Mechanisms: NOT YET ESTABLISHED (account access only)
Long-Term Access: AT RISK (account may be disabled or password reset)

PERSISTENCE OBJECTIVES:
-----------------------
Primary Objective: Create persistence mechanisms that survive password resets
Secondary Objective: Maintain access even if account is secured
End Goal: Long-term access for data exfiltration and lateral movement

AVAILABLE PERSISTENCE METHODS:
------------------------------
1. App Password for IMAP/Legacy Auth:
   - Bypasses MFA for email access
   - Survives password resets
   - Low detection risk
   - Success Rate: HIGH (optimal persistence tactic)

2. Mailbox Forwarding Rule:
   - Forwards all emails to external address
   - Long-term data exfiltration
   - Survives password resets
   - Success Rate: MEDIUM-HIGH (good persistence method)

3. Conditional Access Policy Modification:
   - Modifies access policies
   - May allow future access
   - High detection risk
   - Success Rate: LOW-MEDIUM (high detection risk)

4. One-Time Data Exfiltration:
   - Gets data but no persistence
   - No long-term access
   - Success Rate: LOW (no persistence)

NEXT STEPS - PERSISTENCE:
-------------------------
Current Objective: Create app password for IMAP/legacy auth
Next Objective: Create mailbox forwarding rule for long-term exfiltration
End Goal: Maintain access even if account is disabled or password reset

ALTERNATIVE APPROACHES:
----------------------
Create Mailbox Forwarding Rule to External Address:
  - Good long-term exfiltration method
  - Survives password resets
  - Medium detection risk
  - Success Rate: MEDIUM-HIGH (good persistence method)

Perform One-Time Data Exfiltration Only:
  - Gets data but no persistence
  - No long-term access
  - Success Rate: LOW (no persistence)

Attempt Another MFA Reset After Being Blocked:
  - Noisy and likely to fail
  - High detection risk
  - Success Rate: LOW (high detection risk)

OPTIMAL STRATEGY:
----------------
Create app password for IMAP/legacy auth:
  - Bypasses MFA for email access
  - Survives password resets
  - Low detection risk
  - Provides long-term email access
  - Success Rate: HIGH (optimal persistence tactic)

CURRENT STATUS:
--------------
Account Access: ACTIVE (full account takeover achieved)
Persistence Mechanisms: NOT YET ESTABLISHED (account access only)
App Password Creation: READY (can create app password for IMAP/legacy auth)
Mailbox Forwarding: READY (can create forwarding rule)
Long-Term Access: AT RISK (account may be disabled or password reset)

READINESS FOR LONG-TERM ACCESS:
-------------------------------
Persistence Preparation: READY (can create app passwords, mailbox rules)
Account Access: ACTIVE (can create persistence mechanisms)
Long-Term Access: POSSIBLE (can establish persistence that survives resets)
Success Probability: HIGH (optimal conditions achieved)

CONCLUSION:
-----------
Account takeover is COMPLETE, but persistence mechanisms are NOT YET 
ESTABLISHED. We need to create app passwords or mailbox forwarding rules to 
maintain long-term access even if the account is secured. App password for 
IMAP/legacy auth is the optimal persistence tactic.

Ready to proceed with persistence establishment in next 1-2 minutes."""


def generate_phase4_blue():
    """Blue Team: Persistence detection and containment"""
    return """Microsoft Defender for Office 365 Alert
==========================================
Alert ID: DO-2024-004567
Severity: Critical
Time: 09:53:00 UTC
User: finance.director@corp.local
Department: Finance
Domain: CORP.LOCAL

ALERT DETAILS:
--------------
Alert Title: Suspicious Persistence Mechanisms Detected
Alert Type: Account Persistence / Token Abuse
Detection Method: Policy change detection + token activity analysis
Risk Score: 98/100

PERSISTENCE MECHANISM DETECTION:
---------------------------------
App Password Creation Attempt: DETECTED (09:52:00 UTC)
Mailbox Forwarding Rule Creation Attempt: DETECTED (09:52:15 UTC)
Conditional Access Policy Modification Attempt: DETECTED (09:52:30 UTC)
Token Refresh Attempts: DETECTED (multiple attempts from external IP)
Risk Indicator: CRITICAL (attacker establishing persistence mechanisms)

TOKEN ACTIVITY ANALYSIS:
------------------------
Active Tokens: 3 tokens from external IP (185.220.101.45)
Token Types: 
  - OAuth access token (email, OneDrive, Teams)
  - App password token (IMAP/legacy auth) - CREATION ATTEMPTED
  - Refresh token (long-term access) - ACTIVE
Token Expiration: Refresh token valid for 90 days
Risk: HIGH (attacker has long-term access tokens)

ACCOUNT STATUS:
---------------
Account Access: CONFIRMED (attacker has full account control)
MFA Bypassed: YES (MFA reset approved during screen share)
Session Status: ACTIVE (attacker logged in from external IP)
Persistence Mechanisms: ATTEMPTED (app password, mailbox forwarding, policy changes)
Long-Term Access Risk: CRITICAL (attacker establishing persistence)

THREAT ASSESSMENT:
------------------
Attack Type: Account Persistence Establishment
Attack Vector: App passwords, mailbox forwarding, token abuse
Primary Objective: Long-term access that survives password resets
Secondary Objective: Data exfiltration and lateral movement
Risk Level: CRITICAL (attacker establishing persistence, long-term access risk)

Why This Is Critical:
  1. App password creation attempted (bypasses MFA, survives password resets)
  2. Mailbox forwarding rule creation attempted (long-term data exfiltration)
  3. Conditional access policy modification attempted (may allow future access)
  4. Active refresh tokens (long-term access for 90 days)
  5. Account may remain compromised even after password reset

RECOMMENDED ACTIONS:
--------------------
1. CRITICAL: Full token revoke and add Conditional Access block
   - Revokes all authentication tokens (OAuth, app passwords, refresh tokens)
   - Adds conditional access policy block for the account
   - Breaks all persistence mechanisms
   - Hardens future access (prevents token-based persistence)
   - Risk: LOW (optimal mitigation)

2. Disable user account only:
   - Stops immediate abuse but doesn't address token-based persistence
   - App passwords and refresh tokens may remain active
   - Risk: MEDIUM (partial mitigation)

3. Reset user password only:
   - Addresses credential-based access but leaves tokens and app passwords active
   - Refresh tokens may remain valid
   - Risk: MEDIUM (insufficient mitigation)

4. Enable extra logging and auditing only:
   - Observation only, doesn't stop the attack
   - Attacker may establish persistence mechanisms
   - Risk: CRITICAL (insufficient mitigation)

OPTIMAL ACTION:
--------------
Full token revoke and add Conditional Access block:
  - Revokes ALL tokens (OAuth, app passwords, refresh tokens)
  - Breaks ALL persistence mechanisms
  - Hardens future access (prevents token-based persistence)
  - Ensures attacker cannot regain access even with credentials
  - Risk: LOW (optimal mitigation)

CONCLUSION:
-----------
Persistence mechanism establishment is DETECTED. Attacker is attempting to 
create app passwords, mailbox forwarding rules, and modify conditional access 
policies. This is a CRITICAL security incident requiring immediate token 
revocation and policy hardening to break all persistence mechanisms.

IMMEDIATE ACTION REQUIRED: Full token revoke and Conditional Access block to 
break all persistence and harden future access."""

