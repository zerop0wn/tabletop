#!/bin/bash
# Production Status Check Script

set -e

echo "Cyber Tabletop Production Status Check"
echo "===================================="
echo ""

# Check if docker-compose is running
echo "1. Checking Docker Compose services..."
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "   ⚠️  No services are running!"
    echo "   Run: docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

echo "   ✓ Services are running"
echo ""

# Check service status
echo "2. Service Status:"
docker-compose -f docker-compose.prod.yml ps
echo ""

# Check if backend is accessible
echo "3. Checking backend connectivity..."
BACKEND_CONTAINER=$(docker-compose -f docker-compose.prod.yml ps -q backend)
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "   ⚠️  Backend container not found!"
    exit 1
fi

# Test if backend is responding
if docker exec "$BACKEND_CONTAINER" curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✓ Backend health check passed"
else
    echo "   ⚠️  Backend health check failed"
    echo "   Checking backend logs..."
    docker-compose -f docker-compose.prod.yml logs backend --tail=50
fi
echo ""

# Check if nginx can reach backend
echo "4. Checking nginx to backend connectivity..."
FRONTEND_CONTAINER=$(docker-compose -f docker-compose.prod.yml ps -q frontend)
if [ -z "$FRONTEND_CONTAINER" ]; then
    echo "   ⚠️  Frontend container not found!"
    exit 1
fi

# Test from nginx container
if docker exec "$FRONTEND_CONTAINER" wget -q --spider http://backend:8000/health 2>&1; then
    echo "   ✓ Nginx can reach backend"
else
    echo "   ⚠️  Nginx cannot reach backend!"
    echo "   This is likely the cause of the 502 error."
    echo ""
    echo "   Checking network connectivity..."
    docker exec "$FRONTEND_CONTAINER" ping -c 2 backend || echo "   ⚠️  Cannot ping backend hostname"
fi
echo ""

# Check nginx configuration
echo "5. Checking nginx configuration..."
if docker exec "$FRONTEND_CONTAINER" nginx -t 2>&1; then
    echo "   ✓ Nginx configuration is valid"
else
    echo "   ⚠️  Nginx configuration has errors!"
fi
echo ""

# Show recent logs
echo "6. Recent Backend Logs (last 20 lines):"
docker-compose -f docker-compose.prod.yml logs backend --tail=20
echo ""

echo "7. Recent Frontend/Nginx Logs (last 20 lines):"
docker-compose -f docker-compose.prod.yml logs frontend --tail=20
echo ""

echo "===================================="
echo "Diagnostic complete!"
echo ""
echo "Common fixes:"
echo "1. If backend is not running: docker-compose -f docker-compose.prod.yml up -d backend"
echo "2. If database migrations needed: docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head"
echo "3. If services need restart: docker-compose -f docker-compose.prod.yml restart"
echo ""

