import pytest

import pricing


def test_known_symbol_returns_a_price(monkeypatch):
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    assert 180.0 < pricing.get_quote("AAPL") < 200.0


def test_unknown_symbol_raises(monkeypatch):
    monkeypatch.setattr(pricing, "UPSTREAM_LATENCY_SECONDS", 0)
    with pytest.raises(LookupError):
        pricing.get_quote("NOPE")
