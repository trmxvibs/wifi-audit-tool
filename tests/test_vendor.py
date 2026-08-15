from utils.vendor import get_vendor, annotate_networks, normalize_bssid


def test_get_vendor_known_prefix():
    assert get_vendor("28:28:5D:11:22:33") == "TP-Link"


def test_get_vendor_is_case_insensitive():
    assert get_vendor("28:28:5d:11:22:33") == "TP-Link"


def test_get_vendor_unknown_prefix_returns_unknown():
    assert get_vendor("FF:FF:FF:00:00:00") == "Unknown"


def test_get_vendor_malformed_bssid_returns_unknown():
    assert get_vendor("not-a-mac") == "Unknown"
    assert get_vendor("") == "Unknown"
    assert get_vendor(None) == "Unknown"


def test_normalize_bssid_strips_and_uppercases():
    assert normalize_bssid("  28:28:5d:11:22:33 ") == "28:28:5D:11:22:33"


def test_annotate_networks_adds_vendor_without_mutating_input():
    networks = [{"bssid": "28:28:5D:11:22:33", "essid": "Test"}]
    annotated = annotate_networks(networks)

    assert annotated[0]["vendor"] == "TP-Link"
    assert "vendor" not in networks[0]  # original list untouched
