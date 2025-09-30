#!/bin/bash

# Start script for Exoplanet AI Discovery Platform

echo "🌌 Starting Exoplanet AI Discovery Platform..."

# Function to cleanup processes
cleanup() {
    echo "🛑 Shutting down services..."
    kill 0
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start backend API server
echo "🚀 Starting FastAPI backend..."
cd /app/backend
python ultra_simple_api.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start nginx for frontend
echo "🌐 Starting nginx for static frontend..."
nginx -g "daemon off;" &
NGINX_PID=$!

# Wait for both processes
wait $BACKEND_PID $NGINX_PID
