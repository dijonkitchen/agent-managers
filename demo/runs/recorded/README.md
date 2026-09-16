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

**No `end` record in the flat log.** The referee session was still open at
capture, so its session span is bounded by the last hop.

**Session time is not a comparison.** All three sessions were opened
within 36s of each other and closed within 24s, which is why their spans
come out 4215.8s, 4200.3s and 4192.0s. That measures the sitting. `Work
time` — first hop to last — is the row that is about the run: flat had
every peer reported back in 983.0s against hub's 3100.3s. The solo control
has no work time at all, because after the phantom reports are dropped it
logs no hops; its 4215.8s session includes 395.5s before its first event
and a 2816.9s idle tail waiting on a human.
