#!/bin/bash

# Update package lists
sudo apt-get update

# Install VLC
sudo apt-get install -y vlc

# Install Python dependencies
pip install -r requirements.txt

# Run the Python script
python3 main.py
