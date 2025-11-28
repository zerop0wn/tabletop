#!/bin/bash
# Troubleshoot 502 Bad Gateway Error

set -e

echo "Troubleshooting 502 Bad Gateway Error"
echo "======================================"
echo ""

# Check if services are running
echo "1. Checking service status..."
docker-compose -f docker-compose.prod.yml ps
echo ""

# Check backend container
echo "2. Checking backend container..."
BACKEND_CONTAINER=$(docker-compose -f docker-compose.prod.yml ps -q backend)
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "   ❌ Backend container is NOT running!"
    echo "   Starting backend..."
    docker-compose -f docker-compose.prod.yml up -d backend
    sleep 5
else
    echo "   ✓ Backend container found: $BACKEND_CONTAINER"
fi
echo ""

# Check if backend is listening on port 8000
echo "3. Checking if backend is listening on port 8000..."
if docker exec "$BACKEND_CONTAINER" netstat -tuln 2>/dev/null | grep -q ":8000" || \
   docker exec "$BACKEND_CONTAINER" ss -tuln 2>/dev/null | grep -q ":8000"; then
    echo "   ✓ Backend is listening on port 8000"
else
    echo "   ❌ Backend is NOT listening on port 8000"
fi
echo ""

# Test backend health endpoint directly
echo "4. Testing backend health endpoint directly..."
if docker exec "$BACKEND_CONTAINER" wget -q -O- http://localhost:8000/health 2>/dev/null; then
    echo "   ✓ Backend health endpoint responds"
else
    echo "   ❌ Backend health endpoint does NOT respond"
fi
echo ""

# Check backend logs for errors
echo "5. Recent backend logs (last 30 lines):"
docker-compose -f docker-compose.prod.yml logs backend --tail=30
echo ""

# Check if backend can reach database
echo "6. Checking database connectivity from backend..."
if docker exec "$BACKEND_CONTAINER" python -c "
import os
import sys
try:
    from sqlalchemy import create_engine, text
    db_url = os.getenv('DATABASE_URL', '')
    if db_url:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print('   ✓ Database connection successful')
    else:
        print('   ❌ DATABASE_URL not set')
        sys.exit(1)
except Exception as e:
    print(f'   ❌ Database connection failed: {e}')
    sys.exit(1)
" 2>&1; then
    echo ""
else
    echo "   ❌ Database connectivity check failed"
fi
echo ""

# Check network connectivity from frontend to backend
echo "7. Checking network connectivity (frontend -> backend)..."
FRONTEND_CONTAINER=$(docker-compose -f docker-compose.prod.yml ps -q frontend)
if [ -z "$FRONTEND_CONTAINER" ]; then
    echo "   ❌ Frontend container not found!"
else
    if docker exec "$FRONTEND_CONTAINER" wget -q --spider --timeout=5 http://backend:8000/health 2>&1; then
        echo "   ✓ Frontend can reach backend"
    else
        echo "   ❌ Frontend CANNOT reach backend!"
        echo "   Testing DNS resolution..."
        docker exec "$FRONTEND_CONTAINER" nslookup backend 2>&1 || docker exec "$FRONTEND_CONTAINER" getent hosts backend 2>&1
    fi
fi
echo ""

# Check nginx configuration
echo "8. Checking nginx configuration..."
if docker exec "$FRONTEND_CONTAINER" nginx -t 2>&1; then
    echo "   ✓ Nginx configuration is valid"
    echo "   Reloading nginx..."
    docker exec "$FRONTEND_CONTAINER" nginx -s reload 2>&1 || echo "   ⚠️  Nginx reload failed (may need restart)"
else
    echo "   ❌ Nginx configuration has errors!"
fi
echo ""

# Show network information
echo "9. Docker network information:"
docker network inspect tabletop_internal 2>/dev/null | grep -A 5 "Containers" || \
docker network ls | grep tabletop
echo ""

echo "======================================"
echo "Troubleshooting complete!"
echo ""
echo "Common fixes:"
echo "1. Restart backend: docker-compose -f docker-compose.prod.yml restart backend"
echo "2. Restart frontend: docker-compose -f docker-compose.prod.yml restart frontend"
echo "3. Restart all: docker-compose -f docker-compose.prod.yml restart"
echo "4. Rebuild and restart: docker-compose -f docker-compose.prod.yml up -d --build"
echo "5. Check .env.production file has all required variables"
echo ""

