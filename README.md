# 🛡️ WiFi Auditing Tool 

<p align="center">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/trmxvibs/wifi-audit-tool/python-app.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white">
  <img alt="Python Version" src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python">
  <img alt="License" src="https://img.shields.io/github/license/trmxvibs/wifi-audit-tool?style=for-the-badge&color=yellow">
  <br>
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/trmxvibs/wifi-audit-tool?style=for-the-badge&color=blueviolet">
  <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/trmxvibs/wifi-audit-tool?style=for-the-badge">
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/trmxvibs/wifi-audit-tool?style=for-the-badge&color=green&logo=github">
</p>

A command-line toolkit designed for ethical hackers and network security enthusiasts using Kali Linux. This tool simplifies scanning WiFi networks, capturing handshakes, and generating crack commands through an easy-to-use, interactive menu.

---

> [!CAUTION]
> ## 🛑 Ethical Hacking Disclaimer
>
> This tool is intended for **educational purposes and authorized security testing ONLY**.
>
> Using this tool on networks without explicit, written permission from the owner is **illegal**. The developer is not responsible for any misuse or damage caused by this program. **Use responsibly.**

---

## 🚀 Key Features

* **Automatic Monitor Mode:** Automatically enables and disables monitor mode on your wireless adapter.
* **Network Scanning:** Scans for all nearby WiFi networks using `airodump-ng`.
* **WPA/WPA2 Handshake Capture:** Easily targets a specific network (by BSSID and channel) to capture WPA/WPA2 handshakes.

---

## 🛠️ Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/trmxvibs/wifi-audit-tool.git
    cd wifi-audit-tool
    ```

2.  Make the install script executable:
    ```bash
    chmod +x install.sh
    ```

3.  Run the installer (this will use `sudo` to install dependencies):
    ```bash
    ./install.sh
    ```

---

## ⚡ Usage & Example Workflow

Always run the tool with `sudo` (root) privileges:

```bash
sudo python3 wifi_audit.py
```




