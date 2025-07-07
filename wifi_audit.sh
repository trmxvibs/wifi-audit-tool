#!/bin/bash

echo "==== WiFi Auditing Tool ===="
echo "For Education & Authorized Testing Only!"

which iw > /dev/null 2>&1 || { echo "iw not found! Install with apt install iw"; exit 1; }
which airodump-ng > /dev/null 2>&1 || { echo "aircrack-ng not found! Install with apt install aircrack-ng"; exit 1; }

echo "Available interfaces:"
iw dev | grep Interface | awk '{print NR ")", $2}'

read -p "Select interface (name): " iface
if [[ -z "$iface" ]]; then
  echo "No interface selected. Exiting."
  exit 1
fi

echo "Putting $iface in monitor mode (requires root)..."
sudo ip link set $iface down
sudo iw $iface set monitor control
sudo ip link set $iface up

read -p "Start WiFi scan & capture? (y/n): " choice
if [[ "$choice" == "y" ]]; then
    sudo airodump-ng $iface
else
    echo "Aborting scan."
fi

echo "Remember: Use only on networks you own or have written permission to test!"