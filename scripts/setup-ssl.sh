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
    if command -v dnf &> /dev/null; then
        # Amazon Linux 2023, Fedora, RHEL 9+
        sudo dnf install -y certbot
    elif command -v yum &> /dev/null; then
        # Amazon Linux 2, CentOS 7, RHEL 7/8
        sudo yum install -y certbot
    elif command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y certbot
    else
        echo "Unsupported OS. Please install Certbot manually."
        echo "For Amazon Linux 2023, try: sudo dnf install -y certbot"
        exit 1
    fi
fi

# Create directory for ACME challenges
mkdir -p /var/www/certbot

# Check if port 80 is in use
if lsof -i :80 > /dev/null 2>&1 || netstat -tuln | grep -q ':80 '; then
    echo "Warning: Port 80 appears to be in use. Checking what's using it..."
    lsof -i :80 || netstat -tuln | grep ':80 '
    echo ""
    echo "Please stop any services using port 80 before continuing."
    echo "Common services: nginx, apache, docker containers"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to stop..."
fi

# Stop any running web server temporarily (if needed)
systemctl stop nginx 2>/dev/null || true
systemctl stop httpd 2>/dev/null || true
systemctl stop apache2 2>/dev/null || true

# Stop any Docker containers that might be using port 80
docker ps --format "{{.Names}}" | grep -E "(frontend|nginx|web)" | xargs -r docker stop 2>/dev/null || true

# Check firewall status
if command -v firewall-cmd &> /dev/null; then
    echo "Checking firewalld..."
    if systemctl is-active --quiet firewalld; then
        echo "Opening port 80 in firewalld..."
        firewall-cmd --permanent --add-service=http
        firewall-cmd --reload
    fi
fi

# Check iptables
if iptables -L -n | grep -q "REJECT.*80"; then
    echo "Warning: iptables may be blocking port 80"
    echo "You may need to run: sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT"
fi

# Obtain certificate using standalone mode
echo "Obtaining SSL certificate..."
echo "Make sure port 80 is open in your EC2 Security Group and DNS points to this server!"
echo ""
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

