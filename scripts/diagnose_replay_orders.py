"""Replay recorded actions in the official engine and explain failed market units."""

import argparse
from copy import deepcopy
import json
from pathlib import Path

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as engine

ROOT = Path(__file__).resolve().parents[1]


def diagnose(case):
    data = json.loads((ROOT / case["raw_path"]).read_text())
    config = dict(data["configuration"], seed=data["info"]["seed"])
    env = make("kaggriculture", configuration=config)
    original_interpreter, original_commit = env.interpreter, engine._commit_unit
    current, failures = [], []
    def interpreter(state, environment):
        current[:] = [state]
        return original_interpreter(state, environment)
    def commit(op, item, price, farm, private, market, capacity=100):
        player = next(i for i, f in enumerate(current[0][0].observation.farms) if f is farm)
        before = {"cash": farm["money"], "shed_item": private["shed"].get(item, 0),
                  "shed_total": sum(private["shed"].values())}
        ok = original_commit(op, item, price, farm, private, market, capacity)
        if not ok and player == case["seat"]:
            obs = current[0][player].observation
            reason = "UNKNOWN"
            if op == "SELL" and before["shed_item"] == 0:
                reason = "EMPTY_SHED_ITEM"
            elif op.startswith("BUY") and before["cash"] < price:
                reason = "INSUFFICIENT_CASH"
            elif op in {"BUY_PRODUCT", "BUY_ANIMAL"} and before["shed_total"] >= capacity:
                reason = "SHED_CAPACITY"
            failures.append({"turn": obs.day * 24 + obs.hour, "op": op, "item": item,
                             "price": price, "reason": reason, **before})
        return ok
    env.interpreter, engine._commit_unit = interpreter, commit
    try:
        for t in range(719):
            env.step([deepcopy(data["steps"][t+1][p]["action"]) for p in (0, 1)])
            actual = env.steps[-1]
            for p in (0, 1):
                expected = data["steps"][t+1][p]["observation"]
                if actual[p].observation.farms != expected["farms"] or actual[p].observation.private != expected["private"]:
                    raise ValueError("Replay state mismatch at turn " + str(t))
    finally:
        engine._commit_unit = original_commit
    return {"seed": case["seed"], "seat": case["seat"], "opponent": case["opponent"],
            "full_farm_private_parity": True, "failures": failures}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.cases.read_text())
    results = [diagnose(c) for c in source["cases"]]
    with args.output.open("x") as handle:
        json.dump({"candidate": source["candidate"], "cases": results,
                   "scope": "Exact recorded-action replay, not a policy improvement experiment"}, handle, indent=2)
        handle.write("\n")
    print(json.dumps(results, indent=2))
