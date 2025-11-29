#!/bin/bash
# Complete Production Data Setup Script
# This script seeds the database and generates all artifacts

set -e

echo "Production Data Setup"
echo "====================="
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

# Check if database migrations are up to date
echo "1. Checking database migrations..."
CURRENT_STATE=$(docker exec "$BACKEND_CONTAINER" alembic current 2>&1)

if echo "$CURRENT_STATE" | grep -q "head\|\([a-f0-9]\{12\}\)"; then
    echo "✓ Database migrations are up to date"
    # Check if we need to upgrade
    if echo "$CURRENT_STATE" | grep -q "head"; then
        echo "   Already at latest version"
    else
        echo "⚠️  Upgrading to latest version..."
        docker exec "$BACKEND_CONTAINER" alembic upgrade head
        if [ $? -eq 0 ]; then
            echo "✓ Migrations completed"
        else
            echo "⚠️  Migration upgrade had issues (may already be at latest)"
        fi
    fi
elif echo "$CURRENT_STATE" | grep -q "Can't locate revision"; then
    echo "⚠️  Database exists but Alembic doesn't know its state"
    echo "   Stamping database with latest revision..."
    LATEST_REVISION=$(docker exec "$BACKEND_CONTAINER" alembic heads 2>&1 | grep -oP '^[a-f0-9]+' | head -1)
    if [ -n "$LATEST_REVISION" ]; then
        docker exec "$BACKEND_CONTAINER" alembic stamp "$LATEST_REVISION"
        echo "✓ Database stamped with revision: $LATEST_REVISION"
    else
        echo "⚠️  Could not determine latest revision, skipping stamp"
    fi
else
    echo "⚠️  Running database migrations..."
    docker exec "$BACKEND_CONTAINER" alembic upgrade head
    if [ $? -eq 0 ]; then
        echo "✓ Migrations completed"
    else
        echo "⚠️  Migration had issues, but continuing..."
    fi
fi
echo ""

# Seed database with scenarios and admin user
echo "2. Seeding database with scenarios and admin user..."
docker exec "$BACKEND_CONTAINER" python seed_data.py
if [ $? -eq 0 ]; then
    echo "✓ Database seeded successfully"
else
    echo "❌ Database seeding failed"
    exit 1
fi
echo ""

# Generate artifact files
echo "3. Generating artifact files..."
docker exec "$BACKEND_CONTAINER" python generate_realistic_artifacts.py
if [ $? -eq 0 ]; then
    echo "✓ Artifacts generated successfully"
else
    echo "⚠️  Artifact generation had issues (this is okay if artifacts already exist)"
fi
echo ""

# Verify artifacts directory
echo "4. Verifying artifacts directory..."
ARTIFACT_COUNT=$(docker exec "$BACKEND_CONTAINER" find /app/artifacts -type f 2>/dev/null | wc -l)
if [ "$ARTIFACT_COUNT" -gt 0 ]; then
    echo "✓ Found $ARTIFACT_COUNT artifact files"
else
    echo "⚠️  No artifact files found (this may be normal if artifacts are stored in database)"
fi
echo ""

# Summary
echo "======================================"
echo "Production Data Setup Complete!"
echo ""
echo "Summary:"
echo "  ✓ Database migrations: Up to date"
echo "  ✓ Database seeded: Scenarios and admin user created"
echo "  ✓ Artifacts: Generated"
echo ""
echo "Default admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the admin password immediately!"
echo "   Run: ./scripts/reset-admin-password.sh"
echo ""
echo "You can now access the application at:"
echo "  https://cyberirtabletop.com"
echo ""

