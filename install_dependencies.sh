#!/bin/bash

source .venv/bin/activate

pip install -r requirements.txt

pip show requests

echo "Dependencies installed successfully!"