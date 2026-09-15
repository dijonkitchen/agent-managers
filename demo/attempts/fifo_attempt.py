"""What passed Archie's checklist and failed Desi's: a TTL cache with FIFO eviction.

Fresh within 5 seconds, capped at MAX entries, errors never stored. It
clears every constraint in TASK.md. It also evicts the symbol someone is
watching as soon as MAX unrelated symbols have been requested behind it,
because a hit does not make an entry any younger.

The fix is one line: move_to_end on a hit. Nobody asks for that line
until somebody asks who is looking at the screen.
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
        return hit[1]  # served, but stays exactly as old in the queue
    price = _upstream_quote(symbol)  # raises: nothing is stored
    _cache[symbol] = (now, price)
    while len(_cache) > MAX_ENTRIES:
        _cache.popitem(last=False)  # oldest inserted, not least recently used
    return price
