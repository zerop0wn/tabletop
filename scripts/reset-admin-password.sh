#!/bin/bash
# Reset Admin Password Script
# This script resets the admin user's password in the production database

set -e

echo "Reset Admin Password"
echo "===================="
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
    sleep 5
    BACKEND_CONTAINER=$(docker-compose --env-file .env.production -f docker-compose.prod.yml ps -q backend)
    if [ -z "$BACKEND_CONTAINER" ]; then
        echo "❌ Failed to start backend container"
        exit 1
    fi
fi

echo "✓ Backend container is running"
echo ""

# Prompt for new password
read -sp "Enter new password for admin user (min 6 characters): " new_password
echo ""
echo ""

if [ ${#new_password} -lt 6 ]; then
    echo "❌ Password must be at least 6 characters long"
    exit 1
fi

# Confirm password
read -sp "Confirm new password: " confirm_password
echo ""
echo ""

if [ "$new_password" != "$confirm_password" ]; then
    echo "❌ Passwords do not match"
    exit 1
fi

echo "Resetting admin password..."
echo ""

# Run Python script inside backend container to reset password
docker exec "$BACKEND_CONTAINER" python -c "
import sys
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import GMUser
from app.auth import get_password_hash

db: Session = SessionLocal()
try:
    # Find admin user
    admin_user = db.query(GMUser).filter(GMUser.username == 'admin').first()
    if not admin_user:
        print('❌ Admin user not found in database')
        print('You may need to run seed_data.py first')
        sys.exit(1)
    
    # Update password
    admin_user.password_hash = get_password_hash('$new_password')
    db.commit()
    print('✓ Admin password reset successfully')
    print('')
    print('You can now login with:')
    print('  Username: admin')
    print('  Password: (the password you just set)')
except Exception as e:
    print(f'❌ Error resetting password: {e}')
    db.rollback()
    sys.exit(1)
finally:
    db.close()
"

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Password reset complete!"
    echo ""
    echo "You can now login at: https://cyberirtabletop.com"
    echo "Username: admin"
    echo ""
else
    echo ""
    echo "❌ Password reset failed. Check the error message above."
    exit 1
fi

