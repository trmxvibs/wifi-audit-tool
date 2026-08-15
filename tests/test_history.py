from modules import history

SAMPLE_NETWORKS = [{"bssid": "AA:BB:CC:DD:EE:FF", "essid": "TestNet", "privacy": "OPN"}]
SAMPLE_FINDINGS = [("high", "TestNet is an OPEN network")]


def test_append_scan_writes_a_jsonl_line(tmp_path):
    path = str(tmp_path / "history.jsonl")
    history.append_scan(SAMPLE_NETWORKS, SAMPLE_FINDINGS, path=path)

    with open(path) as f:
        lines = f.readlines()
    assert len(lines) == 1


def test_load_history_missing_file_returns_empty_list(tmp_path):
    path = str(tmp_path / "does_not_exist.jsonl")
    assert history.load_history(path=path) == []


def test_load_history_returns_records_oldest_first(tmp_path):
    path = str(tmp_path / "history.jsonl")
    history.append_scan(SAMPLE_NETWORKS, SAMPLE_FINDINGS, path=path)
    history.append_scan([], [], path=path)

    records = history.load_history(path=path)
    assert len(records) == 2
    assert records[0]["network_count"] == 1
    assert records[1]["network_count"] == 0


def test_load_history_skips_corrupt_lines(tmp_path):
    path = str(tmp_path / "history.jsonl")
    history.append_scan(SAMPLE_NETWORKS, SAMPLE_FINDINGS, path=path)
    with open(path, "a") as f:
        f.write("not valid json\n")

    records = history.load_history(path=path)
    assert len(records) == 1  # corrupt line skipped, not crashed on


def test_summarize_history_counts_high_findings(tmp_path):
    path = str(tmp_path / "history.jsonl")
    history.append_scan(SAMPLE_NETWORKS, SAMPLE_FINDINGS, path=path)

    summary = history.summarize_history(path=path)
    assert len(summary) == 1
    _, net_count, high_count = summary[0]
    assert net_count == 1
    assert high_count == 1
