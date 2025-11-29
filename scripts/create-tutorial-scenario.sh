#!/bin/bash
# Create Tutorial Scenario Script
# This script runs the Python script to create the tutorial scenario

set -e

echo "Creating Tutorial Scenario"
echo "==========================="
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
echo "Creating tutorial scenario..."
docker cp scripts/create-tutorial-scenario.py "$BACKEND_CONTAINER:/app/create_tutorial.py"
docker exec "$BACKEND_CONTAINER" python /app/create_tutorial.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Tutorial scenario should now be available!"
    echo ""
    echo "Refresh your browser and check the scenario dropdown."
else
    echo ""
    echo "❌ Failed to create tutorial scenario"
    exit 1
fi

