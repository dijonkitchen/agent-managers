import json

import log_messages as lm


def test_agent_spawn_from_lead_records_lead_to_named_agent():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "tool_input": {"name": "rocky", "subagent_type": "rocky", "prompt": "go"},
    }
    rec = lm.to_record(event, lead="manny", now=100.0)
    assert rec == {"ts": 100.0, "kind": "spawn", "from": "manny", "to": "rocky", "chars": 2}


def test_agent_spawn_falls_back_to_subagent_type_when_unnamed():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "ivory", "prompt": "read"},
    }
    rec = lm.to_record(event, lead="lead", now=1.0)
    assert rec["to"] == "ivory"


def test_send_message_inside_subagent_uses_agent_type_as_sender():
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "SendMessage",
        "agent_type": "rocky",
        "tool_input": {"to": "ivory", "message": "shipped it"},
    }
    rec = lm.to_record(event, lead="referee", now=2.0)
    assert rec == {"ts": 2.0, "kind": "message", "from": "rocky", "to": "ivory", "chars": 10}


def test_subagent_stop_records_report_back_to_lead():
    event = {"hook_event_name": "SubagentStop", "agent_type": "ivory"}
    rec = lm.to_record(event, lead="manny", now=3.0)
    assert rec == {"ts": 3.0, "kind": "report", "from": "ivory", "to": "manny", "chars": 0}


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
        "tool_input": {"name": "rocky", "prompt": "hi"},
    }
    lm.main(json.dumps(event))
    lines = log.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["to"] == "rocky"


def test_main_ignores_malformed_input(tmp_path, monkeypatch):
    log = tmp_path / "run.jsonl"
    monkeypatch.setenv("AGENT_LOG", str(log))
    lm.main("not json")
    assert not log.exists()
