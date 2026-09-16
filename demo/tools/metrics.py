#!/usr/bin/env python3
"""Summarize JSONL message logs into one markdown table, one column per run.

Usage: metrics.py hub=RUN.jsonl flat=RUN.jsonl -o metrics.md
"""

import argparse
from pathlib import Path

from render_graph import read_jsonl

ROWS = [
    ("Spawns", "spawns"),
    ("Messages", "messages"),
    ("Reports to lead", "reports"),
    ("Total hops", "total"),
    ("Distinct edges", "edges"),
    ("Prompt chars sent", "chars"),
    ("Wall time (s)", "wall_seconds"),
]


def summarize(records: list[dict]) -> dict:
    kinds = {"spawn": 0, "message": 0, "report": 0}
    for r in records:
        if r["from"] == r["to"]:
            continue  # a self-edge is bookkeeping, not coordination
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    ts = [r["ts"] for r in records]  # every record, so start/end still set wall time
    hops = kinds["spawn"] + kinds["message"] + kinds["report"]
    return {
        "spawns": kinds["spawn"],
        "messages": kinds["message"],
        "reports": kinds["report"],
        "total": hops,
        "chars": sum(r.get("chars", 0) for r in records),
        "edges": len({(r["from"], r["to"]) for r in records if r["from"] != r["to"]}),
        "wall_seconds": round(max(ts) - min(ts), 1) if ts else 0.0,
    }


def _fmt(v) -> str:
    return f"{v:g}" if isinstance(v, float) else str(v)


def to_markdown(runs: dict[str, dict], note: str | None = None) -> str:
    names = list(runs)
    lines = ["| Metric | " + " | ".join(names) + " |", "| --- | " + " | ".join("---" for _ in names) + " |"]
    for label, key in ROWS:
        lines.append(f"| {label} | " + " | ".join(_fmt(runs[n][key]) for n in names) + " |")
    table = "\n".join(lines) + "\n"
    # The caption travels with the numbers, so the deck can never claim a
    # provenance the table does not have.
    return table if note is None else f"{table}\n{note}\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("runs", nargs="+", help="name=path.jsonl")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--note", help="provenance caption rendered under the table")
    args = ap.parse_args()
    runs = {}
    for spec in args.runs:
        name, _, path = spec.partition("=")
        runs[name] = summarize(read_jsonl(Path(path)))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(to_markdown(runs, args.note))


if __name__ == "__main__":
    main()
