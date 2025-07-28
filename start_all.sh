#!/bin/bash

echo "🚀 Starting Stock Predictive Analytics Tracker..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   cd backend && pip install -r requirements.txt"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo "✅ Dependencies ready!"
echo ""
echo "🎯 Starting both servers..."
echo ""

# Start backend in background
echo "🔧 Starting Backend..."
./start_backend.sh &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting Frontend..."
./start_frontend.sh &
FRONTEND_PID=$!

echo ""
echo "🎉 Both servers are starting..."
echo "📍 Backend: http://127.0.0.1:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📚 API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user to stop
wait 