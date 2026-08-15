"""
Compares two scan results (e.g. today's scan vs. last week's from
history) to answer: what's new, what's gone, and did any network's
security get weaker or stronger.

Networks are matched by BSSID (the stable identifier) rather than
ESSID, since two different APs can share the same SSID.
"""

# Rough ordering so we can tell "got weaker" from "got stronger".
# Higher number = weaker security.
_SECURITY_RANK = {
    "WPA3": 0,
    "WPA2": 1,
    "WPA": 2,
    "WEP": 3,
    "OPN": 4,
    "OPEN": 4,
    "": 5,  # unknown/blank privacy field
}


def _rank(privacy):
    return _SECURITY_RANK.get((privacy or "").upper(), 5)


def diff_scans(old_networks, new_networks):
    """
    Returns a dict describing the difference between two scans:
      - 'new':     networks present now but not in the old scan
      - 'missing': networks present before but not seen now
      - 'changed': networks present in both, whose 'privacy' field
                   differs, with 'weaker' (bool) telling direction
    """
    old_by_bssid = {n.get("bssid"): n for n in old_networks if n.get("bssid")}
    new_by_bssid = {n.get("bssid"): n for n in new_networks if n.get("bssid")}

    new_list = [n for bssid, n in new_by_bssid.items() if bssid not in old_by_bssid]
    missing_list = [n for bssid, n in old_by_bssid.items() if bssid not in new_by_bssid]

    changed = []
    for bssid, new_net in new_by_bssid.items():
        old_net = old_by_bssid.get(bssid)
        if old_net is None:
            continue
        old_privacy = old_net.get("privacy", "")
        new_privacy = new_net.get("privacy", "")
        if old_privacy != new_privacy:
            changed.append({
                "bssid": bssid,
                "essid": new_net.get("essid", old_net.get("essid", "")),
                "old_privacy": old_privacy,
                "new_privacy": new_privacy,
                "weaker": _rank(new_privacy) > _rank(old_privacy),
            })

    return {"new": new_list, "missing": missing_list, "changed": changed}


def format_diff_summary(diff):
    """Returns a short list of human-readable strings describing a diff."""
    lines = []
    for n in diff["new"]:
        lines.append(f"[NEW] {n.get('essid', '(hidden)')} ({n.get('bssid', '?')})")
    for n in diff["missing"]:
        lines.append(f"[GONE] {n.get('essid', '(hidden)')} ({n.get('bssid', '?')})")
    for c in diff["changed"]:
        direction = "WEAKER" if c["weaker"] else "stronger"
        lines.append(
            f"[CHANGED] {c['essid']} ({c['bssid']}): "
            f"{c['old_privacy']} -> {c['new_privacy']} ({direction})"
        )
    if not lines:
        lines.append("No changes detected since the last scan.")
    return lines
