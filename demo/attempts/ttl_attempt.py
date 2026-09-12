"""What passed Ivory's checklist: a TTL-bounded LRU.

Fresh within 5 seconds, capped at MAX entries, errors never stored.
"""

import random
import time
from collections import OrderedDict

UPSTREAM_LATENCY_SECONDS = 0.5
TTL_SECONDS = 5.0
MAX_ENTRIES = 128

_cache: OrderedDict[str, tuple[float, float]] = OrderedDict()


def _upstream_quote(symbol: str) -> float:
    time.sleep(UPSTREAM_LATENCY_SECONDS)
    if symbol not in {"AAPL", "GOOG", "MSFT", "NVDA"}:
        raise LookupError(f"unknown symbol: {symbol}")
    base = {"AAPL": 190.0, "GOOG": 140.0, "MSFT": 410.0, "NVDA": 120.0}[symbol]
    return round(base + random.uniform(-1.0, 1.0), 2)


def get_quote(symbol: str) -> float:
    now = time.monotonic()
    hit = _cache.get(symbol)
    if hit is not None and now - hit[0] < TTL_SECONDS:
        _cache.move_to_end(symbol)
        return hit[1]
    price = _upstream_quote(symbol)  # raises: nothing is stored
    _cache[symbol] = (now, price)
    _cache.move_to_end(symbol)
    while len(_cache) > MAX_ENTRIES:
        _cache.popitem(last=False)
    return price
