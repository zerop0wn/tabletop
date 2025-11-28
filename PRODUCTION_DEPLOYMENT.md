# Production Deployment Guide for cyberirtabletop.com

This guide walks you through deploying the Cyber Tabletop application to production with HTTPS/SSL support.

## Prerequisites

1. **EC2 Instance** running Linux (Ubuntu 20.04+ or Amazon Linux 2+)
2. **Domain Name** `cyberirtabletop.com` pointing to your EC2 instance's public IP
3. **Docker** and **Docker Compose** installed
4. **Ports Open**: 22 (SSH), 80 (HTTP), 443 (HTTPS)

## Step 1: DNS Configuration

1. Log into your domain registrar
2. Add/Update A records:
   - `cyberirtabletop.com` → `YOUR_EC2_PUBLIC_IP`
   - `www.cyberirtabletop.com` → `YOUR_EC2_PUBLIC_IP` (optional)
3. Wait for DNS propagation (can take up to 48 hours, usually 1-2 hours)

Verify DNS:
```bash
dig cyberirtabletop.com
# or
nslookup cyberirtabletop.com
```

## Step 2: Clone and Prepare Repository

```bash
# SSH into your EC2 instance
ssh ec2-user@YOUR_EC2_IP

# Clone the repository
git clone https://github.com/zerop0wn/tabletop.git
cd tabletop

# Create production environment file
cp env.production.template .env.production
nano .env.production  # Edit with your values
```

## Step 3: Configure Environment Variables

Edit `.env.production` with secure values:

```bash
# Generate a strong password for PostgreSQL
openssl rand -base64 32

# Generate a strong JWT secret
openssl rand -base64 64
```

Update `.env.production`:
- `POSTGRES_PASSWORD`: Strong database password
- `JWT_SECRET_KEY`: Strong random secret (min 32 characters)
- `CORS_ORIGINS`: `https://cyberirtabletop.com,https://www.cyberirtabletop.com`

## Step 4: Set Up SSL Certificates

### Option A: Automated Setup (Recommended)

```bash
# Make script executable
chmod +x scripts/setup-ssl.sh

# Run SSL setup (requires sudo)
sudo ./scripts/setup-ssl.sh
```

**Note**: You may need to update the email address in `scripts/setup-ssl.sh` before running.

### Option B: Manual Setup

```bash
# Install Certbot
sudo yum install certbot  # Amazon Linux
# or
sudo apt-get update && sudo apt-get install certbot  # Ubuntu

# Obtain certificate
sudo certbot certonly --standalone \
  --non-interactive \
  --agree-tos \
  --email admin@cyberirtabletop.com \
  -d cyberirtabletop.com \
  -d www.cyberirtabletop.com
```

## Step 5: Set Up Certificate Auto-Renewal

Let's Encrypt certificates expire every 90 days. Set up automatic renewal:

```bash
# Make renewal script executable
chmod +x scripts/renew-cert.sh

# Add to crontab (runs daily at midnight)
sudo crontab -e

# Add this line:
0 0 * * * /home/ec2-user/tabletop/scripts/renew-cert.sh >> /var/log/certbot-renewal.log 2>&1
```

Test renewal:
```bash
sudo certbot renew --dry-run
```

## Step 6: Update Security Group

Ensure your EC2 Security Group allows:
- **Port 22** (SSH) - from your IP only
- **Port 80** (HTTP) - from anywhere (for Let's Encrypt)
- **Port 443** (HTTPS) - from anywhere

## Step 7: Build and Start Production Stack

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Step 8: Initialize Database

```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Seed initial data (creates admin user and scenarios)
docker-compose -f docker-compose.prod.yml exec backend python seed_data.py
```

## Step 9: Verify Deployment

1. **Check HTTPS**: Visit `https://cyberirtabletop.com`
   - Should redirect from HTTP automatically
   - SSL certificate should be valid

2. **Test Login**: 
   - Default credentials: `admin` / `admin123`
   - **IMPORTANT**: Change password immediately after first login

3. **Check API**: Visit `https://cyberirtabletop.com/api/health`
   - Should return: `{"status":"healthy"}`

4. **Test Frontend**: All pages should load correctly

## Step 10: Post-Deployment Security

### Change Default Admin Password

1. Log in as admin
2. Go to Game Manager settings
3. Change password to a strong password

### Firewall Configuration

Ensure only necessary ports are open:
```bash
# Check current firewall rules
sudo iptables -L -n

# Or if using firewalld
sudo firewall-cmd --list-all
```

### Database Security

- Database is only accessible from within Docker network
- No external port exposure
- Strong password set in `.env.production`

## Monitoring and Maintenance

### Check Service Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Restart Services

```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Backup Database

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U cybertabletop cybertabletop > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U cybertabletop cybertabletop < backup_file.sql
```

## Troubleshooting

### SSL Certificate Issues

**Problem**: Certificate not found
```bash
# Check certificate location
ls -la /etc/letsencrypt/live/cyberirtabletop.com/

# Verify certificate
sudo certbot certificates
```

**Problem**: Certificate renewal fails
- Ensure port 80 is accessible
- Check firewall rules
- Verify DNS still points to correct IP

### Nginx Issues

**Problem**: 502 Bad Gateway
```bash
# Check if backend is running
docker-compose -f docker-compose.prod.yml ps backend

# Check backend logs
docker-compose -f docker-compose.prod.yml logs backend
```

**Problem**: Frontend not loading
```bash
# Check frontend container
docker-compose -f docker-compose.prod.yml logs frontend

# Verify nginx config
docker-compose -f docker-compose.prod.yml exec frontend nginx -t
```

### CORS Issues

If you see CORS errors:
1. Check `.env.production` has correct `CORS_ORIGINS`
2. Restart backend: `docker-compose -f docker-compose.prod.yml restart backend`
3. Check browser console for exact error

## Production Checklist

- [ ] DNS configured and propagated
- [ ] SSL certificates obtained
- [ ] Environment variables configured
- [ ] Strong passwords set
- [ ] Security group configured
- [ ] Services running
- [ ] Database initialized
- [ ] HTTPS working
- [ ] Admin password changed
- [ ] Certificate auto-renewal configured
- [ ] Backups configured
- [ ] Monitoring set up

## Support

For issues or questions:
1. Check logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify configuration files
3. Check SSL certificate status: `sudo certbot certificates`
4. Test connectivity: `curl -I https://cyberirtabletop.com`

