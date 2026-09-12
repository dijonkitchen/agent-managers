Synthetic runs. They exist so `make graphs` and the deck build without
running Claude. Replace them with real runs by writing to
`demo/runs/hub.jsonl` and `demo/runs/flat.jsonl` (gitignored), which
`make graphs` prefers when present.
