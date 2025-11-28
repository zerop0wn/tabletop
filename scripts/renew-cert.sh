#!/bin/bash
# SSL Certificate Renewal Script
# This script renews Let's Encrypt certificates and reloads Nginx
# Should be run via cron: 0 0 * * * /path/to/renew-cert.sh

set -e

DOMAIN="cyberirtabletop.com"

echo "Checking certificate renewal for $DOMAIN..."

# Renew certificates
certbot renew --quiet

# Reload Nginx if certificates were renewed
if [ $? -eq 0 ]; then
    echo "Reloading Nginx..."
    docker-compose -f docker-compose.prod.yml exec frontend nginx -s reload || true
    echo "Certificate renewal complete"
else
    echo "No renewal needed"
fi

