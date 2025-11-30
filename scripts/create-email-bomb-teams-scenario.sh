#!/bin/bash
# Script to create the Email Bomb + Teams Call scenario
# Usage: ./scripts/create-email-bomb-teams-scenario.sh

set -e

echo "=========================================="
echo "Creating Email Bomb + Teams Call Scenario"
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
docker cp backend/generate_email_bomb_teams_artifacts.py "$BACKEND_CONTAINER:/app/generate_email_bomb_teams_artifacts.py"

if [ $? -ne 0 ]; then
    echo "❌ Error copying artifact generation script"
    exit 1
fi

echo "✓ Artifact generation script copied"
echo ""

# Step 2: Copy scenario creation script and create scenario
echo "Step 2: Creating scenario in database..."
docker cp backend/create_email_bomb_teams_scenario.py "$BACKEND_CONTAINER:/app/create_email_bomb_teams_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/create_email_bomb_teams_scenario.py

if [ $? -ne 0 ]; then
    echo "❌ Error creating scenario"
    exit 1
fi

echo ""
echo "✅ Successfully created Email Bomb + Teams Call scenario!"
echo ""
echo "Scenario: 'Email Bomb & Social Engineering Attack'"
echo "- 5 phases with artifact-driven decisions"
echo "- Phase 1: Email Bomb Deployment"
echo "- Phase 2: Teams Call Impersonation"
echo "- Phase 3: Credential Harvesting"
echo "- Phase 4: Remote Access & Persistence"
echo "- Phase 5: Initial Access & C2 Communication"
echo "- Detailed Defender/E5 security tool artifacts for Blue Team"
echo "- Realistic Red Team social engineering and tool outputs"
echo "- Intermediate difficulty level"
echo ""
echo "You can now create a game using this scenario from the GM console."

