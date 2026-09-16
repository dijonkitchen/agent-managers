"""Keep pricing's module-level cache from leaking between tests.

demo/tests/test_attempts.py scores demo/target/pricing through the harness,
which leaves entries stamped with the harness's frozen fake clock. On a host
with low uptime those stamps can still look fresh to the real time.monotonic(),
so a later test would be served a harness value instead of a real quote.
"""

import pytest

import pricing


@pytest.fixture(autouse=True)
def _clear_pricing_cache():
    pricing._cache.clear()
    yield
    pricing._cache.clear()
