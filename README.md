# agent-managers

A live demo and Marp deck comparing two multi-agent topologies on the
same task with the same three agents, plus a single-agent control:

- **Solo (control)**: one session, Agent tool disallowed. No delegation
  possible. The baseline both cited papers measure against.
- **Hub-and-spoke**: Manny (the manager) is the only agent that talks
  to Codie and Archie. Codie and Archie cannot talk to each other.
- **Flat**: Codie, Archie, and Manny are peers. Anyone can message anyone.
  Nobody has authority.

The only thing that changes between the two runs is who is allowed to
talk to whom. The deck shows three diffs: the wiring diff (tiny), the
message graph (star vs triangle), and the resulting code diff (large).

## The cast

| Agent | Role | Tools | Instinct |
| ----- | ---- | ----- | -------- |
| Codie | Coder | Read + write | Tries code ideas immediately |
| Archie | Researcher / architect | Read-only | Reads everything, then recommends |
| Manny | Manager | Delegation only, no file access | Routes, sequences, decides |

Definitions live in `.claude/agents/`.

## The task

`demo/target/` is a tiny pricing module with a slow upstream quote
function. The task (`demo/target/TASK.md`) is to add caching under a
freshness and memory constraint. The reflex answer (`functools.lru_cache`)
violates the freshness constraint, which is what makes the topologies
diverge: Codie reaches for it first, Archie catches it.

## Running the demo

Requires Claude Code and, for the flat run, agent teams enabled.

```sh
demo/run-solo.sh   # Control: one session, cannot spawn anyone
demo/run-hub.sh    # Manny is the session; Codie and Archie are subagents
demo/run-flat.sh   # A referee session spawns all three as peer teammates
```

Each run works in its own worktree and branch under `.worktrees/`, named
`<run>-<timestamp>`, so a run can be repeated as often as a rehearsal
needs without colliding with what the last one left behind. Every run
starts from the main checkout's current commit. `make clean-worktrees`
drops the worktrees; it leaves the branches, which hold the run output.

Each run appends session start and end, every spawn, message, and
subagent report to `demo/runs/<name>.jsonl` via the hooks in
`.claude/settings.json`.
The runs are non-deterministic. Record them with `asciinema rec` and
replay the recording on stage instead of running live.

## The claims are tests

- `demo/tests/test_scenarios.py` asserts each topology's strengths and
  weaknesses from the run logs: solo has zero coordination cost and no
  second opinion; hub is a star with a validation loop but runs
  sequentially; flat starts everyone at once and finishes first but
  talks past the lead with more hops and more context.
- `demo/tests/test_attempts.py` scores three caching implementations
  against the four TASK.md constraints: the untouched module, Codie's
  `lru_cache` reflex in `demo/attempts/`, and the TTL-bounded cache
  that passes Archie's checklist.
- `demo/target/test_acceptance.py` is the task's definition of done.
  Deselected by default; `make acceptance` runs it.

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
| `.claude/agents/` | Codie, Manny, Archie definitions |
| `.claude/settings.json` | Hooks that log spawns and messages |
| `demo/target/` | The codebase the agents modify |
| `demo/lib/worktree.sh` | Fresh worktree and branch per run |
| `demo/hooks/log_messages.py` | Hook script: hook event -> JSONL record |
| `demo/tools/render_graph.py` | JSONL -> SVG message graph |
| `demo/tools/metrics.py` | JSONL -> markdown metrics table |
| `demo/tools/scenarios.py` | Structural predicates over a run log |
| `demo/tools/constraints.py` | TASK.md constraints as checks against any pricing module |
| `demo/attempts/` | Reference caching attempts scored by the tests |
| `demo/runs/samples/` | Synthetic solo, hub, and flat runs so the deck builds without Claude |
| `slides/slides.md` | The Marp deck |
