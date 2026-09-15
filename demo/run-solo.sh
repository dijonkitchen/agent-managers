#!/usr/bin/env bash
# Control run: one session, no delegation. The Agent tool is disallowed
# so the session cannot spawn anyone. Same task, same prompt shape.
set -euo pipefail
cd "$(dirname "$0")/.."
source demo/lib/worktree.sh

# Absolute, and deliberately in the main checkout: the run itself happens
# in a worktree, but `make graphs` reads all three logs from here.
export AGENT_LOG="$(main_checkout)/demo/runs/solo.jsonl"
export AGENT_LEAD_NAME=solo
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0
rm -f "$AGENT_LOG"

task="$(cat demo/target/TASK.md)"

# Fresh worktree and branch per run, so the demo can be rehearsed.
worktree="$(prepare_worktree solo)"
branch="$(basename "$worktree")"
cd "$worktree"

# `--disallowedTools` is variadic, so the prompt has to come after `--`,
# or it gets swallowed word-by-word as extra deny rules.
exec claude --disallowedTools Agent -- "Complete this task on your own. You are already on the branch '$branch', created for this run.

$task"
