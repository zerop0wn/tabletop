#!/bin/bash
# Script to verify artifact files exist in both container and host
# Usage: ./scripts/verify-artifact-files.sh

set -e

echo "=========================================="
echo "Verifying Artifact Files"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.dev.yml" ] && [ ! -f "docker-compose.prod.yml" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Determine which docker-compose file to use and get backend container
if [ -f "docker-compose.prod.yml" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    ENV_FILE="--env-file .env.production"
    BACKEND_CONTAINER=$(docker-compose $ENV_FILE -f "$COMPOSE_FILE" ps -q backend)
else
    COMPOSE_FILE="docker-compose.dev.yml"
    ENV_FILE=""
    BACKEND_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q backend)
fi

# Check if backend container is running
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container is not running!"
    exit 1
fi

echo "✓ Backend container is running"
echo ""

# Check files in container
echo "1. Checking files INSIDE container at /app/artifacts/files/:"
docker exec "$BACKEND_CONTAINER" ls -la /app/artifacts/files/ | head -10
echo ""

# Check files on host
echo "2. Checking files on HOST at ./backend/artifacts/files/:"
if [ -d "backend/artifacts/files" ]; then
    ls -la backend/artifacts/files/ | head -10
else
    echo "   ❌ Directory backend/artifacts/files/ does not exist on host!"
    echo "   Creating directory..."
    mkdir -p backend/artifacts/files
    echo "   ✓ Directory created"
fi

echo ""

# Test a specific file
test_file="hr_recon_phase1.txt"
echo "3. Testing specific file: $test_file"
echo "   In container:"
if docker exec "$BACKEND_CONTAINER" test -f "/app/artifacts/files/$test_file"; then
    size=$(docker exec "$BACKEND_CONTAINER" stat -c%s "/app/artifacts/files/$test_file")
    echo "   ✓ File exists in container (size: $size bytes)"
else
    echo "   ❌ File NOT found in container"
fi

echo "   On host:"
if [ -f "backend/artifacts/files/$test_file" ]; then
    size=$(stat -c%s "backend/artifacts/files/$test_file" 2>/dev/null || stat -f%z "backend/artifacts/files/$test_file" 2>/dev/null || echo "unknown")
    echo "   ✓ File exists on host (size: $size bytes)"
else
    echo "   ❌ File NOT found on host"
    echo ""
    echo "   ⚠️  WARNING: File exists in container but not on host!"
    echo "   This suggests the volume mount may not be working correctly."
    echo "   Try copying files from container to host:"
    echo "   docker cp $BACKEND_CONTAINER:/app/artifacts/files/$test_file backend/artifacts/files/"
fi

echo ""
echo "4. Testing route directly:"
echo "   Testing: GET /artifacts/files/$test_file"
response=$(docker exec "$BACKEND_CONTAINER" curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/artifacts/files/$test_file 2>/dev/null || echo "000")
if [ "$response" = "200" ]; then
    echo "   ✓ Route returns 200 OK"
elif [ "$response" = "404" ]; then
    echo "   ❌ Route returns 404 Not Found"
    echo "   This means the route is being matched but the file check is failing"
else
    echo "   ⚠️  Route test failed (response code: $response)"
fi

echo ""
echo "=========================================="
echo "Verification Complete"
echo "=========================================="

