# Recorded runs

Real runs, kept deliberately. `demo/runs/*.jsonl` is gitignored because
rehearsal output is noise; the logs here are the exception, checked in so
the deck can cite measured numbers instead of the synthetic samples.

Evidence, not a build input. `make graphs` reads `demo/runs/*.jsonl` and
falls back to `demo/runs/samples/`; it does not look in this directory.

## `flat-20260916.jsonl`

The flat run on branch `flat-20260916-204643` — the referee spawned codie,
archie, and manny as peers, and they added the TTL-bounded cache to
`demo/target/pricing.py`. 116 records, unedited.

| Metric | flat (recorded) | flat (sample) | hub (sample) |
| --- | --- | --- | --- |
| Spawns | 3 | 3 | 2 |
| Messages | 51 | 13 | 2 |
| Reports to lead | 61 | 3 | 4 |
| Total hops | 115 | 19 | 8 |
| Distinct edges | 13 | 12 | 4 |
| Prompt chars sent | 155032 | 3030 | 1350 |
| Wall time (s) | 1420.4 | 268 | 385 |

### What the real numbers change

The samples get flat's *shape* right and its *cost* wrong. Every ordered
pair of peers really was used, and codie really did ship before archie
answered. But the sample understates coordination cost by a wide margin:
51x the prompt chars, 6x the hops, and 16x the largest single hop (10,610
chars against 640). "Flat is chattier" is the sample's claim; "flat is
chattier by one and a half orders of magnitude" is this run's.

### Three caveats, because the log is unedited

**Reports to lead overcounts.** 22 of the 61 reports are `referee ->
referee` self-edges: `SubagentStop` fires in the parent session on every
teammate turn, and its hook input carries no `agent_type`, so the sender
falls back to the lead. The row is closer to a turn count than a report
count, and it inflates flat's total hops against hub's.

**Distinct edges is 13, not 12.** This log predates the alias fix in
`2a591a6`: manny's two reports to the referee were recorded as `manny ->
main`, drawing one session as two nodes. With that fix the same run yields
12 distinct edges and 6 peer edges, which is what
`test_flat_weakness_peers_talk_past_the_lead` asserts. Future runs record
it correctly; this file is kept as recorded.

**No `end` record.** The referee session was still open when the run was
captured, so wall time is bounded by the last hop rather than `SessionEnd`.

### One claim this run does not support

`test_flat_strength_finishes_before_hub` asserts flat beats hub on wall
time. Recorded flat took 1420.4s against the synthetic hub's 385s — but
the hub figure is invented, so this is not evidence that flat is slower.
The comparison is simply untestable until a real hub run is recorded
alongside this one. Worth resolving before the claim goes on a slide.
