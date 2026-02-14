# WiFi Audit Tool — Command Line Wireless Security Toolkit

<p align="center">

<img src="https://img.shields.io/badge/Type-WiFi%20Security%20Toolkit-black?style=for-the-badge">
<img src="https://img.shields.io/badge/Platform-Kali%20Linux-red?style=for-the-badge">
<img src="https://img.shields.io/badge/Interface-CLI-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Use-Authorized%20Testing-green?style=for-the-badge">

<br>

<img src="https://img.shields.io/github/actions/workflow/status/trmxvibs/wifi-audit-tool/python-app.yml?branch=main&style=for-the-badge">
<img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/github/license/trmxvibs/wifi-audit-tool?style=for-the-badge">
<img src="https://img.shields.io/github/issues/trmxvibs/wifi-audit-tool?style=for-the-badge">

</p>

---

## Overview

WiFi Audit Tool is a command-line wireless security toolkit built for Kali Linux environments. It is designed to streamline authorized wireless network assessments through an interactive menu-driven workflow.

The tool automates common audit steps such as enabling monitor mode, scanning nearby networks, and preparing WPA/WPA2 handshake capture sessions using standard aircrack-ng utilities.

---

## Authorization Requirement

<img src="https://img.shields.io/badge/Authorization-Required-critical?style=for-the-badge">

This tool is intended strictly for **authorized security testing**.

Running scans or capture operations against networks without explicit written permission may violate laws and regulations. The author and contributors are not responsible for misuse or resulting damage.

Allowed use cases:

- Networks you own
- Networks you are contracted to test
- Controlled lab environments

---

## Core Features

<img src="https://img.shields.io/badge/Feature-Monitor%20Mode%20Automation-informational?style=flat-square">

Automatically enables and disables monitor mode on the selected wireless adapter.

<img src="https://img.shields.io/badge/Feature-Network%20Scanning-informational?style=flat-square">

Discovers nearby wireless networks using airodump-ng.

<img src="https://img.shields.io/badge/Feature-Handshake%20Capture-informational?style=flat-square">

Targets a selected BSSID and channel to capture WPA/WPA2 handshakes.

<img src="https://img.shields.io/badge/Feature-Crack%20Command%20Helper-informational?style=flat-square">

Generates ready-to-run cracking commands for offline analysis tools.

---

## Dependencies

<img src="https://img.shields.io/badge/Backend-Aircrack--ng-important?style=flat-square">
<img src="https://img.shields.io/badge/Tool-iw-important?style=flat-square">
<img src="https://img.shields.io/badge/Access-root-important?style=flat-square">

Required components:

- Python 3.8 or higher
- aircrack-ng suite
- airodump-ng
- iw
- iproute2
- Kali Linux or compatible distribution

---

## Installation

### Clone Repository

```bash
git clone https://github.com/trmxvibs/wifi-audit-tool.git
cd wifi-audit-tool
```

### Make Installer Executable

```bash
chmod +x install.sh
```

### Install Dependencies

```bash
./install.sh
```

---

## Usage

Run with root privileges:

```bash
sudo python3 wifi_audit.py
```

An interactive menu will guide adapter selection, scanning, and capture setup.

---

## Example Authorized Audit Workflow

Typical permitted lab workflow:

1. Select wireless adapter
2. Enable monitor mode
3. Scan nearby access points
4. Choose target BSSID and channel
5. Start capture session
6. Verify handshake capture
7. Perform offline password audit using external tools

Example: testing your own lab router to verify password strength and capture reliability.

---

## Common Error: No Interfaces Detected

Error:

```
Error detecting interfaces: Command ['iw', 'dev'] returned non-zero exit status 1
```

### Cause

Occurs when running Kali inside Android/Termux or NetHunter guest mode. The host OS blocks direct access to the internal WiFi chipset.

### Fix

Use external hardware.

---

## Required Hardware

<img src="https://img.shields.io/badge/Hardware-External%20USB%20Adapter-required?style=flat-square">

You need:

- OTG adapter
- External USB WiFi adapter
- Monitor mode supported chipset

Supported chipsets:

- Atheros AR9271
- Ralink RT5370

---

## Recommended Environment

<img src="https://img.shields.io/badge/Environment-Native%20Kali-success?style=flat-square">

Best reliability:

- Native Kali Linux
- Kali Live USB
- Kali VM with USB passthrough
- Dedicated test adapter

---

---

## Author

<img src="https://img.shields.io/badge/Author-Lokesh%20Kumar-black?style=for-the-badge">
<img src="https://img.shields.io/badge/Role-Security%20Researcher-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Focus-WiFi%20Auditing-red?style=for-the-badge">

Independent security enthusiast focused on wireless security testing, Kali Linux tooling, and practical command-line automation.

### Contact


### GitHub: [Lokesh-Kumar](https://github.com/trmxvibs)
### YouTube: [Lokesh-Kumar](https://youtube.com/@termux2)

### Contributions

Pull requests, issue reports, and security improvement suggestions are welcome.  
For major changes, open an issue first to discuss the proposal.

---
