"""
Verify artifact file creation and list actual file locations.
"""
import sys
from pathlib import Path

# Test the same path the generation script uses
ARTIFACTS_DIR = Path("/app/artifacts/files")

print("=" * 60)
print("VERIFYING ARTIFACT FILE CREATION")
print("=" * 60)
print()

# Check directory
print(f"ARTIFACTS_DIR: {ARTIFACTS_DIR}")
print(f"  Exists: {ARTIFACTS_DIR.exists()}")
print(f"  Is directory: {ARTIFACTS_DIR.is_dir() if ARTIFACTS_DIR.exists() else 'N/A'}")
print()

# Try to create directory
try:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Directory created/verified")
except Exception as e:
    print(f"✗ Error creating directory: {e}")
print()

# List all files in directory
if ARTIFACTS_DIR.exists():
    try:
        all_items = list(ARTIFACTS_DIR.iterdir())
        files = [f for f in all_items if f.is_file()]
        dirs = [d for d in all_items if d.is_dir()]
        
        print(f"Directory contents:")
        print(f"  Files: {len(files)}")
        print(f"  Directories: {len(dirs)}")
        print()
        
        if files:
            print("Files found:")
            for f in sorted(files):
                size = f.stat().st_size
                print(f"  ✓ {f.name} ({size} bytes)")
        else:
            print("  No files found in directory")
        
        if dirs:
            print("\nSubdirectories found:")
            for d in sorted(dirs):
                print(f"  📁 {d.name}")
        
    except Exception as e:
        print(f"✗ Error listing directory: {e}")
else:
    print("✗ Directory does not exist")

print()
print("=" * 60)

# Try to create a test file
test_file = ARTIFACTS_DIR / "test_file.txt"
try:
    with open(test_file, 'w') as f:
        f.write("Test content")
    print(f"✓ Test file created: {test_file}")
    
    # Verify it exists
    if test_file.exists():
        print(f"✓ Test file verified: {test_file.exists()}, size: {test_file.stat().st_size} bytes")
    else:
        print(f"✗ Test file not found after creation!")
        
    # Try to read it back
    with open(test_file, 'r') as f:
        content = f.read()
        print(f"✓ Test file readable: {len(content)} characters")
        
except Exception as e:
    print(f"✗ Error creating test file: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)

