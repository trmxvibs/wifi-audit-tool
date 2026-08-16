"""
Loads/saves a small local JSON config file storing defaults
(interface, scan duration, export format) so the user doesn't have
to retype the same CLI flags every run. CLI flags, when given, still
always win over the config file.
"""
import json
import os

DEFAULT_CONFIG_PATH = ".wifi_audit_config.json"

DEFAULTS = {
    "iface": None,
    "scan_duration": 30,
    "export_format": "json",
    "history_path": "scan_history.jsonl",
}


def load_config(path=DEFAULT_CONFIG_PATH):
    """
    Returns the saved config merged over DEFAULTS. Missing file or
    invalid JSON both fall back to DEFAULTS rather than crashing —
    a broken config file shouldn't stop the tool from running.
    """
    config = dict(DEFAULTS)
    if not os.path.exists(path):
        return config
    try:
        with open(path, "r", encoding="utf-8") as f:
            saved = json.load(f)
        if isinstance(saved, dict):
            config.update(saved)
    except (json.JSONDecodeError, OSError):
        pass
    return config


def save_config(config, path=DEFAULT_CONFIG_PATH):
    """Writes the given config dict to disk as JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def set_default(key, value, path=DEFAULT_CONFIG_PATH):
    """Loads the current config, updates one key, and saves it back."""
    if key not in DEFAULTS:
        raise KeyError(f"Unknown config key: {key}")
    config = load_config(path)
    config[key] = value
    save_config(config, path)
    return config
