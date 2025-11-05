import sys
import subprocess
import os
import re 
from utils.helpers import colorful_print
from modules import scan, handshake, report

def check_kali_dependencies():
    """"""
    colorful_print("Checking dependencies for Kali Linux...", "yellow")
    
    if os.geteuid() != 0:
        colorful_print("Error: This tool must be run as root (use sudo).", "red")
        sys.exit(1)

    tools = ["airodump-ng", "aireplay-ng", "iw", "ip"]
    missing_tools = []
    
    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode != 0:
            missing_tools.append(tool)
            
    if missing_tools:
        colorful_print(f"Error: Missing required tools: {', '.join(missing_tools)}", "red")
        sys.exit(1)
    
    colorful_print("All dependencies are satisfied.", "green")

def select_interface():
    """ """
    colorful_print("Detecting wireless interfaces...", "cyan")
    try:
       
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
    """  """
    colorful_print(f"Putting {iface} into monitor mode...", "yellow")
    try:
        subprocess.run(['ip', 'link', 'set', iface, 'down'], check=True)
        subprocess.run(['iw', iface, 'set', 'monitor', 'control'], check=True)
        subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)
        colorful_print(f"{iface} is now in monitor mode.", "green")
    except subprocess.CalledProcessError as e:
        colorful_print(f"Failed to set monitor mode: {e}", "red")
        colorful_print("Try running 'rfkill unblock wifi'", "yellow")
        sys.exit(1)

def main_menu():
    colorful_print("\n==== WiFi Auditing Tool (Kali Edition) ====", "cyan")
    print("1) Scan WiFi Networks")
    print("2) Capture Handshake")
    print("3) Vulnerability Report / Crack")
    print("4) Scan History")
    print("5) Guidelines & Help")
    print("6) Exit")
    choice = input("Select option: ")
    return choice

def run():
    check_kali_dependencies()
    iface = select_interface()
    set_monitor_mode(iface)
    
    while True:
        choice = main_menu()
        if choice == "1":
            scan.start(iface)
        elif choice == "2":
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
            colorful_print("Disabling monitor mode and exiting...", "green")
            subprocess.run(['ip', 'link', 'set', iface, 'down'], check=True)
            subprocess.run(['iw', iface, 'set', 'type', 'managed'], check=True)
            subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)
            sys.exit(0)
        else:
            colorful_print("Invalid choice!", "red")

if __name__ == '__main__':
    run()
