import sys
import subprocess
import os
import re
from utils.helpers import colorful_print
from modules import scan, handshake, report

def check_kali_dependencies():
    """Checks dependencies specifically for Kali Linux."""
    colorful_print("Checking dependencies for Kali Linux...", "yellow")
    
    # 1. Check for root privileges (required for aircrack-ng)
    if os.geteuid() != 0:
        colorful_print("Error: This tool must be run as root (use sudo).", "red")
        colorful_print("Please run using: 'sudo python3 wifi_audit.py'", "red")
        sys.exit(1)

    # 2. Check for core tools
    tools = ["airodump-ng", "aireplay-ng", "iw", "ip"]
    missing_tools = []
    
    for tool in tools:
        # Use subprocess.run to check if 'which' command succeeds
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode != 0:
            missing_tools.append(tool)
            
    if missing_tools:
        colorful_print(f"Error: Missing required tools: {', '.join(missing_tools)}", "red")
        colorful_print(f"Please install them using: sudo apt-get install <package_name>", "red")
        colorful_print("Common packages: 'aircrack-ng' (for airodump/aireplay), 'iw', 'iproute2' (for ip)", "yellow")
        sys.exit(1)
    
    colorful_print("All dependencies are satisfied. Tool is ready.", "green")

def select_interface():
    """Lets the user select a wireless interface."""
    colorful_print("Detecting wireless interfaces...", "cyan")
    try:
        # List interfaces using 'iw dev'
        result = subprocess.run(['iw', 'dev'], capture_output=True, text=True, check=True)
        interfaces = re.findall(r'Interface\s+(\w+)', result.stdout)
        
        if not interfaces:
            colorful_print("No wireless interfaces found. Exiting.", "red")
            sys.exit(1)
            
        print("Available interfaces:")
        for i, iface in enumerate(interfaces, 1):
            print(f"{i}) {iface}")
            
        choice = input("Select interface to use (number): ")
        selected_iface = interfaces[int(choice) - 1]
        return selected_iface
        
    except Exception as e:
        colorful_print(f"Error detecting interfaces: {e}", "red")
        sys.exit(1)

def set_monitor_mode(iface):
    """Sets the selected interface into monitor mode."""
    colorful_print(f"Putting {iface} into monitor mode...", "yellow")
    try:
        # Use ip and iw commands to set monitor mode
        subprocess.run(['ip', 'link', 'set', iface, 'down'], check=True)
        subprocess.run(['iw', iface, 'set', 'monitor', 'control'], check=True)
        subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)
        colorful_print(f"{iface} is now in monitor mode.", "green")
    except subprocess.CalledProcessError as e:
        colorful_print(f"Failed to set monitor mode: {e}", "red")
        colorful_print("Try running 'rfkill unblock wifi' and try again.", "yellow")
        sys.exit(1)

def main_menu():
    """Displays the main menu and returns user's choice."""
    colorful_print("\n==== WiFi Auditing Tool (Kali Edition) ====", "cyan")
    print("1) Scan WiFi Networks")
    print("2) Capture Handshake")
    print("3) Vulnerability Report / Crack")
    print("4) Scan History")
    print("5) Guidelines & Help")
    print("6) Exit")
    choice = input("Select option: ")
    return choice

def stop_monitor_mode(iface):
    """Reverts interface back to managed mode."""
    colorful_print(f"Reverting {iface} to managed mode...", "yellow")
    try:
        subprocess.run(['ip', 'link', 'set', iface, 'down'], check=True)
        subprocess.run(['iw', iface, 'set', 'type', 'managed'], check=True)
        subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)
        colorful_print("Interface is back in managed mode.", "green")
    except subprocess.CalledProcessError as e:
        colorful_print(f"Warning: Failed to reset interface {iface}: {e}", "red")

def run():
    """Main execution flow."""
    check_kali_dependencies()
    iface = select_interface()
    set_monitor_mode(iface)
    
    try:
        while True:
            choice = main_menu()
            if choice == "1":
                # Pass the interface name to the scan function
                scan.start(iface)
            elif choice == "2":
                # Pass the interface name to the handshake function
                handshake.start(iface)
            elif choice == "3":
                report.show()
            elif choice == "4":
                report.history()
            elif choice == "5":
                try:
                    with open("README.md") as f:
                        print(f.read())
                except FileNotFoundError:
                    colorful_print("README.md file not found.", "red")
            elif choice == "6":
                break # Exit loop to clean up
            else:
                colorful_print("Invalid choice!", "red")
                
    except KeyboardInterrupt:
        print("\nExiting due to user request (Ctrl+C).")
    finally:
        # This will run whether exiting normally (option 6) or via Ctrl+C
        stop_monitor_mode(iface)
        colorful_print("Thank you for using WiFi Auditing Tool!", "green")
        sys.exit(0)

if __name__ == '__main__':
    run()
