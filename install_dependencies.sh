#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Verify that requests is installed
pip show requests

echo "Dependencies installed successfully!"