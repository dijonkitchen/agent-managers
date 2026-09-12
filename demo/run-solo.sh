#!/usr/bin/env bash
# Control run: one session, no delegation. The Agent tool is disallowed
# so the session cannot spawn anyone. Same task, same prompt shape.
set -euo pipefail
cd "$(dirname "$0")/.."

export AGENT_LOG=demo/runs/solo.jsonl
export AGENT_LEAD_NAME=solo
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0
rm -f "$AGENT_LOG"

exec claude --disallowedTools Agent "Complete this task on your own. Use the branch name 'solo'.

$(cat demo/target/TASK.md)"
