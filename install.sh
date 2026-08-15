#!/bin/bash
set -e

echo "Installing dependencies for Kali Linux..."

sudo apt-get update
sudo apt-get install -y python3-pip python3-venv aircrack-ng git

# Modern Kali/Debian (PEP 668) block system-wide pip installs.
# Using --break-system-packages keeps this a simple root-run tool
# instead of forcing a venv (the tool needs root anyway for aircrack-ng).
pip3 install -r requirements.txt --break-system-packages

echo "Done! Run: sudo python3 wifi_audit.py"
