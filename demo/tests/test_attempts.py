"""Score each caching attempt against the four constraints.

This is the code-diff slide as a test: the reflex answer passes half,
the TTL-bounded cache passes all, and the untouched module passes only
the checks it satisfies by doing nothing.

The `shipped_*` modules are what the three captured runs really produced,
and the last three tests here are the scorecard's violations row.
"""

from collections import OrderedDict
from pathlib import Path

import pytest

import constraints as c
import lru_attempt
import pricing
import shipped_flat
import shipped_hub
import shipped_solo
import ttl_attempt

EXPECTED = {
    #                  1 repeats  2 refresh  3 bounded  4 errors
    "uncached (pricing)": (False, True,  True,  True),
    "lru_cache (Codie, minute 1)": (True, False, False, True),
    "ttl + bounded (Archie's checklist)": (True, True, True, True),
}
MODULES = {
    "uncached (pricing)": pricing,
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


# --- What the three captured runs actually shipped -------------------------

SHIPPED = {"solo": shipped_solo, "hub": shipped_hub, "flat": shipped_flat}


@pytest.mark.parametrize("run", list(SHIPPED), ids=list(SHIPPED))
def test_every_topology_shipped_a_passing_cache(run, monkeypatch):
    """The scorecard's "Violations at ship: 0, 0, 0" row.

    The task is built to bait `lru_cache`, and the deck used to predict that
    flat would ship it and solo would ship an unchecked reflex. Neither
    happened: on 2026-09-16 all three runs passed all four constraints,
    including the control that had nobody to check it.
    """
    assert all(check(c.Harness(SHIPPED[run], monkeypatch)) for check in c.CHECKS.values())


def test_no_topology_reached_for_lru_cache():
    for name, mod in SHIPPED.items():
        assert not hasattr(mod, "lru_cache"), name
        assert "lru_cache" not in Path(mod.__file__).read_text(), name


def test_the_three_runs_converged_on_the_same_design():
    """Same structure and the same two constants, one of which is arbitrary.

    Nothing in TASK.md names 128; `demo/runs/recorded/README.md` records that
    anything from 16 to 1024 passes every test. Three wirings of one model
    picking it anyway is the low-variance result, measured rather than cited.
    """
    for mod in SHIPPED.values():
        assert mod.TTL_SECONDS == 5.0
        assert mod.MAX_ENTRIES == 128
        assert isinstance(mod._cache, OrderedDict)
