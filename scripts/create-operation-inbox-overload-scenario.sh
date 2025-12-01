#!/bin/bash
# Script to create the Operation Inbox Overload scenario
# Usage: ./scripts/create-operation-inbox-overload-scenario.sh

set -e

echo "=========================================="
echo "Creating Operation Inbox Overload Scenario"
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

# Step 1: Copy scenario creation script and create scenario
echo "Step 1: Creating scenario in database..."
docker cp backend/create_operation_inbox_overload_scenario.py "$BACKEND_CONTAINER:/app/create_operation_inbox_overload_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/create_operation_inbox_overload_scenario.py

if [ $? -ne 0 ]; then
    echo "❌ Error creating scenario"
    exit 1
fi

echo ""
echo "✅ Successfully created Operation Inbox Overload scenario!"
echo ""
echo "Scenario: 'Operation Inbox Overload'"
echo "- 5 phases with artifact-driven decisions"
echo "- Phase 0: Email Flood Disruption"
echo "- Phase 1: Panic Driven Help-Seeking"
echo "- Phase 2: Teams Impersonation Callback"
echo "- Phase 3: MFA Reset Attempt & Endpoint Foothold"
echo "- Phase 4: Persistence vs Containment"
echo "- 0-10 scoring scale with clear optimal choices"
echo "- Focus on identity and endpoint containment decisions"
echo ""
echo "Note: Artifacts are currently placeholders. Implement artifact generation"
echo "      functions to populate realistic artifacts for each phase."
echo ""
echo "You can now create a game using this scenario from the GM console."

