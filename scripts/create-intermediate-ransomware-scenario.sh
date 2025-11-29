#!/bin/bash
# Script to create the intermediate ransomware scenario and generate artifacts
# Usage: ./scripts/create-intermediate-ransomware-scenario.sh

set -e

echo "=========================================="
echo "Creating Intermediate Ransomware Scenario"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.dev.yml" ] && [ ! -f "docker-compose.prod.yml" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Determine which docker-compose file to use
if [ -f "docker-compose.prod.yml" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    ENV_FILE="--env-file .env.production"
else
    COMPOSE_FILE="docker-compose.dev.yml"
    ENV_FILE=""
fi

echo "Step 1: Generating artifact files..."
docker-compose -f "$COMPOSE_FILE" $ENV_FILE exec -T backend python /app/generate_intermediate_ransomware_artifacts.py

if [ $? -ne 0 ]; then
    echo "❌ Error generating artifacts"
    exit 1
fi

echo ""
echo "Step 2: Creating scenario in database..."
docker-compose -f "$COMPOSE_FILE" $ENV_FILE exec -T backend python /app/create_intermediate_ransomware_scenario.py

if [ $? -ne 0 ]; then
    echo "❌ Error creating scenario"
    exit 1
fi

echo ""
echo "✅ Successfully created intermediate ransomware scenario!"
echo ""
echo "Scenario: 'Ransomware Attack: Corporate Network Compromise'"
echo "- 5 phases with artifact-driven decisions"
echo "- Detailed Defender/E5 security tool artifacts for Blue Team"
echo "- Realistic Red Team reconnaissance and tool outputs"
echo "- Intermediate difficulty level"
echo ""
echo "You can now create a game using this scenario from the GM console."

