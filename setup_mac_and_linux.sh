#!/bin/bash

echo "Initializing NASA Terminal Dashboard Unix Deployment..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in system PATH."
    exit 1
fi

echo "Installing required package arrays from specifications..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Environment installation complete. Launching terminal interface..."
    sleep 2
    python3 nasa.py
else
    echo "Deployment failed during dependency package installation."
    exit 1
fi