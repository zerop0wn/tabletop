#!/bin/bash
# Add Tutorial Scenario to Production Database
# This script runs the seed script which will create the tutorial scenario if it doesn't exist

set -e

echo "Adding Tutorial Scenario to Production Database"
echo "================================================"
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
    echo "Starting backend..."
    docker-compose --env-file .env.production -f docker-compose.prod.yml up -d backend
    sleep 10
    BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
    if [ -z "$BACKEND_CONTAINER" ]; then
        echo "❌ Failed to start backend container"
        exit 1
    fi
fi

echo "✓ Backend container is running"
echo ""

# Run seed script (it will create tutorial scenario if it doesn't exist)
echo "Running seed script to create tutorial scenario..."
docker exec "$BACKEND_CONTAINER" python seed_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Tutorial scenario should now be available!"
    echo ""
    echo "You can now:"
    echo "1. Refresh the 'Create New Game' page"
    echo "2. Look for 'Tutorial: Basic Security Incident' in the scenario dropdown"
    echo ""
else
    echo ""
    echo "❌ Failed to create tutorial scenario. Check the logs above for errors."
    exit 1
fi

