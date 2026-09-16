import metrics as m

HUB = [
    {"ts": 100.0, "kind": "spawn", "from": "manny", "to": "archie", "chars": 40},
    {"ts": 130.0, "kind": "report", "from": "archie", "to": "manny", "chars": 0},
    {"ts": 131.0, "kind": "spawn", "from": "manny", "to": "codie", "chars": 60},
    {"ts": 190.0, "kind": "report", "from": "codie", "to": "manny", "chars": 0},
]
FLAT = [
    {"ts": 100.0, "kind": "spawn", "from": "referee", "to": "codie", "chars": 20},
    {"ts": 100.5, "kind": "spawn", "from": "referee", "to": "archie", "chars": 20},
    {"ts": 105.0, "kind": "message", "from": "codie", "to": "archie", "chars": 30},
    {"ts": 120.0, "kind": "message", "from": "archie", "to": "codie", "chars": 80},
    {"ts": 121.0, "kind": "message", "from": "codie", "to": "archie", "chars": 10},
    {"ts": 150.0, "kind": "report", "from": "codie", "to": "referee", "chars": 0},
]


def test_summarize_counts_by_kind_and_wall_time():
    s = m.summarize(HUB)
    assert s == {
        "spawns": 2, "messages": 0, "reports": 2, "total": 4,
        "chars": 100, "edges": 4, "wall_seconds": 90.0,
    }


def test_summarize_flat_has_peer_edges():
    s = m.summarize(FLAT)
    assert s["messages"] == 3
    assert s["edges"] == 5
    assert s["wall_seconds"] == 50.0


def test_summarize_empty_run():
    assert m.summarize([])["wall_seconds"] == 0.0


def test_markdown_table_has_one_column_per_run():
    md = m.to_markdown({"hub": m.summarize(HUB), "flat": m.summarize(FLAT)})
    lines = md.splitlines()
    assert lines[0] == "| Metric | hub | flat |"
    assert "| Messages | 0 | 3 |" in lines
    assert "| Wall time (s) | 90 | 50 |" in lines


SOLO = [
    {"ts": 100.0, "kind": "start", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 160.0, "kind": "end", "from": "solo", "to": "solo", "chars": 0},
]


def test_start_and_end_set_wall_time_but_do_not_count_as_hops():
    s = m.summarize(SOLO)
    assert s["total"] == 0
    assert s["edges"] == 0
    assert s["wall_seconds"] == 60.0
