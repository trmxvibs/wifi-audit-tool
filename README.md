# WiFi Auditing Tool  

**Compatible with Termux (Android), Kali Linux, and WSL (Windows Subsystem for Linux)**

---

## Overview

WiFi Auditing Tool is a command-line toolkit designed for ethical hackers, penetration testers, and network security enthusiasts. This tool simplifies the process of scanning WiFi networks, capturing handshakes, performing basic network vulnerability analysis, and generating reports—all through an easy-to-use interactive menu.

> **Warning:**  
> This tool is intended for educational and authorized penetration testing **only**.  
> **Never** use it on networks without explicit permission from the owner.  
> Illegal and unauthorized use is strictly prohibited and may result in criminal prosecution.

---

## Features

- **WiFi Network Scanning**  
  Detects nearby wireless networks, showing SSID, signal strength, and security protocol.

- **AI-Powered Recommendations**  
  Suggests potentially vulnerable or insecure networks based on scan results.

- **Handshake Capture**  
  Initiates WPA/WPA2 handshake capture (requires monitor mode and root access).

- **Vulnerability Summary Report**  
  Generates a summary of detected risks (e.g., open networks, WEP, WPS enabled).

- **Scan History**  
  Maintains local logs of previous scans and actions.

- **Automatic Dependency Checking**  
  Installs and verifies required packages and dependencies.

- **User-Friendly Interface**  
  Colorful, interactive CLI menu for simple navigation.

---

## Installation

**1. Clone the Repository**

```bash
git clone https://github.com/trmxvibs/wifi-audit-tool.git
cd wifi-audit-tool
```

**2. Run the Installer**

```bash
chmod +x install.sh
./install.sh
```

*The installer will automatically detect your environment (Termux, Kali, WSL) and install all dependencies.*

---

## Usage

```bash
python3 wifi_audit.py
```

*You must run with root privileges for full functionality (especially handshake capture).*

---

## Requirements

- Python 3.x
- [aircrack-ng](https://www.aircrack-ng.org/)
- [iw](https://wireless.wiki.kernel.org/en/users/documentation/iw)
- [net-tools](https://wiki.linuxfoundation.org/networking/net-tools)
- git

**On Android (Termux), these can be installed using `pkg`**

**On Kali Linux/WSL, use `apt`**

---

## Main Menu

1. **Scan WiFi Networks**  
   Scan and list available WiFi networks.

2. **Capture Handshake**  
   Initiate handshake capture for a selected network (requires compatible WiFi card and monitor mode).

3. **Vulnerability Report**  
   Generate a vulnerability assessment based on scan data.

4. **Scan History**  
   View logs of previous scans and actions.

5. **Guidelines & Help**  
   View usage guidelines, disclaimer, and troubleshooting help.

6. **Exit**  
   Quit the tool.

---

## Ethical Guidelines & Disclaimer

- **This tool is strictly for learning, research, and authorized penetration testing.**
- Use only on networks you own or have written permission to test.
- The authors and contributors are not responsible for any misuse or illegal actions.
- By using this tool, you agree to comply with all local, state, and federal laws.

---

## Directory Structure

```sql
wifi-audit-tool/
│
├── README.md
├── install.sh
├── requirements.txt
├── wifi_audit.py
├── modules/
│   ├── scan.py
│   ├── handshake.py
│   └── report.py
└── utils/
    ├── helpers.py
    └── ai_helper.py
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a new Pull Request

---

## License

This project is licensed under the MIT License.

---

## Credits

Developed by [Lokesh_Kumar].  
Inspired by open-source security research and the ethical hacking community.

---
