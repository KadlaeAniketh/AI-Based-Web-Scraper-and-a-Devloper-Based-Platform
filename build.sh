#!/bin/bash
set -euo pipefail

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Chromium for Selenium
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver
