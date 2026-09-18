.PHONY: slides pdf clean

# The deck is self-contained: every figure on it is inline SVG apart from
# the one raster asset in slides/assets, so a build is Markdown in, HTML or
# PDF out. Nothing is generated, nothing is fetched.
slides/slides.build.md: slides/slides.md
	cp slides/slides.md $@

slides: slides/slides.build.md
	mkdir -p dist && cp -r slides/assets dist/
	npx --yes @marp-team/marp-cli@4.5.1 --html slides/slides.build.md -o dist/index.html < /dev/null

pdf: slides/slides.build.md
	mkdir -p dist
	npx --yes @marp-team/marp-cli@4.5.1 --html --allow-local-files slides/slides.build.md -o dist/slides.pdf < /dev/null

clean:
	rm -rf dist slides/slides.build.md
