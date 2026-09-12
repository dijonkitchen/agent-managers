"""Rocky's first attempt: the reflex answer.

Caches forever and without bound. Passes constraints 1 and 4, fails 2 and 3.
"""

import random
import time
from functools import lru_cache

UPSTREAM_LATENCY_SECONDS = 0.5


def _upstream_quote(symbol: str) -> float:
    time.sleep(UPSTREAM_LATENCY_SECONDS)
    if symbol not in {"AAPL", "GOOG", "MSFT", "NVDA"}:
        raise LookupError(f"unknown symbol: {symbol}")
    base = {"AAPL": 190.0, "GOOG": 140.0, "MSFT": 410.0, "NVDA": 120.0}[symbol]
    return round(base + random.uniform(-1.0, 1.0), 2)


@lru_cache(maxsize=None)
def get_quote(symbol: str) -> float:
    return _upstream_quote(symbol)
