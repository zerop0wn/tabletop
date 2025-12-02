#!/bin/bash
# Script to rebuild and restart the backend container
# This ensures the latest code is included in the Docker image

set -e

echo "=========================================="
echo "Rebuilding Backend Container"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    echo "Please create it from env.production.template"
    exit 1
fi

echo "✓ .env.production found"
echo ""

# Rebuild backend image
echo "Step 1: Rebuilding backend image..."
docker-compose --env-file .env.production -f docker-compose.prod.yml build backend

if [ $? -ne 0 ]; then
    echo "❌ Error rebuilding backend"
    exit 1
fi

echo ""
echo "✓ Backend image rebuilt"
echo ""

# Restart backend
echo "Step 2: Restarting backend container..."
docker-compose --env-file .env.production -f docker-compose.prod.yml up -d backend

if [ $? -ne 0 ]; then
    echo "❌ Error restarting backend"
    exit 1
fi

echo ""
echo "✓ Backend container restarted"
echo ""

# Wait for backend to be ready
echo "Step 3: Waiting for backend to be ready..."
sleep 5

# Check backend health
BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
if [ -n "$BACKEND_CONTAINER" ]; then
    if docker exec "$BACKEND_CONTAINER" sh -c "command -v curl >/dev/null && curl -s http://localhost:8000/health || python -c \"import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())\"" 2>/dev/null | grep -q "healthy"; then
        echo "✓ Backend is healthy"
    else
        echo "⚠️  Backend may still be starting up"
    fi
fi

echo ""
echo "✅ Backend rebuild and restart complete!"
echo ""
echo "The backend container now has the latest code including:"
echo "  - Updated scoring.py with Operation Inbox Overload"
echo "  - Updated Phase 5 scoring for ransomware scenario"
echo ""
echo "You can now run the diagnostic script again:"
echo "  sudo ./scripts/diagnose-operation-inbox-overload-scoring.sh"

