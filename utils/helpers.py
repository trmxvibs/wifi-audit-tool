import subprocess
import sys

def colorful_print(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def check_dependencies():
    tools = ["aircrack-ng", "iw", "net-tools"]
    missing = []
    for tool in tools:
        if subprocess.call(f"type {tool}", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            missing.append(tool)
    if missing:
        colorful_print(f"Missing dependencies: {', '.join(missing)}", "red")
        colorful_print("Please run ./install.sh to install them.", "red")
        sys.exit(1)
