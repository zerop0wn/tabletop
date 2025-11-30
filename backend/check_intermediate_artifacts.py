"""
Check if intermediate ransomware artifact files exist and verify their locations.
"""
import sys
sys.path.insert(0, '/app')

from pathlib import Path

ARTIFACTS_DIR = Path("/app/artifacts/files")

# Expected files for intermediate ransomware scenario
expected_files = [
    # Phase 1
    "defender_hr_alert_phase1.txt",
    "defender_ops_alert_phase1.txt",
    "sentinel_phishing_phase1.txt",
    "hr_recon_phase1.txt",
    "ops_recon_phase1.txt",
    "c2_status_phase1.txt",
    # Phase 2
    "persistence_testing_phase2.txt",
    "detection_risk_phase2.txt",
    "defender_process_phase2.txt",
    "system_audit_phase2.txt",
    # Phase 3
    "fs_prod_recon_phase3.txt",
    "app_dev_recon_phase3.txt",
    "vuln_scan_phase3.txt",
    "sentinel_vuln_phase3.txt",
    # Phase 4
    "network_mapping_phase4.txt",
    "access_test_phase4.txt",
    "db_access_logs_phase4.txt",
    "network_seg_phase4.txt",
    # Phase 5
    "exfil_testing_phase5.txt",
    "data_transfer_phase5.txt",
    "dlp_analysis_phase5.txt",
    "bandwidth_analysis_phase5.txt",
]

print("=" * 60)
print("CHECKING INTERMEDIATE RANSOMWARE ARTIFACTS")
print("=" * 60)
print()

# Check if directory exists
if not ARTIFACTS_DIR.exists():
    print(f"❌ Artifacts directory does not exist: {ARTIFACTS_DIR}")
    print(f"   Creating directory...")
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"   ✓ Directory created")
else:
    print(f"✓ Artifacts directory exists: {ARTIFACTS_DIR}")

print()

# Check each expected file
missing_files = []
existing_files = []

for filename in expected_files:
    file_path = ARTIFACTS_DIR / filename
    if file_path.exists() and file_path.is_file():
        size = file_path.stat().st_size
        existing_files.append(filename)
        print(f"✓ {filename} ({size} bytes)")
    else:
        missing_files.append(filename)
        print(f"❌ {filename} - NOT FOUND")

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total expected files: {len(expected_files)}")
print(f"Files found: {len(existing_files)}")
print(f"Files missing: {len(missing_files)}")

if missing_files:
    print()
    print("MISSING FILES:")
    for filename in missing_files:
        print(f"  - {filename}")
    print()
    print("Run the artifact generation script to create these files:")
    print("  sudo ./scripts/regenerate-intermediate-artifacts.sh")
else:
    print()
    print("✅ All artifact files are present!")

print()

# List all .txt files in the directory
all_txt_files = list(ARTIFACTS_DIR.glob("*.txt"))
print(f"All .txt files in {ARTIFACTS_DIR}: {len(all_txt_files)}")
if all_txt_files:
    print("Files found:")
    for f in sorted(all_txt_files):
        print(f"  - {f.name}")

