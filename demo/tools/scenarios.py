"""Structural predicates over a run log. Used by the scenario tests.

A "hop" is a spawn, message, or report. Start and end rows only bound
the run in time.
"""

HOP_KINDS = {"spawn", "message", "report"}


def hop_records(records: list[dict]) -> list[dict]:
    return [r for r in records if r["kind"] in HOP_KINDS]


def hops(records: list[dict]) -> int:
    return len(hop_records(records))


def count(records: list[dict], kind: str) -> int:
    return sum(1 for r in records if r["kind"] == kind)


def agents(records: list[dict]) -> set[str]:
    return {r["from"] for r in records} | {r["to"] for r in records}


def prompt_chars(records: list[dict]) -> int:
    return sum(r.get("chars", 0) for r in hop_records(records))


def max_hop_chars(records: list[dict]) -> int:
    return max((r.get("chars", 0) for r in hop_records(records)), default=0)


def distinct_edges(records: list[dict]) -> int:
    return len({(r["from"], r["to"]) for r in hop_records(records) if r["from"] != r["to"]})


def peer_edges(records: list[dict], lead: str) -> set[tuple[str, str]]:
    """Directed edges that bypass the lead entirely."""
    return {(r["from"], r["to"]) for r in hop_records(records)
            if lead not in (r["from"], r["to"]) and r["from"] != r["to"]}


def is_star(records: list[dict], lead: str) -> bool:
    return hops(records) > 0 and not peer_edges(records, lead)


def wall_seconds(records: list[dict]) -> float:
    ts = [r["ts"] for r in records]
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
