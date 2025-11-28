#!/bin/bash
# Complete Production Restart Script
# This ensures all services restart with correct environment variables

set -e

echo "Complete Production Restart"
echo "==========================="
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    echo "Please create it from env.production.template"
    exit 1
fi

echo "✓ .env.production found"
echo ""

# Stop all services
echo "1. Stopping all services..."
docker-compose --env-file .env.production -f docker-compose.prod.yml down
echo ""

# Wait a moment
sleep 2

# Start database first
echo "2. Starting database..."
docker-compose --env-file .env.production -f docker-compose.prod.yml up -d db
echo "Waiting for database to be ready..."
sleep 10
echo ""

# Start backend
echo "3. Starting backend..."
docker-compose --env-file .env.production -f docker-compose.prod.yml up -d backend
echo "Waiting for backend to start..."
sleep 10
echo ""

# Check backend health
echo "4. Checking backend health..."
BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
if [ -n "$BACKEND_CONTAINER" ]; then
    # Try curl first, then python if curl not available
    if docker exec "$BACKEND_CONTAINER" sh -c "command -v curl >/dev/null && curl -s http://localhost:8000/health || python -c \"import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())\"" 2>/dev/null | grep -q "healthy"; then
        echo "✓ Backend is healthy"
    else
        echo "❌ Backend health check failed"
        echo "Backend logs:"
        docker-compose --env-file .env.production -f docker-compose.prod.yml logs backend --tail=30
        echo ""
        echo "⚠️  If you see database password errors, run:"
        echo "   ./scripts/fix-database-password.sh"
        exit 1
    fi
else
    echo "❌ Backend container not found"
    exit 1
fi
echo ""

# Start frontend
echo "5. Starting frontend..."
docker-compose --env-file .env.production -f docker-compose.prod.yml up -d frontend
echo "Waiting for frontend to start..."
sleep 5
echo ""

# Check nginx can reach backend
echo "6. Checking nginx -> backend connectivity..."
FRONTEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q frontend)
if [ -n "$FRONTEND_CONTAINER" ]; then
    if docker exec "$FRONTEND_CONTAINER" wget -q --spider --timeout=5 http://backend:8000/health 2>&1; then
        echo "✓ Nginx can reach backend"
    else
        echo "❌ Nginx cannot reach backend"
        echo "This will cause 502 errors"
        echo ""
        echo "Checking network..."
        docker network inspect tabletop_internal 2>/dev/null | grep -A 10 "Containers" || echo "Network check failed"
    fi
else
    echo "❌ Frontend container not found"
fi
echo ""

# Reload nginx
echo "7. Reloading nginx..."
if docker exec "$FRONTEND_CONTAINER" nginx -t 2>&1; then
    docker exec "$FRONTEND_CONTAINER" nginx -s reload 2>&1 || echo "⚠️  Nginx reload failed, will restart"
    docker-compose --env-file .env.production -f docker-compose.prod.yml restart frontend
    echo "✓ Nginx reloaded"
else
    echo "❌ Nginx configuration has errors"
    docker exec "$FRONTEND_CONTAINER" nginx -t
fi
echo ""

# Final status check
echo "8. Final service status:"
docker-compose --env-file .env.production -f docker-compose.prod.yml ps
echo ""

# Test API endpoint
echo "9. Testing API endpoint..."
sleep 2
if curl -k -s https://cyberirtabletop.com/api/health | grep -q "healthy"; then
    echo "✓ API is responding correctly"
else
    echo "❌ API test failed"
    echo "Response:"
    curl -k -v https://cyberirtabletop.com/api/health 2>&1 | head -20
fi
echo ""

echo "======================================"
echo "Restart complete!"
echo ""
echo "If you still see 502 errors:"
echo "1. Check backend logs: docker-compose --env-file .env.production -f docker-compose.prod.yml logs backend"
echo "2. Check frontend logs: docker-compose --env-file .env.production -f docker-compose.prod.yml logs frontend"
echo "3. Verify .env.production has all required variables"
echo ""

