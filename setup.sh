#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

rm dmi_util.cmd
chmod +x dmi_util.sh
mv dmi_util.sh dmi_util.cmd

# Step 1: Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y libeccodes0 libeccodes-dev
sudo apt-get install python3-venv

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
