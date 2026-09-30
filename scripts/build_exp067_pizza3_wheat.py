from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/exp066_liquidity_wool_flush/main.py"
TARGETS = (4, 6, 8, 10, 13, 16)


LAYER = r'''

# EXP067: first-three Pizza Shops early-route correction.  EXP054 normally
# adds a 13-cell strawberry tranche on day 11 even when the first three public
# shops all consume WHEAT/MILK/TOMATO and no shop consumes strawberry.  In that
# rare, fully observable regime, redirect a bounded number of those new seed
# buys and plant commands to wheat.  Existing crops, movement, harvesting,
# animals, sales, and every other shop regime inherit EXP066 exactly.
_E67_PARENT = exp063_wool_flush_agent
_E67_TARGET = __TARGET__
_E67_STATE = {}
_E67_REPORT = {"calls": 0, "commits": 0, "seed_units": 0, "plants": 0, "errors": 0}


def exp067_pizza3_wheat_agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    if step == 0:
        _E67_STATE[seat] = {"committed": False, "seed_units": 0, "plants": 0}
        _E67_REPORT.update(calls=0, commits=0, seed_units=0, plants=0, errors=0)
    _E67_REPORT["calls"] += 1
    parent = _E67_PARENT(observation, configuration)
    try:
        state = _E67_STATE.setdefault(seat, {"committed": False, "seed_units": 0, "plants": 0})
        shops = list(((observation.get("town") or {}).get("unlocked_shops") or []))
        if not state["committed"] and 216 <= step <= 239 and shops[:3] == ["PIZZA_SHOP"] * 3:
            state["committed"] = True
            _E67_REPORT["commits"] += 1
        if not state["committed"] or step > 287:
            return parent

        result = dict(parent)
        changed = False
        market = []
        for order in parent.get("market") or []:
            revised = list(order)
            if (
                len(revised) >= 3
                and revised[:2] == ["BUY_SEED", "STRAWBERRY"]
                and state["seed_units"] < _E67_TARGET
            ):
                quantity = max(0, int(revised[2]))
                if quantity <= _E67_TARGET - state["seed_units"]:
                    revised[1] = "WHEAT"
                    state["seed_units"] += quantity
                    _E67_REPORT["seed_units"] += quantity
                    changed = True
            market.append(revised)

        farmer = list(parent.get("farmer") or ["PASS"])
        hands = [list(command) for command in (parent.get("hands") or [])]
        commands = [farmer, *hands]
        for index, command in enumerate(commands):
            if state["plants"] >= _E67_TARGET:
                break
            if len(command) >= 2 and command[:2] == ["PLANT", "STRAWBERRY"]:
                commands[index] = ["PLANT", "WHEAT"]
                state["plants"] += 1
                _E67_REPORT["plants"] += 1
                changed = True

        if not changed:
            return parent
        result["market"] = market
        result["farmer"] = commands[0]
        result["hands"] = commands[1:]
        race = _RACE_STATE.get(seat)
        if race is not None and race.get("prev_action") is not None and race.get("step") == step:
            race["prev_action"] = result
        return result
    except Exception:
        _E67_REPORT["errors"] += 1
        return parent


exp067_pizza3_wheat_agent.telemetry = _E67_REPORT
agent = exp067_pizza3_wheat_agent
kaggle_submission_agent = agent
'''


source = SOURCE.read_text(encoding="utf-8")
for target in TARGETS:
    output = ROOT / f"experiments/exp067_pizza3_wheat{target}/main.py"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source + LAYER.replace("__TARGET__", str(target)), encoding="utf-8", newline="\n")
    compile(output.read_bytes(), str(output), "exec")
    print(output, output.stat().st_size)
