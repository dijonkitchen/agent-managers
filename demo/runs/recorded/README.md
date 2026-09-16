# Recorded runs

The three captured logs exactly as the hook wrote them, on 2026-09-16.
`demo/runs/*.jsonl` is gitignored because rehearsal output is noise; these
are the exception, kept so every number on the deck can be traced back to
an unedited file.

**Evidence, not a build input.** `make graphs` reads `demo/runs/*.jsonl`
and falls back to `demo/runs/samples/`, which now holds the normalized
copies of these same runs. Nothing reads this directory.

| File | Branch | Records |
| --- | --- | --- |
| `solo-20260916-raw.jsonl` | `solo-20260916-204608` | 4 |
| `hub-20260916-raw.jsonl` | `hub-20260916-204627` | 62 |
| `flat-20260916-raw.jsonl` | `flat-20260916-204643` | 118 |

All three carry a `SessionEnd`. The copy committed on the flat branch has
116 records and no `end`, because it was snapshotted while the referee
session was still open; these are the complete logs.

## The sequential re-run, `*-sequential-raw.jsonl`

The three runs above were captured concurrently in one attended sitting,
which contaminates every timing row. They were run again the same day,
one at a time and unattended, to find out how much. **Do not build the
deck from these:** the flat one is not a flat run (see below), so the
set has no valid three-way comparison in it.

| | attended, concurrent | sequential, unattended |
| --- | --- | --- |
| solo session | 4215.8s | **245.9s** |
| hub session | 4200.3s | 945.7s |
| hub hop span | 3100.3s | 888.1s |
| hub agent busy | 1360.9s | **762.6s** |

Excluding the lead got hub from 3100.3s to 1360.9s; running it alone got
it to 762.6s. So `busy_seconds` removes the operator's stalls but not
contention between the agents themselves — three sessions sharing one
machine and one rate limit slow the agents down too, and no read-side
metric can subtract that. **Capture sequentially; it is not optional.**

### The flat run cannot be captured headless

`run-flat.sh` says agent teams need an interactive terminal. Without one
they silently do not activate: the referee still spawns codie, archie and
manny, but as ordinary subagents with no `SendMessage` tool. The result
looks like a run and is not one — 2 peer edges against 6, 2 messages
against 51, and codie and archie never spoke at all. Kept here only as
the counter-example.

### What the re-run does confirm

**No phantom self-reports, in either new log.** The attended runs logged
40 (hub), 23 (flat) and 2 (solo); the unattended ones logged none. So
`SubagentStop` firing against the lead is tied to the attended session
pattern rather than being universal. The hook fix still guards a real
failure mode — it just is not one every run hits.

**The agent ids came back**, as `a048b5ba8621c9933` (archie) and
`a27175c3bd5f57f5c` (codie). `normalize_run.py` refused the log until
both were named, on ids it had never seen.

**Hub was strictly sequential this time** — peak 1 delegation in flight,
against 2 in the attended run. So "the hub runs sequentially" is a
property of the run, not of the topology, which is why the scenario test
asserts the weaker, stable claim.

**Six runs, one design.** Every agent that has written this cache chose
`OrderedDict`, `TTL_SECONDS = 5.0` and `MAX_ENTRIES = 128` — the three
attended runs, plus solo, hub and flat again here. Only the lock varies
(2 of 6). In the degenerate flat run codie and archie each produced that
design independently, in parallel, having never exchanged a message.

### These runs do not exercise the fixes

`prepare_worktree` starts every run from the main checkout's `HEAD`, so
all six ran against `dfa8b00` — without the hook fix, the `manny.md`
wording, or anything else on this branch. Re-run after merging to test
those.

## What was changed to promote them

`normalize_run.py` rewrote destinations onto the agents behind them, and
nothing else — no records added, removed, or reordered, no timestamps or
character counts touched.

**`manny -> main` became `manny -> referee`** in the flat run. Manny
addressed the referee session by its `ListAgents` name, so one session was
drawn as two nodes: 13 distinct edges and 7 peer edges, where
`test_flat_weakness_peers_talk_past_the_lead` asserts 6. The hook now does
this itself, so future runs record it correctly.

**Two agent ids became names** in the hub run:
`ab9d1ed5f9bbcf43b` → `archie`, `a08df1e74b04059d2` → `codie`. Manny
resumed teammates by the opaque ids `ListAgents` prints, so the hub graph
came out with five nodes and six edges for what is a three-node, four-edge
star.

The log never pairs an id with a name, so that mapping is an inference,
and it is worth stating why it is not a guess. Manny made 10 delegations:
2 cold spawns, 2 resumes of `ab9d1ed`, 6 of `a08df1e`. There were exactly
10 reports back: 3 from Archie and 7 from Codie, i.e. 2 and 6 after their
respective cold spawns. Only one assignment balances — 2 to Archie, 6 to
Codie — and it is corroborated by content: `ab9d1ed` received two research
briefs of 3,990 and 3,576 chars while `a08df1e` received six
implementation rounds, which is the loop `.claude/agents/manny.md`
prescribes. `manny.md` now tells Manny to resume by name.

## Three things the raw logs show that the metrics deliberately do not

**40 of the hub run's 50 reports, and 23 of the flat run's 62, are
self-edges.** `SubagentStop` fires in the parent session on every teammate
turn and its hook input carries no `agent_type`, so the sender fell back
to the lead. That row was closer to a turn count than a report count, and
it inflated flat's hops against hub's. Worse, in the hub run those
phantom reports closed delegations in `max_concurrent_delegations` and
hid the fact that Manny ran two agents at once. The hook no longer writes
them and every predicate now skips them, so the promoted logs still
contain them and the numbers do not.

**Session time is not a comparison.** All three sessions were opened
within 36s of each other and closed within 24s, which is why their spans
come out 4215.8s, 4200.3s and 4192.0s. That measures the sitting, not the
run. `Work time` — first hop to last — is the row that is about the run.

**Work time is not a clean comparison either.** Flat had every peer
reported back in 983.0s against hub's 3100.3s, but 1505s of hub's span is
two gaps — 967.4s and 537.4s, 49% of the total — that both sit *after* a
report from Codie and *before* Manny's next message. Nothing was delegated
during them, so they are not agent work; a manager agent with no file
tools does not spend sixteen minutes composing a 4,000-char message.
They are the shape of an operator running three sessions at once. Flat's
largest gap is 78.6s and its five largest sum to 31% of its span, which is
what an unattended run looks like.

So flat finishing first is real — its last hop lands while hub still had
half its hops to go — but the **3.2x margin is not measurable from this
capture**. Capture the three runs sequentially and unattended to get a
number worth putting on a slide.

The solo control has no work time at all: after the phantom reports are
dropped it logs no hops. Its 4215.8s session included 395.5s before its
first event and a 2816.9s idle tail waiting on a human.
