.PHONY: test acceptance graphs promote-runs slides pdf clean clean-worktrees

test:
	uv run --group dev pytest -q

# TASK.md's definition of done, run against demo/target/pricing.py.
acceptance:
	uv run --group dev pytest -q -m acceptance demo/target

# Render message graphs and the metrics table from the JSONL runs.
#
# Captured runs in demo/runs/ are used only when all three are present.
# The fallback is deliberately all-or-nothing: one real column beside two
# synthetic ones reads as a comparison, and is not one.
captured = $(wildcard demo/runs/solo.jsonl) $(wildcard demo/runs/hub.jsonl) $(wildcard demo/runs/flat.jsonl)

ifeq ($(words $(captured)),3)
run = demo/runs/$(1).jsonl
noteflag = --note 'Captured run, not yet promoted. Rebuild with `make graphs`.'
else
run = demo/runs/samples/$(1).jsonl
# By file, not by value: the caption is prose and may hold apostrophes.
noteflag = --note-file demo/runs/samples/PROVENANCE.txt
endif

graphs:
	uv run python demo/tools/render_graph.py $(call run,solo) -o slides/assets/solo.svg
	uv run python demo/tools/render_graph.py $(call run,hub) -o slides/assets/hub.svg
	uv run python demo/tools/render_graph.py $(call run,flat) -o slides/assets/flat.svg
	uv run python demo/tools/metrics.py \
	  solo=$(call run,solo) hub=$(call run,hub) flat=$(call run,flat) \
	  $(noteflag) -o slides/assets/metrics.md

# Copy the three captured runs over the tracked samples, so the deck shows
# real data everywhere -- including Pages, which only ever builds from a
# clean clone and so never sees the gitignored demo/runs/*.jsonl.
#
# Each log goes through normalize_run.py, which refuses a log holding a
# destination it cannot pair with an agent. That refusal is the point: it
# is how the hub run's raw agent ids were caught instead of being published
# as two extra nodes. Pass the mapping through ALIASES when it trips, e.g.
#   make promote-runs ALIASES='--alias a08df1e74b04059d2=codie'
ALIASES ?=
promote-runs:
	@test $(words $(captured)) -eq 3 || \
	  { echo "need all three of demo/runs/{solo,hub,flat}.jsonl; run the three demo/run-*.sh first"; exit 1; }
	for run in solo hub flat; do \
	  uv run python demo/tools/normalize_run.py demo/runs/$$run.jsonl $(ALIASES) \
	    -o demo/runs/samples/$$run.jsonl || exit 1; \
	done
	printf 'Captured run, promoted with `make promote-runs`. Rebuild with `make graphs`.\n' \
	  > demo/runs/samples/PROVENANCE.txt

# Inject the generated metrics table at the <!-- METRICS --> marker.
slides/slides.build.md: slides/slides.md graphs
	sed -e '/<!-- METRICS -->/r slides/assets/metrics.md' slides/slides.md > $@

slides: slides/slides.build.md
	mkdir -p dist && cp -r slides/assets dist/
	npx --yes @marp-team/marp-cli@4.5.1 --html slides/slides.build.md -o dist/index.html < /dev/null

pdf: slides/slides.build.md
	mkdir -p dist
	npx --yes @marp-team/marp-cli@4.5.1 --html --allow-local-files slides/slides.build.md -o dist/slides.pdf < /dev/null

clean:
	rm -rf dist slides/slides.build.md slides/assets/*.svg slides/assets/metrics.md

# Drop every per-run worktree. Kept out of `clean` because it discards
# whatever the agents did. Branches are left alone on purpose: each run's
# <name>-<timestamp> branch holds that run's output.
clean-worktrees:
	for path in .worktrees/*/; do \
	  [ -d "$$path" ] && git worktree remove --force "$$path" || true; \
	done
	git worktree prune
