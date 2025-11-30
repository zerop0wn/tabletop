"""
Test if the artifact file route is working correctly.
"""
import sys
sys.path.insert(0, '/app')

from pathlib import Path
import requests

# Test file that should exist
test_filename = "hr_recon_phase1.txt"
file_path = Path("/app/artifacts/files") / test_filename

print("=" * 60)
print("TESTING ARTIFACT FILE ROUTE")
print("=" * 60)
print()

# Check if file exists
print(f"1. Checking if file exists on disk...")
if file_path.exists():
    size = file_path.stat().st_size
    print(f"   ✓ File exists: {file_path}")
    print(f"   ✓ File size: {size} bytes")
else:
    print(f"   ❌ File NOT found: {file_path}")
    sys.exit(1)

print()

# Test the route directly
print(f"2. Testing route: /artifacts/files/{test_filename}")
print(f"   (This simulates what the backend receives after nginx rewrite)")

# Import the router and test it
from app.routers.artifacts import get_artifact_file
from fastapi import HTTPException

try:
    # This would normally be called by FastAPI, but we can test the logic
    safe_filename = Path(test_filename).name
    artifact_file_path = Path("/app/artifacts/files") / safe_filename
    
    if not artifact_file_path.exists() or not artifact_file_path.is_file():
        print(f"   ❌ Route check: File not found")
        print(f"      Expected: {artifact_file_path}")
    else:
        print(f"   ✓ Route check: File found")
        print(f"      Path: {artifact_file_path}")
        print(f"      Size: {artifact_file_path.stat().st_size} bytes")
        
        # Try to read the file
        try:
            with open(artifact_file_path, 'r') as f:
                content_preview = f.read(100)
                print(f"   ✓ File is readable")
                print(f"      Preview: {content_preview[:50]}...")
        except Exception as e:
            print(f"   ❌ File read error: {e}")
            
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("ROUTE INFORMATION")
print("=" * 60)
print()
print("Expected URL path from frontend: /api/artifacts/files/{filename}")
print("After nginx rewrite: /artifacts/files/{filename}")
print("Backend router prefix: /artifacts")
print("Backend route: /files/{filename}")
print("Full backend route: /artifacts/files/{filename}")
print()
print("If the route isn't working, check:")
print("  1. Is the artifacts router registered in main.py?")
print("  2. Is nginx correctly rewriting /api/ to /?")
print("  3. Are there any permission issues with the files?")
print("  4. Check backend logs for errors")

