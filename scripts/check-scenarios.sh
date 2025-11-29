#!/bin/bash
# Check what scenarios exist in the database

set -e

echo "Checking Scenarios in Database"
echo "==============================="
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
    exit 1
fi

echo "Querying database for scenarios..."
echo ""

# Query all scenarios
docker exec "$BACKEND_CONTAINER" python -c "
from app.database import SessionLocal
from app.models import Scenario

db = SessionLocal()
try:
    scenarios = db.query(Scenario).all()
    print(f'Found {len(scenarios)} scenario(s):')
    print('')
    for scenario in scenarios:
        print(f'  ID: {scenario.id}')
        print(f'  Name: {scenario.name}')
        print(f'  Description: {scenario.description[:80] if scenario.description else \"None\"}...')
        print(f'  Phases: {len(scenario.phases)}')
        print('')
    
    # Check specifically for tutorial
    tutorial = db.query(Scenario).filter(Scenario.name == 'Tutorial: Basic Security Incident').first()
    if tutorial:
        print('✓ Tutorial scenario EXISTS in database')
        print(f'  Tutorial ID: {tutorial.id}')
        print(f'  Tutorial Phases: {len(tutorial.phases)}')
    else:
        print('❌ Tutorial scenario NOT FOUND in database')
        print('')
        print('Checking for similar names...')
        similar = db.query(Scenario).filter(Scenario.name.like('%Tutorial%')).all()
        if similar:
            for s in similar:
                print(f'  Found: {s.name} (ID: {s.id})')
        else:
            print('  No scenarios with \"Tutorial\" in name found')
finally:
    db.close()
"

echo ""
echo "======================================"

