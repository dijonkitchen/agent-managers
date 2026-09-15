"""The TASK.md constraints as checks that run against any pricing module.

`CHECKS` is the four constraints as written. `DESI_CHECKS` is the fifth,
which is not in TASK.md: Desi proposed it after asking who is looking at
the screen. `ALL_CHECKS` is both.

A module qualifies if it exposes `get_quote`, `_upstream_quote`, and
`UPSTREAM_LATENCY_SECONDS`, the same shape as demo/target/pricing.py.
The harness replaces the upstream with a counter and freezes time so
each check is deterministic.
"""

import importlib
import time
from collections import Counter
from types import ModuleType

TTL_SECONDS = 5.0
MANY_SYMBOLS = 10_000
HOT_CHURN_SYMBOLS = 1_024  # more than any reasonable cache bound


class Harness:
    def __init__(self, mod: ModuleType, monkeypatch) -> None:
        mod = importlib.reload(mod)  # reset any module-level cache
        self.calls = 0
        self.per_symbol: Counter[str] = Counter()
        self.now = 1_000.0
        self.fail_next = False
        monkeypatch.setattr(mod, "UPSTREAM_LATENCY_SECONDS", 0)
        monkeypatch.setattr(mod, "_upstream_quote", self._upstream)
        monkeypatch.setattr(time, "monotonic", lambda: self.now)
        monkeypatch.setattr(time, "time", lambda: self.now)
        self.get = mod.get_quote

    def _upstream(self, symbol: str) -> float:
        self.calls += 1
        self.per_symbol[symbol] += 1
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


def hot_symbol_survives_churn(h: Harness) -> bool:
    """A symbol someone is actively watching is not evicted by churn.

    Desi's constraint, and not in TASK.md. The bounded-memory
    constraint is satisfied by any eviction policy, FIFO included.
    Under FIFO the symbol on screen is dropped by traffic for symbols
    nobody is looking at, so the person watching pays the upstream
    latency again every time the churn laps the cache. Time is frozen
    here, so one fetch is the correct answer.
    """
    h.get("AAPL")
    for i in range(HOT_CHURN_SYMBOLS):
        h.get(f"S{i}")
        h.get("AAPL")  # still on screen, still being watched
    return h.per_symbol["AAPL"] == 1


# TASK.md, as written.
CHECKS = {
    "1 caches repeats": caches_repeats,
    "2 refreshes after 5s": refreshes_after_ttl,
    "3 bounded memory": bounded_memory,
    "4 errors not cached": does_not_cache_errors,
}

# The constraint nobody wrote down.
DESI_CHECKS = {
    "5 watched symbol stays warm": hot_symbol_survives_churn,
}

ALL_CHECKS = CHECKS | DESI_CHECKS
