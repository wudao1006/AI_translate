#!/bin/bash
# Quick start script for AI Translation Assistant (Linux/Mac)

echo "========================================"
echo "AI Translation Assistant - Quick Start"
echo "========================================"
echo ""

# Check if .env exists in backend
if [ ! -f backend/.env ]; then
    echo "[WARNING] backend/.env not found!"
    echo "Please copy backend/.env.example to backend/.env and configure your API keys."
    echo ""
    exit 1
fi

echo "[1/3] Starting backend server..."
echo ""

PYTHON_EXE="./myenv/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
    echo "[WARNING] myenv not found. Falling back to system Python."
    echo "          Consider running: source myenv/bin/activate"
    echo ""
    PYTHON_EXE="python"
fi

cd backend
$PYTHON_EXE app.py &
BACKEND_PID=$!
cd ..

echo "[2/3] Backend started at http://localhost:8000"
echo "Backend PID: $BACKEND_PID"
echo ""

sleep 3

echo "[3/3] You can now start the Flutter app:"
echo "   cd flutter_app"
echo "   flutter run"
echo ""

echo "========================================"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "To stop backend: kill $BACKEND_PID"
echo ""
