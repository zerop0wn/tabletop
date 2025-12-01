#!/bin/bash
# Script to remove Red Team artifacts from Operation Inbox Overload scenario
# Usage: ./scripts/remove-operation-inbox-overload-red-artifacts.sh

set -e

echo "=========================================="
echo "Removing Red Team Artifacts from Operation Inbox Overload"
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

# Copy and run the removal script
echo "Removing Red Team artifacts..."
docker cp backend/remove_operation_inbox_overload_red_artifacts.py "$BACKEND_CONTAINER:/app/remove_operation_inbox_overload_red_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/remove_operation_inbox_overload_red_artifacts.py

if [ $? -ne 0 ]; then
    echo "❌ Error removing artifacts"
    exit 1
fi

echo ""
echo "✅ Successfully removed Red Team artifacts from Operation Inbox Overload!"
echo ""
echo "Only Blue Team artifacts remain in the scenario."

