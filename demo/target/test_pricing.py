import pytest

import constraints as c
import pricing


def test_known_symbol_returns_a_price(monkeypatch):
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    assert 180.0 < pricing.get_quote("AAPL") < 200.0


def test_unknown_symbol_raises(monkeypatch):
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    with pytest.raises(LookupError):
        pricing.get_quote("NOPE")


@pytest.fixture
def upstream(monkeypatch):
    """A counted, freezable stand-in for the slow upstream service."""
    return c.Harness(pricing, monkeypatch)


def test_repeat_within_the_ttl_hits_upstream_once(upstream):
    assert upstream.get("AAPL") == upstream.get("AAPL")
    assert upstream.calls == 1


def test_each_symbol_is_cached_separately(upstream):
    for symbol in ("AAPL", "GOOG", "AAPL", "GOOG"):
        upstream.get(symbol)
    assert upstream.calls == 2


def test_quote_is_refetched_once_it_turns_five_seconds_old(upstream):
    upstream.get("AAPL")
    upstream.advance(pricing.TTL_SECONDS - 0.1)
    upstream.get("AAPL")
    assert upstream.calls == 1
    upstream.advance(0.1)
    upstream.get("AAPL")
    assert upstream.calls == 2


def test_cache_never_grows_past_max_entries(upstream):
    for i in range(pricing.MAX_ENTRIES * 3):
        upstream.get(f"S{i}")
    assert len(pricing._cache) == pricing.MAX_ENTRIES


def test_eviction_drops_the_least_recently_used_symbol(upstream):
    upstream.get("AAPL")
    for i in range(pricing.MAX_ENTRIES - 1):
        upstream.get(f"S{i}")
    upstream.get("AAPL")  # a cache hit, so AAPL becomes the newest entry again
    before = upstream.calls
    upstream.get("NEW")  # fills the cache, evicting S0 as least recently used
    assert upstream.calls == before + 1
    upstream.get("AAPL")
    assert upstream.calls == before + 1
    upstream.get("S0")
    assert upstream.calls == before + 2


def test_failed_upstream_call_is_not_cached(upstream):
    upstream.fail_next = True
    with pytest.raises(LookupError):
        upstream.get("AAPL")
    assert upstream.get("AAPL") == 1.0
    assert upstream.calls == 2
