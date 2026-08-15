"""
Persists each scan's results to a local JSONL (one JSON object per
line) history file, so scans can be tracked over time — e.g. "has
this network always been open, or did it change last week?"

JSONL instead of a single JSON array so appending never requires
reading + rewriting the whole file.
"""
import json
import os
from datetime import datetime, timezone

DEFAULT_HISTORY_PATH = "scan_history.jsonl"


def append_scan(networks, findings, path=DEFAULT_HISTORY_PATH):
    """
    Appends one scan's results as a single JSON line. Returns the
    record that was written.
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "network_count": len(networks),
        "networks": networks,
        "findings": [{"severity": sev, "message": msg} for sev, msg in findings],
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record


def load_history(path=DEFAULT_HISTORY_PATH):
    """
    Returns all past scan records as a list, oldest first. Returns an
    empty list if the history file doesn't exist yet, and silently
    skips any line that isn't valid JSON (e.g. a truncated last write)
    rather than crashing the caller.
    """
    if not os.path.exists(path):
        return []

    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def summarize_history(path=DEFAULT_HISTORY_PATH):
    """
    Returns a short list of (timestamp, network_count, high_findings_count)
    tuples for display in the menu's "Scan History" option.
    """
    records = load_history(path)
    summary = []
    for rec in records:
        high_count = sum(
            1 for f in rec.get("findings", []) if f.get("severity") == "high"
        )
        summary.append((rec.get("timestamp", "?"), rec.get("network_count", 0), high_count))
    return summary
