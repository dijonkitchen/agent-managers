#!/usr/bin/env bash
# Control run: one session, no delegation. The Agent tool is disallowed
# so the session cannot spawn anyone. Same task, same prompt shape.
set -euo pipefail
cd "$(dirname "$0")/.."
source demo/lib/worktree.sh

# Absolute, and deliberately in the main checkout: the run itself happens
# in a worktree, but `make graphs` reads all three logs from here.
export AGENT_LOG="$PWD/demo/runs/solo.jsonl"
export AGENT_LEAD_NAME=solo
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0
rm -f "$AGENT_LOG"

task="$(cat demo/target/TASK.md)"
cd "$(prepare_worktree solo)"

exec claude --disallowedTools Agent "Complete this task on your own. You are already on the branch 'solo'.

$task"
