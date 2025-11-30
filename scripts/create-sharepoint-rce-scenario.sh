#!/bin/bash
# Script to create the SharePoint RCE Zero-Day Exploitation scenario
# Usage: ./scripts/create-sharepoint-rce-scenario.sh

set -e

echo "=========================================="
echo "Creating SharePoint RCE Scenario"
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
docker cp backend/generate_sharepoint_rce_artifacts.py "$BACKEND_CONTAINER:/app/generate_sharepoint_rce_artifacts.py"

if [ $? -ne 0 ]; then
    echo "❌ Error copying artifact generation script"
    exit 1
fi

echo "✓ Artifact generation script copied"
echo ""

# Step 2: Copy scenario creation script and create scenario
echo "Step 2: Creating scenario in database..."
docker cp backend/create_sharepoint_rce_scenario.py "$BACKEND_CONTAINER:/app/create_sharepoint_rce_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/create_sharepoint_rce_scenario.py

if [ $? -ne 0 ]; then
    echo "❌ Error creating scenario"
    exit 1
fi

echo ""
echo "✅ Successfully created SharePoint RCE Zero-Day Exploitation scenario!"
echo ""
echo "Scenario: 'SharePoint RCE Zero-Day Exploitation'"
echo "- 5 phases with artifact-driven decisions"
echo "- Phase 1: Vulnerability Disclosure & Initial Reconnaissance"
echo "- Phase 2: Exploitation Attempt & Initial Access"
echo "- Phase 3: Privilege Escalation & Persistence"
echo "- Phase 4: Data Access & Exfiltration"
echo "- Phase 5: Remediation & Post-Incident"
echo "- Detailed security advisories, WAF logs, IIS logs, and Defender alerts for Blue Team"
echo "- Realistic Red Team reconnaissance, exploitation, and tool outputs"
echo "- Intermediate-Advanced difficulty level"
echo ""
echo "You can now create a game using this scenario from the GM console."

