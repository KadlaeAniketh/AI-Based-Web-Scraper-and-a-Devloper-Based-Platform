#!/bin/bash
set -euo pipefail

# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    libfreetype6 \
    libharfbuzz0b \
    libjpeg62-turbo \
    libopenjp2-7 \
    libpng16-16 \
    libtiff5 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    poppler-utils  # Required for pdf2image

# Install Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
