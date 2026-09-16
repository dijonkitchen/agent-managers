#!/usr/bin/env python3
"""Claude Code hook: append one JSONL record per spawn, message, or report.

Wired in .claude/settings.json for PreToolUse (Agent, SendMessage),
SubagentStop, SessionStart, and SessionEnd. Start and end are self-edges
so a run with no spawns still has a node and a wall time. Reads the hook event from stdin and appends to $AGENT_LOG
(default demo/runs/current.jsonl). The lead's name comes from
$AGENT_LEAD_NAME (default "lead") because the main session's hook input
only carries agent_type when started with --agent.

Record shape: {"ts", "kind", "from", "to", "chars"}.
"""

from __future__ import annotations

import json
import os
import sys
import time

DEFAULT_LOG = "demo/runs/current.jsonl"

# Names a teammate may use for the main session. It is the lead, so recording
# the raw name would draw one session as two nodes.
MAIN_SESSION_ALIASES = frozenset({"main"})


def to_record(event: dict, lead: str, now: float) -> dict | None:
    sender = event.get("agent_type") or lead
    name = event.get("hook_event_name")

    if name == "SubagentStop":
        return {"ts": now, "kind": "report", "from": sender, "to": lead, "chars": 0}
    if name in ("SessionStart", "SessionEnd"):
        kind = "start" if name == "SessionStart" else "end"
        return {"ts": now, "kind": kind, "from": sender, "to": sender, "chars": 0}

    if name != "PreToolUse":
        return None

    tool = event.get("tool_name")
    args = event.get("tool_input") or {}
    if tool == "Agent":
        to = args.get("name") or args.get("subagent_type") or "agent"
        return {"ts": now, "kind": "spawn", "from": sender, "to": to,
                "chars": len(args.get("prompt", ""))}
    if tool == "SendMessage":
        to = args.get("to", "?")
        return {"ts": now, "kind": "message", "from": sender,
                "to": lead if to in MAIN_SESSION_ALIASES else to,
                "chars": len(args.get("message", ""))}
    return None


def main(raw: str) -> None:
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        return
    record = to_record(event, lead=os.environ.get("AGENT_LEAD_NAME", "lead"), now=time.time())
    if record is None:
        return
    path = os.environ.get("AGENT_LOG", DEFAULT_LOG)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main(sys.stdin.read())
