#!/bin/bash
# Script to fix missing artifacts - regenerates files and verifies links

set -e

echo "Fixing Missing Artifacts"
echo "========================"
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    exit 1
fi

# Check if backend container is running
BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container is not running!"
    exit 1
fi

echo "✓ Backend container is running"
echo ""

# Step 1: Generate artifact files
echo "Step 1: Generating artifact files..."
docker cp backend/generate_new_ransomware_artifacts.py "$BACKEND_CONTAINER:/app/generate_new_ransomware_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/generate_new_ransomware_artifacts.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate artifact files"
    exit 1
fi

echo "✓ Artifact files generated"
echo ""

# Step 2: Run diagnostic
echo "Step 2: Running diagnostic..."
docker cp backend/diagnose_artifacts.py "$BACKEND_CONTAINER:/app/diagnose_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/diagnose_artifacts.py

echo ""
echo "======================================"
echo "If artifacts are still missing, the scenario may need to be recreated."
echo "Run: sudo ./scripts/create-new-ransomware-scenario.sh"
echo ""

