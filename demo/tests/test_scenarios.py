"""Each topology's strengths and weaknesses, as executable claims.

Runs against real logs in demo/runs/ when present, else the samples.
If a real run breaks one of these, that is a finding, not a flake.
"""

from pathlib import Path

import pytest

import scenarios as sc
from render_graph import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


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


def test_hub_strength_every_spawn_is_reported_back_and_validated(hub):
    assert sc.count(hub, "report") == sc.count(hub, "spawn")
    assert sc.validation_rounds(hub, lead="manny") >= 1


def test_hub_strength_briefs_are_small(hub, flat):
    assert sc.max_hop_chars(hub) < sc.max_hop_chars(flat)


def test_hub_weakness_work_is_sequential(hub):
    assert sc.max_concurrent_spawns(hub, lead="manny") == 1


# --- Flat: parallel and fast; but chatty and unbounded ---------------------

def test_flat_strength_everyone_starts_at_once(flat):
    assert sc.max_concurrent_spawns(flat, lead="referee") == 3


def test_flat_strength_finishes_before_hub(flat, hub):
    assert sc.wall_seconds(flat) < sc.wall_seconds(hub)


def test_flat_weakness_peers_talk_past_the_lead(flat):
    assert not sc.is_star(flat, lead="referee")
    assert len(sc.peer_edges(flat, lead="referee")) == 6  # every ordered pair of 3 peers


def test_flat_weakness_more_hops_and_more_context_than_hub(flat, hub):
    assert sc.hops(flat) > sc.hops(hub)
    assert sc.prompt_chars(flat) > sc.prompt_chars(hub)


def test_flat_weakness_coder_ships_before_researcher_answers(flat):
    assert sc.first_ts(flat, sender="rocky") < sc.first_ts(flat, sender="ivory")


# --- Across the three: paths grow with the square of the team --------------

def test_edges_grow_solo_to_hub_to_flat(solo, hub, flat):
    assert sc.distinct_edges(solo) < sc.distinct_edges(hub) < sc.distinct_edges(flat)
