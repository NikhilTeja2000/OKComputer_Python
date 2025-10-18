#!/bin/bash

echo "=========================================="
echo "Personalized Diet Analytics Dashboard"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import dash" 2>/dev/null; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

echo "Starting dashboard..."
echo "Dashboard will be available at: http://localhost:8050"
echo "Press Ctrl+C to stop"
echo "=========================================="

python dashboard_app.py