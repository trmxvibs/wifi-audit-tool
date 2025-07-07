import sys
from utils.helpers import check_dependencies, colorful_print
from modules import scan, handshake, report

def main_menu():
    colorful_print("==== WiFi Auditing Tool ====", "cyan")
    print("1) Scan WiFi Networks")
    print("2) Capture Handshake")
    print("3) Vulnerability Report")
    print("4) Scan History")
    print("5) Guidelines & Help")
    print("6) Exit")
    choice = input("Select option: ")
    return choice

def run():
    check_dependencies()
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
            with open("README.md") as f:
                print(f.read())
        elif choice == "6":
            colorful_print("Thank you for using WiFi Auditing Tool!", "green")
            sys.exit(0)
        else:
            colorful_print("Invalid choice!", "red")

if __name__ == '__main__':
    run()