import sys
import subprocess 
import os        
from utils.helpers import colorful_print
from modules import scan, handshake, report

def check_kali_dependencies():
   
    colorful_print("Checking dependencies for Kali Linux...", "yellow")
    
   
    if os.geteuid() != 0:
        colorful_print("Error: This tool must be run as root (use sudo).", "red")
        colorful_print(" 'sudo python3 wifi_audit.py' , "red")
        sys.exit(1)

    tools = ["airodump-ng", "aireplay-ng", "iw", "ip"]
    missing_tools = []
    
    for tool in tools:
      
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode != 0:
            missing_tools.append(tool)
            
    if missing_tools:
        colorful_print(f"Error: Missing required tools: {', '.join(missing_tools)}", "red")
        colorful_print(f"Please install them using: sudo apt-get install <package_name>", "red")
        colorful_print("Common packages: 'aircrack-ng' (for airodump/aireplay), 'iw', 'iproute2' (for ip)", "yellow")
        sys.exit(1)
    
    colorful_print("All dependencies are satisfied. Tool is ready.", "green")

def main_menu():
    colorful_print("==== WiFi Auditing Tool (Kali Edition) ====", "cyan")
    print("1) Scan WiFi Networks")
    print("2) Capture Handshake")
    print("3) Vulnerability Report")
    print("4) Scan History")
    print("5) Guidelines & Help")
    print("6) Exit")
    choice = input("Select option: ")
    return choice

def run():
    check_kali_dependencies() 
    while True:
        choice = main_menu()
        if choice == "1":
            scan.start()
        elif choice == "2":
            handshake.start()
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
            colorful_print("Thank you for using WiFi Auditing Tool!", "green")
            sys.exit(0)
        else:
            colorful_print("Invalid choice!", "red")

if __name__ == '__main__':
    run()
