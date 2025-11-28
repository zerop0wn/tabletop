#!/bin/bash
# SSL Certificate Setup Script for cyberirtabletop.com
# This script sets up Let's Encrypt SSL certificates using Certbot

set -e

DOMAIN="cyberirtabletop.com"
EMAIL="admin@cyberirtabletop.com"  # Change this to your email

echo "Setting up SSL certificates for $DOMAIN..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install Certbot if not already installed
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    if [ -f /etc/redhat-release ]; then
        # RHEL/CentOS/Amazon Linux
        yum install -y certbot
    elif [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y certbot
    else
        echo "Unsupported OS. Please install Certbot manually."
        exit 1
    fi
fi

# Create directory for ACME challenges
mkdir -p /var/www/certbot

# Stop any running web server temporarily (if needed)
# systemctl stop nginx 2>/dev/null || true

# Obtain certificate using standalone mode
echo "Obtaining SSL certificate..."
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" \
    --preferred-challenges http

# Set proper permissions
chmod 755 /etc/letsencrypt/live
chmod 755 /etc/letsencrypt/archive
chmod 644 /etc/letsencrypt/live/$DOMAIN/fullchain.pem
chmod 600 /etc/letsencrypt/live/$DOMAIN/privkey.pem

echo "SSL certificate obtained successfully!"
echo "Certificate location: /etc/letsencrypt/live/$DOMAIN/"
echo ""
echo "Next steps:"
echo "1. Update docker-compose.prod.yml with your production environment variables"
echo "2. Start the production stack: docker-compose -f docker-compose.prod.yml up -d"
echo "3. Test certificate renewal: certbot renew --dry-run"

