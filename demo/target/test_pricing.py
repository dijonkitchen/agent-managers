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


@pytest.fixture(autouse=True)
def _clean_cache():
    """The default suite never reloads the module, so state leaks between tests."""
    pricing.reset_cache()
    yield
    pricing.reset_cache()


@pytest.fixture
def upstream(monkeypatch):
    """Replace the upstream with a call counter and freeze the clock."""
    calls = []
    now = [1_000.0]

    def fake(symbol):
        calls.append(symbol)
        if symbol == "BOOM":
            raise LookupError("upstream down")
        return 1.0

    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    monkeypatch.setattr(pricing, "_upstream_quote", fake)
    monkeypatch.setattr(time, "monotonic", lambda: now[0])
    return type("Upstream", (), {"calls": calls, "advance": staticmethod(lambda s: now.__setitem__(0, now[0] + s))})


def test_repeat_calls_within_ttl_hit_upstream_once(upstream):
    assert pricing.get_quote("AAPL") == pricing.get_quote("AAPL")
    assert upstream.calls == ["AAPL"]


def test_quote_is_refetched_once_it_exceeds_the_ttl(upstream):
    pricing.get_quote("AAPL")
    upstream.advance(pricing.TTL_SECONDS + 0.001)
    pricing.get_quote("AAPL")
    assert upstream.calls == ["AAPL", "AAPL"]


def test_quote_is_refetched_at_exactly_the_ttl(upstream):
    """Age must be strictly under the TTL: at 5.0s the quote is already too old."""
    pricing.get_quote("AAPL")
    upstream.advance(pricing.TTL_SECONDS)
    pricing.get_quote("AAPL")
    assert upstream.calls == ["AAPL", "AAPL"]


def test_quote_is_still_served_just_under_the_ttl(upstream):
    pricing.get_quote("AAPL")
    upstream.advance(pricing.TTL_SECONDS - 0.001)
    pricing.get_quote("AAPL")
    assert upstream.calls == ["AAPL"]


def test_distinct_symbols_are_cached_independently(upstream):
    pricing.get_quote("AAPL")
    pricing.get_quote("GOOG")
    pricing.get_quote("AAPL")
    assert upstream.calls == ["AAPL", "GOOG"]


def test_cache_never_grows_past_max_entries(upstream):
    for i in range(pricing.MAX_ENTRIES * 3):
        pricing.get_quote(f"S{i}")
    assert pricing.cache_size() == pricing.MAX_ENTRIES


def test_least_recently_used_symbol_is_evicted_first(upstream):
    for i in range(pricing.MAX_ENTRIES):
        pricing.get_quote(f"S{i}")
    pricing.get_quote("S0")  # S0 is now the most recently used; S1 is the oldest
    pricing.get_quote("NEW")
    del upstream.calls[:]
    pricing.get_quote("S0")
    pricing.get_quote("S1")
    assert upstream.calls == ["S1"]


def test_failed_upstream_call_is_not_cached(upstream):
    for _ in range(2):
        with pytest.raises(LookupError):
            pricing.get_quote("BOOM")
    assert upstream.calls == ["BOOM", "BOOM"]


def test_failure_does_not_evict_a_good_cached_quote(upstream):
    pricing.get_quote("AAPL")
    with pytest.raises(LookupError):
        pricing.get_quote("BOOM")
    del upstream.calls[:]
    pricing.get_quote("AAPL")
    assert upstream.calls == []


def test_stale_quote_is_never_served_when_the_refresh_fails(upstream, monkeypatch):
    """An expired entry is refused even when no fresh price can replace it.

    Not a freshness-vs-availability choice: the age check refuses a stale
    entry whether or not it was deleted, so there is no variant of this
    cache that would have served the old price here.
    """
    pricing.get_quote("AAPL")
    upstream.advance(pricing.TTL_SECONDS + 1)
    monkeypatch.setattr(pricing, "_upstream_quote", lambda s: (_ for _ in ()).throw(LookupError("down")))
    with pytest.raises(LookupError):
        pricing.get_quote("AAPL")
