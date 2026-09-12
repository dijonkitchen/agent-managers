# agent-managers

A live demo and Marp deck comparing two multi-agent topologies on the
same task with the same three agents:

- **Hub-and-spoke**: Manny (the manager) is the only agent that talks
  to Rocky and Ivory. Rocky and Ivory cannot talk to each other.
- **Flat**: Rocky, Ivory, and Manny are peers. Anyone can message anyone.
  Nobody has authority.

The only thing that changes between the two runs is who is allowed to
talk to whom. The deck shows three diffs: the wiring diff (tiny), the
message graph (star vs triangle), and the resulting code diff (large).

## The cast

| Agent | Role | Tools | Instinct |
| ----- | ---- | ----- | -------- |
| Rocky | Coder | Read + write | Tries code ideas immediately |
| Ivory | Researcher / architect | Read-only | Reads everything, then recommends |
| Manny | Manager | Delegation only, no file access | Routes, sequences, decides |

Definitions live in `.claude/agents/`.

## The task

`demo/target/` is a tiny pricing module with a slow upstream quote
function. The task (`demo/target/TASK.md`) is to add caching under a
freshness and memory constraint. The reflex answer (`functools.lru_cache`)
violates the freshness constraint, which is what makes the topologies
diverge: Rocky reaches for it first, Ivory catches it.

## Running the demo

Requires Claude Code and, for the flat run, agent teams enabled.

```sh
demo/run-hub.sh    # Manny is the session; Rocky and Ivory are subagents
demo/run-flat.sh   # A referee session spawns all three as peer teammates
```

Each run appends every spawn and message to `demo/runs/<name>.jsonl`
via the PreToolUse and SubagentStop hooks in `.claude/settings.json`.
The runs are non-deterministic. Record them with `asciinema rec` and
replay the recording on stage instead of running live.

## Building the slides

```sh
make test     # unit tests for the logger, graph renderer, metrics
make graphs   # JSONL -> slides/assets/{hub,flat}.svg + metrics.md
make slides   # -> dist/index.html
make pdf      # -> dist/slides.pdf
```

`make graphs` uses real runs from `demo/runs/` when present and falls
back to the synthetic samples in `demo/runs/samples/`. Pushes to `main`
deploy `dist/` to GitHub Pages via `.github/workflows/slides.yml`.

## Layout

| Path | Purpose |
| ---- | ------- |
| `.claude/agents/` | Rocky, Manny, Ivory definitions |
| `.claude/settings.json` | Hooks that log spawns and messages |
| `demo/target/` | The codebase the agents modify |
| `demo/hooks/log_messages.py` | Hook script: hook event -> JSONL record |
| `demo/tools/render_graph.py` | JSONL -> SVG message graph |
| `demo/tools/metrics.py` | JSONL -> markdown metrics table |
| `demo/runs/samples/` | Synthetic runs so the deck builds without Claude |
| `slides/slides.md` | The Marp deck |
