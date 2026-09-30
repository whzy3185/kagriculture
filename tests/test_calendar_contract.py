"""Model correctness tests; synthetic examples are not playing-strength evidence."""
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib.util
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kaggle_environments.agent import get_last_callable
from src.current_env import make_environment

spec = importlib.util.spec_from_file_location("calendar_builder", ROOT / "scripts/build_calendar_candidates.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

@lru_cache(None)
def namespace(number, modified):
    package, _ = builder.BASES[number]
    path = (ROOT / "agents/candidates" / ("exp20260930_calendar_" + number) / "main.py"
            if modified else ROOT / "benchmark_packages" / package / "main.py")
    return get_last_callable(path.read_text(), path=str(path)).__globals__

def observation(inventory=9850, shops=None):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    for y in range(5,10):
        for x in range(5,10):
            tiles[y][x] = "LOCKED"
    return {"step":432,"player":0,"town":{"unlocked_shops":shops or ["BAKERY"]*6},
            "market":{"inventory":{"TOMATO":inventory},"prices":{"TOMATO":60}},
            "farms":[{"tiles":tiles,"money":12000,"unlocked_quadrants":["NW","NE","SW"]},
                     {"tiles":[[None for _ in range(10)] for _ in range(10)]}],
            "private":{"seeds":{},"shed":{}}}

def tomato_price(inventory):
    if inventory < 10000:
        u = (10000-inventory)/200
        return max(1, round(60+24*(u+8*max(0,u-1)**2)))
    return max(1, round(60-36*math.sqrt((inventory-10000)/200)))

def independent_reference(obs, seventh_day):
    inv = float(obs["market"]["inventory"]["TOMATO"])
    shops = float(sum(s in ("PIZZA_SHOP","FARMERS_MARKET") for s in obs["town"]["unlocked_shops"]))
    their = [t for row in obs["farms"][1]["tiles"] for t in row if isinstance(t,dict) and t.get("crop")=="TOMATO"]
    revenue = 0
    for day in range(18,30):
        if day in (seventh_day,24): shops += .25
        inv -= 1+6*shops-2.4
        inv += .75*sum(day >= int(t["planted_day"])+8 for t in their)
        if day in (26,27,28,29):
            for _ in range(20):
                revenue += tomato_price(round(inv))
                inv += 1
    return revenue

def test_only_the_calendar_and_comment_change():
    for number,(package,expected) in builder.BASES.items():
        original = (ROOT / "benchmark_packages" / package / "main.py").read_bytes()
        modified = (ROOT / "agents/candidates" / ("exp20260930_calendar_"+number) / "main.py").read_bytes()
        assert hashlib.sha256(original).hexdigest() == expected
        assert modified == original.replace(builder.OLD,builder.NEW).replace(builder.OLD_COMMENT,builder.NEW_COMMENT)
        assert namespace(number,True)["_HD2_FUTURE"] == 0.0
        assert namespace(number,True)["_CXTB_MIN_REVENUE"] == 9000

def test_official_real_game_shop_calendar():
    env = make_environment(260930500)
    env.run(["pass","pass"])
    for day,count in ((0,0),(3,1),(18,6),(20,6),(21,7),(22,7),(24,8),(29,8)):
        assert len(env.steps[day*24][0].observation.town.unlocked_shops) == count
    assert [str(s.status) for s in env.state] == ["DONE","DONE"]

def test_expected_revenue_matches_independent_calendar_reference():
    for number in builder.BASES:
        for inventory in (9400,9650,9800,9950,10000,10200):
            for shops in (["BAKERY"]*6, ["PIZZA_SHOP"]*3+["YARN_STORE"]*3):
                obs = observation(inventory,shops)
                obs["farms"][1]["tiles"][0][0] = {"crop":"TOMATO","planted_day":16}
                frozen = deepcopy(obs)
                a=namespace(number,False)["_cxtb_expected_revenue"](obs)
                b=namespace(number,True)["_cxtb_expected_revenue"](obs)
                assert a == independent_reference(obs,22)
                assert b == independent_reference(obs,21)
                assert b >= a
                assert obs == frozen

def test_synthetic_boundary_can_flip_only_when_all_gates_pass():
    for number in builder.BASES:
        old,new = namespace(number,False),namespace(number,True)
        example = None
        for inventory in range(9400,10001):
            obs=observation(inventory)
            if old["_cxtb_expected_revenue"](obs)<9000<=new["_cxtb_expected_revenue"](obs):
                example=obs; break
        assert example is not None, "The exact model should have a synthetic calendar boundary"
        saved=[g["_IMPL"].chassis.routes for g in (old,new)]
        try:
            # Isolate physical/finance gates, not a valid full-game route test.
            for g in (old,new): g["_IMPL"].chassis.routes={}
            assert not old["_cxtb_qualifies"](example,None)
            assert new["_cxtb_qualifies"](example,None)
            blocked=deepcopy(example);blocked["farms"][0]["money"]=11999
            assert not new["_cxtb_qualifies"](blocked,None)
            blocked=deepcopy(example);blocked["private"]["seeds"]["TOMATO"]=1
            assert not new["_cxtb_qualifies"](blocked,None)
            blocked=deepcopy(example);blocked["farms"][0]["tiles"][5][5]=None
            assert not new["_cxtb_qualifies"](blocked,None)
        finally:
            for g,routes in zip((old,new),saved):g["_IMPL"].chassis.routes=routes
