#!/usr/bin/env python3
"""
Create placeholder artifact files for the scenario.
Run this after seeding the database to create the actual files.
"""
import os
from pathlib import Path

# Create artifacts directory
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

# List of artifact files referenced in seed_data.py
ARTIFACT_FILES = [
    "phishing_email_phase1.png",
    "edr_alert_phase1.txt",
    "nmap_scan_phase2.txt",
    "c2_traffic_phase2.txt",
    "privilege_escalation_phase3.txt",
    "lateral_movement_phase3.txt",
    "exfiltration_traffic_phase4.txt",
    "data_classification_phase4.pdf",
    "ransomware_note_phase5.png",
    "impact_assessment_phase5.pdf",
    "backup_status_phase5.txt",
]

def create_placeholder_image(filename: str):
    """Create a simple placeholder - for now just create a text file that won't 404."""
    # Create a simple text placeholder (won't display as image but prevents 404)
    with open(ARTIFACTS_DIR / filename, 'w') as f:
        f.write(f"Placeholder for {filename}\n")
        f.write("This is a placeholder file. Replace with actual image file.\n")
        f.write("To create actual images, you can:\n")
        f.write("1. Take screenshots and save them with this filename\n")
        f.write("2. Use image editing software to create realistic artifacts\n")
        f.write("3. Upload via the API: POST /api/artifacts/upload\n")
    print(f"Created placeholder file: {filename} (replace with actual image)")

def create_placeholder_text(filename: str, content: str = None):
    """Create a placeholder text file."""
    if content is None:
        content = f"Placeholder content for {filename}\n\n"
        content += "This is a placeholder file. Replace with actual content.\n"
    
    with open(ARTIFACTS_DIR / filename, 'w') as f:
        f.write(content)
    print(f"Created placeholder text file: {filename}")

def create_placeholder_pdf(filename: str):
    """Create a placeholder PDF file."""
    # Create a simple text placeholder (won't display as PDF but prevents 404)
    with open(ARTIFACTS_DIR / filename, 'w') as f:
        f.write(f"Placeholder for {filename}\n")
        f.write("This is a placeholder file. Replace with actual PDF.\n")
        f.write("To create actual PDFs, you can:\n")
        f.write("1. Create PDFs using any PDF creation tool\n")
        f.write("2. Save them with this filename in the artifacts directory\n")
        f.write("3. Upload via the API: POST /api/artifacts/upload\n")
    print(f"Created placeholder file: {filename} (replace with actual PDF)")

if __name__ == "__main__":
    print("Creating placeholder artifact files...")
    print(f"Artifacts directory: {ARTIFACTS_DIR}")
    
    # Create placeholder files
    for filename in ARTIFACT_FILES:
        filepath = ARTIFACTS_DIR / filename
        if filepath.exists():
            print(f"Skipping {filename} (already exists)")
            continue
        
        if filename.endswith('.png'):
            create_placeholder_image(filename)
        elif filename.endswith('.txt'):
            # Create specific content for text files
            if 'siem' in filename.lower():
                content = """[2024-01-15 10:23:45] WARNING: Suspicious PowerShell execution detected
[2024-01-15 10:23:46] INFO: Process tree: powershell.exe -> cmd.exe -> whoami.exe
[2024-01-15 10:23:47] ALERT: Encoded command detected in process arguments
[2024-01-15 10:23:48] WARNING: Network connection to external IP: 192.0.2.100:443
"""
            elif 'nmap' in filename.lower():
                content = """Starting Nmap 7.94 scan
Scanning 192.168.0.0/24
Discovered hosts:
192.168.0.10 - Windows Server 2019 (DC-01)
192.168.0.20 - Windows Server 2019 (FS-01)
192.168.0.21 - Windows Server 2019 (FS-02)
192.168.0.30 - Windows Server 2019 (BACKUP-01)

Open ports on 192.168.0.10 (DC-01):
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
389/tcp  open  ldap
445/tcp  open  microsoft-ds
636/tcp  open  ldapssl
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
3389/tcp open  ms-wbt-server
5985/tcp open  wsman

Open ports on 192.168.0.20 (FS-01):
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5985/tcp open  wsman

Open ports on 192.168.0.21 (FS-02):
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5985/tcp open  wsman
"""
            elif 'c2' in filename.lower() or 'traffic' in filename.lower():
                content = """Network Traffic Analysis Report
================================

Source IP: 192.168.0.42 (WS-FIN-042)
Destination IP: 185.220.101.45
Protocol: TCP/443 (HTTPS)
Duration: 6 hours
Total Bytes: ~450 GB

Connection Pattern:
- Initial connection: 10:23:45 UTC
- Beacon interval: Every 300 seconds
- Data transfer: Burst pattern, 75 GB/hour
- Connection maintained: Persistent

DNS Queries:
- update-check.tk -> 185.220.101.45
- secure-invoice-download.tk -> 45.146.164.110

Traffic Characteristics:
- Encrypted (TLS 1.3)
- Unusual payload sizes
- Long-lived connections
- Periodic small transfers (beaconing)
"""
            elif 'privilege' in filename.lower():
                content = """Windows Security Event Log
==========================

Event ID: 4624 - Successful Logon
Time: 2024-01-15 10:45:23 UTC
Account: DOMAIN\\svc_backup
Source: WS-FIN-042 (192.168.0.42)
Target: DC-01 (192.168.0.10)
Logon Type: 3 (Network)
Authentication: NTLM

Event ID: 4672 - Special Privileges Assigned
Time: 2024-01-15 10:45:24 UTC
Account: DOMAIN\\svc_backup
Privileges: SeBackupPrivilege, SeRestorePrivilege, SeDebugPrivilege

Event ID: 5145 - Network Share Accessed
Time: 2024-01-15 10:45:25 UTC
Account: DOMAIN\\svc_backup
Share: \\\\DC-01\\SYSVOL
Access: Read, Write

Note: Credentials appear to have been harvested from memory dump.
"""
            elif 'lateral' in filename.lower():
                content = """SIEM Correlation Alert: Lateral Movement
=========================================

Time Range: 2024-01-15 10:45:00 - 11:30:00 UTC
Source: WS-FIN-042 (192.168.0.42)
Technique: Pass-the-Hash

Target Systems:
1. FS-01 (192.168.0.20)
   - Authentication: 10:46:12 UTC
   - Shares Accessed: \\FS-01\\Finance
   - Files Enumerated: 1,234 files

2. FS-02 (192.168.0.21)
   - Authentication: 10:52:33 UTC
   - Shares Accessed: \\FS-02\\HR\\PII
   - Files Enumerated: 856 files

3. BACKUP-01 (192.168.0.30)
   - Authentication: 11:15:47 UTC
   - Shares Accessed: \\BACKUP-01\\Backups
   - Files Enumerated: 2,109 files

Sensitive Directories Accessed:
- \\FS-01\\Finance\\Q4_Financials.xlsx
- \\FS-02\\HR\\PII\\Employee_Records.db
- \\FS-01\\R&D\\Proprietary\\Algorithm_Source.zip
"""
            elif 'exfiltration' in filename.lower():
                content = """Network Flow Analysis: Data Exfiltration
========================================

Time Range: 2024-01-15 11:00:00 - 17:00:00 UTC
Source Systems: FS-01, FS-02
Destination IPs: 185.220.101.45, 45.146.164.110
Protocol: TCP/443 (HTTPS)
Total Data: ~450 GB

Transfer Breakdown:
- 11:00-13:00: 150 GB (FS-01 -> 185.220.101.45)
- 13:00-15:00: 180 GB (FS-02 -> 45.146.164.110)
- 15:00-17:00: 120 GB (FS-01 -> 185.220.101.45)

File Types Detected:
- .db files: 45 GB
- .xlsx files: 120 GB
- .pdf files: 85 GB
- .docx files: 95 GB
- .zip files: 105 GB

Transfer Rate: ~75 GB/hour
Method: Cloud storage APIs (Mega.nz, Dropbox)
"""
            elif 'backup' in filename.lower():
                content = """Backup System Status Report
============================

BACKUP-01 (Onsite):
- Status: ENCRYPTED
- Last Backup: 2024-01-15 08:00:00 UTC
- Encryption Time: 2024-01-15 10:00:00 UTC
- Recovery: Not possible (encrypted)

Offsite Backup Location:
- Status: INTACT
- Last Successful Backup: 2024-01-14 20:00:00 UTC
- Backup Coverage: 95% of critical systems, 80% of user data
- Location: Secure offsite facility

Recovery Metrics:
- RPO (Recovery Point Objective): 36 hours
- RTO (Recovery Time Objective): 48 hours
- Data Loss Window: 36 hours maximum

Backup Contents:
- Critical Systems: 15 file servers, 8 app servers
- User Data: 80% coverage
- Database Backups: All critical databases
- Configuration: All system configs
"""
            else:
                content = None
            create_placeholder_text(filename, content)
        elif filename.endswith('.pdf'):
            create_placeholder_pdf(filename)
        else:
            # Generic placeholder
            with open(filepath, 'w') as f:
                f.write(f"Placeholder for {filename}\n")
            print(f"Created placeholder file: {filename}")
    
    print(f"\nDone! Created placeholder files in {ARTIFACTS_DIR}")
    print("You can replace these with actual artifact files later.")

