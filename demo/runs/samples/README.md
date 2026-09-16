Stand-in runs. They exist so `make graphs` and the deck build without
running Claude, and they are what CI publishes, since a clean clone never
has the gitignored `demo/runs/*.jsonl`.

Replace them with captured runs via `make promote-runs`, which copies all
three logs over these files and rewrites `PROVENANCE.txt`. That caption is
the single source of truth for what the deck claims about these numbers, so
keep it accurate: it is rendered under the metrics table.
