#!/bin/bash
# Diagnostic script to check phase-specific actions

set -e

echo "Diagnosing Phase Actions"
echo "========================"
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
docker cp backend/diagnose_phase_actions.py "$BACKEND_CONTAINER:/app/diagnose_phase_actions.py"
docker exec "$BACKEND_CONTAINER" python /app/diagnose_phase_actions.py

