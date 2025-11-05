import sys

def colorful_print(text, color):
    """
    Prints text in a specified color using ANSI escape codes.
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m", # Added yellow
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    # Print the colored text, defaulting to 'reset' if color is not found
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")
