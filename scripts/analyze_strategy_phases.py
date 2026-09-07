"""Descriptive phase telemetry on frozen development games, not a new trial."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path

import experiment_eval as evaluator

ROOT = Path(__file__).resolve().parents[1]
BOUNDARIES = (0, 72, 144, 180, 360, 540, 719)


def phase(turn):
    if not 0 <= turn < 719:
        raise ValueError("Not an executed decision turn")
    return next(f"{a}:{b}" for a, b in zip(BOUNDARIES, BOUNDARIES[1:]) if a <= turn < b)


def snapshot(state, seat):
    obs = state[seat]["observation"]
    farm = obs["farms"][seat]
    tiles = [t for row in farm["tiles"] for t in row]
    counts = Counter(t.get("crop") or t.get("animal") or t.get("kind")
                     for t in tiles if isinstance(t, dict))
    private = obs["private"]
    return {"cash": farm["money"], "hands": len(farm["hands"]),
            "quadrants": len(farm["unlocked_quadrants"]), "tiles": dict(counts),
            "empty_tiles": sum(t is None for t in tiles),
            "carried_units": sum(sum(inv.values()) for inv in private["inventories"]),
            "shed_units": sum(private["shed"].values()),
            "shops": obs.get("town", {}).get("unlocked_shops", [])}


def run_diagnostic(candidate, opponent, seed, seat):
    engine = evaluator.engine
    original_make = evaluator.make
    originals = {name: getattr(engine, name) for name in ("_commit_unit", "_do_hire", "_do_buy_land")}
    captured, current, flows, quantities = [], [], Counter(), Counter()

    def identify(farm):
        state = current[0]
        player = next(p for p, f in enumerate(state[0].observation.farms) if f is farm)
        return player, phase(state[0].observation.day * 24 + state[0].observation.hour)

    def make(*args, **kwargs):
        env = original_make(*args, **kwargs)
        captured.append(env)
        interpreter = env.interpreter
        def observed(state, environment):
            current[:] = [state]
            return interpreter(state, environment)
        env.interpreter = observed
        return env

    def commit(op, item, price, farm, private, market, capacity=100):
        player, window = identify(farm)
        before = farm["money"]
        result = originals["_commit_unit"](op, item, price, farm, private, market, capacity)
        if result:
            flows[(player, window, op, item)] += farm["money"] - before
            quantities[(player, window, op, item)] += 1
        return result

    def spending(name, label):
        def call(farm, *args, **kwargs):
            player, window = identify(farm)
            before = farm["money"]
            result = originals[name](farm, *args, **kwargs)
            delta = farm["money"] - before
            flows[(player, window, label, "")] += delta
            quantities[(player, window, label, "")] += int(delta < 0)
            return result
        return call

    evaluator.make = make
    engine._commit_unit = commit
    engine._do_hire = spending("_do_hire", "HIRE")
    engine._do_buy_land = spending("_do_buy_land", "BUY_LAND")
    try:
        result = evaluator.run_game(candidate, opponent, seed, seat)
    finally:
        evaluator.make = original_make
        for name, function in originals.items():
            setattr(engine, name, function)
    env = captured[0]
    if not result["valid_terminal"]:
        raise ValueError("Diagnostic episode failed; do not aggregate")
    action_counts = Counter()
    for step_index, state in enumerate(env.steps[1:], 1):
        for p in (0, 1):
            action = state[p].action
            for command in [action["farmer"], *action["hands"]]:
                action_counts[(p, phase(step_index - 1), command[0])] += 1
    for p in (0, 1):
        observed_cash = env.steps[-1][p].observation.farms[p]["money"]
        reconciled_cash = 3000 + sum(v for k, v in flows.items() if k[0] == p)
        if abs(observed_cash - reconciled_cash) > 1e-8:
            raise ValueError("Cash flow does not reconcile")
    return {"evaluation": result,
            "snapshots": {str(t): [snapshot(env.steps[t], p) for p in (0, 1)]
                          for t in (*BOUNDARIES, 240)},
            "flows": [{"seat": p, "phase": w, "op": op, "item": item,
                       "cash_delta": value, "filled_units_or_events": quantities[(p, w, op, item)]}
                      for (p, w, op, item), value in sorted(flows.items())],
            "requested_unit_actions": [{"seat": p, "phase": w, "op": op, "count": n}
                                       for (p, w, op), n in sorted(action_counts.items())]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--opponent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite diagnostic evidence")
    candidate = ROOT / "agents/candidates/exp006_independent.py"
    baseline = ROOT / "experiments/results/EXP-006-development-full.json"
    old = json.loads(baseline.read_text())
    expected = {(r["seed"], r["seat"]): r for r in old["rows"] if r["opponent"] == args.opponent.stem}
    if evaluator.sha(candidate) != old["agent_sha"] or evaluator.sha(args.opponent) != old["opponent_hashes"][args.opponent.stem]:
        raise ValueError("Frozen policy mismatch")
    rows = []
    for seed in (201, 202):
        for seat in (0, 1):
            row = run_diagnostic(candidate, str(args.opponent), seed, seat)
            for key in ("ours", "theirs", "faults", "actions", "calls", "statuses"):
                if row["evaluation"][key] != expected[(seed, seat)][key]:
                    raise ValueError("Instrumentation altered recorded development result: " + key)
            rows.append(row)
            print(json.dumps({"seed": seed, "seat": seat, "margin": row["evaluation"]["margin"],
                              "cash_reconciled": True, "development_parity": True}), flush=True)
    report = {"timestamp": datetime.now(timezone.utc).isoformat(),
              "scope": "Descriptive remeasurement of four existing development games; not independent evidence",
              "agent_sha": evaluator.sha(candidate), "opponent_sha": evaluator.sha(args.opponent),
              "engine_version": evaluator.__version__, "engine_sha": evaluator.sha(evaluator.engine.__file__),
              "diagnostic_sha": evaluator.sha(__file__), "evaluator_sha": evaluator.sha(evaluator.__file__),
              "source_development_sha": evaluator.sha(baseline), "rows": rows}
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
