import os
from modules.scan import parse_airodump_csv

FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_scan-01.csv')


def test_parse_airodump_csv_returns_only_ap_section():
    """Should parse 3 APs and stop before the Station MAC section."""
    networks = parse_airodump_csv(FIXTURE)
    assert len(networks) == 3


def test_parse_airodump_csv_extracts_expected_fields():
    networks = parse_airodump_csv(FIXTURE)
    home = next(n for n in networks if n['essid'] == 'HomeNetwork')
    assert home['bssid'] == '00:11:22:33:44:55'
    assert home['channel'] == '6'
    assert home['privacy'] == 'WPA2'
    assert home['power'] == '-45'


def test_parse_airodump_csv_handles_open_and_wep():
    networks = parse_airodump_csv(FIXTURE)
    privacies = {n['essid']: n['privacy'] for n in networks}
    assert privacies['FreeWiFi'] == 'OPN'
    assert privacies['OldRouter'] == 'WEP'


def test_parse_airodump_csv_missing_file_returns_empty_list():
    assert parse_airodump_csv('/tmp/does_not_exist_12345.csv') == []


def test_parse_airodump_csv_no_header_returns_empty_list(tmp_path):
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text("not,a,real,airodump,file\n")
    assert parse_airodump_csv(str(bad_file)) == []
