# agent-managers

A Marp deck: **how to survive the AI age as an engineer.**

The talk is a ladder. Each rung is something you do to go faster, and the
wall it hands you that the next rung exists to clear — one agent, several
agents in one repo, worktrees, tabs, you as the hub, delegation, a wired
fleet, diversity, a bought cast, and then deleting the scaffolding again.
The refrain is "how do you 10x again?", and the last answer is that you
don't; you manage.

## The argument

| | |
| --- | --- |
| **The climb** | Every rung is cleared by a management move, not a smarter model |
| **The research** | Solo is already the 10x. Structure contains errors; it cannot fix clones. |
| **The wiring** | Topology is the decision: the same agents cost 0, n−1, or n(n−1)/2 edges, and the cheapest wiring amplifies errors the most |
| **The stop rule** | Every rung has a shelf life. Build it cheap, build it deletable, and ask quarterly which agent is now a worse version of one good session. |

## Building

```sh
make slides   # -> dist/index.html (plus dist/assets/)
make pdf      # -> dist/slides.pdf
make clean
```

Both targets run a pinned `@marp-team/marp-cli` through `npx`, so a build
is Markdown in, HTML or PDF out. Nothing is generated: the images are
checked in under `slides/assets/`, and the rest of the figures are inline
SVG in the Markdown.

`npm run slides:watch` opens a live preview. It uses the locally installed
marp-cli, so run `npm install` first.

Pushes to `main` deploy `dist/` to GitHub Pages via
`.github/workflows/slides.yml`, which also uploads `dist/slides.pdf` as a
build artifact. Pull requests build but do not deploy.

## Layout

| Path | Purpose |
| ---- | ------- |
| `slides/slides.md` | The deck: theme, styles, and every slide. Speaker notes live in HTML comments. |
| `slides/assets/` | Images the deck references — the pictorial characters (GLaDOS, Sonic, Batman's utility belt, the White Rabbit), the BMad banner, and the BMad delivery-loop diagram. |

The three remaining diagrams — the context-switching wheel, the five
message graphs, and the closing companion cube — are inline SVG in
`slides.md` rather than files.

## Sources

Every number on a slide comes from published research, credited on the
slide itself or in its speaker notes, and collected on the deck's final
slide: Kim et al. on scaling agent systems, Anthropic's Frontier Red Team
on multiagent failure modes, BMAD-METHOD, and the Claude Code docs. The
closing act argues from Sutton's Bitter Lesson.

The deck makes no measurement of its own — the only figures it derives are
edge counts, and those are arithmetic.
