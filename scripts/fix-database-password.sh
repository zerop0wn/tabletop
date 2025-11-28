#!/bin/bash
# Fix Database Password Mismatch
# This script updates the database password or recreates the database volume

set -e

echo "Fix Database Password Mismatch"
echo "==============================="
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    exit 1
fi

# Load environment variables
export $(cat .env.production | grep -v '^#' | grep -v '^$' | xargs)

echo "Current POSTGRES_PASSWORD from .env.production: ${POSTGRES_PASSWORD:0:10}..."
echo ""

# Stop all services
echo "1. Stopping all services..."
docker-compose --env-file .env.production -f docker-compose.prod.yml down
echo ""

# Ask user what they want to do
echo "Choose an option:"
echo "1. Recreate database volume (WARNING: This will DELETE all data)"
echo "2. Update password in existing database (requires old password)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "⚠️  WARNING: This will DELETE all existing data!"
    read -p "Are you sure? Type 'yes' to continue: " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Aborted."
        exit 0
    fi
    
    echo ""
    echo "2. Removing database volume..."
    docker volume rm tabletop_postgres_data 2>/dev/null || echo "Volume doesn't exist or already removed"
    echo ""
    
    echo "3. Starting database with new password..."
    docker-compose --env-file .env.production -f docker-compose.prod.yml up -d db
    echo "Waiting for database to be ready..."
    sleep 10
    echo ""
    
    echo "4. Database recreated successfully!"
    echo "   Next steps:"
    echo "   - Run migrations: docker-compose --env-file .env.production -f docker-compose.prod.yml exec backend alembic upgrade head"
    echo "   - Seed data: docker-compose --env-file .env.production -f docker-compose.prod.yml exec backend python seed_data.py"
    
elif [ "$choice" = "2" ]; then
    echo ""
    read -p "Enter the OLD database password: " old_password
    echo ""
    
    echo "2. Starting database with old password temporarily..."
    # Create a temporary docker-compose override
    cat > docker-compose.temp.yml <<EOF
services:
  db:
    environment:
      POSTGRES_PASSWORD: ${old_password}
EOF
    
    docker-compose -f docker-compose.prod.yml -f docker-compose.temp.yml up -d db
    sleep 10
    echo ""
    
    echo "3. Updating password in database..."
    docker-compose -f docker-compose.prod.yml -f docker-compose.temp.yml exec -T db psql -U cybertabletop -d postgres <<EOF
ALTER USER cybertabletop WITH PASSWORD '${POSTGRES_PASSWORD}';
EOF
    echo ""
    
    echo "4. Restarting database with new password..."
    docker-compose -f docker-compose.prod.yml -f docker-compose.temp.yml down
    rm docker-compose.temp.yml
    docker-compose --env-file .env.production -f docker-compose.prod.yml up -d db
    sleep 10
    echo ""
    
    echo "5. Password updated successfully!"
else
    echo "Invalid choice. Aborted."
    exit 1
fi

echo ""
echo "======================================"
echo "Database password fix complete!"
echo ""
echo "You can now start the backend:"
echo "  docker-compose --env-file .env.production -f docker-compose.prod.yml up -d backend"
echo ""

