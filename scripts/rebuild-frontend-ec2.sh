#!/bin/bash
# Script to rebuild the frontend on EC2

echo "Rebuilding frontend container..."
cd /opt/tabletop

# Rebuild the frontend service
sudo docker-compose --env-file .env.production -f docker-compose.prod.yml build frontend

# Restart the frontend service
sudo docker-compose --env-file .env.production -f docker-compose.prod.yml up -d frontend

echo "Frontend rebuild complete!"
echo "Check logs with: sudo docker-compose --env-file .env.production -f docker-compose.prod.yml logs frontend --tail=50"

