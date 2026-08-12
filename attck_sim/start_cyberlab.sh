#!/bin/bash

echo "🚀 Starting CyberLab..."

cd "$(dirname "$0")"

# Check Docker
if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed!"
    exit 1
fi

# Start launcher
cd Launcher
docker-compose up -d

# Wait for backend
sleep 5

# Open UI
xdg-open http://localhost:5000 2>/dev/null || sensible-browser http://localhost:5000

echo "✅ CyberLab is ready!"
