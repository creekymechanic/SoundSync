#!/bin/bash

# Create and activate a virtual environment
python3 -m venv audio_monitor_env
source audio_monitor_env/bin/activate

# Install required packages
pip install -r requirements2.txt

# Run the Python script
python main.py

# Deactivate the virtual environment
deactivate