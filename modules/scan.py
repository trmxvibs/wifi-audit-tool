import subprocess
import sys
from utils.helpers import colorful_print

def start(iface):
    colorful_print(f"Starting network scan on {iface}...", "cyan")
    colorful_print("Press Ctrl+C to stop scanning and return to menu.", "yellow")
    try:
        subprocess.run(['airodump-ng', iface])
    except subprocess.CalledProcessError as e:
        colorful_print(f"Error starting scan: {e}", "red")
    except KeyboardInterrupt:
        colorful_print("\nScan stopped. Returning to main menu.", "green")
