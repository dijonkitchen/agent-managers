.PHONY: test graphs slides pdf clean

test:
	uv run --group dev pytest -q

# Render message graphs and the metrics table from the JSONL runs.
# Real runs in demo/runs/*.jsonl take precedence over the samples.
graphs:
	python3 demo/tools/render_graph.py $(or $(wildcard demo/runs/hub.jsonl),demo/runs/samples/hub.jsonl) -o slides/assets/hub.svg
	python3 demo/tools/render_graph.py $(or $(wildcard demo/runs/flat.jsonl),demo/runs/samples/flat.jsonl) -o slides/assets/flat.svg
	python3 demo/tools/metrics.py \
	  hub=$(or $(wildcard demo/runs/hub.jsonl),demo/runs/samples/hub.jsonl) \
	  flat=$(or $(wildcard demo/runs/flat.jsonl),demo/runs/samples/flat.jsonl) \
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
