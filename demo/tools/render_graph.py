#!/usr/bin/env python3
"""Render a JSONL message log as an SVG message graph.

Nodes are agents, placed on a circle. Each directed edge is weighted by
how many spawns, messages, or reports went that way. A hub-and-spoke run
draws as a star; a flat run draws as a mesh.

Usage: render_graph.py RUN.jsonl -o OUT.svg [--title TEXT]
"""

import argparse
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

W, H, R, NODE_R = 640, 460, 145, 38
COLORS = {"manny": "#e0a800", "codie": "#e05a2b", "archie": "#3b7dd8", "desi": "#8a4fbd"}


@dataclass
class Graph:
    nodes: list[str] = field(default_factory=list)
    edges: dict[tuple[str, str], int] = field(default_factory=dict)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def build_graph(records: list[dict]) -> Graph:
    names: set[str] = set()
    edges: dict[tuple[str, str], int] = {}
    for r in records:
        src, dst = r["from"], r["to"]
        names.update((src, dst))
        if src != dst:
            edges[(src, dst)] = edges.get((src, dst), 0) + 1
    return Graph(nodes=sorted(names), edges=edges)


def _positions(nodes: list[str]) -> dict[str, tuple[float, float]]:
    cx, cy = W / 2, H / 2 + 20
    n = len(nodes)
    return {
        name: (cx + R * math.cos(2 * math.pi * i / n - math.pi / 2),
               cy + R * math.sin(2 * math.pi * i / n - math.pi / 2))
        for i, name in enumerate(nodes)
    } if n else {}


def _edge(pos, src, dst, weight, offset) -> str:
    (x1, y1), (x2, y2) = pos[src], pos[dst]
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1
    ux, uy = dx / length, dy / length
    # Shift parallel opposite-direction edges apart so both stay visible.
    px, py = -uy * offset, ux * offset
    sx, sy = x1 + ux * NODE_R + px, y1 + uy * NODE_R + py
    ex, ey = x2 - ux * (NODE_R + 6) + px, y2 - uy * (NODE_R + 6) + py
    mx, my = (sx + ex) / 2 + px * 1.2, (sy + ey) / 2 + py * 1.2
    width = 1.5 + min(weight, 8) * 0.6
    return (
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
        f'stroke="#555" stroke-width="{width:.1f}" marker-end="url(#arrow)"/>'
        f'<text x="{mx:.1f}" y="{my:.1f}" font-size="14" text-anchor="middle" '
        f'fill="#222" stroke="#fff" stroke-width="4" paint-order="stroke">{weight}</text>'
    )


def to_svg(graph: Graph, title: str = "") -> str:
    pos = _positions(graph.nodes)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" font-family="sans-serif">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" '
        'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#555"/></marker></defs>',
        f'<text x="{W/2}" y="28" font-size="22" text-anchor="middle" fill="#222">{title}</text>',
    ]
    for (src, dst), weight in sorted(graph.edges.items()):
        offset = 9 if (dst, src) in graph.edges else 0
        parts.append(_edge(pos, src, dst, weight, offset))
    for name, (x, y) in pos.items():
        color = COLORS.get(name, "#888")
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" fill="{color}" stroke="#222" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y+5:.1f}" font-size="16" font-weight="bold" '
            f'text-anchor="middle" fill="#fff">{name}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--title", default=None)
    args = ap.parse_args()
    title = args.title if args.title is not None else args.run.stem
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(to_svg(build_graph(read_jsonl(args.run)), title=title))


if __name__ == "__main__":
    main()
