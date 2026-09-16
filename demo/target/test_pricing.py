import importlib
import time

import pytest

import pricing


def test_known_symbol_returns_a_price(monkeypatch):
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    assert 180.0 < pricing.get_quote("AAPL") < 200.0


def test_unknown_symbol_raises(monkeypatch):
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    with pytest.raises(LookupError):
        pricing.get_quote("NOPE")


# --- caching behaviour -------------------------------------------------


class _Clock:
    """A fake monotonic clock; only moves when we tell it to."""

    def __init__(self, now: float = 1_000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class _CountingUpstream:
    """Stand-in for the slow upstream: counts calls, can be made to fail."""

    def __init__(self, price: float = 1.0) -> None:
        self.calls = 0
        self.price = price
        self.fail_next = False

    def __call__(self, symbol: str) -> float:
        self.calls += 1
        if self.fail_next:
            self.fail_next = False
            raise LookupError(f"upstream down: {symbol}")
        return self.price


@pytest.fixture
def cached(monkeypatch):
    """Reload pricing (dropping the module-level cache) and seam in fakes.

    Mirrors demo/tools/constraints.Harness: reload first, then patch, so the
    module-level cache starts empty and the clock/upstream are ours.
    """
    importlib.reload(pricing)
    clock = _Clock()
    upstream = _CountingUpstream()
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    monkeypatch.setattr(pricing, "_upstream_quote", upstream)
    monkeypatch.setattr(time, "monotonic", clock)
    yield pricing, clock, upstream
    importlib.reload(pricing)


def test_repeat_within_ttl_hits_upstream_once(cached):
    mod, _clock, upstream = cached
    first = mod.get_quote("AAPL")
    second = mod.get_quote("AAPL")
    assert upstream.calls == 1
    assert first == second


def test_quote_older_than_ttl_is_refetched(cached):
    mod, clock, upstream = cached
    mod.get_quote("AAPL")
    clock.advance(mod.TTL_SECONDS + 0.1)
    mod.get_quote("AAPL")
    assert upstream.calls == 2


def test_quote_just_inside_ttl_is_served_from_cache(cached):
    mod, clock, upstream = cached
    mod.get_quote("AAPL")
    clock.advance(mod.TTL_SECONDS - 0.1)
    mod.get_quote("AAPL")
    assert upstream.calls == 1


def test_quote_exactly_at_ttl_is_stale(cached):
    mod, clock, upstream = cached
    mod.get_quote("AAPL")
    clock.advance(mod.TTL_SECONDS)
    mod.get_quote("AAPL")
    assert upstream.calls == 2


def test_cache_is_bounded(cached):
    mod, _clock, upstream = cached
    for i in range(mod.MAX_ENTRIES + 1):
        mod.get_quote(f"S{i}")
    assert len(mod._cache) <= mod.MAX_ENTRIES
    before = upstream.calls
    mod.get_quote("S0")
    assert upstream.calls == before + 1


def test_recently_read_symbols_survive_eviction(cached):
    mod, _clock, upstream = cached
    mod.get_quote("AAPL")
    for i in range(mod.MAX_ENTRIES - 1):
        mod.get_quote(f"S{i}")
        mod.get_quote("AAPL")  # keep AAPL the most recently used entry
    before = upstream.calls
    mod.get_quote("AAPL")
    assert upstream.calls == before


def test_failed_upstream_is_not_cached(cached):
    mod, _clock, upstream = cached
    upstream.fail_next = True
    with pytest.raises(LookupError):
        mod.get_quote("AAPL")
    assert "AAPL" not in mod._cache
    before = upstream.calls
    assert mod.get_quote("AAPL") == upstream.price
    assert upstream.calls == before + 1


def test_clock_moving_backwards_refetches(cached):
    mod, clock, upstream = cached
    mod.get_quote("AAPL")
    clock.advance(-10.0)
    mod.get_quote("AAPL")
    assert upstream.calls == 2
