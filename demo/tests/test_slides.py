"""The scorecard slide's printed numbers, checked against the run logs.

`slides.md` hardcodes the scorecard, because a talk needs prose around each
figure -- "17.4k (cold brief)", "20, O(n)" -- that a generated table cannot
carry. The deck claims in return that every row on it is a pytest and that a
real run disagreeing with a slide turns the build red. This is the test that
makes that true: it parses the rendered row and compares it to the same
predicates `make graphs` uses, so a re-capture cannot quietly leave stale
numbers on the slide.

The metrics table on "By the numbers" needs no test -- it is generated.
"""

import re
from pathlib import Path

import pytest

import scenarios as sc
from render_graph import read_jsonl

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT.parent / "slides" / "slides.md"


def load(name: str) -> list[dict]:
    real = ROOT / "runs" / f"{name}.jsonl"
    return read_jsonl(real if real.exists() else ROOT / "runs" / "samples" / f"{name}.jsonl")


def scorecard() -> dict[str, tuple[str, str]]:
    """Row label -> (hub cell, flat cell) from the Honest scorecard table."""
    body = SLIDES.read_text().split("# Honest scorecard", 1)[1]
    rows = {}
    for line in body.splitlines():
        if not line.startswith("|"):
            if rows:  # the table ended
                break
            continue
        cells = [c.strip().strip("*").strip() for c in line.strip("|").split("|")]
        if len(cells) == 4 and cells[0] not in ("", "---"):
            rows[cells[0]] = (cells[2], cells[3])
    assert rows, f"no scorecard table found in {SLIDES}"
    return rows


def number(cell: str) -> float:
    """The leading figure in a cell, so "20, O(n)" and "17.4k" both parse."""
    m = re.match(r"([\d.]+)\s*k?", cell)
    assert m, f"no number in scorecard cell {cell!r}"
    value = float(m.group(1))
    return value * 1000 if "k" in cell.split()[0] else value


@pytest.fixture(scope="module")
def rows():
    return scorecard()


@pytest.fixture(scope="module")
def runs():
    return {"hub": (load("hub"), "manny"), "flat": (load("flat"), "referee")}


# Each row: the predicate behind it, and how the slide rounds it.
ROW_PREDICATES = {
    "Agents at once": lambda r, lead: sc.max_concurrent_delegations(r, lead),
    "Hops": lambda r, lead: sc.hops(r),
    "Context moved": lambda r, lead: round(sc.prompt_chars(r), -3),
    "Biggest single hop": lambda r, lead: round(sc.max_hop_chars(r), -2),
    "Agent effort": lambda r, lead: round(sc.agent_seconds(r, lead)),
    "Latency (agents busy)": lambda r, lead: round(sc.busy_seconds(r, lead)),
    "Parallelism": lambda r, lead: round(sc.parallelism(r, lead), 2),
}


@pytest.mark.parametrize("label", ROW_PREDICATES)
@pytest.mark.parametrize("column", ["hub", "flat"])
def test_scorecard_row_matches_the_logs(label, column, rows, runs):
    records, lead = runs[column]
    cell = rows[label][0 if column == "hub" else 1]
    printed = number(cell)
    measured = ROW_PREDICATES[label](records, lead)
    # Chars and seconds are printed rounded, so compare at the slide's own
    # precision rather than demanding the raw value.
    if label in ("Context moved", "Biggest single hop"):
        printed = round(printed, -2 if label == "Biggest single hop" else -3)
    assert printed == pytest.approx(measured), (
        f"{column} {label!r} reads {cell!r} on the slide but the log says {measured}"
    )


def test_solo_column_is_a_control_with_nothing_to_report(rows):
    solo = load("solo")
    assert number(rows["Hops"][0]) >= 0  # the table parsed
    assert sc.hops(solo) == 0
    # Solo has no agents to be busy, so those rows are an em dash, not a zero.
    line = SLIDES.read_text().split("# Honest scorecard", 1)[1]
    for label in ("Agent effort", "Latency (agents busy)", "Parallelism"):
        row = next(l for l in line.splitlines() if l.startswith(f"| {label} "))
        assert row.strip("|").split("|")[1].strip() == "—", (
            f"{label} shows a solo figure, but solo logs no hops to measure one from"
        )


def test_every_claim_slide_lists_the_scenario_tests_that_exist():
    """The test-name slide is a screenshot of the suite; keep it one."""
    listed = {
        line.strip()
        for line in SLIDES.read_text().splitlines()
        if re.fullmatch(r"(solo|hub|flat|edges)_[a-z0-9_]+", line.strip())
    }
    source = (ROOT / "tests" / "test_scenarios.py").read_text()
    defined = {
        m.group(1)
        for m in re.finditer(r"^def test_((?:solo|hub|flat|edges)_[a-z0-9_]+)\(", source, re.M)
    }
    assert listed == defined, (
        "slides.md and test_scenarios.py disagree:\n"
        f"  only on the slide: {sorted(listed - defined)}\n"
        f"  only in the suite: {sorted(defined - listed)}"
    )
