#!/bin/bash

echo "🛑 Stopping Stock Analytics Docker containers..."
echo ""

# Stop and remove containers
docker compose down

echo "✅ Containers stopped and removed!"
echo ""

# Optional: Remove images (uncomment if you want to clean up images too)
# echo "🧹 Removing Docker images..."
# docker compose down --rmi all
# echo "✅ Images removed!"

echo "🎯 To start again, run: ./docker-start.sh" 