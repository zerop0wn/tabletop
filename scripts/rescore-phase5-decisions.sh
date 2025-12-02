#!/bin/bash
# Script to re-score Phase 5 decisions for existing games
# Usage: ./scripts/rescore-phase5-decisions.sh

set -e

echo "=========================================="
echo "Re-scoring Phase 5 Decisions"
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

# Copy and run the re-scoring script
echo "Re-scoring Phase 5 decisions..."
docker cp backend/rescore_phase5_decisions.py "$BACKEND_CONTAINER:/app/rescore_phase5_decisions.py"
docker exec "$BACKEND_CONTAINER" python /app/rescore_phase5_decisions.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Phase 5 decisions re-scored successfully!"
    echo ""
    echo "The audience view should now show updated scores."
else
    echo ""
    echo "❌ Failed to re-score decisions"
    exit 1
fi

