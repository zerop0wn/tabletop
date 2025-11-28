#!/bin/bash
# SSL Certificate Setup Script using DNS validation (no port 80 required)
# This is useful when port 80 is in use or you can't open it

set -e

DOMAIN="cyberirtabletop.com"
EMAIL="admin@cyberirtabletop.com"  # Change this to your email

echo "Setting up SSL certificates for $DOMAIN using DNS validation..."
echo ""
echo "This method requires you to add TXT records to your DNS."
echo "You'll be prompted to add records during the process."
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install Certbot if not already installed
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y certbot
    elif command -v yum &> /dev/null; then
        sudo yum install -y certbot
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y certbot
    else
        echo "Unsupported OS. Please install Certbot manually."
        exit 1
    fi
fi

# Obtain certificate using DNS validation
echo "Obtaining SSL certificate using DNS validation..."
echo ""
echo "You will be prompted to add TXT records to your DNS."
echo "Example: _acme-challenge.cyberirtabletop.com -> [value provided]"
echo ""
read -p "Press Enter when ready to continue..."

certbot certonly \
    --manual \
    --preferred-challenges dns \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    -d "www.$DOMAIN"

# Set proper permissions
chmod 755 /etc/letsencrypt/live
chmod 755 /etc/letsencrypt/archive
chmod 644 /etc/letsencrypt/live/$DOMAIN/fullchain.pem
chmod 600 /etc/letsencrypt/live/$DOMAIN/privkey.pem

echo ""
echo "SSL certificate obtained successfully!"
echo "Certificate location: /etc/letsencrypt/live/$DOMAIN/"
echo ""
echo "Next steps:"
echo "1. Update docker-compose.prod.yml with your production environment variables"
echo "2. Start the production stack: docker-compose -f docker-compose.prod.yml up -d"
echo "3. Test certificate renewal: certbot renew --dry-run"

