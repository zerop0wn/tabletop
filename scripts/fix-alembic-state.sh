#!/bin/bash
# Fix Alembic Migration State
# This script stamps the database with the current migration version if tables already exist

set -e

echo "Fixing Alembic Migration State"
echo "==============================="
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

# Check current Alembic state
echo "1. Checking current Alembic state..."
CURRENT_VERSION=$(docker exec "$BACKEND_CONTAINER" alembic current 2>&1 | grep -oP '\([a-f0-9]+\)' | head -1 | tr -d '()' || echo "")

if [ -z "$CURRENT_VERSION" ]; then
    echo "⚠️  No Alembic version found. Database tables exist but Alembic doesn't know about them."
    echo ""
    echo "2. Stamping database with latest migration..."
    
    # Get the latest revision hash
    LATEST_REVISION=$(docker exec "$BACKEND_CONTAINER" alembic heads 2>&1 | grep -oP '^[a-f0-9]+' | head -1)
    
    if [ -z "$LATEST_REVISION" ]; then
        echo "❌ Could not determine latest revision"
        exit 1
    fi
    
    echo "   Latest revision: $LATEST_REVISION"
    echo "   Stamping database..."
    
    docker exec "$BACKEND_CONTAINER" alembic stamp "$LATEST_REVISION"
    
    if [ $? -eq 0 ]; then
        echo "✓ Database stamped successfully"
    else
        echo "❌ Failed to stamp database"
        exit 1
    fi
else
    echo "✓ Alembic version found: $CURRENT_VERSION"
    echo "   Database is already properly tracked by Alembic"
fi

echo ""
echo "3. Verifying Alembic state..."
docker exec "$BACKEND_CONTAINER" alembic current

echo ""
echo "======================================"
echo "Alembic state fixed!"
echo ""
echo "You can now run:"
echo "  ./scripts/setup-production-data.sh"
echo ""

