#!/bin/bash

# Create and activate a virtual environment
python3 -m venv video_loop_env
source video_loop_env/bin/activate

# Install required packages
pip install -r requirements2.txt

# Run the Python script
python main.py

# Deactivate the virtual environment
deactivate