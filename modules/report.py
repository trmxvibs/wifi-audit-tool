import glob
import os
from utils.helpers import colorful_print

def history():
    colorful_print("Fetching capture history...", "cyan")
    
    cap_files = glob.glob('*.cap')
    
    if not cap_files:
        colorful_print("No .cap capture files found.", "yellow")
        return
        
    print("Found capture files:")
    for f in cap_files:
        print(f"- {f}")

def show():
    colorful_print("Generate Crack Command / Report...", "cyan")
    
    cap_files = glob.glob('*.cap')
    
    if not cap_files:
        colorful_print("No .cap files found to analyze.", "red")
        colorful_print("Run 'Capture Handshake' (Option 2) first.", "yellow")
        return

    print("Available capture files:")
    for i, f in enumerate(cap_files, 1):
        print(f"{i}) {f}")
    
    try:
        choice = int(input("Select file to crack (number): "))
        selected_file = cap_files[choice - 1]
        
        wordlist = input("Enter path to your wordlist (e.g., /usr/share/wordlists/rockyou.txt): ")
        
        if not os.path.exists(wordlist):
            colorful_print("Wordlist file not found! Please check the path.", "red")
            return
            
        colorful_print("\nTo crack this file, run the following command:", "green")
        print(f"\nsudo aircrack-ng -w {wordlist} {selected_file}\n")
        
    except (ValueError, IndexError):
        colorful_print("Invalid selection.", "red")
    except Exception as e:
        colorful_print(f"An error occurred: {e}", "red")
