"""
Generate artifact files for the new artifact-driven Ransomware scenario.
Creates realistic Microsoft Defender, Sentinel, and Red Team tool outputs.
"""
import os
from pathlib import Path

# Artifacts directory
ARTIFACTS_DIR = Path(__file__).parent / "artifacts" / "files"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def create_phase1_artifacts():
    """Phase 1: Initial Access - IT vs Sales Department"""
    
    # Blue Team: IT Department Alert
    content = """Microsoft Defender for Endpoint Alert
Alert ID: DA-2024-002456
Severity: High
Time: 09:23:15 UTC
Device: WS-IT-089
User: it.admin@corp.local
Department: IT

Alert Details:
- Alert Title: Suspicious email attachment execution detected
- Process: mshta.exe
- Parent Process: outlook.exe
- File Hash: 9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f
- Action Taken: BLOCKED by Defender for Endpoint
- EDR Agent Status: Active, Latest Version (10.0.26100.1)
- Defender Antivirus: Enabled, Real-time Protection: ON
- Cloud Protection: Enabled
- Last Scan: 09:00:00 UTC (Clean)

Additional Context:
- Device is fully onboarded to Microsoft Defender for Endpoint
- Advanced Threat Protection (ATP) enabled
- Automated Investigation: Triggered immediately
- Device Risk Score: Low (35/100) - Strong security posture
- User has Domain Admin privileges (high-value target)
- Network segmentation: Isolated VLAN
- Last Security Update: 1 day ago

Recommendation: Attack blocked successfully. Device isolated automatically. Low risk of persistence."""
    
    with open(ARTIFACTS_DIR / "defender_it_alert_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: defender_it_alert_phase1.txt")
    
    # Blue Team: Sales Department Alert
    content = """Microsoft Defender for Endpoint Alert
Alert ID: DA-2024-002457
Severity: Medium
Time: 09:24:32 UTC
Device: WS-SLS-203
User: sales.rep@corp.local
Department: Sales

Alert Details:
- Alert Title: Suspicious script execution detected
- Process: wscript.exe
- Parent Process: outlook.exe
- File Hash: 8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e
- Action Taken: DETECTED (not blocked)
- EDR Agent Status: Active but Outdated (Version 10.0.19045.1 - Last updated: 60 days ago)
- Defender Antivirus: Enabled, Real-time Protection: ON
- Cloud Protection: Enabled (but agent outdated)
- Last Scan: 08:30:00 UTC (Clean)

Additional Context:
- Device is onboarded to Microsoft Defender for Endpoint but agent is outdated
- Advanced Threat Protection (ATP): Enabled but may have coverage gaps
- Automated Investigation: Not triggered (agent outdated, reduced capabilities)
- Device Risk Score: High (82/100) - Due to outdated agent and successful execution
- User has Standard User privileges (but local admin account present)
- Network segmentation: Standard VLAN (less restricted)
- Last Security Update: 60 days ago

WARNING: Outdated EDR agent may have reduced detection capabilities. Script executed successfully. Device requires immediate attention."""
    
    with open(ARTIFACTS_DIR / "defender_sales_alert_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: defender_sales_alert_phase1.txt")
    
    # Blue Team: Sentinel Analysis
    content = """Microsoft Sentinel Incident Report
Incident ID: INC-2024-00289
Title: Phishing Campaign - IT and Sales Departments Affected
Severity: High
Status: Active Investigation

Summary:
Phishing emails delivered to two departments:
- IT Department: 8 emails opened, 2 links clicked
- Sales Department: 15 emails opened, 5 links clicked

Email Security (Microsoft Defender for Office 365):
- IT emails: 6/8 blocked by Safe Links, 2/8 delivered
- Sales emails: 5/15 blocked, 10/15 delivered
- Overall: 11/23 emails blocked (48% success rate)

Endpoint Response:
- IT (WS-IT-089): Alert generated, action BLOCKED by Defender for Endpoint
- Sales (WS-SLS-203): Alert generated, action DETECTED (not blocked)

Risk Assessment:
- IT Department: Low Risk - Strong EDR coverage, latest agent, attack blocked
- Sales Department: High Risk - Outdated EDR agent, detection only (not blocked), script executed

Network Analysis:
- IT Department: Isolated VLAN, restricted network access
- Sales Department: Standard VLAN, broader network access

Recommendation: Prioritize investigation and containment of Sales department endpoint (WS-SLS-203) due to higher risk score, outdated security controls, and successful script execution."""
    
    with open(ARTIFACTS_DIR / "sentinel_phishing_analysis_new_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: sentinel_phishing_analysis_new_phase1.txt")
    
    # Red Team: IT Reconnaissance
    content = """Target: IT Department (WS-IT-089)
User: it.admin@corp.local

Initial Access Status:
✓ Email delivered: YES
✓ Link clicked: YES
✓ Payload executed: YES
✓ C2 beacon established: NO (blocked)

System Information:
- OS: Windows 11 Enterprise (Build 22621)
- Domain: CORP.LOCAL
- User Privileges: Domain Administrator (high-value)
- EDR Agent: Microsoft Defender for Endpoint - ACTIVE, Latest Version
- Defender Status: Real-time protection ON, Cloud protection ON
- Last Security Update: 1 day ago
- Network: Isolated VLAN (restricted access)

Security Posture Assessment:
- EDR Coverage: EXCELLENT (latest agent, active monitoring)
- Detection Risk: VERY HIGH (attack was BLOCKED immediately)
- Persistence Difficulty: VERY HIGH (requires bypassing strong EDR)
- User Privileges: HIGH (domain admin, but strong security)
- Network Isolation: HIGH (isolated VLAN, limited lateral movement)

Assessment: High-value target (domain admin) but EXCELLENT security controls. Attack was blocked immediately. Establishing persistence will be extremely difficult and high-risk. Not recommended for initial persistence."""
    
    with open(ARTIFACTS_DIR / "it_recon_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: it_recon_phase1.txt")
    
    # Red Team: Sales Reconnaissance
    content = """Target: Sales Department (WS-SLS-203)
User: sales.rep@corp.local

Initial Access Status:
✓ Email delivered: YES
✓ Link clicked: YES
✓ Payload executed: YES
✓ C2 beacon established: YES (active)

System Information:
- OS: Windows 10 Enterprise (Build 19045)
- Domain: CORP.LOCAL
- User Privileges: Standard User (but local admin account present)
- EDR Agent: Microsoft Defender for Endpoint - OUTDATED (Version 19045.1, 60 days old)
- Defender Status: Real-time protection ON, but agent outdated
- Last Security Update: 60 days ago
- Network: Standard VLAN (broader access)

Security Posture Assessment:
- EDR Coverage: WEAK (outdated agent, may have detection gaps)
- Detection Risk: MEDIUM (attack was DETECTED but not blocked)
- Persistence Difficulty: MEDIUM (local admin account available, weaker EDR)
- User Privileges: MEDIUM (standard user but admin on device)
- Network Isolation: LOW (standard VLAN, good lateral movement potential)

Assessment: Medium-value target with WEAKER security controls. Attack was detected but not blocked. Outdated EDR agent provides opportunity for persistence with lower detection risk. Better target for establishing foothold."""
    
    with open(ARTIFACTS_DIR / "sales_recon_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: sales_recon_phase1.txt")
    
    # Red Team: C2 Status Comparison
    content = """C2 Communication Status Report

Target 1: WS-IT-089 (IT Department)
- Connection: ESTABLISHED then TERMINATED
- Server: 185.220.101.78:443
- Status: BLOCKED by Defender for Endpoint
- Last Check-in: 09:23:18 UTC (then blocked)
- Detection: VERY HIGH - Defender blocked connection immediately
- Persistence: FAILED - All persistence mechanisms blocked
- Risk: HIGH - Strong EDR, isolated network

Target 2: WS-SLS-203 (Sales Department)
- Connection: ACTIVE
- Server: 185.220.101.78:443
- Status: OPERATIONAL
- Last Check-in: 09:24:35 UTC (ongoing, stable)
- Detection: MEDIUM - Detected but not blocked
- Persistence: PARTIAL - Some mechanisms successful
- Risk: MEDIUM - Outdated EDR, standard network

Recommendation: Focus persistence efforts on WS-SLS-203 (Sales). IT target has excellent EDR and blocked our attack immediately. Sales target has outdated agent and better opportunity for successful persistence with lower detection risk."""
    
    with open(ARTIFACTS_DIR / "c2_status_comparison_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: c2_status_comparison_phase1.txt")


def create_phase2_artifacts():
    """Phase 2: Establishing Persistence"""
    
    # Blue Team: Process Monitoring
    content = """Microsoft Defender for Endpoint - Process Monitoring Report
Device: WS-SLS-203
Time Range: 09:25:00 - 09:35:00 UTC

Detected Processes:
1. Scheduled Task Creation Attempt
   - Process: schtasks.exe
   - Command: /Create /TN "UpdateCheck" /TR "powershell.exe -File C:\\Temp\\payload.dll"
   - Status: DETECTED and LOGGED
   - Detection Confidence: High
   - Action: Alert generated, process monitored
   - Scheduled Task: Created successfully (not blocked)

2. Registry Modification Attempt
   - Process: reg.exe
   - Location: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
   - Value: "UpdateCheck"
   - Status: DETECTED and LOGGED
   - Detection Confidence: Medium
   - Action: Alert generated, change logged
   - Registry Key: Modified successfully (not blocked)

3. Service Creation Attempt
   - Process: sc.exe
   - Service Name: "WindowsUpdateService"
   - Status: DETECTED and BLOCKED
   - Detection Confidence: Very High
   - Action: Service creation blocked by Defender
   - Service: NOT created

Analysis:
- Scheduled Tasks: Defender detects but does not block creation (monitoring only)
- Registry Run Keys: Defender detects but does not block modification (monitoring only)
- Service Creation: Defender actively blocks service creation attempts

Recommendation: Monitor scheduled tasks and registry keys. Service creation is well-protected."""
    
    with open(ARTIFACTS_DIR / "defender_process_monitoring_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: defender_process_monitoring_phase2.txt")
    
    # Red Team: Detection Test Results
    content = """Persistence Mechanism Detection Test Results
Target: WS-SLS-203
Test Date: 09:25:00 - 09:35:00 UTC

Test 1: Scheduled Task Persistence
- Method: schtasks.exe /Create
- Detection: DETECTED (alert generated)
- Blocking: NOT BLOCKED (task created successfully)
- Visibility: HIGH (appears in task scheduler, easily discovered)
- Reliability: MEDIUM (can be removed by admin)
- Recommendation: Works but highly visible

Test 2: Registry Run Key Persistence
- Method: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
- Detection: DETECTED (alert generated)
- Blocking: NOT BLOCKED (registry modified successfully)
- Visibility: LOW (hidden in registry, less obvious)
- Reliability: HIGH (survives reboots, less likely to be removed)
- Recommendation: Best option - lower visibility, higher reliability

Test 3: Service Creation Persistence
- Method: sc.exe create WindowsUpdateService
- Detection: DETECTED
- Blocking: BLOCKED (service creation failed)
- Visibility: N/A (blocked)
- Reliability: N/A (blocked)
- Recommendation: Not viable - actively blocked by Defender

Conclusion: Registry Run Key offers best balance of success rate, low visibility, and reliability."""
    
    with open(ARTIFACTS_DIR / "persistence_test_results_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: persistence_test_results_phase2.txt")


def create_phase3_artifacts():
    """Phase 3: Privilege Escalation - FS-01 vs APP-02"""
    
    # Blue Team: Vulnerability Scan Results
    content = """Microsoft Defender Vulnerability Management Report
Scan Date: 2024-01-15 10:00:00 UTC

File Server FS-01:
- OS: Windows Server 2019 (Build 17763.5570)
- Patch Status: FULLY PATCHED
- Last Security Update: 2 days ago
- Critical Vulnerabilities: 0
- High Vulnerabilities: 0
- Medium Vulnerabilities: 2 (non-exploitable)
- Local Privilege Escalation (LPE) Vulnerabilities: 0
- Exploit Availability: None known
- Security Posture: EXCELLENT

Application Server APP-02:
- OS: Windows Server 2019 (Build 17763.5122)
- Patch Status: PARTIALLY PATCHED
- Last Security Update: 45 days ago
- Critical Vulnerabilities: 1 (CVE-2024-XXXXX - Local Privilege Escalation)
- High Vulnerabilities: 2
- Medium Vulnerabilities: 5
- Local Privilege Escalation (LPE) Vulnerabilities: 1 (unpatched)
- Exploit Availability: Public exploit available
- Security Posture: POOR

Risk Assessment:
- FS-01: Low Risk - Fully patched, no known exploits
- APP-02: High Risk - Unpatched LPE vulnerability with public exploit

Recommendation: Prioritize patching APP-02 immediately. FS-01 is secure."""
    
    with open(ARTIFACTS_DIR / "vulnerability_scan_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: vulnerability_scan_phase3.txt")
    
    # Blue Team: Sentinel Vulnerability Correlation
    content = """Microsoft Sentinel - Vulnerability Correlation Analysis
Incident ID: INC-2024-00301
Time: 10:15:00 UTC

Correlation Findings:
1. File Server FS-01
   - Vulnerability Status: No critical vulnerabilities
   - Patch Level: Current
   - Exploit Activity: None detected
   - Privilege Escalation Risk: LOW
   - Recommendation: Monitor but low priority

2. Application Server APP-02
   - Vulnerability Status: CVE-2024-XXXXX (LPE) unpatched
   - Patch Level: 45 days behind
   - Exploit Activity: Suspicious process behavior detected
   - Privilege Escalation Risk: HIGH
   - Recommendation: Immediate containment required

Threat Intelligence:
- CVE-2024-XXXXX has public exploit available
- Known to be used in ransomware campaigns
- Allows standard user to gain SYSTEM privileges

Recommendation: APP-02 is at high risk for privilege escalation. FS-01 is secure."""
    
    with open(ARTIFACTS_DIR / "sentinel_vuln_correlation_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: sentinel_vuln_correlation_phase3.txt")
    
    # Red Team: Host Reconnaissance
    content = """Host Reconnaissance Report - File Server FS-01
Target: FS-01
IP: 192.168.10.15
OS: Windows Server 2019 (Build 17763.5570)

System Information:
- Patch Level: Fully patched (latest)
- Local Privilege Escalation Vulnerabilities: None found
- Exploit Availability: None
- Security Controls: Strong (fully updated)
- Privilege Escalation Difficulty: VERY HIGH

Assessment: FS-01 is fully patched with no known LPE vulnerabilities. Privilege escalation would require zero-day exploit or credential theft. High risk of detection, low probability of success."""
    
    with open(ARTIFACTS_DIR / "fs01_recon_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: fs01_recon_phase3.txt")
    
    # Red Team: Host Reconnaissance
    content = """Host Reconnaissance Report - Application Server APP-02
Target: APP-02
IP: 192.168.10.28
OS: Windows Server 2019 (Build 17763.5122)

System Information:
- Patch Level: Partially patched (45 days behind)
- Local Privilege Escalation Vulnerabilities: CVE-2024-XXXXX (unpatched)
- Exploit Availability: Public exploit available (tested and working)
- Security Controls: Weak (outdated patches)
- Privilege Escalation Difficulty: LOW

Exploit Details:
- CVE-2024-XXXXX: Local Privilege Escalation
- Exploit Type: Kernel-level vulnerability
- Success Rate: High (90%+ in testing)
- Detection Risk: Medium (some EDR detection possible)

Assessment: APP-02 has unpatched LPE vulnerability with working exploit. High probability of successful privilege escalation with moderate detection risk. Recommended target."""
    
    with open(ARTIFACTS_DIR / "app02_recon_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: app02_recon_phase3.txt")


def create_phase4_artifacts():
    """Phase 4: Lateral Movement - Database Server Selection"""
    
    # Blue Team: Access Log Analysis
    content = """Microsoft Sentinel - Database Access Log Analysis
Time Range: 10:30:00 - 11:00:00 UTC

Database Server: DB-CUST-01 (Customer Database)
- Access Attempts: 3 failed, 0 successful
- Authentication Method: SQL Authentication
- Network Path: Requires VPN + Database Gateway
- Access Control: STRICT (role-based access control)
- Network Segmentation: Isolated database VLAN
- DLP Protection: Enabled (customer PII)
- Risk Level: LOW (access blocked, strong controls)

Database Server: DB-FIN-02 (Financial Records)
- Access Attempts: 8 failed, 2 successful (read-only)
- Authentication Method: Windows Authentication
- Network Path: Direct from application servers
- Access Control: MODERATE (some users have read access)
- Network Segmentation: Standard VLAN (less isolated)
- DLP Protection: Enabled but less restrictive
- Risk Level: HIGH (some access successful, weaker controls)

Analysis:
- DB-CUST-01: Strong security, access blocked, isolated
- DB-FIN-02: Weaker security, some access successful, less isolated

Recommendation: DB-FIN-02 shows signs of potential compromise. DB-CUST-01 is secure."""
    
    with open(ARTIFACTS_DIR / "database_access_logs_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: database_access_logs_phase4.txt")
    
    # Blue Team: Network Segmentation Analysis
    content = """Network Segmentation and Access Analysis

Database Server DB-CUST-01:
- Network Segment: Isolated Database VLAN (VLAN 50)
- Access Requirements: VPN + Database Gateway + MFA
- Firewall Rules: Restrictive (only specific IPs)
- Network Path Complexity: HIGH (multiple hops, gateways)
- Lateral Movement Difficulty: VERY HIGH
- Recommendation: Well-protected, low risk

Database Server DB-FIN-02:
- Network Segment: Standard Application VLAN (VLAN 20)
- Access Requirements: Windows Authentication (from domain)
- Firewall Rules: Moderate (allows application server access)
- Network Path Complexity: LOW (direct from application servers)
- Lateral Movement Difficulty: MEDIUM
- Recommendation: Less protected, higher risk

Conclusion: DB-FIN-02 is more accessible and has weaker network segmentation."""
    
    with open(ARTIFACTS_DIR / "network_segmentation_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: network_segmentation_phase4.txt")
    
    # Red Team: Network Mapping
    content = """Network Mapping and Access Test Results

Target 1: DB-CUST-01 (Customer Database)
- IP: 192.168.50.10
- Network Path: Requires VPN (not accessible from current position)
- Access Tests: All failed (blocked by firewall/gateway)
- Authentication: SQL Auth required (credentials not available)
- Network Isolation: HIGH (isolated VLAN)
- Access Difficulty: VERY HIGH
- Recommendation: Not accessible from current position

Target 2: DB-FIN-02 (Financial Records)
- IP: 192.168.20.45
- Network Path: Direct from APP-02 (accessible)
- Access Tests: 2 successful (read-only access obtained)
- Authentication: Windows Auth (domain credentials work)
- Network Isolation: MEDIUM (standard VLAN)
- Access Difficulty: MEDIUM
- Recommendation: Accessible and partially compromised

Conclusion: DB-FIN-02 is the viable target. DB-CUST-01 is not accessible."""
    
    with open(ARTIFACTS_DIR / "network_mapping_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: network_mapping_phase4.txt")


def create_phase5_artifacts():
    """Phase 5: Data Exfiltration Method Selection"""
    
    # Blue Team: DLP Alert Analysis
    content = """Microsoft Purview Data Loss Prevention (DLP) Alert Analysis
Time: 11:30:00 - 12:00:00 UTC

HTTPS Exfiltration Detection:
- Detection Method: Network traffic analysis + content inspection
- Detection Capability: HIGH (inspects encrypted traffic via SSL inspection)
- Alert Threshold: 10MB+ transfers to external domains
- False Positive Rate: LOW
- Detection Time: Real-time
- Blocking Capability: YES (can block HTTPS transfers)
- Status: ACTIVE and EFFECTIVE

DNS Tunneling Detection:
- Detection Method: DNS query pattern analysis
- Detection Capability: MEDIUM (pattern-based, some false positives)
- Alert Threshold: Unusual DNS query patterns
- False Positive Rate: MEDIUM (legitimate DNS can trigger)
- Detection Time: Near real-time (5-10 minute delay)
- Blocking Capability: PARTIAL (can block suspicious domains)
- Status: ACTIVE but LESS EFFECTIVE

Recommendation: HTTPS exfiltration is well-monitored. DNS tunneling has detection gaps."""
    
    with open(ARTIFACTS_DIR / "dlp_alert_analysis_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: dlp_alert_analysis_phase5.txt")
    
    # Blue Team: Network Bandwidth Analysis
    content = """Network Bandwidth and Traffic Analysis
Time: 11:30:00 - 12:00:00 UTC

HTTPS Traffic:
- Baseline: 50-100 MB/hour (normal)
- Current: 250 MB in 30 minutes (anomalous)
- Detection: FLAGGED by DLP
- Pattern: Large file transfers to external IP
- Visibility: HIGH (traffic inspected)
- Recommendation: Monitor and potentially block

DNS Traffic:
- Baseline: 100-200 queries/hour (normal)
- Current: 5000 queries in 30 minutes (anomalous)
- Detection: FLAGGED by DNS monitoring
- Pattern: Unusual query patterns, large payloads
- Visibility: MEDIUM (pattern-based detection)
- Recommendation: Investigate but may be false positive

Analysis: Both methods show anomalies, but HTTPS is more clearly malicious."""
    
    with open(ARTIFACTS_DIR / "bandwidth_analysis_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: bandwidth_analysis_phase5.txt")
    
    # Red Team: Exfiltration Test Results
    content = """Data Exfiltration Method Testing Results
Test Date: 11:30:00 - 12:00:00 UTC

Method 1: HTTPS Encrypted Tunnel
- Speed: 5-10 MB/minute (slower)
- Detection: DETECTED by DLP (traffic inspected)
- Blocking: Can be blocked by DLP policies
- Visibility: HIGH (traffic volume visible)
- Reliability: MEDIUM (may be blocked)
- Recommendation: Higher detection risk

Method 2: DNS Tunneling
- Speed: 1-2 MB/minute (slower but steady)
- Detection: PARTIALLY DETECTED (pattern-based, some false positives)
- Blocking: PARTIAL (can block suspicious domains but not all)
- Visibility: MEDIUM (blends with normal DNS)
- Reliability: HIGH (less likely to be fully blocked)
- Recommendation: Lower detection risk, more reliable

Conclusion: DNS tunneling offers better stealth and reliability despite slower speed."""
    
    with open(ARTIFACTS_DIR / "exfiltration_test_results_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: exfiltration_test_results_phase5.txt")


def main():
    """Generate all artifact files"""
    print("Generating artifact files for new Ransomware scenario...")
    print("=" * 60)
    
    create_phase1_artifacts()
    print()
    create_phase2_artifacts()
    print()
    create_phase3_artifacts()
    print()
    create_phase4_artifacts()
    print()
    create_phase5_artifacts()
    print()
    
    print("=" * 60)
    print("✓ All artifact files generated successfully!")


if __name__ == "__main__":
    main()

