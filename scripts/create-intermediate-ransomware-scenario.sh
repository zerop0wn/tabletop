#!/bin/bash
# Script to create the intermediate ransomware scenario and generate artifacts
# Usage: ./scripts/create-intermediate-ransomware-scenario.sh

set -e

echo "=========================================="
echo "Creating Intermediate Ransomware Scenario"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.dev.yml" ] && [ ! -f "docker-compose.prod.yml" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Determine which docker-compose file to use and get backend container
if [ -f "docker-compose.prod.yml" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    ENV_FILE="--env-file .env.production"
    BACKEND_CONTAINER=$(docker-compose $ENV_FILE -f "$COMPOSE_FILE" ps -q backend)
else
    COMPOSE_FILE="docker-compose.dev.yml"
    ENV_FILE=""
    BACKEND_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q backend)
fi

# Check if backend container is running
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container is not running!"
    exit 1
fi

echo "✓ Backend container is running"
echo ""

# Step 1: Copy artifact generation script and generate artifacts
echo "Step 1: Generating artifact files..."
docker cp backend/generate_intermediate_ransomware_artifacts.py "$BACKEND_CONTAINER:/app/generate_intermediate_ransomware_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/generate_intermediate_ransomware_artifacts.py

if [ $? -ne 0 ]; then
    echo "❌ Error generating artifacts"
    exit 1
fi

echo ""
echo "✓ Artifact files generated"
echo ""

# Step 2: Copy scenario creation script and create scenario
echo "Step 2: Creating scenario in database..."
docker cp backend/create_intermediate_ransomware_scenario.py "$BACKEND_CONTAINER:/app/create_intermediate_ransomware_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/create_intermediate_ransomware_scenario.py

if [ $? -ne 0 ]; then
    echo "❌ Error creating scenario"
    exit 1
fi

echo ""
echo "✅ Successfully created intermediate ransomware scenario!"
echo ""
echo "Scenario: 'Ransomware Attack: Corporate Network Compromise'"
echo "- 5 phases with artifact-driven decisions"
echo "- Detailed Defender/E5 security tool artifacts for Blue Team"
echo "- Realistic Red Team reconnaissance and tool outputs"
echo "- Intermediate difficulty level"
echo ""
echo "You can now create a game using this scenario from the GM console."

