#!/bin/bash
# Script to purge all scenarios except tutorial and delete all games

set -e

echo "PURGE SCENARIOS AND GAMES"
echo "========================="
echo ""
echo "⚠️  WARNING: This will delete:"
echo "   - All games"
echo "   - All scenarios EXCEPT the Tutorial scenario"
echo "   - All related data (teams, players, votes, etc.)"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

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

echo ""
echo "✓ Backend container is running"
echo ""

# Copy and run the purge script
echo "Running purge script..."
docker cp backend/purge_scenarios.py "$BACKEND_CONTAINER:/app/purge_scenarios.py"
docker exec "$BACKEND_CONTAINER" python /app/purge_scenarios.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Purge completed successfully!"
    echo ""
    echo "You can now create new scenarios from scratch."
else
    echo ""
    echo "❌ Purge failed"
    exit 1
fi

