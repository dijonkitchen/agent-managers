"""Price quotes for a handful of symbols, served from a slow upstream.

This is the codebase the agents modify during the demo. Keep it small:
the point is the design decision, not the code.
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
