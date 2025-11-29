#!/bin/bash
# Script to create the new artifact-driven Ransomware scenario

set -e

echo "Creating New Ransomware Scenario"
echo "=================================="
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

echo ""
echo "✓ Artifact files generated"
echo ""

# Step 2: Create scenario in database
echo "Step 2: Creating scenario in database..."
docker cp backend/create_new_ransomware_scenario.py "$BACKEND_CONTAINER:/app/create_new_ransomware_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/create_new_ransomware_scenario.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ New Ransomware scenario created successfully!"
    echo ""
    echo "Scenario: 'Ransomware Attack: Advanced Persistent Threat'"
    echo "Phases: 5"
    echo "Artifacts: 10"
    echo ""
    echo "You can now create a new game using this scenario."
else
    echo ""
    echo "❌ Failed to create scenario"
    exit 1
fi

