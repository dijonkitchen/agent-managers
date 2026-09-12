"""Acceptance tests for TASK.md. Run with: uv run pytest -m acceptance demo/target

Deselected by default so the baseline suite stays green before the
agents have done the work.
"""

import pytest

import constraints as c
import pricing

pytestmark = pytest.mark.acceptance


@pytest.mark.parametrize("name,check", list(c.CHECKS.items()), ids=list(c.CHECKS))
def test_constraint(name, check, monkeypatch):
    assert check(c.Harness(pricing, monkeypatch)), name
