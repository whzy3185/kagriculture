import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from kaggle_environments.agent import get_last_callable
from kaggle_environments.envs.kaggriculture import kaggriculture as engine

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("purchase_trigger", ROOT / "agents/candidates/exp20260908_01.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def setup(money):
    bot = policy.Chassis({0: [{"farmer": ["PASS"], "hands": [], "market": []}] * 719})
    called = []
    def requirements(view, route, start, end):
        called.append((start, end))
        return 100, {}
    bot._block_requirements = requirements
    bot.future_sells = lambda route, item, step: 0
    view = SimpleNamespace(money=money, shed={}, prices={"WHEAT": 35, "MILK": 160},
                           hires_today=2, quadrants=1, in_hands=lambda item: 0)
    return bot, view, called


def test_insufficient_current_purchase_triggers_existing_guard():
    bot, view, called = setup(18)
    bot._budget_guard({"market": [["BUY_PRODUCT", "WHEAT", 1]]}, view, 0, 198)
    assert called == [(198, 270)]


def test_affordable_nonboundary_turn_does_not_trigger():
    bot, view, called = setup(35)
    action = {"market": [["BUY_PRODUCT", "WHEAT", 1]]}
    bot._budget_guard(action, view, 0, 198)
    assert called == []
    assert action == {"market": [["BUY_PRODUCT", "WHEAT", 1]]}


def test_original_boundary_behavior_remains():
    bot, view, called = setup(1000)
    bot._budget_guard({"market": []}, view, 0, 216)
    assert called == [(216, 288)]


def test_estimate_tracks_sequential_hires_and_land_costs():
    bot, view, _ = setup(0)
    action = {"market": [["BUY_SEED", "WHEAT", 2], ["BUY_PRODUCT", "MILK", 2],
                         ["HIRE"], ["HIRE"], ["BUY_LAND"], ["BUY_ANIMAL", "COW", 1]]}
    assert bot._current_purchase_cost(action, view) == 1745


def test_no_purchase_and_empty_market_slots_do_not_trigger():
    bot, view, called = setup(0)
    bot._budget_guard({"market": [["SELL", "WHEAT", 0]]}, view, 0, 198)
    assert called == []


@pytest.mark.parametrize("seat", [0, 1])
def test_official_entrypoint_contract_on_both_seats(seat):
    path = ROOT / "agents/candidates/exp20260908_01.py"
    entry = get_last_callable(path.read_text(), path=str(path))
    obs = {"step": 0, "day": 0, "hour": 0, "player": seat,
           "farms": [engine._new_farm(10, 3000), engine._new_farm(10, 3000)],
           "private": engine._new_private(), "market": engine._new_market(),
           "town": {"unlocked_shops": []}}
    action = entry(obs, {})
    assert entry.__name__ == "agent"
    assert all(isinstance(action[k], list) for k in ("farmer", "hands", "market"))
    assert len(action["hands"]) == 0 and len(action["market"]) <= 10
    json.dumps(action, allow_nan=False)
