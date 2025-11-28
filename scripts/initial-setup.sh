#!/bin/bash
# Initial Production Setup Script
# Run this script once to set up the production environment

set -e

echo "Cyber Tabletop Production Setup"
echo "================================"
echo ""

# Check if running as root for SSL setup
if [ "$EUID" -ne 0 ]; then 
    echo "Note: SSL setup requires root. You may need to run 'sudo ./scripts/setup-ssl.sh' separately."
    SSL_SETUP=false
else
    SSL_SETUP=true
fi

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "Creating .env.production from template..."
    cp env.production.template .env.production
    echo ""
    echo "⚠️  IMPORTANT: Edit .env.production and set:"
    echo "   - POSTGRES_PASSWORD (use: openssl rand -base64 32)"
    echo "   - JWT_SECRET_KEY (use: openssl rand -base64 64)"
    echo ""
    read -p "Press Enter after you've edited .env.production..."
fi

# Check if SSL certificates exist
if [ ! -d "/etc/letsencrypt/live/cyberirtabletop.com" ]; then
    echo "SSL certificates not found."
    if [ "$SSL_SETUP" = true ]; then
        echo "Running SSL setup..."
        ./scripts/setup-ssl.sh
    else
        echo "Please run: sudo ./scripts/setup-ssl.sh"
        exit 1
    fi
else
    echo "✓ SSL certificates found"
fi

# Build production images
echo ""
echo "Building production Docker images..."
docker-compose -f docker-compose.prod.yml build

# Start services
echo ""
echo "Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database to be ready
echo ""
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo ""
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

# Seed initial data
echo ""
echo "Seeding initial data..."
docker-compose -f docker-compose.prod.yml exec -T backend python seed_data.py

echo ""
echo "=================================="
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Visit https://cyberirtabletop.com"
echo "2. Log in with: admin / admin123"
echo "3. Change the admin password immediately"
echo "4. Set up certificate auto-renewal:"
echo "   sudo crontab -e"
echo "   Add: 0 0 * * * $(pwd)/scripts/renew-cert.sh"
echo ""
echo "Check service status:"
echo "  docker-compose -f docker-compose.prod.yml ps"
echo ""
echo "View logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""

