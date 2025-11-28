#!/bin/bash
# Start Production Stack Script
# This script helps start the production environment

set -e

echo "Starting Cyber Tabletop Production Stack"
echo "=========================================="
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "⚠️  .env.production not found!"
    echo ""
    echo "Creating from template..."
    cp env.production.template .env.production
    echo ""
    echo "⚠️  IMPORTANT: You MUST edit .env.production before starting!"
    echo ""
    echo "Required values:"
    echo "  - POSTGRES_PASSWORD: Generate with: openssl rand -base64 32"
    echo "  - JWT_SECRET_KEY: Generate with: openssl rand -base64 64"
    echo ""
    read -p "Press Enter to open .env.production for editing (Ctrl+C to cancel)..."
    ${EDITOR:-nano} .env.production
fi

# Check if SSL certificates exist
if [ ! -f /etc/letsencrypt/live/cyberirtabletop.com/fullchain.pem ]; then
    echo "⚠️  SSL certificates not found!"
    echo "Run: sudo ./scripts/setup-ssl.sh"
    exit 1
fi

echo "✓ SSL certificates found"
echo ""

# Build production images
echo "Building production Docker images..."
docker-compose -f docker-compose.prod.yml build

# Start services
echo ""
echo "Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "Service Status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "=========================================="
echo "Production stack started!"
echo ""
echo "Next steps:"
echo "1. Wait a moment for services to fully start"
echo "2. Visit https://cyberirtabletop.com"
echo "3. Run database migrations:"
echo "   docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head"
echo "4. Seed initial data:"
echo "   docker-compose -f docker-compose.prod.yml exec backend python seed_data.py"
echo ""
echo "View logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""

