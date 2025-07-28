#!/bin/bash

echo "🚀 Setting up Stock Predictive Analytics Tracker..."
echo ""

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment and install backend dependencies
echo "🔧 Installing backend dependencies..."
source venv/bin/activate
cd backend && pip install -r requirements.txt && cd ..

# Install frontend dependencies
echo "🎨 Installing frontend dependencies..."
cd frontend && npm install && cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 To start the application, run:"
echo "   ./start_all.sh"
echo ""
echo "Or start individually:"
echo "   ./start_backend.sh  # Backend only"
echo "   ./start_frontend.sh # Frontend only"
echo ""
echo "📍 Backend: http://127.0.0.1:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📚 API Docs: http://127.0.0.1:8000/docs" 