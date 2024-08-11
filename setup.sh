#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Step 1: Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y libeccodes0 libeccodes-dev

# Step 2: Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Step 3: Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 4: Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
