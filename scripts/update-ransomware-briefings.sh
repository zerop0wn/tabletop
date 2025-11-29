#!/bin/bash
# Script to update briefing texts for the new Ransomware scenario

set -e

echo "Updating Ransomware Scenario Briefings"
echo "======================================="
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

# Copy and run the update script
echo "Updating briefing texts..."
docker cp backend/update_ransomware_briefings.py "$BACKEND_CONTAINER:/app/update_ransomware_briefings.py"
docker exec "$BACKEND_CONTAINER" python /app/update_ransomware_briefings.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Briefing texts updated successfully!"
    echo ""
    echo "Refresh your browser to see the updated briefings."
else
    echo ""
    echo "❌ Failed to update briefing texts"
    exit 1
fi

