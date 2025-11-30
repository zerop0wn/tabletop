#!/bin/bash
# Script to create the AI Application Data Leakage & Permission Misconfiguration scenario
# Usage: ./scripts/create-ai-app-scenario.sh

set -e

echo "=========================================="
echo "Creating AI Application Security Scenario"
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

# Step 1: Copy artifact generation script
echo "Step 1: Copying artifact generation script..."
docker cp backend/generate_ai_app_artifacts.py "$BACKEND_CONTAINER:/app/generate_ai_app_artifacts.py"

if [ $? -ne 0 ]; then
    echo "❌ Error copying artifact generation script"
    exit 1
fi

echo "✓ Artifact generation script copied"
echo ""

# Step 2: Copy scenario creation script and create scenario
echo "Step 2: Creating scenario in database..."
docker cp backend/create_ai_app_scenario.py "$BACKEND_CONTAINER:/app/create_ai_app_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/create_ai_app_scenario.py

if [ $? -ne 0 ]; then
    echo "❌ Error creating scenario"
    exit 1
fi

echo ""
echo "✅ Successfully created AI Application Data Leakage & Permission Misconfiguration scenario!"
echo ""
echo "Scenario: 'AI Application Data Leakage & Permission Misconfiguration'"
echo "- 5 phases with artifact-driven decisions"
echo "- Phase 1: Initial Detection - Suspicious AI API Activity"
echo "- Phase 2: Investigation - Unauthorized Document Access"
echo "- Phase 3: Containment - Data Leakage Confirmed"
echo "- Phase 4: Remediation - Permission Fixes & Access Review"
echo "- Phase 5: Post-Incident - Security Improvements"
echo "- Realistic AI API logs, access control audits, and permission misconfiguration reports for Blue Team"
echo "- Realistic Red Team reconnaissance, exploitation, and prompt injection tool outputs"
echo "- Intermediate-Advanced difficulty level"
echo ""
echo "You can now create a game using this scenario from the GM console."

