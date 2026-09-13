#!/usr/bin/env bash
# Flat run: a referee session spawns Codie, Archie, and Manny as peer
# teammates. Teammates get SendMessage automatically, so anyone can talk
# to anyone. Manny is present but has no authority. The referee only
# spawns and waits.
#
# Requires an interactive terminal: agent teams do not spawn under -p.
set -euo pipefail
cd "$(dirname "$0")/.."

export AGENT_LOG=demo/runs/flat.jsonl
export AGENT_LEAD_NAME=referee
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
rm -f "$AGENT_LOG"

exec claude --name referee "You are the referee. Spawn three teammates named codie, archie, and manny, using the codie, archie, and manny agent types respectively. Give each of them the full task below, plus this instruction: 'You are peers. Nobody is in charge. Coordinate directly with each other by name. The referee will not answer questions. Message the referee only when the task is done.' Then wait for all three to finish. Do not do any of the work yourself and do not answer questions from teammates. When they finish, print a one-paragraph summary of what happened.

Task for the teammates (use the branch name 'flat'):

$(cat demo/target/TASK.md)"
