"""
Redesigned Ransomware Scenario - Artifact-Driven Decisions
This file contains the redesigned phases with artifact-driven decision making.
"""

# Phase 1: Initial Compromise - REDESIGNED
# Decision: Which phishing target to focus on (Finance vs Marketing)
# Artifacts will show which target is more vulnerable

PHASE_1_REDESIGN = {
    "name": "Phase 1: Initial Compromise",
    "briefing_text": """At 08:15 AM, your phishing campaign has successfully delivered emails to two departments:
- Finance Department: 12 emails opened, 3 links clicked
- Marketing Department: 8 emails opened, 2 links clicked

Both departments have users who clicked the malicious links. You now have initial access attempts on workstations in both departments. However, you have limited resources and want to focus your efforts on the target that offers the **best chance of establishing a persistent foothold without immediate detection**.

You've collected initial reconnaissance data on both targets. Your decision: **Which department should you prioritize for establishing persistence?**

- Option A: Focus on Finance Department (WS-FIN-042)
- Option B: Focus on Marketing Department (WS-MKT-015)
- Option C: Split efforts between both departments

**Remember:** Review the artifacts carefully. They contain critical information about security posture, EDR coverage, and user privileges that will determine your success.""",
    "red_objective": "Analyze the reconnaissance data from both departments to identify which target offers the best opportunity for establishing persistent access with minimal detection risk. Focus your initial persistence efforts on the most vulnerable target.",
    "blue_objective": "Review security telemetry from both departments to identify which department shows the most concerning indicators of compromise. Prioritize containment and investigation efforts on the department with the highest risk of successful attacker persistence.",
}

# Phase 3: Privilege Escalation - REDESIGNED (the two-host example)
PHASE_3_REDESIGN = {
    "name": "Phase 3: Privilege Escalation & Lateral Movement",
    "briefing_text": """You have successfully established user-level access on two workstations:
- WS-FIN-01 (Finance Department)
- WS-MKT-02 (Marketing Department)

Your goal is to escalate to local administrator / SYSTEM privileges on at least one host to enable ransomware deployment and lateral movement. However, you have limited time and want to focus your escalation attempt where there is a **high probability of success**.

You've collected system information and vulnerability intelligence on both hosts. Your decision: **Which host should you prioritize for privilege escalation?**

- Option A: Attempt privilege escalation on WS-FIN-01 using generic token-stealing and UAC bypass techniques
- Option B: Attempt privilege escalation on WS-MKT-02 using the specific local privilege escalation exploit identified in vulnerability scans
- Option C: Split efforts and run automated priv-esc tooling on both hosts in parallel

**Remember:** Review the artifacts carefully. They contain system information, patch levels, EDR status, and vulnerability scan results that will determine your success.""",
    "red_objective": "Analyze system information and vulnerability data from both hosts to identify which target offers the best opportunity for successful privilege escalation. Focus your escalation attempt on the host with the highest probability of success based on the evidence.",
    "blue_objective": "Review security telemetry and vulnerability scan data to identify which host is at greater risk of imminent privilege escalation. Prioritize containment and investigation efforts on the host with the highest risk based on the evidence.",
}

# Phase 4: Data Exfiltration - REDESIGNED
# Decision: Which data source to prioritize (File Server 1 vs File Server 2)
PHASE_4_REDESIGN = {
    "name": "Phase 4: Data Exfiltration",
    "briefing_text": """You have successfully obtained domain administrator credentials and have access to multiple file servers:
- FS-01 (Finance File Server): Contains financial records, customer PII, and proprietary research data
- FS-02 (HR/Operations File Server): Contains employee records, HR data, and operational documents

Both servers contain valuable data, but you have limited time before defenders detect your presence. You need to prioritize which data source to exfiltrate first to maximize the value of stolen data while minimizing detection risk.

You've mapped network paths, analyzed data classification, and reviewed access logs. Your decision: **Which file server should you prioritize for data exfiltration?**

- Option A: Prioritize exfiltration from FS-01 (Finance) - High-value financial and customer data
- Option B: Prioritize exfiltration from FS-02 (HR/Operations) - Employee records and operational data
- Option C: Exfiltrate from both servers simultaneously using parallel streams

**Remember:** Review the artifacts carefully. They contain network topology, data classification, DLP policies, and monitoring coverage that will determine your success and detection risk.""",
    "red_objective": "Analyze network topology, data classification, and monitoring coverage to identify which file server offers the best opportunity for successful data exfiltration with minimal detection. Prioritize exfiltration from the source that provides maximum value with lowest detection risk.",
    "blue_objective": "Review network monitoring, data loss prevention (DLP) alerts, and access logs to identify which file server is at greatest risk of data exfiltration. Prioritize containment and monitoring efforts on the server with the highest risk based on the evidence.",
}

