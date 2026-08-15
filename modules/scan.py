import csv
import glob
import os
import subprocess
from utils.helpers import colorful_print


def start(iface):
    """Starts the airodump-ng scan (live, interactive table view)."""
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


def parse_airodump_csv(csv_path):
    """
    Parses an airodump-ng CSV export (the AP section only) into a list
    of dicts: bssid, essid, channel, power, privacy, cipher, authentication.

    airodump-ng's CSV has two sections separated by a blank line:
    the AP list, then a "Station MAC" header for the client list.
    We only care about the AP section here.
    """
    networks = []
    if not os.path.exists(csv_path):
        return networks

    with open(csv_path, newline='', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0].strip() == 'BSSID':
            header_idx = i
            break
    if header_idx is None:
        return networks

    for row in rows[header_idx + 1:]:
        if not row or not row[0].strip():
            break  # blank line = end of AP section
        if row[0].strip() == 'Station MAC':
            break  # safety, in case there was no blank line
        if len(row) < 14:
            continue  # malformed/short row, skip rather than crash
        networks.append({
            'bssid': row[0].strip(),
            'channel': row[3].strip(),
            'privacy': row[5].strip(),
            'cipher': row[6].strip(),
            'authentication': row[7].strip(),
            'power': row[8].strip(),
            'essid': row[13].strip() or '(hidden)',
        })
    return networks


def timed_scan(iface, duration, output_prefix='scan_result'):
    """
    Runs airodump-ng for a fixed duration, writing CSV output, then
    parses and returns the structured network list. Unlike start(),
    this doesn't require the user to Ctrl+C — it stops itself.
    """
    colorful_print(
        f"Running timed scan on {iface} for {duration}s (structured output)...", "cyan"
    )

    # Clean up any stale files from a previous run with the same prefix
    for stale in glob.glob(f"{output_prefix}-*.csv"):
        os.remove(stale)

    command = [
        'timeout', str(duration),
        'airodump-ng', '--output-format', 'csv', '-w', output_prefix, iface
    ]
    try:
        subprocess.run(command, capture_output=True)
    except subprocess.CalledProcessError as e:
        colorful_print(f"Error running timed scan: {e}", "red")
        return []

    matches = sorted(glob.glob(f"{output_prefix}-*.csv"))
    if not matches:
        colorful_print("No scan output file was produced.", "red")
        return []

    networks = parse_airodump_csv(matches[-1])
    colorful_print(f"Timed scan complete: {len(networks)} network(s) found.", "green")
    return networks
