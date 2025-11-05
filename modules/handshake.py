import subprocess
import sys
from utils.helpers import colorful_print

def start(iface):
    """Starts the handshake capture process."""
    colorful_print("Starting handshake capture module...", "cyan")
    
    # Ask user for info from the scan (Option 1)
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
        '-w', output_file,  # Save to file
        iface
    ]

    colorful_print(f"Running: {' '.join(command)}", "yellow")
    colorful_print("Waiting for handshake... Press Ctrl+C to stop.", "yellow")
    
    try:
        subprocess.run(command)
        colorful_print(f"Capture saved to {output_file}-01.cap", "green")
    except subprocess.CalledProcessError as e:
        colorful_print(f"Error starting capture: {e}", "red")
    except KeyboardInterrupt:
        colorful_print(f"\nCapture stopped. File saved as {output_file}-01.cap", "green")
