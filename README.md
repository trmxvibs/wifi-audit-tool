# WiFi Audit Tool

A command-line wireless security auditing toolkit for Kali Linux. It wraps the standard `aircrack-ng` suite in a menu-driven workflow, adds structured scan output, offline vendor identification, scan history, and JSON/HTML/CSV reporting — so an authorized wireless assessment produces a proper audit trail instead of just terminal scrollback.

[![Tests](https://img.shields.io/github/actions/workflow/status/trmxvibs/wifi-audit-tool/python-app.yml?branch=main&label=tests)](https://github.com/trmxvibs/wifi-audit-tool/actions)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/trmxvibs/wifi-audit-tool)](LICENSE)

---

## ⚠️ Authorization required

This tool is for **authorized security testing only** — networks you own, networks you are contracted to test, or a controlled lab environment. Running scans or capture operations against networks without explicit written permission may violate the law. The author and contributors are not responsible for misuse.

---

## What it does

- **Scans nearby networks** via `airodump-ng`, either as a live terminal view or as a timed, structured scan you can act on programmatically.
- **Identifies device vendors** offline from each BSSID's OUI prefix (no internet call needed in the field).
- **Flags weak security** — open networks, WEP, WPA (non-WPA2/3), and WPA2 with WPS enabled — with a plain-language explanation of the risk.
- **Logs every scan** to a local history file, so you can track a network's posture over time.
- **Compares two scans** to show what's new, what disappeared, and whether any network's security got weaker or stronger since last time.
- **Exports reports** as JSON, HTML, or CSV.
- **Captures WPA/WPA2 handshakes** against a chosen BSSID/channel, and generates the matching `aircrack-ng` command for offline analysis.
- **Runs interactively or non-interactively** — the same tool works as a guided menu or as a scriptable CLI for automation.
- **Remembers your defaults** (interface, scan duration, export format) via a small local config file.

---

## Installation

```bash
git clone https://github.com/trmxvibs/wifi-audit-tool.git
cd wifi-audit-tool
chmod +x install.sh
./install.sh
```

`install.sh` installs `aircrack-ng`, `python3-pip`, and this project's Python dependencies. It uses `--break-system-packages` for the pip install, which is required on modern Kali/Debian (PEP 668) since this tool needs to run as root alongside `aircrack-ng` rather than in an isolated virtualenv.

**Requirements:**
- Python 3.8+
- `aircrack-ng` suite (`airodump-ng`, `aireplay-ng`)
- `iw`, `iproute2`
- Kali Linux or a compatible distribution
- A wireless adapter that supports monitor mode (see [Hardware](#hardware) below)

---

## Usage

### Interactive mode

```bash
sudo python3 wifi_audit.py
```

```
==== WiFi Auditing Tool (Kali Edition) ====
1) Scan WiFi Networks (live view)
2) Timed Scan + Security Analysis (structured, with vendor lookup)
3) Capture Handshake
4) Vulnerability Report / Crack
5) Scan History (from disk, persists across runs)
6) Export Last Scan Report (JSON/HTML/CSV)
7) Compare Last Scan to Previous Scan
8) Configure Defaults (interface, scan duration, export format)
9) Guidelines & Help
10) Exit
```

### Non-interactive / scripted mode

For automation or scheduled audits, skip the menu entirely:

```bash
sudo python3 wifi_audit.py --scan-duration 30 --iface wlan0mon --export report.json
```

| Flag | Description |
|---|---|
| `--scan-duration SECONDS` | Runs a timed scan, analyzes it, then exits (no menu). |
| `--iface IFACE` | Wireless interface to use. Defaults to the first detected interface. |
| `--export PATH` | Export path. Format is chosen by extension: `.json`, `.html`, or `.csv`. |

Every scan — interactive or scripted — is automatically logged to `scan_history.jsonl`, so `Compare Last Scan to Previous Scan` works regardless of which mode you used.

---

## Example authorized workflow

1. Run a timed scan against your lab network (option 2).
2. Review the security findings — open networks and WEP are flagged HIGH severity.
3. Export the report (option 6) to hand off or archive.
4. A week later, scan again and use **Compare** (option 7) to see if anything changed — a network that quietly dropped from WPA2 to open, for example.
5. If a target needs a deeper look, capture its handshake (option 3) and generate the offline crack command (option 4).

---

## Hardware

Most built-in laptop WiFi chipsets don't support monitor mode, and phone-hosted Kali (Termux/NetHunter) generally can't access the internal chipset at all. You'll need an external adapter:

- A USB WiFi adapter with a monitor-mode-capable chipset (e.g. Atheros AR9271, Ralink RT5370)
- An OTG adapter, if running from a phone

**Best reliability:** native Kali Linux, a Kali Live USB, or a Kali VM with USB passthrough to a dedicated test adapter.

If you see `Error detecting interfaces: Command ['iw', 'dev'] returned non-zero exit status 1`, this is almost always the host OS blocking direct chipset access (common in Android/Termux/NetHunter guest mode) — switch to external hardware.

---

## Project layout

```
wifi_audit.py            # entry point — interactive menu + CLI argument parsing
modules/
  scan.py                # airodump-ng wrapper + CSV output parsing
  handshake.py            # handshake capture
  report.py               # JSON/HTML/CSV export, crack-command generation
  history.py               # persistent JSONL scan history
  compare.py                # scan-to-scan diffing
utils/
  helpers.py               # colored output, validated input prompts
  ai_helper.py              # rule-based security classifier (not ML-based — see docstring)
  vendor.py                  # offline BSSID -> vendor lookup
  config.py                   # local defaults file
tests/                        # pytest suite (42 tests) covering every module above
```

---

## Testing

```bash
pip install -r requirements.txt --break-system-packages
PYTHONPATH=. pytest
```

CI runs this suite plus `flake8` on every push via GitHub Actions.

---

## Author

**Lokesh Kumar** — independent security enthusiast focused on wireless security testing, Kali Linux tooling, and command-line automation.

- GitHub: [@trmxvibs](https://github.com/trmxvibs)
- YouTube: [@termux2](https://youtube.com/@termux2)

### Contributing

Issues and pull requests are welcome. For significant changes, please open an issue first to discuss what you'd like to change.
