#!/bin/bash
# Diagnostic script to check why artifacts aren't showing

set -e

echo "Diagnosing Artifacts"
echo "===================="
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    exit 1
fi

# Check if backend container is running
BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container is not running!"
    exit 1
fi

echo "✓ Backend container is running"
echo ""

# Copy and run the diagnostic script
echo "Running diagnostic..."
docker cp backend/diagnose_artifacts.py "$BACKEND_CONTAINER:/app/diagnose_artifacts.py"
docker exec "$BACKEND_CONTAINER" python /app/diagnose_artifacts.py

