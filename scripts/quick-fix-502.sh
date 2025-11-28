#!/bin/bash
# Quick fix for 502 Bad Gateway

set -e

echo "Quick Fix for 502 Bad Gateway"
echo "=============================="
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    echo "Please create it from env.production.template"
    exit 1
fi

echo "✓ .env.production found"
echo ""

# Load environment variables
export $(cat .env.production | grep -v '^#' | xargs)

# Check service status
echo "1. Current service status:"
docker-compose --env-file .env.production -f docker-compose.prod.yml ps
echo ""

# Stop all services
echo "2. Stopping all services..."
docker-compose --env-file .env.production -f docker-compose.prod.yml down
echo ""

# Pull latest nginx config (if needed)
echo "3. Pulling latest code..."
git pull
echo ""

# Rebuild and start services
echo "4. Building and starting services..."
docker-compose --env-file .env.production -f docker-compose.prod.yml up -d --build
echo ""

# Wait for services to start
echo "5. Waiting for services to initialize..."
sleep 10
echo ""

# Check service status again
echo "6. Service status after restart:"
docker-compose --env-file .env.production -f docker-compose.prod.yml ps
echo ""

# Check backend logs
echo "7. Backend logs (last 20 lines):"
docker-compose --env-file .env.production -f docker-compose.prod.yml logs backend --tail=20
echo ""

# Test backend health
echo "8. Testing backend health endpoint..."
BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
if [ -n "$BACKEND_CONTAINER" ]; then
    if docker exec "$BACKEND_CONTAINER" wget -q -O- http://localhost:8000/health 2>/dev/null; then
        echo "✓ Backend is healthy"
    else
        echo "❌ Backend health check failed"
        echo "Check logs: docker-compose -f docker-compose.prod.yml logs backend"
    fi
else
    echo "❌ Backend container not found"
fi
echo ""

# Test nginx to backend connectivity
echo "9. Testing nginx -> backend connectivity..."
FRONTEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q frontend)
if [ -n "$FRONTEND_CONTAINER" ]; then
    if docker exec "$FRONTEND_CONTAINER" wget -q --spider --timeout=5 http://backend:8000/health 2>&1; then
        echo "✓ Nginx can reach backend"
    else
        echo "❌ Nginx cannot reach backend"
        echo "This is the cause of the 502 error"
    fi
else
    echo "❌ Frontend container not found"
fi
echo ""

# Reload nginx
echo "10. Reloading nginx configuration..."
if docker exec "$FRONTEND_CONTAINER" nginx -t 2>&1; then
    docker exec "$FRONTEND_CONTAINER" nginx -s reload 2>&1 || echo "⚠️  Nginx reload failed, restarting..."
    docker-compose --env-file .env.production -f docker-compose.prod.yml restart frontend
    echo "✓ Nginx reloaded"
else
    echo "❌ Nginx configuration has errors"
fi
echo ""

echo "======================================"
echo "Fix complete!"
echo ""
echo "Test the API:"
echo "  curl https://cyberirtabletop.com/api/health"
echo ""
echo "If still getting 502, check:"
echo "  1. Backend logs: docker-compose --env-file .env.production -f docker-compose.prod.yml logs backend"
echo "  2. Frontend logs: docker-compose --env-file .env.production -f docker-compose.prod.yml logs frontend"
echo "  3. Run full diagnostic: ./scripts/troubleshoot-502.sh"
echo ""

