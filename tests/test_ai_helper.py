from utils.ai_helper import classify_network, suggest_network


def test_classify_open_network_is_high_severity():
    net = {'essid': 'FreeWiFi', 'privacy': 'OPN'}
    severity, message = classify_network(net)
    assert severity == 'high'
    assert 'FreeWiFi' in message


def test_classify_wep_network_is_high_severity():
    net = {'essid': 'OldRouter', 'privacy': 'WEP'}
    severity, message = classify_network(net)
    assert severity == 'high'


def test_classify_wpa2_network_is_fine():
    net = {'essid': 'HomeNetwork', 'privacy': 'WPA2', 'cipher': 'CCMP'}
    assert classify_network(net) is None


def test_suggest_network_sorts_high_before_medium(capsys):
    networks = [
        {'essid': 'A', 'privacy': 'WPA'},   # medium
        {'essid': 'B', 'privacy': 'WEP'},   # high
    ]
    findings = suggest_network(networks)
    assert findings[0][0] == 'high'
    assert findings[1][0] == 'medium'


def test_suggest_network_empty_list_returns_empty(capsys):
    assert suggest_network([]) == []
