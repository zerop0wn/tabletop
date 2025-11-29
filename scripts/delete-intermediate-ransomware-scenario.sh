#!/bin/bash
# Script to delete the intermediate ransomware scenario
# Usage: ./scripts/delete-intermediate-ransomware-scenario.sh

set -e

echo "=========================================="
echo "Deleting Intermediate Ransomware Scenario"
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

# Copy and run the deletion script
echo "Deleting scenario..."
docker cp backend/delete_intermediate_ransomware_scenario.py "$BACKEND_CONTAINER:/app/delete_intermediate_ransomware_scenario.py"
docker exec "$BACKEND_CONTAINER" python /app/delete_intermediate_ransomware_scenario.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Scenario deleted successfully!"
    echo ""
    echo "You can now re-run the creation script to recreate it with updated URLs:"
    echo "  sudo ./scripts/create-intermediate-ransomware-scenario.sh"
else
    echo ""
    echo "❌ Failed to delete scenario"
    exit 1
fi

