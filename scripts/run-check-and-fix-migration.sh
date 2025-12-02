#!/bin/bash
# Copy and run the check_and_fix_migration.py helper inside the backend container
# Usage: ./scripts/run-check-and-fix-migration.sh

set -e

echo "============================================"
echo "Ensuring legacy databases have required cols"
echo "============================================"
echo ""

# Verify we're at the project root
if [ ! -f "docker-compose.dev.yml" ] && [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Please run this script from the project root"
    exit 1
fi

# Prefer production compose file when available
if [ -f "docker-compose.prod.yml" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    ENV_FILE="--env-file .env.production"
    BACKEND_CONTAINER=$(docker-compose $ENV_FILE -f "$COMPOSE_FILE" ps -q backend)
else
    COMPOSE_FILE="docker-compose.dev.yml"
    ENV_FILE=""
    BACKEND_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q backend)
fi

if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container is not running. Start it with docker-compose up backend."
    exit 1
fi

echo "✓ Backend container detected ($BACKEND_CONTAINER)"
echo ""

# Step 1: Copy the latest version of the helper script
echo "Step 1: Copying check_and_fix_migration.py into backend container..."
docker cp backend/check_and_fix_migration.py "$BACKEND_CONTAINER:/app/check_and_fix_migration.py"

if [ $? -ne 0 ]; then
    echo "❌ Error copying check_and_fix_migration.py"
    exit 1
fi

echo "✓ Helper script copied"
echo ""

# Step 2: Run the script inside the container
echo "Step 2: Running schema backfill script..."
docker exec "$BACKEND_CONTAINER" python /app/check_and_fix_migration.py

if [ $? -ne 0 ]; then
    echo "❌ Error running check_and_fix_migration.py"
    exit 1
fi

echo ""
echo "✅ check_and_fix_migration.py completed successfully"
echo "   Review the output above to confirm each column now exists."
