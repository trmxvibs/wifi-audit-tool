import json
from modules import report

SAMPLE_NETWORKS = [
    {'bssid': '00:11:22:33:44:55', 'essid': 'HomeNetwork', 'channel': '6',
     'privacy': 'WPA2', 'power': '-45'},
]
SAMPLE_FINDINGS = [('high', 'FreeWiFi is an OPEN network')]


def test_export_json_writes_valid_json(tmp_path):
    out = tmp_path / "report.json"
    report.export_json(SAMPLE_NETWORKS, SAMPLE_FINDINGS, str(out))

    data = json.loads(out.read_text())
    assert data['network_count'] == 1
    assert data['networks'][0]['essid'] == 'HomeNetwork'
    assert data['findings'][0]['severity'] == 'high'
    assert 'generated_at' in data


def test_export_html_writes_valid_html(tmp_path):
    out = tmp_path / "report.html"
    report.export_html(SAMPLE_NETWORKS, SAMPLE_FINDINGS, str(out))

    html = out.read_text()
    assert '<html' in html
    assert 'HomeNetwork' in html
    assert 'FreeWiFi is an OPEN network' in html


def test_export_html_escapes_essid_to_prevent_injection(tmp_path):
    """A malicious/odd SSID like <script> should not break out of the HTML."""
    networks = [{'bssid': 'AA:BB:CC:DD:EE:FF', 'essid': '<script>alert(1)</script>',
                 'channel': '1', 'privacy': 'OPN', 'power': '-50'}]
    out = tmp_path / "report.html"
    report.export_html(networks, [], str(out))

    html = out.read_text()
    assert '<script>alert(1)</script>' not in html
    assert '&lt;script&gt;' in html


def test_export_csv_writes_valid_csv_with_header(tmp_path):
    import csv
    out = tmp_path / "report.csv"
    networks = [{'bssid': '00:11:22:33:44:55', 'essid': 'HomeNetwork', 'channel': '6',
                 'privacy': 'WPA2', 'cipher': 'CCMP', 'authentication': 'PSK',
                 'power': '-45', 'vendor': 'TP-Link'}]
    report.export_csv(networks, str(out))

    with open(out, newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]['essid'] == 'HomeNetwork'
    assert rows[0]['vendor'] == 'TP-Link'


def test_export_csv_missing_fields_default_to_empty(tmp_path):
    import csv
    out = tmp_path / "report.csv"
    report.export_csv([{'bssid': 'AA:BB:CC:DD:EE:FF'}], str(out))  # no essid, vendor, etc.

    with open(out, newline='') as f:
        rows = list(csv.DictReader(f))
    assert rows[0]['essid'] == ''
    assert rows[0]['vendor'] == ''
