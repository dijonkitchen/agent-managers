"""Score each caching attempt against the four constraints.

This is the code-diff slide as a test: the reflex answer passes half,
the TTL-bounded cache passes all, and the uncached baseline passes
only the checks it satisfies by doing nothing.
"""

import pytest

import constraints as c
import lru_attempt
import pricing
import ttl_attempt
import uncached_attempt

EXPECTED = {
    #                          1 repeats  2 refresh  3 bounded  4 errors
    "uncached (baseline)": (False, True,  True,  True),
    "lru_cache (Codie, minute 1)": (True, False, False, True),
    "ttl + bounded (Archie's checklist)": (True, True, True, True),
}
MODULES = {
    "uncached (baseline)": uncached_attempt,
    "lru_cache (Codie, minute 1)": lru_attempt,
    "ttl + bounded (Archie's checklist)": ttl_attempt,
}


@pytest.mark.parametrize("attempt", list(EXPECTED), ids=list(EXPECTED))
@pytest.mark.parametrize("idx,check", list(enumerate(c.CHECKS.values())), ids=list(c.CHECKS))
def test_attempt_matches_expected_scorecard(attempt, idx, check, monkeypatch):
    got = check(c.Harness(MODULES[attempt], monkeypatch))
    assert got is EXPECTED[attempt][idx]


def test_archie_checklist_passes_every_constraint(monkeypatch):
    assert all(check(c.Harness(ttl_attempt, monkeypatch)) for check in c.CHECKS.values())


def test_reflex_answer_fails_freshness_and_bound(monkeypatch):
    assert not c.refreshes_after_ttl(c.Harness(lru_attempt, monkeypatch))
    assert not c.bounded_memory(c.Harness(lru_attempt, monkeypatch))


def test_shipped_pricing_module_passes_every_constraint(monkeypatch):
    """pricing.py is no longer the uncached baseline: it is the finished work."""
    try:
        assert all(check(c.Harness(pricing, monkeypatch)) for check in c.CHECKS.values())
    finally:
        # The harness leaves a fake-clock timestamp in the real module's cache,
        # which would look fresh to a later test reading a real clock.
        pricing.reset_cache()
