#!/bin/bash
# Script to regenerate artifact files for the intermediate ransomware scenario
# Usage: ./scripts/regenerate-intermediate-artifacts.sh

set -e

echo "=========================================="
echo "Regenerating Intermediate Ransomware Artifacts"
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

# Copy and run the artifact generation script
echo "Generating artifact files..."
docker cp backend/generate_intermediate_ransomware_artifacts.py "$BACKEND_CONTAINER:/app/generate_intermediate_ransomware_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/generate_intermediate_ransomware_artifacts.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Artifact files generated successfully!"
    echo ""
    echo "Verifying files were created..."
    docker exec "$BACKEND_CONTAINER" ls -la /app/artifacts/files/*.txt | head -20
    echo ""
    echo "You can now use the scenario. Artifacts should be accessible."
else
    echo ""
    echo "❌ Failed to generate artifact files"
    exit 1
fi

