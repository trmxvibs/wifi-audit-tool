# test_scan.py
def test_wifi_scanner_returns_results():
    result = scan_wifi()
    assert len(result) > 0
