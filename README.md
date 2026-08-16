<div align="center">

# 📡 WiFi Audit Tool

### Command-Line Wireless Security Auditing Toolkit for Kali Linux

<p>
<img src="https://img.shields.io/badge/Type-WiFi%20Security%20Toolkit-black?style=for-the-badge&logo=wifi&logoColor=white" />
<img src="https://img.shields.io/badge/Platform-Kali%20Linux-red?style=for-the-badge&logo=kalilinux&logoColor=white" />
<img src="https://img.shields.io/badge/Interface-CLI-blue?style=for-the-badge&logo=gnometerminal&logoColor=white" />
<img src="https://img.shields.io/badge/Use-Authorized%20Testing%20Only-critical?style=for-the-badge" />
</p>

<p>
<img src="https://img.shields.io/github/actions/workflow/status/trmxvibs/wifi-audit-tool/python-app.yml?branch=main&style=for-the-badge&label=CI" />
<img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/github/license/trmxvibs/wifi-audit-tool?style=for-the-badge" />
<img src="https://img.shields.io/badge/Tests-42%20passing-success?style=for-the-badge&logo=pytest&logoColor=white" />
</p>

<p>
<img src="https://img.shields.io/github/stars/trmxvibs/wifi-audit-tool?style=for-the-badge&color=yellow" />
<img src="https://img.shields.io/github/forks/trmxvibs/wifi-audit-tool?style=for-the-badge&color=blue" />
<img src="https://img.shields.io/github/issues/trmxvibs/wifi-audit-tool?style=for-the-badge&color=orange" />
<img src="https://img.shields.io/github/last-commit/trmxvibs/wifi-audit-tool?style=for-the-badge" />
</p>

<p>
<img src="https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square" />
<img src="https://img.shields.io/badge/Flake8-Passing-brightgreen?style=flat-square&logo=python" />
</p>

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [⚠️ Authorization Requirement](#️-authorization-requirement)
- [Core Features](#-core-features)
- [Project Architecture](#-project-architecture)
- [Dependencies](#-dependencies)
- [Installation](#️-installation)
- [Usage — Basic](#-usage--basic-interactive-mode)
- [Usage — Advanced](#-usage--advanced-scripted--automation-mode)
- [Configuration](#️-configuration)
- [Feature Deep Dive](#-feature-deep-dive)
- [Example Authorized Workflow](#-example-authorized-workflow)
- [Hardware Requirements](#-hardware-requirements)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🧭 Overview

<img src="https://img.shields.io/badge/Category-Wireless%20Pentesting-informational?style=flat-square" />
<img src="https://img.shields.io/badge/Backend-aircrack--ng-important?style=flat-square" />
<img src="https://img.shields.io/badge/Output-JSON%20%7C%20HTML%20%7C%20CSV-blueviolet?style=flat-square" />

**WiFi Audit Tool** is a command-line wireless security toolkit built for Kali Linux environments. It wraps the standard `aircrack-ng` suite in a guided, menu-driven workflow — and layers structured scan output, offline vendor identification, historical tracking, and multi-format reporting on top, so an authorized wireless assessment produces a real audit trail instead of just terminal scrollback.

It's built for two audiences at once:

| Audience | How they use it |
|---|---|
| 🟢 **Beginners** | Guided interactive menu — no flags to memorize |
| 🔵 **Advanced users** | Non-interactive CLI flags for scripting, cron jobs, and CI pipelines |

---

## ⚠️ Authorization Requirement

<img src="https://img.shields.io/badge/Authorization-Required-critical?style=for-the-badge" />
<img src="https://img.shields.io/badge/Unauthorized%20Use-Illegal-red?style=for-the-badge" />

> This tool is intended **strictly** for authorized security testing.

Running scans or capture operations against networks without explicit written permission may violate laws and regulations in your jurisdiction. The author and contributors are **not responsible** for misuse or resulting damage.

**✅ Allowed use cases:**
- Networks you own
- Networks you are contracted / engaged to test
- Controlled lab environments

**❌ Not allowed:**
- Any network you don't have explicit written permission to test

---

## 🚀 Core Features

<table>
<tr><td>

<img src="https://img.shields.io/badge/Feature-Monitor%20Mode%20Automation-informational?style=flat-square" />

</td><td>Automatically enables and disables monitor mode on the selected wireless adapter.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Structured%20Scanning-informational?style=flat-square" />

</td><td>Timed scans parsed into structured data (BSSID, ESSID, channel, privacy, power) — not just raw terminal output.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Vendor%20Lookup-informational?style=flat-square" />

</td><td>Offline BSSID → manufacturer identification via OUI prefix. No internet required in the field.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Security%20Analysis-informational?style=flat-square" />

</td><td>Rule-based classifier flags open networks, WEP, WPA (non-WPA2/3), and WPA2+WPS as HIGH/MEDIUM risk with plain-language explanations.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Scan%20History-informational?style=flat-square" />

</td><td>Every scan is logged to a local JSONL history file — track a network's security posture over time.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Scan%20Comparison-informational?style=flat-square" />

</td><td>Diff two scans to see what's new, what disappeared, and whether any network's security got weaker or stronger.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Multi--Format%20Export-informational?style=flat-square" />

</td><td>Export any scan/report as JSON, HTML (styled), or CSV (spreadsheet-ready).</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Handshake%20Capture-informational?style=flat-square" />

</td><td>Targets a selected BSSID and channel to capture WPA/WPA2 handshakes.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Crack%20Command%20Helper-informational?style=flat-square" />

</td><td>Generates ready-to-run `aircrack-ng` cracking commands for offline analysis.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-CLI%20Automation-informational?style=flat-square" />

</td><td>Fully non-interactive mode for cron jobs, CI pipelines, or scripted audits.</td></tr>

<tr><td>

<img src="https://img.shields.io/badge/Feature-Persistent%20Config-informational?style=flat-square" />

</td><td>Save default interface, scan duration, and export format so you stop retyping the same flags.</td></tr>

</table>

---

## 🏗 Project Architecture

```
wifi-audit-tool/
│
├── wifi_audit.py              # Entry point — interactive menu + argparse CLI
│
├── modules/
│   ├── scan.py                 # airodump-ng wrapper + CSV output parsing
│   ├── handshake.py             # WPA/WPA2 handshake capture
│   ├── report.py                 # JSON / HTML / CSV export + crack-command generator
│   ├── history.py                 # Persistent JSONL scan history
│   └── compare.py                  # Scan-to-scan diffing engine
│
├── utils/
│   ├── helpers.py               # Colorized output (colorama) + validated input prompts
│   ├── ai_helper.py              # Rule-based network security classifier
│   ├── vendor.py                  # Offline BSSID → vendor (OUI) lookup
│   └── config.py                   # Local defaults file (JSON)
│
├── tests/                       # pytest suite — 42 tests across every module above
│   └── fixtures/                 # Sample airodump-ng CSV fixtures for parser tests
│
├── .github/workflows/            # CI: pytest + flake8 on every push
├── install.sh                     # Dependency installer (PEP 668 safe)
└── requirements.txt
```

<div align="center">
<img src="https://img.shields.io/badge/Architecture-Modular-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Test%20Coverage-Every%20Module-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/Style-flake8%20Clean-brightgreen?style=flat-square" />
</div>

---

## 📦 Dependencies

<img src="https://img.shields.io/badge/Backend-Aircrack--ng-important?style=flat-square" />
<img src="https://img.shields.io/badge/Tool-iw-important?style=flat-square" />
<img src="https://img.shields.io/badge/Tool-iproute2-important?style=flat-square" />
<img src="https://img.shields.io/badge/Access-root-important?style=flat-square" />
<img src="https://img.shields.io/badge/Lib-colorama-important?style=flat-square" />

| Dependency | Purpose |
|---|---|
| Python 3.8+ | Runtime |
| `aircrack-ng` suite | `airodump-ng`, `aireplay-ng` — scanning & capture |
| `iw` | Interface / monitor-mode management |
| `iproute2` | Interface up/down control |
| `colorama` | Cross-platform colored terminal output |
| Kali Linux (or compatible) | Target OS |

---

## ⚙️ Installation

<img src="https://img.shields.io/badge/Step-1%20of%203-blue?style=flat-square" />

### Clone the repository

```bash
git clone https://github.com/trmxvibs/wifi-audit-tool.git
cd wifi-audit-tool
```

<img src="https://img.shields.io/badge/Step-2%20of%203-blue?style=flat-square" />

### Make the installer executable

```bash
chmod +x install.sh
```

<img src="https://img.shields.io/badge/Step-3%20of%203-blue?style=flat-square" />

### Run the installer

```bash
./install.sh
```

This installs `aircrack-ng`, `python3-pip`, and the Python dependencies in `requirements.txt`. It uses `--break-system-packages` for the pip install — required on modern Kali/Debian (PEP 668) since this tool runs as root alongside `aircrack-ng` rather than in an isolated virtualenv.

---

## 🟢 Usage — Basic (Interactive Mode)

<img src="https://img.shields.io/badge/Difficulty-Beginner-brightgreen?style=flat-square" />

Run with root privileges:

```bash
sudo python3 wifi_audit.py
```

You'll get a guided menu:

```
==== WiFi Auditing Tool (Kali Edition) ====
1)  Scan WiFi Networks (live view)
2)  Timed Scan + Security Analysis (structured, with vendor lookup)
3)  Capture Handshake
4)  Vulnerability Report / Crack
5)  Scan History (from disk, persists across runs)
6)  Export Last Scan Report (JSON/HTML/CSV)
7)  Compare Last Scan to Previous Scan
8)  Configure Defaults (interface, scan duration, export format)
9)  Guidelines & Help
10) Exit
```

Just follow the prompts — adapter selection, scan duration, and file paths are all asked interactively.

---

## 🔵 Usage — Advanced (Scripted / Automation Mode)

<img src="https://img.shields.io/badge/Difficulty-Advanced-orange?style=flat-square" />
<img src="https://img.shields.io/badge/Scriptable-Yes-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Cron%20Friendly-Yes-blue?style=flat-square" />

Skip the menu entirely for automation, cron jobs, or CI-driven audits:

```bash
sudo python3 wifi_audit.py --scan-duration 30 --iface wlan0mon --export report.json
```

| Flag | Type | Description |
|---|---|---|
| `--scan-duration SECONDS` | int | Runs a timed scan, analyzes it, then exits. Omit for interactive menu. |
| `--iface IFACE` | string | Wireless interface to use. Defaults to first detected interface. |
| `--export PATH` | path | Export destination. Format inferred from extension: `.json`, `.html`, `.csv`. |

**Example — daily cron audit:**

```bash
# /etc/cron.daily/wifi-audit
sudo python3 /opt/wifi-audit-tool/wifi_audit.py \
  --iface wlan0mon \
  --scan-duration 60 \
  --export /var/log/wifi-audit/$(date +%F).json
```

Every scan — interactive or scripted — is automatically logged to `scan_history.jsonl`, so **Compare Last Scan to Previous Scan** works regardless of which mode you used.

---

## ⚙️ Configuration

<img src="https://img.shields.io/badge/Config-Persistent%20JSON-lightgrey?style=flat-square" />

Set your own defaults once (interactive menu, option 8) so you don't have to retype flags:

```json
{
  "iface": "wlan0mon",
  "scan_duration": 60,
  "export_format": "csv",
  "history_path": "scan_history.jsonl"
}
```

Stored in `.wifi_audit_config.json` in your working directory. CLI flags always override the config file when both are given.

---

## 🔬 Feature Deep Dive

### 📡 Structured Scanning
`airodump-ng` output is parsed directly from its CSV export into clean Python dicts — `bssid`, `essid`, `channel`, `privacy`, `cipher`, `authentication`, `power` — ready for analysis, export, or scripting.

### 🏷 Offline Vendor Lookup
<img src="https://img.shields.io/badge/Network-Not%20Required-success?style=flat-square" />

Every BSSID is matched against its OUI (organizationally unique identifier) prefix to reveal the manufacturer — TP-Link, Netgear, Cisco, Ubiquiti, and more — entirely offline.

### 🛡 Security Classifier
<img src="https://img.shields.io/badge/Type-Rule--Based-yellow?style=flat-square" />

Not machine learning — a transparent, auditable rule set:

| Privacy | Severity | Reason |
|---|---|---|
| Open (`OPN`) | 🔴 HIGH | No encryption — traffic readable by anyone nearby |
| WEP | 🔴 HIGH | Broken since ~2005, crackable in minutes |
| WPA (non-WPA2/3) | 🟠 MEDIUM | Vulnerable to known TKIP attacks |
| WPA2 + WPS | 🟠 MEDIUM | WPS PIN attacks may apply |
| WPA2 / WPA3 | ✅ Clean | No issues flagged |

### 🕰 Scan History & Comparison
Every scan is appended to `scan_history.jsonl`. The **Compare** feature diffs your latest scan against the previous one:

```
[NEW] NewNeighborWifi (DE:AD:BE:EF:00:01)
[GONE] FreeWiFi (AA:BB:CC:DD:EE:FF)
[CHANGED] HomeNetwork (00:11:22:33:44:55): WPA2 -> WEP (WEAKER)
```

### 📤 Multi-Format Export
| Format | Best for |
|---|---|
| **JSON** | Programmatic processing, archiving |
| **HTML** | Human-readable report, client hand-off (XSS-safe, escaped output) |
| **CSV** | Spreadsheet analysis, filtering, sorting |

---

## 🧪 Example Authorized Workflow

<img src="https://img.shields.io/badge/Workflow-Lab%20Tested-blue?style=flat-square" />

1. Run a timed scan against your lab network (**option 2**)
2. Review flagged findings — open networks and WEP show as HIGH severity
3. Export the report (**option 6**) to archive or hand off
4. A week later, scan again and use **Compare** (**option 7**) — catch a network that quietly dropped from WPA2 to open
5. For deeper analysis, capture the target's handshake (**option 3**) and generate the offline crack command (**option 4**)

---

## 🔧 Hardware Requirements

<img src="https://img.shields.io/badge/Hardware-External%20USB%20Adapter-required?style=flat-square" />
<img src="https://img.shields.io/badge/Chipset-Monitor%20Mode%20Capable-important?style=flat-square" />

Most built-in laptop WiFi chipsets don't support monitor mode, and phone-hosted Kali (Termux/NetHunter) generally can't access the internal chipset at all.

**You need:**
- A USB WiFi adapter with a monitor-mode-capable chipset
- An OTG adapter, if running from a phone

**Supported chipsets (tested):**
- Atheros AR9271
- Ralink RT5370

**✅ Recommended environments:**
<img src="https://img.shields.io/badge/Environment-Native%20Kali-success?style=flat-square" />

- Native Kali Linux
- Kali Live USB
- Kali VM with USB passthrough
- Dedicated test adapter

---

## ✅ Testing

<img src="https://img.shields.io/badge/Tests-42%20passing-success?style=for-the-badge&logo=pytest&logoColor=white" />
<img src="https://img.shields.io/badge/Coverage-Every%20Module-brightgreen?style=for-the-badge" />
<img src="https://img.shields.io/badge/Lint-flake8%20clean-brightgreen?style=for-the-badge" />

```bash
pip install -r requirements.txt --break-system-packages
PYTHONPATH=. pytest -v
```

CI runs this full suite plus `flake8` on every push via GitHub Actions — badge at the top of this README reflects live status.

| Test file | Covers |
|---|---|
| `test_scan.py`, `test_scan_parsing.py` | airodump-ng wrapper + CSV parsing |
| `test_ai_helper.py` | Security severity classification |
| `test_vendor.py` | OUI vendor lookup |
| `test_history.py` | JSONL scan history persistence |
| `test_compare.py` | Scan diffing logic |
| `test_config.py` | Config load/save/defaults |
| `test_report_export.py` | JSON/HTML/CSV export, XSS-safety |
| `test_utils.py` | Colorized output helpers |

---

## 🩹 Troubleshooting

<details>
<summary><b>❌ Error: No Interfaces Detected</b></summary>

```
Error detecting interfaces: Command ['iw', 'dev'] returned non-zero exit status 1
```

**Cause:** Occurs when running Kali inside Android/Termux or NetHunter guest mode — the host OS blocks direct access to the internal WiFi chipset.

**Fix:** Use an external USB adapter (see [Hardware Requirements](#-hardware-requirements)).

</details>

<details>
<summary><b>❌ pip install fails with "externally-managed-environment"</b></summary>

This is expected on modern Kali/Debian (PEP 668). `install.sh` already handles this with `--break-system-packages`. If installing manually, add the same flag.

</details>

<details>
<summary><b>❌ Monitor mode fails to enable</b></summary>

Try:
```bash
rfkill unblock wifi
```
then re-run the tool.

</details>

---

## 🤝 Contributing

<img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" />
<img src="https://img.shields.io/badge/Issues-Open-blue?style=for-the-badge" />

Pull requests, issue reports, and security improvement suggestions are welcome. For significant changes, please open an issue first to discuss the proposal.

---

## 👤 Author

<div align="center">

<img src="https://img.shields.io/badge/Author-Lokesh%20Kumar-black?style=for-the-badge" />
<img src="https://img.shields.io/badge/Role-Security%20Researcher-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Focus-WiFi%20Auditing-red?style=for-the-badge" />

Independent security enthusiast focused on wireless security testing, Kali Linux tooling, and practical command-line automation.

[![GitHub](https://img.shields.io/badge/GitHub-trmxvibs-181717?style=for-the-badge&logo=github)](https://github.com/trmxvibs)
[![YouTube](https://img.shields.io/badge/YouTube-@termux2-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@termux2)

</div>

---

## 📄 License

<img src="https://img.shields.io/github/license/trmxvibs/wifi-audit-tool?style=for-the-badge" />

Licensed under the terms in [LICENSE](LICENSE).

---

<div align="center">
<sub>Built for authorized security testing. Use responsibly. 🛡️</sub>
</div>
