"""What the HUB run shipped, verbatim from `hub-20260916-204627`.

Manny routing Archie then Codie, with eight validation rounds. The only
thing it has that the solo control does not is a `threading.Lock` -- which
nothing in TASK.md asks for and no test exercises. Kept here, rather than
merged into demo/target/pricing.py, so the task stays unsolved for the
next run.
"""

import random
import threading
import time
from collections import OrderedDict

UPSTREAM_LATENCY_SECONDS = 0.5

#: A served quote is never older than this.
TTL_SECONDS = 5.0
#: Hard cap on cached symbols, so memory stays bounded however many
#: distinct symbols are asked for. Upstream serves 4; 128 leaves ample
#: headroom for a few tens of KB.
MAX_ENTRIES = 128

#: symbol -> (monotonic timestamp taken before the fetch, price).
#: Module-level so `importlib.reload(pricing)` resets it.
_cache: "OrderedDict[str, tuple[float, float]]" = OrderedDict()
#: Guards `_cache` only. Never held across an upstream call: doing so would
#: serialise every caller behind one slow request.
_lock = threading.Lock()


def _upstream_quote(symbol: str) -> float:
    """Simulate a slow, rate-limited upstream price service."""
    time.sleep(UPSTREAM_LATENCY_SECONDS)
    if symbol not in {"AAPL", "GOOG", "MSFT", "NVDA"}:
        raise LookupError(f"unknown symbol: {symbol}")
    base = {"AAPL": 190.0, "GOOG": 140.0, "MSFT": 410.0, "NVDA": 120.0}[symbol]
    return round(base + random.uniform(-1.0, 1.0), 2)


def get_quote(symbol: str) -> float:
    """Return the current price for `symbol`, at most TTL_SECONDS old."""
    now = time.monotonic()

    with _lock:
        hit = _cache.get(symbol)
        if hit is not None and 0.0 <= now - hit[0] < TTL_SECONDS:
            _cache.move_to_end(symbol)  # read counts as recency
            return hit[1]

    # Outside the lock and before any mutation: if this raises, nothing was
    # ever written, so a failure is never cached.
    price = _upstream_quote(symbol)

    with _lock:
        # `now` is read before the fetch, so an entry is treated as older
        # than it is -- conservative on the freshness guarantee.
        _cache[symbol] = (now, price)
        _cache.move_to_end(symbol)  # assigning an existing key does not reorder
        while len(_cache) > MAX_ENTRIES:
            _cache.popitem(last=False)

    return price
