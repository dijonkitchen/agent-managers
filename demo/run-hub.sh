#!/usr/bin/env bash
# Hub-and-spoke run: Manny is the session. Rocky and Ivory are subagents
# that can only report back to Manny. They have no SendMessage tool, so
# the topology is enforced by the mechanism, not by the prompt.
set -euo pipefail
cd "$(dirname "$0")/.."

export AGENT_LOG=demo/runs/hub.jsonl
export AGENT_LEAD_NAME=manny
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0
rm -f "$AGENT_LOG"

exec claude --agent manny "Coordinate Rocky and Ivory to complete this task. Use the branch name 'hub'.

$(cat demo/target/TASK.md)"
