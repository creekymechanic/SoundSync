#!/bin/bash

# Update package lists
sudo apt-get update

# Install VLC
sudo apt-get install -y vlc

# Install virtualenv if not installed
pip install --user virtualenv

# Create a virtual environment named 'venv' in the current directory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies in the virtual environment
pip install -r requirements.txt

# Run the Python script inside the virtual environment
python3 main.py

# Deactivate the virtual environment after the script finishes
deactivate
