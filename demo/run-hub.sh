#!/usr/bin/env bash
# Hub-and-spoke run: Manny is the session. Codie and Archie are subagents
# that can only report back to Manny. They have no SendMessage tool, so
# the topology is enforced by the mechanism, not by the prompt.
set -euo pipefail
cd "$(dirname "$0")/.."
source demo/lib/worktree.sh

# Absolute, and deliberately in the main checkout: the run itself happens
# in a worktree, but `make graphs` reads all three logs from here.
export AGENT_LOG="$PWD/demo/runs/hub.jsonl"
export AGENT_LEAD_NAME=manny
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0
rm -f "$AGENT_LOG"

task="$(cat demo/target/TASK.md)"
cd "$(prepare_worktree hub)"

exec claude --agent manny "Coordinate Codie and Archie to complete this task. You are already on the branch 'hub'.

$task"
