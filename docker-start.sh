#!/bin/bash

echo "🐳 Starting Stock Analytics with Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please ensure Docker Desktop is running."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker environment ready!"
echo ""

# Build and start services
echo "🔨 Building and starting services..."
docker compose up --build -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "🎉 Stock Analytics is now running!"
    echo ""
    echo "📍 Frontend: http://localhost:3000"
    echo "📍 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "🔧 To view logs: docker compose logs -f"
    echo "🛑 To stop: docker compose down"
    echo ""
else
    echo "❌ Services failed to start. Check logs with: docker compose logs"
    exit 1
fi 