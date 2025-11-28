#!/bin/bash
# Pre-flight check script for SSL certificate setup
# Run this before setup-ssl.sh to diagnose issues

echo "SSL Certificate Setup Pre-Flight Check"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Warning: Not running as root. Some checks may fail."
    echo ""
fi

# Check DNS
echo "1. Checking DNS resolution..."
DOMAIN="cyberirtabletop.com"
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
DNS_IP=$(dig +short $DOMAIN | tail -n1)

echo "   Your EC2 Public IP: $PUBLIC_IP"
echo "   DNS resolves to:    $DNS_IP"

if [ "$PUBLIC_IP" = "$DNS_IP" ]; then
    echo "   ✓ DNS is correctly pointing to this server"
else
    echo "   ✗ DNS mismatch! Domain points to $DNS_IP but this server is $PUBLIC_IP"
    echo "   Please update your DNS A record to point to $PUBLIC_IP"
fi
echo ""

# Check port 80 availability
echo "2. Checking port 80..."
if lsof -i :80 > /dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ':80 '; then
    echo "   ⚠️  Port 80 is in use:"
    lsof -i :80 2>/dev/null || netstat -tuln | grep ':80 '
    echo "   You may need to stop these services before running Certbot"
else
    echo "   ✓ Port 80 is available"
fi
echo ""

# Check firewall
echo "3. Checking firewall..."
if command -v firewall-cmd &> /dev/null; then
    if systemctl is-active --quiet firewalld; then
        echo "   firewalld is active"
        if firewall-cmd --list-ports 2>/dev/null | grep -q "80/tcp"; then
            echo "   ✓ Port 80 is allowed in firewalld"
        else
            echo "   ✗ Port 80 is NOT allowed in firewalld"
            echo "   Run: sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload"
        fi
    else
        echo "   firewalld is not active"
    fi
fi

if command -v iptables &> /dev/null; then
    if iptables -L INPUT -n 2>/dev/null | grep -q "REJECT.*80\|DROP.*80"; then
        echo "   ⚠️  iptables may be blocking port 80"
    fi
fi
echo ""

# Check Security Group (requires AWS CLI)
echo "4. Checking EC2 Security Group..."
if command -v aws &> /dev/null; then
    INSTANCE_ID=$(ec2-metadata --instance-id 2>/dev/null | cut -d " " -f 2)
    if [ -n "$INSTANCE_ID" ]; then
        SG_ID=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' --output text 2>/dev/null)
        if [ -n "$SG_ID" ]; then
            PORT_80_OPEN=$(aws ec2 describe-security-groups --group-ids $SG_ID --query 'SecurityGroups[0].IpPermissions[?FromPort==`80`]' --output text 2>/dev/null)
            if [ -n "$PORT_80_OPEN" ]; then
                echo "   ✓ Port 80 is open in Security Group $SG_ID"
            else
                echo "   ✗ Port 80 is NOT open in Security Group $SG_ID"
                echo "   Please add an inbound rule: Type=HTTP, Port=80, Source=0.0.0.0/0"
            fi
        fi
    fi
else
    echo "   ⚠️  AWS CLI not installed - cannot check Security Group automatically"
    echo "   Please verify manually in AWS Console that port 80 is open"
fi
echo ""

# Test external connectivity
echo "5. Testing external connectivity to port 80..."
if command -v nc &> /dev/null; then
    if timeout 5 nc -z localhost 80 2>/dev/null; then
        echo "   ✓ Port 80 is listening locally"
    else
        echo "   ⚠️  Port 80 is not listening locally (this is OK if nothing is running)"
    fi
else
    echo "   ⚠️  netcat not installed - skipping local port test"
fi
echo ""

# Check Certbot installation
echo "6. Checking Certbot..."
if command -v certbot &> /dev/null; then
    echo "   ✓ Certbot is installed: $(certbot --version)"
else
    echo "   ✗ Certbot is not installed"
    echo "   Install with: sudo dnf install -y certbot (Amazon Linux 2023)"
fi
echo ""

echo "======================================"
echo "Pre-flight check complete!"
echo ""
echo "If all checks pass, you can run: sudo ./scripts/setup-ssl.sh"
echo ""

