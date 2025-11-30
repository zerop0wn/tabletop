"""
Test artifact file access directly.
"""
import sys
sys.path.insert(0, '/app')

from pathlib import Path

ARTIFACTS_DIR = Path("/app/artifacts/files")

# Test files
test_files = [
    "c2_status_phase1.txt",  # This one works
    "hr_recon_phase1.txt",   # This one doesn't
    "ops_recon_phase1.txt",  # This one doesn't
]

print("=" * 60)
print("TESTING ARTIFACT FILE ACCESS")
print("=" * 60)
print()

for filename in test_files:
    file_path = ARTIFACTS_DIR / filename
    print(f"Testing: {filename}")
    print(f"  Path: {file_path}")
    print(f"  Exists: {file_path.exists()}")
    if file_path.exists():
        print(f"  Is file: {file_path.is_file()}")
        print(f"  Size: {file_path.stat().st_size} bytes")
        # Try to read first line
        try:
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                print(f"  First line: {first_line[:50]}...")
        except Exception as e:
            print(f"  Read error: {e}")
    else:
        # Check if directory exists
        print(f"  ARTIFACTS_DIR exists: {ARTIFACTS_DIR.exists()}")
        if ARTIFACTS_DIR.exists():
            # List files
            files = list(ARTIFACTS_DIR.glob("*.txt"))
            similar = [f.name for f in files if filename.lower() in f.name.lower() or f.name.lower() in filename.lower()]
            print(f"  Similar files: {similar[:5]}")
    print()

