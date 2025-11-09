#!/bin/bash

echo "🚨 WEB SECURITY LAB - FOR EDUCATIONAL PURPOSES ONLY 🚨"
echo "DO NOT DEPLOY TO INTERNET OR PRODUCTION ENVIRONMENTS"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python init_db.py

echo ""
echo "✅ Setup complete! Starting application..."
echo "📱 Access the lab at: http://localhost:5000"
echo "🔒 Current mode: $(grep 'MODE =' app.py | head -1 | cut -d'"' -f2)"
echo ""

# Run the application
python app.py