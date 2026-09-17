import json

import normalize_run as nr

FLAT = [
    {"ts": 100.0, "kind": "start", "from": "referee", "to": "referee", "chars": 0},
    {"ts": 101.0, "kind": "spawn", "from": "referee", "to": "manny", "chars": 10},
    {"ts": 120.0, "kind": "message", "from": "manny", "to": "main", "chars": 30},
    {"ts": 130.0, "kind": "report", "from": "manny", "to": "referee", "chars": 0},
    {"ts": 140.0, "kind": "end", "from": "referee", "to": "referee", "chars": 0},
]


def test_lead_is_read_from_the_start_record():
    assert nr.lead_of(FLAT) == "referee"


def test_lead_is_none_without_a_start_record():
    assert nr.lead_of([{"ts": 1.0, "kind": "report", "from": "a", "to": "b", "chars": 0}]) is None


def test_a_message_to_the_main_session_is_attributed_to_the_lead():
    out = nr.normalize(FLAT)
    assert out[2]["to"] == "referee"
    # Everything else is untouched, including the record count.
    assert len(out) == len(FLAT)
    assert [r["kind"] for r in out] == [r["kind"] for r in FLAT]


def test_an_explicit_alias_renames_both_endpoints():
    records = [
        {"ts": 1.0, "kind": "start", "from": "manny", "to": "manny", "chars": 0},
        {"ts": 2.0, "kind": "message", "from": "manny", "to": "deadbeef1234", "chars": 5},
        {"ts": 3.0, "kind": "report", "from": "deadbeef1234", "to": "manny", "chars": 0},
    ]
    out = nr.normalize(records, aliases={"deadbeef1234": "codie"})
    assert out[1]["to"] == "codie"
    assert out[2]["from"] == "codie"


def test_an_unmapped_alias_is_left_alone():
    records = [
        {"ts": 1.0, "kind": "start", "from": "manny", "to": "manny", "chars": 0},
        {"ts": 2.0, "kind": "message", "from": "manny", "to": "cafe9876", "chars": 5},
    ]
    assert nr.normalize(records)[1]["to"] == "cafe9876"


def test_unknown_names_are_reported_so_nothing_is_silently_renamed():
    records = [
        {"ts": 1.0, "kind": "start", "from": "manny", "to": "manny", "chars": 0},
        {"ts": 2.0, "kind": "spawn", "from": "manny", "to": "codie", "chars": 5},
        {"ts": 3.0, "kind": "message", "from": "manny", "to": "deadbeef1234", "chars": 5},
    ]
    assert nr.unresolved(records) == {"deadbeef1234"}
    assert nr.unresolved(nr.normalize(records, aliases={"deadbeef1234": "codie"})) == set()


def test_a_name_only_ever_spawned_is_not_unresolved():
    assert nr.unresolved(FLAT) == {"main"}
    assert nr.unresolved(nr.normalize(FLAT)) == set()


def test_main_writes_the_normalized_log(tmp_path, capsys):
    src = tmp_path / "flat.jsonl"
    src.write_text("".join(json.dumps(r) + "\n" for r in FLAT))
    out = tmp_path / "out.jsonl"
    nr.main([str(src), "-o", str(out)])
    written = [json.loads(line) for line in out.read_text().splitlines()]
    assert written[2]["to"] == "referee"


def test_main_refuses_a_log_it_cannot_fully_resolve(tmp_path, capsys):
    src = tmp_path / "hub.jsonl"
    src.write_text(
        json.dumps({"ts": 1.0, "kind": "start", "from": "manny", "to": "manny", "chars": 0}) + "\n"
        + json.dumps({"ts": 2.0, "kind": "message", "from": "manny", "to": "deadbeef1234", "chars": 5}) + "\n"
    )
    out = tmp_path / "out.jsonl"
    assert nr.main([str(src), "-o", str(out)]) == 1
    assert "deadbeef1234" in capsys.readouterr().err
    assert not out.exists()
