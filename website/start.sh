#!/bin/bash

echo "🚀 Starting BaxBench Website..."

# Start backend server
echo "Starting backend server on port 8000..."
python3 server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start frontend on different port
echo "Starting frontend on port 3001..."
PORT=3001 npm start &
FRONTEND_PID=$!

echo "✅ Website running!"
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait