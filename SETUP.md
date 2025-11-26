# Quick Setup Guide

## If Startup Appears Stuck

The services are actually running! Here's what to check:

### 1. Verify Services Are Running

Check that all containers are up:
```bash
docker-compose -f docker-compose.dev.yml ps
```

You should see:
- `db-1` - Running
- `backend-1` - Running  
- `frontend-dev-1` - Running

### 2. Initialize Database (IMPORTANT!)

The database needs to be initialized before you can use the app:

```bash
# Run migrations
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# Seed initial data (creates admin user and sample scenario)
docker-compose -f docker-compose.dev.yml exec backend python seed_data.py
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

### 4. Login Credentials

After seeding data:
- Username: `admin`
- Password: `admin123`

### 5. If Frontend Can't Connect to Backend

Check the browser console for errors. The frontend should automatically proxy API requests through Vite.

If you see connection errors, verify:
- Backend is accessible at http://localhost:8001/docs
- Check browser console for CORS or network errors

### Troubleshooting

**Port conflicts:**
- If port 8001 is in use, change it in `docker-compose.dev.yml` (line 26)
- If port 5173 is in use, change it in `docker-compose.dev.yml` (line 44)

**Database connection issues:**
```bash
# Check database logs
docker-compose -f docker-compose.dev.yml logs db

# Restart services
docker-compose -f docker-compose.dev.yml restart
```

**Reset everything:**
```bash
# Stop and remove all containers and volumes
docker-compose -f docker-compose.dev.yml down -v

# Start fresh
docker-compose -f docker-compose.dev.yml up --build
```

