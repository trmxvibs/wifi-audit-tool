#!/bin/bash
echo "Installing dependencies..."
pkg install -y python aircrack-ng git
pip install -r requirements.txt
echo "Done! Run: python wifi_audit.py"