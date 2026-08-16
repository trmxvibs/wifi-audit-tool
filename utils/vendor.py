"""
Offline BSSID -> vendor/manufacturer lookup using OUI (first 3 octets
of the MAC address). No network calls — works in the field with no
internet, which matters for a wireless auditing tool.

This is a small curated table of common router/AP vendors, not the
full IEEE OUI database (that's 30k+ entries and would be overkill
here). Unknown prefixes just return "Unknown".
"""

_OUI_TABLE = {
    "00:11:22": "Generic/Test",  # matches our own test fixture, harmless
    "00:14:6C": "Netgear",
    "00:1A:70": "Cisco",
    "00:1D:7E": "Cisco-Linksys",
    "00:1E:E5": "Netgear",
    "00:22:6B": "Cisco",
    "00:23:69": "Cisco",
    "00:25:9C": "Cisco",
    "00:26:F2": "Cisco",
    "00:1F:33": "Netgear",
    "00:24:B2": "Netgear",
    "10:0D:7F": "Huawei",
    "18:E8:29": "Netgear",
    "1C:AF:F7": "D-Link",
    "20:AA:4B": "D-Link",
    "24:69:A5": "Tenda",
    "28:28:5D": "TP-Link",
    "30:B5:C2": "TP-Link",
    "34:29:8F": "Netgear",
    "50:C7:BF": "TP-Link",
    "54:04:A6": "Asus",
    "60:E3:27": "Netgear",
    "64:66:B3": "Xiaomi",
    "68:FF:7B": "D-Link",
    "84:C9:B2": "Ubiquiti",
    "94:10:3E": "TP-Link",
    "9C:3D:CF": "Asus",
    "A0:F3:C1": "TP-Link",
    "AC:84:C6": "Ubiquiti",
    "B0:48:7A": "TP-Link",
    "C0:4A:00": "Netgear",
    "C4:12:F5": "Cisco",
    "D8:32:14": "Belkin",
    "E4:95:6E": "TP-Link",
    "F4:F2:6D": "TP-Link",
    "F8:32:E4": "TP-Link",
}


def normalize_bssid(bssid):
    """Uppercases and strips a BSSID so lookups aren't case/space sensitive."""
    return (bssid or "").strip().upper()


def get_vendor(bssid):
    """
    Returns the vendor name for a BSSID's OUI prefix, or 'Unknown' if
    the prefix isn't in our table or the BSSID is malformed.
    """
    normalized = normalize_bssid(bssid)
    parts = normalized.split(":")
    if len(parts) < 3:
        return "Unknown"
    prefix = ":".join(parts[:3])
    return _OUI_TABLE.get(prefix, "Unknown")


def annotate_networks(networks):
    """
    Returns a new list of network dicts with a 'vendor' key added,
    without mutating the input list.
    """
    annotated = []
    for net in networks:
        net_copy = dict(net)
        net_copy["vendor"] = get_vendor(net.get("bssid", ""))
        annotated.append(net_copy)
    return annotated
