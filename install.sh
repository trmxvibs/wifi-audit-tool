#!/bin/bash

echo "Installing dependencies for Kali Linux..."

sudo apt-get update


sudo apt-get install -y python3-pip aircrack-ng git


pip3 install -r requirements.txt

echo "Done! Run: sudo python3 wifi_audit.py"
