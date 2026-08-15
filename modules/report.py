import csv
import glob
import json
import os
from datetime import datetime, timezone
from html import escape
from utils.helpers import colorful_print


def export_csv(networks, output_path):
    """
    Exports scan results as CSV — useful for opening in a spreadsheet
    for filtering/sorting, which JSON/HTML don't offer directly.
    Findings aren't included since they're prose, not tabular data.
    """
    fieldnames = ["essid", "bssid", "channel", "privacy", "cipher", "authentication", "power", "vendor"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for net in networks:
            writer.writerow({field: net.get(field, "") for field in fieldnames})
    colorful_print(f"CSV report saved to {output_path}", "green")


def export_json(networks, findings, output_path):
    """Exports scan results + security findings as a JSON report."""
    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'network_count': len(networks),
        'networks': networks,
        'findings': [{'severity': sev, 'message': msg} for sev, msg in findings],
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    colorful_print(f"JSON report saved to {output_path}", "green")


def export_html(networks, findings, output_path):
    """Exports scan results + security findings as a simple standalone HTML report."""
    rows = "\n".join(
        f"<tr><td>{escape(n.get('essid', ''))}</td><td>{escape(n.get('bssid', ''))}</td>"
        f"<td>{escape(n.get('channel', ''))}</td><td>{escape(n.get('privacy', ''))}</td>"
        f"<td>{escape(n.get('power', ''))}</td></tr>"
        for n in networks
    )
    finding_items = "\n".join(
        f"<li class='{escape(sev)}'><strong>{escape(sev.upper())}</strong>: {escape(msg)}</li>"
        for sev, msg in findings
    ) or "<li>No issues found.</li>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>WiFi Audit Report</title>
<style>
  body {{ font-family: sans-serif; margin: 2rem; color: #222; }}
  table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
  th {{ background: #333; color: #fff; }}
  li.high {{ color: #b00020; }}
  li.medium {{ color: #b06a00; }}
</style>
</head>
<body>
<h1>WiFi Audit Report</h1>
<p>Generated: {escape(datetime.now(timezone.utc).isoformat())}</p>
<h2>Networks ({len(networks)})</h2>
<table>
<tr><th>ESSID</th><th>BSSID</th><th>Channel</th><th>Privacy</th><th>Power</th></tr>
{rows}
</table>
<h2>Security Findings</h2>
<ul>
{finding_items}
</ul>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    colorful_print(f"HTML report saved to {output_path}", "green")


def history():
    """Shows previously captured .cap files."""
    colorful_print("Fetching capture history...", "cyan")
    
    # Find all .cap files in the current directory
    cap_files = glob.glob('*.cap')
    
    if not cap_files:
        colorful_print("No .cap capture files found.", "yellow")
        return
        
    print("Found capture files:")
    for f in cap_files:
        print(f"- {f}")

def show():
    """Generates the aircrack-ng command for a selected file."""
    colorful_print("Generate Crack Command / Report...", "cyan")
    
    # Find .cap files (airodump adds '-01', '-02' etc)
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
