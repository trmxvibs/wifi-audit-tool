import subprocess
import sys
from utils.helpers import colorful_print

def start(iface):
    """Starts the airodump-ng scan."""
    colorful_print(f"Starting network scan on {iface}...", "cyan")
    colorful_print("Press Ctrl+C to stop scanning and return to menu.", "yellow")
    try:
        # Run airodump-ng directly on the interface
        subprocess.run(['airodump-ng', iface])
    except subprocess.CalledProcessError as e:
        colorful_print(f"Error starting scan: {e}", "red")
    except KeyboardInterrupt:
        # When user presses Ctrl+C, return gracefully
        colorful_print("\nScan stopped. Returning to main menu.", "green")
