#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment (from project root)
source venv/bin/activate

# Set Python path to include the backend directory
export PYTHONPATH="$SCRIPT_DIR/backend:$PYTHONPATH"

# Start the backend server
echo "🚀 Starting Stock Analytics Backend..."
echo "📍 Server will be available at: http://127.0.0.1:8000"
echo "📚 API Documentation: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 