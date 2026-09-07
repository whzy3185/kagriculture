"""Paired evaluation and exact official-interpreter telemetry for own candidates."""

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import time

import numpy as np
from kaggle_environments import __version__, make
from kaggle_environments.envs.kaggriculture import kaggriculture as engine

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_agent(path, disabled=()):
    spec = importlib.util.spec_from_file_location("isolated_agent", Path(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for flag in disabled:
        if not hasattr(module, flag):
            raise ValueError("Unknown ablation flag")
        setattr(module, flag, False)
    fn = module.agent

    def call(obs, config):
        return fn(obs, config) if fn.__code__.co_argcount >= 2 else fn(obs)

    return call


def run_game(candidate, opponent, seed, seat, disabled=()):
    policy = load_agent(candidate, disabled)
    rival = opponent if opponent in {"starter", "pass"} else load_agent(opponent)
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    counters = Counter()
    actions = Counter()
    latencies = []
    current = []
    original_interpreter = env.interpreter
    originals = {n: getattr(engine, n) for n in (
        "_apply_unit_action", "_commit_unit", "_do_hire", "_do_buy_land", "_drop_inventories_to_shed")}
    fills = Counter()

    def measured(obs, config):
        begin = time.perf_counter()
        try:
            result = policy(obs, config)
            json.dumps(result, allow_nan=False)
            if not isinstance(result, dict) or any(not isinstance(result.get(k), list) for k in ("farmer", "hands", "market")):
                counters["contract_errors"] += 1
            elif len(result["hands"]) != len(obs["farms"][seat]["hands"]) or len(result["market"]) > 10:
                counters["contract_errors"] += 1
            return result
        except Exception:
            counters["exceptions"] += 1
            raise
        finally:
            latencies.append(time.perf_counter() - begin)

    def is_ours(farm):
        return bool(current) and farm is current[0].observation.farms[seat]

    def stock(private):
        return sum(private["shed"].values()) + sum(sum(x.values()) for x in private["inventories"])

    def unit(farm, private, idx, action, board, day, tpd, capacity=100):
        ours = is_ours(farm)
        before = deepcopy((farm, private)) if ours else None
        answer = originals["_apply_unit_action"](farm, private, idx, action, board, day, tpd, capacity)
        if ours:
            op = action[0] if isinstance(action, list) and action else "MALFORMED"
            actions[op] += 1
            if op != "PASS" and before == (farm, private):
                counters["unit_noops"] += 1
            if op == "DROP":
                counters["overflow_units"] += max(0, stock(before[1]) - stock(private))
        return answer

    def commit(op, item, price, farm, private, market, capacity=100):
        result = originals["_commit_unit"](op, item, price, farm, private, market, capacity)
        if is_ours(farm):
            if result:
                fills[(op, item)] += 1
            else:
                counters["failed_market_attempts"] += 1
        return result

    def hire(farm, private, board, mult=1):
        before = len(farm["hands"])
        originals["_do_hire"](farm, private, board, mult)
        if is_ours(farm):
            fills[("HIRE", "")] += len(farm["hands"]) - before

    def land(farm, board):
        before = len(farm["unlocked_quadrants"])
        originals["_do_buy_land"](farm, board)
        if is_ours(farm):
            fills[("BUY_LAND", "")] += len(farm["unlocked_quadrants"]) - before

    def drop(private, capacity):
        ours = bool(current) and private is current[seat].observation.private
        before = stock(private) if ours else 0
        originals["_drop_inventories_to_shed"](private, capacity)
        if ours:
            counters["overflow_units"] += max(0, before - stock(private))

    def interpreter(state, environment):
        nonlocal current
        current = state
        if not state[0].observation.get("farms"):
            return original_interpreter(state, environment)
        fills.clear()
        a = state[seat].action or {}
        requested = Counter()
        for order in a.get("market", []):
            parsed = engine._parse_order(order)
            if parsed is None:
                counters["contract_errors"] += 1
            elif parsed["type"] in {"HIRE", "BUY_LAND"}:
                requested[(parsed["type"], "")] += 1
            else:
                requested[(parsed["type"], parsed["item"])] += parsed["remaining"]
        plant = Counter(x[1] for x in [a.get("farmer", []), *a.get("hands", [])] if len(x) >= 2 and x[0] == "PLANT")
        seeds = state[seat].observation.private["seeds"]
        counters["atomic_plant_rejections"] += sum(n for crop, n in plant.items() if n > seeds.get(crop, 0))
        result = original_interpreter(state, environment)
        counters["unfilled_requested_market_units"] += sum(max(0, n - fills[k]) for k, n in requested.items())
        return result

    engine._apply_unit_action, engine._commit_unit = unit, commit
    engine._do_hire, engine._do_buy_land = hire, land
    engine._drop_inventories_to_shed = drop
    env.interpreter = interpreter
    begin = time.perf_counter()
    try:
        players = [rival, rival]
        players[seat] = measured
        env.run(players)
    finally:
        for name, fn in originals.items():
            setattr(engine, name, fn)
    final = env.steps[-1]
    valid = all(s.status == "DONE" and isinstance(s.reward, (int, float)) for s in final) and len(env.steps) == 720
    ours, theirs = final[seat].reward, final[1 - seat].reward
    private = final[seat].observation.private
    row = {"seed": seed, "seat": seat, "opponent": Path(opponent).stem,
           "ours": ours, "theirs": theirs, "statuses": [s.status for s in final],
           "valid_terminal": valid, "faults": dict(counters), "actions": dict(actions),
           "calls": len(latencies), "runtime_mean": statistics.fmean(latencies) if latencies else None,
           "runtime_p95": float(np.quantile(latencies, .95)) if latencies else None,
           "runtime_p99": float(np.quantile(latencies, .99)) if latencies else None,
           "runtime_max": max(latencies, default=None), "wall_seconds": time.perf_counter() - begin,
           "terminal_carried_units": sum(sum(x.values()) for x in private["inventories"]),
           "terminal_shed_units": sum(private["shed"].values())}
    if valid:
        row["margin"] = ours - theirs
        row["points"] = 1. if ours > theirs else .5 if ours == theirs else 0.
    return row


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["opponent"]].append(row)
    results = {}
    for name, group in groups.items():
        valid = all(r["valid_terminal"] for r in group)
        errors = Counter()
        for r in group:
            errors.update(r["faults"])
        results[name] = {"games": len(group), "valid": valid, "faults": dict(errors)}
        if valid:
            margins = [r["margin"] for r in group]
            results[name].update(points=statistics.fmean(r["points"] for r in group),
                                 wins=sum(r["points"] == 1 for r in group),
                                 draws=sum(r["points"] == .5 for r in group),
                                 mean_bank=statistics.fmean(r["ours"] for r in group),
                                 mean_margin=statistics.fmean(margins),
                                 median_margin=statistics.median(margins),
                                 std_margin=statistics.stdev(margins) if len(margins) > 1 else 0.)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=Path, required=True)
    parser.add_argument("--opponents", nargs="+", required=True)
    parser.add_argument("--seed-start", type=int, required=True)
    parser.add_argument("--seeds", type=int, required=True)
    parser.add_argument("--disable", nargs="*", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.seeds < 1 or args.output.exists():
        raise SystemExit("Invalid count or output already exists")
    rows = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    progress = args.output.with_suffix(".progress.jsonl")
    with progress.open("x") as log:
        for opponent in args.opponents:
            for seed in range(args.seed_start, args.seed_start + args.seeds):
                for seat in (0, 1):
                    row = run_game(args.agent, opponent, seed, seat, args.disable)
                    rows.append(row)
                    log.write(json.dumps(row) + "\n")
                    log.flush()
                    print(json.dumps({k: row[k] for k in ("seed", "seat", "opponent", "ours", "theirs", "faults")}), flush=True)
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "agent_sha": sha(args.agent),
              "engine_version": __version__, "engine_sha": sha(engine.__file__),
              "evaluator_sha": sha(__file__), "disabled": args.disable,
              "opponent_hashes": {Path(p).stem: sha(p) for p in args.opponents if Path(p).is_file()},
              "seed_start": args.seed_start, "seed_count": args.seeds, "seat_swapped": True,
              "summary": summarize(rows), "rows": rows, "submission_approval": False}
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print(json.dumps(report["summary"], indent=2))
    if not all(r["valid_terminal"] for r in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
