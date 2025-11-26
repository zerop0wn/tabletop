# EC2 Setup Guide

## Required Configuration Changes

### 1. Get Your EC2 Public IP or Domain
```bash
# Get your public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Or if you have a domain, use that instead
```

### 2. Update Backend CORS Settings

Edit `backend/app/main.py` and update the CORS origins:

```python
# Replace this line (around line 15):
allow_origins=["http://localhost:5173", "http://localhost:3000"],

# With (replace YOUR_EC2_IP with your actual IP or domain):
allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
    "http://YOUR_EC2_IP:5173",
    "http://YOUR_EC2_IP",
    "https://YOUR_EC2_IP",  # If using HTTPS
    "https://yourdomain.com",  # If using a domain
],
```

### 3. Update Frontend API Configuration

The frontend uses a proxy in development. For production access, you have two options:

**Option A: Update Vite Proxy (for development)**
Edit `frontend/vite.config.ts` - the proxy should work as-is since it uses Docker networking, but if accessing from outside, you may need to update `frontend/src/api/client.ts`:

**Option B: Update API Client (recommended for EC2)**
Edit `frontend/src/api/client.ts`:

```typescript
// Replace:
const API_BASE_URL = '/api'

// With (replace YOUR_EC2_IP with your actual IP):
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'http://YOUR_EC2_IP:8001/api'  // Use public IP for production
  : '/api'  // Use proxy for local development
```

### 4. Update Docker Compose Environment

Edit `docker-compose.dev.yml` and update the frontend environment:

```yaml
frontend-dev:
  # ... existing config ...
  environment:
    - VITE_API_URL=http://YOUR_EC2_IP:8001/api  # Update this
```

### 5. Security Group Configuration

Make sure your EC2 security group allows:
- **Port 5173** (TCP) - Frontend dev server
- **Port 8001** (TCP) - Backend API
- **Port 5432** (TCP) - PostgreSQL (optional, only if accessing from outside)

### 6. Restart Services

After making changes:
```bash
cd /opt/tabletop
sudo docker-compose -f docker-compose.dev.yml restart backend frontend-dev
```

## Quick Setup Script

Replace `YOUR_EC2_IP` with your actual IP:

```bash
export EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "Your EC2 IP: $EC2_IP"

# Update backend CORS
sed -i "s|allow_origins=\[\"http://localhost:5173\", \"http://localhost:3000\"\]|allow_origins=[\"http://localhost:5173\", \"http://localhost:3000\", \"http://$EC2_IP:5173\", \"http://$EC2_IP\"]|g" backend/app/main.py

# Update docker-compose environment
sed -i "s|VITE_API_URL=http://backend:8000|VITE_API_URL=http://$EC2_IP:8001/api|g" docker-compose.dev.yml

# Restart services
sudo docker-compose -f docker-compose.dev.yml restart backend frontend-dev
```

## Access URLs

- **Frontend**: `http://YOUR_EC2_IP:5173`
- **Backend API**: `http://YOUR_EC2_IP:8001`
- **API Health Check**: `http://YOUR_EC2_IP:8001/health`

