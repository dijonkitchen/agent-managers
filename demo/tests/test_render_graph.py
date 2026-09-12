import render_graph as rg

HUB = [
    {"ts": 1, "kind": "spawn", "from": "manny", "to": "ivory", "chars": 10},
    {"ts": 2, "kind": "report", "from": "ivory", "to": "manny", "chars": 0},
    {"ts": 3, "kind": "spawn", "from": "manny", "to": "rocky", "chars": 10},
    {"ts": 4, "kind": "report", "from": "rocky", "to": "manny", "chars": 0},
    {"ts": 5, "kind": "spawn", "from": "manny", "to": "rocky", "chars": 10},
]


def test_build_graph_counts_edges_and_collects_nodes():
    g = rg.build_graph(HUB)
    assert g.nodes == ["ivory", "manny", "rocky"]
    assert g.edges[("manny", "rocky")] == 2
    assert g.edges[("manny", "ivory")] == 1
    assert g.edges[("ivory", "manny")] == 1


def test_build_graph_ignores_self_edges():
    g = rg.build_graph([{"ts": 1, "kind": "message", "from": "a", "to": "a", "chars": 1}])
    assert g.edges == {}
    assert g.nodes == ["a"]


def test_svg_contains_every_node_label_and_edge_weight():
    svg = rg.to_svg(rg.build_graph(HUB), title="hub")
    assert svg.startswith("<svg")
    for name in ("ivory", "manny", "rocky"):
        assert name in svg
    assert ">2<" in svg  # weight label on manny -> rocky
    assert "hub" in svg


def test_svg_for_empty_run_is_still_valid():
    svg = rg.to_svg(rg.build_graph([]), title="empty")
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")


def test_read_jsonl_skips_blank_lines(tmp_path):
    p = tmp_path / "run.jsonl"
    p.write_text('{"ts":1,"kind":"spawn","from":"a","to":"b","chars":1}\n\n')
    assert len(rg.read_jsonl(p)) == 1


def test_solo_run_renders_a_single_node():
    records = [{"ts": 1, "kind": "start", "from": "solo", "to": "solo", "chars": 0}]
    g = rg.build_graph(records)
    assert g.nodes == ["solo"] and g.edges == {}
    assert "solo" in rg.to_svg(g, title="solo")
