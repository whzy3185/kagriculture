import importlib
from pathlib import Path
import zlib

import pytest


@pytest.fixture
def modules(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return {name: importlib.import_module(name) for name in (
        "recover_public_sources", "evaluate_public_panel", "compare_selected_replays", "summarize_public_panel")}


def test_notebook_constant_recovery_does_not_execute_calls(modules):
    recovered = modules["recover_public_sources"].constants([
        "GOOD = 'literal'\nBAD = missing_function_that_must_not_run()\n"])
    assert recovered == {"GOOD": "literal"}


def test_payload_requires_complete_single_compressed_stream(modules):
    inflate = modules["recover_public_sources"].inflate
    payload = zlib.compress(b"example")
    assert inflate(payload) == b"example"
    for bad in (payload[:-1], payload + b"trailing"):
        with pytest.raises(ValueError):
            inflate(bad)


def test_failed_games_remain_in_public_comparison_denominator(modules):
    rows = [{"candidate": "a", "opponent": "b", "valid_terminal": False},
            {"candidate": "a", "opponent": "b", "valid_terminal": True}]
    assert modules["evaluate_public_panel"].summary(rows) == {"a vs b": {"games": 2, "valid": False}}


def test_market_fingerprint_preserves_order_slots(modules):
    key = modules["compare_selected_replays"].action_key
    a = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 1], ["SELL", "MILK", 1]]}
    b = {**a, "market": list(reversed(a["market"]))}
    assert key(a, "field") == key(b, "field")
    assert key(a, "market") != key(b, "market")


def test_empty_or_mixed_engine_panels_cannot_select_champion(modules):
    summarize = modules["summarize_public_panel"].summarize
    with pytest.raises(ValueError):
        summarize([])
    with pytest.raises(ValueError):
        summarize([{"engine_sha": "a", "evaluator_sha": "same"},
                   {"engine_sha": "b", "evaluator_sha": "same"}])
