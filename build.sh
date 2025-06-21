#!/bin/bash
set -euo pipefail

# Install Python dependencies
pip install -r requirements.txt

# Install Chromium for Selenium (required for headless browsing)
sudo apt-get update
sudo apt-get install -y chromium-browser
