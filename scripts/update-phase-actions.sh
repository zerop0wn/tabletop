#!/bin/bash
# Update Phase Actions Script
# This script updates existing scenario phases with phase-specific actions

set -e

echo "Updating Phase Actions"
echo "======================"
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    exit 1
fi

# Load environment variables
export $(cat .env.production | grep -v '^#' | grep -v '^$' | xargs)

# Check if backend container is running
BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container is not running!"
    exit 1
fi

echo "✓ Backend container is running"
echo ""

# Copy the script to the container and run it
echo "Updating phase actions..."
docker cp backend/update_phase_actions.py "$BACKEND_CONTAINER:/app/update_phase_actions.py"
docker exec "$BACKEND_CONTAINER" python /app/update_phase_actions.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Phase actions updated successfully!"
    echo ""
    echo "Refresh your browser to see the new voting options."
else
    echo ""
    echo "❌ Failed to update phase actions"
    exit 1
fi

