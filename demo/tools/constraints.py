"""The four TASK.md constraints as checks that run against any pricing module.

A module qualifies if it exposes `get_quote`, `_upstream_quote`, and
`UPSTREAM_LATENCY_SECONDS`, the same shape as demo/target/pricing.py.
The harness replaces the upstream with a counter and freezes time so
each check is deterministic.
"""

import importlib
import time
from types import ModuleType

TTL_SECONDS = 5.0
MANY_SYMBOLS = 10_000


class Harness:
    def __init__(self, mod: ModuleType, monkeypatch) -> None:
        mod = importlib.reload(mod)  # reset any module-level cache
        self.calls = 0
        self.now = 1_000.0
        self.fail_next = False
        monkeypatch.setattr(mod, "UPSTREAM_LATENCY_SECONDS", 0)
        monkeypatch.setattr(mod, "_upstream_quote", self._upstream)
        monkeypatch.setattr(time, "monotonic", lambda: self.now)
        monkeypatch.setattr(time, "time", lambda: self.now)
        self.get = mod.get_quote

    def _upstream(self, symbol: str) -> float:
        self.calls += 1
        if self.fail_next:
            self.fail_next = False
            raise LookupError("upstream down")
        return 1.0

    def advance(self, seconds: float) -> None:
        self.now += seconds


def caches_repeats(h: Harness) -> bool:
    """Repeated calls within the TTL hit upstream once."""
    h.get("AAPL")
    h.get("AAPL")
    return h.calls == 1


def refreshes_after_ttl(h: Harness) -> bool:
    """A quote older than the TTL is fetched again."""
    h.get("AAPL")
    h.advance(TTL_SECONDS + 0.1)
    h.get("AAPL")
    return h.calls == 2


def bounded_memory(h: Harness) -> bool:
    """After many distinct symbols, the first one has been evicted."""
    for i in range(MANY_SYMBOLS):
        h.get(f"S{i}")
    before = h.calls
    h.get("S0")
    return h.calls == before + 1


def does_not_cache_errors(h: Harness) -> bool:
    """A failed upstream call is retried on the next request."""
    h.fail_next = True
    try:
        h.get("AAPL")
    except LookupError:
        pass
    before = h.calls
    h.get("AAPL")
    return h.calls == before + 1


CHECKS = {
    "1 caches repeats": caches_repeats,
    "2 refreshes after 5s": refreshes_after_ttl,
    "3 bounded memory": bounded_memory,
    "4 errors not cached": does_not_cache_errors,
}
