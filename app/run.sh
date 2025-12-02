#!/bin/bash

# Simple script to run the Ikon News Scraper web application

echo "Starting Ikon News Scraper Web Application..."
echo "----------------------------------------"
echo ""

# Get the script's directory (app folder)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Flask is not installed. Installing dependencies..."
    pip3 install --user -r "$PARENT_DIR/requirements.txt" || {
        echo "Failed to install dependencies. Please run:"
        echo "pip3 install --user -r requirements.txt"
        exit 1
    }
fi

echo "Starting Flask server from app directory..."
echo "Scraper will run from: $PARENT_DIR"
echo "Open your browser and go to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$SCRIPT_DIR"
python3 app.py
