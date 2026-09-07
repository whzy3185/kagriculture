import importlib.util
import json
from pathlib import Path

from kaggle_environments.envs.kaggriculture import kaggriculture as engine

PATH = Path(__file__).resolve().parents[1] / "agents/candidates/exp006_independent.py"
spec = importlib.util.spec_from_file_location("independent", PATH)
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def observation(day=0, hour=0, money=3000, hands=()):
    farm = engine._new_farm(10, money)
    farm["hands"] = list(hands)
    private = engine._new_private()
    private["inventories"] += [{} for _ in hands]
    return {"player": 0, "day": day, "hour": hour,
            "farms": [farm, engine._new_farm(10, money)], "private": private,
            "market": engine._new_market(), "town": {"unlocked_shops": []}}


def test_price_function_matches_official_integer_quotes():
    for item in engine.PRODUCTS:
        for inventory in range(9000, 11001, 7):
            assert policy.price(item, inventory) == engine.market_price(item, inventory)


def test_sparse_price_overrides_match_official():
    params = engine._resolve_market_params({"MILK": {"above_target": .5}, "CARROT": {"below_func": "linear"}})
    for item in params:
        for inventory in (9000, 9999, 10000, 10001, 10100):
            assert policy.price(item, inventory, params) == engine.market_price(item, inventory, params)


def test_fallback_contract():
    assert policy.agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}


def test_new_crop_is_watered_before_night():
    obs = observation(hour=23)
    obs["farms"][0]["tiles"][4][4] = engine._new_plant("MELON", 0, 24)
    assert policy.agent(obs)["farmer"] == ["WATER"]


def test_no_last_hour_planting():
    obs = observation(hour=23)
    obs["private"]["seeds"]["MELON"] = 10
    assert policy.agent(obs)["farmer"][0] != "PLANT"


def test_shared_square_work_is_not_duplicated():
    obs = observation(hands=[[4, 4]])
    obs["farms"][0]["tiles"][4][4] = engine._new_plant("MELON", 0, 24)
    action = policy.agent(obs)
    assert action["farmer"] == ["WATER"]
    assert action["hands"][0] != ["WATER"]


def test_visible_seed_budget():
    obs = observation(hands=[[3, 4], [2, 4], [1, 4]])
    obs["private"]["seeds"]["MELON"] = 1
    action = policy.agent(obs)
    assert sum(a[0] == "PLANT" for a in [action["farmer"], *action["hands"]]) <= 1


def test_peak_day_water_precedes_harvest():
    obs = observation(day=4)
    tile = engine._new_plant("WHEAT", 0, 24)
    tile["yield_units"] = 3
    obs["farms"][0]["tiles"][4][4] = tile
    assert policy.agent(obs)["farmer"] == ["WATER"]
    tile["watered_today"] = True
    tile["yield_units"] = 4
    assert policy.agent(obs)["farmer"] == ["HARVEST"]


def test_final_turn_drop_can_sell_same_turn():
    obs = observation(day=29, hour=22)
    obs["private"]["inventories"][0] = {"MELON": 8}
    action = policy.agent(obs)
    assert action["farmer"] == ["DROP"]
    assert ["SELL", "MELON", 8] in action["market"]


def test_drop_will_not_discard_overflow():
    obs = observation(day=29, hour=22)
    obs["private"]["shed"]["WHEAT"] = 99
    obs["private"]["inventories"][0] = {"MELON": 8}
    action = policy.agent(obs)
    assert action["farmer"] == ["PLACE", "MELON", 1]


def test_purchases_do_not_borrow_unknown_sale_receipts():
    for money in (0, 10, 79, 80, 250, 500, 3000):
        obs = observation(money=money)
        obs["private"]["shed"]["MELON"] = 100
        action = policy.agent(obs)
        spent, hires, land = 0, 0, 0
        for order in action["market"]:
            if order[0] == "HIRE":
                spent += engine._hire_cost(hires)
                hires += 1
            elif order[0] == "BUY_LAND":
                spent += engine.LAND_PRICES[land]
                land += 1
            elif order[0] == "BUY_SEED":
                spent += engine.CROPS[order[1]]["seed"] * order[2]
        assert spent <= money
        assert len(action["market"]) <= 10
        json.dumps(action, allow_nan=False)
