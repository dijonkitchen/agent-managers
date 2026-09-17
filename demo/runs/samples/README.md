The three 2026-09-16 captured runs, normalized. Not stand-ins: these are
what the deck's metrics table, graphs and scorecard are built from, and what
CI publishes, since a clean clone never has the gitignored
`demo/runs/*.jsonl`. The unedited logs, and exactly what normalizing
changed, are in `demo/runs/recorded/`.

Replace them with a fresh capture via `make promote-runs`, which copies all
three logs over these files and rewrites `PROVENANCE.txt`. That caption is
the single source of truth for what the deck claims about these numbers, so
keep it accurate: it is rendered under the metrics table.

`demo/tests/test_slides.py` compares the scorecard printed on
`slides/slides.md` against these logs, so promoting a new capture whose
numbers differ turns the build red until the slide is updated.
