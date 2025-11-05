import subprocess
import sys
from utils.helpers import colorful_print

def start(iface):
    colorful_print("Starting handshake capture module...", "cyan")
    
    bssid = input("Enter Target BSSID (MAC Address): ")
    channel = input("Enter Target Channel: ")
    output_file = input("Enter output filename (e.g., 'handshake_capture'): ")

    if not bssid or not channel or not output_file:
        colorful_print("All fields are required. Aborting.", "red")
        return

    command = [
        'airodump-ng',
        '--bssid', bssid,
        '--channel', channel,
        '-w', output_file,  
        iface
    ]

    colorful_print(f"Running: {' '.join(command)}", "yellow")
    colorful_print("Waiting for handshake... Press Ctrl+C to stop.", "yellow")
    
    try:
        subprocess.run(command)
        colorful_print(f"Capture saved to {output_file}.cap", "green")
    except subprocess.CalledProcessError as e:
        colorful_print(f"Error starting capture: {e}", "red")
    except KeyboardInterrupt:
        colorful_print(f"\nCapture stopped. File saved as {output_file}.cap", "green")
