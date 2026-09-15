#!/usr/bin/env bash
# Flat run: a referee session spawns Codie, Archie, and Manny as peer
# teammates. Teammates get SendMessage automatically, so anyone can talk
# to anyone. Manny is present but has no authority. The referee only
# spawns and waits.
#
# Requires an interactive terminal: agent teams do not spawn under -p.
set -euo pipefail
cd "$(dirname "$0")/.."
source demo/lib/worktree.sh

# Absolute, and deliberately in the main checkout: the run itself happens
# in a worktree, but `make graphs` reads all three logs from here.
export AGENT_LOG="$(main_checkout)/demo/runs/flat.jsonl"
export AGENT_LEAD_NAME=referee
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
rm -f "$AGENT_LOG"

task="$(cat demo/target/TASK.md)"

# Fresh worktree and branch per run, so the demo can be rehearsed.
worktree="$(prepare_worktree flat)"
branch="$(basename "$worktree")"
cd "$worktree"

exec claude --name referee "You are the referee. Spawn three teammates named codie, archie, and manny, using the codie, archie, and manny agent types respectively. Give each of them the full task below, plus this instruction: 'You are peers. Nobody is in charge. Coordinate directly with each other by name. The referee will not answer questions. Message the referee only when the task is done.' Then wait for all three to finish. Do not do any of the work yourself and do not answer questions from teammates. When they finish, print a one-paragraph summary of what happened.

Task for the teammates (you are already on the branch '$branch', created for this run):

$task"
