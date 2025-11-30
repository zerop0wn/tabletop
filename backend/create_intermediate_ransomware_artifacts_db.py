"""
Create intermediate ransomware artifacts directly in the database with content.
This replaces the file-based approach with database storage.
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Artifact, ArtifactType
from backend.generate_intermediate_ransomware_artifacts import (
    create_phase1_artifacts,
    create_phase2_artifacts,
    create_phase3_artifacts,
    create_phase4_artifacts,
    create_phase5_artifacts,
)
import io
from contextlib import redirect_stdout

db: Session = SessionLocal()

# Artifact definitions with their content generation functions
ARTIFACT_DEFINITIONS = [
    # Phase 1
    {
        "name": "Defender Alert - HR Department",
        "type": ArtifactType.LOG_SNIPPET,
        "description": "Microsoft Defender for Endpoint alert for WS-HR-042 (HR Department). Contains detection details, EDR status, and response actions.",
        "filename": "defender_hr_alert_phase1.txt",
        "phase": 1,
    },
    {
        "name": "Defender Alert - Operations Department",
        "type": ArtifactType.LOG_SNIPPET,
        "description": "Microsoft Defender for Endpoint alert for WS-OPS-089 (Operations Department). Contains detection details, EDR status, and response actions.",
        "filename": "defender_ops_alert_phase1.txt",
        "phase": 1,
    },
    {
        "name": "Sentinel Phishing Analysis",
        "type": ArtifactType.INTEL_REPORT,
        "description": "Microsoft Sentinel incident analysis comparing phishing campaign impact on HR and Operations departments. Includes risk scoring and recommendations.",
        "filename": "sentinel_phishing_phase1.txt",
        "phase": 1,
    },
    {
        "name": "HR Department Reconnaissance Report",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Reconnaissance data collected on WS-HR-042 (HR Department). Contains security posture assessment, EDR status, and user privilege information.",
        "filename": "hr_recon_phase1.txt",
        "phase": 1,
    },
    {
        "name": "Operations Department Reconnaissance Report",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Reconnaissance data collected on WS-OPS-089 (Operations Department). Contains security posture assessment, EDR status, and user privilege information.",
        "filename": "ops_recon_phase1.txt",
        "phase": 1,
    },
    {
        "name": "C2 Connection Status Comparison",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Command and Control (C2) connection test results comparing HR and Operations workstations. Shows which target has operational C2 connectivity.",
        "filename": "c2_status_phase1.txt",
        "phase": 1,
    },
    # Phase 2
    {
        "name": "Persistence Method Testing Results",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Results from testing three persistence mechanisms: Scheduled Tasks, Registry Run Keys, and WMI Event Subscriptions. Includes reliability and detection risk assessment.",
        "filename": "persistence_testing_phase2.txt",
        "phase": 2,
    },
    {
        "name": "Detection Risk Assessment",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Assessment of detection risk for each persistence method based on security tool responses and system logging.",
        "filename": "detection_risk_phase2.txt",
        "phase": 2,
    },
    {
        "name": "Defender Process Monitoring",
        "type": ArtifactType.LOG_SNIPPET,
        "description": "Microsoft Defender for Endpoint process monitoring showing detection and blocking status for each persistence method attempt.",
        "filename": "defender_process_phase2.txt",
        "phase": 2,
    },
    {
        "name": "System Audit Logs",
        "type": ArtifactType.LOG_SNIPPET,
        "description": "Windows System audit logs showing successful modifications for each persistence method. Includes registry changes, scheduled task creation, and WMI subscription attempts.",
        "filename": "system_audit_phase2.txt",
        "phase": 2,
    },
    # Phase 3
    {
        "name": "FS-PROD-01 Reconnaissance Report",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Reconnaissance data collected on File Server FS-PROD-01. Contains vulnerability scan results, patch status, and exploit availability.",
        "filename": "fs_prod_recon_phase3.txt",
        "phase": 3,
    },
    {
        "name": "APP-DEV-02 Reconnaissance Report",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Reconnaissance data collected on Application Server APP-DEV-02. Contains vulnerability scan results, patch status, and exploit availability.",
        "filename": "app_dev_recon_phase3.txt",
        "phase": 3,
    },
    {
        "name": "Vulnerability Scan Results",
        "type": ArtifactType.INTEL_REPORT,
        "description": "Microsoft Defender Vulnerability Management scan results for FS-PROD-01 and APP-DEV-02. Includes CVE details, patch status, and risk scoring.",
        "filename": "vuln_scan_phase3.txt",
        "phase": 3,
    },
    {
        "name": "Sentinel Vulnerability Correlation",
        "type": ArtifactType.INTEL_REPORT,
        "description": "Microsoft Sentinel correlation of vulnerability data with exploit activity. Shows which server has active exploit attempts.",
        "filename": "sentinel_vuln_phase3.txt",
        "phase": 3,
    },
    # Phase 4
    {
        "name": "Network Mapping Results",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Network mapping and connectivity test results for DB-CUST-PROD and DB-HR-PROD. Shows network segmentation and access paths.",
        "filename": "network_mapping_phase4.txt",
        "phase": 4,
    },
    {
        "name": "Database Access Test Results",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Connection test results for both databases. Shows which database accepts connections and which is blocked.",
        "filename": "access_test_phase4.txt",
        "phase": 4,
    },
    {
        "name": "Database Access Logs",
        "type": ArtifactType.LOG_SNIPPET,
        "description": "Database access logs showing connection attempts and query activity for DB-CUST-PROD and DB-HR-PROD.",
        "filename": "db_access_logs_phase4.txt",
        "phase": 4,
    },
    {
        "name": "Network Segmentation Analysis",
        "type": ArtifactType.INTEL_REPORT,
        "description": "Microsoft Defender for Cloud network segmentation analysis showing VLAN assignments and access controls for both databases.",
        "filename": "network_seg_phase4.txt",
        "phase": 4,
    },
    # Phase 5
    {
        "name": "Exfiltration Method Testing",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Testing results for HTTPS tunnel and DNS tunneling exfiltration methods. Includes speed, reliability, and detection risk assessment.",
        "filename": "exfil_testing_phase5.txt",
        "phase": 5,
    },
    {
        "name": "Data Transfer Analysis",
        "type": ArtifactType.TOOL_OUTPUT,
        "description": "Analysis of data transfer capabilities for both exfiltration methods. Includes bandwidth, reliability, and detection risk comparison.",
        "filename": "data_transfer_phase5.txt",
        "phase": 5,
    },
    {
        "name": "DLP Alert Analysis",
        "type": ArtifactType.INTEL_REPORT,
        "description": "Microsoft Purview Data Loss Prevention alert analysis comparing detection capabilities for HTTPS and DNS tunneling exfiltration methods.",
        "filename": "dlp_analysis_phase5.txt",
        "phase": 5,
    },
    {
        "name": "Network Bandwidth Analysis",
        "type": ArtifactType.LOG_SNIPPET,
        "description": "Microsoft Defender for Cloud network bandwidth analysis showing anomalies for HTTPS and DNS traffic patterns.",
        "filename": "bandwidth_analysis_phase5.txt",
        "phase": 5,
    },
]

def get_artifact_content(filename: str) -> str:
    """Get artifact content by generating it from the artifact generation script."""
    # Import the generation functions and capture their output
    from pathlib import Path
    import tempfile
    import os
    
    # Create a temporary directory to capture file writes
    with tempfile.TemporaryDirectory() as tmpdir:
        # Monkey-patch the ARTIFACTS_DIR in the generation module
        import backend.generate_intermediate_ransomware_artifacts as gen_module
        original_dir = gen_module.ARTIFACTS_DIR
        gen_module.ARTIFACTS_DIR = Path(tmpdir)
        
        try:
            # Run the appropriate generation function
            if "phase1" in filename:
                create_phase1_artifacts()
            elif "phase2" in filename:
                create_phase2_artifacts()
            elif "phase3" in filename:
                create_phase3_artifacts()
            elif "phase4" in filename:
                create_phase4_artifacts()
            elif "phase5" in filename:
                create_phase5_artifacts()
            
            # Read the generated file
            file_path = Path(tmpdir) / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"[Error: Could not generate content for {filename}]"
        finally:
            # Restore original directory
            gen_module.ARTIFACTS_DIR = original_dir

try:
    print("=" * 60)
    print("Creating Intermediate Ransomware Artifacts in Database")
    print("=" * 60)
    print()
    
    created_count = 0
    updated_count = 0
    
    for artifact_def in ARTIFACT_DEFINITIONS:
        # Check if artifact already exists
        existing = db.query(Artifact).filter(Artifact.name == artifact_def["name"]).first()
        
        if existing:
            print(f"⏭️  Artifact already exists: {artifact_def['name']}")
            # Update content if missing
            if not existing.content:
                print(f"   Updating content for: {artifact_def['name']}")
                existing.content = get_artifact_content(artifact_def["filename"])
                updated_count += 1
        else:
            print(f"📝 Creating artifact: {artifact_def['name']}")
            content = get_artifact_content(artifact_def["filename"])
            
            artifact = Artifact(
                name=artifact_def["name"],
                type=artifact_def["type"],
                description=artifact_def["description"],
                content=content,
                file_url=None,  # No file URL needed - content is in DB
            )
            db.add(artifact)
            created_count += 1
    
    db.commit()
    
    print()
    print("=" * 60)
    print("✅ Artifact Creation Complete!")
    print("=" * 60)
    print(f"Created: {created_count} artifacts")
    print(f"Updated: {updated_count} artifacts")
    print()
    print("Artifacts are now stored in the database with content.")
    print("The scenario creation script can now link to these artifacts.")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

