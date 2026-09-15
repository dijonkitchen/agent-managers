.PHONY: test acceptance graphs slides pdf clean

test:
	uv run --group dev pytest -q

# TASK.md's definition of done, run against demo/target/pricing.py.
acceptance:
	uv run --group dev pytest -q -m acceptance demo/target

# Render message graphs and the metrics table from the JSONL runs.
# Real runs in demo/runs/*.jsonl take precedence over the samples.
run = $(or $(wildcard demo/runs/$(1).jsonl),demo/runs/samples/$(1).jsonl)

graphs:
	uv run python demo/tools/render_graph.py $(call run,solo) -o slides/assets/solo.svg
	uv run python demo/tools/render_graph.py $(call run,hub) -o slides/assets/hub.svg
	uv run python demo/tools/render_graph.py $(call run,flat) -o slides/assets/flat.svg
	uv run python demo/tools/metrics.py \
	  solo=$(call run,solo) hub=$(call run,hub) flat=$(call run,flat) \
	  -o slides/assets/metrics.md

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
