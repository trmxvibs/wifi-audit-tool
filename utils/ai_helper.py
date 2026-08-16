"""
Simple rule-based security analysis for scanned networks.

Not actually "AI" (no model involved) — this is a rule-based classifier.
Named ai_helper for now to match the existing menu wiring; consider
renaming to security_advisor.py in a future cleanup.

Consumes the list-of-dicts shape produced by modules.scan.parse_airodump_csv:
    {'bssid', 'channel', 'privacy', 'cipher', 'authentication', 'power', 'essid'}
"""

WEAK_PRIVACY = {"WEP"}
OPEN_PRIVACY = {"OPN", "OPEN", ""}


def classify_network(net):
    """Returns (severity, message) for a single network dict, or None if fine."""
    privacy = net.get('privacy', '').upper()
    essid = net.get('essid', '(unknown)')

    if privacy in OPEN_PRIVACY:
        return ("high", f"{essid} is an OPEN network (no encryption) — traffic is readable by anyone nearby.")
    if privacy in WEAK_PRIVACY:
        return ("high", f"{essid} uses WEP — broken since ~2005, crackable in minutes.")
    if privacy == "WPA":
        return ("medium", f"{essid} uses WPA (not WPA2/3) — vulnerable to known TKIP attacks.")
    if privacy == "WPA2" and "WPS" in net.get('cipher', '').upper():
        return ("medium", f"{essid} is WPA2 with WPS active — WPS PIN attacks may apply.")
    return None


def suggest_network(networks):
    """
    Analyzes a list of network dicts and prints security recommendations,
    sorted worst-first. Returns the list of (severity, message) findings
    so callers (e.g. report export) can reuse them instead of re-parsing.
    """
    if not networks:
        print("\nNo networks to analyze.")
        return []

    findings = []
    for net in networks:
        result = classify_network(net)
        if result:
            findings.append(result)

    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: severity_order.get(f[0], 3))

    print("\nSecurity Recommendations:")
    if not findings:
        print("- All scanned networks appear to use modern security (WPA2/WPA3, no WPS flagged).")
    else:
        for severity, message in findings:
            tag = "[HIGH]" if severity == "high" else "[MED] "
            print(f"- {tag} {message}")

    return findings
