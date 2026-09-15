"""Score each caching attempt against the constraints.

This is the code-diff slide as a test. The first four checks are
TASK.md's, so they are what Archie validates against. The fifth is
Desi's, is not in the written task, and is the only one that tells
FIFO eviction apart from LRU.
"""

import pytest

import constraints as c
import fifo_attempt
import lru_attempt
import pricing
import ttl_attempt

EXPECTED = {
    #                                    repeats refresh bounded errors  watched
    "uncached (pricing)":                 (False, True,   True,   True,   False),
    "lru_cache (Codie, minute 1)":        (True,  False,  False,  True,   True),
    "ttl + FIFO (Archie's checklist)":    (True,  True,   True,   True,   False),
    "ttl + LRU (Archie and Desi)":        (True,  True,   True,   True,   True),
}
MODULES = {
    "uncached (pricing)": pricing,
    "lru_cache (Codie, minute 1)": lru_attempt,
    "ttl + FIFO (Archie's checklist)": fifo_attempt,
    "ttl + LRU (Archie and Desi)": ttl_attempt,
}


@pytest.mark.parametrize("attempt", list(EXPECTED), ids=list(EXPECTED))
@pytest.mark.parametrize("idx,check", list(enumerate(c.ALL_CHECKS.values())), ids=list(c.ALL_CHECKS))
def test_attempt_matches_expected_scorecard(attempt, idx, check, monkeypatch):
    got = check(c.Harness(MODULES[attempt], monkeypatch))
    assert got is EXPECTED[attempt][idx]


def test_only_ttl_lru_passes_every_constraint(monkeypatch):
    assert all(check(c.Harness(ttl_attempt, monkeypatch)) for check in c.ALL_CHECKS.values())


def test_reflex_answer_fails_freshness_and_bound(monkeypatch):
    assert not c.refreshes_after_ttl(c.Harness(lru_attempt, monkeypatch))
    assert not c.bounded_memory(c.Harness(lru_attempt, monkeypatch))


def test_desis_constraint_is_the_only_one_fifo_fails(monkeypatch):
    """Why Desi earns a seat: FIFO clears the whole written task."""
    assert all(check(c.Harness(fifo_attempt, monkeypatch)) for check in c.CHECKS.values())
    assert not c.hot_symbol_survives_churn(c.Harness(fifo_attempt, monkeypatch))


def test_desis_constraint_is_not_in_the_written_task():
    assert set(c.DESI_CHECKS) & set(c.CHECKS) == set()
    assert set(c.ALL_CHECKS) == set(c.CHECKS) | set(c.DESI_CHECKS)
