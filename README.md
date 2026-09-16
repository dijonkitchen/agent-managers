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
violates the freshness constraint, which is what the task is designed to
bait.

**The 2026-09-16 runs did not take the bait.** All three — including solo,
with nobody to check it — shipped a TTL-bounded LRU that passes all four
constraints, with the same `OrderedDict`, the same `TTL_SECONDS = 5.0` and
the same `MAX_ENTRIES = 128`, a number no constraint asks for. Topology
changed the cost by a factor of 93 in hops and 3.5 in context moved; it
did not change the answer. That is the low-variance finding the deck cites
from Anthropic's swarm work, showing up in the demo's own data, and it is a
more interesting result than the divergence the task was built to produce.
The `lru_cache` version lives in `demo/attempts/` as a scored exhibit, not
as something a run produced.

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
  second opinion; hub is a star with a validation loop that serializes
  most of the work and pays its context once per agent; flat starts
  everyone at once and finishes first but talks past the lead with more
  hops and more context. The captured runs falsified two earlier claims
  here — that the hub never ran two agents at once, and that its briefs
  were small — so both were restated. A red test is a finding.
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

`make graphs` uses captured runs from `demo/runs/` only when all three
are present, and otherwise falls back to the tracked copies in
`demo/runs/samples/` — which hold the 2026-09-16 runs, not stand-ins.
The caption under the table states which source it used.
Pushes to `main` deploy `dist/` to GitHub Pages via
`.github/workflows/slides.yml`.

To put real numbers on the deck, capture all three runs and promote them:

```sh
./demo/run-solo.sh && ./demo/run-hub.sh && ./demo/run-flat.sh
make promote-runs graphs
```

Capture before landing any branch that completes `demo/target/TASK.md`.
`prepare_worktree` starts each run from the main checkout's `HEAD`, so once
the task is already done on `main` the agents have nothing to do and the
logs are worthless. `demo/runs/*.jsonl` is gitignored and CI builds from a
clean clone, so `make promote-runs` is what gets real data as far as Pages.

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
| `demo/runs/samples/` | The solo, hub, and flat runs the deck builds from |
| `demo/runs/recorded/` | The same runs unedited, with what normalizing changed |
| `demo/tools/normalize_run.py` | Resolves a recorded destination onto the agent behind it |
| `slides/slides.md` | The Marp deck |
