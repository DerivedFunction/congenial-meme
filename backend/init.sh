#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "✅ Virtual environment created."
else
  echo "🔁 Virtual environment already exists."
fi

# Activate the virtual environment
source venv/Scripts/activate

# Install requirements
pip install -r requirements.txt
echo "📦 Dependencies installed."
chmod +x *.sh
echo "*.sh files made executable."