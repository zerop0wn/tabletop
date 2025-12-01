#!/bin/bash
# Script to update Operation Inbox Overload artifacts with generated content
# Usage: ./scripts/update-operation-inbox-overload-artifacts.sh

set -e

echo "=========================================="
echo "Updating Operation Inbox Overload Artifacts"
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
docker cp backend/generate_operation_inbox_overload_artifacts.py "$BACKEND_CONTAINER:/app/generate_operation_inbox_overload_artifacts.py"

if [ $? -ne 0 ]; then
    echo "❌ Error copying artifact generation script"
    exit 1
fi

echo "✓ Artifact generation script copied"
echo ""

# Step 2: Copy update script and run it
echo "Step 2: Updating artifacts in database..."
docker cp backend/update_operation_inbox_overload_artifacts.py "$BACKEND_CONTAINER:/app/update_operation_inbox_overload_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/update_operation_inbox_overload_artifacts.py

if [ $? -ne 0 ]; then
    echo "❌ Error updating artifacts"
    exit 1
fi

echo ""
echo "✅ Successfully updated Operation Inbox Overload artifacts!"
echo ""
echo "All artifacts now have generated content."

