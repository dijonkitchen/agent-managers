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

# symbol -> (fetched_at, price), ordered least- to most-recently used.
_cache: OrderedDict[str, tuple[float, float]] = OrderedDict()


def _upstream_quote(symbol: str) -> float:
    """Simulate a slow, rate-limited upstream price service."""
    time.sleep(UPSTREAM_LATENCY_SECONDS)
    if symbol not in {"AAPL", "GOOG", "MSFT", "NVDA"}:
        raise LookupError(f"unknown symbol: {symbol}")
    base = {"AAPL": 190.0, "GOOG": 140.0, "MSFT": 410.0, "NVDA": 120.0}[symbol]
    return round(base + random.uniform(-1.0, 1.0), 2)


def get_quote(symbol: str) -> float:
    """Return the price for `symbol`, reusing a quote for up to TTL_SECONDS.

    Upstream is slow and rate-limited, so quotes are cached. The cache is
    capped at MAX_ENTRIES and evicts least-recently-used symbols, which
    keeps memory flat however many distinct symbols get asked for.
    """
    now = time.monotonic()
    cached = _cache.get(symbol)
    if cached is not None and now - cached[0] < TTL_SECONDS:
        _cache.move_to_end(symbol)
        return cached[1]
    price = _upstream_quote(symbol)  # raises before we store: errors are not cached
    _cache[symbol] = (now, price)
    _cache.move_to_end(symbol)  # plain assignment leaves an existing key in place
    while len(_cache) > MAX_ENTRIES:
        _cache.popitem(last=False)
    return price
