import importlib
import json
from pathlib import Path

import pytest
from kaggle_environments.envs.kaggriculture import kaggriculture as engine


@pytest.fixture
def diagnostic(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("analyze_strategy_phases")


def test_phase_boundaries_match_executed_decisions(diagnostic):
    assert [diagnostic.phase(t) for t in (0, 71, 72, 143, 144, 179, 180, 718)] == [
        "0:72", "0:72", "72:144", "72:144", "144:180", "144:180", "180:360", "540:719"]
    for t in (-1, 719, 720):
        with pytest.raises(ValueError):
            diagnostic.phase(t)


def test_snapshot_counts_assets_without_pricing_as_terminal_cash(diagnostic):
    farm = engine._new_farm(10, 123)
    farm["tiles"][0][0] = engine._new_animal("COW", 0)
    private = engine._new_private()
    private["inventories"][0] = {"MILK": 2}
    private["shed"]["WHEAT"] = 3
    state = [{"observation": {"farms": [farm], "private": private}}]
    row = diagnostic.snapshot(state, 0)
    assert row["cash"] == 123
    assert row["tiles"] == {"COW": 1}
    assert row["empty_tiles"] == 24
    assert (row["carried_units"], row["shed_units"]) == (2, 3)


@pytest.mark.parametrize("crop", ["TOMATO", "STRAWBERRY"])
@pytest.mark.parametrize("fertilized,units", [(False, 1), (True, 2)])
def test_recurring_crop_has_four_production_events_under_ideal_service(crop, fertilized, units):
    # Isolate production arithmetic; free perfect service here is not an ROI model.
    tile = engine._new_plant(crop, 0, 24)
    farm = {"tiles": [[tile]]}
    events = []
    for day in range(20):
        tile["watered_today"] = True
        tile["fertilized_until_day"] = day if fertilized else -1
        engine._daily_refresh_plants(farm, day, 24)
        if tile["yield_units"]:
            events.append((day + 1, tile["yield_units"]))
        tile["yield_units"] = 0
    first, interval = engine.CROPS[crop]["first_yield_day"], engine.CROPS[crop]["interval"]
    assert events == [(first + i * interval, units) for i in range(4)]


def test_saved_phase_ledger_reconciles_both_seats():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "experiments/results/EXP-006-phase-audit.json").read_text())
    assert {(r["evaluation"]["seed"], r["evaluation"]["seat"]) for r in report["rows"]} == {
        (201, 0), (201, 1), (202, 0), (202, 1)}
    for row in report["rows"]:
        for seat in (0, 1):
            cash = 3000 + sum(f["cash_delta"] for f in row["flows"] if f["seat"] == seat)
            assert cash == row["snapshots"]["719"][seat]["cash"]


def test_summary_reproduces_saved_derived_evidence(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root / "scripts"))
    module = importlib.import_module("summarize_strategy_evidence")
    expected = json.loads((root / "experiments/results/STRATEGY-DEPTH-20260907.json").read_text())
    assert module.summarize({}) == expected
