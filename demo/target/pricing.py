"""Price quotes for a handful of symbols, served from a slow upstream.

This is the codebase the agents modify during the demo. Keep it small:
the point is the design decision, not the code.
"""

import random
import time
from collections import OrderedDict

UPSTREAM_LATENCY_SECONDS = 0.5
TTL_SECONDS = 5.0
MAX_ENTRIES = 128

# symbol -> (fetched_at, price), ordered oldest-used first so the least
# recently used entry is the one that gets evicted.
_cache: "OrderedDict[str, tuple[float, float]]" = OrderedDict()


def _upstream_quote(symbol: str) -> float:
    """Simulate a slow, rate-limited upstream price service."""
    time.sleep(UPSTREAM_LATENCY_SECONDS)
    if symbol not in {"AAPL", "GOOG", "MSFT", "NVDA"}:
        raise LookupError(f"unknown symbol: {symbol}")
    base = {"AAPL": 190.0, "GOOG": 140.0, "MSFT": 410.0, "NVDA": 120.0}[symbol]
    return round(base + random.uniform(-1.0, 1.0), 2)


def get_quote(symbol: str) -> float:
    """Return the current price for `symbol`, from cache when it is fresh.

    A cached price is served only while it is younger than `TTL_SECONDS`.
    The cache holds at most `MAX_ENTRIES` symbols, evicting the least
    recently used one, so memory stays flat however many symbols are asked
    for. An upstream failure propagates and leaves nothing behind.

    Not locked, and not thread-safe: `move_to_end` and `del` below both
    raise `KeyError` if another thread evicts the symbol between the
    `.get()` and those lines, so concurrent use crashes rather than
    merely double-fetching. A lock would serialise every symbol behind
    one 0.5s fetch, and no caller in this repo is threaded.
    """
    now = time.monotonic()
    cached = _cache.get(symbol)
    if cached is not None:
        fetched_at, price = cached
        if now - fetched_at < TTL_SECONDS:
            _cache.move_to_end(symbol)
            return price
        del _cache[symbol]  # already refused above; drop it so it frees a slot

    price = _upstream_quote(symbol)  # on failure, nothing is cached
    _cache[symbol] = (now, price)  # absent by now, so this appends at the end
    while len(_cache) > MAX_ENTRIES:
        _cache.popitem(last=False)
    return price


def cache_size() -> int:
    """Number of symbols currently held. Never exceeds `MAX_ENTRIES`."""
    return len(_cache)


def reset_cache() -> None:
    """Drop every cached quote. For tests and for a forced refresh."""
    _cache.clear()
