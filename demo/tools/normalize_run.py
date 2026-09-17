#!/usr/bin/env python3
"""Resolve the agent names in a captured run log to the agents behind them.

The hook records a SendMessage destination verbatim, so an agent reached by
something other than the name it was spawned with becomes a second node on
the graph. Two ways that happened in the captured runs:

- a teammate addressed the lead session as "main", splitting one session
  into two nodes and turning the flat run's six peer edges into seven;
- Manny resumed teammates by the opaque ids `ListAgents` prints, so the hub
  run drew five nodes and six edges for a three-node, four-edge star.

The hook now handles the first case itself. The second cannot be fixed
downstream by rule: the log never pairs an id with a name, so the mapping
has to be supplied and stated. `--alias` is that statement, and the tool
refuses to write a log that still holds a name it cannot account for,
rather than quietly emitting a graph with invented nodes.

Usage: normalize_run.py RUN.jsonl -o OUT.jsonl [--alias ID=NAME ...]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Names a teammate may use for the lead session, mirroring the hook.
LEAD_ALIASES = frozenset({"main"})

# What an opaque agent id looks like next to a name like "codie".
OPAQUE = re.compile(r"^[0-9a-f]{8,}$")


def lead_of(records: list[dict]) -> str | None:
    """The lead is whoever the session's `start` record is attributed to."""
    return next((r["from"] for r in records if r["kind"] == "start"), None)


def spawned_names(records: list[dict]) -> set[str]:
    """Names that are known to be agents, because something spawned them."""
    return {r["to"] for r in records if r["kind"] == "spawn"}


def normalize(records: list[dict], aliases: dict[str, str] | None = None) -> list[dict]:
    lead = lead_of(records)
    resolve = dict(aliases or {})
    if lead is not None:
        resolve.update({alias: lead for alias in LEAD_ALIASES})
    out = []
    for r in records:
        r = dict(r)
        r["from"] = resolve.get(r["from"], r["from"])
        r["to"] = resolve.get(r["to"], r["to"])
        out.append(r)
    return out


def unresolved(records: list[dict]) -> set[str]:
    """Endpoint names that are neither the lead, nor spawned, nor a peer name.

    A peer in a flat run is never spawned under its own name by the agent
    that messages it, so "looks like an opaque id" and "is a known lead
    alias" are the only signals worth acting on. Anything else is left to
    the operator.
    """
    lead = lead_of(records)
    known = spawned_names(records) | ({lead} if lead else set())
    names = {r["from"] for r in records} | {r["to"] for r in records}
    return {n for n in names - known if n in LEAD_ALIASES or OPAQUE.match(n)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--alias", action="append", default=[], metavar="NAME=AGENT",
                    help="map a recorded name onto the agent behind it")
    args = ap.parse_args(argv)

    aliases = dict(spec.split("=", 1) for spec in args.alias)
    records = [json.loads(line) for line in args.run.read_text().splitlines() if line.strip()]
    out = normalize(records, aliases)

    left = unresolved(out)
    if left:
        print(
            f"{args.run}: cannot account for {sorted(left)}; pass --alias NAME=AGENT for each",
            file=sys.stderr,
        )
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(r) + "\n" for r in out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
