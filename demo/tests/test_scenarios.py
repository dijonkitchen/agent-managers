"""Each topology's strengths and weaknesses, as executable claims.

Runs against real logs in demo/runs/ when present, else the samples.
If a real run breaks one of these, that is a finding, not a flake.
"""

from pathlib import Path

import pytest

import scenarios as sc
from render_graph import read_jsonl

ROOT = Path(__file__).resolve().parents[1]

# A log captured before the hook stopped writing the lead's own SubagentStop
# records. Every predicate has to agree these are not coordination, or the
# solo control reads as having hops it could not have had.
WITH_SELF_EDGES = [
    {"ts": 100.0, "kind": "start", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 130.0, "kind": "report", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 145.0, "kind": "report", "from": "solo", "to": "solo", "chars": 0},
    {"ts": 160.0, "kind": "end", "from": "solo", "to": "solo", "chars": 0},
]


def test_self_edges_are_not_hops_for_any_predicate():
    assert sc.hops(WITH_SELF_EDGES) == 0
    assert sc.count(WITH_SELF_EDGES, "report") == 0
    assert sc.distinct_edges(WITH_SELF_EDGES) == 0
    assert sc.peer_edges(WITH_SELF_EDGES, lead="solo") == set()
    assert sc.work_seconds(WITH_SELF_EDGES) == 0.0
    assert sc.max_concurrent_delegations(WITH_SELF_EDGES, lead="solo") == 0
    # The session was still open that long, which is a different question.
    assert sc.wall_seconds(WITH_SELF_EDGES) == 60.0


# Two agents, one after the other, then both at once.
BUSY = [
    {"ts": 0.0, "kind": "start", "from": "lead", "to": "lead", "chars": 0},
    {"ts": 10.0, "kind": "spawn", "from": "lead", "to": "a", "chars": 1},
    {"ts": 30.0, "kind": "report", "from": "a", "to": "lead", "chars": 0},   # a busy 20s
    {"ts": 100.0, "kind": "spawn", "from": "lead", "to": "b", "chars": 1},   # lead sat 70s
    {"ts": 110.0, "kind": "message", "from": "lead", "to": "a", "chars": 1},
    {"ts": 130.0, "kind": "report", "from": "b", "to": "lead", "chars": 0},  # b busy 30s
    {"ts": 140.0, "kind": "report", "from": "a", "to": "lead", "chars": 0},  # a busy 30s
]


def test_busy_time_excludes_the_lead_sitting_on_the_baton():
    # Span is 130s, but 70s of it is the lead holding the work.
    assert sc.work_seconds(BUSY) == 130.0
    # a: 10-30 and 110-140. b: 100-130. Union = 20 + 40 = 60.
    assert sc.busy_seconds(BUSY, lead="lead") == 60.0


def test_agent_seconds_is_effort_and_busy_seconds_is_latency():
    # a 20 + 30, b 30 = 80 agent-seconds compressed into 60s of wall clock.
    assert sc.agent_seconds(BUSY, lead="lead") == 80.0
    assert sc.parallelism(BUSY, lead="lead") == 80.0 / 60.0


def test_a_run_with_nobody_working_is_not_parallel():
    assert sc.busy_seconds(WITH_SELF_EDGES, lead="solo") == 0.0
    assert sc.agent_seconds(WITH_SELF_EDGES, lead="solo") == 0.0
    assert sc.parallelism(WITH_SELF_EDGES, lead="solo") == 0.0


def load(name: str) -> list[dict]:
    real = ROOT / "runs" / f"{name}.jsonl"
    return read_jsonl(real if real.exists() else ROOT / "runs" / "samples" / f"{name}.jsonl")


@pytest.fixture(scope="module")
def solo():
    return load("solo")


@pytest.fixture(scope="module")
def hub():
    return load("hub")


@pytest.fixture(scope="module")
def flat():
    return load("flat")


# --- Solo: no coordination cost, no second opinion -------------------------

def test_solo_strength_zero_coordination_cost(solo):
    assert sc.hops(solo) == 0
    assert sc.prompt_chars(solo) == 0


def test_solo_weakness_nobody_checks_the_work(solo):
    assert sc.validation_rounds(solo, lead="solo") == 0
    assert sc.agents(solo) == {"solo"}


# --- Hub: star, validated, briefed; but sequential -------------------------

def test_hub_strength_every_hop_touches_the_lead(hub):
    assert sc.is_star(hub, lead="manny")
    assert sc.peer_edges(hub, lead="manny") == set()


def test_hub_strength_every_delegation_is_reported_back_and_validated(hub):
    assert sc.count(hub, "report") == sc.delegations(hub, lead="manny")
    assert sc.validation_rounds(hub, lead="manny") >= 1


def test_hub_strength_later_rounds_resume_agents_with_their_context(hub):
    # One cold spawn per agent; every later round is a message to a named
    # agent, which keeps its history instead of being re-briefed from zero.
    assert sc.count(hub, "spawn") <= len(sc.agents(hub) - {"manny"})
    assert sc.count(hub, "message") >= 1


def test_hub_strength_resuming_an_agent_is_cheaper_than_briefing_one(hub):
    """The saving is in the resume, not in the brief being small.

    The captured run's cold spawn of codie was 17,411 chars -- larger than
    anything the flat run sent in a single hop. What hub buys is that it pays
    that once per agent: its eight later rounds averaged ~2,975 chars against
    ~10,246 for the two cold briefs, because a resumed agent already holds
    the context.
    """
    assert sc.mean_chars(hub, "message") < sc.mean_chars(hub, "spawn")


def test_hub_weakness_the_lead_serializes_most_of_the_work(hub, flat):
    """Not strictly sequential, but close, and capped by the lead's attention.

    The captured hub run overlapped exactly one of manny's ten delegations --
    he resumed archie and codie ten seconds apart before either reported --
    so the peak was two in flight, not one. Every other round waited on a
    report. Flat had all three peers running from its first minute.
    """
    delegated = sc.delegations(hub, lead="manny")
    assert sc.validation_rounds(hub, lead="manny") >= delegated - 2
    assert sc.max_concurrent_delegations(hub, lead="manny") < sc.max_concurrent_delegations(
        flat, lead="referee"
    )


# --- Flat: parallel and fast; but chatty and unbounded ---------------------

def test_flat_strength_everyone_starts_at_once(flat):
    assert sc.max_concurrent_delegations(flat, lead="referee") == 3


def test_flat_strength_finishes_before_hub(flat, hub):
    """Measured on time attributable to agents, not on the session clock.

    Session spans are a dead heat near 4200s: all three runs were captured in
    one sitting and closed together. Hop spans say flat 983.0s against hub
    3100.3s, but 1504s of hub's is two gaps where Manny held the baton and
    nothing was delegated -- the operator, not the topology. Excluding the
    lead entirely: flat 871.7s against hub 1360.9s, a 1.6x margin rather
    than 3.2x, and the one this capture can actually support.
    """
    assert sc.busy_seconds(flat, lead="referee") < sc.busy_seconds(hub, lead="manny")


def test_flat_strength_is_parallelism_not_efficiency(flat, hub):
    """Flat wins on latency while spending the same effort.

    Total agent-seconds are within 12% -- hub 1399.2, flat 1233.6 -- so flat
    is not doing less work, it is doing it at once. Hub's effort/latency
    ratio is 1.03, which is serial; flat's is 1.42.
    """
    assert sc.parallelism(hub, lead="manny") < 1.1
    assert sc.parallelism(flat, lead="referee") > 1.3
    # Effort is comparable; latency is not.
    effort = sc.agent_seconds(flat, lead="referee") / sc.agent_seconds(hub, lead="manny")
    assert 0.8 < effort < 1.2


def test_flat_weakness_peers_talk_past_the_lead(flat):
    assert not sc.is_star(flat, lead="referee")
    assert len(sc.peer_edges(flat, lead="referee")) == 6  # every ordered pair of 3 peers


def test_flat_weakness_more_hops_and_more_context_than_hub(flat, hub):
    assert sc.hops(flat) > sc.hops(hub)
    assert sc.prompt_chars(flat) > sc.prompt_chars(hub)


def test_flat_weakness_coder_ships_before_researcher_answers(flat):
    assert sc.first_ts(flat, sender="codie") < sc.first_ts(flat, sender="archie")


# --- Across the three: paths grow with the square of the team --------------

def test_edges_grow_solo_to_hub_to_flat(solo, hub, flat):
    assert sc.distinct_edges(solo) < sc.distinct_edges(hub) < sc.distinct_edges(flat)
