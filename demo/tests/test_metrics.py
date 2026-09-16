import json
import sys

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
        "chars": 100, "edges": 4, "work_seconds": 90.0, "wall_seconds": 90.0,
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
    assert "| Work time (s) | 90 | 50 |" in lines
    assert "| Session time (s) | 90 | 50 |" in lines


SOLO = [
    {"ts": 100.0, "kind": "start", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 160.0, "kind": "end", "from": "solo", "to": "solo", "chars": 0},
]


def test_start_and_end_set_wall_time_but_do_not_count_as_hops():
    s = m.summarize(SOLO)
    assert s["total"] == 0
    assert s["edges"] == 0
    assert s["wall_seconds"] == 60.0


# What the captured solo run actually held: SubagentStop fired twice in a
# session started with `--disallowedTools Agent`, so nothing could have
# reported to anyone. The hook no longer writes these, but logs captured
# before that fix still carry them.
SOLO_WITH_PHANTOM_REPORTS = [
    {"ts": 100.0, "kind": "start", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 130.0, "kind": "report", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 145.0, "kind": "report", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 160.0, "kind": "end", "from": "solo", "to": "solo", "chars": 0},
]


def test_a_report_to_self_is_not_a_hop():
    s = m.summarize(SOLO_WITH_PHANTOM_REPORTS)
    assert s["reports"] == 0
    assert s["total"] == 0
    assert s["edges"] == 0
    assert s["wall_seconds"] == 60.0


def test_work_time_spans_the_hops_not_the_open_session():
    """The three captured runs were opened and closed together in one sitting.

    Their session spans came out 4215.8s, 4200.3s and 4192.0s -- an artifact
    of when the operator quit, not of how long any topology took. The span
    from first hop to last is the part that is about the run.
    """
    assert m.summarize(HUB)["work_seconds"] == 90.0
    assert m.summarize(FLAT)["work_seconds"] == 50.0


def test_a_run_with_no_hops_has_no_work_time():
    assert m.summarize(SOLO)["work_seconds"] == 0.0
    assert m.summarize([])["work_seconds"] == 0.0


def test_markdown_table_carries_a_provenance_note():
    md = m.to_markdown({"hub": m.summarize(HUB)}, note="Captured run.")
    assert md.splitlines()[0] == "| Metric | hub |"
    assert md.rstrip().endswith("Captured run.")


def test_markdown_table_without_a_note_is_just_the_table():
    assert m.to_markdown({"hub": m.summarize(HUB)}).rstrip().endswith("|")


def test_note_file_carries_prose_the_makefile_could_not_quote(tmp_path, monkeypatch):
    """PROVENANCE.txt is prose, so interpolating it into the recipe broke on
    the first apostrophe. The caption is read from the file instead."""
    run = tmp_path / "hub.jsonl"
    run.write_text("".join(json.dumps(r) + "\n" for r in HUB))
    note = tmp_path / "PROVENANCE.txt"
    note.write_text("Captured run. Session time measures the sitting, not the run's work.\n")
    out = tmp_path / "metrics.md"
    monkeypatch.setattr(
        sys, "argv",
        ["metrics.py", f"hub={run}", "--note-file", str(note), "-o", str(out)],
    )
    m.main()
    assert out.read_text().rstrip().endswith("not the run's work.")
