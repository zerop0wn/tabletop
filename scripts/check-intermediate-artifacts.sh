#!/bin/bash
# Script to check if intermediate ransomware artifact files exist
# Usage: ./scripts/check-intermediate-artifacts.sh

set -e

echo "=========================================="
echo "Checking Intermediate Ransomware Artifacts"
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

# Copy and run the check script
echo "Checking artifact files..."
docker cp backend/check_intermediate_artifacts.py "$BACKEND_CONTAINER:/app/check_intermediate_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/check_intermediate_artifacts.py

