#!/bin/bash
set -euo pipefail

# Install system dependencies for Chromium
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver

# Set up Python environment
python -m pip install --upgrade pip
pip install -r requirements.txt

# Fix any potential ChromaDB issues
pip install --force-reinstall -U numpy
