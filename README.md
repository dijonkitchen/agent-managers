# agent-managers

A Marp deck: **how to survive the AI age as an engineer.**

The talk is a ladder. Each rung is something you do to go faster, and the
wall it hands you that the next rung exists to clear — one agent, several
agents, thrash, worktrees, tabs, you as the hub, delegation, a fleet. The
refrain is "how do you 10x again?", and the last answer is that you don't;
you manage.

## The argument

| | |
| --- | --- |
| **The climb** | Every rung is cleared by a management move, not a smarter model |
| **The research** | Solo is already the 10x. Structure contains errors; it cannot fix clones. |
| **The wiring** | One config line — who may talk to whom — sets whether paths grow n−1 or n(n−1)/2 |
| **The stop rule** | As simple as possible, but no simpler. Climb to the wall in front of you. |

## Building

```sh
make slides   # -> dist/index.html
make pdf      # -> dist/slides.pdf
make clean
```

The deck is self-contained: every figure on it is inline SVG, so a build is
Markdown in, HTML or PDF out. Nothing is generated and nothing is fetched.

Pushes to `main` deploy `dist/` to GitHub Pages via
`.github/workflows/slides.yml`.

## Layout

| Path | Purpose |
| ---- | ------- |
| `slides/slides.md` | The deck. Speaker notes live in HTML comments. |
| `slides/assets/` | Raster images. Diagrams are inline SVG in the deck; these are the pictorial characters (GLaDOS, Sonic, the utility belt, the White Rabbit). |

## Sources

Every figure quoted on a slide is linked on the deck's final slide —
Kim et al. on scaling agent systems, Anthropic's Frontier Red Team on
multiagent failure modes, Google's Project Oxygen, Brooks, Conway, Sutton,
BMAD-METHOD, and the Claude Code docs.

Every number on a slide comes from published research. The deck makes no
measurement of its own — the only figures it derives are edge counts, and
those are arithmetic.
