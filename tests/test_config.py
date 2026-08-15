from utils import config as config_module


def test_load_config_missing_file_returns_defaults(tmp_path):
    path = str(tmp_path / "no_such_config.json")
    loaded = config_module.load_config(path=path)
    assert loaded == config_module.DEFAULTS


def test_save_and_load_config_roundtrip(tmp_path):
    path = str(tmp_path / "config.json")
    config_module.save_config({"iface": "wlan0", "scan_duration": 60,
                                "export_format": "csv", "history_path": "hist.jsonl"}, path=path)
    loaded = config_module.load_config(path=path)
    assert loaded["iface"] == "wlan0"
    assert loaded["scan_duration"] == 60


def test_load_config_corrupt_file_falls_back_to_defaults(tmp_path):
    path = str(tmp_path / "bad_config.json")
    with open(path, "w") as f:
        f.write("{not valid json")
    loaded = config_module.load_config(path=path)
    assert loaded == config_module.DEFAULTS


def test_set_default_updates_one_key_and_persists(tmp_path):
    path = str(tmp_path / "config.json")
    config_module.set_default("scan_duration", 45, path=path)
    loaded = config_module.load_config(path=path)
    assert loaded["scan_duration"] == 45
    assert loaded["iface"] is None  # untouched keys keep their default


def test_set_default_unknown_key_raises():
    try:
        config_module.set_default("not_a_real_key", "x", path="/tmp/unused.json")
        assert False, "expected KeyError"
    except KeyError:
        pass
