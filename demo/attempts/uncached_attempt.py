"""The starting point: no cache at all.

Kept as an attempt so the scorecard still has its baseline row after
pricing.py grew a cache. Numbered by `constraints.CHECKS`, it passes
checks 2, 3 and 4 by doing nothing and fails check 1 for the same
reason. (TASK.md numbers its constraints differently: its constraint 1
is the 5s bound, which caching nothing satisfies trivially.)
"""

import random
import time

UPSTREAM_LATENCY_SECONDS = 0.5


def _upstream_quote(symbol: str) -> float:
    """Simulate a slow, rate-limited upstream price service."""
    time.sleep(UPSTREAM_LATENCY_SECONDS)
    if symbol not in {"AAPL", "GOOG", "MSFT", "NVDA"}:
        raise LookupError(f"unknown symbol: {symbol}")
    base = {"AAPL": 190.0, "GOOG": 140.0, "MSFT": 410.0, "NVDA": 120.0}[symbol]
    return round(base + random.uniform(-1.0, 1.0), 2)


def get_quote(symbol: str) -> float:
    """Return the current price for `symbol`."""
    return _upstream_quote(symbol)
