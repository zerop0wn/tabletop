#!/bin/bash
# Wrapper script for docker-compose.prod.yml that loads .env.production

set -e

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    echo "Please create it from env.production.template"
    exit 1
fi

# Export variables from .env.production
export $(cat .env.production | grep -v '^#' | grep -v '^$' | xargs)

# Run docker-compose with the exported environment
docker-compose --env-file .env.production -f docker-compose.prod.yml "$@"

