import json

import log_messages as lm


def test_agent_spawn_from_lead_records_lead_to_named_agent():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "tool_input": {"name": "codie", "subagent_type": "codie", "prompt": "go"},
    }
    rec = lm.to_record(event, lead="manny", now=100.0)
    assert rec == {"ts": 100.0, "kind": "spawn", "from": "manny", "to": "codie", "chars": 2}


def test_agent_spawn_falls_back_to_subagent_type_when_unnamed():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "archie", "prompt": "read"},
    }
    rec = lm.to_record(event, lead="lead", now=1.0)
    assert rec["to"] == "archie"


def test_send_message_inside_subagent_uses_agent_type_as_sender():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "SendMessage",
        "agent_type": "codie",
        "tool_input": {"to": "archie", "message": "shipped it"},
    }
    rec = lm.to_record(event, lead="referee", now=2.0)
    assert rec == {"ts": 2.0, "kind": "message", "from": "codie", "to": "archie", "chars": 10}


def test_subagent_stop_records_report_back_to_lead():
    event = {"hook_event_name": "SubagentStop", "agent_type": "archie"}
    rec = lm.to_record(event, lead="manny", now=3.0)
    assert rec == {"ts": 3.0, "kind": "report", "from": "archie", "to": "manny", "chars": 0}


def test_unrelated_tool_is_ignored():
    event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "ls"}}
    assert lm.to_record(event, lead="lead", now=0.0) is None


def test_main_appends_one_json_line(tmp_path, monkeypatch, capsys):
    log = tmp_path / "run.jsonl"
    monkeypatch.setenv("AGENT_LOG", str(log))
    monkeypatch.setenv("AGENT_LEAD_NAME", "manny")
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "tool_input": {"name": "codie", "prompt": "hi"},
    }
    lm.main(json.dumps(event))
    lines = log.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["to"] == "codie"


def test_main_ignores_malformed_input(tmp_path, monkeypatch):
    log = tmp_path / "run.jsonl"
    monkeypatch.setenv("AGENT_LOG", str(log))
    lm.main("not json")
    assert not log.exists()


def test_session_start_and_end_record_self_edges_for_the_lead():
    start = lm.to_record({"hook_event_name": "SessionStart"}, lead="solo", now=5.0)
    end = lm.to_record({"hook_event_name": "SessionEnd"}, lead="solo", now=9.0)
    assert start == {"ts": 5.0, "kind": "start", "from": "solo", "to": "solo", "chars": 0}
    assert end == {"ts": 9.0, "kind": "end", "from": "solo", "to": "solo", "chars": 0}


def test_session_start_inside_named_session_uses_agent_type():
    rec = lm.to_record({"hook_event_name": "SessionStart", "agent_type": "manny"}, lead="x", now=1.0)
    assert rec["from"] == "manny"


def test_send_message_to_the_main_session_resolves_to_the_lead():
    # A teammate addressing the referee session as "main" is talking to the
    # lead. Recording the raw name makes one session two nodes, which adds a
    # phantom edge to the graph and breaks the flat peer-edge count.
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "SendMessage",
        "agent_type": "manny",
        "tool_input": {"to": "main", "message": "done"},
    }
    rec = lm.to_record(event, lead="referee", now=4.0)
    assert rec == {"ts": 4.0, "kind": "message", "from": "manny", "to": "referee", "chars": 4}


def test_send_message_to_a_peer_named_like_nothing_special_is_untouched():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "SendMessage",
        "agent_type": "manny",
        "tool_input": {"to": "codie", "message": "done"},
    }
    assert lm.to_record(event, lead="referee", now=4.0)["to"] == "codie"
