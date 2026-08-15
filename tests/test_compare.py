from modules.compare import diff_scans, format_diff_summary

OLD = [
    {"bssid": "AA:AA:AA:AA:AA:AA", "essid": "StaysSame", "privacy": "WPA2"},
    {"bssid": "BB:BB:BB:BB:BB:BB", "essid": "WillDisappear", "privacy": "WPA2"},
    {"bssid": "CC:CC:CC:CC:CC:CC", "essid": "GetsWeaker", "privacy": "WPA2"},
]

NEW = [
    {"bssid": "AA:AA:AA:AA:AA:AA", "essid": "StaysSame", "privacy": "WPA2"},
    {"bssid": "CC:CC:CC:CC:CC:CC", "essid": "GetsWeaker", "privacy": "OPN"},
    {"bssid": "DD:DD:DD:DD:DD:DD", "essid": "BrandNew", "privacy": "WPA2"},
]


def test_diff_detects_new_network():
    diff = diff_scans(OLD, NEW)
    new_bssids = {n["bssid"] for n in diff["new"]}
    assert "DD:DD:DD:DD:DD:DD" in new_bssids


def test_diff_detects_missing_network():
    diff = diff_scans(OLD, NEW)
    missing_bssids = {n["bssid"] for n in diff["missing"]}
    assert "BB:BB:BB:BB:BB:BB" in missing_bssids


def test_diff_detects_security_change_and_direction():
    diff = diff_scans(OLD, NEW)
    changed = diff["changed"]
    assert len(changed) == 1
    assert changed[0]["bssid"] == "CC:CC:CC:CC:CC:CC"
    assert changed[0]["old_privacy"] == "WPA2"
    assert changed[0]["new_privacy"] == "OPN"
    assert changed[0]["weaker"] is True


def test_diff_unchanged_network_not_in_changed_list():
    diff = diff_scans(OLD, NEW)
    changed_bssids = {c["bssid"] for c in diff["changed"]}
    assert "AA:AA:AA:AA:AA:AA" not in changed_bssids


def test_diff_no_changes_returns_empty_lists():
    diff = diff_scans(OLD, OLD)
    assert diff["new"] == []
    assert diff["missing"] == []
    assert diff["changed"] == []


def test_format_diff_summary_no_changes():
    diff = {"new": [], "missing": [], "changed": []}
    lines = format_diff_summary(diff)
    assert lines == ["No changes detected since the last scan."]


def test_format_diff_summary_includes_all_categories():
    diff = diff_scans(OLD, NEW)
    lines = format_diff_summary(diff)
    joined = " ".join(lines)
    assert "BrandNew" in joined
    assert "WillDisappear" in joined
    assert "GetsWeaker" in joined
    assert "WEAKER" in joined
