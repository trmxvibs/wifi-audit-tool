import argparse
import sys
import subprocess
import os
import re
from utils.helpers import colorful_print, prompt_int
from modules import scan, handshake, report, history, compare
from utils.ai_helper import suggest_network
from utils.vendor import annotate_networks
from utils.config import load_config, set_default

# Holds the most recent timed_scan() result in-memory so the
# "Export Report" menu option can reuse it without rescanning.
_last_scan_networks = []
_last_scan_findings = []

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
        colorful_print("Please install them using: sudo apt-get install <package_name>", "red")
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

        while True:
            choice = input("Select interface to use (number): ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(interfaces)):
                colorful_print(
                    f"Invalid choice. Enter a number between 1 and {len(interfaces)}.", "red"
                )
                continue
            return interfaces[int(choice) - 1]

    except subprocess.CalledProcessError as e:
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
    print("1) Scan WiFi Networks (live view)")
    print("2) Timed Scan + Security Analysis (structured, with vendor lookup)")
    print("3) Capture Handshake")
    print("4) Vulnerability Report / Crack")
    print("5) Scan History (from disk, persists across runs)")
    print("6) Export Last Scan Report (JSON/HTML/CSV)")
    print("7) Compare Last Scan to Previous Scan")
    print("8) Configure Defaults (interface, scan duration, export format)")
    print("9) Guidelines & Help")
    print("10) Exit")
    choice = input("Select option: ")
    return choice


def run_timed_scan(iface):
    """
    Menu handler: run a timed scan, annotate with vendor info, analyze,
    log to history, and keep the result in-memory for export/compare.
    """
    global _last_scan_networks, _last_scan_findings
    config = load_config()
    duration_input = input(f"Scan duration in seconds (default {config['scan_duration']}): ").strip()
    duration = int(duration_input) if duration_input.isdigit() else config['scan_duration']

    networks = scan.timed_scan(iface, duration)
    networks = annotate_networks(networks)  # adds 'vendor' per network
    findings = suggest_network(networks)

    history.append_scan(networks, findings, path=config['history_path'])
    colorful_print(f"Scan logged to {config['history_path']}.", "cyan")

    _last_scan_networks, _last_scan_findings = networks, findings


def export_last_scan():
    """Menu handler: export the most recent timed scan to JSON, HTML, or CSV."""
    if not _last_scan_networks:
        colorful_print("No scan results yet. Run 'Timed Scan' (option 2) first.", "red")
        return
    fmt = input("Export format (json/html/csv): ").strip().lower()
    default_name = "wifi_audit_report." + (fmt if fmt in ("html", "csv") else "json")
    path = input(f"Output path (default {default_name}): ").strip() or default_name
    if fmt == "html":
        report.export_html(_last_scan_networks, _last_scan_findings, path)
    elif fmt == "csv":
        report.export_csv(_last_scan_networks, path)
    else:
        report.export_json(_last_scan_networks, _last_scan_findings, path)


def show_scan_history():
    """Menu handler: prints past logged scans AND past .cap capture files."""
    report.history()  # original behavior: lists .cap files (unchanged)

    config = load_config()
    summary = history.summarize_history(path=config['history_path'])
    if not summary:
        colorful_print("No scan history yet. Run 'Timed Scan' (option 2) first.", "yellow")
        return
    colorful_print(f"\nScan History ({len(summary)} scan(s)):", "cyan")
    for timestamp, net_count, high_count in summary:
        tag = f"[{high_count} HIGH]" if high_count else "[clean]"
        print(f"  {timestamp} — {net_count} network(s) {tag}")


def compare_last_scan():
    """Menu handler: diffs the current in-memory scan against the previous logged scan."""
    if not _last_scan_networks:
        colorful_print("No current scan yet. Run 'Timed Scan' (option 2) first.", "red")
        return
    config = load_config()
    past = history.load_history(path=config['history_path'])
    if len(past) < 2:
        colorful_print("Need at least 2 logged scans to compare. Run Timed Scan again later.", "yellow")
        return
    previous_scan = past[-2]  # last one is the current scan we just logged
    diff = compare.diff_scans(previous_scan.get("networks", []), _last_scan_networks)
    colorful_print(f"\nChanges since {previous_scan.get('timestamp', '?')}:", "cyan")
    for line in compare.format_diff_summary(diff):
        print(f"  {line}")


def configure_defaults():
    """Menu handler: lets the user persist default iface/duration/export format."""
    config = load_config()
    colorful_print("\nCurrent defaults:", "cyan")
    for key, value in config.items():
        print(f"  {key}: {value}")

    duration_input = input(f"New default scan duration in seconds (blank to keep {config['scan_duration']}): ").strip()
    if duration_input.isdigit():
        set_default('scan_duration', int(duration_input))

    fmt_input = input(f"New default export format json/html/csv (blank to keep {config['export_format']}): ").strip().lower()
    if fmt_input in ('json', 'html', 'csv'):
        set_default('export_format', fmt_input)

    colorful_print("Defaults saved.", "green")

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
                run_timed_scan(iface)
            elif choice == "3":
                # Pass the interface name to the handshake function
                handshake.start(iface)
            elif choice == "4":
                report.show()
            elif choice == "5":
                show_scan_history()
            elif choice == "6":
                export_last_scan()
            elif choice == "7":
                compare_last_scan()
            elif choice == "8":
                configure_defaults()
            elif choice == "9":
                try:
                    with open("README.md") as f:
                        print(f.read())
                except FileNotFoundError:
                    colorful_print("README.md file not found.", "red")
            elif choice == "10":
                break  # Exit loop to clean up
            else:
                colorful_print("Invalid choice!", "red")
                
    except KeyboardInterrupt:
        print("\nExiting due to user request (Ctrl+C).")
    finally:
        # This will run whether exiting normally (option 6) or via Ctrl+C
        stop_monitor_mode(iface)
        colorful_print("Thank you for using WiFi Auditing Tool!", "green")
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser(
        description="WiFi Auditing Tool — for authorized security testing only."
    )
    parser.add_argument(
        '--scan-duration', type=int, metavar='SECONDS',
        help="Run non-interactively: timed scan for SECONDS, analyze, then exit. "
             "Omit this flag to use the normal interactive menu."
    )
    parser.add_argument(
        '--iface', metavar='IFACE',
        help="Wireless interface to use. If omitted in non-interactive mode, "
             "the first detected interface is used."
    )
    parser.add_argument(
        '--export', metavar='PATH',
        help="Export the scan report to PATH. Format is chosen by extension "
             "(.json or .html); defaults to JSON."
    )
    return parser.parse_args()


def run_non_interactive(args):
    """Scripting-friendly path: scan, analyze, log, export, exit. No menu."""
    check_kali_dependencies()
    config = load_config()

    iface = args.iface or config['iface']
    if not iface:
        result = subprocess.run(['iw', 'dev'], capture_output=True, text=True, check=True)
        detected = re.findall(r'Interface\s+(\w+)', result.stdout)
        if not detected:
            colorful_print("No wireless interfaces found. Exiting.", "red")
            sys.exit(1)
        iface = detected[0]
        colorful_print(f"No --iface given, using first detected: {iface}", "yellow")

    set_monitor_mode(iface)
    try:
        networks = scan.timed_scan(iface, args.scan_duration)
        networks = annotate_networks(networks)
        findings = suggest_network(networks)
        history.append_scan(networks, findings, path=config['history_path'])

        if args.export:
            if args.export.endswith('.html'):
                report.export_html(networks, findings, args.export)
            elif args.export.endswith('.csv'):
                report.export_csv(networks, args.export)
            else:
                report.export_json(networks, findings, args.export)
    finally:
        stop_monitor_mode(iface)
        sys.exit(0)


if __name__ == '__main__':
    cli_args = parse_args()
    if cli_args.scan_duration:
        run_non_interactive(cli_args)
    else:
        run()
