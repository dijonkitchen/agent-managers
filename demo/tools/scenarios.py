"""Structural predicates over a run log. Used by the scenario tests.

A "hop" is a spawn, message, or report between two distinct agents. Start
and end rows only bound the run in time, and a self-edge is bookkeeping
rather than coordination -- a log captured before the hook stopped writing
them holds the lead's own SubagentStop records, which credited the solo
control with two hops it could not have had.
"""

HOP_KINDS = {"spawn", "message", "report"}


def hop_records(records: list[dict]) -> list[dict]:
    return [r for r in records if r["kind"] in HOP_KINDS and r["from"] != r["to"]]


def hops(records: list[dict]) -> int:
    return len(hop_records(records))


def count(records: list[dict], kind: str) -> int:
    """Hops of one kind. Self-edges do not count, same as everywhere else."""
    return sum(1 for r in hop_records(records) if r["kind"] == kind)


def agents(records: list[dict]) -> set[str]:
    return {r["from"] for r in records} | {r["to"] for r in records}


def prompt_chars(records: list[dict]) -> int:
    return sum(r.get("chars", 0) for r in hop_records(records))


def max_hop_chars(records: list[dict]) -> int:
    return max((r.get("chars", 0) for r in hop_records(records)), default=0)


def mean_chars(records: list[dict], kind: str) -> float:
    """Average context carried by one hop of `kind`. 0.0 when there are none."""
    sizes = [r.get("chars", 0) for r in hop_records(records) if r["kind"] == kind]
    return sum(sizes) / len(sizes) if sizes else 0.0


def distinct_edges(records: list[dict]) -> int:
    return len({(r["from"], r["to"]) for r in hop_records(records)})


def peer_edges(records: list[dict], lead: str) -> set[tuple[str, str]]:
    """Directed edges that bypass the lead entirely."""
    return {(r["from"], r["to"]) for r in hop_records(records)
            if lead not in (r["from"], r["to"])}


def is_star(records: list[dict], lead: str) -> bool:
    return hops(records) > 0 and not peer_edges(records, lead)


def wall_seconds(records: list[dict]) -> float:
    ts = [r["ts"] for r in records]
    return max(ts) - min(ts) if ts else 0.0


def busy_intervals(records: list[dict], lead: str) -> dict[str, list[tuple[float, float]]]:
    """Per non-lead agent, the stretches where it owed someone a response.

    An agent is busy from the moment something is addressed to it until its
    next outgoing event. The lead is excluded on purpose: when the lead is
    the interactive session, "the lead is thinking" and "the operator walked
    away" are the same thing in the log, and only one of them is the run.
    """
    hops = sorted(hop_records(records), key=lambda r: r["ts"])
    out: dict[str, list[tuple[float, float]]] = {}
    for agent in agents(records) - {lead}:
        spans, opened = [], None
        for r in hops:
            if r["to"] == agent and opened is None:
                opened = r["ts"]
            elif r["from"] == agent and opened is not None:
                spans.append((opened, r["ts"]))
                opened = None
        out[agent] = spans
    return out


def _union(spans: list[tuple[float, float]]) -> float:
    merged: list[list[float]] = []
    for lo, hi in sorted(spans):
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    return sum(hi - lo for lo, hi in merged)


def busy_seconds(records: list[dict], lead: str) -> float:
    """Wall-clock time with at least one non-lead agent working.

    The run's latency, with the lead's stalls excluded. Use this to compare
    topologies; `work_seconds` still counts whatever the lead sat on.
    """
    return _union([s for spans in busy_intervals(records, lead).values() for s in spans])


def agent_seconds(records: list[dict], lead: str) -> float:
    """Total agent effort: the same intervals summed rather than unioned.

    `busy_seconds` is how long the run took; this is how much work it cost.
    Their ratio is how much parallelism the topology actually got.
    """
    return sum(hi - lo for spans in busy_intervals(records, lead).values() for lo, hi in spans)


def parallelism(records: list[dict], lead: str) -> float:
    """Effort divided by latency. 1.0 is strictly serial."""
    busy = busy_seconds(records, lead)
    return agent_seconds(records, lead) / busy if busy else 0.0


def work_seconds(records: list[dict]) -> float:
    """First hop to last, ignoring self-edges.

    `wall_seconds` runs start to end, which for a session means "until the
    operator quit": the three captured runs were opened within 36s of each
    other and closed within 24s, so their spans come out a dead heat around
    4200s. A self-edge report is the lead session's own turn, not a hop
    between agents, so it does not bound the work either -- the captured
    flat run's peers had all reported back by 983s and the referee session
    then idled for another 2000s.
    """
    ts = [r["ts"] for r in hop_records(records)]
    return max(ts) - min(ts) if ts else 0.0


def first_ts(records: list[dict], sender: str) -> float:
    return min(r["ts"] for r in hop_records(records) if r["from"] == sender)


def is_delegation(r: dict, lead: str) -> bool:
    """A spawn, or a message from the lead that resumes a named agent."""
    return r["from"] == lead and r["kind"] in ("spawn", "message")


def delegations(records: list[dict], lead: str) -> int:
    return sum(1 for r in hop_records(records) if is_delegation(r, lead))


def validation_rounds(records: list[dict], lead: str) -> int:
    """Times the lead re-delegated after receiving a report: a check loop."""
    rounds, pending = 0, False
    for r in sorted(hop_records(records), key=lambda r: r["ts"]):
        if r["kind"] == "report" and r["to"] == lead:
            pending = True
        elif is_delegation(r, lead) and pending:
            rounds += 1
            pending = False
    return rounds


def max_concurrent_delegations(records: list[dict], lead: str) -> int:
    """Peak number of the lead's delegations alive at once, closed by a report."""
    events = []
    for r in hop_records(records):
        if is_delegation(r, lead):
            events.append((r["ts"], 1))
        elif r["kind"] == "report" and r["to"] == lead:
            events.append((r["ts"], -1))
    alive = peak = 0
    for _, delta in sorted(events, key=lambda e: (e[0], e[1])):
        alive += delta
        peak = max(peak, alive)
    return peak
